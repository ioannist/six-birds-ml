"""Shared scientific sampling and scoring utilities for r8–r13."""
from __future__ import annotations
import numpy as np
import torch
from scripts import multiround_panels as choice
CONDITIONS = ('unaltered', 'A_ablated', 'raw_ablated', 'both_ablated')
NATURAL_DONOR_SEED = 2026100301
PREFIX_DONOR_SEED = 2026100303
CAVEAT = 'Because A is determined by the raw records, no such crossed-input test alone can establish which route a free network would choose on consistent data.'
INTERPRETATION = {'A_only': 'A-answer route dominates under this intervention', 'raw_only': 'raw-record route dominates under this intervention', 'neither': 'routes are operationally redundant under this intervention', 'both': 'routes cooperate, or the network reacts to route conflict'}

def donor_indices(count: int, seed: int, *, target_count: int | None=None) -> np.ndarray:
    """Sample legal donor episodes with replacement on an independent stream."""
    if count < 2 or (target_count is not None and target_count < 1):
        raise ValueError('donor population or target panel is empty')
    targets = count if target_count is None else target_count
    rng = np.random.default_rng(seed)
    donors = rng.integers(0, count, size=targets, dtype=np.int64)
    if targets == count:
        collision = donors == np.arange(count)
        while collision.any():
            donors[collision] = rng.integers(0, count, size=int(collision.sum()))
            collision = donors == np.arange(count)
    return donors

def route_inputs(target_A: torch.Tensor, target_raw: torch.Tensor, donor_A: torch.Tensor, donor_raw: torch.Tensor, condition: str) -> tuple[torch.Tensor, torch.Tensor]:
    if condition not in CONDITIONS:
        raise ValueError('route-ablation condition differs')
    if target_A.shape != donor_A.shape or target_raw.shape != donor_raw.shape:
        raise ValueError('paired route shapes differ')
    return (donor_A if condition in ('A_ablated', 'both_ablated') else target_A, donor_raw if condition in ('raw_ablated', 'both_ablated') else target_raw)

@torch.no_grad()
def predict_conditions(model: choice.ChoiceNetwork, records: np.ndarray, donors: np.ndarray, *, batch_size: int=128) -> tuple[dict[str, np.ndarray], dict]:
    """Execute all routes with paired legal donors and a shared target state."""
    if records.ndim != 4 or records.shape[2:] != (4, 2) or donors.shape != records.shape:
        raise ValueError('paired episode record shapes differ')
    outputs = {name: [] for name in CONDITIONS}
    changed = {'A_rounds': 0, 'raw_rounds': 0, 'total_rounds': 0}
    for offset in range(0, len(records), batch_size):
        left = torch.from_numpy(records[offset:offset + batch_size]).long()
        right = torch.from_numpy(donors[offset:offset + batch_size]).long()
        rows, rounds = left.shape[:2]
        _, target_A, target_raw = model.round_interfaces(left.reshape(-1, 4, 2))
        _, donor_A, donor_raw = model.round_interfaces(right.reshape(-1, 4, 2))
        target_A = target_A.reshape(rows, rounds, 5, -1)
        donor_A = donor_A.reshape(rows, rounds, 5, -1)
        target_raw = target_raw.reshape(rows, rounds, -1)
        donor_raw = donor_raw.reshape(rows, rounds, -1)
        changed['A_rounds'] += int((target_A != donor_A).any((-1, -2)).sum())
        changed['raw_rounds'] += int((target_raw != donor_raw).any(-1).sum())
        changed['total_rounds'] += rows * rounds
        for condition in CONDITIONS:
            A, raw = route_inputs(target_A, target_raw, donor_A, donor_raw, condition)
            state = None
            logits = []
            for at in range(rounds):
                prediction, state = model.upper_step(A[:, at], raw[:, at], state)
                logits.append(prediction)
            outputs[condition].append(torch.softmax(torch.stack(logits, 1), -1).numpy())
    return ({name: np.concatenate(rows) for name, rows in outputs.items()}, changed)

def damage(unaltered: dict, altered: dict, *, equal: bool) -> dict:
    changes = {'natural_KL_increase_bits': altered['natural_excess_KL_bits'] - unaltered['natural_excess_KL_bits'], 'law_max_TV_increase': altered['mode_law']['maximum_TV'] - unaltered['mode_law']['maximum_TV']}
    if equal:
        changes['witness_pair_TV_increase'] = altered['mode_law']['witness_pair_mean_prediction_TV'] - unaltered['mode_law']['witness_pair_mean_prediction_TV']
        witness = changes['witness_pair_TV_increase'] > 0.02
    else:
        changes['witness_recovery_decline'] = unaltered['mode_law']['witness_recovery_fraction'] - altered['mode_law']['witness_recovery_fraction']
        witness = changes['witness_recovery_decline'] > 0.2
    changes['damaged'] = bool(changes['natural_KL_increase_bits'] > 0.01 or changes['law_max_TV_increase'] > 0.02 or witness)
    return changes

def interpretation(A_damaged: bool, raw_damaged: bool) -> str:
    key = 'both' if A_damaged and raw_damaged else 'A_only' if A_damaged else 'raw_only' if raw_damaged else 'neither'
    return INTERPRETATION[key]
