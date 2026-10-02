"""Completed-board process, exact oracle, and frozen-A upper recurrence."""

from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from recombination_promotion.serialization.minimal_recombination import (
    DEFAULT_MASS_VOCAB, DEFAULT_TEMPLATE_NAMES, MinimalConfig,
    _parse_visible_prompt, answer_for_config, serialize_config, solve_from_visible_tokens,
)

from . import game
from .continuous import history_digest
from .memory import MemoryNetwork, VALUE_INDEX, history_split


P = ((Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
     (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)))
P_EQUAL = (Fraction(3, 8), Fraction(1, 4), Fraction(3, 8))
CATEGORY_NAMES = ("L", "N", "H")
TRAIN_EPISODES, TRAIN_ROUNDS = 40_000, 8
TEST_EPISODES, TEST_ROUNDS = 5_000, 12
TRAIN_DATA_SEED, TEST_DATA_SEED = 2026092801, 2026092802
RENDER_SEED = 2026092803
A_CHECKPOINT = Path("reports/phase11/oldgame_memory/continuous/"
                    "continuous_seed0_r7/trajectories/parent_A_step_002000.pt")


def board_category(board: tuple[int, ...]) -> int:
    value = board[0]
    return 0 if value <= 12 else 2 if value >= 24 else 1


@dataclass(frozen=True)
class Boards:
    boards: tuple[tuple[int, ...], ...]
    placements: dict[tuple[int, ...], tuple[int, ...]]
    by_category: tuple[tuple[int, ...], ...]

    def placement(self, board_index: int, generator: np.random.Generator) -> tuple[int, ...]:
        candidates = self.placements[self.boards[board_index]]
        packed = candidates[int(generator.integers(len(candidates)))]
        return tuple((packed // (30 ** position)) % 30 for position in range(4))


def enumerate_boards() -> Boards:
    """Enumerate ordered four-record placements without changing the old game."""

    grouped: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for choices in product(range(30), repeat=4):
        board = [0] * 5
        packed = 0
        for position, choice in enumerate(choices):
            slot, mass_index = divmod(choice, len(game.MASSES))
            board[slot] += game.MASSES[mass_index]
            packed += choice * 30 ** position
        grouped[tuple(board)].append(packed)
    boards = tuple(sorted(grouped))
    by_category = tuple(tuple(index for index, board in enumerate(boards)
                              if board_category(board) == category)
                        for category in range(3))
    counts = tuple(len(section) for section in by_category)
    if len(boards) != 24_435 or counts != (22_491, 1_835, 109):
        raise ValueError(f"completed-board enumeration differs: {len(boards)}, {counts}")
    if sum(map(len, grouped.values())) != 30 ** 4:
        raise ValueError("ordered placement census differs")
    return Boards(boards, {board: tuple(values) for board, values in grouped.items()},
                  by_category)


def update_mode(mode: int, category: int) -> int:
    if mode not in (0, 1) or category not in range(3):
        raise ValueError("mode or board category differs")
    return 0 if category == 0 else 1 if category == 2 else mode


def entropy_bits(probabilities: tuple[Fraction, ...]) -> float:
    return -sum(float(value) * math.log2(float(value)) for value in probabilities if value)


def kl_bits(truth: tuple[Fraction, ...], predicted: tuple[float, ...]) -> float:
    if any(value <= 0 for value in predicted):
        raise ValueError("predictive row has a nonpositive probability")
    return sum(float(value) * math.log2(float(value) / predicted[index])
               for index, value in enumerate(truth))


def mix(q: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    return tuple((1 - q) * p0 + q * p1 for p0, p1 in zip(P[0], P[1]))


def oracle() -> dict:
    middle = mix(Fraction(1, 2))
    js = entropy_bits(middle) - (entropy_bits(P[0]) + entropy_bits(P[1])) / 2
    rows = []
    for round_index in range(1, TEST_ROUNDS + 1):
        q = Fraction(1, 2) * (1 - Fraction(1, 2 ** (round_index - 1)))
        predicted = mix(q)
        conditional = (float(1 - q) * kl_bits(P[0], tuple(map(float, predicted)))
                       + float(q) * kl_bits(P[1], tuple(map(float, predicted))))
        rows.append({"round": round_index, "q_mode1_given_N": [q.numerator, q.denominator],
                     "A_only_excess_bits": conditional / 4})
    if (P[0] != (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
            or P[1] != (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2))
            or abs(entropy_bits(P[0]) - 1.5) > 1e-12
            or abs(entropy_bits(P[1]) - 1.5) > 1e-12
            or abs(js - 0.06127812445913283) > 1e-10):
        raise ValueError("exact mode-law oracle differs")
    return {"ideal_loss_bits": 1.5, "witness_JS_bits": js,
            "p0_rational": [[p.numerator, p.denominator] for p in P[0]],
            "p1_rational": [[p.numerator, p.denominator] for p in P[1]],
            "equal_p_rational": [[p.numerator, p.denominator] for p in P_EQUAL],
            "natural_A_only_excess": rows}


def render_board(boards: Boards, board_index: int, *, seed: int) -> dict:
    """Use the Stage-1 serializer and parser with fresh round-specific names."""

    rng = np.random.default_rng(seed)
    choices = boards.placement(board_index, rng)
    order = list(range(3))
    rng.shuffle(order)
    order.append(3)
    slots = list(range(5))
    rng.shuffle(slots)
    template = DEFAULT_TEMPLATE_NAMES[int(rng.integers(3))]
    placements = tuple((DEFAULT_MASS_VOCAB[choices[index] % 6],
                        f"h{choices[index] // 6}") for index in order)
    config = MinimalConfig(config_id=f"multiround_{seed}_{board_index}",
                           placements=placements,
                           query_order=tuple(f"h{slot}" for slot in slots),
                           template=template, nonce_binding="random")
    tokens = serialize_config(config, p=5)
    parsed, query_order, parsed_template = _parse_visible_prompt(tokens, p=5)
    if parsed != placements or query_order != config.query_order or parsed_template != template:
        raise ValueError("Stage-1 rendering or binding resolution differs")
    histories = tuple(tuple(game.MASSES[DEFAULT_MASS_VOCAB.index(mass)]
                            for mass, slot in parsed if slot == f"h{index}")
                      for index in range(5))
    if tuple(game.sigma(history) for history in histories) != boards.boards[board_index]:
        raise ValueError("rendered board differs from selected completed board")
    if solve_from_visible_tokens(tokens, p=5) != answer_for_config(config, p=5):
        raise ValueError("visible-token answer differs")
    return {"tokens": tokens, "histories": histories, "template": template,
            "query_order": query_order, "placements": placements}


@dataclass(frozen=True)
class Episodes:
    boards: np.ndarray
    categories: np.ndarray
    modes: np.ndarray
    targets: np.ndarray
    lengths: np.ndarray
    rendering_seeds: np.ndarray


def episodes(boards: Boards, count: int, rounds: int, seed: int,
             *, equal_p: bool = False, stop_third_N: bool = False) -> Episodes:
    rng = np.random.default_rng(seed)
    board_ids = np.full((count, rounds), -1, dtype=np.int32)
    categories = np.full((count, rounds), -1, dtype=np.int8)
    modes = np.full((count, rounds), -1, dtype=np.int8)
    targets = np.full((count, rounds), -1, dtype=np.int8)
    rendering_seeds = rng.integers(0, 2 ** 63 - 1, (count, rounds), dtype=np.int64)
    lengths = np.full(count, rounds, dtype=np.int8)
    for episode in range(count):
        mode = 0
        neutral_run = 0
        pending_category = None
        for at in range(rounds):
            if pending_category is None:
                value = int(rng.integers(8))
                category = (0 if value < 3 else 1 if value < 5 else 2) if equal_p else (
                    0 if value < 4 else 1 if value < 6 else 2)
            else:
                category = pending_category
            if stop_third_N and category == 1 and neutral_run == 2:
                # The previous round's target remains observed, but this
                # third N contributes neither an input nor a loss.
                lengths[episode] = at
                break
            categories[episode, at] = category
            choices = boards.by_category[category]
            board_ids[episode, at] = choices[int(rng.integers(len(choices)))]
            mode = update_mode(mode, category)
            modes[episode, at] = mode
            neutral_run = neutral_run + 1 if category == 1 else 0
            # The next target is drawn from the current mode, with no selection
            # or rejection based on that target.
            next_value = int(rng.integers(8))
            if equal_p:
                pending_category = 0 if next_value < 3 else 1 if next_value < 5 else 2
            elif mode == 0:
                pending_category = 0 if next_value < 4 else 1 if next_value < 6 else 2
            else:
                pending_category = 0 if next_value < 2 else 1 if next_value < 4 else 2
            targets[episode, at] = pending_category
    return Episodes(board_ids, categories, modes, targets, lengths, rendering_seeds)


def unseen_past_pairs(train: Episodes, test: Episodes) -> np.ndarray:
    known = set()
    for episode in range(len(train.lengths)):
        for at in range(2, int(train.lengths[episode])):
            known.add((int(train.boards[episode, at - 2]),
                       int(train.boards[episode, at - 1])))
    return np.array([[at < int(test.lengths[episode]) and at >= 2
                      and (int(test.boards[episode, at - 2]),
                                   int(test.boards[episode, at - 1])) not in known
                      for at in range(test.boards.shape[1])]
                     for episode in range(len(test.lengths))], dtype=bool)


def load_frozen_A(repo_root: Path) -> tuple[MemoryNetwork, dict]:
    path = repo_root / A_CHECKPOINT
    saved = torch.load(path, map_location="cpu", weights_only=False)
    split = history_split(0)
    if (saved["seed"] != 0 or saved["arm"] != "parent_A" or saved["step"] != 2000
            or saved["history_sha256"] != history_digest(game.histories())
            or saved["train_sha256"] != history_digest(split.train)
            or saved["scores"]["all"]["sum"] != {"correct": 1555, "total": 1555}):
        raise ValueError("frozen A checkpoint authority differs")
    model = MemoryNetwork(width=saved["width"])
    model.load_state_dict(saved["model"])
    model.eval()
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    histories = game.histories()
    with torch.no_grad():
        predicted = []
        for offset in range(0, len(histories), 256):
            predicted.extend(model(histories[offset:offset + 256],
                                   kind=game.KIND_SUM).logits.argmax(-1).tolist())
    correct = sum(predicted[index] == VALUE_INDEX[game.sigma(history)]
                  for index, history in enumerate(histories))
    if correct != 1555:
        raise ValueError("frozen A sum answers differ on legal histories")
    return model, {"checkpoint": str(A_CHECKPOINT),
                   "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                   "all_history_sum_correct": correct, "all_history_count": len(histories)}


@torch.no_grad()
def cache_board_answers(model: MemoryNetwork, boards: Boards) -> np.ndarray:
    histories = []
    for board in boards.boards:
        packed = boards.placements[board][0]
        placements = tuple((packed // (30 ** position)) % 30 for position in range(4))
        histories.extend(tuple(game.MASSES[choice % 6] for choice in placements
                               if choice // 6 == slot) for slot in range(5))
    predicted = []
    for offset in range(0, len(histories), 512):
        result = model(histories[offset:offset + 512], kind=game.KIND_SUM)
        predicted.extend(int(value) for value in result.logits.argmax(-1).tolist())
    values = np.empty((len(boards.boards), 5), dtype=np.int16)
    inverse = {index: value for value, index in VALUE_INDEX.items()}
    for index in range(len(boards.boards)):
        values[index] = [inverse[predicted[5 * index + slot]] for slot in range(5)]
    true = np.asarray(boards.boards, dtype=np.int16)
    if not np.array_equal(values, true):
        raise ValueError("frozen A board-answer cache differs from exact sums")
    return values


def episode_inputs(episodes: Episodes, answer_cache: np.ndarray) -> np.ndarray:
    """Materialize only frozen-A answers; padding carries no observation."""

    if answer_cache.shape[1] != 5:
        raise ValueError("frozen A cache must have five per-slot answers")
    valid = episodes.boards >= 0
    if np.any(episodes.boards[valid] >= len(answer_cache)):
        raise ValueError("episode board lies outside the frozen A cache")
    answers = np.zeros((*episodes.boards.shape, 5), dtype=np.int64)
    answers[valid] = answer_cache[episodes.boards[valid]]
    if not np.array_equal(answers[valid], answer_cache[episodes.boards[valid]]):
        raise ValueError("upper input differs from frozen A answers")
    return answers


class UpperGRU(nn.Module):
    def __init__(self, width: int = 32) -> None:
        super().__init__()
        self.sum_embedding = nn.Embedding(37, 8)
        self.gru = nn.GRU(5 * 8, width, batch_first=True)
        self.head = nn.Linear(width, 3)

    def forward(self, sums: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        if sums.ndim != 3 or sums.shape[-1] != 5 or sums.dtype != torch.long:
            raise ValueError("upper input is not five categorical A sum answers")
        if torch.any(sums < 0) or torch.any(sums > 36):
            raise ValueError("upper A sum answer exceeds the old-game vocabulary")
        packed = nn.utils.rnn.pack_padded_sequence(
            self.sum_embedding(sums).flatten(-2), lengths.cpu(),
            batch_first=True, enforce_sorted=False)
        output, _ = self.gru(packed)
        padded, _ = nn.utils.rnn.pad_packed_sequence(
            output, batch_first=True, total_length=sums.shape[1])
        return self.head(padded)


class CurrentBoardHead(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.sum_embedding = nn.Embedding(37, 8)
        self.round_embedding = nn.Embedding(13, 8)
        self.head = nn.Sequential(nn.Linear(48, 32), nn.Tanh(), nn.Linear(32, 3))

    def forward(self, sums: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        if sums.ndim != 3 or sums.shape[-1] != 5 or sums.dtype != torch.long:
            raise ValueError("current-board input is not five categorical A sums")
        rounds = torch.arange(sums.shape[1], device=sums.device).expand(len(sums), -1)
        state = torch.cat((self.sum_embedding(sums).flatten(-2),
                           self.round_embedding(rounds)), -1)
        return self.head(state)


def masked_cross_entropy(logits: torch.Tensor, targets: torch.Tensor,
                         lengths: torch.Tensor) -> torch.Tensor:
    positions = torch.arange(targets.shape[1], device=targets.device)[None, :]
    active = positions < lengths[:, None]
    return F.cross_entropy(logits[active], targets[active])
