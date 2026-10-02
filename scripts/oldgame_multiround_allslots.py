"""Registered all-slot predictive study; no training at import time."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import warnings
from pathlib import Path
from recombination_promotion.public_paths import public_path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from recombination_promotion.oldgame_ext.memory import VALUE_INDEX
from recombination_promotion.oldgame_ext.multiround import enumerate_boards, load_frozen_A
from recombination_promotion.oldgame_ext.multiround_allslots import (
    AllSlotsNetwork, CoverageSampler, Episodes, ExecutedOracle, ROW_FLOAT, VALUES36, check_law,
    eligible_pairs, mode_blind_row, oracle_rows, sample_episodes,
    verify_panel,
)
from scripts import multiround_panels as choice


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/phase11/oldgame_memory/multiround/study_r10_allslots"
SPEC = OUTPUT / "specification.md"
ARMS = ("free", "free_a", "a_forced")
LAWS = ("original", "equal")
SEEDS = (0, 1, 2)
AUDITS = (0, 1000, 2000, 5000, 10000, 15000, 20000)
STREAM_SEED = 2026101001
TEST_SEED = 2026101002
PROBE_SEED = 2026101003
PAIR_LIMIT = 0.05
SMOKE_ROOT = public_path("build/oldgame_ext/r10_smoke")
DEVICE = torch.device("cpu")
EQUAL_TV_LIMIT = .02
MINIMUM_ACCURATE_PAIRS = 20
INTERCHANGE_PAIRS = 1024
DECODER_RCOND = 1e-7  # Discard numerical rank below float32 carrier precision.
specification = OUTPUT / "analysis_specification.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def source_identities() -> dict:
    names = ("src/recombination_promotion/oldgame_ext/multiround_allslots.py",
             "src/recombination_promotion/oldgame_ext/multiround.py",
             "src/recombination_promotion/oldgame_ext/multiround_choice.py",
             "scripts/oldgame_multiround_allslots.py",
             "scripts/multiround_panels.py", "scripts/oldgame_allslots_execution.py",
             "scripts/oldgame_multiround_jagged.py",
             "src/recombination_promotion/oldgame_ext/multiround_jagged.py")
    return {name: sha(ROOT / name) for name in names}


def text_rules() -> dict:
    text = SPEC.read_text()
    return {
        "claims_verbatim": text.split("### Three claims to register\n", 1)[1].split(
            "\n### Smallest B change", 1)[0].strip(),
        "outcome_table_verbatim": text.split("### Outcome-to-conclusion rules\n", 1)[1].split(
            "\nThe deterministic relation", 1)[0].strip(),
        "scope_verbatim": text.split("**Scope of the answer.** ", 1)[1].split("\n\n", 1)[0],
    }


def _board_split(boards) -> dict:
    """Preserve one representative of every Q/slot/value in training."""

    rng = np.random.default_rng(2026101004)
    required = set()
    by_q = CoverageSampler(boards)
    for q in range(3):
        for group in by_q.by_pair[q]:
            required.add(int(group[0]))
    all_ids = np.arange(len(boards.boards), dtype=np.int64)
    remaining = np.asarray([i for i in all_ids if i not in required], dtype=np.int64)
    rng.shuffle(remaining)
    train = np.asarray(sorted(required) + remaining[:19_548 - len(required)].tolist())
    heldout = remaining[19_548 - len(required):]
    if len(train) != 19_548 or len(heldout) != len(all_ids) - len(train):
        raise ValueError("board split size differs")
    if any(len(x) != 150 for x in CoverageSampler(boards, train).pairs):
        raise ValueError("training board coverage differs")
    return {"train_board_ids": train.tolist(), "heldout_board_ids": heldout.tolist(),
            "selection_seed": 2026101004, "required_representatives": len(required)}


def _probe_split(boards, board_split: dict) -> dict:
    rng = np.random.default_rng(PROBE_SEED)
    train_pool = np.asarray(board_split["train_board_ids"], dtype=np.int64)
    held_pool = np.asarray(board_split["heldout_board_ids"], dtype=np.int64)
    required = set()
    for slot in range(5):
        for value in VALUES36:
            candidate = [i for i in train_pool if boards.boards[int(i)][slot] == value]
            required.add(int(candidate[0]))
    others = np.asarray([i for i in train_pool if i not in required], dtype=np.int64)
    rng.shuffle(others)
    rng.shuffle(held_pool)
    train = np.asarray(sorted(required) + others[:2048 - len(required)].tolist())
    heldout = held_pool[:512]
    rare = sorted({int(next(i for i in train_pool if boards.boards[int(i)][slot] == value))
                   for slot in range(5) for value in VALUES36 if value >= 28})
    return {"train_board_ids": train.tolist(), "heldout_board_ids": heldout.tolist(),
            "train_render_seeds": rng.integers(0, 2**63 - 1, len(train),
                                               dtype=np.int64).tolist(),
            "heldout_render_seeds": rng.integers(0, 2**63 - 1, len(heldout),
                                                 dtype=np.int64).tolist(),
            "rare_board_ids": np.repeat(rare, 20).tolist(),
            "rare_render_seeds": rng.integers(0, 2**63 - 1, len(rare) * 20, dtype=np.int64).tolist(),
            "recurrent_context": {"seed": 2026101012, "rounds": 12,
                                  "public_queries": "seeded_uniform_all_five"}}


def _panel(sampler: CoverageSampler, count: int, rounds: int, seed: int, equal: bool):
    return sample_episodes(sampler, count, rounds, seed, equal=equal)


def save_panel(path: Path, panel) -> None:
    np.savez_compressed(path, **vars(panel))


def load_panel(path: Path):
    from recombination_promotion.oldgame_ext.multiround_allslots import Episodes

    with np.load(path) as data:
        return Episodes(*(data[key] for key in ("boards", "queries", "targets",
                                                 "lengths", "rendering_seeds",
                                                 "last_nonzero")))


def register() -> dict:
    if (OUTPUT / "registration.json").exists():
        raise ValueError("r10 registration already exists")
    boards = enumerate_boards()
    law = check_law()
    split = _board_split(boards)
    train_sampler = CoverageSampler(boards, np.asarray(split["train_board_ids"]))
    test_sampler = CoverageSampler(boards, np.asarray(split["heldout_board_ids"]))
    frequencies = train_sampler.conditional_frequencies()
    if any(len(x) != 150 for x in train_sampler.pairs):
        raise ValueError("150-pair training coverage differs")
    if min(value for q in frequencies for row in q for value in row if value) < 1 / 300:
        raise ValueError("declared conditional coverage bound fails")
    output = OUTPUT
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "board_split.json", split)
    probe = _probe_split(boards, split)
    write_json(output / "probe_split.json", probe)
    write_json(output / "interchange_pairs.json", select_pair_ids(boards, split))
    table = {str(q): [[str(value) for value in row] for row in frequencies[q]]
             for q in range(3)}
    write_json(output / "conditional_frequency.json", table)
    panels = {}
    for label, sampler, count in (("natural", train_sampler, 5000),
                                  ("heldout_board", test_sampler, 1000),
                                  ("blind_fit", train_sampler, 2048)):
        for law_name in LAWS:
            path = output / f"{label}_{law_name}.npz"
            panel = _panel(sampler, count, 12,
                           TEST_SEED + {"natural": 0, "heldout_board": 10,
                                        "blind_fit": 20}[label] + (law_name == "equal"),
                           law_name == "equal")
            verify_panel(panel, sampler, equal=law_name == "equal")
            save_panel(path, panel)
            panels[path.name] = sha(path)
            if label == "natural":
                rng = np.random.default_rng(TEST_SEED + 30 + (law_name == "equal"))
                rendered = Episodes(panel.boards.copy(), panel.queries.copy(),
                                    panel.targets.copy(), panel.lengths.copy(),
                                    rng.integers(0, 2**63 - 1, panel.boards.shape,
                                                 dtype=np.int64),
                                    panel.last_nonzero.copy())
                path = output / f"rerender_{law_name}.npz"
                save_panel(path, rendered)
                panels[path.name] = sha(path)
    from scripts import oldgame_allslots_execution as execution
    first_batches = {}
    for law_name in LAWS:
        for seed in SEEDS:
            stream = execution.DeviceCoverageStream(execution.r11.BoardTables(DEVICE, boards),
                train_sampler, seed, equal=law_name == "equal")
            stream.draw()
            first_batches[f"{law_name}_seed{seed}"] = stream.rolling.hex()
    _, source = load_frozen_A(ROOT)
    rules = text_rules()
    row = {"role": "r10_allslots_registered", "spec_sha256": sha(SPEC), **rules,
           "source_A": source, "board_split_sha256": sha(output / "board_split.json"),
           "calibration_specification_sha256": sha(specification),
           "interchange_pairs_sha256": sha(output / "interchange_pairs.json"),
           "intervention_settings": intervention_settings(),
           "probe_split_sha256": sha(output / "probe_split.json"),
           "frequency_sha256": sha(output / "conditional_frequency.json"),
           "panel_sha256": panels, "law": law,
           "source_identities": source_identities(),
           "first_stream_batch_sha256": first_batches,
           "first_stream_batch_device": DEVICE.type,
           "board_counts_by_Q": [8115, 8140, 8180],
           "supported_pairs_by_Q": [len(x) for x in train_sampler.pairs],
           "conditional_frequency_table": table,
           "criteria": {"natural_and_covered_KL_fraction_of_blind": 0.10,
                        "constructed_maximum_TV": 0.05,
                        "donor_follow": 0.80, "positive_donor_follow": 0.95,
                        "null_donor_follow": 0.20,
                        "probe_positive_accuracy": 0.99,
                        "minimum_evaluation_cell_observations": 20,
                        "futility_gap_fraction": 0.10, "equal_law_TV": EQUAL_TV_LIMIT,
                        "minimum_accurate_interchange_pairs": MINIMUM_ACCURATE_PAIRS},
           "settings": {"steps": 20000, "batch": 256, "lr": .003,
                        "weight_decay": .01, "rounds": 8, "test_rounds": 12,
                        "audits": AUDITS, "arms": ARMS, "laws": LAWS, "seeds": SEEDS,
                        "stream_seed_base": STREAM_SEED, "test_seed": TEST_SEED,
                        "probe_seed": PROBE_SEED, "device_default": "cuda", "precision": "float32",
                        "maximum_processes": 5, "CPU_threads_per_process": 1,
                        "execution_widths": {"free": 3, "free_a": 3, "a_forced": 1},
                        "linear_fit_device": "cpu", "MLP_fit_device": "audit_device",
                        "linear_settings": {"C": 10, "class_weight": "balanced", "tol": 1e-5,
                                            "max_iter": 5000, "standardization": "training_only"}},
           "choices": [
               "The first board category is uniform; later categories are sampled from the exact queried row.",
               "Training uses a fixed seeded online board/query/render stream; board identities are "
               "restricted to the registered 19,548-board training pool.",
               "The held-out-board panel uses the disjoint 4,887-board pool; a separate natural panel "
               "uses training boards and independent rendering seeds. The rerender panel repeats "
               "those board/query identities with new rendering seeds; the mode-blind row is fitted "
               "on a separate registered training episode panel.",
               "The free-plus-A loss supervises the raw carrier's five-sum reader at coefficient one; "
               "the frozen-A arm clamps the raw route to zero.",
               "Probe fits use 2,048 training and 512 held-out board identities, fixed seeds, "
               "linear C=10 class-balanced regression and a width-64 MLP for 100 updates.",
               "Interchange alignment is an unregularized orthogonal Procrustes fit on training boards; "
               "each of five three-dimensional blocks represents one exact sum and the final dimension "
               "is residual. Pairing uses the full board-disjoint held-out pool (not just the "
               "512-board probe sample) and 1,024 fixed distinct eligible pairs per slot, or all if fewer. The same prediction-independent pairs and renderings apply to every control and network, including smoke.",
               "Smoke audits update 0 and the requested smoke endpoint, with smaller panel and probe samples "
               "declared in its checkpoint; it is not production evidence.",
               "Rare values 28–36 use a separately labelled held-out-rendering panel on shared board identities, with twenty independent renderings per selected board.",
               "Upper probes use twelve-round registered contexts with varied public queries; labels are current sums, never recurrent-memory targets supplied to the model.",
               "Every reader, shuffled-label control, alignment and independent other-slot decoder is persisted with its audit.",
               "Pre-launch positives are executed hard-answer and rotated raw-carrier oracles. Supported negatives are the no-op oracle and shuffled rotated oracle. The untrained conditional result is descriptive and unsupported, not a gate.",
               "Internal use additionally requires each seed's fixed 20k a_forced positive (donor-follow >=0.95, twenty accurate pairs per slot) and the evaluated network's supported shuffled-alignment negative. No checkpoint selection or extra training is allowed.",
               "Selectivity uses an independent training-only float64 affine least-squares decoder to fifteen oracle coordinates, followed by nearest prototypes. Its relative rank cutoff is 1e-7, declared for float32 carrier precision. Zero other-slot decoded changes is required; logistic decoding is supplementary. Oracle semantic integrity uses the known inverse rotation separately.",
               "A failed supported negative or selectivity check limits interpretation to B performance and A readability; it does not prevent those measurements. Internal use is then uncalibrated.",
               "Only equal-law unintended prediction changes are judged, at TV 0.02; donor-following original-law contrasts do not apply to equal-law models.",
               "Training draws coverage boards, placements and record orders on the chosen device, with independent per-run streams. A changed device does not claim identical random streams.",
           ]}
    write_json(output / "registration.json", row)
    (output / "registration.md").write_text(
        "# r10 registered all-slot study\n\n" + rules["claims_verbatim"] +
        "\n\n## Outcome readings (verbatim)\n\n" + rules["outcome_table_verbatim"] +
        "\n\n## Scope (verbatim)\n\n" + rules["scope_verbatim"] +
        "\n\n## Pass bars and choices\n\n" + json.dumps(
            {"criteria": row["criteria"], "settings": row["settings"],
             "source_A": source, "choices": row["choices"]}, indent=2) + "\n")
    return row


def registration() -> dict:
    row = json.loads((OUTPUT / "registration.json").read_text())
    if row["spec_sha256"] != sha(SPEC) or row["source_A"] != load_frozen_A(ROOT)[1]:
        raise ValueError("r10 registered sources differ")
    if row["source_identities"] != source_identities():
        raise ValueError("r10 implemented sources differ")
    if (row["calibration_specification_sha256"] != sha(specification) or
            row["intervention_settings"] != intervention_settings()):
        raise ValueError("r10 calibration amendments differ")
    for name, key in (("board_split.json", "board_split_sha256"),
                      ("probe_split.json", "probe_split_sha256"),
                      ("conditional_frequency.json", "frequency_sha256"),
                      ("interchange_pairs.json", "interchange_pairs_sha256")):
        if row[key] != sha(OUTPUT / name):
            raise ValueError(f"r10 registered {name} differs")
    if any(sha(OUTPUT / name) != value for name, value in row["panel_sha256"].items()):
        raise ValueError("r10 registered evaluation panel differs")
    return row


def records_for(panel: Episodes, boards) -> np.ndarray:
    return choice.record_projection(panel.boards, panel.rendering_seeds, boards)


@torch.no_grad()
def predict(model: AllSlotsNetwork, panel: Episodes, boards, *, batch=128) -> np.ndarray:
    records = records_for(panel, boards)
    rows = []
    model.eval()
    for start in range(0, len(records), batch):
        end = min(start + batch, len(records))
        logits, _ = model(torch.from_numpy(records[start:end]).long().to(DEVICE),
                          torch.from_numpy(panel.queries[start:end]).long().to(DEVICE),
                          torch.from_numpy(panel.lengths[start:end]).long().to(DEVICE))
        rows.append(torch.softmax(logits.float(), -1).cpu().numpy())
    return np.concatenate(rows)


def panel_from_ids(board_ids: np.ndarray, queries: np.ndarray, boards,
                   *, seed=2026101005) -> Episodes:
    rng = np.random.default_rng(seed)
    states = np.empty((*board_ids.shape, 5), dtype=np.int64)
    for i in range(len(board_ids)):
        previous = np.zeros(5, dtype=np.int64)
        for at, board_id in enumerate(board_ids[i]):
            current = np.asarray(boards.boards[int(board_id)], dtype=np.int64)
            previous = np.where(current > 0, current, previous)
            states[i, at] = previous
    return Episodes(board_ids, queries, np.zeros_like(board_ids),
                    np.full(len(board_ids), board_ids.shape[1], dtype=np.int64),
                    rng.integers(0, 2**63 - 1, board_ids.shape, dtype=np.int64), states)


def constructed_panels(boards) -> dict[str, Episodes]:
    pairs = eligible_pairs(boards, np.arange(len(boards.boards)))
    witness, holds = [], []
    witness_q, hold_q = [], []
    for slot in range(5):
        left, right = pairs[slot][0]
        neutral = next(i for i, board in enumerate(boards.boards) if board[slot] == 0)
        for source in (left, right):
            witness.append((source, neutral))
            holds.append((source,) + (neutral,) * 8)
            witness_q.append((slot, slot))
            hold_q.append((slot,) * 9)
    law_ids, law_queries = [], []
    for slot in range(5):
        for value in VALUES36:
            board_id = next(i for i, board in enumerate(boards.boards)
                            if board[slot] == value)
            law_ids.append((board_id,))
            law_queries.append((slot,))
    return {"law_rows": panel_from_ids(np.asarray(law_ids),
                                       np.asarray(law_queries), boards,
                                       seed=2026101007),
            "witness": panel_from_ids(np.asarray(witness), np.asarray(witness_q), boards),
            "eight_hold": panel_from_ids(np.asarray(holds), np.asarray(hold_q), boards,
                                         seed=2026101006)}


def kl_bits(truth: np.ndarray, predicted: np.ndarray) -> np.ndarray:
    value = np.clip(predicted, 1e-12, 1)
    return np.sum(truth * np.log2(truth / value), axis=-1)


def tv(truth: np.ndarray, predicted: np.ndarray) -> np.ndarray:
    return np.abs(truth - predicted).sum(axis=-1) / 2


def score(predicted: np.ndarray, panel: Episodes, *, equal: bool,
          minimum_cell: int = 20) -> dict:
    exact = oracle_rows(panel, equal=equal)
    errors = kl_bits(exact, predicted)
    value_indices = np.vectorize(VALUE_INDEX.__getitem__)(
        np.take_along_axis(panel.last_nonzero, panel.queries[..., None], -1)[..., 0])
    covered = np.zeros(value_indices.shape, dtype=bool)
    counts = []
    for slot in range(5):
        slot_counts = []
        for index in range(36):
            count = int(((panel.queries == slot) & (value_indices == index)).sum())
            slot_counts.append(count)
            if count >= minimum_cell:
                covered |= (panel.queries == slot) & (value_indices == index)
        counts.append(slot_counts)
    return {"rounds": int(errors.size), "KL_bits": float(errors.mean()),
            "maximum_TV": float(tv(exact, predicted).max()),
            "covered_value_KL_bits": float(errors[covered].mean()) if covered.any() else None,
            "covered_rounds": int(covered.sum()), "cell_counts": counts,
            "uncovered_cells": [[slot, i] for slot in range(5) for i in range(36)
                                if counts[slot][i] < minimum_cell]}


def blind_rows(panel: Episodes, trained_rows: np.ndarray) -> np.ndarray:
    row = mode_blind_row(trained_rows)
    return np.broadcast_to(row, (*panel.boards.shape, 3)).copy()


def b_audit(model: AllSlotsNetwork | None, law: str, boards, *, smoke=False,
            blind: np.ndarray | None = None) -> dict:
    equal = law == "equal"
    natural = load_panel(OUTPUT / f"natural_{law}.npz")
    heldout = load_panel(OUTPUT / f"heldout_board_{law}.npz")
    rerender = load_panel(OUTPUT / f"rerender_{law}.npz")
    if smoke:
        natural = Episodes(*(value[:256] for value in vars(natural).values()))
        heldout = Episodes(*(value[:128] for value in vars(heldout).values()))
        rerender = Episodes(*(value[:256] for value in vars(rerender).values()))
    panels = {"natural": natural, "heldout_board": heldout,
              "heldout_rendering": rerender, **constructed_panels(boards)}
    evaluated = {}
    natural_prediction = None
    for name, panel in panels.items():
        exact = oracle_rows(panel, equal=equal)
        prediction = (np.broadcast_to(blind, exact.shape).copy() if blind is not None else
                      predict(ExecutedOracle(equal=equal).to(DEVICE) if model is None else model,
                              panel, boards))
        evaluated[name] = score(prediction, panel, equal=equal,
                                minimum_cell=5 if smoke else 20)
        if name == "natural":
            natural_prediction = prediction
        if name == "heldout_rendering":
            evaluated[name]["prediction_rerender_maximum_TV"] = float(tv(
                natural_prediction, prediction).max())
        if name == "witness":
            rows = prediction[:, -1]
            differences = tv(rows[0::2], rows[1::2])
            evaluated[name]["minimum_prediction_pair_TV"] = float(differences.min())
            evaluated[name]["maximum_prediction_pair_TV"] = float(differences.max())
            exact_rows = exact[:, -1]
            evaluated[name]["minimum_exact_pair_TV"] = float(tv(
                exact_rows[0::2], exact_rows[1::2]).min())
    return evaluated


def _probe_data(split: dict, boards):
    result = []
    for name in ("train", "heldout"):
        ids = np.asarray(split[f"{name}_board_ids"], dtype=np.int64)
        seeds = np.asarray(split[f"{name}_render_seeds"], dtype=np.int64)
        records = choice.record_projection(ids[:, None], seeds[:, None], boards)[:, 0]
        sums = np.asarray([boards.boards[int(i)] for i in ids], dtype=np.int64)
        indices = np.vectorize(VALUE_INDEX.__getitem__)(sums)
        categories = np.where(sums <= 12, 0, np.where(sums >= 24, 2, 1))
        result.append((records, indices, categories, ids))
    return result


def oracle_features(indices: np.ndarray) -> np.ndarray:
    # The registered r8 oracle geometry separates all 36 exact values linearly.
    height = 1 - 2 * (indices + .5) / 36
    radius = np.sqrt(1 - height * height)
    angle = indices * np.pi * (3 - np.sqrt(5))
    coords = np.stack((radius * np.cos(angle), radius * np.sin(angle), height), -1)
    return np.pad(coords.reshape(len(indices), 15), ((0, 0), (0, 1))).astype(np.float32)


@torch.no_grad()
def carriers(model, records, *, history=None, queries=None):
    model.eval()
    raw, upper = [], []
    for start in range(0, len(records), 256):
        block = torch.from_numpy(records[start:start + 256]).long().to(DEVICE)
        if history is None:
            _, answers, values = model.round_interfaces(block)
            _, state = model.upper_step(answers, values, torch.zeros(len(block), device=DEVICE, dtype=torch.long))
        else:
            x = torch.from_numpy(history[start:start + 256]).long().to(DEVICE)
            q = torch.from_numpy(queries[start:start + 256]).long().to(DEVICE)
            trace = model(x, q, torch.full((len(x),), x.shape[1], device=DEVICE), return_trace=True)
            values, state = trace["raw_states"][:, -1], trace["upper_states"][:, -1]
        raw.append(values.float().cpu().numpy())
        upper.append(state.float().cpu().numpy())
    return np.concatenate(raw), np.concatenate(upper)


def _probe_context(records, split, boards, seed):
    rng = np.random.default_rng(seed)
    count = len(records)
    ids = rng.choice(split["train_board_ids"], (count, 12))
    seeds = rng.integers(0, 2**63 - 1, ids.shape, dtype=np.int64)
    history = choice.record_projection(ids, seeds, boards)
    history[:, -1] = records
    return history, rng.integers(0, 5, (count, 12), dtype=np.int64)


def _interval(correct, total):
    if total == 0:
        return None
    p, z = correct / total, 1.959963984540054
    scale = 1 + z*z / total
    mean = (p + z*z / (2*total)) / scale
    half = z * np.sqrt(p*(1-p)/total + z*z/(4*total*total)) / scale
    return [max(0., mean-half), min(1., mean+half)]


def _prediction_counts(predicted, truth, classes):
    ok = np.asarray(predicted) == truth
    return {"correct": int(ok.sum()), "total": len(ok), "accuracy": float(ok.mean()),
            "CI95": _interval(int(ok.sum()), len(ok)),
            "per_value": {str(value): {"correct": int(ok[truth == value].sum()),
                "total": int((truth == value).sum()),
                "CI95": _interval(int(ok[truth == value].sum()), int((truth == value).sum()))}
                for value in range(classes)}}


def apply_probe(fitted, inputs):
    x = (np.asarray(inputs) - np.asarray(fitted["mean"])) / np.asarray(fitted["scale"])
    if fitted["family"] == "linear":
        logits = x @ np.asarray(fitted["weight"]).T + np.asarray(fitted["bias"])
        if len(fitted["classes"]) == 2 and logits.shape[1] == 1:
            logits = np.concatenate((-logits, logits), axis=1)
        return np.asarray(fitted["classes"])[logits.argmax(-1)]
    with torch.no_grad():
        x = torch.as_tensor(x, dtype=torch.float32, device=DEVICE)
        hidden = F.relu(F.linear(x, torch.tensor(fitted["w0"], device=DEVICE),
                                 torch.tensor(fitted["b0"], device=DEVICE)))
        return F.linear(hidden, torch.tensor(fitted["w1"], device=DEVICE),
                        torch.tensor(fitted["b1"], device=DEVICE)).argmax(-1).cpu().numpy()


@torch.enable_grad()
def fit_probe(x, y, held, truth, family, classes, seed, *, smoke=False):
    mean, scale = x.mean(0), x.std(0)
    scale = np.where(scale == 0, 1., scale)
    fitted = {"family": family, "mean": mean.tolist(), "scale": scale.tolist()}
    if family == "linear":
        from sklearn.exceptions import ConvergenceWarning
        from sklearn.linear_model import LogisticRegression
        reader = LogisticRegression(C=10, class_weight="balanced", tol=1e-5, max_iter=5000)
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter("always", ConvergenceWarning)
            reader.fit((x-mean)/scale, y)
        convergence = [str(item.message) for item in observed if issubclass(item.category, ConvergenceWarning)]
        iterations = np.atleast_1d(reader.n_iter_).astype(int).tolist()
        fitted.update(weight=reader.coef_.tolist(), bias=reader.intercept_.tolist(),
                      classes=reader.classes_.tolist())
        evidence = {"n_iter": iterations, "warnings": convergence,
                    "converged": not convergence and max(iterations) < 5000, "fit_device": "cpu"}
    else:
        with torch.random.fork_rng(devices=[DEVICE] if DEVICE.type == "cuda" else []):
            torch.manual_seed(seed)
            reader = nn.Sequential(nn.Linear(x.shape[1], 64), nn.ReLU(), nn.Linear(64, classes)).to(DEVICE)
        optimizer = torch.optim.Adam(reader.parameters(), lr=.03)
        xx = torch.as_tensor((x-mean)/scale, device=DEVICE, dtype=torch.float32)
        yy = torch.as_tensor(y, device=DEVICE, dtype=torch.long)
        for _ in range(20 if smoke else 100):
            optimizer.zero_grad(set_to_none=True)
            F.cross_entropy(reader(xx), yy).backward()
            optimizer.step()
        fitted.update(w0=reader[0].weight.detach().cpu().tolist(), b0=reader[0].bias.detach().cpu().tolist(),
                      w1=reader[2].weight.detach().cpu().tolist(), b1=reader[2].bias.detach().cpu().tolist())
        evidence = {"fixed_updates": 20 if smoke else 100, "fit_device": DEVICE.type, "converged": None}
    predicted = apply_probe(fitted, held)
    return {**_prediction_counts(predicted, truth, classes), "predictions": predicted.tolist(),
            "fitted": fitted, **evidence}


def probe_audit(model, boards, *, smoke=False, oracle=False):
    split = json.loads((OUTPUT / "probe_split.json").read_text())
    if smoke:
        split = {**split, **{key: split[key][:256 if key.startswith("train") else 128]
                            for key in ("train_board_ids", "train_render_seeds",
                                        "heldout_board_ids", "heldout_render_seeds")}}
    (train, y, cat, _), (held, truth, truth_cat, _) = _probe_data(split, boards)
    rare_ids = np.asarray(split["rare_board_ids"])
    rare_seeds = np.asarray(split["rare_render_seeds"])
    rare = choice.record_projection(rare_ids[:, None], rare_seeds[:, None], boards)[:, 0]
    rare_sums = np.asarray(boards.boards)[rare_ids]
    rare_truth = np.vectorize(VALUE_INDEX.__getitem__)(rare_sums)
    rare_cat = np.where(rare_sums <= 12, 0, np.where(rare_sums >= 24, 2, 1))
    features = []
    for records, labels, seed in ((train, y, 2026101012), (held, truth, 2026101013),
                                  (rare, rare_truth, 2026101014)):
        if oracle:
            # Calibration carrier is reconstructed independently from record tokens.
            oracle_model = ExecutedOracle()
            resolved = oracle_model.round_interfaces(torch.tensor(records))[1].argmax(-1).numpy()
            if not np.array_equal(resolved, labels):
                raise ValueError("probe oracle record answers differ")
            raw = oracle_features(resolved)
            features.append((raw, np.pad(raw, ((0, 0), (0, 16)))))
        else:
            history, queries = _probe_context(records, split, boards, seed)
            features.append(carriers(model, records, history=history, queries=queries))
    result = {"sites": {}, "train_boards": len(train), "heldout_boards": len(held),
              "rare_scope": "Held-out renderings on shared board identities; not board-disjoint generalization.",
              "upper_scope": "Twelve-round registered recurrent histories and seeded public queries.",
              "rare_values_28_to_36": {str(slot): {str(value): {
                  "train": int((y[:, slot] == VALUE_INDEX[value]).sum()),
                  "heldout": int((truth[:, slot] == VALUE_INDEX[value]).sum()),
                  "heldout_rendering": int((rare_truth[:, slot] == VALUE_INDEX[value]).sum())}
                  for value in VALUES36 if value >= 28} for slot in range(5)},
              "heldout_labels": {"sum": truth.tolist(), "category": truth_cat.tolist()}}
    permutation = np.random.default_rng(PROBE_SEED + 100).permutation(len(train))
    result["majority_floor"] = {}
    for site_index, site in enumerate(("raw", "upper")):
        x, z, r = (part[site_index] for part in features)
        result["sites"][site] = {}
        for family in ("linear", "mlp64"):
            result["sites"][site][family] = {}
            for task, labels, expected, rare_expected, classes in (
                    ("sum", y, truth, rare_truth, 36), ("category", cat, truth_cat, rare_cat, 3)):
                entries = []
                for slot in range(5):
                    fit = fit_probe(x, labels[:, slot], z, expected[:, slot], family, classes,
                                    PROBE_SEED + slot, smoke=smoke)
                    shuffled = fit_probe(x, labels[permutation, slot], z, expected[:, slot],
                                         family, classes, PROBE_SEED + slot, smoke=smoke)
                    rp = apply_probe(fit["fitted"], r)
                    fit["rare_rendering"] = {**_prediction_counts(rp, rare_expected[:, slot], classes),
                                             "predictions": rp.tolist()}
                    fit["shuffled_floor"] = shuffled
                    entries.append(fit)
                result["sites"][site][family][task] = entries
                result["majority_floor"][task] = [float((expected[:, slot] ==
                    np.bincount(labels[:, slot], minlength=classes).argmax()).mean()) for slot in range(5)]
    return result


def fit_alignment(train_x: np.ndarray, train_indices: np.ndarray,
                  *, shuffle=False) -> dict:
    """Orthogonal fit, using only registered probe-training board identities."""

    target = oracle_features(train_indices).astype(np.float64)
    if shuffle:
        target = target[np.random.default_rng(2026101007).permutation(len(target))]
    source = train_x.astype(np.float64)
    source_mean = source.mean(0)
    target_mean = target.mean(0)
    left, _, right = np.linalg.svd((source - source_mean).T @ (target - target_mean))
    rotation = left @ right
    return {"rotation": rotation, "source_mean": source_mean,
            "target_mean": target_mean, "train_rows": len(source),
            "shuffled_labels": shuffle}


def align(states: np.ndarray, fitted: dict) -> np.ndarray:
    return ((states - fitted["source_mean"]) @ fitted["rotation"]
            + fitted["target_mean"])


def unalign(states: np.ndarray, fitted: dict) -> np.ndarray:
    return ((states - fitted["target_mean"]) @ fitted["rotation"].T
            + fitted["source_mean"])


def patch_block(base: np.ndarray, donor: np.ndarray, slot: int) -> np.ndarray:
    if base.shape != donor.shape or base.shape[-1] != 16 or slot not in range(5):
        raise ValueError("aligned slot block differs")
    result = base.copy()
    result[..., 3 * slot:3 * slot + 3] = donor[..., 3 * slot:3 * slot + 3]
    if not np.array_equal(np.delete(result, slice(3 * slot, 3 * slot + 3), axis=-1),
                          np.delete(base, slice(3 * slot, 3 * slot + 3), axis=-1)):
        raise ValueError("other aligned slot blocks changed")
    return result


def decoded_indices(aligned: np.ndarray) -> np.ndarray:
    prototypes = oracle_features(np.arange(36)[:, None].repeat(5, axis=1))[:, :3]
    distances = np.sum((aligned[..., None, :] - prototypes) ** 2, axis=-1)
    return distances.argmin(-1)


def intervention_settings():
    return {"pairs_per_slot": INTERCHANGE_PAIRS, "pair_seed": 2026101008,
            "render_seed_offset": 2026101009, "trained_positive_step": 20000,
            "positive_routes": ["hard_answer_oracle", "rotated_raw_oracle"],
            "supported_negatives": ["noop_oracle", "rotated_shuffled_alignment"],
            "untrained_conditional_status": "UNSUPPORTED_DESCRIPTIVE_ONLY",
            "decoder": {"type": "float64_affine_least_squares_to_15_coordinates",
                        "rcond": DECODER_RCOND, "fit": "training_boards_only",
                        "decision": "nearest_prototype", "other_slot_changes_allowed": 0},
            "logistic_decoder_role": "SUPPLEMENTARY_SENSITIVITY_ONLY"}


def fit_coordinate_decoder(states, labels):
    x = np.column_stack((np.asarray(states, dtype=np.float64), np.ones(len(states))))
    target = oracle_features(labels)[:, :15]
    coefficients, _, rank, singular = np.linalg.lstsq(x, target, rcond=DECODER_RCOND)
    error = x @ coefficients - target
    return {"coefficients": coefficients.tolist(), "rank": int(rank),
            "singular_values": singular.tolist(), "rcond": DECODER_RCOND,
            "training_rows": len(x), "training_RMSE": float(np.sqrt(np.mean(error**2))),
            "training_maximum_absolute_error": float(np.abs(error).max()),
            "fit_scope": "TRAINING_BOARDS_ONLY_INDEPENDENT_OF_ALIGNMENT"}


def decode_coordinates(states, fitted):
    x = np.column_stack((np.asarray(states, dtype=np.float64), np.ones(len(states))))
    coordinates = (x @ np.asarray(fitted["coefficients"])).reshape(-1, 5, 3)
    return decoded_indices(coordinates)


def select_pair_ids(boards, split):
    held = np.asarray(split["heldout_board_ids"], dtype=np.int64)
    eligible = eligible_pairs(boards, held)
    rng = np.random.default_rng(2026101008)
    slots = {}
    for slot in range(5):
        pool = eligible[slot]
        selected = rng.choice(len(pool), size=min(INTERCHANGE_PAIRS, len(pool)), replace=False)
        slots[str(slot)] = {"pairs": [list(pool[int(i)]) for i in selected],
                            "eligible_count": len(pool)}
    return {"selection_seed": 2026101008, "render_seed_offset": 2026101009,
            "prediction_independent": True, "slots": slots}


def _paired_records(boards, split: dict):
    manifest = json.loads((OUTPUT / "interchange_pairs.json").read_text())
    registered = json.loads((OUTPUT / "registration.json").read_text())
    if sha(OUTPUT / "interchange_pairs.json") != registered["interchange_pairs_sha256"]:
        raise ValueError("r10 fixed pair list digest differs")
    if manifest != select_pair_ids(boards, split):
        raise ValueError("r10 fixed eligible pair list differs")
    result = {}
    for slot in range(5):
        data = manifest["slots"][str(slot)]
        pairs = data["pairs"]
        ids = np.asarray([item for pair in pairs for item in pair], dtype=np.int64)
        seeds = ids + np.int64(2026101009)
        records = choice.record_projection(ids[:, None], seeds[:, None], boards)[:, 0]
        result[slot] = {"pairs": pairs, "records": records,
                        "eligible_count": data["eligible_count"], "selected_count": len(pairs)}
    return result


class RotatedCarrierOracle(ExecutedOracle):
    """Geometric carrier calibration executed through the upper-step interface."""

    def __init__(self, rotation, *, equal=False):
        super().__init__(equal=equal)
        self.rotation = rotation

    def round_interfaces(self, records):
        logits, answers, _ = super().round_interfaces(records)
        raw = oracle_features(answers.argmax(-1).cpu().numpy()) @ self.rotation
        return logits, answers, torch.tensor(raw, device=records.device, dtype=torch.float32)

    def upper_step(self, answers, raw, query, previous=None):
        original = raw.cpu().numpy() @ self.rotation.T
        indices = np.stack([decoded_indices(original[:, 3*k:3*k+3][:, None, :])[:, 0]
                            for k in range(5)], axis=1)
        encoded = F.one_hot(torch.tensor(indices, device=raw.device), 36).float()
        return super().upper_step(encoded, raw, query, previous)


class HardAnswerOracle(ExecutedOracle):
    arm = "a_forced"

    def round_interfaces(self, records):
        logits, answers, _ = super().round_interfaces(records)
        raw = torch.tensor(oracle_features(answers.argmax(-1).cpu().numpy()),
                           dtype=torch.float32, device=records.device)
        return logits, answers, raw


@torch.no_grad()
def interchange(model, boards, *, smoke=False, oracle=False, shuffled_alignment=False,
                law="original", contaminate=False, noop=False):
    split = json.loads((OUTPUT / "probe_split.json").read_text())
    split["heldout_board_ids"] = json.loads((OUTPUT / "board_split.json").read_text())["heldout_board_ids"]
    split["heldout_render_seeds"] = [int(i) + 2026101009 for i in split["heldout_board_ids"]]
    (train_records, train_y, _, _), _ = _probe_data(split, boards)
    if oracle:
        rotation, _ = np.linalg.qr(np.random.default_rng(2026101010).normal(size=(16, 16)))
        model = RotatedCarrierOracle(rotation, equal=law == "equal").to(DEVICE)
    train_raw = carriers(model, train_records)[0]
    fitted = fit_alignment(train_raw, train_y, shuffle=shuffled_alignment)
    # Independent full-coordinate readers, not the unchanged aligned blocks.
    decoders = [fit_probe(train_raw, train_y[:, slot], train_raw, train_y[:, slot],
                           "linear", 36, PROBE_SEED + slot)["fitted"] for slot in range(5)]
    coordinate_decoder = fit_coordinate_decoder(train_raw, train_y)
    candidates = _paired_records(boards, split)
    result = {"slots": {}, "alignment_train_boards": len(train_y),
              "shuffled_alignment": shuffled_alignment, "oracle_rotated_carrier": oracle,
              "alignment": {key: value.tolist() if isinstance(value, np.ndarray) else value
                            for key, value in fitted.items()},
              "independent_other_slot_decoders": decoders, "law": law,
              "independent_coordinate_decoder": coordinate_decoder,
              "pair_list_sha256": sha(OUTPUT / "interchange_pairs.json"),
              "contaminating_intervention": contaminate, "noop_intervention": noop}
    for slot, data in candidates.items():
        pairs, record = data["pairs"], data["records"]
        _, answers, raw_tensor = model.round_interfaces(torch.tensor(record, device=DEVICE).long())
        raw = raw_tensor.float().cpu().numpy().astype(np.float64)
        aligned = align(raw, fitted)
        patched_aligned = patch_block(aligned[0::2], aligned[1::2], slot)
        if contaminate:
            patched_aligned[:, 3*((slot+1)%5):3*((slot+1)%5)+3] += 10
        patched_raw_array = unalign(patched_aligned, fitted)
        if noop:
            patched_raw_array = raw[0::2].copy()
        query = torch.full((len(pairs),), slot, device=DEVICE, dtype=torch.long)
        base_pred = model.upper_step(answers[0::2], raw_tensor[0::2], query)[0].float().softmax(-1).cpu().numpy()
        donor_pred = model.upper_step(answers[1::2], raw_tensor[1::2], query)[0].float().softmax(-1).cpu().numpy()
        if getattr(model, "arm", None) == "a_forced":
            patched_answers = answers[0::2].clone()
            if not noop:
                patched_answers[:, slot] = answers[1::2, slot]
            # The oracle exposes the semantic answer coordinates for independent decoding.
            if isinstance(model, HardAnswerOracle):
                patched_raw_array = oracle_features(patched_answers.argmax(-1).cpu().numpy())
            else:
                patched_raw_array = raw[0::2]
            patched_raw = torch.tensor(patched_raw_array, device=DEVICE, dtype=raw_tensor.dtype)
            if shuffled_alignment:
                # Shuffled raw alignment is not an executed intervention on this hard-answer route.
                result["shuffled_alignment_scope"] = "NOT_APPLICABLE_TO_HARD_ANSWER_PATCH"
        else:
            patched_answers = answers[0::2]
            patched_raw = torch.tensor(patched_raw_array, device=DEVICE, dtype=raw_tensor.dtype)
        prediction = model.upper_step(patched_answers, patched_raw, query)[0].float().softmax(-1).cpu().numpy()
        values = np.asarray([boards.boards[i][slot] for pair in pairs for i in pair])
        exact = ROW_FLOAT[np.vectorize(VALUE_INDEX.__getitem__)(values)]
        if law == "equal":
            exact = np.ones_like(exact) / 3
        base_row, donor_row = exact[0::2], exact[1::2]
        valid = (tv(base_pred, base_row) <= PAIR_LIMIT) & (tv(donor_pred, donor_row) <= PAIR_LIMIT)
        follow = tv(prediction, donor_row) < tv(prediction, base_row)
        # Score the executed float32 patch, not its pre-cast idealization.
        patched_raw_array = patched_raw.float().cpu().numpy().astype(np.float64)
        before = decode_coordinates(raw[0::2], coordinate_decoder)
        after = decode_coordinates(patched_raw_array, coordinate_decoder)
        changed = before != after
        changed[:, slot] = False
        logistic_before = np.stack([apply_probe(d, raw[0::2]) for d in decoders], -1)
        logistic_after = np.stack([apply_probe(d, patched_raw_array) for d in decoders], -1)
        logistic_changed = logistic_before != logistic_after
        logistic_changed[:, slot] = False
        semantic = None
        if oracle or isinstance(model, HardAnswerOracle):
            actual = patched_raw_array @ model.rotation.T if oracle else patched_raw_array
            expected_indices = np.asarray([[VALUE_INDEX[boards.boards[a][k]] for k in range(5)]
                                           for a,b in pairs])
            if not noop:
                expected_indices[:,slot] = [VALUE_INDEX[boards.boards[b][slot]] for a,b in pairs]
            expected = oracle_features(expected_indices)
            semantic_indices = decoded_indices(actual[:,:15].reshape(-1,5,3))
            prototypes = oracle_features(np.arange(36)[:,None].repeat(5,axis=1))[:,:3]
            distances = ((actual[:,:15].reshape(-1,5,1,3)-prototypes)**2).sum(-1)
            ordered = np.sort(distances, axis=-1)
            margins = ordered[:,:,1]-ordered[:,:,0]
            mismatches = semantic_indices != expected_indices
            semantic = {"donor_slot_errors": int(mismatches[:,slot].sum()),
                        "other_slot_errors": int(np.delete(mismatches,slot,axis=1).sum()),
                        "reconstruction_RMSE": float(np.sqrt(np.mean((actual-expected)**2))),
                        "maximum_absolute_reconstruction_error": float(np.abs(actual-expected).max()),
                        "minimum_decision_margin": float(margins.min()),
                        "decision_margins": margins.tolist(),
                        "decoder": "KNOWN_INVERSE_ROTATION_AND_PROTOTYPES" if oracle else "HARD_ANSWER_PROTOTYPES"}
        supported = int(valid.sum()) >= MINIMUM_ACCURATE_PAIRS
        per_pair = [{"base": int(a), "donor": int(b), "accurate_unpatched": bool(valid[i]),
                     "base_prediction": base_pred[i].tolist(), "donor_prediction": donor_pred[i].tolist(),
                     "patched_prediction": prediction[i].tolist(), "TV_to_base": float(tv(prediction[i], base_row[i])),
                     "TV_to_donor": float(tv(prediction[i], donor_row[i])),
                     "unwanted_prediction_change_TV": float(tv(prediction[i], base_pred[i])),
                     "other_slot_before": before[i].tolist(), "other_slot_after": after[i].tolist(),
                     "other_slot_changes": int(changed[i].sum()),
                     "supplementary_logistic_before": logistic_before[i].tolist(),
                     "supplementary_logistic_after": logistic_after[i].tolist()} for i, (a,b) in enumerate(pairs)]
        count = int((follow & valid).sum())
        result["slots"][str(slot)] = {
            "eligible_pairs": data["eligible_count"], "evaluated_pairs": len(pairs),
            "accurate_unpatched_pairs": int(valid.sum()), "donor_follow_count": count,
            "donor_follow_rate": count/len(pairs) if pairs else None,
            "donor_follow_rate_among_accurate": count/int(valid.sum()) if valid.any() else None,
            "donor_follow_CI95": _interval(count, int(valid.sum())),
            "status": "SUPPORTED" if supported else "UNCALIBRATED_INSUFFICIENT_ACCURATE_PAIRS",
            "mean_TV_to_base": float(tv(prediction, base_row).mean()),
            "mean_TV_to_donor": float(tv(prediction, donor_row).mean()),
            "maximum_unwanted_prediction_change_TV": float(tv(prediction, base_pred).max()),
            "other_slot_probe_changes": int(changed.sum()), "pair_ids": pairs, "per_pair": per_pair,
            "supplementary_logistic_other_slot_changes": int(logistic_changed.sum()),
            "oracle_semantic_integrity": semantic,
            "per_base_value": {str(value): {"evaluated_pairs":int((values[0::2] == value).sum()),
                "accurate_pairs":int((valid & (values[0::2] == value)).sum()),
                "donor_follow_count":int((follow & valid & (values[0::2] == value)).sum()),
                "CI95":_interval(int((follow & valid & (values[0::2] == value)).sum()),
                                   int((valid & (values[0::2] == value)).sum()))}
                for value in VALUES36},
            "per_donor_value_counts": {str(value): int((values[1::2] == value).sum()) for value in VALUES36},
            "aligned_exact_sum_decoding": float((before[:, slot] == np.vectorize(VALUE_INDEX.__getitem__)(
                np.asarray([boards.boards[a][slot] for a,b in pairs]))).mean())}
    return result


def _new_model(arm: str, seed: int) -> AllSlotsNetwork:
    source, _ = load_frozen_A(ROOT)
    return AllSlotsNetwork(arm, seed, source.core).to(DEVICE).eval()


def _audit(model: AllSlotsNetwork, law: str, boards, *, smoke=False) -> dict:
    started = time.monotonic()
    with torch.random.fork_rng():
        b = b_audit(model, law, boards, smoke=smoke)
        probes = probe_audit(model, boards, smoke=smoke)
        patch = interchange(model, boards, smoke=smoke, law=law)
        shuffled = interchange(model, boards, smoke=smoke, law=law, shuffled_alignment=True)
        panel = load_panel(OUTPUT / f"natural_{law}.npz")
        altered = load_panel(OUTPUT / f"rerender_{law}.npz")
        count = 256 if smoke else len(panel.boards)
        answer_rows = []
        for chosen in (panel, altered):
            records = records_for(Episodes(*(v[:count] for v in vars(chosen).values())), boards)
            correct, differences = np.zeros(5, dtype=np.int64), 0
            saved = []
            for at in range(0, count, 128):
                chunk = torch.as_tensor(records[at:at+128], device=DEVICE).long()
                with torch.no_grad():
                    values = model(chunk, torch.as_tensor(chosen.queries[at:at+128], device=DEVICE),
                        torch.as_tensor(chosen.lengths[at:at+128], device=DEVICE), return_trace=True)
                logits = values["A_logits"] if model.arm == "free_a" else values["frozen_A_answers"]
                if model.arm == "free":
                    logits = values["A_logits"]
                answer = logits.argmax(-1).cpu().numpy()
                truth = np.searchsorted(VALUES36, np.asarray(boards.boards)[chosen.boards[at:at+128]])
                correct += (answer == truth).sum(axis=(0,1))
                saved.append(answer)
            answer_rows.append({"correct_by_slot": correct.tolist(), "total_by_slot": count*panel.boards.shape[1],
                                "answers": np.concatenate(saved)})
        differences = answer_rows[0]["answers"] != answer_rows[1]["answers"]
        interface = {"reader": "frozen_exact_A" if model.arm == "a_forced" else "raw_A_head",
            "correct_by_slot": answer_rows[0]["correct_by_slot"], "total_by_slot": answer_rows[0]["total_by_slot"],
            "rerender_component_differences": int(differences.sum()),
            "rerender_vector_differences": int(differences.any(-1).sum())}
    return {"B": b, "probes": probes, "interchange": patch, "shuffled_interchange": shuffled,
            "A_interface": interface,
            "elapsed_seconds": time.monotonic() - started}


def _positive_probe(probe: dict) -> bool:
    return all(any(site[family][task][slot]["accuracy"] >= .99 and
                   site[family][task][slot].get("converged") is not False and
                   (task != "sum" or all(
                       (value := site[family][task][slot]["rare_rendering"]["per_value"][str(VALUE_INDEX[v])])["total"] >= 20
                       and value["correct"] / value["total"] >= .99 for v in VALUES36 if v >= 28))
                   for site in probe["sites"].values() for family in ("linear", "mlp64"))
               for task in ("sum", "category") for slot in range(5))


def calibrate():
    registration()
    if (OUTPUT/"calibration.json").exists():
        raise ValueError("r10 calibration already exists")
    boards = enumerate_boards()
    untrained = _new_model("free", 0)
    blind = mode_blind_row(oracle_rows(load_panel(OUTPUT/"blind_fit_original.npz")))
    row = {"registration_sha256": sha(OUTPUT/"registration.json"), "exact_oracle": {},
           "mode_blind": {}, "untrained": {}, "probe": {}, "interchange": {},
           "mode_blind_row": blind.tolist(), "device": DEVICE.type,
           "eligible_pairs_by_slot": {str(k): len(v) for k,v in eligible_pairs(boards,
               np.asarray(json.loads((OUTPUT/"board_split.json").read_text())["heldout_board_ids"])).items()}}
    for law in LAWS:
        row["exact_oracle"][law] = b_audit(None, law, boards)
        row["mode_blind"][law] = b_audit(None, law, boards,
                                        blind=blind if law == "original" else np.ones(3)/3)
        row["untrained"][law] = b_audit(untrained, law, boards)
    row["probe"]["oracle"] = probe_audit(None, boards, oracle=True)
    row["probe"]["untrained"] = probe_audit(untrained, boards)
    row["interchange"]["rotated_oracle"] = interchange(None, boards, oracle=True)
    row["interchange"]["hard_answer_oracle"] = interchange(HardAnswerOracle().to(DEVICE), boards)
    row["interchange"]["noop_oracle"] = interchange(None, boards, oracle=True, noop=True)
    row["interchange"]["rotated_shuffled_alignment"] = interchange(None, boards, oracle=True,
                                                                  shuffled_alignment=True)
    row["interchange"]["contaminating"] = interchange(None, boards, oracle=True, contaminate=True)
    row["interchange"]["untrained"] = interchange(untrained, boards)
    row["interchange"]["untrained_shuffled_alignment"] = interchange(untrained, boards,
                                                                   shuffled_alignment=True)
    row["trained_positive_status"] = "DEFERRED_TO_EACH_SEEDS_FIXED_20000_ENDPOINT"
    row["untrained_conditional_status"] = "UNSUPPORTED_DESCRIPTIVE_ONLY"
    row["interchange"]["equal_oracle"] = interchange(None, boards, oracle=True, law="equal")
    decisions = {}
    for law in LAWS:
        decisions[law] = {kind: _b_pass({"B": row[kind][law]}, row, law)
                          for kind in ("exact_oracle", "mode_blind", "untrained")}
    row["decisions"] = decisions
    passes = lambda bars: all(v for key,v in bars.items() if key != "bounds")
    row["checks"] = {
        "executed_oracle_passes_both_laws": all(passes(decisions[law]["exact_oracle"]) for law in LAWS),
        "mode_blind_original_fails": not passes(decisions["original"]["mode_blind"]),
        "mode_blind_equal_passes": passes(decisions["equal"]["mode_blind"]),
        "untrained_original_fails": not passes(decisions["original"]["untrained"]),
        "oracle_probe_positive": _positive_probe(row["probe"]["oracle"]),
        "rotated_oracle_executed_patch_passes": all(
            r["status"] == "SUPPORTED" and r["donor_follow_rate_among_accurate"] >= .95
            for r in row["interchange"]["rotated_oracle"]["slots"].values()),
        "hard_answer_oracle_executed_patch_passes": all(
            r["status"] == "SUPPORTED" and r["donor_follow_rate_among_accurate"] >= .95
            for r in row["interchange"]["hard_answer_oracle"]["slots"].values()),
        "rotated_oracle_semantic_integrity": all(
            r["oracle_semantic_integrity"]["donor_slot_errors"] == 0 and
            r["oracle_semantic_integrity"]["other_slot_errors"] == 0
            for r in row["interchange"]["rotated_oracle"]["slots"].values()),
        "contamination_detected": all(r["other_slot_probe_changes"] > 0
            for r in row["interchange"]["contaminating"]["slots"].values()),
        "equal_intervention_invariant": all(r["maximum_unwanted_prediction_change_TV"] <= EQUAL_TV_LIMIT
            for r in row["interchange"]["equal_oracle"]["slots"].values())}
    row["intervention_calibration_status"] = {str(slot): prelaunch_use_gate(
        row["interchange"]["rotated_oracle"]["slots"][str(slot)],
        row["interchange"]["hard_answer_oracle"]["slots"][str(slot)],
        row["interchange"]["noop_oracle"]["slots"][str(slot)],
        row["interchange"]["rotated_shuffled_alignment"]["slots"][str(slot)])
        for slot in range(5)}
    row["interpretation_scope"] = ("INTERNAL_USE_REQUIRES_FIXED_ENDPOINT_TRAINED_CALIBRATION"
        if all(r["passes"] for r in row["intervention_calibration_status"].values())
        else "B_PERFORMANCE_AND_A_READABILITY_ONLY")
    write_json(OUTPUT/"calibration.json", row)
    if not all(row["checks"].values()):
        raise ValueError(f"r10 calibration separation fails: {row['checks']}")
    return {"checks": row["checks"], "interpretation_scope": row["interpretation_scope"],
        "intervention_calibration_status": row["intervention_calibration_status"],
        "eligible_pairs_by_slot": row["eligible_pairs_by_slot"]}


def prelaunch_use_gate(rotated, hard, noop, shuffled):
    controls = {"rotated": rotated, "hard": hard, "noop": noop, "shuffled": shuffled}
    unsupported = [k for k,r in controls.items() if r["accurate_unpatched_pairs"] < MINIMUM_ACCURATE_PAIRS]
    checks = {"supported": not unsupported,
              "positive_rates": all((r["donor_follow_rate_among_accurate"] or 0) >= .95 for r in (rotated,hard)),
              "negative_rates": all(r["donor_follow_rate_among_accurate"] is not None and
                  r["donor_follow_rate_among_accurate"] <= .20 for r in (noop,shuffled)),
              "independent_selectivity": all(r["other_slot_probe_changes"] == 0 for r in (rotated,hard)),
              "oracle_semantic_integrity": all(r["oracle_semantic_integrity"]["donor_slot_errors"] == 0 and
                  r["oracle_semantic_integrity"]["other_slot_errors"] == 0 for r in (rotated,hard))}
    passes = all(checks.values())
    return {"status": "CALIBRATED" if passes else "UNCALIBRATED", "passes": passes,
            "checks": checks, "insufficient_support": unsupported,
            "rates": {k:r["donor_follow_rate_among_accurate"] for k,r in controls.items()},
            "denominators": {k:r["accurate_unpatched_pairs"] for k,r in controls.items()},
            "CI95": {k:r["donor_follow_CI95"] for k,r in controls.items()}}


def intervention_gate(observed, positive, prelaunch, shuffled, *, equal=False, positive_step=None):
    if equal:
        if observed["accurate_unpatched_pairs"] < MINIMUM_ACCURATE_PAIRS:
            return {"status": "UNCALIBRATED", "insufficient_support": ["observed"], "passes": False}
        unwanted = observed["maximum_unwanted_prediction_change_TV"]
        return {"status": "EQUAL_LAW", "unwanted_prediction_change_TV": unwanted,
                "passes": unwanted <= EQUAL_TV_LIMIT, "control_failure": unwanted > EQUAL_TV_LIMIT}
    controls = {"observed": observed, "fixed_endpoint_a_forced": positive,
                "model_shuffled_alignment": shuffled}
    unsupported = [name for name,row in controls.items() if row is None or
                   row["accurate_unpatched_pairs"] < MINIMUM_ACCURATE_PAIRS]
    if unsupported or positive_step != 20000 or prelaunch is None or not prelaunch["passes"]:
        return {"status": "UNCALIBRATED", "insufficient_support": unsupported, "passes": False,
                "positive_step": positive_step, "fixed_endpoint_positive": positive_step == 20000,
                "prelaunch_use_calibrated": prelaunch is not None and prelaunch["passes"]}
    positive_ok = positive["donor_follow_rate_among_accurate"] >= .95
    calibrated = positive_ok and shuffled["donor_follow_rate_among_accurate"] <= .20
    return {"status": "CALIBRATED" if calibrated else "UNCALIBRATED",
            "positive_rate": positive["donor_follow_rate_among_accurate"],
            "shuffled_rate": shuffled["donor_follow_rate_among_accurate"],
            "positive_CI95": positive["donor_follow_CI95"],
            "shuffled_CI95": shuffled["donor_follow_CI95"],
            "passes": bool(calibrated and observed["donor_follow_rate_among_accurate"] >= .8 and
                           observed["other_slot_probe_changes"] == 0)}


class EpisodeStream:
    def __init__(self, seed: int, equal: bool) -> None:
        self.seed = STREAM_SEED + seed + 100 * equal
        self.rng = np.random.default_rng(self.seed)
        self.rolling = bytes(32)
        self.draws = 0

    def draw(self, sampler: CoverageSampler, batch: int, rounds: int, equal: bool):
        seed = int(self.rng.integers(0, 2**63 - 1))
        panel = sample_episodes(sampler, batch, rounds, seed, equal=equal)
        state = hashlib.sha256()
        state.update(self.rolling)
        state.update(seed.to_bytes(8, "little"))
        for value in vars(panel).values():
            state.update(value.tobytes())
        self.rolling = state.digest()
        self.draws += 1
        return panel

    def state(self) -> dict:
        return {"seed": self.seed, "rng_state": self.rng.bit_generator.state,
                "rolling_sha256": self.rolling.hex(), "draws": self.draws}

    def restore(self, state: dict) -> None:
        if state["seed"] != self.seed:
            raise ValueError("r10 stream seed differs")
        self.rng.bit_generator.state = state["rng_state"]
        self.rolling = bytes.fromhex(state["rolling_sha256"])
        self.draws = state["draws"]
        if self.state() != state:
            raise ValueError("r10 stream restoration differs")


def train_loss(model: AllSlotsNetwork, records: torch.Tensor, panel: Episodes,
               boards) -> tuple[torch.Tensor, dict]:
    queries = torch.from_numpy(panel.queries).long()
    lengths = torch.from_numpy(panel.lengths).long()
    predicted, a_logits = model(records, queries, lengths)
    target = torch.from_numpy(panel.targets).long()
    b_loss = F.cross_entropy(predicted.reshape(-1, 3), target.reshape(-1))
    a_loss = b_loss.new_zeros(())
    if model.arm == "free_a":
        sums = np.asarray(boards.boards, dtype=np.int64)[panel.boards]
        indices = np.vectorize(VALUE_INDEX.__getitem__)(sums)
        a_loss = F.cross_entropy(a_logits.reshape(-1, 36),
                                 torch.from_numpy(indices.reshape(-1)).long())
    return b_loss + a_loss, {"B": float(b_loss.detach()), "A": float(a_loss.detach())}


def _name(arm: str, law: str, seed: int) -> str:
    if arm not in ARMS or law not in LAWS or seed not in SEEDS:
        raise ValueError("r10 run setting differs")
    return f"{arm}_{law}_seed{seed}"


def run(arm, law, seed, *, output_root=OUTPUT, smoke=False, steps=None, bulk_root=None):
    from scripts import oldgame_allslots_execution as execution
    import sys
    return execution.run_chunk(sys.modules[__name__], [execution.Run(arm, law, seed)],
        DEVICE, output_root, bulk_root or (output_root/"bulk"), steps=steps or (200 if smoke else 20000),
        smoke=smoke)[0]


def _b_pass(audit: dict, calibration: dict, law: str) -> dict:
    measured = audit["B"]
    blind = calibration["mode_blind"][law]["natural"]
    factor = .1 if law == "original" else 1.0
    natural_bound = max(.01 if law == "equal" else 0,
                        factor * blind["KL_bits"])
    covered_bound = max(.01 if law == "equal" else 0,
                        factor * blind["covered_value_KL_bits"])
    return {"natural_KL": measured["natural"]["KL_bits"] <= natural_bound,
            "covered_value_KL": (measured["natural"]["covered_value_KL_bits"]
                                 is not None and measured["natural"][
                                     "covered_value_KL_bits"] <= covered_bound),
            "constructed_law_TV": max(measured[name]["maximum_TV"]
                                      for name in ("law_rows", "witness", "eight_hold")) <= (
                                          EQUAL_TV_LIMIT if law == "equal" else .05),
            "same_board_witness": (measured["witness"]["maximum_TV"] <= .05 and
                                   (measured["witness"]["maximum_prediction_pair_TV"] <= EQUAL_TV_LIMIT
                                    if law == "equal" else
                                    measured["witness"]["minimum_prediction_pair_TV"] >= .05)),
            "bounds": {"natural_KL": natural_bound,
                       "covered_value_KL": covered_bound}}


def _probe_gain(current: dict, initial: dict, oracle: dict, split: dict, boards) -> dict:
    held = np.asarray(split["heldout_board_ids"], dtype=np.int64)
    sums = np.asarray([boards.boards[int(i)] for i in held])
    truth = {"sum": np.vectorize(VALUE_INDEX.__getitem__)(sums),
             "category": np.where(sums <= 12, 0, np.where(sums >= 24, 2, 1))}
    if "heldout_labels" in current:
        truth = {key: np.asarray(value) for key, value in current["heldout_labels"].items()}
    rng = np.random.default_rng(2026101011)
    result = {}
    for site in ("raw", "upper"):
        result[site] = {}
        for family in ("linear", "mlp64"):
            result[site][family] = {}
            for task in ("sum", "category"):
                result[site][family][task] = []
                for slot in range(5):
                    now = current["sites"][site][family][task][slot]
                    before = initial["sites"][site][family][task][slot]
                    positive = oracle["sites"][site][family][task][slot]
                    delta = ((np.asarray(now["predictions"]) == truth[task][:, slot]).astype(float)
                             - (np.asarray(before["predictions"]) == truth[task][:, slot]).astype(float))
                    draws = rng.integers(0, len(delta), (1000, len(delta)))
                    interval = np.quantile(delta[draws].mean(1), [.025, .975]).tolist()
                    converged = all(item.get("converged", True) is not False
                                    for item in (now, before, positive))
                    per_value_gain = {}
                    for value in now["per_value"]:
                        selected = truth[task][:, slot] == int(value)
                        selected_delta = delta[selected]
                        per_value_gain[value] = {"total":len(selected_delta),
                            "gain":float(selected_delta.mean()) if len(selected_delta) else None,
                            "paired_CI95":np.quantile(selected_delta[rng.integers(0,len(selected_delta),
                                (1000,len(selected_delta)))].mean(1),[.025,.975]).tolist()
                                if len(selected_delta) else None}
                    result[site][family][task].append({
                        "slot": slot, "before": before["accuracy"],
                        "endpoint": now["accuracy"], "gain": float(delta.mean()),
                        "paired_CI95": interval, "positive_accuracy": positive["accuracy"],
                        "fits_converged": converged,
                        "readability_gain": (interval[0] > 0 and converged and
                                             now["accuracy"] > max(current["majority_floor"][task][slot],
                                                                    now["shuffled_floor"]["accuracy"]) and
                                             positive["accuracy"] >= .99 and
                                             before["accuracy"] < positive["accuracy"] - .01),
                        "majority_floor": current["majority_floor"][task][slot],
                        "correct": now["correct"], "total": now["total"],
                        "per_value": now["per_value"], "shuffled_floor": now["shuffled_floor"],
                        "before_per_value":before["per_value"], "oracle_per_value":positive["per_value"],
                        "per_value_gain":per_value_gain,
                        "rare_rendering": now["rare_rendering"],
                        "rare_readable": (task != "sum" or all(
                            (value := now["rare_rendering"]["per_value"][str(VALUE_INDEX[v])])["total"] >= 20 and
                            value["correct"] / value["total"] >= .99 and
                            (positive_value := positive["rare_rendering"]["per_value"][str(VALUE_INDEX[v])])["total"] >= 20 and
                            positive_value["correct"] / positive_value["total"] >= .99
                            for v in VALUES36 if v >= 28)),
                    })
    return result


def endpoint_claim(b_pass, readable, patches, *, equal_control_failure=False):
    if equal_control_failure:
        return "CONTROL_FAILURE"
    if b_pass and readable and patches:
        return "A_MEDIATED_UNDER_REGISTERED_ALIGNMENT"
    if b_pass and readable:
        return "PATHWAY_UNRESOLVED"
    if b_pass:
        return "SUFFICIENT_QUOTIENT_OR_INCOMPLETE_EXACT_SUM_READABILITY"
    return "B_INCOMPLETE"


def aggregate(output_root=OUTPUT, *, bulk_root=None):
    from scripts.oldgame_allslots_report import aggregate_saved

    return aggregate_saved(__import__(__name__, fromlist=["*"]), output_root, bulk_root)


def main() -> None:
    global DEVICE
    from scripts import oldgame_allslots_execution as execution
    torch.set_num_threads(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("register", "calibrate", "run", "aggregate", "verify-gpu"))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--arm", choices=ARMS)
    parser.add_argument("--law", choices=LAWS)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--runs", choices=ARMS)
    parser.add_argument("--run-name", action="append")
    parser.add_argument("--chunk-runs", type=int)
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--verification-output", type=Path)
    parser.add_argument("--bulk-root", type=Path, default=execution.BULK)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-root", type=Path, default=None)
    arguments = parser.parse_args()
    DEVICE = execution.r11.configure(arguments.device)
    if arguments.stage == "register":
        result = register()
        print("registration", sha(OUTPUT / "registration.json"), result["law"])
    elif arguments.stage == "calibrate":
        result = calibrate()
        print(json.dumps(result, sort_keys=True))
    elif arguments.stage == "aggregate":
        print(json.dumps(aggregate(arguments.output_root or OUTPUT, bulk_root=arguments.bulk_root), sort_keys=True))
    elif arguments.stage == "verify-gpu":
        destination = arguments.verification_output or OUTPUT / f"verification_{DEVICE.type}.json"
        try:
            result = execution.verification(__import__(__name__, fromlist=["*"]), DEVICE,
                trace=arguments.trace, destination=destination)
        except Exception as error:
            if not destination.exists():
                write_json(destination, {"pass": False, "error": str(error), "device": DEVICE.type,
                    "registration_sha256": sha(OUTPUT / "registration.json"),
                    "source_hashes": source_identities()})
            raise
        print(json.dumps(result, sort_keys=True))
    else:
        candidates = execution.all_runs()
        if arguments.run_name:
            runs = [r for r in candidates if r.name in arguments.run_name]
            if len(runs) != len(arguments.run_name):
                parser.error("unknown or duplicated run name")
        elif arguments.runs:
            runs = [r for r in candidates if r.arm == arguments.runs and
                    (arguments.law is None or r.law == arguments.law) and
                    (arguments.seed is None or r.seed == arguments.seed)]
        elif arguments.arm is not None and arguments.law is not None and arguments.seed is not None:
            runs = [execution.Run(arguments.arm, arguments.law, arguments.seed)]
        else:
            parser.error("run needs --runs, repeated --run-name, or --arm/--law/--seed")
        width = arguments.chunk_runs or (1 if runs[0].arm == "a_forced" else 3)
        if width not in (1, 3) or (any(r.arm == "a_forced" for r in runs) and width != 1):
            parser.error("raw width is 3; hard A must use direct width 1")
        if not arguments.smoke and arguments.steps != 20000:
            parser.error("production endpoint remains 20,000 updates")
        output = arguments.output_root or (SMOKE_ROOT if arguments.smoke else OUTPUT)
        study = __import__(__name__, fromlist=["*"])
        result = []
        for at in range(0, len(runs), width):
            result.extend(execution.run_chunk(study, runs[at:at+width], DEVICE, output,
                arguments.bulk_root, steps=arguments.steps, smoke=arguments.smoke))
        print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
