"""Device execution, independent optimizers and durable r10 continuation."""

from __future__ import annotations

import hashlib
import json
import resource
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from recombination_promotion.public_paths import public_path, metadata_matches

import numpy as np
import torch
from torch.func import functional_call, stack_module_state, vmap

from recombination_promotion.oldgame_ext.multiround_allslots import (
    CoverageSampler, DeviceCoverageStream, ROW_FLOAT, VALUES36,
)
from scripts import oldgame_multiround_jagged as r11

BULK = public_path("bulk/study_r10_allslots_bulk")


@dataclass(frozen=True)
class Run:
    arm: str
    law: str
    seed: int

    @property
    def name(self):
        return f"{self.arm}_{self.law}_seed{self.seed}"


def all_runs():
    return [Run(arm, law, seed) for arm in ("free", "free_a", "a_forced")
            for law in ("original", "equal") for seed in (0, 1, 2)]


def publish(path, value):
    """Publish a bound payload; an interrupted two-file publication is recoverable."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError("r10 checkpoint destination is nonempty")
    pending = path.with_suffix(".pending")
    digest = path.with_suffix(".pending.sha256")
    torch.save(value, pending)
    digest.write_text(r11.sha(pending) + "\n")
    pending.rename(path)
    digest.rename(path.with_suffix(".sha256"))


def bound_load(path):
    path = Path(path)
    digest = path.with_suffix(".sha256")
    pending_digest = path.with_suffix(".pending.sha256")
    if not digest.exists() and pending_digest.exists():
        if pending_digest.read_text().strip() != r11.sha(path):
            raise ValueError("r10 pending checkpoint digest differs")
        pending_digest.rename(digest)
    if not digest.exists() or digest.read_text().strip() != r11.sha(path):
        raise ValueError("r10 checkpoint digest differs")
    return torch.load(path, map_location="cpu", weights_only=False)


def recover(directory):
    for digest in directory.glob("checkpoint_step_*.pending.sha256"):
        path = digest.with_suffix("").with_suffix(".pt")
        pending = path.with_suffix(".pending")
        if not path.exists() and pending.exists():
            if digest.read_text().strip() != r11.sha(pending):
                raise ValueError("r10 pending checkpoint digest differs")
            pending.rename(path)
        if path.exists():
            bound_load(path)


def grouped_loss(output, batches, runs):
    logits, a_logits = output
    result, details = [], []
    for index, (batch, run) in enumerate(zip(batches, runs, strict=True)):
        b = torch.nn.functional.cross_entropy(logits[index].reshape(-1, 3), batch.targets.flatten())
        a = b.new_zeros(())
        if run.arm == "free_a":
            values = torch.tensor(VALUES36, device=b.device)
            targets = torch.searchsorted(values, batch.sums.contiguous())
            a = torch.nn.functional.cross_entropy(a_logits[index].reshape(-1, 36), targets.flatten())
        result.append(a+b)
        details.append({"B": float(b.detach()), "A": float(a.detach())})
    return torch.stack(result), details


class Engine(r11.GroupEngine):
    def __init__(self, study, runs, device):
        if len({r.arm == "a_forced" for r in runs}) != 1:
            raise ValueError("r10 execution batch mixes hard and masked A")
        if runs[0].arm == "a_forced" and len(runs) != 1:
            raise ValueError("r10 hard A requires direct width one")
        self.study, self.runs, self.device = study, runs, device
        self.models = [study._new_model(r.arm, r.seed).to(device) for r in runs]
        self.parameters, self.buffers = stack_module_state(self.models)
        self.optimizer = r11.StackedAdamW(self.parameters, len(runs))

    def forward(self, records, queries, lengths):
        template = self.models[0]
        if len(self.runs) == 1:
            output = functional_call(template, (
                {k: v[0] for k, v in self.parameters.items()},
                {k: v[0] for k, v in self.buffers.items()}),
                (records[0], queries[0], lengths[0]))
            return tuple(v[None] for v in output)
        return vmap(lambda p, b, x, q, n: functional_call(template, (p, b), (x, q, n)),
                    in_dims=(0, 0, 0, 0, 0))(
            self.parameters, self.buffers, records, queries, lengths)

    def update(self, batches, active):
        self.optimizer.zero_grad()
        output = self.forward(torch.stack([b.records for b in batches]),
                              torch.stack([b.queries for b in batches]),
                              torch.stack([b.lengths for b in batches]))
        loss, details = grouped_loss(output, batches, self.runs)
        if not torch.isfinite(loss).all():
            raise ValueError("r10 non-finite training loss")
        (loss*active).sum().backward()
        if any(v.grad is not None and not torch.isfinite(v.grad).all() for v in self.parameters.values()):
            raise ValueError("r10 non-finite gradient")
        used = torch.tensor([r.arm == "free_a" for r in self.runs], device=self.device)
        self.optimizer.step(active, {k: used for k in self.parameters if k.startswith("raw_sum_head.")})
        return details

    def model_at(self, index, *, cpu=False):
        model = self.study._new_model(self.runs[index].arm, self.runs[index].seed)
        model.load_state_dict({k: v[index].detach() for k, v in self.parameters.items()}, strict=True)
        return model.to("cpu" if cpu else self.device).eval()


def make_streams(study, runs, device):
    boards = study.enumerate_boards()
    tables = r11.BoardTables(device, boards)
    split = json.loads((study.OUTPUT / "board_split.json").read_text())
    sampler = CoverageSampler(boards, np.asarray(split["train_board_ids"]))
    return [DeviceCoverageStream(tables, sampler, r.seed, equal=r.law == "equal") for r in runs]


def stopped_on_restore(saved):
    return [bool(stop or (curve and curve[-1].get("record", curve[-1]).get("futility", {}).get("stop", False)))
            for stop, curve in zip(saved["stopped"], saved["curves"], strict=True)]


def futility(first, current):
    gap = max(first["loss_parts"]["B"] - first["oracle_B_loss_floor_nats"], 0.)
    closed = (first["loss_parts"]["B"]-current["loss_parts"]["B"])/gap if gap else 0.
    initial = first["audit"]["B"]["natural"]["KL_bits"]
    kl_closed = (initial-current["audit"]["B"]["natural"]["KL_bits"])/initial if initial else 0.
    return {"loss_gap_closed": closed, "natural_KL_gap_closed": kl_closed,
            "stop": closed < .1 and kl_closed < .1}


def run_chunk(study, runs, device, output, bulk, *, steps=20000, smoke=False):
    study.registration()
    if not smoke:
        calibration = json.loads((study.OUTPUT / "calibration.json").read_text())
        if not all(calibration["checks"].values()):
            raise ValueError("r10 calibration failed; production execution refused")
        if calibration["registration_sha256"] != study.sha(study.OUTPUT / "registration.json"):
            raise ValueError("r10 calibration registration binding differs")
    authority = {"registration_sha256": study.sha(study.OUTPUT / "registration.json"),
                 "calibration_sha256": study.sha(study.OUTPUT / "calibration.json"),
                 "runs": [r.name for r in runs], "device": device.type, "precision": "float32", "smoke": smoke}
    group_id = hashlib.sha256("\n".join(authority["runs"]).encode()).hexdigest()[:16]
    group = bulk / ("group_" + group_id)
    group.mkdir(parents=True, exist_ok=True)
    recover(group)
    engine, streams = Engine(study, runs, device), make_streams(study, runs, device)
    curves, stopped, start = [[] for _ in runs], [False]*len(runs), 0
    windows = [[] for _ in runs]
    paths = sorted(group.glob("checkpoint_step_*.pt"))
    if paths:
        saved = bound_load(paths[-1])
        if not metadata_matches(saved["authority"], authority):
            raise ValueError("r10 checkpoint authority differs")
        engine.restore(saved["engine"])
        for stream, state in zip(streams, saved["streams"], strict=True):
            stream.restore(state)
        curves, stopped, start = saved["curves"], stopped_on_restore(saved), saved["step"]
        windows = saved["windows"]
    for run in runs:
        directory = output / run.name
        directory.mkdir(parents=True, exist_ok=True)
        recover(bulk / run.name)
        settings_path = directory / "settings.json"
        binding = {"authority": authority, "bulk": str(bulk), "run": run.__dict__}
        if settings_path.exists() and json.loads(settings_path.read_text()) != binding:
            raise ValueError("r10 existing run settings differ")
        if not settings_path.exists():
            study.write_json(settings_path, binding)
        r11._write_progress(directory / "progress.log", f"START step={start} target={steps}")
    boards = study.enumerate_boards()
    seconds, audit_seconds = 0., 0.
    schedule = {0, steps} if smoke else set(study.AUDITS)
    for step in range(start, steps+1):
        if all(stopped):
            break
        if step > start:
            started = time.monotonic()
            states = [s.state() if stopped[i] else None for i,s in enumerate(streams)]
            batches = [s.draw() for s in streams]
            for stream,state in zip(streams,states,strict=True):
                if state is not None:
                    stream.restore(state)
            details = engine.update(batches, torch.tensor([not s for s in stopped], device=device))
            for i, detail in enumerate(details):
                windows[i].append(detail); windows[i] = windows[i][-100:]
            if device.type == "cuda":
                torch.cuda.synchronize()
            seconds += time.monotonic()-started
        elif not paths:
            states = [s.state() for s in streams]
            batches = [s.draw() for s in streams]
            with torch.no_grad():
                _, details = grouped_loss(engine.forward(torch.stack([b.records for b in batches]),
                    torch.stack([b.queries for b in batches]), torch.stack([b.lengths for b in batches])), batches, runs)
            for stream, state in zip(streams, states, strict=True):
                stream.restore(state)
            windows = [[d] for d in details]
        if step not in schedule or (step == start and paths):
            continue
        for i, run in enumerate(runs):
            if stopped[i]:
                continue
            model = engine.model_at(i)
            audit = study._audit(model, run.law, boards, smoke=smoke)
            audit_seconds += audit["elapsed_seconds"]
            detail = {key: float(np.mean([d[key] for d in windows[i]])) for key in ("A", "B")}
            truth = ROW_FLOAT if run.law == "original" else np.ones((36, 3))/3
            row = {"step": step, "loss_parts": detail, "audit": audit,
                   "oracle_B_loss_floor_nats": (curves[i][0]["record"]["oracle_B_loss_floor_nats"]
                        if curves[i] else float(-np.sum(truth[np.searchsorted(VALUES36,
                            batches[i].remembered.gather(2, batches[i].queries[..., None])[..., 0].cpu().numpy())]
                            * np.log(truth[np.searchsorted(VALUES36,
                            batches[i].remembered.gather(2, batches[i].queries[..., None])[..., 0].cpu().numpy())]), axis=-1).mean())),
                   "coverage": {key: getattr(streams[i], key).cpu().tolist() for key in (
                       "current", "current_by_Q", "current_queried", "remembered_queried")},
                   "precision": "float32", "reduced_smoke": smoke}
            if step == 5000:
                row["futility"] = futility(curves[i][0]["record"], row)
                stopped[i] = row["futility"]["stop"]
            directory = bulk / run.name
            directory.mkdir(parents=True, exist_ok=True)
            exposures = directory / f"exposure_step_{step:06d}.npz"
            np.savez_compressed(exposures, **{key: getattr(streams[i], key).cpu().numpy() for key in (
                "current", "current_by_Q", "current_queried", "remembered_queried",
                "board_counts", "rendering_counts", "placement_counts")})
            row["exposure"] = {"path": str(exposures), "sha256": study.sha(exposures)}
            path = directory / f"audit_step_{step:06d}.json"
            study.write_json(path, row)
            curves[i].append({"step": step, "path": str(path), "sha256": study.sha(path), "record": row})
            r11._write_progress(output / run.name / "progress.log",
                f"CHECKPOINT step={step} B_loss={detail['B']} KL={audit['B']['natural']['KL_bits']}")
        publish(group / f"checkpoint_step_{step:06d}.pt", {
            "authority": authority, "step": step, "engine": engine.state(),
            "streams": [s.state() for s in streams], "curves": curves, "stopped": stopped,
            "windows": windows})
        group_path = group / f"checkpoint_step_{step:06d}.pt"
        for i, run in enumerate(runs):
            if curves[i][-1]["step"] == step:
                publish(bulk / run.name / f"checkpoint_step_{step:06d}.pt", {
                    "model": {key: value[i].detach().cpu() for key, value in engine.parameters.items()},
                    "arm": run.arm, "law": run.law, "seed": run.seed, "step": step,
                    "group_checkpoint": str(group_path), "group_sha256": study.sha(group_path),
                    "authority": authority})
    summaries = []
    for i, run in enumerate(runs):
        curve = [{k: v for k, v in row.items() if k != "record"} for row in curves[i]]
        summary = {"arm": run.arm, "law": run.law, "seed": run.seed, "last_step": curve[-1]["step"],
                   "smoke": smoke, "futility_stop": stopped[i], "authority": authority,
                   "curve": curve, "resumed_from": start, "width": len(runs),
                   "training_seconds": seconds, "audit_seconds": audit_seconds,
                   "updates_per_second": (max(curve[-1]["step"]-start, 0)/seconds if seconds else 0),
                   "worker_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   "GPU_peak_bytes": torch.cuda.max_memory_allocated() if device.type == "cuda" else None,
                   "observed_current_slot_value_counts": streams[i].current.cpu().tolist(),
                   "observed_current_by_Q_counts": streams[i].current_by_Q.cpu().tolist(),
                   "observed_current_query_value_counts": streams[i].current_queried.cpu().tolist(),
                   "observed_remembered_query_value_counts": streams[i].remembered_queried.cpu().tolist()}
        study.write_json(output / run.name / "summary.json", summary)
        r11._write_progress(output / run.name / "progress.log",
            f"{'FUTILITY_STOP' if stopped[i] else 'COMPLETE'} step={summary['last_step']}")
        summaries.append(summary)
    return summaries


def verification(study, device, *, trace=False, destination=None):
    study.registration()
    comparisons = {}
    trace_rows = []
    def refuse(message):
        if destination:
            study.write_json(destination, {"pass": False, "error": message,
                "comparisons": comparisons, "trace": trace_rows, "device": device.type,
                "registration_sha256": study.sha(study.OUTPUT / "registration.json"),
                "source_hashes": study.source_identities()})
        raise ValueError(message)
    for arm in ("free", "free_a", "a_forced"):
        runs = [Run(arm, "original", seed) for seed in (range(3) if arm != "a_forced" else (0,))]
        engine = Engine(study, runs, device)
        single = [Engine(study, [r], device) for r in runs]
        ordinary = [study._new_model(r.arm, r.seed) for r in runs]
        optimizers = [torch.optim.AdamW(m.parameters(), lr=.003, weight_decay=.01) for m in ordinary]
        streams = make_streams(study, runs, device)
        max_difference, trace_rows = 0., []
        resumed, restored = None, None
        for step in range(1, 9):
            batches = [s.draw() for s in streams]
            if trace:
                trace_rows.append({"step": step, "phase": "before_update", "arm": arm,
                    "parameter_differences": {key: [float((value[i]-dict(model.named_parameters())[key]).detach().abs().max())
                        for i,model in enumerate(ordinary)] for key,value in engine.parameters.items()},
                    "rolling_hashes": [s.rolling.hex() for s in streams]})
            if step > 3:
                for stream, original in zip(restored, batches, strict=True):
                    replay = stream.draw()
                    for key in vars(replay):
                        if not torch.equal(getattr(replay, key), getattr(original, key)):
                            raise ValueError("r10 restored stream differs")
            engine.update(batches, torch.ones(len(runs), device=device, dtype=torch.bool))
            if resumed:
                resumed.update(batches, torch.ones(len(runs), device=device, dtype=torch.bool))
            differences = {}
            for i, (model, optimizer, batch) in enumerate(zip(ordinary, optimizers, batches, strict=True)):
                single[i].update([batch], torch.ones(1, device=device, dtype=torch.bool))
                optimizer.zero_grad(set_to_none=True)
                loss, _ = grouped_loss(tuple(v[None] for v in model(batch.records, batch.queries, batch.lengths)), [batch], [runs[i]])
                loss.sum().backward(); optimizer.step()
                for key, value in model.named_parameters():
                    reference = value.detach()
                    actual = engine.parameters[key][i].detach()
                    delta = float((actual-reference).abs().max())
                    differences[key] = max(differences.get(key, 0), delta)
                    max_difference = max(max_difference, delta)
                    if not torch.allclose(actual, reference, atol=3e-5, rtol=3e-5):
                        if trace:
                            trace_rows.append({"step":step,"run":runs[i].name,"parameter":key,
                                "parameter_difference":delta,
                                "gradient_difference":float((engine.parameters[key].grad[i]-value.grad).abs().max())
                                    if value.grad is not None else None})
                        refuse(f"r10 ordinary AdamW differs: {arm} {key}")
                    if not torch.allclose(actual, single[i].parameters[key][0], atol=3e-5, rtol=3e-5):
                        raise ValueError("r10 independent execution differs")
                    if value.grad is not None:
                        for name, state_key in (("first", "exp_avg"), ("second", "exp_avg_sq")):
                            if not torch.allclose(getattr(engine.optimizer, name)[key][i], optimizer.state[value][state_key], atol=3e-5, rtol=3e-5):
                                raise ValueError("r10 optimizer moments differ")
            if trace:
                trace_rows.append({"step": step, "phase":"after_update", "parameter_maximum_differences": differences,
                    "gradient_maximum_differences": {key: [float((engine.parameters[key].grad[i]-value.grad).abs().max())
                        if value.grad is not None and engine.parameters[key].grad is not None else None
                        for i,model in enumerate(ordinary) for name,value in model.named_parameters() if name == key]
                        for key in engine.parameters}})
            if step == 3:
                with tempfile.TemporaryDirectory() as temporary:
                    path = Path(temporary) / "restore.pt"
                    publish(path, {"engine": engine.state(), "streams": [s.state() for s in streams]})
                    saved = bound_load(path)
                resumed, restored = Engine(study, runs, device), make_streams(study, runs, device)
                resumed.restore(saved["engine"])
                for stream, state in zip(restored, saved["streams"], strict=True):
                    stream.restore(state)
        for key, value in engine.parameters.items():
            if not torch.equal(value, resumed.parameters[key]):
                raise ValueError("r10 parameter restoration is not exact")
        for name in ("first", "second", "parameter_steps"):
            for key, value in getattr(engine.optimizer, name).items():
                if not torch.equal(value, getattr(resumed.optimizer, name)[key]):
                    raise ValueError("r10 optimizer restoration is not exact")
        for actual, restored_stream in zip(streams, restored, strict=True):
            for key, value in actual.state().items():
                other = restored_stream.state()[key]
                if isinstance(value, torch.Tensor) and not torch.equal(value, other):
                    raise ValueError("r10 exposure restoration differs")
                if isinstance(value, str) and value != other:
                    raise ValueError("r10 rolling hash restoration differs")
                if isinstance(value, int) and value != other:
                    raise ValueError("r10 draw count restoration differs")
                if key == "generators" and not all(torch.equal(a,b) for a,b in zip(value,other,strict=True)):
                    raise ValueError("r10 generator restoration differs")
        comparisons[arm] = {"width": len(runs), "updates": 8, "restore_step": 3,
                            "maximum_difference": max_difference, "pass": True, "trace": trace_rows}
    result = {"pass": True, "device": device.type, "comparisons": comparisons,
              "registration_sha256": study.sha(study.OUTPUT / "registration.json"),
              "source_hashes": study.source_identities(), "tolerances": r11.EQUIVALENCE_TOLERANCE}
    if destination:
        study.write_json(destination, result)
    return result
