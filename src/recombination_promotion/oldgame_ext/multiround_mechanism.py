"""Four separately registered mechanisms; records are the only model input."""

from __future__ import annotations

import copy
from dataclasses import dataclass

import numpy as np
import torch
from torch.nn import functional as F

from . import game
from .memory import VALUES, VALUE_INDEX
from .multiround_jagged import JaggedNetwork


AUDITS = (0, 1000, 2000, 5000, 10000, 15000, 20000)
EROSION = ("adam", "reduced", "sgd", "blocked")
NOISE = ("raw_sampled", "raw_probability", "sums_sampled", "sums_probability")
ACCESS = ("disconnected", "frozen", "live", "exact")


@dataclass(frozen=True)
class Run:
    experiment: str
    condition: str
    seed: int
    law: str = "original"

    @property
    def name(self):
        return f"{self.experiment}_{self.condition}_{self.law}_seed{self.seed}"

    @property
    def supervised(self):
        return self.condition.startswith("sums_") or self.condition in ACCESS[:3]

    @property
    def probability(self):
        return self.condition.endswith("probability")

    @property
    def encoding(self):
        return "numerical" if self.condition == "numerical" else "onehot"


def all_runs():
    return ([Run("erosion", c, s) for c in EROSION for s in range(3)] +
            [Run("noise", c, s) for c in NOISE for s in range(3)] +
            [Run("access", c, s) for c in ACCESS for s in range(3)] +
            [Run("encoding", "numerical", s) for s in range(3)] +
            [Run("encoding", c, s, "equal") for c in ("onehot", "numerical")
             for s in range(3)])


def hard_answers(logits):
    soft = logits.softmax(-1)
    hard = F.one_hot(logits.argmax(-1), 36).to(soft.dtype)
    return hard + (soft - soft.detach())


def encode_answers(answers, encoding):
    if encoding == "onehot":
        return answers
    if encoding != "numerical":
        raise ValueError("unknown encoding")
    values = answers.new_tensor(VALUES)
    sums = (answers * values).sum(-1) / 36
    return torch.cat((sums[..., None], 1 - sums[..., None],
                      answers.new_zeros((*sums.shape, 34))), -1)


class MechanismNetwork(JaggedNetwork):
    def __init__(self, condition):
        connected = condition in ("frozen", "live", "exact", "onehot", "numerical")
        super().__init__(dual=connected)
        self.condition = condition
        self.encoding = "numerical" if condition == "numerical" else "onehot"
        # Present in every condition, frozen independently of the live route.
        self.supplier_embedding = copy.deepcopy(self.raw_embedding)
        self.supplier_encoder = copy.deepcopy(self.raw_encoder)
        self.supplier_head = copy.deepcopy(self.raw_sum_head)
        for module in (self.memory, self.supplier_embedding,
                       self.supplier_encoder, self.supplier_head):
            module.requires_grad_(False)

    def raw_state(self, records, *, supplier=False):
        embedding = self.supplier_embedding if supplier else self.raw_embedding
        encoder = self.supplier_encoder if supplier else self.raw_encoder
        x = embedding(records[..., 0] * 6 + records[..., 1])
        state = x.new_zeros((len(records), encoder.hidden_size))
        for at in range(4):
            state = self._gru_cell(x[:, at], state, encoder.weight_ih_l0,
                                   encoder.weight_hh_l0, encoder.bias_ih_l0,
                                   encoder.bias_hh_l0)
        return state

    def supplier_logits(self, records):
        return self.supplier_head(self.raw_state(records, supplier=True)).reshape(-1, 5, 36)

    def round_interfaces(self, records):
        raw = self.raw_state(records)
        live = self.raw_sum_head(raw).reshape(-1, 5, 36)
        if self.condition in ("exact", "onehot", "numerical"):
            # Execute learned frozen A, not semantic targets.
            logits, answers, _ = super().round_interfaces(records)
            return logits, answers, raw
        if self.condition == "live":
            answers = hard_answers(live)
        elif self.condition == "frozen":
            answers = hard_answers(self.supplier_logits(records)).detach()
        else:
            answers = torch.zeros_like(live)
        return live, answers, raw

    def upper_step(self, answers, raw, previous=None):
        return super().upper_step(encode_answers(answers, self.encoding), raw, previous)


def exact_rows(batch):
    rows = batch.records.new_tensor([[.5, .25, .25], [.25, .25, .5]],
                                    dtype=torch.float32)
    if batch.equal_law:
        rows[:] = rows.new_tensor([.375, .25, .375])
    return rows[batch.modes]


def prediction_loss(logits, batch, *, probability=False):
    p = exact_rows(batch)
    logq = logits.log_softmax(-1)
    ce = -(p * logq).sum(-1) if probability else F.cross_entropy(
        logits.flatten(0, 1), batch.targets.flatten(), reduction="none").reshape_as(batch.targets)
    floor_rows = -(p * p.log()).sum(-1) if probability else -p.log().gather(
        -1, batch.targets[..., None])[..., 0]
    def average(value):
        return .5 * (value[:128].mean() + value[128:][batch.b_active[128:]].mean())
    return average(ce), average(floor_rows)


def sums_loss(logits, batch):
    values = batch.sums.new_tensor(VALUES)
    target = torch.searchsorted(values, batch.sums)
    return F.cross_entropy(logits[batch.active].flatten(0, 1),
                           target[batch.active].flatten())


def loss_parts(output, batch, run):
    b, floor = prediction_loss(output[0], batch, probability=run.probability)
    a = sums_loss(output[2], batch) if run.supervised else b.new_zeros(())
    return b + a, {"B": float(b.detach()), "A": float(a.detach()),
                   "target_floor": float(floor), "excess_prediction_loss": float((b - floor).detach())}


def gradient_conflict(model, batch):
    output = model(batch.records, batch.lengths, return_all=True)
    b, _ = prediction_loss(output[0], batch,
                           probability=model.condition.endswith("probability"))
    a = sums_loss(output[2], batch)
    parameters = [p for n, p in model.named_parameters()
                  if n.startswith(("raw_encoder.", "raw_embedding."))]
    def gradient(loss):
        gs = torch.autograd.grad(loss, parameters, retain_graph=True, allow_unused=True)
        return torch.cat([(torch.zeros_like(p) if g is None else g).flatten()
                          for p, g in zip(parameters, gs, strict=True)])
    gb, ga = gradient(b), gradient(a)
    dot = (gb * ga).sum()  # Never CUDA vector dot.
    nb, na = gb.norm(), ga.norm()
    route = torch.autograd.grad(b, list(model.raw_sum_head.parameters()), allow_unused=True)
    return {"prediction_gradient_norm": float(nb), "sums_gradient_norm": float(na),
            "cosine": float(dot / (nb * na)) if nb * na > 0 else None,
            "prediction_gradient_effect_on_sums": float(-dot),
            "sums_gradient_effect_on_prediction": float(-dot),
            "live_sums_route_prediction_gradient_norm": float(torch.stack([
                g.square().sum() for g in route if g is not None]).sum().sqrt())
                if any(g is not None for g in route) else 0.}


def matched_sgd_rate(gradients, lr=.003, eps=1e-8):
    norm = torch.stack([g.square().sum() for g in gradients]).sum().sqrt()
    displacement = torch.stack([(lr * g / (g.abs() + eps)).square().sum()
                                for g in gradients]).sum().sqrt()
    if norm == 0:
        raise ValueError("first-batch sums gradient is zero; SGD rate undefined")
    return float(displacement / norm)


def gradient_statistics(g, eps=1e-8):
    a = g.abs()
    return {"norm": float(g.norm()), "zero": float((a == 0).float().mean()),
            "le_eps": float((a <= eps).float().mean()),
            "eps_to_10eps": float(((a > eps) & (a <= 10 * eps)).float().mean()),
            "gt_10eps": float((a > 10 * eps).float().mean())}


def histories_logits(core):
    hs = game.histories()
    device = core.start_state.device
    state = core.start_state.expand(len(hs), -1)
    for at in range(4):
        mass = torch.tensor([game.MASSES.index(h[at]) if len(h) > at else 0 for h in hs],
                            device=device)
        changed = core.step(state, mass)
        active = torch.tensor([len(h) > at for h in hs], device=device)
        state = torch.where(active[:, None], changed, state)
    return core.answer(state, game.KIND_SUM)


def margin_counts(logits):
    truth = logits.new_tensor([VALUE_INDEX[game.sigma(h)] for h in game.histories()],
                              dtype=torch.long)
    alt = logits.detach().clone().scatter(1, truth[:, None], -torch.inf).max(-1).values
    margins = logits.gather(1, truth[:, None])[:, 0] - alt
    return {"correct": int((logits.argmax(-1) == truth).sum()), "total": len(truth),
            "margins": margins.detach().cpu().tolist(),
            "predictions": logits.argmax(-1).cpu().tolist()}


def fixed_geometry_pairs(boards, split, seed=2026101304):
    """Read identities only. Select pairs and permutations before states exist."""
    rng = np.random.default_rng(seed)
    result = {}
    for name in ("train", "heldout"):
        ids = set(split[name])
        fibers = {}
        for i in sorted(ids):
            b = boards.boards[i]
            fibers.setdefault(tuple(b[1:]), []).append((b[0], i))
        pairs = []
        for fiber in fibers.values():
            for at, (a, i) in enumerate(sorted(fiber)):
                for b, j in sorted(fiber)[at + 1:]:
                    if b - a == 1 or b - a >= 4:
                        pairs.append([i, j, a, b])
        counts = {}
        for _, _, a, b in pairs:
            counts[f"{a}_{b}"] = counts.get(f"{a}_{b}", 0) + 1
        result[name] = {"pairs": pairs, "label_permutation": rng.permutation(
            2 * len(pairs)).tolist(), "reader_label_permutations": {
                key: rng.permutation(2 * count).tolist() for key, count in counts.items()}}
    return result


def cutoff_summary(census):
    result = []
    for rendering in (census["registered_rendering"], *census["additional_fixed_renderings"]):
        groups = {}
        for name, selected in (("cutoff", lambda v: 11 <= v <= 13 or 23 <= v <= 25),
                               ("complement", lambda v: not (11 <= v <= 13 or 23 <= v <= 25))):
            rows = [r for v, r in rendering["by_slot1_sum_twelfths"].items() if selected(int(v))]
            n = sum(r["boards"] for r in rows)
            errors = sum(r["above_0_02_TV"] for r in rows)
            groups[name] = {"boards": n, "prediction_TV_errors": errors,
                            "error_rate": errors / n if n else None,
                            "maximum_TV": max((r["maximum_TV"] for r in rows), default=None)}
        result.append({"rendering": rendering["rendering"], **groups})
    return result
