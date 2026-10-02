"""Shared scientific functions used by r8–r13."""
from __future__ import annotations


import copy


import math


import random


from collections import defaultdict


from dataclasses import dataclass


import torch


from torch import nn


from torch.nn import functional as F


from . import game


from .tables import CellTable


VALUES = tuple(sorted({game.sigma(history) for history in game.histories()}))


VALUE_INDEX = {value: index for index, value in enumerate(VALUES)}


MASS_INDEX = {mass: index for index, mass in enumerate(game.MASSES)}


@dataclass(frozen=True)
class HistorySplit:
    train: tuple[game.History, ...]
    heldout: tuple[game.History, ...]
    selected_length3: tuple[game.History, ...]
    selected_length4: tuple[game.History, ...]

    def counts(self) -> dict[str, object]:
        return {
            "train": len(self.train), "heldout": len(self.heldout),
            "train_by_length": {str(k): sum(len(h) == k for h in self.train)
                                for k in range(5)},
            "heldout_by_length": {str(k): sum(len(h) == k for h in self.heldout)
                                  for k in range(5)},
            "seeded_length3": len(self.selected_length3),
            "seeded_length4": len(self.selected_length4),
        }


def history_split(seed: int) -> HistorySplit:
    """Freeze 10% length-three and 20% length-four holds, with descendants."""

    rng = random.Random(seed)
    histories = game.histories()
    at3 = tuple(h for h in histories if len(h) == 3)
    at4 = tuple(h for h in histories if len(h) == 4)
    selected3 = set(rng.sample(at3, round(0.10 * len(at3))))
    selected4 = set(rng.sample(at4, round(0.20 * len(at4))))
    held = selected3 | selected4 | {h for h in at4 if h[:3] in selected3}
    train = tuple(h for h in histories if h not in held)
    heldout = tuple(h for h in histories if h in held)
    train_set = set(train)
    if train_set & set(heldout) or len(train) + len(heldout) != len(histories):
        raise AssertionError("history split overlaps or omits a history")
    if any(h[:length] not in train_set for h in train
           for length in range(len(h))):
        raise AssertionError("training histories are not prefix-closed")
    return HistorySplit(train, heldout, tuple(sorted(selected3)),
                        tuple(sorted(selected4)))


@dataclass
class MemoryResult:
    logits: torch.Tensor
    final_codes: torch.Tensor | None
    code_trace: tuple[torch.Tensor, ...]
    reconstruction: torch.Tensor
    commitment: torch.Tensor


class MemoryCore(nn.Module):
    """A learned continuous update, with no built-in addition or max law."""

    def __init__(self, width: int) -> None:
        super().__init__()
        self.width = width
        self.start_state = nn.Parameter(torch.zeros(width))
        self.mass_embedding = nn.Embedding(6, width)
        self.transition = nn.Sequential(
            nn.Linear(2 * width, width), nn.GELU(), nn.Linear(width, width),
            nn.Tanh(),
        )
        self.kind_embedding = nn.Embedding(3, width)
        self.readout = nn.Sequential(
            nn.Linear(2 * width, width), nn.GELU(), nn.Linear(width, len(VALUES)),
        )

    def step(self, state: torch.Tensor, mass_index: torch.Tensor) -> torch.Tensor:
        return self.transition(torch.cat((state, self.mass_embedding(mass_index)), -1))

    def answer(self, state: torch.Tensor, kind: int) -> torch.Tensor:
        kinds = torch.full((state.shape[0],), kind, dtype=torch.long,
                           device=state.device)
        return self.readout(torch.cat((state, self.kind_embedding(kinds)), -1))


class SeparateMaxReadout(nn.Module):
    """Independent copy of the parent's max function at initialization."""

    def __init__(self, core: MemoryCore) -> None:
        super().__init__()
        self.kind_vector = nn.Parameter(
            core.kind_embedding.weight[game.KIND_MAX].detach().clone())
        self.readout = copy.deepcopy(core.readout)

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        kind = self.kind_vector.expand(state.shape[0], -1)
        return self.readout(torch.cat((state, kind), -1))


class MemoryNetwork(nn.Module):
    """Only a selected code vector persists after each quantized update."""

    def __init__(self, *, width: int = 64, n_codes: int | None = None,
                 separate_max_readout: bool = False) -> None:
        super().__init__()
        self.core = MemoryCore(width)
        self.codebook = (nn.Parameter(torch.zeros(n_codes, width))
                         if n_codes is not None else None)
        self.max_readout: SeparateMaxReadout | None = None
        self.twin_soft_enabled = False
        self.twin_temperature: float | None = None
        self.twin_map_record: dict | None = None
        self._twin_group_indices: torch.Tensor | None = None
        self._twin_group_mask: torch.Tensor | None = None
        self._twin_group_has_alternative: torch.Tensor | None = None
        if separate_max_readout:
            self.install_separate_max_readout()

    @property
    def n_codes(self) -> int | None:
        return None if self.codebook is None else self.codebook.shape[0]

    def install_separate_max_readout(self) -> None:
        if self.max_readout is not None:
            raise ValueError("separate max readout is already installed")
        self.max_readout = SeparateMaxReadout(self.core)

    def configure_twin_assignment(self, old_codes: int,
                                  source_codes: list[int] | tuple[int, ...],
                                  temperature: float, *, enabled: bool) -> None:
        """Declare the nearby old-code families used only by training gradients."""

        if (self.codebook is None or not 0 < old_codes < self.n_codes
                or len(source_codes) != self.n_codes - old_codes
                or any(not isinstance(source, int) or not 0 <= source < old_codes
                       for source in source_codes)
                or not math.isfinite(temperature) or temperature <= 0):
            raise ValueError("twin assignment or temperature is invalid")
        old_to_twins: dict[int, list[int]] = defaultdict(list)
        for offset, source in enumerate(source_codes):
            old_to_twins[source].append(old_codes + offset)
        groups = []
        for code in range(self.n_codes):
            source = source_codes[code - old_codes] if code >= old_codes else code
            groups.append((source, *old_to_twins[source]))
        width = max(map(len, groups))
        self._twin_group_indices = torch.tensor(
            [list(group) + [group[0]] * (width - len(group)) for group in groups],
            dtype=torch.long)
        self._twin_group_mask = torch.tensor(
            [[position < len(group) for position in range(width)] for group in groups],
            dtype=torch.bool)
        self._twin_group_has_alternative = torch.tensor(
            [len(group) > 1 for group in groups], dtype=torch.bool)
        self.twin_temperature = temperature
        self.twin_soft_enabled = enabled
        self.twin_map_record = {
            "old_code_count": old_codes,
            "old_to_twins": {str(source): twins
                             for source, twins in sorted(old_to_twins.items()) if twins},
            "source_codes": list(source_codes),
            "temperature": temperature,
            "training_only_soft_gradient_enabled": enabled}

    def answer(self, state: torch.Tensor, kind: int) -> torch.Tensor:
        if kind == game.KIND_MAX and self.max_readout is not None:
            return self.max_readout(state)
        return self.core.answer(state, kind)

    def nearest(self, state: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Float32 squared Euclidean distance; smallest index wins exact ties."""

        if self.codebook is None:
            raise ValueError("continuous teacher has no finite codebook")
        if state.dtype != torch.float32 or self.codebook.dtype != torch.float32:
            raise ValueError("nearest-code assignment requires float32")
        if not bool(torch.isfinite(state).all() and torch.isfinite(self.codebook).all()):
            raise ValueError("nearest-code assignment has non-finite state or center")
        distances = (state[:, None, :] - self.codebook[None, :, :]).square().sum(-1)
        indices = distances.argmin(-1)
        return indices, self.codebook[indices]

    def quantize(self, state: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor,
                                                     torch.Tensor, torch.Tensor]:
        indices, selected = self.nearest(state)
        # Forward value is exactly the selected code. Answer gradients reach
        # BOTH core and codebook; reconstruction reaches only codebook;
        # commitment reaches the core and, through earlier selected states,
        # possibly the codebook. No continuous residual persists.
        carried = selected + (state - state.detach())
        if self.training and self.twin_soft_enabled:
            group = self._twin_group_indices.to(state.device)[indices]
            valid = self._twin_group_mask.to(state.device)[indices]
            has_alternative = self._twin_group_has_alternative.to(state.device)[indices]
            centers = self.codebook[group]
            squared = (state[:, None, :] - centers).square().sum(-1)
            weights = torch.softmax(
                (-squared / self.twin_temperature).masked_fill(~valid, -torch.inf),
                dim=-1)
            soft = (weights[..., None] * centers).sum(1)
            # The executed value remains the hard nearest code. For paired
            # families, the surrogate carries gradients through both centers
            # and their distance-dependent weights; unpaired codes retain the
            # original identity straight-through gradient.
            paired = selected + (soft - soft.detach())
            carried = torch.where(has_alternative[:, None], paired, carried)
        reconstruction = F.mse_loss(selected, state.detach())
        commitment = F.mse_loss(state, selected.detach())
        return carried, indices, reconstruction, commitment

    def forward(self, histories: tuple[game.History, ...] | list[game.History],
                *, kind: int = game.KIND_SUM) -> MemoryResult:
        if not histories or kind not in (0, 1, 2):
            raise ValueError("memory batch or query kind is invalid")
        device = self.core.start_state.device
        state = self.core.start_state.expand(len(histories), -1)
        reconstruction = state.new_zeros(())
        commitment = state.new_zeros(())
        loss_terms = 0
        codes = None
        code_trace = []
        if self.codebook is not None:
            state, codes, rec, com = self.quantize(state)
            code_trace.append(codes)
            reconstruction = reconstruction + rec
            commitment = commitment + com
            loss_terms += 1
        for position in range(4):
            active = [index for index, h in enumerate(histories) if len(h) > position]
            if not active:
                break
            indices = torch.tensor(active, dtype=torch.long, device=device)
            masses = torch.tensor([MASS_INDEX[histories[index][position]]
                                   for index in active], dtype=torch.long, device=device)
            following = self.core.step(state[indices], masses)
            if self.codebook is not None:
                following, new_codes, rec, com = self.quantize(following)
                reconstruction = reconstruction + rec
                commitment = commitment + com
                codes = codes.index_copy(0, indices, new_codes)
                code_trace.append(codes)
                loss_terms += 1
            state = state.index_copy(0, indices, following)
        if loss_terms:
            reconstruction = reconstruction / loss_terms
            commitment = commitment / loss_terms
        return MemoryResult(self.answer(state, kind), codes,
                            tuple(code_trace),
                            reconstruction, commitment)

    @torch.no_grad()
    def teacher_states(self, histories: tuple[game.History, ...]) -> torch.Tensor:
        if self.codebook is not None:
            raise ValueError("codebook initialization requires a continuous teacher")
        device = self.core.start_state.device
        states = []
        for history in histories:
            state = self.core.start_state.unsqueeze(0)
            for mass in history:
                state = self.core.step(
                    state, torch.tensor([MASS_INDEX[mass]], device=device))
            states.append(state[0])
        return torch.stack(states)

    @torch.no_grad()
    def extract_tables(self) -> CellTable:
        if self.codebook is None:
            raise ValueError("continuous teacher has no finite carrier")
        was_training = self.training
        self.eval()
        n = self.n_codes
        start = int(self.nearest(self.core.start_state.unsqueeze(0))[0][0])
        states = self.codebook.detach().repeat_interleave(6, dim=0)
        masses = torch.arange(6, device=states.device).repeat(n)
        following = self.core.step(states, masses)
        transition = self.nearest(following)[0].reshape(n, 6).tolist()
        answer = []
        for kind in range(3):
            logits = self.answer(self.codebook.detach(), kind)
            if not bool(torch.isfinite(logits).all()):
                raise ValueError("extracted memory answer has non-finite values")
            answer.append(tuple(VALUES[index] for index in logits.argmax(-1).tolist()))
        if was_training:
            self.train()
        return CellTable(
            tuple(tuple(int(value) for value in row) for row in transition),
            tuple(tuple(answer[kind][code] for kind in range(3))
                  for code in range(n)), start)

