"""Paired B-only route-access study on the recorded old-game panels."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import time
import warnings
from pathlib import Path
from recombination_promotion.public_paths import identity_matches

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from recombination_promotion.oldgame_ext.multiround import (
    P, P_EQUAL, enumerate_boards, load_frozen_A,
)
from recombination_promotion.oldgame_ext.multiround_choice import ChoiceNetwork
from scripts import multiround_scoring as prior
from scripts import multiround_interventions as ablation
from scripts import multiround_panels as choice
from scripts import multiround_streams as online


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/phase11/oldgame_memory/multiround/study_r8_route_access"
SPEC = OUTPUT / "specification.md"
SOURCE = choice.OUTPUT
AUDITS = (0, 1000, 2000, 5000, 10000, 15000, 20000)
ROUTES = ("a_only", "raw_only", "dual")
LAWS = ("original", "equal")
SEEDS = (0, 1, 2)
LINEAR_PROBE_SETTINGS = {
    "standardization": "StandardScaler_fit_on_probe_training_only",
    "estimator": "LogisticRegression",
    "C": 10.0,
    "class_weight": "balanced",
    "tol": 1e-5,
    "max_iter": 5000,
}
READINGS = (
    "A-only learns B faster or passes when raw-only does not: access to completed A "
    "objects helps realize the predictive extension; it does not show spontaneous A formation.\n"
    "Raw-only passes B; only slot-1 A improves: B-only training organized the rewarded "
    "slot-1 information, not a full five-slot A layer.\n"
    "Raw-only passes B; all five sums improve: full A became readable in those states; "
    "readability alone does not establish causal use.\n"
    "Raw-only passes B; no sum improves: B was learned without measured new A "
    "readability; report any high baseline decodability.\n"
    "Dual outperforms both: access to both routes helps under this architecture; "
    "interpret interventions with the deterministic-overlap caveat.\n"
    "Equal-law witness split or route-dependent gain: control failure."
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


class RouteNetwork(ChoiceNetwork):
    """The inherited A core is frozen; only the declared upper route varies."""

    def __init__(self, route: str, seed: int, *, verify_source: bool = True) -> None:
        if route not in ROUTES:
            raise ValueError("route differs")
        torch.manual_seed(seed)
        super().__init__()
        self.route = route
        if verify_source:
            source, _ = load_frozen_A(ROOT)
            self.memory.load_state_dict(source.core.state_dict(), strict=True)
        self.memory.requires_grad_(False)
        self.memory.eval()

    def train(self, mode: bool = True):
        super().train(mode)
        self.memory.eval()
        return self

    def upper_step(self, answers: torch.Tensor, raw: torch.Tensor,
                   previous: torch.Tensor | None = None):
        if self.route == "raw_only":
            answers = torch.zeros_like(answers)
        if self.route == "a_only":
            raw = torch.zeros_like(raw)
        return super().upper_step(answers, raw, previous)


def b_only_loss(model: RouteNetwork, records: torch.Tensor, lengths: torch.Tensor,
                targets: torch.Tensor) -> torch.Tensor:
    _, logits = model(records, lengths)
    active = torch.arange(logits.shape[1])[None, :] < lengths[:, None]
    return F.cross_entropy(logits[active], targets[active])


def registration() -> dict:
    row = json.loads((OUTPUT / "registration.json").read_text())
    if (row["spec_sha256"] != sha(SPEC)
            or row["panels_sha256"] != sha(SOURCE / "manifest.json")
            or row["A_source"] != load_frozen_A(ROOT)[1]
            or row["Gate_A_sha256"] != sha(choice.routed.GATE / "results.json")
            or row.get("linear_probe_settings") != LINEAR_PROBE_SETTINGS):
        raise ValueError("r8 registration authority differs")
    return row


def register() -> dict:
    if (OUTPUT / "registration.json").exists():
        raise ValueError("r8 registration already exists")
    choice.verify_panels(SOURCE)
    _, frozen = load_frozen_A(ROOT)
    note = {
        "role": "r8_route_access_B_only", "spec_sha256": sha(SPEC),
        "claims_verbatim": SPEC.read_text().split("### Three claims\n", 1)[1].split(
            "\n### Arms and training", 1)[0].strip(),
        "criteria": {"KL_bits": .01, "witness_recovery": .8,
                     "law_and_intervention_TV": .02},
        "predeclared_reading": READINGS,
        "A_source": frozen, "panels_sha256": sha(SOURCE / "manifest.json"),
        "Gate_A_sha256": sha(choice.routed.GATE / "results.json"),
        "linear_probe_settings": LINEAR_PROBE_SETTINGS,
        "settings": {"steps": 20000, "batch": 256, "lr": .003, "weight_decay": .01,
                     "audit_steps": AUDITS, "routes": ROUTES, "laws": LAWS, "seeds": SEEDS,
                     "futility_at": 5000, "futility_gap_fraction": .10},
        "choices": [
            "Use the verified r5 Gate A routed panels and r6 legal donor indices unchanged.",
            "Use the r3 online episode stream; pair it across routes within each seed and law.",
            "Probe split: 2048 training and 512 held-out board identities, independent render seeds; "
            "linear probe uses train-only standardization and class-balanced logistic "
            "regression (C=10, tol=1e-5, 5000 iterations), "
            "MLP probe uses 100 full-batch Adam updates at lr 0.03 and a fixed seed.",
            "Probe gain intervals: 1000 board-bootstrap draws, seed 2026100803.",
            "Smoke uses 1000 updates and scratch output only; production retains fixed 20000.",
        ],
    }
    save_json(OUTPUT / "registration.json", note)
    (OUTPUT / "registration.md").write_text(
        "# r8 registered route-access study\n\n" + note["claims_verbatim"] +
        "\n\n## Criteria\n\n" + json.dumps(note["criteria"], sort_keys=True) +
        "\n\n## Predeclared reading\n\n" + READINGS +
        "\n\n## Source and choices\n\n" + json.dumps(
            {key: note[key] for key in ("A_source", "settings", "linear_probe_settings",
                                        "choices")}, indent=2) + "\n")
    return note


def _panels(law: str) -> tuple:
    name = "test" if law == "original" else "equal_test"
    panel = choice.load_episodes(SOURCE / f"{name}.npz")
    records = np.load(SOURCE / f"{name}_records.npy")
    prefix_records = np.load(SOURCE / "prefix_records.npy")
    prefix_lengths = np.load(SOURCE / "prefix_lengths.npy")
    prefix_meta = json.loads((SOURCE / "prefix_metadata.json").read_text())
    return panel, records, prefix_records, prefix_lengths, prefix_meta


def _donors(law: str, prefix_length: int):
    index = LAWS.index(law)
    natural = ablation.donor_indices(5000, ablation.NATURAL_DONOR_SEED + index)
    prefix = ablation.donor_indices(5000, ablation.PREFIX_DONOR_SEED + index,
                                    target_count=prefix_length)
    return natural, prefix


def _kl(probabilities: np.ndarray, panel, law: str, mask: np.ndarray | None = None) -> float:
    active = prior._active(panel) if mask is None else mask
    truth = np.asarray(P_EQUAL if law == "equal" else P, dtype=float)
    exact = (np.broadcast_to(truth, probabilities[active].shape)
             if law == "equal" else truth[panel.modes[active]])
    predicted = np.clip(probabilities[active], 1e-12, 1)
    return float(np.mean(np.sum(exact * np.log2(exact / predicted), axis=-1)))


@torch.no_grad()
def audit_model(model: RouteNetwork, law: str, unseen: np.ndarray | None = None,
                *, probes: bool = True, require_unseen: bool = False) -> dict:
    model.eval()
    panel, records, prefix_records, prefix_lengths, prefix_meta = _panels(law)
    natural, sums = choice.predict_panel(model, records, panel.lengths)
    prefix, _ = choice.predict_panel(model, prefix_records, prefix_lengths)
    mode_law = choice.prefix_score(prefix, prefix_lengths, prefix_meta,
                                   equal=law == "equal")
    rerender = choice.rerender_score(model, np.load(SOURCE / "rerender_records.npy"))
    with np.load(SOURCE / "swap_records.npz") as saved:
        swaps = choice.swap_score(model, saved["board_ids"], saved["records"],
                                  json.loads((SOURCE / "swap_scenarios.json").read_text()),
                                  equal=law == "equal")
    unseen_kl = None if unseen is None or not unseen.any() else _kl(natural, panel, law, unseen)
    scores = {"natural_excess_KL_bits": _kl(natural, panel, law),
              "unseen_excess_KL_bits": unseen_kl, "unseen_count": 0 if unseen is None else int(unseen.sum()),
              "mode_law": mode_law, "rerender": rerender, "swaps": swaps,
              "A_components_correct": int((sums[prior._active(panel)] ==
                  choice.sum_targets(panel, enumerate_boards())[prior._active(panel)]).sum())}
    witness = (mode_law["witness_pair_mean_prediction_TV"] <= .02 if law == "equal"
               else mode_law["witness_recovery_fraction"] >= .8)
    scores["criteria"] = {
        "natural_KL": scores["natural_excess_KL_bits"] <= .01,
        "unseen_KL": ((not require_unseen) if unseen_kl is None else unseen_kl <= .01),
        "witness": bool(witness), "law_TV": mode_law["maximum_TV"] <= .02,
        "rerender": rerender["pass"], "swaps": swaps["natural_swap_pass"],
    }
    scores["B_pass"] = all(scores["criteria"].values())
    if probes and model.route == "raw_only":
        with torch.enable_grad():
            scores["probes"] = probe_audit(model)
    return scores


@torch.no_grad()
def route_damage(model: RouteNetwork, law: str) -> dict:
    model.eval()
    panel, records, prefix_records, prefix_lengths, prefix_meta = _panels(law)
    natural_ix, prefix_ix = _donors(law, len(prefix_records))
    natural, natural_changes = ablation.predict_conditions(model, records,
                                                              records[natural_ix])
    prefix, prefix_changes = ablation.predict_conditions(
        model, prefix_records, records[prefix_ix, :prefix_records.shape[1]])
    rows = {key: {"natural_excess_KL_bits": _kl(values, panel, law),
                  "mode_law": choice.prefix_score(prefix[key], prefix_lengths, prefix_meta,
                                                  equal=law == "equal")}
            for key, values in natural.items()}
    effects = {key: ablation.damage(rows["unaltered"], rows[key], equal=law == "equal")
               for key in ablation.CONDITIONS if key != "unaltered"}
    if model.route == "a_only" and (not np.array_equal(natural["raw_ablated"], natural["unaltered"])
                                    or not np.array_equal(prefix["raw_ablated"], prefix["unaltered"])):
        raise ValueError("inactive raw route changed prediction")
    if model.route == "raw_only" and (not np.array_equal(natural["A_ablated"], natural["unaltered"])
                                      or not np.array_equal(prefix["A_ablated"], prefix["unaltered"])):
        raise ValueError("inactive A route changed prediction")
    return {"conditions": rows, "effects": effects, "natural_route_changes": natural_changes,
            "prefix_route_changes": prefix_changes,
            "interpretation": ablation.interpretation(effects["A_ablated"]["damaged"],
                                                        effects["raw_ablated"]["damaged"]),
            "caveat": ablation.CAVEAT}


class ExactRowModel(ChoiceNetwork):
    """Finite predictive oracle with a forced route or current-board-only null."""

    def __init__(self, route: str, law: str, *, current_only: bool = False) -> None:
        super().__init__()
        self.route, self.law, self.current_only = route, law, current_only

    def round_interfaces(self, records: torch.Tensor):
        from recombination_promotion.oldgame_ext import game
        from recombination_promotion.oldgame_ext.memory import VALUE_INDEX

        totals = torch.zeros((len(records), 5), dtype=torch.long)
        masses = torch.tensor(game.MASSES, dtype=torch.long)
        for at in range(4):
            totals.scatter_add_(1, records[:, at, :1], masses[records[:, at, 1:2]])
        values = torch.tensor([VALUE_INDEX.get(sum_value, 0) for sum_value in range(37)])
        answers = F.one_hot(values[totals], 36).float()
        category = torch.where(totals[:, 0] <= 12, 0,
                               torch.where(totals[:, 0] >= 24, 2, 1)).float()
        raw = torch.zeros((len(records), 16))
        raw[:, 0] = category
        return answers * 20, answers, raw

    def upper_step(self, answers, raw, previous=None):
        if previous is None:
            previous = torch.zeros((len(raw), 32))
        if self.law == "equal":
            rows = torch.tensor([list(map(float, P_EQUAL))] * len(raw))
            return rows.log(), previous
        if self.route == "a_only":
            from recombination_promotion.oldgame_ext.memory import VALUES
            indices = answers[:, 0].argmax(-1)
            sums = torch.tensor([int(value) for value in VALUES])[indices]
            category = torch.where(sums <= 12, 0, torch.where(sums >= 24, 2, 1))
        elif self.route == "raw_only":
            category = raw[:, 0].long()
        else:
            raise ValueError("exact oracle route differs")
        mode = torch.where(category == 0, 0, torch.where(category == 2, 1,
                           previous[:, 0].long()))
        updated = previous.clone()
        updated[:, 0] = mode.float()
        rows = torch.tensor([[float(x) for x in P[0]], [float(x) for x in P[1]]])[mode]
        if self.current_only:
            # With initial mode zero, the current-board null also knows the
            # round index, as in the registered current-board comparator.
            q = .5 * (1 - torch.pow(torch.tensor(.5), previous[:, 1]))
            neutral = ((1 - q[:, None]) * torch.tensor([float(x) for x in P[0]])
                       + q[:, None] * torch.tensor([float(x) for x in P[1]]))
            rows = torch.where((category == 1)[:, None], neutral, rows)
            updated[:, 1] = previous[:, 1] + 1
        return rows.log(), updated


def probe_split() -> dict:
    """Board-disjoint train/heldout identities with all sum values in training."""
    boards = enumerate_boards()
    pool = np.asarray(boards.boards, dtype=np.int64)
    rng = np.random.default_rng(2026100801)
    selected: set[int] = set()
    from recombination_promotion.oldgame_ext.memory import VALUES
    for slot in range(5):
        for value in VALUES:
            eligible = np.flatnonzero(pool[:, slot] == value)
            if len(eligible):
                selected.add(int(eligible[0]))
    others = np.asarray([i for i in range(len(pool)) if i not in selected])
    rng.shuffle(others)
    train = np.asarray(sorted(selected) + others[:2048 - len(selected)].tolist())
    heldout = others[2048 - len(selected):2048 - len(selected) + 512]
    if len(train) != 2048 or len(heldout) != 512 or set(train) & set(heldout):
        raise ValueError("probe board split differs")
    if any(len(np.unique(pool[train, slot])) != 36 for slot in range(5)):
        raise ValueError("probe training misses a sum value")
    train_seeds = rng.integers(0, 2**63 - 1, len(train), dtype=np.int64)
    test_seeds = rng.integers(0, 2**63 - 1, len(heldout), dtype=np.int64)
    return {"train_board_ids": train.tolist(), "heldout_board_ids": heldout.tolist(),
            "train_render_seeds": train_seeds.tolist(),
            "heldout_render_seeds": test_seeds.tolist()}


def _probe_data(split: dict):
    boards = enumerate_boards()
    values = np.asarray(boards.boards, dtype=np.int64)
    batches = []
    for prefix in ("train", "heldout"):
        ids = np.asarray(split[f"{prefix}_board_ids"], dtype=np.int64)
        seeds = np.asarray(split[f"{prefix}_render_seeds"], dtype=np.int64)
        records = choice.record_projection(ids[:, None], seeds[:, None], boards)[:, 0]
        from recombination_promotion.oldgame_ext.memory import VALUE_INDEX
        batches.append((records, np.vectorize(VALUE_INDEX.__getitem__)(values[ids])))
    return batches


@torch.no_grad()
def _carrier(model: RouteNetwork, records: np.ndarray, *, oracle_carrier=False):
    if oracle_carrier:
        from recombination_promotion.oldgame_ext import game
        values = np.zeros((len(records), 5), dtype=np.int64)
        for at in range(4):
            for row in range(len(records)):
                values[row, records[row, at, 0]] += game.MASSES[records[row, at, 1]]
        # Three dimensions per slot; distinct unit vectors admit linear class separation.
        from recombination_promotion.oldgame_ext.memory import VALUE_INDEX
        indices = np.vectorize(VALUE_INDEX.__getitem__)(values)
        height = 1 - 2 * (indices + .5) / 36
        radial = np.sqrt(1 - height * height)
        theta = indices * np.pi * (3 - np.sqrt(5))
        coords = np.stack((radial * np.cos(theta), radial * np.sin(theta), height), -1)
        raw = np.pad(coords.reshape(len(values), 15), ((0, 0), (0, 1)))
        upper = np.pad(raw, ((0, 0), (0, 16)))
        return raw.astype(np.float32), upper.astype(np.float32)
    sections = [], []
    for offset in range(0, len(records), 256):
        _, answers, raw = model.round_interfaces(torch.from_numpy(records[offset:offset + 256]))
        _, upper = model.upper_step(answers, raw, None)
        sections[0].append(raw.numpy())
        sections[1].append(upper.numpy())
    return np.concatenate(sections[0]), np.concatenate(sections[1])


def _fit_probe(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray,
               test_y: np.ndarray, *, family: str, seed: int) -> dict:
    """Fixed-budget linear or width-64 two-layer categorical reader."""
    if family == "linear":
        from sklearn.exceptions import ConvergenceWarning
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler().fit(train_x)
        fitted_x = scaler.transform(train_x)
        heldout_x = scaler.transform(test_x)
        reader = LogisticRegression(C=10, class_weight="balanced", tol=1e-5,
                                    max_iter=5000)
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter("always", ConvergenceWarning)
            reader.fit(fitted_x, train_y)
        convergence_warnings = [str(item.message) for item in observed
                                if issubclass(item.category, ConvergenceWarning)]
        n_iter = [int(value) for value in np.atleast_1d(reader.n_iter_)]
        converged = not convergence_warnings and max(n_iter) < 5000
        probabilities = np.clip(reader.predict_proba(heldout_x), 1e-12, 1)
        prediction = reader.predict(heldout_x)
        return {"accuracy": float(np.mean(prediction == test_y)),
                "cross_entropy_nats": float(-np.log(probabilities[
                    np.arange(len(test_y)), test_y]).mean()),
                "correct": int(np.sum(prediction == test_y)), "total": len(test_y),
                "predictions": prediction.tolist(), "n_iter": n_iter,
                "convergence_warnings": convergence_warnings, "converged": converged}
    torch.manual_seed(seed)
    x = torch.tensor(train_x, dtype=torch.float32)
    y = torch.tensor(train_y, dtype=torch.long)
    z = torch.tensor(test_x, dtype=torch.float32)
    reader = nn.Sequential(nn.Linear(x.shape[1], 64), nn.ReLU(), nn.Linear(64, 36))
    optimizer = torch.optim.Adam(reader.parameters(), lr=.03)
    for _ in range(100):
        optimizer.zero_grad(set_to_none=True)
        loss = F.cross_entropy(reader(x), y)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        logits = reader(z)
        prediction = logits.argmax(-1).numpy()
        return {"accuracy": float(np.mean(prediction == test_y)),
                "cross_entropy_nats": float(F.cross_entropy(logits, torch.tensor(test_y)).item()),
                "correct": int(np.sum(prediction == test_y)), "total": len(test_y),
                "predictions": prediction.tolist()}


def probe_audit(model: RouteNetwork, *, split: dict | None = None,
                oracle_carrier=False) -> dict:
    if split is None:
        split = json.loads((OUTPUT / "probe_split.json").read_text())
    (train_records, train_y), (test_records, test_y) = _probe_data(split)
    train_carriers = _carrier(model, train_records, oracle_carrier=oracle_carrier)
    test_carriers = _carrier(model, test_records, oracle_carrier=oracle_carrier)
    results = {}
    for site in (0, 1):
        site_name = ("raw", "upper")[site]
        results[site_name] = {}
        for family in ("linear", "mlp64"):
            rows = []
            for slot in range(5):
                rows.append(_fit_probe(train_carriers[site], train_y[:, slot],
                                       test_carriers[site], test_y[:, slot],
                                       family=family, seed=2026100802 + slot))
            results[site_name][family] = rows
    floors = []
    rng = np.random.default_rng(2026100804)
    for slot in range(5):
        counts = np.bincount(train_y[:, slot], minlength=36)
        majority = int(counts.argmax())
        shuffled = rng.permutation(test_y[:, slot])
        floors.append({"majority_accuracy": float(np.mean(test_y[:, slot] == majority)),
                       "shuffled_accuracy": float(np.mean(shuffled == test_y[:, slot]))})
    return {"sites": results, "floors": floors, "train_boards": len(train_y),
            "heldout_boards": len(test_y)}


def _probe_summary(row: dict) -> dict:
    return {site: {family: [round(slot["accuracy"], 5) for slot in slots]
                   for family, slots in families.items()}
            for site, families in row["sites"].items()}


def _calibration_model(route: str, law: str, *, current_only=False):
    return ExactRowModel(route, law, current_only=current_only).eval()


def calibrate() -> dict:
    registration()
    if any((OUTPUT / _run_name(route, law, seed)).exists()
           for route in ROUTES for law in LAWS for seed in SEEDS):
        raise ValueError("r8 calibration cannot change after a production run")
    split = probe_split()
    save_json(OUTPUT / "probe_split.json", split)
    row = {"frozen_A": load_frozen_A(ROOT)[1], "probe_split_sha256": sha(OUTPUT / "probe_split.json"),
           "B": {}, "interventions": {}, "probe": {}}
    for law in LAWS:
        row["B"][law] = {}
        row["interventions"][law] = {}
        for name, model in (
            ("forced_A", _calibration_model("a_only", law)),
            ("forced_raw", _calibration_model("raw_only", law)),
            ("current_board_null", _calibration_model("a_only", law, current_only=True)),
        ):
            b = audit_model(model, law, probes=False)
            effects = route_damage(model, law)
            row["B"][law][name] = b
            row["interventions"][law][name] = effects
        if not row["B"][law]["forced_A"]["B_pass"] or not row["B"][law]["forced_raw"]["B_pass"]:
            raise ValueError("predictive oracle fails B controls")
    if row["B"]["original"]["current_board_null"]["B_pass"]:
        raise ValueError("current-board-only null incorrectly passes original law")
    # The constant equal-law row is the exact no-mode null.
    if row["B"]["equal"]["current_board_null"]["natural_excess_KL_bits"] > 1e-10:
        raise ValueError("equal-law constant-row null differs")
    untrained = RouteNetwork("raw_only", 0).eval()
    with torch.random.fork_rng():
        row["probe"]["update0"] = probe_audit(untrained, split=split)
        row["probe"]["oracle"] = probe_audit(untrained, split=split, oracle_carrier=True)
    row["probe"]["oracle_calibrated"] = all(
        slot["accuracy"] >= .99 and slot.get("converged", True)
        for families in row["probe"]["oracle"]["sites"].values()
        for slots in families.values() for slot in slots)
    row["probe"]["update0_summary"] = _probe_summary(row["probe"]["update0"])
    row["probe"]["oracle_summary"] = _probe_summary(row["probe"]["oracle"])
    row["probe"]["calibration_failure_scope"] = (
        None if row["probe"]["oracle_calibrated"] else
        "Spontaneous A readability is not interpretable for probe families below .99; B arms remain valid.")
    save_json(OUTPUT / "calibration.json", row)
    return {"oracle_original_KL": row["B"]["original"]["forced_A"]["natural_excess_KL_bits"],
            "current_board_null_KL": row["B"]["original"]["current_board_null"]["natural_excess_KL_bits"],
            "inactive_route_effects_zero": True,
            "oracle_probe": row["probe"]["oracle_summary"],
            "update0_probe": row["probe"]["update0_summary"],
            "probe_calibrated": row["probe"]["oracle_calibrated"]}


def _run_name(route: str, law: str, seed: int) -> str:
    if route not in ROUTES or law not in LAWS or seed not in SEEDS:
        raise ValueError("r8 run setting differs")
    return f"{route}_{law}_seed{seed}"


def _save_checkpoint(path: Path, model: RouteNetwork, optimizer, stream, candidates,
                     step: int, route: str, law: str, seed: int, curve: list) -> None:
    record = {"model": model.state_dict(), "optimizer": optimizer.state_dict(),
              "stream": stream.state(), "candidates_seen": candidates.seen,
              "torch_rng_state": torch.get_rng_state(), "step": step,
              "route": route, "law": law, "seed": seed, "curve": curve,
              "registration_sha256": sha(OUTPUT / "registration.json"),
              "calibration_sha256": sha(OUTPUT / "calibration.json")}
    if path.exists():
        raise ValueError("r8 checkpoint already exists")
    torch.save(record, path)
    (path.with_suffix(".sha256")).write_text(sha(path) + "\n")


def _restore(run: Path, model: RouteNetwork, optimizer, stream, candidates,
             route: str, law: str, seed: int) -> tuple[int, list]:
    paths = sorted(run.glob("checkpoint_step_*.pt"))
    if not paths:
        return 0, []
    path = paths[-1]
    if path.with_suffix(".sha256").read_text().strip() != sha(path):
        raise ValueError("r8 checkpoint digest differs")
    saved = torch.load(path, map_location="cpu", weights_only=False)
    if (saved["route"], saved["law"], saved["seed"]) != (route, law, seed) or (
            not identity_matches(saved["registration_sha256"], sha(OUTPUT / "registration.json")) or
            not identity_matches(saved["calibration_sha256"], sha(OUTPUT / "calibration.json"))):
        raise ValueError("r8 checkpoint authority differs")
    model.load_state_dict(saved["model"])
    optimizer.load_state_dict(saved["optimizer"])
    stream.rng.bit_generator.state = saved["stream"]["numpy_rng_state"]
    stream.rolling = bytes.fromhex(saved["stream"]["rolling_batch_sha256"])
    stream.draws = saved["stream"]["draws"]
    if stream.state() != saved["stream"]:
        raise ValueError("r8 episode stream restoration differs")
    candidates.seen = saved["candidates_seen"]
    torch.set_rng_state(saved["torch_rng_state"])
    return int(saved["step"]), saved["curve"]


def _checkpoint_audit(model: RouteNetwork, law: str, candidates,
                      *, include_probes=True) -> dict:
    unseen = candidates.mask() if candidates.seen.any() and candidates.mask().any() else None
    with torch.no_grad(), torch.random.fork_rng():
        row = audit_model(model, law, unseen, probes=include_probes, require_unseen=True)
        row["route_damage"] = route_damage(model, law)
    return row


def _futile(curve: list, current: dict, law: str) -> bool:
    initial = curve[0]
    floor_loss = math.log(2) * 1.5 if law == "original" else (
        -sum(float(p) * math.log(float(p)) for p in P_EQUAL))
    initial_gap = max(initial["train_loss_nats"] - floor_loss, 0.0)
    train_closed = ((initial["train_loss_nats"] - current["train_loss_nats"]) /
                    initial_gap if initial_gap > 0 else 0)
    kl_gap = initial["audit"]["natural_excess_KL_bits"]
    kl_closed = ((kl_gap - current["audit"]["natural_excess_KL_bits"]) / kl_gap
                 if kl_gap > 0 else 0)
    current["futility"] = {"train_loss_gap_closed": train_closed,
                           "natural_KL_gap_closed": kl_closed,
                           "no_detectable_B_learning": train_closed < .1 and kl_closed < .1}
    return current["futility"]["no_detectable_B_learning"]


def run(route: str, law: str, seed: int, *, output_root: Path = OUTPUT,
        smoke: bool = False) -> dict:
    registration()
    if not (OUTPUT / "calibration.json").exists():
        raise ValueError("r8 calibration missing")
    _run_name(route, law, seed)
    if smoke and output_root == OUTPUT:
        raise ValueError("smoke output must be outside the registered study")
    steps = 1000 if smoke else 20000
    audits = (0, 1000) if smoke else AUDITS
    run_dir = output_root / _run_name(route, law, seed)
    run_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    boards = enumerate_boards()
    model = RouteNetwork(route, seed)
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),
                                  lr=.003, weight_decay=.01)
    stream = online.OnlineStream(boards, seed, equal_p=law == "equal")
    panel = choice.load_episodes(SOURCE / ("test.npz" if law == "original" else "equal_test.npz"))
    candidates = online.UnseenCandidates(panel)
    current_step, curve = _restore(run_dir, model, optimizer, stream, candidates,
                                   route, law, seed)
    progress = run_dir / "progress.log"

    def log(message: str):
        with progress.open("a") as handle:
            handle.write(message + "\n")
            handle.flush()
        print(message, flush=True)

    log(f"START route={route} law={law} seed={seed} step={current_step} target={steps}")
    if (run_dir / "summary.json").exists():
        recorded = json.loads((run_dir / "summary.json").read_text())
        if recorded["last_step"] == steps or (
                recorded["last_step"] == 5000 and not smoke):
            log(f"COMPLETE existing_step={recorded['last_step']}")
            return recorded
    if current_step == 0 and not curve:
        # Measured update-0 training loss uses the first stream batch without consuming it.
        state = stream.state()
        _, batch = stream.draw()
        records = torch.from_numpy(choice.episode_records(batch, boards))
        lengths = torch.from_numpy(batch.lengths.astype(np.int64))
        targets = torch.from_numpy(batch.targets.astype(np.int64))
        with torch.no_grad():
            initial_loss = float(b_only_loss(model, records, lengths, targets))
        stream.rng.bit_generator.state = state["numpy_rng_state"]
        stream.rolling = bytes.fromhex(state["rolling_batch_sha256"])
        stream.draws = state["draws"]
        row = {"step": 0, "train_loss_nats": initial_loss,
               "audit": _checkpoint_audit(model, law, candidates),
               "stream": stream.state(), "elapsed_seconds": 0.0}
        curve.append(row)
        save_json(run_dir / "audit_step_000000.json", row)
        _save_checkpoint(run_dir / "checkpoint_step_000000.pt", model, optimizer, stream,
                         candidates, 0, route, law, seed, curve)
        log(f"CHECKPOINT step=0 loss={initial_loss:.6f} KL={row['audit']['natural_excess_KL_bits']:.6f}")
    model.train()
    latest_loss = curve[-1]["train_loss_nats"]
    step = current_step
    futile_stop = False
    for step in range(current_step + 1, steps + 1):
        _, batch = stream.draw()
        candidates.observe(batch)
        records = torch.from_numpy(choice.episode_records(batch, boards))
        lengths = torch.from_numpy(batch.lengths.astype(np.int64))
        targets = torch.from_numpy(batch.targets.astype(np.int64))
        optimizer.zero_grad(set_to_none=True)
        loss = b_only_loss(model, records, lengths, targets)
        if not torch.isfinite(loss):
            raise ValueError("r8 B loss non-finite")
        loss.backward()
        optimizer.step()
        latest_loss = float(loss.detach())
        if step in audits:
            row = {"step": step, "train_loss_nats": latest_loss,
                   "audit": _checkpoint_audit(model, law, candidates),
                   "stream": stream.state(),
                   "elapsed_seconds": time.monotonic() - started}
            stop = _futile(curve, row, law) if step == 5000 else False
            curve.append(row)
            save_json(run_dir / f"audit_step_{step:06d}.json", row)
            _save_checkpoint(run_dir / f"checkpoint_step_{step:06d}.pt", model, optimizer,
                             stream, candidates, step, route, law, seed, curve)
            log(f"CHECKPOINT step={step} loss={latest_loss:.6f} "
                f"KL={row['audit']['natural_excess_KL_bits']:.6f} "
                f"B_pass={row['audit']['B_pass']}")
            if stop:
                log(f"FUTILITY_STOP step={step}")
                futile_stop = True
                break
        elif step % 250 == 0:
            log(f"PROGRESS step={step} loss={latest_loss:.6f}")
    elapsed = time.monotonic() - started
    summary = {"route": route, "law": law, "seed": seed, "last_step": step,
               "smoke": smoke, "elapsed_seconds": elapsed,
               "updates_per_second": max(0, step - current_step) / elapsed,
               "worker_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "curve": [{"step": row["step"], "train_loss_nats": row["train_loss_nats"],
                          "natural_excess_KL_bits": row["audit"]["natural_excess_KL_bits"],
                          "B_pass": row["audit"]["B_pass"]} for row in curve]}
    save_json(run_dir / "summary.json", summary)
    if not futile_stop:
        log(f"COMPLETE step={step} updates_per_second={summary['updates_per_second']:.4f} "
            f"max_rss_kib={summary['worker_max_rss_kib']}")
    return summary


def _probe_gain(current: dict, baseline: dict, oracle_row: dict,
                heldout_targets: np.ndarray) -> dict:
    rng = np.random.default_rng(2026100803)
    result = {}
    for site, families in current["sites"].items():
        result[site] = {}
        for family, slots in families.items():
            result[site][family] = []
            for slot, item in enumerate(slots):
                old = baseline["sites"][site][family][slot]
                oracle_item = oracle_row["sites"][site][family][slot]
                # Paired board bootstrap of correctness differences.
                truth = heldout_targets[:, slot]
                new_ok = np.asarray(item["predictions"]) == truth
                old_ok = np.asarray(old["predictions"]) == truth
                differences = new_ok.astype(float) - old_ok.astype(float)
                draws = rng.integers(0, len(truth), size=(1000, len(truth)))
                ci = np.quantile(differences[draws].mean(1), [.025, .975]).tolist()
                result[site][family].append({
                    "slot": slot, "gain": float(differences.mean()), "gain_CI95": ci,
                    "oracle_calibrated": oracle_item["accuracy"] >= .99,
                    "fits_converged": all(value.get("converged", True)
                                          for value in (item, old, oracle_item)),
                    "untrained_at_oracle_ceiling": old["accuracy"] >= oracle_item["accuracy"] - .01,
                    "training_related_gain": (ci[0] > 0 and all(
                        value.get("converged", True) for value in (item, old, oracle_item))
                                              and oracle_item["accuracy"] >= .99
                                              and old["accuracy"] < oracle_item["accuracy"] - .01),
                })
    return result


def _endpoint_probe_rows(rows: dict, endpoint_audits: dict) -> list[dict]:
    """Align saved endpoint probes and paired intervals across the two laws."""

    aligned = []
    for seed in SEEDS:
        original = rows[f"raw_only_original_seed{seed}"]["probe_table"]
        equal = rows[f"raw_only_equal_seed{seed}"]["probe_table"]
        by_law = {"original": original, "equal": equal}
        for site in ("raw", "upper"):
            for family in ("linear", "mlp64"):
                for slot in range(5):
                    entry = {"seed": seed, "carrier": site, "probe_family": family,
                             "slot": slot + 1}
                    for law in LAWS:
                        audits = endpoint_audits[f"raw_only_{law}_seed{seed}"]
                        baseline = audits[0]["audit"]["probes"]
                        endpoint = audits[20000]["audit"]["probes"]
                        gain = next(row for row in by_law[law]
                                    if row["step"] == 20000)["gain"][site][family][slot]
                        before = baseline["sites"][site][family][slot]
                        after = endpoint["sites"][site][family][slot]
                        entry[law] = {
                            "update0_accuracy": before["accuracy"],
                            "endpoint_accuracy": after["accuracy"],
                            "paired_gain": gain["gain"],
                            "paired_gain_CI95": gain["gain_CI95"],
                            "majority_floor": endpoint["floors"][slot]["majority_accuracy"],
                            "converged": gain["fits_converged"] if family == "linear" else None,
                            "fit_status": ("converged" if gain["fits_converged"] else
                                           "not converged") if family == "linear" else
                                          "fixed budget; convergence not assessed",
                        }
                    aligned.append(entry)
    return aligned


def _probe_cell(row: dict) -> str:
    interval = row["paired_gain_CI95"]
    return (f"{row['update0_accuracy']:.3f} → {row['endpoint_accuracy']:.3f}; "
            f"Δ {row['paired_gain']:+.3f} [{interval[0]:+.3f}, {interval[1]:+.3f}]; "
            f"floor {row['majority_floor']:.3f}; {row['fit_status']}")


def aggregate() -> dict:
    registration()
    calibration = json.loads((OUTPUT / "calibration.json").read_text())
    heldout_targets = _probe_data(json.loads((OUTPUT / "probe_split.json").read_text()))[1][1]
    rows = {}
    endpoint_audits = {}
    for law in LAWS:
        for seed in SEEDS:
            for route in ROUTES:
                name = _run_name(route, law, seed)
                run_dir = OUTPUT / name
                if not (run_dir / "summary.json").exists():
                    continue
                summary = json.loads((run_dir / "summary.json").read_text())
                audits = [json.loads(path.read_text()) for path in sorted(
                    run_dir.glob("audit_step_*.json"))]
                crossing = next((row["step"] for row in audits if row["audit"]["B_pass"]), None)
                endpoint = next((row for row in audits if row["step"] == 20000), None)
                entry = {"first_audited_crossing": crossing,
                         "endpoint_label": ("B_PASS" if endpoint and endpoint["audit"]["B_pass"]
                                            else "FUTILITY_STOP" if summary["last_step"] == 5000
                                            else "B_INCOMPLETE"),
                         "loss_KL_curve": summary["curve"],
                         "route_damage_curve": [{"step": row["step"],
                             "effects": row["audit"]["route_damage"]["effects"]} for row in audits]}
                if route == "raw_only":
                    endpoint_audits[name] = {row["step"]: row for row in audits}
                    paired_update0 = audits[0]["audit"]["probes"]
                    entry["probe_table"] = [{"step": row["step"],
                        "heldout": _probe_summary(row["audit"]["probes"]),
                        "gain": _probe_gain(row["audit"]["probes"],
                            paired_update0, calibration["probe"]["oracle"], heldout_targets)}
                        for row in audits]
                rows[name] = entry
    endpoint_probes = _endpoint_probe_rows(rows, endpoint_audits)
    failed_raw_bars = []
    for seed in SEEDS:
        name = f"raw_only_original_seed{seed}"
        endpoint = endpoint_audits[name][20000]["audit"]
        cases = endpoint["swaps"]["cases"]
        named_cases = ("reset_L", "set_H", "neutral_N", "same_category_substitution",
                       "upper_state_exchange_same_N")
        failed_raw_bars.append({
            "seed": seed,
            "law_TV": {"pass": endpoint["criteria"]["law_TV"],
                       "maximum_TV": endpoint["mode_law"]["maximum_TV"],
                       "limit": .02},
            "swaps": {"pass": endpoint["criteria"]["swaps"], "limit": .02,
                      "failed_cases_maximum_TV": {
                          key: cases[key]["maximum_TV"] for key in named_cases
                          if cases[key]["maximum_TV"] > .02}},
        })
    raw_original_incomplete = all(
        rows[f"raw_only_original_seed{seed}"]["endpoint_label"] == "B_INCOMPLETE"
        for seed in SEEDS)
    selected = (
        "Original-law raw-only is B-incomplete in all three seeds: the worst-case "
        "mode-law and causal-swap bars fail. Its increased measured slot-1 A readability "
        "is conditional on that B failure; the registered readings requiring raw-only "
        "to pass B do not apply. Other slots' reduced probe accuracy does not establish "
        "information absence or erasure. Equal-law slot-1 gains are also reported."
        if raw_original_incomplete else
        "Select an applicable registered reading from the completed B criteria and "
        "probe results; no raw-only B-incomplete conclusion is asserted here.")
    report = {"registered_reading": READINGS, "selected_applicable_reading": selected,
              "rows": rows, "raw_only_endpoint_probes": endpoint_probes,
              "raw_only_failed_original_bars": failed_raw_bars,
              "historical_comparator": "r5 was trained with A-answer loss; it is not paired with r8",
              "route_conflict_caveat": ablation.CAVEAT}
    save_json(OUTPUT / "aggregate.json", report)
    saved_report = json.loads((OUTPUT / "aggregate.json").read_text())
    rows = saved_report["rows"]
    endpoint_probes = saved_report["raw_only_endpoint_probes"]
    failed_raw_bars = saved_report["raw_only_failed_original_bars"]
    report_lines = [
        "# r8 route-access aggregate", "", "## Registered readings (verbatim)", "",
        saved_report["registered_reading"], "", "## Selected applicable reading", "",
        saved_report["selected_applicable_reading"], "",
        "## B endpoints", "", "| Run | First crossing | Endpoint |",
        "|---|---:|---|",
        *(f"| {key} | {value['first_audited_crossing']} | {value['endpoint_label']} |"
          for key, value in sorted(rows.items())), "",
        "## Raw-only original-law failed bars at 20,000 updates", "",
        "| Seed | Law maximum TV (limit 0.020) | Failed swap cases: maximum TV "
        "(limit 0.020) |", "|---:|---:|---|",
        *(f"| {row['seed']} | {row['law_TV']['maximum_TV']:.6f} "
          f"({'pass' if row['law_TV']['pass'] else 'fail'}) | "
          + ", ".join(f"{key} {value:.6f}" for key, value in
                      row["swaps"]["failed_cases_maximum_TV"].items()) + " |"
          for row in failed_raw_bars), "",
        "## Raw-only endpoint probe measurements", "",
        "Each law cell gives update-0 → 20,000 held-out accuracy; paired gain "
        "[saved 95% interval]; majority floor; linear-fit convergence. The MLP is "
        "fixed-budget, with convergence not assessed.", "",
        "| Seed | Carrier | Probe | Slot | Original law | Equal law |",
        "|---:|---|---|---:|---|---|",
        *(f"| {row['seed']} | {row['carrier']} | {row['probe_family']} | "
          f"{row['slot']} | {_probe_cell(row['original'])} | "
          f"{_probe_cell(row['equal'])} |" for row in endpoint_probes), "",
        saved_report["route_conflict_caveat"], "",
    ]
    (OUTPUT / "aggregate.md").write_text("\n".join(report_lines))
    return {"runs": len(rows), "endpoint_passes": sum(
        row["endpoint_label"] == "B_PASS" for row in rows.values())}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    command = parser.add_subparsers(dest="stage", required=True)
    command.add_parser("register")
    command.add_parser("calibrate")
    training = command.add_parser("run")
    training.add_argument("--route", required=True, choices=ROUTES)
    training.add_argument("--law", required=True, choices=LAWS)
    training.add_argument("--seed", required=True, type=int, choices=SEEDS)
    training.add_argument("--smoke", action="store_true")
    training.add_argument("--output-root", type=Path, default=OUTPUT)
    command.add_parser("aggregate")
    args = parser.parse_args()
    if args.stage == "register":
        result = register()
    elif args.stage == "calibrate":
        result = calibrate()
    elif args.stage == "run":
        result = run(args.route, args.law, args.seed,
                     output_root=args.output_root, smoke=args.smoke)
    else:
        result = aggregate()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
