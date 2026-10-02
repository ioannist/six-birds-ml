"""Exact five-slot predictive law and finite legal-board sampler."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from . import game
from .memory import VALUES, VALUE_INDEX
from .multiround import Boards
from .multiround_choice import ChoiceNetwork
from .multiround_jagged import JaggedNetwork, rendering_ids


VALUES36 = tuple(int(value) for value in VALUES)
assert len(VALUES36) == 36 and VALUES36[0] == 0
ROW = tuple(
    (Fraction(10 + 7 * (i // 6), 100),
     Fraction(10 + 7 * (i % 6), 100),
     Fraction(80 - 7 * (i // 6 + i % 6), 100))
    for i in range(36)
)
EQUAL_ROW = (Fraction(1, 3),) * 3
ROW_FLOAT = np.asarray(ROW, dtype=np.float64)
EQUAL_FLOAT = np.asarray(EQUAL_ROW, dtype=np.float64)


def check_law() -> dict:
    if len(set(ROW)) != 36 or any(sum(p) != 1 or min(p) <= 0 for p in ROW):
        raise ValueError("36-row law differs")
    minimum = min(sum(abs(a - b) for a, b in zip(ROW[i], ROW[j])) / 2
                  for i in range(36) for j in range(i + 1, 36))
    if minimum != Fraction(7, 100):
        raise ValueError("36-row separation differs")
    return {"rows": 36, "minimum_pairwise_TV": str(minimum)}


def category(board: tuple[int, ...]) -> int:
    return sum(board) % 3


def update(last_nonzero: np.ndarray, board: tuple[int, ...]) -> np.ndarray:
    result = np.asarray(last_nonzero, dtype=np.int64).copy()
    board_values = np.asarray(board, dtype=np.int64)
    if result.shape != (5,):
        raise ValueError("five-slot state differs")
    result[board_values > 0] = board_values[board_values > 0]
    return result


def law_row(last_nonzero: np.ndarray, query: int, *, equal: bool = False) -> np.ndarray:
    if query not in range(5):
        raise ValueError("public query differs")
    return EQUAL_FLOAT.copy() if equal else ROW_FLOAT[VALUE_INDEX[int(last_nonzero[query])]].copy()


@dataclass(frozen=True)
class Episodes:
    boards: np.ndarray
    queries: np.ndarray
    targets: np.ndarray
    lengths: np.ndarray
    rendering_seeds: np.ndarray
    last_nonzero: np.ndarray


class CoverageSampler:
    """Half uniform and half supported-slot-value sampling within each Q."""

    def __init__(self, boards: Boards, board_ids: np.ndarray | None = None) -> None:
        self.boards = boards
        self.ids = (np.arange(len(boards.boards), dtype=np.int64) if board_ids is None
                    else np.asarray(board_ids, dtype=np.int64))
        if len(np.unique(self.ids)) != len(self.ids):
            raise ValueError("board identities repeat")
        self.id_set = set(map(int, self.ids))
        self.by_q = tuple(np.asarray([i for i in self.ids if category(boards.boards[int(i)]) == q],
                                     dtype=np.int64) for q in range(3))
        self.pairs = []
        self.by_pair = []
        for q in range(3):
            groups = defaultdict(list)
            for board_id in self.by_q[q]:
                for slot, value in enumerate(boards.boards[int(board_id)]):
                    groups[(slot, value)].append(int(board_id))
            pairs = tuple(sorted(groups))
            self.pairs.append(pairs)
            self.by_pair.append(tuple(np.asarray(groups[pair], dtype=np.int64)
                                      for pair in pairs))
        self.pairs = tuple(self.pairs)
        self.by_pair = tuple(self.by_pair)

    def draw(self, q: int, rng: np.random.Generator) -> int:
        if q not in range(3):
            raise ValueError("category differs")
        if int(rng.integers(2)) == 0:
            group = self.by_q[q]
        else:
            group = self.by_pair[q][int(rng.integers(len(self.pairs[q])))]
        return int(group[int(rng.integers(len(group)))])

    def conditional_frequencies(self) -> list[list[list[Fraction]]]:
        """Exact P(board slot k has value v | sampled category Q)."""

        result = []
        for q in range(3):
            rows = [[Fraction(0) for _ in VALUES36] for _ in range(5)]
            size = len(self.by_q[q])
            pair_count = len(self.pairs[q])
            for board_id in self.by_q[q]:
                for slot, value in enumerate(self.boards.boards[int(board_id)]):
                    rows[slot][VALUE_INDEX[value]] += Fraction(1, 2 * size)
            for group in self.by_pair[q]:
                weight = Fraction(1, 2 * pair_count * len(group))
                for board_id in group:
                    for slot, value in enumerate(self.boards.boards[int(board_id)]):
                        rows[slot][VALUE_INDEX[value]] += weight
            if any(sum(row) != 1 for row in rows):
                raise ValueError("conditional board frequency differs")
            result.append(rows)
        return result


def sample_episodes(sampler: CoverageSampler, count: int, rounds: int, seed: int,
                    *, equal: bool = False) -> Episodes:
    rng = np.random.default_rng(seed)
    board_ids = np.empty((count, rounds), dtype=np.int64)
    queries = rng.integers(0, 5, (count, rounds), dtype=np.int64)
    targets = np.empty((count, rounds), dtype=np.int64)
    render = rng.integers(0, 2**63 - 1, (count, rounds), dtype=np.int64)
    states = np.empty((count, rounds, 5), dtype=np.int64)
    for episode in range(count):
        state = np.zeros(5, dtype=np.int64)
        next_q = int(rng.integers(3))  # Publicly declared initial-board choice.
        for at in range(rounds):
            board_id = sampler.draw(next_q, rng)
            board_ids[episode, at] = board_id
            state = update(state, sampler.boards.boards[board_id])
            states[episode, at] = state
            next_q = int(rng.choice(3, p=law_row(state, int(queries[episode, at]),
                                                    equal=equal)))
            targets[episode, at] = next_q
    return Episodes(board_ids, queries, targets, np.full(count, rounds, dtype=np.int64),
                    render, states)


def oracle_rows(panel: Episodes, *, equal: bool = False) -> np.ndarray:
    indices = np.vectorize(VALUE_INDEX.__getitem__)(
        np.take_along_axis(panel.last_nonzero, panel.queries[..., None], -1)[..., 0])
    return np.broadcast_to(EQUAL_FLOAT, (*indices.shape, 3)).copy() if equal else ROW_FLOAT[indices]


def verify_panel(panel: Episodes, sampler: CoverageSampler, *, equal: bool) -> dict:
    if not (panel.boards.shape == panel.queries.shape == panel.targets.shape ==
            panel.rendering_seeds.shape):
        raise ValueError("episode panel dimensions differ")
    if panel.last_nonzero.shape != (*panel.boards.shape, 5):
        raise ValueError("episode state dimensions differ")
    for episode in range(len(panel.boards)):
        state = np.zeros(5, dtype=np.int64)
        for at, board_id in enumerate(panel.boards[episode]):
            if int(board_id) not in sampler.id_set:
                raise ValueError("episode board outside declared pool")
            board = sampler.boards.boards[int(board_id)]
            if at and category(board) != int(panel.targets[episode, at - 1]):
                raise ValueError("next board category differs from sampled target")
            state = update(state, board)
            if not np.array_equal(state, panel.last_nonzero[episode, at]):
                raise ValueError("episode exact state differs")
            if int(panel.queries[episode, at]) not in range(5):
                raise ValueError("episode public query differs")
    return {"episodes": len(panel.boards), "rounds": int(panel.boards.size),
            "exact_state_replay": True, "sampled_category_link": True,
            "equal_law": equal}


def mode_blind_row(rows: np.ndarray) -> np.ndarray:
    mean = rows.reshape(-1, 3).mean(axis=0)
    if not np.isclose(mean.sum(), 1):
        raise ValueError("mode-blind row differs")
    return mean


def eligible_pairs(boards: Boards, ids: np.ndarray) -> dict[int, list[tuple[int, int]]]:
    result = {}
    for slot in range(5):
        grouped = defaultdict(list)
        for board_id in ids:
            board = boards.boards[int(board_id)]
            if board[slot] > 0:
                grouped[board[:slot] + board[slot + 1:]].append(int(board_id))
        pairs = []
        for group in grouped.values():
            for left_index, left in enumerate(group):
                for right in group[left_index + 1:]:
                    a = ROW[VALUE_INDEX[boards.boards[left][slot]]]
                    b = ROW[VALUE_INDEX[boards.boards[right][slot]]]
                    if sum(abs(x - y) for x, y in zip(a, b)) / 2 >= Fraction(7, 100):
                        pairs.append((left, right))
        result[slot] = pairs
    return result


class AllSlotsNetwork(ChoiceNetwork):
    """Public-query recurrence; B never receives the hidden state or target Q."""

    def __init__(self, arm: str, seed: int, frozen_core=None) -> None:
        if arm not in ("free", "free_a", "a_forced"):
            raise ValueError("all-slots arm differs")
        torch.manual_seed(seed)
        super().__init__()
        self.arm = arm
        self.upper = nn.GRUCell(32 + 16 + 5, 32)
        self.raw_sum_head = nn.Linear(16, 5 * 36)
        if frozen_core is not None:
            self.memory.load_state_dict(frozen_core.state_dict(), strict=True)
        self.memory.requires_grad_(False)
        self.memory.eval()

    def train(self, mode: bool = True):
        super().train(mode)
        self.memory.eval()
        return self

    def upper_step(self, answers: torch.Tensor, raw: torch.Tensor,
                   query: torch.Tensor, previous: torch.Tensor | None = None):
        if query.ndim != 1 or len(query) != len(raw):
            raise ValueError("public query input differs")
        if previous is None:
            previous = raw.new_zeros((len(raw), 32))
        if self.arm == "a_forced":
            raw = torch.zeros_like(raw)
        else:
            answers = torch.zeros_like(answers)
        carried = torch.cat((self.answer_embedding(answers.flatten(1)), raw,
                             F.one_hot(query, 5).to(raw.dtype)), -1)
        state = JaggedNetwork._gru_cell(carried, previous, self.upper.weight_ih,
            self.upper.weight_hh, self.upper.bias_ih, self.upper.bias_hh)
        return self.category_head(state), state

    def round_interfaces(self, records):
        # Explicit GRU equations give the same raw encoder while admitting vmap.
        # Raw arms do not evaluate the inactive hard-A interface.
        symbols = self.raw_embedding(records[..., 0] * 6 + records[..., 1])
        raw = symbols.new_zeros((len(records), 16))
        for at in range(4):
            raw = JaggedNetwork._gru_cell(symbols[:, at], raw,
                self.raw_encoder.weight_ih_l0, self.raw_encoder.weight_hh_l0,
                self.raw_encoder.bias_ih_l0, self.raw_encoder.bias_hh_l0)
        if self.arm != "a_forced":
            zeros = raw.new_zeros((len(records), 5, 36))
            return zeros, zeros, raw
        logits, answers, _ = super().round_interfaces(records)
        return logits, answers, raw

    def forward(self, records: torch.Tensor, queries: torch.Tensor,
                lengths: torch.Tensor, *, return_trace: bool = False):
        if records.ndim != 4 or records.shape[2:] != (4, 2):
            raise ValueError("episode records differ")
        if queries.shape != records.shape[:2] or lengths.shape != records.shape[:1]:
            raise ValueError("public queries or episode lengths differ")
        batch, rounds = records.shape[:2]
        _, answers, raw = self.round_interfaces(records.reshape(batch * rounds, 4, 2))
        raw_sum = self.raw_sum_head(raw).reshape(batch, rounds, 5, 36)
        answers = answers.reshape(batch, rounds, 5, 36)
        raw = raw.reshape(batch, rounds, 16)
        state = None
        logits, states = [], []
        for at in range(rounds):
            row, state = self.upper_step(answers[:, at], raw[:, at], queries[:, at], state)
            logits.append(row)
            states.append(state)
        result = torch.stack(logits, 1)
        if return_trace:
            return {"logits": result, "raw_states": raw,
                    "upper_states": torch.stack(states, 1), "A_logits": raw_sum,
                    "frozen_A_answers": answers}
        return result, raw_sum


class ExecutedOracle(nn.Module):
    """Reconstruct five sums and last nonzero memory from executed records."""

    def __init__(self, *, equal=False):
        super().__init__()
        self.equal = equal
        self.register_buffer("masses", torch.tensor(game.MASSES))
        self.register_buffer("values", torch.tensor(VALUES36))
        self.register_buffer("rows", torch.tensor(ROW_FLOAT, dtype=torch.float32))

    def round_interfaces(self, records):
        sums = torch.zeros((len(records), 5), device=records.device, dtype=torch.long)
        sums.scatter_add_(1, records[..., 0], self.masses[records[..., 1]])
        answers = F.one_hot(torch.searchsorted(self.values, sums), 36).float()
        return answers, answers, torch.zeros((len(records), 16), device=records.device)

    def upper_step(self, answers, raw, query, previous=None):
        sums = self.values[answers.argmax(-1)]
        previous = torch.zeros_like(sums) if previous is None else previous
        state = torch.where(sums > 0, sums, previous)
        value = state.gather(1, query[:, None])[:, 0]
        rows = self.rows[torch.searchsorted(self.values, value)]
        if self.equal:
            rows = torch.ones_like(rows) / 3
        return rows.log(), state

    def forward(self, records, queries, lengths):
        state, rows = None, []
        for at in range(records.shape[1]):
            _, answers, raw = self.round_interfaces(records[:, at])
            row, state = self.upper_step(answers, raw, queries[:, at], state)
            rows.append(row)
        return torch.stack(rows, 1), answers


@dataclass
class DeviceEpisodes:
    records: torch.Tensor
    boards: torch.Tensor
    queries: torch.Tensor
    targets: torch.Tensor
    lengths: torch.Tensor
    sums: torch.Tensor
    remembered: torch.Tensor
    categories: torch.Tensor


class DeviceCoverageStream:
    """Device-resident finite coverage mixture with independent seeded streams."""

    def __init__(self, tables, sampler, seed, *, equal=False):
        self.tables, self.equal = tables, equal
        device = tables.device
        self.generators = [torch.Generator(device=device).manual_seed(
            2026101001 + seed + 100 * equal + offset) for offset in (0, 100000, 200000)]
        self.rows = torch.tensor(ROW_FLOAT, device=device, dtype=torch.float32)
        self.values = torch.tensor(VALUES36, device=device)
        self.q_pools = [torch.tensor(x, device=device) for x in sampler.by_q]
        flat, offsets, sizes = [], [], []
        for groups in sampler.by_pair:
            for group in groups:
                offsets.append(len(flat)); sizes.append(len(group)); flat.extend(group.tolist())
        self.flat = torch.tensor(flat, device=device)
        self.offsets = torch.tensor(offsets, device=device).reshape(3, 150)
        self.sizes = torch.tensor(sizes, device=device).reshape(3, 150)
        self.current = torch.zeros((5, 36), device=device, dtype=torch.long)
        self.current_by_Q = torch.zeros((3, 5, 36), device=device, dtype=torch.long)
        self.current_queried = torch.zeros((5, 36), device=device, dtype=torch.long)
        self.remembered_queried = torch.zeros_like(self.current)
        self.board_counts = torch.zeros(24435, device=device, dtype=torch.long)
        self.rendering_counts = torch.zeros(30**4, device=device, dtype=torch.long)
        self.placement_counts = torch.zeros_like(self.rendering_counts)
        self.draws, self.rolling = 0, bytes(32)

    def draw(self, batch=256, rounds=8):
        device = self.tables.device
        category_rng, board_rng, render_rng = self.generators
        rand = lambda shape, generator: torch.rand(shape, device=device, generator=generator)
        queries = torch.randint(5, (batch, rounds), device=device, generator=category_rng)
        next_q = (rand((batch,), category_rng) * 3).long()
        remembered = torch.zeros((batch, 5), device=device, dtype=torch.long)
        board_rows, target_rows, memory_rows, category_rows = [], [], [], []
        for at in range(rounds):
            mixture = rand((batch,), board_rng) < .5
            pair = (rand((batch,), board_rng) * 150).long()
            uniform = rand((batch,), board_rng)
            selected = torch.zeros(batch, device=device, dtype=torch.long)
            for q, pool in enumerate(self.q_pools):
                selected = torch.where(next_q == q, pool[(uniform * len(pool)).long()], selected)
            index = self.offsets[next_q, pair] + (uniform * self.sizes[next_q, pair]).long()
            selected = torch.where(mixture, self.flat[index], selected)
            sums = self.tables.board_sums[selected]
            remembered = torch.where(sums > 0, sums, remembered)
            remembered_index = torch.searchsorted(self.values, remembered.contiguous())
            probability = self.rows[remembered_index.gather(1, queries[:, at:at + 1])[:, 0]]
            if self.equal:
                probability = torch.ones_like(probability) / 3
            u = rand((batch,), category_rng)
            target = (u[:, None] > probability.cumsum(-1)).sum(-1).clamp_max(2)
            board_rows.append(selected); target_rows.append(target)
            memory_rows.append(remembered.clone()); category_rows.append(next_q)
            indices = torch.searchsorted(self.values, sums.contiguous())
            ones = torch.ones(batch, device=device, dtype=torch.long)
            for slot in range(5):
                self.current[slot].index_add_(0, indices[:, slot], ones)
                flat_counts = self.current_by_Q[:, slot].reshape(-1).clone()
                flat_counts.index_add_(0, next_q * 36 + indices[:, slot], ones)
                self.current_by_Q[:, slot] = flat_counts.reshape(3, 36)
            self.current_queried.view(-1).index_add_(0,
                queries[:, at] * 36 + indices.gather(1, queries[:, at:at + 1])[:, 0], ones)
            self.remembered_queried.view(-1).index_add_(0,
                queries[:, at] * 36 + remembered_index.gather(1, queries[:, at:at + 1])[:, 0], ones)
            next_q = target
        ids = torch.stack(board_rows, 1)
        counts = self.tables.placement_counts[ids].long()
        placement = (rand(ids.shape, render_rng) * counts).long()
        packed = self.tables.placements[ids, placement].long()
        order = torch.randint(6, ids.shape, device=device, generator=render_rng)
        permuted = packed.gather(2, self.tables.orders[order])
        records = torch.stack((permuted // 6, permuted % 6), -1)
        ones = torch.ones(ids.numel(), device=device, dtype=torch.long)
        self.board_counts.index_add_(0, ids.flatten(), ones)
        self.rendering_counts.index_add_(0, rendering_ids(records).flatten(), ones)
        self.placement_counts.index_add_(0, rendering_ids(torch.stack((packed // 6, packed % 6), -1)).flatten(), ones)
        result = DeviceEpisodes(records, ids, queries, torch.stack(target_rows, 1),
            torch.full((batch,), rounds, device=device, dtype=torch.long), self.tables.board_sums[ids],
            torch.stack(memory_rows, 1), torch.stack(category_rows, 1))
        digest = __import__("hashlib").sha256(self.rolling)
        for value in vars(result).values():
            digest.update(value.cpu().numpy().tobytes())
        self.rolling, self.draws = digest.digest(), self.draws + 1
        return result

    def state(self):
        return {"generators": [g.get_state() for g in self.generators], "draws": self.draws,
                "rolling": self.rolling.hex(), **{key: getattr(self, key).cpu().clone() for key in (
                    "current", "current_by_Q", "current_queried", "remembered_queried", "board_counts",
                    "rendering_counts", "placement_counts")}}

    def restore(self, state):
        for generator, value in zip(self.generators, state["generators"], strict=True):
            generator.set_state(value.cpu())
        self.draws, self.rolling = state["draws"], bytes.fromhex(state["rolling"])
        for key in state.keys() - {"generators", "draws", "rolling"}:
            setattr(self, key, state[key].to(self.tables.device).clone())
