"""Paired natural and endpoint-supervised neutral-prefix episode streams."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import torch
from torch.nn import functional as F

from .multiround import load_frozen_A
from .multiround_jagged import (
    BoardTables, DeviceBatch, DeviceStream, JaggedNetwork, batch_digest, rendering_ids,
)
from .memory import VALUES


ARMS = ("uniform", "cutoff", "decoy", "a_target", "a_supplied")


@dataclass
class CoverageBatch(DeviceBatch):
    b_active: torch.Tensor
    modes: torch.Tensor
    anchor: torch.Tensor
    neutral_length: torch.Tensor
    equal_law: bool


class CoverageStream(DeviceStream):
    """Reuse device board/placement draws; replace truncation and B supervision."""

    def __init__(self, tables: BoardTables, seed: int, law: str, draw: str):
        super().__init__(tables, seed, law, draw, batch=256, rounds=9)
        offset = seed + 10000 * (law == "equal")
        self.category_rng.manual_seed(202610110000 + offset)
        self.board_rng.manual_seed(202610120000 + offset + 100 *
                                   ("uniform", "cutoff", "decoy").index(draw))
        self.render_rng.manual_seed(202610130000 + offset + 100 *
                                    ("uniform", "cutoff", "decoy").index(draw))
        self.stratum_exposure = torch.zeros((2, 8), dtype=torch.long, device=tables.device)
        self.endpoint_targets = torch.zeros((2, 8, 3), dtype=torch.long,
                                            device=tables.device)
        self.slot_sum_exposure = torch.zeros((5, 37), dtype=torch.long, device=tables.device)

    def _rand(self, high, shape, rng):
        values = super()._rand(high, shape, rng)
        if rng is self.category_rng:
            rows = torch.arange(128, device=self.tables.device)
            anchors = rows // 64
            k = rows // 8 % 8 + 1
            values[128:, 0] = torch.where(anchors == 0, 0, 7)
            # The final target draw at k+1 remains fresh and unconditioned.
            for at in range(1, 9):
                neutral = (torch.full_like(anchors, 3) if self.law == "equal" else
                           torch.where(anchors == 0, 4, 2))
                values[128:, at] = torch.where(at <= k, neutral, values[128:, at])
        return values

    def _count(self, batch, sign):
        active = batch.active
        placements = torch.stack((batch.placements // 6, batch.placements % 6), -1)
        pairs = ((self.board_exposure, batch.board_ids),
                 (self.sum_exposure, batch.sums[..., 0]),
                 (self.render_exposure, batch.render_order),
                 (self.rendering_exposure, rendering_ids(batch.records)),
                 (self.placement_exposure, rendering_ids(placements)))
        for counts, ids in pairs:
            selected = ids[active]
            counts.index_add_(0, selected, torch.full_like(selected, sign))

    def draw_batch(self):
        previous = self.rolling
        old = super().draw_batch()
        self._count(old, -1)
        rows = torch.arange(256, device=self.tables.device)
        anchor = torch.where(rows < 128, -1, (rows - 128) // 64)
        k = torch.where(rows < 128, 8, (rows - 128) // 8 % 8 + 1)
        positions = torch.arange(9, device=self.tables.device)[None]
        active = positions <= k[:, None]
        b_active = (rows[:, None] < 128) | (positions == k[:, None])
        packed = old.placements.gather(2, self.tables.orders[old.render_order])
        records = torch.stack((packed // 6, packed % 6), -1)
        records = torch.where(active[..., None, None], records, 0)
        modes, mode = [], torch.zeros_like(rows)
        for at in range(9):
            category = old.categories[:, at]
            mode = torch.where(category == 0, 0, torch.where(category == 2, 1, mode))
            modes.append(mode)
        batch = CoverageBatch(records, active.sum(1), old.targets, old.categories,
                              old.board_ids, active, old.sums, old.render_order,
                              old.placement_indices, old.placements, b_active,
                              torch.stack(modes, 1), anchor, k, self.law == "equal")
        self._count(batch, 1)
        for slot in range(5):
            ids = batch.sums[..., slot][batch.active]
            self.slot_sum_exposure[slot].index_add_(0, ids, torch.ones_like(ids))
        self.stratum_exposure += 8
        indices = torch.stack((anchor[128:], k[128:] - 1,
                               batch.targets[128:, :].gather(1, k[128:, None])[:, 0]), 1)
        flattened = indices[:, 0] * 24 + indices[:, 1] * 3 + indices[:, 2]
        self.endpoint_targets.view(-1).index_add_(0, flattened,
                                                 torch.ones_like(flattened))
        digest = hashlib.sha256(batch_digest(previous, batch))
        for value in (b_active, batch.modes, anchor, k):
            digest.update(value.cpu().numpy().tobytes())
        self.rolling = digest.digest()
        return batch

    def state(self):
        return {**super().state(), "stratum_exposure": self.stratum_exposure.cpu().clone(),
                "endpoint_targets": self.endpoint_targets.cpu().clone(),
                "slot_sum_exposure": self.slot_sum_exposure.cpu().clone()}

    def restore(self, saved):
        super().restore(saved)
        self.stratum_exposure = saved["stratum_exposure"].to(self.tables.device).clone()
        self.endpoint_targets = saved["endpoint_targets"].to(self.tables.device).clone()
        self.slot_sum_exposure = saved["slot_sum_exposure"].to(self.tables.device).clone()


def new_model(seed: int, arm: str, repo_root: Path):
    if arm not in ARMS:
        raise ValueError("r12 arm differs")
    torch.manual_seed(seed)
    model = JaggedNetwork(dual=arm == "a_supplied")
    source, _ = load_frozen_A(repo_root)
    model.memory.load_state_dict(source.core.state_dict(), strict=True)
    model.memory.requires_grad_(False)
    return model


def coverage_loss(output, batches, arms):
    logits, _, a_logits, _, _ = output
    losses, details = [], []
    for index, (batch, arm) in enumerate(zip(batches, arms, strict=True)):
        ce = F.cross_entropy(logits[index].flatten(0, 1), batch.targets.flatten(),
                             reduction="none").reshape_as(batch.targets)
        natural = ce[:128].mean()
        endpoint = ce[128:][batch.b_active[128:]].mean()
        b_loss = .5 * (natural + endpoint)
        a_loss = b_loss.new_zeros(())
        if arm == "a_target":
            classes = torch.arange(len(VALUES), device=logits.device)
            # All legal sums are the 36 values in the inherited answer vocabulary.
            lookup = torch.full((37,), -1, dtype=torch.long, device=logits.device)
            lookup[torch.tensor(VALUES, device=logits.device)] = classes
            targets = lookup[batch.sums]
            a_loss = F.cross_entropy(a_logits[index][batch.active].flatten(0, 1),
                                     targets[batch.active].flatten())
        probabilities = logits[index].softmax(-1)
        laws = logits.new_tensor([[.5, .25, .25], [.25, .25, .5]])
        if batch is not None and getattr(batch, "equal_law", False):
            laws[:] = logits.new_tensor([.375, .25, .375])
        exact = laws[batch.modes]
        kl = (exact * (exact.log() - probabilities.clamp_min(1e-30).log())).sum(-1) / \
            logits.new_tensor(2.).log()
        losses.append(b_loss + a_loss)
        details.append({"B": float(b_loss.detach()), "A": float(a_loss.detach()),
                        "natural_CE": float(natural.detach()),
                        "coverage_CE": float(endpoint.detach()),
                        "coverage_endpoint_KL_bits": float(kl[128:][batch.b_active[128:]]
                                                            .mean().detach())})
    return torch.stack(losses), details
