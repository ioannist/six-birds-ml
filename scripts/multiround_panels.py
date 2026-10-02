"""Shared scientific sampling and scoring utilities for r8–r13."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import torch
from recombination_promotion.oldgame_ext.memory import VALUE_INDEX
from recombination_promotion.oldgame_ext.multiround import P, P_EQUAL, Episodes, enumerate_boards, kl_bits, oracle
from recombination_promotion.oldgame_ext.multiround_choice import ChoiceNetwork
from scripts import multiround_scoring as prior
from scripts import multiround_routing as routed
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'evidence/panels'
STEPS, PILOT_STEPS, BATCH, LR, WD, CURVE = (20000, 1000, 256, 0.003, 0.01, 250)
TEST_SEED, EQUAL_TEST_SEED, PREFIX_SEED = (2026100101, 2026100102, 2026100103)
RERENDER_SEED, SWAP_SEED = (TEST_SEED + 100, TEST_SEED + 101)
STARTS, LAWS = (('scratch', 'pretrained'), ('original', 'equal'))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_episodes(path: Path) -> Episodes:
    with np.load(path) as saved:
        return Episodes(*(saved[key] for key in ('boards', 'categories', 'modes', 'targets', 'lengths', 'rendering_seeds')))

def record_projection(board_ids: np.ndarray, render_seeds: np.ndarray, boards, *, active: np.ndarray | None=None) -> np.ndarray:
    """Execute the Stage-1 placement/order draws, omitting only text serialization."""
    if board_ids.shape != render_seeds.shape:
        raise ValueError('record projection shape differs')
    result = np.zeros((*board_ids.shape, 4, 2), dtype=np.int64)
    for position in np.ndindex(board_ids.shape):
        if active is not None and (not active[position]):
            continue
        board_id = int(board_ids[position])
        generator = np.random.default_rng(int(render_seeds[position]))
        choices = boards.placement(board_id, generator)
        order = list(range(3))
        generator.shuffle(order)
        order.append(3)
        result[position] = [(choices[index] // 6, choices[index] % 6) for index in order]
    return result

def episode_records(panel: Episodes, boards) -> np.ndarray:
    return record_projection(panel.boards, panel.rendering_seeds, boards, active=prior._active(panel))

def sum_targets(panel: Episodes, boards) -> np.ndarray:
    result = np.zeros((*panel.boards.shape, 5), dtype=np.int64)
    active = prior._active(panel)
    board_values = np.asarray(boards.boards, dtype=np.int64)
    result[active] = np.vectorize(VALUE_INDEX.__getitem__)(board_values[panel.boards[active]])
    return result

def _pathway_scenarios(boards) -> tuple[list[dict], list[dict]]:
    rerender_rng = np.random.default_rng(RERENDER_SEED)
    rerender = []
    for category in range(3):
        selected = rerender_rng.choice(boards.by_category[category], size=16, replace=False)
        for board in selected:
            future = [int(rerender_rng.choice(boards.by_category[1])) for _ in range(2)]
            future.append(int(rerender_rng.choice(boards.by_category[0])))
            rerender.append({'board': int(board), 'continuation': future, 'first_render_seeds': [int(rerender_rng.integers(0, 2 ** 63 - 1)) for _ in range(3)], 'future_render_seeds': [int(rerender_rng.integers(0, 2 ** 63 - 1)) for _ in range(3)]})
    swap_rng = np.random.default_rng(SWAP_SEED)
    swaps = []
    for _ in range(32):
        n, n_other = swap_rng.choice(boards.by_category[1], size=2, replace=False)
        swaps.append({'L': int(swap_rng.choice(boards.by_category[0])), 'H': int(swap_rng.choice(boards.by_category[2])), 'N': int(n), 'N_other': int(n_other)})
    return (rerender, swaps)

def verify_panels(output: Path) -> dict:
    manifest = json.loads((output / 'manifest.json').read_text())
    if manifest['test_seeds'] != {'natural': TEST_SEED, 'equal': EQUAL_TEST_SEED, 'prefix': PREFIX_SEED}:
        raise ValueError('choice independent test seeds differ')
    if manifest['Gate_A']['checkpoint_sha256'] != sha(routed.GATE / 'resolver.pt') or manifest['Gate_A']['audit_sha256'] != sha(routed.GATE / 'results.json') or manifest['panels']['rerender'].get('common_future_record_inputs') is not True:
        raise ValueError('choice panel authority differs')
    if manifest['panels']['rerender']['selection_seed'] != RERENDER_SEED or manifest['panels']['swaps']['selection_seed'] != SWAP_SEED:
        raise ValueError('choice pathway selection seeds differ')
    for name in ('test', 'equal_test'):
        panel = manifest['panels'][name]
        if panel['episode_sha256'] != sha(output / f'{name}.npz') or panel['record_sha256'] != sha(output / f'{name}_records.npy'):
            raise ValueError(f'choice {name} identity differs')
    for name, files in (('prefixes', (('record_sha256', 'prefix_records.npy'), ('length_sha256', 'prefix_lengths.npy'), ('metadata_sha256', 'prefix_metadata.json'))), ('rerender', (('record_sha256', 'rerender_records.npy'), ('scenario_sha256', 'rerender_scenarios.json'))), ('swaps', (('record_sha256', 'swap_records.npz'), ('scenario_sha256', 'swap_scenarios.json')))):
        for field, filename in files:
            if manifest['panels'][name][field] != sha(output / filename):
                raise ValueError(f'choice {name} identity differs: {field}')
    expected_rerender, expected_swaps = _pathway_scenarios(enumerate_boards())
    if json.loads((output / 'rerender_scenarios.json').read_text()) != expected_rerender or json.loads((output / 'swap_scenarios.json').read_text()) != expected_swaps:
        raise ValueError('choice deterministic pathway panels differ')
    return manifest

@torch.no_grad()
def predict_panel(model: ChoiceNetwork, records: np.ndarray, lengths: np.ndarray, *, batch_size: int=128) -> tuple[np.ndarray, np.ndarray]:
    probabilities, sum_predictions = ([], [])
    for offset in range(0, len(records), batch_size):
        section = torch.from_numpy(records[offset:offset + batch_size]).long()
        section_lengths = torch.from_numpy(lengths[offset:offset + batch_size]).long()
        trace = model(section, section_lengths, return_trace=True)
        probabilities.append(torch.softmax(trace['category_logits'], -1).numpy())
        sum_predictions.append(trace['hard_answers'].argmax(-1).numpy())
    return (np.concatenate(probabilities), np.concatenate(sum_predictions))

def prefix_score(probabilities: np.ndarray, lengths: np.ndarray, metadata: list[dict], *, equal: bool) -> dict:
    observed = probabilities[np.arange(len(lengths)), lengths - 1]
    by_run = {}
    for k in range(9):
        for first, mode in ((0, 0), (2, 1)):
            selected = [index for index, row in enumerate(metadata) if row['neutral_run'] == k and row['first'] == first]
            truth = np.asarray(P_EQUAL if equal else P[mode], dtype=float)
            tv = 0.5 * np.abs(observed[selected] - truth).sum(-1)
            by_run[f"{('L', 'H')[mode]}_N{k}"] = {'count': len(selected), 'maximum_TV': float(tv.max()), 'mean_TV': float(tv.mean())}
    k1 = [index for index, row in enumerate(metadata) if row['neutral_run'] == 1]
    witness_loss = float(np.mean([kl_bits(P_EQUAL if equal else P[0 if metadata[index]['first'] == 0 else 1], tuple(map(float, observed[index]))) for index in k1]))
    witness_tv = float(np.mean([0.5 * np.abs(observed[left] - observed[right]).sum() for left, right in zip(k1[:32], k1[32:], strict=True)]))
    cases = {'L_single_round': by_run['L_N0'], 'H_single_round': by_run['H_N0']}
    for k in range(1, 9):
        left, right = (by_run[f'L_N{k}'], by_run[f'H_N{k}'])
        cases[f'N_run_{k}'] = {'count': left['count'] + right['count'], 'maximum_TV': max(left['maximum_TV'], right['maximum_TV']), 'mean_TV': (left['mean_TV'] + right['mean_TV']) / 2}
    return {'rows': by_run, 'cases': cases, 'maximum_TV': max((row['maximum_TV'] for row in by_run.values())), 'witness_excess_bits': witness_loss, 'witness_recovery_fraction': None if equal else 1 - witness_loss / oracle()['witness_JS_bits'], 'witness_pair_mean_prediction_TV': witness_tv}

def rerender_score(model: ChoiceNetwork, records: np.ndarray) -> dict:
    probabilities, sums = predict_panel(model, records, np.full(len(records), 4, dtype=np.int64))
    grouped = probabilities.reshape(48, 3, 4, 3)
    tv = 0.5 * np.abs(grouped - grouped[:, :1]).sum(-1)
    answers = sums.reshape(48, 3, 4, 5)
    same_A = int((answers != answers[:, :1]).sum())
    return {'boards': 48, 'renderings': 144, 'future_continuation_rounds': 3, 'A_answer_mismatched_components': same_A, 'current_maximum_TV': float(tv[:, :, 0].max()), 'continuation_maximum_TV': float(tv[:, :, 1:].max()), 'maximum_TV': float(tv.max()), 'pass': bool(same_A == 0 and tv.max() <= 0.02)}

def _tv(value: np.ndarray, truth) -> float:
    return float(0.5 * np.abs(value - np.asarray(truth, dtype=float)).sum())

@torch.no_grad()
def swap_score(model: ChoiceNetwork, board_ids: np.ndarray, records: np.ndarray, scenarios: list[dict], *, equal: bool) -> dict:
    tensors = torch.from_numpy(records).long()
    _, answers, raw = model.round_interfaces(tensors)
    interfaces = {int(board): (answers[index:index + 1], raw[index:index + 1]) for index, board in enumerate(board_ids)}

    def step(board: int, state=None, *, a_board=None, raw_board=None):
        a = interfaces[int(board if a_board is None else a_board)][0]
        r = interfaces[int(board if raw_board is None else raw_board)][1]
        logits, new_state = model.upper_step(a, r, state)
        return (torch.softmax(logits, -1)[0].numpy(), new_state)
    cases = {name: [] for name in ('reset_L', 'set_H', 'neutral_N', 'same_category_substitution', 'upper_state_exchange_same_N', 'A_swap_exact_row', 'raw_swap_stability', 'raw_swap_exact_row', 'both_swap_exact_row', 'A_swap_effect', 'raw_swap_effect', 'neutral_A_swap_stability', 'neutral_raw_swap_stability')}
    for scenario in scenarios:
        l, h, n, n_other = (scenario[key] for key in ('L', 'H', 'N', 'N_other'))
        p0, p1 = (P_EQUAL, P_EQUAL) if equal else P
        l_row, l_state = step(l)
        h_row, h_state = step(h)
        n_l, n_l_state = step(n, l_state)
        n_h, n_h_state = step(n, h_state)
        cases['neutral_N'].extend((_tv(n_l, p0), _tv(n_h, p1)))
        exchanged_l, _ = step(n, h_state)
        exchanged_h, _ = step(n, l_state)
        cases['upper_state_exchange_same_N'].extend((_tv(exchanged_l, p1), _tv(exchanged_h, p0)))
        for prior_state in (None, l_state, h_state, n_l_state, n_h_state):
            row_l, _ = step(l, prior_state)
            row_h, _ = step(h, prior_state)
            cases['reset_L'].append(_tv(row_l, p0))
            cases['set_H'].append(_tv(row_h, p1))
        for prior_state, truth in ((l_state, p0), (h_state, p1), (n_l_state, p0), (n_h_state, p1)):
            baseline, _ = step(n, prior_state)
            alternative, _ = step(n_other, prior_state)
            only_a, _ = step(n, prior_state, a_board=n_other)
            only_raw, _ = step(n, prior_state, raw_board=n_other)
            cases['same_category_substitution'].append(_tv(alternative, baseline))
            cases['neutral_A_swap_stability'].append(_tv(only_a, baseline))
            cases['neutral_raw_swap_stability'].append(_tv(only_raw, baseline))
            cases['neutral_N'].append(_tv(baseline, truth))
        for source, opposite, baseline_truth, opposite_truth in ((l, h, p0, p1), (h, l, p1, p0)):
            baseline, _ = step(source)
            a_changed, _ = step(source, a_board=opposite)
            raw_changed, _ = step(source, raw_board=opposite)
            both_changed, _ = step(source, a_board=opposite, raw_board=opposite)
            cases['A_swap_exact_row'].append(_tv(a_changed, opposite_truth))
            cases['raw_swap_stability'].append(_tv(raw_changed, baseline))
            cases['raw_swap_exact_row'].append(_tv(raw_changed, opposite_truth))
            cases['both_swap_exact_row'].append(_tv(both_changed, opposite_truth))
            cases['A_swap_effect'].append(_tv(a_changed, baseline))
            cases['raw_swap_effect'].append(_tv(raw_changed, baseline))
            cases['raw_swap_stability'].append(_tv(raw_changed, baseline_truth))
    results = {name: {'count': len(values), 'maximum_TV': max(values), 'mean_TV': float(np.mean(values))} for name, values in cases.items()}
    return {'cases': results, 'natural_swap_pass': all((results[name]['maximum_TV'] <= 0.02 for name in ('reset_L', 'set_H', 'neutral_N', 'same_category_substitution', 'upper_state_exchange_same_N')))}
