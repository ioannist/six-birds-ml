"""Registered r13 mechanism experiments. No implicit study execution."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import resource
import time
from pathlib import Path
from recombination_promotion.public_paths import public_path, metadata_matches

import numpy as np
import torch
from torch.func import stack_module_state

from recombination_promotion.oldgame_ext import game
from recombination_promotion.oldgame_ext.memory import VALUES
from recombination_promotion.oldgame_ext.multiround import load_frozen_A
from recombination_promotion.oldgame_ext.multiround_coverage import CoverageStream
from recombination_promotion.oldgame_ext.multiround_jagged import DeviceStream, new_model
from recombination_promotion.oldgame_ext.multiround_mechanism import (
    AUDITS, NOISE, MechanismNetwork, Run, all_runs,
    cutoff_summary, fixed_geometry_pairs,
    gradient_conflict, gradient_statistics, histories_logits,
    loss_parts, margin_counts, matched_sgd_rate,
)
from scripts import oldgame_multiround_coverage as r12
from scripts import oldgame_multiround_jagged as r11


ROOT = r11.ROOT
OUTPUT = ROOT / "reports/phase11/oldgame_memory/multiround/study_r13_mechanism"
SPEC = OUTPUT / "specification.md"
BULK = public_path("bulk/study_r13_mechanism_bulk")
THREADS = {"CPU_threads_per_process": 1, "maximum_processes": 3}


def source_checkpoint(seed):
    summary = r12.OUTPUT / f"a_target_original_seed{seed}/summary.json"
    row = json.loads(summary.read_text())
    if row["step"] != 20000 or row["authority"]["smoke"]:
        raise ValueError("supplier is not the fixed production endpoint")
    path = public_path(row["bulk_directory"]) / "checkpoint_step_020000.pt"
    saved = r12._bound_load(path)
    if not metadata_matches(saved["authority"], row["authority"]) or saved["step"] != 20000:
        raise ValueError("supplier checkpoint authority differs")
    return path, saved


def identities():
    paths = {"design": SPEC, "script": Path(__file__),
             "module": ROOT / "src/recombination_promotion/oldgame_ext/multiround_mechanism.py",
             "r12_script": Path(r12.__file__), "r11_script": Path(r11.__file__),
             "r12_module": ROOT / "src/recombination_promotion/oldgame_ext/multiround_coverage.py",
             "r11_module": ROOT / "src/recombination_promotion/oldgame_ext/multiround_jagged.py",
             "memory": ROOT / "src/recombination_promotion/oldgame_ext/memory.py",
             "game": ROOT / "src/recombination_promotion/oldgame_ext/game.py",
             "r8_script": Path(r11.r8.__file__), "panels_and_decisions": Path(r11.choice.__file__),
             "probes": ROOT / "src/recombination_promotion/oldgame_ext/jagged_probes.py",
             "probe_split": r11.r8.OUTPUT / "probe_split.json",
             "panels": r11.choice.OUTPUT / "manifest.json",
             "r9_cases": r11.r9.OUTPUT / "results.json"}
    return {key: r11.sha(path) for key, path in paths.items()}


def settings():
    return {"steps": 20000, "erosion_steps": 200, "batch": 256,
            "lr": .003, "wd": .01, "epsilon": 1e-8, "precision": "float32",
            "audit_steps": list(AUDITS), "probe_steps": [0, 5000, 20000],
            "widths": {"noise": 3, "erosion": 1, "access": 1, "encoding": 1},
            **THREADS, "linear_probe": r11.LINEAR_SETTINGS, "MLP_probe": r11.MLP_SETTINGS,
            "numerical_encoding": "(sum_twelfths/36,1-sum_twelfths/36,0,...,0)",
            "loss": "0.5 natural-position mean + 0.5 coverage-endpoint mean; A active rounds x five slots",
            "supplier_ST": "hard + soft - stop_gradient(soft)",
            "criteria": {"KL_bits": .01, "TV": .02, "witness_recovery": .8},
            "futility": {"initial_excess": "B_0 - F_0",
                         "current_excess": "mean of last 100 per-batch excess_prediction_loss",
                         "closure": "(initial_excess - current_excess) / initial_excess",
                         "nonpositive_initial_excess": "loss criterion unavailable; do not stop",
                         "natural_KL_and_supervised_sums": "unchanged"},
            "equivalence_tolerances": r11.EQUIVALENCE_TOLERANCE}


def register(device):
    sources = {str(s): {"path": str(source_checkpoint(s)[0]),
                       "sha256": r11.sha(source_checkpoint(s)[0])} for s in range(3)}
    _, a = load_frozen_A(ROOT)
    boards = r11.enumerate_boards()
    split = json.loads((r11.r8.OUTPUT / "probe_split.json").read_text())
    # Board identities, never network states, determine the geometry panel.
    geometry = fixed_geometry_pairs(boards, {"train": split["train_board_ids"],
                                            "heldout": split["heldout_board_ids"]})
    gp = OUTPUT / "geometry_pairs.json"
    if gp.exists() and json.loads(gp.read_text()) != geometry:
        if any(OUTPUT.glob("*/summary.json")):
            raise ValueError("fixed geometry identities differ after study execution")
        version = 1
        while (OUTPUT / f"geometry_pairs_build_v{version}.json").exists():
            version += 1
        gp.rename(OUTPUT / f"geometry_pairs_build_v{version}.json")
    r11.write_json(gp, geometry)
    row = {"study": "study_r13_mechanism", "specification_verbatim": SPEC.read_text(),
           "source_sha256": identities(), "settings": settings(), "frozen_A": a,
           "supplier_endpoints": sources, "geometry_pairs_sha256": r11.sha(gp),
           "runs": [r.__dict__ for r in all_runs()], "registration_device": device.type,
           "choices": [
               "Reuse r12 panels and decision functions unchanged; N3–N8 is the long panel.",
               "All access conditions instantiate an immobile supplier copy; live and frozen hard answers use the same 36-way straight-through convention.",
               "Erosion uses the r11 original DeviceStream and B-only loss; local histories are exhaustively scored at every update, completed boards are the active sampled rounds.",
               "SGD first-batch rate matches the sums-gradient displacement norm only; fixed decay multiplier is 0.99997.",
               "Zero-gradient blocked memory parameters retain decay and explicit zero Adam moments; they are not skipped.",
               "Fixed audit batch comes from an independent seed 130013; it never consumes the training stream.",
               "Geometry pairs are fixed within the existing board-disjoint probe allocation before states are read; all eligible pairs are retained, including missing-value support.",
               "Readability is reported only for converged linear fits; probe gains use the saved paired predictions and fixed board bootstrap.",
               "Futility uses E0=B0-F0 and the last-100 mean of recorded per-batch excess_prediction_loss; a nonpositive E0 cannot stop a run.",
               "Geometry has a separate analysis amendment and calibration; it is excluded from training calibration and checkpoint authority.",
               "CPU smoke uses reduced census/probe panels and is not a study endpoint; no threshold is changed.",
               "Bulk paths are configurable for permitted temporary CPU checks; host outputs use the prescribed runs directory."]}
    path = OUTPUT / "registration.json"
    if path.exists():
        old = json.loads(path.read_text())
        if {k: v for k, v in old.items() if k != "registration_device"} != {
                k: v for k, v in row.items() if k != "registration_device"}:
            if any(OUTPUT.glob("*/summary.json")):
                raise ValueError("cannot change registration after study runs")
            version = 1
            while (OUTPUT / f"registration_build_v{version}.json").exists():
                version += 1
            path.rename(OUTPUT / f"registration_build_v{version}.json")
            md = OUTPUT / "registration.md"
            if md.exists():
                md.rename(OUTPUT / f"registration_build_v{version}.md")
            for name in ("calibration.json", "calibration.md"):
                p = OUTPUT / name
                if p.exists():
                    p.rename(OUTPUT / f"{p.stem}_build_v{version}{p.suffix}")
        else:
            return old
    r11.write_json(path, row)
    (OUTPUT / "registration.md").write_text("# r13 registration\n\n" + SPEC.read_text() +
        "\n## Fixed implementation choices\n\n" + "\n".join("- " + c for c in row["choices"]) + "\n")
    return row


def registration():
    row = json.loads((OUTPUT / "registration.json").read_text())
    if row["source_sha256"] != identities() or row["settings"] != settings():
        raise ValueError("r13 registration differs from executed sources")
    if row["geometry_pairs_sha256"] != r11.sha(OUTPUT / "geometry_pairs.json"):
        raise ValueError("geometry panel identity differs")
    for s, record in row["supplier_endpoints"].items():
        if record["sha256"] != r11.sha(source_checkpoint(int(s))[0]):
            raise ValueError("fixed supplier identity differs")
    return row


def make_model(run, device):
    torch.manual_seed(run.seed)
    model = MechanismNetwork(run.condition)
    source, _ = load_frozen_A(ROOT)
    model.memory.load_state_dict(source.core.state_dict(), strict=True)
    if run.experiment in ("access", "encoding"):
        _, saved = source_checkpoint(run.seed)
        state = saved["model"]
        for name in ("raw_embedding", "raw_encoder", "raw_sum_head"):
            getattr(model, name).load_state_dict({k[len(name) + 1:]: v for k, v in state.items()
                                                if k.startswith(name + ".")}, strict=True)
        model.supplier_embedding.load_state_dict(model.raw_embedding.state_dict())
        model.supplier_encoder.load_state_dict(model.raw_encoder.state_dict())
        model.supplier_head.load_state_dict(model.raw_sum_head.state_dict())
    return model.to(device)


class Engine(r11.GroupEngine):
    def __init__(self, runs, device):
        if len(runs) > (3 if runs[0].experiment == "noise" else 1):
            raise ValueError("r13 execution width differs")
        if len({r.condition for r in runs}) != 1:
            raise ValueError("execution batch mixes conditions")
        self.runs, self.device = runs, device
        self.models = [make_model(r, device) for r in runs]
        self.parameters, self.buffers = stack_module_state(self.models)
        self.optimizer = r11.StackedAdamW(self.parameters, len(runs))

    def update(self, batches, active):
        self.optimizer.zero_grad()
        output = self.forward(torch.stack([b.records for b in batches]),
                              torch.stack([b.lengths for b in batches]))
        parts = [loss_parts(tuple(v[i] for v in output), b, r)
                 for i, (b, r) in enumerate(zip(batches, self.runs, strict=True))]
        loss = torch.stack([p[0] for p in parts])
        if not torch.isfinite(loss).all():
            raise ValueError("non-finite mechanism training loss")
        (loss * active).sum().backward()
        used = torch.tensor([r.supervised for r in self.runs], device=self.device)
        self.optimizer.step(active, {k: used for k in self.parameters if k.startswith("raw_sum_head.")})
        return [p[1] for p in parts]

    def model_at(self, index, *, cpu=False):
        model = copy.deepcopy(self.models[index])
        model.load_state_dict({k: v[index].detach() for k, v in self.parameters.items()} |
                              {k: v[index].detach() for k, v in self.buffers.items()})
        return model.to("cpu" if cpu else self.device).eval()


def calibration(device, bulk):
    registration()
    start = time.monotonic()
    tables = r11.BoardTables(device)
    result = {"registration_sha256": r11.sha(OUTPUT / "registration.json"),
              "device": device.type, "B": {}, "checks": {}}
    for law in ("original", "equal"):
        candidate = r12._candidate(law)
        stream = CoverageStream(tables, 17, law, "uniform")
        for _ in range(128):
            r11._observe(candidate, stream.draw_batch())
        if not candidate.mask().any():
            raise ValueError("unseen calibration is empty")
        rows = {}
        for name, current in (("oracle", False), ("board_only", True)):
            rows[name] = r11._score_b(r11.r8.ExactRowModel("raw_only", law,
                                       current_only=current).eval(), law, candidate, reject_empty=True)
        if not rows["oracle"]["B_pass"] or rows["board_only"]["B_pass"] != (law == "equal"):
            raise ValueError("law-aware B calibration does not separate")
        result["B"][law] = rows
    untrained = make_model(Run("noise", NOISE[0], 0), device)
    null = r11._score_b(r11.DeviceAuditAdapter(untrained, device), "original",
                         r12._candidate("original"), reject_empty=True)
    if null["B_pass"]:
        raise ValueError("untrained B calibration passes")
    result["untrained_B"] = null
    # Predictive signatures (including every fixed rendering and the saved r9
    # cases) are separate deciding functions from the episode-level B bars.
    result["signatures"] = {}
    for law in ("original", "equal"):
        census = r11.board_census(r11.r8.ExactRowModel("raw_only", law).eval(),
                                  law, torch.device("cpu"))
        panels = (census["registered_rendering"], *census["additional_fixed_renderings"],
                  census["saved_r9_failed_renderings"])
        if any(row["above_0_02_TV"] for row in panels):
            raise ValueError("oracle predictive-signature calibration fails")
        if any(row["boards"] <= 0 for row in panels[:4]):
            raise ValueError("predictive census calibration is empty")
        result["signatures"][law] = {"oracle": census, "cutoff_band": cutoff_summary(census)}
    negative_census = r11.board_census(untrained, "original", device)
    if negative_census["registered_rendering"]["above_0_02_TV"] == 0:
        raise ValueError("untrained predictive census does not separate")
    result["signatures"]["untrained"] = negative_census
    result["diagnosis"] = r12.calibrate_diagnostics()
    exact = make_model(Run("access", "exact", 0), device)
    local = margin_counts(histories_logits(exact.memory))
    boards = r11.a_accuracy(exact, device)
    if local["correct"] != 1555 or boards["vector"]["correct"] != 24435:
        raise ValueError("A positive is not exact")
    result["A"] = {"exact_local": local, "exact_board": boards,
                    "untrained_head": r11.a_accuracy(untrained, device)}
    true_local = [game.sigma(h) for h in game.histories()]
    majority = max(set(true_local), key=true_local.count)
    result["A"]["majority_local"] = {"value": majority,
        "correct": true_local.count(majority), "total": 1555}
    zero = tensor_hash(exact.state_dict())
    replay = margin_counts(histories_logits(exact.memory))
    if tensor_hash(exact.state_dict()) != zero or replay != local:
        raise ValueError("zero-update exact A replay differs")
    logits = histories_logits(exact.memory).detach().clone()
    before = logits.argmax(-1)
    logits[0, (int(before[0]) + 1) % 36] = logits[0].max() + 1
    if margin_counts(logits)["correct"] != 1554:
        raise ValueError("planted logit flip not detected")
    result["probes"] = {"oracle": r11.probe_audit(untrained, device, oracle=True),
                        "untrained": r11.probe_audit(untrained, device)}
    minimum = min(r["accuracy"] for site in result["probes"]["oracle"]["sites"].values()
                  for family in site.values() for r in family["sum36"])
    if minimum < .99 or any(r["converged"] is False for site in
            result["probes"]["oracle"]["sites"].values() for family in site.values()
            for r in family["sum36"]):
        raise ValueError("oracle probes fail")
    # A trained shuffled-label reader, not just a shuffled-prediction count.
    from recombination_promotion.oldgame_ext.jagged_probes import fit_reader
    split = json.loads((r11.r8.OUTPUT / "probe_split.json").read_text())
    (train_records, train_y), (held_records, held_y) = r11.r8._probe_data(split)
    train_carrier = r11.r8._carrier(untrained.cpu(), train_records, oracle_carrier=True)
    held_carrier = r11.r8._carrier(untrained.cpu(), held_records, oracle_carrier=True)
    untrained.to(device)
    floors = {}
    for site, name in enumerate(("raw", "upper")):
        floors[name] = {}
        for family in ("linear", "mlp64"):
            floors[name][family] = []
            for slot in range(5):
                permutation = np.random.default_rng(130015 + slot).permutation(len(train_y))
                floors[name][family].append(fit_reader(
                    torch.from_numpy(train_carrier[site]).to(device),
                    torch.from_numpy(train_y[permutation, slot]).to(device),
                    torch.from_numpy(held_carrier[site]).to(device),
                    torch.from_numpy(held_y[:, slot]).to(device), family=family, seed=130015))
    result["probes"]["fitted_shuffled_label_floor"] = floors
    result["probability_loss"] = {}
    for law in ("original", "equal"):
        b = CoverageStream(tables, 130013, law, "uniform").draw_batch()
        from recombination_promotion.oldgame_ext.multiround_mechanism import exact_rows, prediction_loss
        p = exact_rows(b)
        result["probability_loss"][law] = {}
        for probability in (False, True):
            loss, floor = prediction_loss(p.log(), b, probability=probability)
            if not torch.equal(loss, floor):
                raise ValueError("executed oracle prediction loss differs from target floor")
            result["probability_loss"][law][str(probability)] = float(floor)
    # Analytic first step and zero-gradient decay use the same displacement function.
    parameter = torch.nn.Parameter(torch.tensor([1., -2., .5], device=device))
    gradient = torch.tensor([.2, -1e-10, 0.], device=device)
    old = parameter.detach().clone()
    optimizer = torch.optim.AdamW([parameter], lr=.003, weight_decay=.01)
    parameter.grad = gradient.clone()
    optimizer.step()
    analytic = old * .99997 - .003 * gradient / (gradient.abs() + 1e-8)
    if not torch.allclose(parameter, analytic, atol=2e-7, rtol=0):
        raise ValueError("analytic Adam displacement differs")
    result["movement"] = {"analytic_maximum_error": float((parameter - analytic).detach().abs().max())}
    old = parameter.detach().clone()
    optimizer = torch.optim.AdamW([parameter], lr=.003, weight_decay=.01)
    parameter.grad = torch.zeros_like(parameter)
    optimizer.step()
    if not torch.equal(parameter, old * .99997):
        raise ValueError("blocked gradient decay differs")
    result["movement"]["blocked_decay_displacement"] = float((parameter - old).norm())
    # Executed straight-through route, compared with detached supplier.
    sample = stream.draw_batch()
    live = make_model(Run("access", "live", 0), device)
    frozen = make_model(Run("access", "frozen", 0), device)
    result["supplier_access"] = {"live": gradient_conflict(live, sample),
                                  "detached": gradient_conflict(frozen, sample)}
    if (result["supplier_access"]["live"]["live_sums_route_prediction_gradient_norm"] <= 0 or
            result["supplier_access"]["detached"]["live_sums_route_prediction_gradient_norm"] != 0):
        raise ValueError("supplier access calibration fails")
    result["futility"] = futility_calibration()
    # All associated conclusions remain blocked unless their executed calibration passed.
    result["checks"] = {"B": True, "signatures": True, "sums": True, "probes": True,
                         "movement": True, "futility": result["futility"]["pass"],
                         "diagnosis": True, "supplier_access": True}
    result["elapsed_seconds"] = time.monotonic() - start
    bulk.mkdir(parents=True, exist_ok=True)
    path = bulk / "calibration_details.json"
    r11.write_json(path, result)
    compact = {k: result[k] for k in ("registration_sha256", "device", "checks", "elapsed_seconds")}
    compact["B"] = {law: {name: {"pass": row["B_pass"], "criteria": row["criteria"],
        "natural_KL_bits": row["natural_excess_KL_bits"], "unseen_count": row["unseen_count"],
        "law_maximum_TV": row["mode_law"]["maximum_TV"]} for name, row in rows.items()}
        for law, rows in result["B"].items()}
    compact["A"] = {"local_correct": local["correct"], "local_total": 1555,
                    "board_correct": boards["vector"]["correct"], "board_total": 24435}
    compact["oracle_probe_minimum"] = minimum
    compact["signature_calibration"] = {law: {
        "oracle_cutoff_band": result["signatures"][law]["cutoff_band"],
        "oracle_saved_r9": result["signatures"][law]["oracle"]["saved_r9_failed_renderings"]}
        for law in ("original", "equal")}
    compact["signature_calibration"]["untrained_errors"] = negative_census[
        "registered_rendering"]["above_0_02_TV"]
    compact["futility"] = result["futility"]
    compact["supplier_access"] = result["supplier_access"]
    compact["movement"] = result["movement"]
    compact["details"] = {"path": str(path), "sha256": r11.sha(path)}
    r11.write_json(OUTPUT / "calibration.json", compact)
    (OUTPUT / "calibration.md").write_text("# r13 calibration\n\n" +
        json.dumps(compact, indent=2) + "\n")
    return compact


def geometry_amendment(*, rebuild=False):
    """Independent analysis binding; never added to a training checkpoint authority."""
    from recombination_promotion.oldgame_ext import mechanism_geometry as geometry
    path = OUTPUT / "geometry_amendment.json"
    row = {"scope": "analysis only; no optimizer, endpoint or stopping authority",
           "source_sha256": r11.sha(Path(geometry.__file__)), "settings": geometry.SETTINGS,
           "reader_source_sha256": r11.sha(ROOT / "src/recombination_promotion/oldgame_ext/jagged_probes.py"),
           "pair_identities_sha256": r11.sha(OUTPUT / "geometry_pairs.json"),
           "legacy_failure": {"path": str(OUTPUT / "geometry_failure_build_v1.json"),
                              "sha256": r11.sha(OUTPUT / "geometry_failure_build_v1.json")}}
    if path.exists() and json.loads(path.read_text()) != row:
        if not rebuild:
            raise ValueError("geometry analysis amendment differs")
        version = 1
        while (OUTPUT / f"geometry_amendment_v{version}.json").exists():
            version += 1
        path.rename(OUTPUT / f"geometry_amendment_v{version}.json")
        calibration_path = OUTPUT / "geometry_calibration.json"
        if calibration_path.exists():
            calibration_path.rename(OUTPUT / f"geometry_calibration_v{version}.json")
    if rebuild:
        r11.write_json(path, row)
    elif not path.exists():
        raise ValueError("geometry analysis amendment is absent")
    return row


def geometry_calibration():
    from recombination_promotion.oldgame_ext.mechanism_geometry import calibration
    geometry_amendment()
    row = calibration()
    row["amendment_sha256"] = r11.sha(OUTPUT / "geometry_amendment.json")
    row["legacy_failure"] = geometry_amendment()["legacy_failure"]
    legacy = load_reference(row["legacy_failure"])
    row["original_permutation_result"] = load_reference(legacy["details"])["geometry"]
    r11.write_json(OUTPUT / "geometry_calibration.json", row)
    return row


def supplier_accuracy(model, device, *, smoke=False):
    boards = r11.enumerate_boards()
    ids = np.arange(len(boards.boards))
    if smoke:
        ids = ids[np.linspace(0, len(ids) - 1, 128, dtype=int)]
    truth = torch.tensor(np.asarray(boards.boards)[ids], device=device)
    values = truth.new_tensor(VALUES)
    predictions = [[] for _ in range(4)]
    with torch.no_grad():
        for k in range(4):
            records = r11._census_records(boards, ids, render_offset=k)
            for at in range(0, len(records), 256):
                x = torch.from_numpy(records[at:at + 256]).to(device)
                if model.condition in ("exact", "onehot", "numerical"):
                    logits = model.round_interfaces(x)[0]
                elif model.condition == "live":
                    logits = model.raw_sum_head(model.raw_state(x)).reshape(-1, 5, 36)
                else:
                    logits = model.supplier_logits(x)
                predictions[k].append(values[logits.argmax(-1)])
    predictions = [torch.cat(p) for p in predictions]
    return {"operative": model.dual, "supplier_type": model.condition,
            "per_slot": [{"correct": int((predictions[0][:, k] == truth[:, k]).sum()),
                           "total": len(ids)} for k in range(5)],
            "vector": {"correct": int((predictions[0] == truth).all(-1).sum()), "total": len(ids)},
            "rerender_components": [int((p != predictions[0]).sum()) for p in predictions],
            "immobility_sha256": tensor_hash({n: p for n, p in model.state_dict().items()
                                              if n.startswith("supplier_")})}


def tensor_hash(state):
    h = hashlib.sha256()
    for name, value in sorted(state.items()):
        h.update(name.encode())
        h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def audit(model, run, candidate, stream, device, step, details, bulk, *, smoke):
    start = time.monotonic()
    adapter = r11.DeviceAuditAdapter(model, device)
    b = r11._score_b(adapter, run.law, candidate)
    b["route_damage"] = r11.r8.route_damage(adapter, run.law)
    b["board_census"] = r11.board_census(model, run.law, device, smoke=smoke)
    a = r11.a_accuracy(model, device, smoke=smoke)
    row = {"step": step, "train_parts": details, "audit": b,
           "A_board_accuracy": a, "A_accuracy": a["vector"]["correct"] / a["vector"]["total"],
           "category_error_decomposition": [r12.category_counts(model, device, smoke=smoke,
                 render_offset=k, law=run.law) for k in range(4)],
           "prefix_diagnosis": r12.prefix_diagnosis(model, run.law, stream, device),
           "exposure": r11._exposures(stream, bulk / f"exposure_step_{step:06d}.npz"),
           "stratum_endpoints": stream.stratum_exposure.tolist(),
           "projected_20k_stratum_endpoints": [[160000] * 8] * 2,
           "conditional_endpoint_target_counts": stream.endpoint_targets.tolist(),
           "stream_rolling_hash": stream.rolling.hex(), "reduced_smoke": smoke}
    row["cutoff_band"] = cutoff_summary(b["board_census"])
    row["supplier_accuracy"] = supplier_accuracy(model, device, smoke=smoke)
    row["local_history_scope"] = "frozen A source, not raw-state sums head"
    fixed = CoverageStream(stream.tables, 130013, run.law, "uniform").draw_batch()
    row["gradient_conflict"] = gradient_conflict(model, fixed)
    if step in (0, 5000, 20000) or smoke:
        row["probes"] = r11.probe_audit(model, device, smoke=smoke)
    if run.experiment == "noise" and run.condition.startswith("raw_") and step in (0, 5000, 20000):
        row["geometry"] = geometry_audit(model, device, bulk, step)
    row["elapsed_seconds"] = time.monotonic() - start
    return row


def futility(first, current, run):
    gap = first["train_parts"]["B"] - first["train_parts"]["target_floor"]
    current_excess = current["train_parts"]["excess_prediction_loss"]
    closure = (gap - current_excess) / gap if gap > 0 else None
    kl = first["audit"]["natural_excess_KL_bits"]
    kl_closed = (kl - current["audit"]["natural_excess_KL_bits"]) / kl if kl > 0 else 0
    improved = run.supervised and current["A_accuracy"] > first["A_accuracy"]
    return {"prediction_loss_gap_closed": closure, "natural_KL_gap_closed": kl_closed,
            "initial_excess_prediction_loss": gap, "current_excess_prediction_loss": current_excess,
            "prediction_loss_criterion_available": gap > 0,
            "supervised_sums_improved": improved,
            "stop": gap > 0 and closure < .1 and kl_closed < .1 and not improved}


def futility_calibration():
    run = Run("noise", "raw_sampled", 0)
    first = {"train_parts": {"B": 1.2, "target_floor": 1., "excess_prediction_loss": .2},
             "audit": {"natural_excess_KL_bits": .2}, "A_accuracy": 0.}
    samples = [{"B": .5 + i / 100 + .2, "target_floor": .5 + i / 100,
                "excess_prediction_loss": .2} for i in range(100)]
    current = {"train_parts": r12._mean(samples), "audit": first["audit"], "A_accuracy": 0.}
    stable = futility(first, current, run)
    zero = copy.deepcopy(first)
    zero["train_parts"].update(B=1., excess_prediction_loss=0.)
    unavailable = futility(zero, current, run)
    learned = copy.deepcopy(current)
    learned["train_parts"]["excess_prediction_loss"] = .1
    progress = futility(first, learned, run)
    improved = copy.deepcopy(current)
    improved["A_accuracy"] = .5
    exception = futility(first, improved, Run("noise", "sums_sampled", 0))
    passed = (abs(stable["prediction_loss_gap_closed"]) < 1e-12 and stable["stop"] and
              not unavailable["stop"] and unavailable["prediction_loss_gap_closed"] is None and
              not progress["stop"] and not exception["stop"])
    if not passed:
        raise ValueError("per-batch excess futility calibration failed")
    return {"pass": passed, "sampled_floor_only_change": stable,
            "nonpositive_initial_excess": unavailable, "real_excess_reduction": progress,
            "supervised_sums_exception": exception}


def run_chunk(runs, device, output, bulk, *, steps=20000, smoke=False):
    registration()
    calibrated = json.loads((OUTPUT / "calibration.json").read_text())
    if calibrated["registration_sha256"] != r11.sha(OUTPUT / "registration.json"):
        raise ValueError("calibration binding differs")
    identity = hashlib.sha256("\n".join(r.name for r in runs).encode()).hexdigest()[:16]
    group = bulk / ("group_" + identity)
    group.mkdir(parents=True, exist_ok=True)
    engine = Engine(runs, device)
    tables = r11.BoardTables(device)
    streams = [CoverageStream(tables, r.seed, r.law, "uniform") for r in runs]
    candidates = [r12._candidate(r.law) for r in runs]
    curves, windows, stopped = [[] for _ in runs], [[] for _ in runs], [False] * len(runs)
    authority = {"registration_sha256": r11.sha(OUTPUT / "registration.json"),
                 "calibration_sha256": r11.sha(OUTPUT / "calibration.json"),
                 "runs": [r.name for r in runs], "smoke": smoke}
    paths = sorted(group.glob("checkpoint_step_*.pt"))
    start = 0
    if paths:
        saved = r12._bound_load(paths[-1])
        if not metadata_matches(saved["authority"], authority):
            raise ValueError("resume authority differs")
        engine.restore(saved["engine"])
        for s, state, c, seen in zip(streams, saved["streams"], candidates,
                                      saved["seen"], strict=True):
            s.restore(state)
            c.seen = seen
        start, curves, windows, stopped = (saved[k] for k in ("step", "curves", "windows", "stopped"))
    for run in runs:
        (output / run.name).mkdir(parents=True, exist_ok=True)
        settings_path = output / run.name / "settings.json"
        binding = {"authority": authority, "group": identity, "bulk": str(bulk), "run": run.__dict__}
        if settings_path.exists() and json.loads(settings_path.read_text()) != binding:
            raise ValueError("run directory execution group or settings differ")
        r11.write_json(settings_path, binding)
        r11._write_progress(output / run.name / "progress.log", f"START step={start} target={steps}")
    if not paths:
        old_states = [s.state() for s in streams]
        with torch.no_grad():
            preview = [[] for _ in runs]
            for _ in range(100):
                batches = [s.draw_batch() for s in streams]
                out = engine.forward(torch.stack([b.records for b in batches]),
                                     torch.stack([b.lengths for b in batches]))
                for i, (b, run) in enumerate(zip(batches, runs, strict=True)):
                    preview[i].append(loss_parts(tuple(v[i] for v in out), b, run)[1])
        windows = [[r12._mean(p)] for p in preview]
        for s, old in zip(streams, old_states, strict=True):
            s.restore(old)
    update_seconds, audit_seconds = 0., 0.
    for step in range(start, steps + 1):
        if step > start:
            if all(stopped):
                break
            before = time.monotonic()
            batches = [s.draw_batch() if not stopped[i] else None for i, s in enumerate(streams)]
            ref = next(b for b in batches if b is not None)
            details = engine.update([b or ref for b in batches], torch.tensor(
                [not s for s in stopped], device=device))
            update_seconds += time.monotonic() - before
            for i, b in enumerate(batches):
                if b is not None:
                    r11._observe(candidates[i], b)
                    windows[i] = (windows[i] + [details[i]])[-100:]
        schedule = {0, steps} if smoke else set(AUDITS)
        if step not in schedule or (paths and step == start):
            continue
        for i, run in enumerate(runs):
            if stopped[i]:
                continue
            folder = bulk / run.name
            folder.mkdir(parents=True, exist_ok=True)
            row = audit(engine.model_at(i), run, candidates[i], streams[i], device, step,
                        r12._mean(windows[i]), folder, smoke=smoke)
            if step == 5000:
                row["futility"] = futility(load_reference(curves[i][0]), row, run)
                stopped[i] = row["futility"]["stop"]
            path = folder / f"audit_step_{step:06d}.json"
            checkpoint = folder / f"checkpoint_step_{step:06d}.pt"
            if checkpoint.exists():
                previous = r12._bound_load(checkpoint)
                if not metadata_matches(previous["authority"], authority) or previous["futility_stop"] != stopped[i]:
                    raise ValueError("partly published run checkpoint differs")
                r12._check_numeric(previous["model"], engine.model_at(i, cpu=True).state_dict(), exact=True)
                old = json.loads(path.read_text())
                if old["stream_rolling_hash"] != row["stream_rolling_hash"]:
                    raise ValueError("partly published audit stream differs")
                row = old
            else:
                r11.write_json(path, row)
            curves[i].append({"step": step, "path": str(path), "sha256": r11.sha(path),
                              "train_parts": row["train_parts"], "B_pass": row["audit"]["B_pass"],
                              "natural_KL_bits": row["audit"]["natural_excess_KL_bits"]})
            audit_seconds += row["elapsed_seconds"]
            if not checkpoint.exists():
                r12._save(checkpoint, {"model": engine.model_at(i, cpu=True).state_dict(),
                    "authority": authority, "step": step, "futility_stop": stopped[i]})
        r12._save(group / f"checkpoint_step_{step:06d}.pt", {
            "authority": authority, "step": step, "engine": engine.state(),
            "streams": [s.state() for s in streams], "seen": [c.seen for c in candidates],
            "curves": curves, "windows": windows, "stopped": stopped})
        for i, run in enumerate(runs):
            if curves[i] and curves[i][-1]["step"] == step:
                r11._write_progress(output / run.name / "progress.log",
                    f"CHECKPOINT step={step} B={curves[i][-1]['train_parts']['B']:.8g} KL={curves[i][-1]['natural_KL_bits']:.8g}")
    notes = []
    for i, run in enumerate(runs):
        row = {"run": run.__dict__, "authority": authority, "curve": curves[i],
               "step": int(engine.optimizer.steps[i]), "resumed_from": start,
               "futility_stop": stopped[i], "bulk_directory": str(bulk / run.name),
               "performance": {"update_seconds": update_seconds, "audit_seconds": audit_seconds,
                    "updates_this_execution": max(0, int(engine.optimizer.steps[i]) - start),
                    "width": len(runs), "CPU_threads": torch.get_num_threads(),
                    "RSS_MiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
                    "GPU_peak_MiB": torch.cuda.max_memory_allocated() / 2**20 if device.type == "cuda" else None}}
        r11.write_json(output / run.name / "summary.json", row)
        r11._write_progress(output / run.name / "progress.log",
                           f"{'FUTILITY_STOP' if stopped[i] else 'COMPLETE'} step={row['step']}")
        notes.append(row)
    return notes


def load_reference(row):
    path = public_path(row["path"])
    if r11.sha(path) != row["sha256"]:
        raise ValueError("detailed artifact digest differs")
    return json.loads(path.read_text())


def geometry_audit(model, device, bulk, step):
    from recombination_promotion.oldgame_ext.mechanism_geometry import (
        discrimination_decision, score_pair_discrimination,
    )
    geometry_amendment()
    pairs = json.loads((OUTPUT / "geometry_pairs.json").read_text())
    if r11.sha(OUTPUT / "geometry_pairs.json") != registration()["geometry_pairs_sha256"]:
        raise ValueError("geometry pair authority differs")
    boards = r11.enumerate_boards()
    split = json.loads((r11.r8.OUTPUT / "probe_split.json").read_text())
    arrays, ids_by_split = {}, {}
    with torch.no_grad():
        for name, key in (("train", "train_board_ids"), ("heldout", "heldout_board_ids")):
            ids = np.asarray(split[key])
            ids_by_split[name] = ids
            arrays[name] = []
            for rendering in range(4):
                records = r11._census_records(boards, ids, render_offset=rendering)
                parts = [model.round_interfaces(torch.from_numpy(records[a:a + 256]).to(device))[2]
                         .detach().cpu() for a in range(0, len(records), 256)]
                arrays[name].append(torch.cat(parts))
    mean = arrays["train"][0].mean(0)
    scale = arrays["train"][0].std(0, unbiased=False)
    scale = torch.where(scale == 0, 1, scale)
    features = {key: [(x - mean) / scale for x in vals] for key, vals in arrays.items()}
    path = bulk / f"geometry_step_{step:06d}.npz"
    np.savez_compressed(path, **{f"{key}_{r}": x.numpy() for key, vals in features.items()
                                for r, x in enumerate(vals)}, mean=mean.numpy(), scale=scale.numpy())
    rows = []
    train_ids = {int(v): i for i, v in enumerate(ids_by_split["train"])}
    held_ids = {int(v): i for i, v in enumerate(ids_by_split["heldout"])}
    for a in range(37):
        for b in range(a + 1, 37):
            if b - a != 1 and b - a < 4:
                continue
            train = [p for p in pairs["train"]["pairs"] if p[2:] == [a, b]]
            held = [p for p in pairs["heldout"]["pairs"] if p[2:] == [a, b]]
            row = {"sums": [a, b], "train_pairs": len(train), "heldout_pairs": len(held)}
            if not train or not held:
                row["status"] = "MISSING_SUPPORT"
                rows.append(row)
                continue
            def panel(ps, lookup, key):
                indices = [lookup[p[j]] for p in ps for j in (0, 1)]
                return features[key][0][indices], torch.tensor([0, 1] * len(ps))
            x, y = panel(train, train_ids, "train")
            z, w = panel(held, held_ids, "heldout")
            train_identities = [p[j] for p in train for j in (0, 1)]
            heldout_identities = [p[j] for p in held for j in (0, 1)]
            decoded = score_pair_discrimination(x, y, z, w, train_ids=train_identities,
                heldout_ids=heldout_identities, seed=130014)
            permutation = torch.tensor(pairs["train"]["reader_label_permutations"][f"{a}_{b}"])
            floor = score_pair_discrimination(x, y[permutation], z, w,
                train_ids=train_identities, heldout_ids=heldout_identities, seed=130014)
            distances = (z[::2] - z[1::2]).norm(dim=-1) / math.sqrt(z.shape[-1])
            indices = sorted({held_ids[p[j]] for p in held for j in (0, 1)})
            rerender = torch.cat([(features["heldout"][k][indices] -
                                   features["heldout"][0][indices]).norm(dim=-1) /
                                  math.sqrt(z.shape[-1]) for k in (1, 2, 3)])
            row.update({"status": "MEASURED", "reader": decoded, "label_permutation_floor": floor,
                        "discrimination": discrimination_decision(decoded, [floor]),
                        "distance_mean": float(distances.mean()),
                        "distance_quantiles": torch.quantile(distances, torch.tensor([0., .5, 1.])).tolist(),
                        "rerender_distance_mean": float(rerender.mean())})
            rows.append(row)
    return {"pairs_sha256": r11.sha(OUTPUT / "geometry_pairs.json"),
            "analysis_amendment_sha256": r11.sha(OUTPUT / "geometry_amendment.json"),
            "features": {"path": str(path), "sha256": r11.sha(path)}, "rows": rows,
            "scope": "descriptive geometry; proximity alone is not causal evidence"}


def erosion_step(model, batch, sums_optimizer, other_optimizer, *, blocked=False,
                 sgd=False, sgd_rate=None):
    sums = {n: p for n, p in model.named_parameters() if n.startswith("memory.")}
    before = {n: p.detach().clone() for n, p in sums.items()}
    model.zero_grad(set_to_none=True)
    _, logits = model(batch.records, batch.lengths)
    loss = torch.nn.functional.cross_entropy(logits[batch.active], batch.targets[batch.active])
    if not torch.isfinite(loss):
        raise ValueError("erosion loss is non-finite")
    loss.backward()
    gradients = {n: (torch.zeros_like(p) if p.grad is None else p.grad.detach().clone())
                 for n, p in sums.items()}
    if blocked:
        for p in sums.values():
            p.grad = torch.zeros_like(p)
        gradients = {n: torch.zeros_like(p) for n, p in sums.items()}
    if sgd:
        if sgd_rate is None:
            sgd_rate = matched_sgd_rate(list(gradients.values()))
        with torch.no_grad():
            for n, p in sums.items():
                p.mul_(.99997).add_(gradients[n], alpha=-sgd_rate)
        decay_factor = .99997
    else:
        sums_optimizer.step()
        group = sums_optimizer.param_groups[0]
        decay_factor = 1 - group["lr"] * group["weight_decay"]
    other_optimizer.step()
    tensors = {}
    for n, p in sums.items():
        decay = before[n] * (decay_factor - 1)
        actual = p.detach() - before[n]
        gradient_move = actual - decay
        tensors[n] = {"gradient": gradient_statistics(gradients[n]),
                      "actual_displacement": float(actual.norm()),
                      "gradient_displacement": float(gradient_move.norm()),
                      "decay_displacement": float(decay.norm())}
    return {"B": float(loss.detach()), "tensors": tensors,
            "SGD_rate": sgd_rate, "decay_multiplier": decay_factor}, before


def erosion(run, device, output, bulk, *, steps=200):
    registration()
    folder = bulk / run.name
    folder.mkdir(parents=True, exist_ok=True)
    directory = output / run.name
    directory.mkdir(parents=True, exist_ok=True)
    model = new_model(run.seed, True, repo_root=ROOT).to(device)
    tables = r11.BoardTables(device)
    stream = DeviceStream(tables, run.seed, run.law, "uniform")
    sums = {n: p for n, p in model.named_parameters() if n.startswith("memory.")}
    other = [p for n, p in model.named_parameters() if not n.startswith("memory.")]
    sums_optimizer = torch.optim.AdamW(sums.values(), lr=.0003 if run.condition == "reduced"
                                      else .003, weight_decay=.01)
    other_optimizer = torch.optim.AdamW(other, lr=.003, weight_decay=.01)
    initial = {n: p.detach().clone() for n, p in sums.items()}
    with torch.no_grad():
        first = margin_counts(histories_logits(model.memory))
    if first["correct"] != 1555:
        raise ValueError("erosion update zero is not exact")
    authority = {"registration_sha256": r11.sha(OUTPUT / "registration.json"), "run": run.__dict__}
    paths = sorted(folder.glob("checkpoint_step_*.pt"))
    rows, rate, start = [], None, 0
    paths_by_tensor = dict.fromkeys(sums, 0.)
    seen_flips = set()
    refusal = None
    if paths:
        saved = r12._bound_load(paths[-1])
        if not metadata_matches(saved["authority"], authority):
            raise ValueError("erosion resume authority differs")
        model.load_state_dict(saved["model"])
        sums_optimizer.load_state_dict(saved["sums_optimizer"])
        other_optimizer.load_state_dict(saved["other_optimizer"])
        stream.restore(saved["stream"])
        rows, rate, start = saved["rows"], saved["rate"], saved["step"]
        paths_by_tensor, seen_flips = saved["paths_by_tensor"], set(saved["seen_flips"])
    else:
        rows.append({"step": 0, "local": first, "cumulative_path": 0.})
    started = time.monotonic()
    for step in range(start + 1, steps + 1):
        batch = stream.draw_batch()
        before_margin = rows[-1]["local"]["margins"]
        try:
            record, _ = erosion_step(model, batch, sums_optimizer, other_optimizer,
                blocked=run.condition == "blocked", sgd=run.condition == "sgd", sgd_rate=rate)
            if any(not torch.isfinite(p).all() for p in model.parameters()):
                raise ValueError("non-finite erosion parameters after update")
        except ValueError as error:
            refusal = {"update": step, "reason": str(error), "status": "INCONCLUSIVE_NONFINITE"}
            r11.write_json(folder / "refusal.json", refusal)
            break
        rate = record["SGD_rate"]
        with torch.no_grad():
            local = margin_counts(histories_logits(model.memory))
            logits = model.round_interfaces(batch.records[batch.active])[0]
            target = torch.searchsorted(logits.new_tensor(VALUES), batch.sums[batch.active])
            correct = logits.argmax(-1) == target
        true_indices = [VALUES.index(game.sigma(h)) for h in game.histories()]
        flips = [i for i, truth in enumerate(true_indices)
                 if rows[-1]["local"]["predictions"][i] == truth and local["predictions"][i] != truth
                 and i not in seen_flips]
        seen_flips.update(flips)
        for n, p in sums.items():
            paths_by_tensor[n] += record["tensors"][n]["actual_displacement"]
            record["tensors"][n]["cumulative_path"] = paths_by_tensor[n]
            record["tensors"][n]["displacement_from_initialization"] = float((p - initial[n]).norm())
        previous_path = rows[-1]["cumulative_path"]
        path_increment = math.sqrt(sum(v["actual_displacement"] ** 2
                                      for v in record["tensors"].values()))
        rows.append({"step": step, **record, "local": local,
                     "completed_boards": {"correct_vectors": int(correct.all(-1).sum()),
                                           "boards": len(correct), "correct_components": int(correct.sum()),
                                           "components": correct.numel()},
                     "first_flips": [{"history": list(game.histories()[i]), "history_index": i,
                                       "previous_margin": before_margin[i], "margin": local["margins"][i],
                                       "preceding_update": step} for i in flips],
                     "cumulative_path": previous_path + path_increment,
                     "displacement_from_initialization": math.sqrt(sum(
                         v["displacement_from_initialization"] ** 2 for v in record["tensors"].values())),
                     "stream_hash": stream.rolling.hex()})
        # Each completed observation survives an interruption before the next
        # resumable checkpoint. Replaying that interval must give the same row.
        observation = folder / f"erosion_update_{step:06d}.json"
        if observation.exists() and json.loads(observation.read_text()) != rows[-1]:
            raise ValueError("erosion observation replay differs")
        r11.write_json(observation, rows[-1])
        if step % 50 == 0 or step == steps:
            r12._save(folder / f"checkpoint_step_{step:06d}.pt", {
                "authority": authority, "step": step, "model": model.state_dict(),
                "sums_optimizer": sums_optimizer.state_dict(), "other_optimizer": other_optimizer.state_dict(),
                "stream": stream.state(), "rows": rows, "rate": rate,
                "paths_by_tensor": paths_by_tensor, "seen_flips": sorted(seen_flips)})
        r11._write_progress(directory / "progress.log",
                           f"CHECKPOINT step={step} sum={local['correct']}/1555 path={rows[-1]['cumulative_path']:.9g}")
    path = folder / "erosion_records.json"
    r11.write_json(path, rows)
    note = {"run": run.__dict__, "authority": authority, "step": rows[-1]["step"],
            "requested_steps": steps, "refusal": refusal,
            "resumed_from": start, "records": {"path": str(path), "sha256": r11.sha(path)},
            "final_correct": rows[-1]["local"]["correct"], "SGD_rate": rate,
            "elapsed_seconds": time.monotonic() - started,
            "movement_comparison_scope": "observed common range only; no extrapolation"}
    r11.write_json(directory / "summary.json", note)
    return note


def verification(device, bulk, *, trace=False):
    """Actual r13 losses/streams, width three and direct width one, restore at 3."""
    registration()
    tables = r11.BoardTables(device)
    results = {}
    for condition in ("sums_probability", "live"):
        runs = [Run("noise" if condition.startswith("sums") else "access", condition, s)
                for s in range(3 if condition.startswith("sums") else 1)]
        grouped = Engine(runs, device)
        singles = [Engine([r], device) for r in runs]
        restored = Engine(runs, device)
        streams = [CoverageStream(tables, r.seed, r.law, "uniform") for r in runs]
        second = [CoverageStream(tables, r.seed, r.law, "uniform") for r in runs]
        third = [CoverageStream(tables, r.seed, r.law, "uniform") for r in runs]
        ordinary = [make_model(r, device) for r in runs]
        optimizers = [torch.optim.AdamW([p for p in m.parameters() if p.requires_grad],
                                       lr=.003, weight_decay=.01) for m in ordinary]
        maximum = 0.
        traces = []
        for step in range(1, 9):
            batches = [s.draw_batch() for s in streams]
            before = [tensor_hash({k: v[i] for k, v in grouped.parameters.items()})
                      for i in range(len(runs))]
            detail = grouped.update(batches, torch.ones(len(runs), dtype=torch.bool, device=device))
            for i, (single, stream, model, optimizer) in enumerate(zip(
                    singles, second, ordinary, optimizers, strict=True)):
                b = stream.draw_batch()
                if not torch.equal(b.records, batches[i].records) or not torch.equal(b.targets, batches[i].targets):
                    raise ValueError("verification pairing differs")
                single.update([b], torch.ones(1, dtype=torch.bool, device=device))
                optimizer.zero_grad(set_to_none=True)
                loss_parts(model(b.records, b.lengths, return_all=True), b, runs[i])[0].backward()
                optimizer.step()
                checks = r11._compare_training(r11._engine_run_state(grouped, i),
                    r11._ordinary_run_state(model, optimizer), streams[i], stream,
                    None, None, None, None)
                # Explicitly compare both optimizer moments and parameters; discrete streams exact.
                for k, v in grouped.parameters.items():
                    d = float((v[i] - single.parameters[k][0]).detach().abs().max())
                    maximum = max(maximum, d)
                    if not torch.allclose(v[i], single.parameters[k][0], atol=3e-5, rtol=3e-5):
                        raise ValueError(f"batch/direct parameter difference: {k}")
                if not checks["pass"]:
                    failure = {"pass": False, "condition": condition, "step": step,
                        "checks": checks, "device": device.type,
                        "registration_sha256": r11.sha(OUTPUT / "registration.json"),
                        "source_sha256": identities(), "trace": traces}
                    r11.write_json(bulk / f"verification_{device.type}.json", failure)
                    raise ValueError("ordinary AdamW verification failed; report persisted")
            if step == 3:
                # Serialize, reload and restore: not just an in-memory state copy.
                path = bulk / f"verify_{condition}_step3.pt"
                path.parent.mkdir(parents=True, exist_ok=True)
                torch.save({"engine": grouped.state(), "streams": [s.state() for s in streams]}, path)
                saved = torch.load(path, map_location="cpu", weights_only=False)
                restored.restore(saved["engine"])
                for s, state in zip(third, saved["streams"], strict=True):
                    s.restore(state)
            if step > 3:
                restored.update([s.draw_batch() for s in third],
                                torch.ones(len(runs), dtype=torch.bool, device=device))
                if not r11._equal_discrete(grouped.state(), restored.state()):
                    raise ValueError("nonzero restoration is not exact")
                for s, t in zip(streams, third, strict=True):
                    r12._check_stream(s, t)
            if trace:
                traces.append({"step": step, "before_parameter_sha256": before,
                               "loss_parts": detail, "maximum_parameter_difference": maximum,
                               "gradients": {k: [float(g.norm()) for g in v.grad]
                                             for k, v in grouped.parameters.items() if v.grad is not None}})
                r11.write_json(bulk / f"verification_trace_{device.type}_{condition}.json", traces)
        results[condition] = {"pass": True, "width": len(runs), "restore_update": 3,
                              "restoration_exact": True, "maximum_parameter_difference": maximum,
                              "trace": traces}
    report = {"pass": True, "device": device.type, "comparisons": results,
              "registration_sha256": r11.sha(OUTPUT / "registration.json"),
              "source_sha256": identities(), "tolerances": r11.EQUIVALENCE_TOLERANCE}
    r11.write_json(bulk / f"verification_{device.type}.json", report)
    return report


def aggregate(output, bulk):
    from scripts.oldgame_mechanism_report import aggregate as aggregate_saved

    # Completed training authority stays fixed; reporting has separate bindings.
    report = aggregate_saved(output)
    return {"experiments": {k: len(v) for k, v in report["experiments"].items()},
            "details": report["details"]}


def comparison_readings(experiments, calibrated):
    """Keep endpoints, controls and reduced evidence distinct; never select a checkpoint."""
    result = {name: {"registered_reading": "see verbatim registration",
                     "selected_reading": "NO_STUDY_ENDPOINTS", "seeds": []}
              for name in experiments}
    for name in ("noise", "access", "encoding"):
        for seed in range(3):
            rows = {row["run"]["condition"]: row for row in experiments[name]
                    if row["run"]["seed"] == seed and row["run"]["law"] == "original"
                    and row.get("endpoint_status") not in ("REDUCED_SMOKE", "FUTILITY_STOP")}
            def kl(condition):
                return rows[condition]["endpoint_prediction"]["natural_excess_KL_bits"]
            reading = None
            measurements = {}
            if name == "noise" and set(NOISE) <= rows.keys():
                changes = {version: kl(version + "_sampled") - kl(version + "_probability")
                           for version in ("raw", "sums")}
                residual = kl("sums_probability") - kl("raw_probability")
                measurements = {"sampled_minus_probability_KL": changes,
                                "sums_minus_raw_probability_KL": residual}
                reading = ("Probability targets improve both versions: supports a target-noise contribution."
                           if all(x > 0 for x in changes.values()) else
                           "Probability targets do not improve both versions: little support for noise as a sufficient explanation.")
                if residual > 0:
                    reading += " A sums-loss disadvantage persists under probability targets."
            elif name == "access" and set(("disconnected", "frozen", "live", "exact")) <= rows.keys():
                measurements = {condition: kl(condition) for condition in rows}
                if not rows["exact"]["endpoint_prediction"]["B_pass"]:
                    reading = "Exact sums also fail: downstream recurrence/readout remains a limitation."
                elif kl("frozen") < kl("disconnected"):
                    reading = "Frozen connection improves prediction: supports an access contribution."
                    if kl("live") > kl("frozen"):
                        reading += " Frozen outperforms live; inspect supplier deterioration and gradient conflict for interference evidence."
                elif kl("live") < kl("disconnected"):
                    reading = "Trainable connection improves prediction; access matters under this condition."
                else:
                    reading = "Neither connection improves, but exact sums pass: supplier error remains a candidate."
            elif name == "encoding" and "numerical" in rows:
                onehot = next((r for r in experiments["access"] if r["run"]["condition"] == "exact"
                    and r["run"]["seed"] == seed and r.get("endpoint_status") == "PASS"), None)
                reading = ("Numerical encoding passes: weakens continuous encoding as a sufficient explanation."
                    if rows["numerical"]["endpoint_prediction"]["B_pass"] else
                    "One-hot passes but numerical fails: supports encoding sensitivity, not a precision ceiling."
                    if onehot else "Both encodings incomplete: no encoding-specific explanation established.")
                if not calibrated["geometry"]:
                    reading += " Geometry conclusions blocked by failed calibration."
            if reading is not None:
                result[name]["seeds"].append({"seed": seed, "selected_reading": reading,
                                               "continuous_measurements": measurements})
                result[name]["selected_reading"] = "PER_SEED_DESCRIPTIVE_COMPARISON"
    erosion_rows = experiments["erosion"]
    if erosion_rows:
        result["erosion"]["selected_reading"] = "PER_UPDATE_AND_OBSERVED_MOVEMENT_CURVES; no optimizer attribution from update counts alone"
        for seed in range(3):
            rows = {r["run"]["condition"]: r for r in erosion_rows if r["run"]["seed"] == seed}
            if set(("adam", "reduced", "sgd", "blocked")) <= rows.keys():
                lo = max(r["trajectory"][0]["cumulative_path"] for r in rows.values())
                hi = min(r["trajectory"][-1]["cumulative_path"] for r in rows.values())
                result["erosion"]["seeds"].append({"seed": seed, "common_movement_range": [lo, hi],
                    "endpoint_correct_counts": {c: r["trajectory"][-1]["correct"] for c, r in rows.items()},
                    "interpretation": "Blocked-gradient erosion measures decay or a defect; other curves require comparison on their common observed range."})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("register", "calibrate", "geometry-register",
                        "geometry-calibrate", "run", "verify-gpu", "aggregate"), required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-root", type=Path, default=OUTPUT)
    parser.add_argument("--bulk-root", type=Path, default=BULK)
    parser.add_argument("--experiment", choices=("all", "full", "erosion", "noise", "access", "encoding"), default="all")
    parser.add_argument("--run-name", action="append")
    parser.add_argument("--process", type=int, choices=(0, 1, 2))
    parser.add_argument("--steps", type=int)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--trace", action="store_true")
    args = parser.parse_args()
    device = r11.configure(args.device)
    if args.stage == "register":
        result = register(device)
        geometry_amendment(rebuild=True)
        print(json.dumps({"registered_runs": len(result["runs"]), "registration_sha256": r11.sha(OUTPUT / "registration.json")}))
    elif args.stage == "calibrate":
        print(json.dumps({"training": calibration(device, args.bulk_root),
                          "geometry_analysis": geometry_calibration()}, indent=2))
    elif args.stage == "geometry-register":
        print(json.dumps(geometry_amendment(rebuild=True), indent=2))
    elif args.stage == "geometry-calibrate":
        print(json.dumps(geometry_calibration(), indent=2))
    elif args.stage == "verify-gpu":
        print(json.dumps(verification(device, args.bulk_root, trace=args.trace), indent=2))
    elif args.stage == "aggregate":
        print(json.dumps(aggregate(args.output_root, args.bulk_root), indent=2))
    else:
        runs = [r for r in all_runs() if (args.experiment == "all" or r.experiment == args.experiment
                or (args.experiment == "full" and r.experiment != "erosion"))
                and (args.run_name is None or r.name in args.run_name)]
        if args.run_name and set(args.run_name) - {r.name for r in runs}:
            raise ValueError("unknown or conflicting run names")
        if args.process is not None:
            # Three processes: each condition group assigned to one process. Width
            # three keeps seeds together for noise; all others direct width one.
            keys = list(dict.fromkeys((r.experiment, r.condition, r.law) for r in all_runs()))
            runs = [r for r in runs if keys.index((r.experiment, r.condition, r.law)) % 3 == args.process]
        if not runs:
            raise ValueError("empty run selection")
        if not args.smoke and args.steps is not None:
            raise ValueError("production endpoints fixed; --steps is smoke only")
        for experiment, condition, law in dict.fromkeys((r.experiment, r.condition, r.law) for r in runs):
            subset = [r for r in runs if (r.experiment, r.condition, r.law) == (experiment, condition, law)]
            if experiment == "erosion":
                for run in subset:
                    print(json.dumps(erosion(run, device, args.output_root, args.bulk_root,
                                            steps=min(args.steps or 200, 200))))
            else:
                width = 3 if experiment == "noise" else 1
                for at in range(0, len(subset), width):
                    print(json.dumps(run_chunk(subset[at:at + width], device, args.output_root,
                        args.bulk_root, steps=args.steps or 20000, smoke=args.smoke)))


if __name__ == "__main__":
    main()
