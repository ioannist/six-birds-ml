"""Device-resident records and grouped networks for the jagged-competence study."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from . import game
from .memory import VALUES
from .multiround import Boards, enumerate_boards, load_frozen_A
from .multiround_choice import ChoiceNetwork


DRAW_KINDS = ("uniform", "cutoff", "decoy")
BOUNDARY_SUMS = {"cutoff": ((12,), (13, 23), (24,)),
                 "decoy": ((10,), (16, 20), (27,))}
RECORD_ORDERS = torch.tensor(((0, 1, 2, 3), (0, 2, 1, 3),
                              (1, 0, 2, 3), (1, 2, 0, 3),
                              (2, 0, 1, 3), (2, 1, 0, 3)), dtype=torch.long)


def rendering_ids(records: torch.Tensor) -> torch.Tensor:
    """Injective base-30 identity of the four executed (slot, mass-index) records."""
    symbols = records[..., 0] * 6 + records[..., 1]
    powers = torch.tensor([30 ** at for at in range(4)], device=records.device)
    return (symbols * powers).sum(-1)


def batch_digest(previous: bytes, batch: "DeviceBatch") -> bytes:
    digest = hashlib.sha256(previous)
    for name in ("board_ids", "categories", "targets", "active", "lengths",
                 "placement_indices", "placements", "render_order", "records"):
        value = getattr(batch, name).detach().cpu().contiguous().numpy()
        digest.update(name.encode())
        digest.update(str(value.dtype).encode())
        digest.update(np.asarray(value.shape, dtype="<i8").tobytes())
        digest.update(value.tobytes())
    return digest.digest()


@dataclass
class DeviceBatch:
    records: torch.Tensor
    lengths: torch.Tensor
    targets: torch.Tensor
    categories: torch.Tensor
    board_ids: torch.Tensor
    active: torch.Tensor
    sums: torch.Tensor
    render_order: torch.Tensor
    placement_indices: torch.Tensor
    placements: torch.Tensor


class BoardTables:
    """The enumerated old-game boards and placements, transferred once per device."""

    def __init__(self, device: torch.device, boards: Boards | None = None):
        boards = enumerate_boards() if boards is None else boards
        self.device = device
        self.board_sums = torch.tensor(boards.boards, dtype=torch.long, device=device)
        self.categories = torch.where(self.board_sums[:, 0] <= 12, 0,
                                      torch.where(self.board_sums[:, 0] >= 24, 2, 1))
        self.by_category = []
        self.by_sum = []
        for category in range(3):
            self.by_category.append(torch.tensor(boards.by_category[category],
                                                 dtype=torch.long, device=device))
        for value in range(37):
            self.by_sum.append(torch.nonzero(self.board_sums[:, 0] == value)[:, 0])
        maximum = max(len(boards.placements[board]) for board in boards.boards)
        placement = np.zeros((len(boards.boards), maximum, 4), dtype=np.int16)
        counts = np.zeros(len(boards.boards), dtype=np.int16)
        for index, board in enumerate(boards.boards):
            packed = boards.placements[board]
            counts[index] = len(packed)
            for offset, value in enumerate(packed):
                placement[index, offset] = [(value // 30 ** at) % 30 for at in range(4)]
        self.placements = torch.as_tensor(placement, device=device)
        self.placement_counts = torch.as_tensor(counts, device=device)
        self.orders = RECORD_ORDERS.to(device)
        if [len(self.by_sum[value]) for value in (10, 12, 13, 16, 20, 23, 24, 27)] != [
                285, 285, 285, 285, 25, 25, 25, 25]:
            raise ValueError("r11 boundary/decoy board counts differ")


class DeviceStream:
    """Independent seeded streams; every board and rendering draw stays on device."""

    def __init__(self, tables: BoardTables, seed: int, law: str, draw: str,
                 *, batch: int = 256, rounds: int = 8):
        if draw not in DRAW_KINDS or law not in ("original", "equal"):
            raise ValueError("r11 stream setting differs")
        self.tables, self.seed, self.law, self.draw = tables, seed, law, draw
        self.batch, self.rounds = batch, rounds
        self.category_rng = torch.Generator(device=tables.device)
        self.board_rng = torch.Generator(device=tables.device)
        self.render_rng = torch.Generator(device=tables.device)
        self.category_rng.manual_seed(202609290000 + seed + 10_000 * (law == "equal"))
        self.board_rng.manual_seed(202609300000 + seed + 100 * DRAW_KINDS.index(draw)
                                   + 10_000 * (law == "equal"))
        self.render_rng.manual_seed(202609310000 + seed + 100 * DRAW_KINDS.index(draw)
                                    + 10_000 * (law == "equal"))
        self.draws = 0
        self.rolling = bytes(32)
        self.board_exposure = torch.zeros(len(tables.board_sums), dtype=torch.long,
                                          device=tables.device)
        self.sum_exposure = torch.zeros(37, dtype=torch.long, device=tables.device)
        self.render_exposure = torch.zeros(6, dtype=torch.long, device=tables.device)
        self.rendering_exposure = torch.zeros(30 ** 4, dtype=torch.long,
                                              device=tables.device)
        self.placement_exposure = torch.zeros_like(self.rendering_exposure)

    def _rand(self, high: int, shape: tuple[int, ...], rng: torch.Generator):
        return torch.randint(high, shape, generator=rng, device=self.tables.device)

    def draw_batch(self) -> DeviceBatch:
        # The law is sequential, but all episode rows are drawn together on device.
        b, t = self.batch, self.rounds
        values = self._rand(8, (b, t + 1), self.category_rng)
        initial = torch.where(values[:, 0] < (3 if self.law == "equal" else 4), 0,
                              torch.where(values[:, 0] < (5 if self.law == "equal" else 6),
                                          1, 2))
        categories, modes, targets, active_rows = [], [], [], []
        category = initial
        mode = torch.zeros(b, dtype=torch.long, device=self.tables.device)
        neutral_run = torch.zeros_like(mode)
        active = torch.ones(b, dtype=torch.bool, device=self.tables.device)
        for at in range(t):
            active = active & ~((category == 1) & (neutral_run == 2))
            active_rows.append(active)
            categories.append(category)
            mode = torch.where(category == 0, 0, torch.where(category == 2, 1, mode))
            modes.append(mode)
            neutral_run = torch.where(category == 1, neutral_run + 1, 0)
            value = values[:, at + 1]
            if self.law == "equal":
                target = torch.where(value < 3, 0, torch.where(value < 5, 1, 2))
            else:
                target = torch.where(mode == 0,
                                     torch.where(value < 4, 0, torch.where(value < 6, 1, 2)),
                                     torch.where(value < 2, 0, torch.where(value < 4, 1, 2)))
            targets.append(target)
            category = target
        category = torch.stack(categories, 1)
        active = torch.stack(active_rows, 1)
        target = torch.stack(targets, 1)
        lengths = active.sum(1)
        if bool((lengths < 1).any()):
            raise ValueError("r11 episode has no active round")
        # Candidate indices, mixture decisions, placements and record order are
        # vectorized over all active episode positions; no board-level Python loop.
        board_rand = self._rand(2**31, (b, t), self.board_rng)
        board_ids = torch.zeros((b, t), dtype=torch.long, device=self.tables.device)
        for kind in range(3):
            selected = category == kind
            pool = self.tables.by_category[kind]
            board_ids = torch.where(selected, pool[(board_rand % len(pool))], board_ids)
        if self.draw != "uniform":
            mixture = self._rand(4, (b, t), self.board_rng) == 0
            choice = self._rand(2**31, (b, t), self.board_rng)
            sums = BOUNDARY_SUMS[self.draw]
            for kind in range(3):
                selected = (category == kind) & mixture
                candidates = sums[kind]
                target_sum = torch.where(choice % 2 == 0, candidates[0], candidates[-1])
                for value in candidates:
                    chosen = selected & (target_sum == value)
                    pool = self.tables.by_sum[value]
                    board_ids = torch.where(chosen, pool[(board_rand % len(pool))],
                                            board_ids)
        placement_count = self.tables.placement_counts[board_ids].long()
        placement_at = self._rand(2**31, (b, t), self.render_rng) % placement_count
        placements = self.tables.placements[board_ids, placement_at].long()
        order = self._rand(6, (b, t), self.render_rng)
        packed = placements.gather(2, self.tables.orders[order])
        records = torch.stack((packed // 6, packed % 6), -1)
        records = torch.where(active[..., None, None], records, 0)
        active_ids = board_ids[active]
        self.board_exposure.index_add_(0, active_ids, torch.ones_like(active_ids))
        sums = self.tables.board_sums[board_ids, 0]
        active_sums = sums[active]
        self.sum_exposure.index_add_(0, active_sums, torch.ones_like(active_sums))
        active_orders = order[active]
        self.render_exposure.index_add_(0, active_orders, torch.ones_like(active_orders))
        complete_ids = rendering_ids(records)[active]
        self.rendering_exposure.index_add_(0, complete_ids, torch.ones_like(complete_ids))
        placement_records = torch.stack((placements // 6, placements % 6), -1)
        placement_ids = rendering_ids(placement_records)[active]
        self.placement_exposure.index_add_(0, placement_ids, torch.ones_like(placement_ids))
        batch = DeviceBatch(records, lengths, target, category, board_ids, active,
                            self.tables.board_sums[board_ids], order,
                            placement_at, placements)
        self.rolling = batch_digest(self.rolling, batch)
        self.draws += 1
        return batch

    def state(self) -> dict:
        return {"category": self.category_rng.get_state(),
                "board": self.board_rng.get_state(),
                "render": self.render_rng.get_state(), "draws": self.draws,
                "rolling": self.rolling.hex(),
                "board_exposure": self.board_exposure.detach().cpu().clone(),
                "sum_exposure": self.sum_exposure.detach().cpu().clone(),
                "render_exposure": self.render_exposure.detach().cpu().clone(),
                "rendering_exposure": self.rendering_exposure.detach().cpu().clone(),
                "placement_exposure": self.placement_exposure.detach().cpu().clone()}

    def restore(self, state: dict) -> None:
        self.category_rng.set_state(state["category"])
        self.board_rng.set_state(state["board"])
        self.render_rng.set_state(state["render"])
        self.draws = int(state["draws"])
        self.rolling = bytes.fromhex(state["rolling"])
        for name in ("board_exposure", "sum_exposure", "render_exposure",
                     "rendering_exposure", "placement_exposure"):
            setattr(self, name, state[name].to(self.tables.device).clone())


def nested_dose_masks(active: torch.Tensor, seed: int, *, device: torch.device):
    """One seeded uniform draw gives nested 0/1/10/100-percent masks."""
    generator = torch.Generator(device=device)
    generator.manual_seed(seed)
    draw = torch.rand(active.shape, generator=generator, device=device)
    return {0: active & False, 1: active & (draw < .01),
            10: active & (draw < .10), 100: active.clone()}


class JaggedNetwork(ChoiceNetwork):
    """The r8 record network with a raw-state A reader and selectable A route."""

    def __init__(self, *, dual: bool = False):
        super().__init__()
        self.dual = dual
        self.route = "dual" if dual else "raw_only"
        self.raw_sum_head = nn.Linear(self.raw_encoder.hidden_size, 5 * len(VALUES))

    @staticmethod
    def _gru_cell(value: torch.Tensor, previous: torch.Tensor,
                  weight_ih: torch.Tensor, weight_hh: torch.Tensor,
                  bias_ih: torch.Tensor, bias_hh: torch.Tensor) -> torch.Tensor:
        # The same GRU equations as nn.GRUCell, expanded so torch.func.vmap can
        # batch independent parameter sets (aten::gru has no vmap rule).
        ir, iz, inn = F.linear(value, weight_ih, bias_ih).chunk(3, -1)
        hr, hz, hn = F.linear(previous, weight_hh, bias_hh).chunk(3, -1)
        reset = torch.sigmoid(ir + hr)
        update = torch.sigmoid(iz + hz)
        candidate = torch.tanh(inn + reset * hn)
        return candidate + update * (previous - candidate)

    def round_interfaces(self, records: torch.Tensor):
        rows = len(records)
        raw_symbols = records[..., 0] * 6 + records[..., 1]
        symbols = self.raw_embedding(raw_symbols)
        raw = symbols.new_zeros((rows, self.raw_encoder.hidden_size))
        for at in range(4):
            raw = self._gru_cell(symbols[:, at], raw,
                                 self.raw_encoder.weight_ih_l0,
                                 self.raw_encoder.weight_hh_l0,
                                 self.raw_encoder.bias_ih_l0,
                                 self.raw_encoder.bias_hh_l0)
        if not self.dual:
            zeros = raw.new_zeros((rows, 5, len(VALUES)))
            return zeros, zeros, raw
        state = self.memory.start_state.expand(rows, 5, -1)
        for at in range(4):
            slot = records[:, at, 0]
            mass = records[:, at, 1]
            old = state.gather(1, slot[:, None, None].expand(-1, 1, state.shape[-1]))[:, 0]
            changed = self.memory.step(old, mass)
            state = torch.where(F.one_hot(slot, 5).bool()[..., None], changed[:, None, :],
                                state)
        logits = self.memory.answer(state.reshape(rows * 5, -1), game.KIND_SUM)
        logits = logits.reshape(rows, 5, len(VALUES))
        soft = torch.softmax(logits, -1)
        hard = F.one_hot(logits.argmax(-1), len(VALUES)).to(soft.dtype)
        return logits, hard + (soft - soft.detach()), raw

    def upper_step(self, answers: torch.Tensor, raw: torch.Tensor,
                   previous: torch.Tensor | None = None):
        if not self.dual:
            answers = torch.zeros_like(answers)
        if previous is None:
            previous = raw.new_zeros((len(raw), self.upper.hidden_size))
        value = torch.cat((self.answer_embedding(answers.flatten(1)), raw), -1)
        state = self._gru_cell(value, previous, self.upper.weight_ih,
                               self.upper.weight_hh, self.upper.bias_ih,
                               self.upper.bias_hh)
        return self.category_head(state), state

    def forward(self, records: torch.Tensor, lengths: torch.Tensor, *,
                answer_override: torch.Tensor | None = None,
                raw_override: torch.Tensor | None = None,
                initial_upper: torch.Tensor | None = None,
                return_trace: bool = False, return_all: bool = False):
        batch, rounds = records.shape[:2]
        sum_logits, answers, raw = self.round_interfaces(records.reshape(batch * rounds,
                                                                          4, 2))
        sum_logits = sum_logits.reshape(batch, rounds, 5, -1)
        answers = answers.reshape(batch, rounds, 5, -1)
        raw = raw.reshape(batch, rounds, -1)
        effective_answers = answers if answer_override is None else answer_override
        effective_raw = raw if raw_override is None else raw_override
        state = initial_upper
        logits, upper_states = [], []
        for at in range(rounds):
            predicted, state = self.upper_step(effective_answers[:, at],
                                               effective_raw[:, at], state)
            logits.append(predicted)
            upper_states.append(state)
        raw_sum = self.raw_sum_head(raw).reshape(batch, rounds, 5, len(VALUES))
        categories = torch.stack(logits, 1)
        upper = torch.stack(upper_states, 1)
        if return_trace:
            return {"sum_logits": sum_logits, "hard_answers": answers,
                    "raw_vectors": raw, "category_logits": categories,
                    "upper_states": upper}
        if return_all:
            return categories, sum_logits, raw_sum, raw, upper
        return sum_logits, categories


def new_model(seed: int, dual: bool, *, repo_root=None) -> JaggedNetwork:
    torch.manual_seed(seed)
    model = JaggedNetwork(dual=dual)
    if dual:
        if repo_root is None:
            raise ValueError("erosion requires the exact A source")
        source, _ = load_frozen_A(repo_root)
        model.memory.load_state_dict(source.core.state_dict(), strict=True)
    return model


def grouped_loss(outputs, batches: list[DeviceBatch], selections: list[torch.Tensor | None],
                 *, dual: bool) -> tuple[torch.Tensor, list[dict]]:
    logits, sums, raw_sums = outputs[:3]
    losses, details = [], []
    for index, batch in enumerate(batches):
        active = batch.active
        b_loss = F.cross_entropy(logits[index][active], batch.targets[active])
        target = torch.tensor([int(value) for value in VALUES], device=batch.records.device)
        y = torch.searchsorted(target, batch.sums)
        selection = selections[index]
        if selection is None or not bool(selection.any()):
            a_loss = b_loss.new_zeros(())
            selected = 0
        else:
            a_logits = sums[index] if dual else raw_sums[index]
            all_ce = F.cross_entropy(a_logits.reshape(-1, len(VALUES)), y.reshape(-1),
                                     reduction="none").reshape_as(y).mean(-1)
            a_loss = (all_ce * selection).sum() / active.sum()
            selected = int(selection.sum())
        losses.append(b_loss + a_loss)
        details.append({"B": float(b_loss.detach()), "A": float(a_loss.detach()),
                        "A_selected_rounds": selected, "active_rounds": int(active.sum())})
    return torch.stack(losses), details
