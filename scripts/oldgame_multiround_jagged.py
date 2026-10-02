"""Registered rarity, erosion and A-supervision-dose study on the old game."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from recombination_promotion.public_paths import public_path, identity_matches
from types import SimpleNamespace

import numpy as np
import torch
from torch.func import functional_call, stack_module_state, vmap

from recombination_promotion.oldgame_ext.jagged_probes import (
    LINEAR_SETTINGS, MLP_SETTINGS, fit_reader,
)
from recombination_promotion.oldgame_ext import game
from recombination_promotion.oldgame_ext.multiround import enumerate_boards, load_frozen_A
from recombination_promotion.oldgame_ext.multiround_jagged import (
    BoardTables, DeviceStream, JaggedNetwork, grouped_loss, nested_dose_masks, new_model,
    rendering_ids,
)
from scripts import multiround_panels as choice
from scripts import oldgame_multiround_raw_diagnosis as r9
from scripts import oldgame_multiround_route_access as r8


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/phase11/oldgame_memory/multiround/study_r11_jagged"
SPEC = OUTPUT / "specification.md"
SMOKE = public_path("build/oldgame_ext/r11_smoke")
AUDITS = (0, 1000, 2000, 5000, 10000, 15000, 20000)
EROSION_READOUTS = (1, 5, 10, 50, 100)
EQUIVALENCE_TOLERANCE = {"parameters": {"atol": 3e-5, "rtol": 3e-5},
                         "optimizer_moments": {"atol": 3e-5, "rtol": 3e-5},
                         "discrete_state": "exact"}
PRECISION_TOLERANCE = {"B_loss_nats": .01, "natural_KL_bits": .005,
                       "A_vector_accuracy": .05}
SEEDS = (0, 1, 2)
LAWS = ("original", "equal")
EXPERIMENTS = ("rarity", "dose", "erosion")


@dataclass(frozen=True)
class RunSpec:
    experiment: str
    arm: str
    law: str
    seed: int

    @property
    def name(self) -> str:
        return f"{self.experiment}_{self.arm}_{self.law}_seed{self.seed}"

    @property
    def dual(self) -> bool:
        return self.experiment == "erosion"

    @property
    def draw(self) -> str:
        return self.arm if self.experiment == "rarity" else "uniform"

    @property
    def dose(self) -> int:
        if self.experiment == "dose":
            return int(self.arm.removeprefix("dose"))
        return 100 if self.experiment == "erosion" and self.arm == "a_plus_b" else 0


def all_runs() -> list[RunSpec]:
    return ([RunSpec("rarity", arm, law, seed)
             for arm in ("uniform", "cutoff", "decoy")
             for law in LAWS for seed in SEEDS]
            + [RunSpec("dose", f"dose{dose}", law, seed)
               for dose in (1, 10, 100) for law in LAWS for seed in SEEDS]
            + [RunSpec("erosion", arm, law, seed)
               for arm in ("b_only", "a_plus_b")
               for law in LAWS for seed in SEEDS])


def group_runs(name: str, *, smoke: bool = False,
               explicit: tuple[str, ...] = ()) -> list[RunSpec]:
    if explicit:
        by_name = {run.name: run for run in all_runs()}
        if any(value not in by_name for value in explicit):
            raise ValueError("r11 explicit run identity differs")
        selected = [by_name[value] for value in explicit]
    else:
        if name not in EXPERIMENTS:
            raise ValueError("r11 run group differs")
        selected = [run for run in all_runs() if run.experiment == name]
        if smoke:
            selected = [run for run in selected if run.seed == 0 and law_is_original(run)]
    if len({run.experiment for run in selected}) != 1 or len({run.dual for run in selected}) != 1:
        raise ValueError("one grouped process requires one model architecture")
    return selected


def law_is_original(run: RunSpec) -> bool:
    return run.law == "original"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def configure(device: str) -> torch.device:
    if device not in ("cpu", "cuda"):
        raise ValueError("r11 device differs")
    if device == "cuda":
        if not torch.cuda.is_available():
            raise ValueError("r11 requires visible physical selected GPU")
        if torch.cuda.device_count() != 1:
            raise ValueError("r11 sees more than one accelerator")
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    return torch.device(device)


def source_identities() -> dict:
    paths = {"design": SPEC, "r8_manifest": choice.OUTPUT / "manifest.json",
             "r8_registration": r8.OUTPUT / "registration.json",
             "r8_calibration": r8.OUTPUT / "calibration.json",
             "r9_results": r9.OUTPUT / "results.json",
             "r9_prefix_records": choice.OUTPUT / "prefix_records.npy",
             "r9_swap_records": choice.OUTPUT / "swap_records.npz",
             "module": ROOT / "src/recombination_promotion/oldgame_ext/multiround_jagged.py",
             "probes": ROOT / "src/recombination_promotion/oldgame_ext/jagged_probes.py",
             "script": Path(__file__)}
    return {key: sha(path) for key, path in paths.items()}


EXECUTION_WIDTHS = {"rarity": 3, "dose": 3, "erosion": 1}


def registration() -> dict:
    row = json.loads((OUTPUT / "registration.json").read_text())
    if (row["source_sha256"] != source_identities()
            or row["runs"] != [run.name for run in all_runs()]
            or row["settings"]["bf16_comparison_absolute_tolerances"] !=
            PRECISION_TOLERANCE
            or row["settings"]["equivalence_tolerances"] != EQUIVALENCE_TOLERANCE
            or row["settings"]["early_erosion_readout_steps"] != list(EROSION_READOUTS)
            or row["settings"]["execution_widths"] != EXECUTION_WIDTHS
            or row["settings"]["maximum_CPU_processes"] != 5
            or row["probe_settings"] != {"linear": LINEAR_SETTINGS, "mlp64": MLP_SETTINGS}):
        raise ValueError("r11 registration authority differs")
    return row


def register(device: torch.device) -> dict:
    if (OUTPUT / "registration.json").exists():
        raise ValueError("r11 registration already exists")
    boards = enumerate_boards()
    source, exact_a = load_frozen_A(ROOT)
    del source
    spec = SPEC.read_text()
    note = {
        "study": "r11_jagged_competence", "source_sha256": source_identities(),
        "claims_and_readings_verbatim": spec,
        "runs": [run.name for run in all_runs()],
        "exact_A_source": exact_a,
        "board_counts": [len(part) for part in boards.by_category],
        "settings": {"updates": 20000, "batch": 256, "rounds": 8,
                     "AdamW_learning_rate": .003, "AdamW_weight_decay": .01,
                     "audit_steps": list(AUDITS), "futility_update": 5000,
                     "early_erosion_readout_steps": list(EROSION_READOUTS),
                     "equivalence_tolerances": EQUIVALENCE_TOLERANCE,
                     "execution_widths": EXECUTION_WIDTHS,
                     "equivalence_check": {"widths": EXECUTION_WIDTHS,
                                           "batch": 256, "rounds": 8,
                                           "updates": 8, "nonzero_restore_update": 3,
                                           "restoration_tolerance": "exact"},
                     "futility_gap_fraction": .10, "A_loss_normalizer": "all_active_rounds",
                     "precision": "fp32 until the GPU 1k comparison accepts bf16",
                     "bf16_comparison_absolute_tolerances": PRECISION_TOLERANCE,
                     "evaluation_precision": "fp32", "device_default": "cuda",
                     "maximum_CPU_processes": 5, "CPU_threads_per_process": 1},
        "probe_settings": {"linear": LINEAR_SETTINGS, "mlp64": MLP_SETTINGS},
        "choices": [
            "Five processes use distinct CPU cores: one width-three rarity process, "
            "one width-three dose process, and three width-one erosion processes, one "
            "per seed. Each erosion process executes its four arm/law cases sequentially.",
            "Width one calls the model directly through functional_call, without vmap. "
            "Width-three erosion is a comparison diagnostic only, not study execution.",
            "AdamW applies the ordinary torch scalar bias corrections and operation "
            "order to each parameter slice, skipping an auxiliary head with no A loss.",
            "One seed/law uses the same category stream across rarity arms; within-category "
            "board and rendering streams have separately declared seeds.",
            "A single seeded uniform round mask per seed/law/update yields nested 1%, "
            "10% and 100% dose selections, independent of board and label.",
            "The r8 raw record architecture receives an unused auxiliary raw-state sum head "
            "in all raw arms, so the shared uniform zero-dose arm is identical.",
            "The r8 source A core is copied into both erosion starts; all parameters are "
            "trainable after update zero. B-only has no A loss.",
            "Complete rendering identities encode the four ordered (slot, mass-index) "
            "records in base 30. All active rendering and placement counts are retained; "
            "the rolling hash binds the executed records and the placement choices. "
            "Names and templates are tested on the fixed Stage-1 audit panels.",
            "Unseen calibration uses the seed-17 online stream for 16 updates and "
            "requires a nonempty tracked mask in the same B scorer as training.",
            "Saved r9 failing prefix and swap renderings are identified, counted and "
            "scored separately from the four board-census renderings.",
            "Futility compares the B-loss components at both endpoints. Erosion "
            "readouts at updates 1, 5, 10, 50 and 100 use the fixed 128-board panel.",
            "A CPU smoke uses reduced probe and board panels only; those audits are not "
            "admissible as study endpoints.",
        ],
        "registration_device": device.type,
    }
    if note["board_counts"] != [22491, 1835, 109] or len(note["runs"]) != 48:
        raise ValueError("r11 board or run census differs")
    write_json(OUTPUT / "registration.json", note)
    (OUTPUT / "registration.md").write_text(
        "# r11 registered jagged-competence study\n\n" + spec +
        "\n\n## Declared implementation choices\n\n" +
        "\n".join(f"- {choice}" for choice in note["choices"]) + "\n")
    return note


class StackedAdamW:
    """Elementwise independent AdamW states on stacked parameter tensors."""

    def __init__(self, parameters: dict[str, torch.Tensor], count: int,
                 *, lr: float = .003, wd: float = .01):
        self.parameters, self.lr, self.wd = parameters, lr, wd
        self.steps = torch.zeros(count, dtype=torch.long, device=next(iter(parameters.values())).device)
        self.first = {key: torch.zeros_like(value) for key, value in parameters.items()}
        self.second = {key: torch.zeros_like(value) for key, value in parameters.items()}
        self.parameter_steps = {key: torch.zeros(count, dtype=torch.long) for key in parameters}

    def zero_grad(self):
        for value in self.parameters.values():
            value.grad = None

    @torch.no_grad()
    def step(self, active: torch.Tensor, participation: dict[str, torch.Tensor] | None = None):
        self.steps += active.long()
        enabled = active.cpu()
        selected_by_parameter = ({key: value.cpu() for key, value in participation.items()}
                                 if participation else {})
        for key, value in self.parameters.items():
            if value.grad is None:
                continue
            selected = enabled & selected_by_parameter.get(key, enabled)
            self.parameter_steps[key] += selected.long()
            # Match torch AdamW's scalar bias corrections and operation order.
            # Float32 tensor powers can change a hard routing decision even
            # when their parameter differences are initially very small.
            for index in torch.nonzero(selected)[:, 0].tolist():
                gradient = value.grad[index]
                first, second = self.first[key][index], self.second[key][index]
                value[index].mul_(1 - self.lr * self.wd)
                first.lerp_(gradient, 1 - .9)
                second.mul_(.999).addcmul_(gradient, gradient, value=1 - .999)
                step = int(self.parameter_steps[key][index])
                denominator = (second.sqrt() / (1 - .999 ** step) ** .5).add_(1e-8)
                value[index].addcdiv_(first, denominator, value=-self.lr / (1 - .9 ** step))

    def state(self):
        return {"steps": self.steps.detach().cpu().clone(),
                "parameter_steps": {key: value.detach().cpu().clone()
                                    for key, value in self.parameter_steps.items()},
                "first": {key: value.detach().cpu().clone()
                          for key, value in self.first.items()},
                "second": {key: value.detach().cpu().clone()
                           for key, value in self.second.items()}}

    def restore(self, saved):
        self.steps.copy_(saved["steps"].to(self.steps.device))
        for name in ("first", "second", "parameter_steps"):
            for key, value in getattr(self, name).items():
                value.copy_(saved[name][key].to(value.device))


class GroupEngine:
    def __init__(self, runs: list[RunSpec], device: torch.device):
        self.runs, self.device = runs, device
        self.models = [new_model(run.seed, run.dual, repo_root=ROOT if run.dual else None)
                       .to(device) for run in runs]
        self.parameters, self.buffers = stack_module_state(self.models)
        self.optimizer = StackedAdamW(self.parameters, len(runs))

    def forward(self, records: torch.Tensor, lengths: torch.Tensor):
        template = self.models[0]
        if len(self.runs) == 1:
            output = functional_call(
                template, ({key: value[0] for key, value in self.parameters.items()},
                           {key: value[0] for key, value in self.buffers.items()}),
                (records[0], lengths[0]), {"return_all": True})
            return tuple(value[None] for value in output)
        return vmap(lambda p, b, x, n: functional_call(
            template, (p, b), (x, n), {"return_all": True}),
            in_dims=(0, 0, 0, 0))(self.parameters, self.buffers, records, lengths)

    def update(self, batches, selections, active, *, precision="fp32"):
        self.optimizer.zero_grad()
        records = torch.stack([batch.records for batch in batches])
        lengths = torch.stack([batch.lengths for batch in batches])
        with torch.autocast(self.device.type, dtype=torch.bfloat16,
                            enabled=precision == "bf16"):
            output = self.forward(records, lengths)
            losses, details = grouped_loss(output, batches, selections,
                                           dual=self.runs[0].dual)
        if not bool(torch.isfinite(losses).all()):
            raise ValueError("r11 non-finite training loss")
        (losses * active.float()).sum().backward()
        # Ordinary AdamW skips a parameter whose loss has no path to it. A
        # stacked auxiliary-head tensor can have a gradient in only some runs.
        # Those slices must also skip decay, moments and the Adam step counter.
        used = torch.tensor([selection is not None and bool(selection.any())
                             for selection in selections], device=self.device)
        participation = ({key: used for key in self.parameters
                          if key.startswith("raw_sum_head.")}
                         if not self.runs[0].dual else {})
        self.optimizer.step(active, participation)
        return [float(value) for value in losses.detach()], details

    def model_at(self, index: int, *, cpu=False):
        model = JaggedNetwork(dual=self.runs[index].dual)
        state = {key: value[index].detach().cpu() if cpu else value[index].detach()
                 for key, value in self.parameters.items()}
        model.load_state_dict(state, strict=True)
        model.to("cpu" if cpu else self.device).eval()
        return model

    def state(self):
        return {"parameters": {key: value.detach().cpu().clone() for key, value
                               in self.parameters.items()},
                "buffers": {key: value.detach().cpu().clone() for key, value
                            in self.buffers.items()},
                "optimizer": self.optimizer.state()}

    def restore(self, saved):
        with torch.no_grad():
            for key, value in self.parameters.items():
                value.copy_(saved["parameters"][key].to(self.device))
            for key, value in self.buffers.items():
                value.copy_(saved["buffers"][key].to(self.device))
        self.optimizer.restore(saved["optimizer"])


class DeviceAuditAdapter(torch.nn.Module):
    """Execute r8's scoring panels on the selected device, return CPU rows."""

    def __init__(self, model: JaggedNetwork, device: torch.device):
        super().__init__()
        self.model, self.device, self.route = model.eval(), device, model.route

    @torch.no_grad()
    def round_interfaces(self, records):
        result = self.model.round_interfaces(records.to(self.device))
        return tuple(value.float().cpu() for value in result)

    @torch.no_grad()
    def upper_step(self, answers, raw, previous=None):
        output = self.model.upper_step(
            answers.to(self.device), raw.to(self.device),
            None if previous is None else previous.to(self.device))
        return tuple(value.float().cpu() for value in output)

    @torch.no_grad()
    def forward(self, records, lengths, *, answer_override=None, raw_override=None,
                initial_upper=None, return_trace=False):
        options = {"answer_override": None if answer_override is None else
                   answer_override.to(self.device),
                   "raw_override": None if raw_override is None else raw_override.to(self.device),
                   "initial_upper": None if initial_upper is None else
                   initial_upper.to(self.device), "return_trace": return_trace}
        result = self.model(records.to(self.device), lengths.to(self.device), **options)
        if isinstance(result, dict):
            return {key: value.float().cpu() for key, value in result.items()}
        return tuple(value.float().cpu() for value in result)


def _probe_arrays(model: JaggedNetwork, device: torch.device, split: dict):
    (train_records, train_y), (heldout_records, heldout_y) = r8._probe_data(split)
    features = []
    with torch.no_grad():
        for records in (train_records, heldout_records):
            raw_parts, upper_parts = [], []
            for start in range(0, len(records), 256):
                _, answers, raw = model.round_interfaces(torch.from_numpy(
                    records[start:start + 256]).to(device))
                _, upper = model.upper_step(answers, raw)
                raw_parts.append(raw.float())
                upper_parts.append(upper.float())
            features.append((torch.cat(raw_parts), torch.cat(upper_parts)))
    return features, (torch.from_numpy(train_y).to(device),
                      torch.from_numpy(heldout_y).to(device))


def probe_audit(model: JaggedNetwork, device: torch.device, *, smoke=False,
                oracle=False) -> dict:
    split = json.loads((r8.OUTPUT / "probe_split.json").read_text())
    if oracle:
        (train_records, train_y), (heldout_records, heldout_y) = r8._probe_data(split)
        train_carrier = r8._carrier(model.cpu(), train_records, oracle_carrier=True)
        test_carrier = r8._carrier(model.cpu(), heldout_records, oracle_carrier=True)
        features = [(torch.from_numpy(train_carrier[site]).to(device),
                     torch.from_numpy(test_carrier[site]).to(device)) for site in range(2)]
        targets = (torch.from_numpy(train_y).to(device),
                   torch.from_numpy(heldout_y).to(device))
        model.to(device)
    else:
        (train_features, test_features), targets = _probe_arrays(model, device, split)
        features = [(train_features[site], test_features[site]) for site in range(2)]
    train_y, test_y = targets
    if smoke:
        # The first training identities include the forced value coverage.
        count = 256
        features = [(train[:count], test[:64]) for train, test in features]
        train_y, test_y = train_y[:count], test_y[:64]
        slots = (0,)
    else:
        slots = range(5)
    result = {"raw": {}, "upper": {}}
    values = torch.tensor([int(value) for value in __import__(
        "recombination_promotion.oldgame_ext.memory", fromlist=["VALUES"]).VALUES],
        device=device)
    for site, (train, test) in zip(("raw", "upper"), features, strict=True):
        for family in ("linear", "mlp64"):
            result[site][family] = {"sum36": [], "category3": []}
            for slot in slots:
                for task, y, z in (("sum36", train_y[:, slot], test_y[:, slot]),
                                   ("category3", torch.where(values[train_y[:, slot]] <= 12,
                                    0, torch.where(values[train_y[:, slot]] >= 24, 2, 1)),
                                    torch.where(values[test_y[:, slot]] <= 12, 0,
                                    torch.where(values[test_y[:, slot]] >= 24, 2, 1)))):
                    result[site][family][task].append(fit_reader(
                        train, y, test, z, family=family, seed=2026100802 + slot,
                        max_iter=250 if smoke else 5000))
    rng = np.random.default_rng(2026100804)
    floors = {"sum36": [], "category3": []}
    for slot in range(5):
        source = train_y[:, slot].cpu().numpy()
        target = test_y[:, slot].cpu().numpy()
        for task in floors:
            if task == "category3":
                from recombination_promotion.oldgame_ext.memory import VALUES
                source = np.where(np.asarray(VALUES)[source] <= 12, 0,
                                  np.where(np.asarray(VALUES)[source] >= 24, 2, 1))
                target = np.where(np.asarray(VALUES)[target] <= 12, 0,
                                  np.where(np.asarray(VALUES)[target] >= 24, 2, 1))
            majority = int(np.bincount(source).argmax())
            floors[task].append({"slot": slot + 1,
                                 "majority_accuracy": float(np.mean(target == majority)),
                                 "shuffled_accuracy": float(np.mean(
                                     rng.permutation(target) == target))})
    return {"sites": result, "floors": floors, "train_boards": len(train_y),
            "heldout_boards": len(test_y), "reduced_smoke": smoke,
            "probe_fit_devices": {"linear": "cpu", "mlp64": device.type}}


_CENSUS_CACHE: dict[tuple[int, bytes], np.ndarray] = {}


def _census_records(boards, indices: np.ndarray, *, render_offset: int):
    key = (render_offset, indices.tobytes())
    if key not in _CENSUS_CACHE:
        seeds = indices + np.int64(2026100901 + 1_000_003 * render_offset)
        _CENSUS_CACHE[key] = choice.record_projection(indices, seeds, boards)
    return _CENSUS_CACHE[key]


@lru_cache(maxsize=1)
def _saved_r9_renderings() -> tuple[dict, ...]:
    saved = json.loads((r9.OUTPUT / "results.json").read_text())
    boards = enumerate_boards()
    _, _, prefix, lengths, metadata = r8._panels("original")
    with np.load(choice.OUTPUT / "swap_records.npz") as rows:
        swap = {int(board): record.copy() for board, record in
                zip(rows["board_ids"], rows["records"], strict=True)}
    found = {}

    def add(board, record, source):
        total = [0] * 5
        for slot, mass in record:
            total[int(slot)] += game.MASSES[int(mass)]
        if tuple(total) != boards.boards[int(board)]:
            raise ValueError("r11 saved r9 records differ from the declared board")
        identity = int(rendering_ids(torch.from_numpy(record)))
        row = found.setdefault(identity, {"board_id": int(board),
                                         "rendering_id": identity,
                                         "records": record.tolist(), "sources": []})
        if row["board_id"] != int(board):
            raise ValueError("r11 saved rendering has inconsistent board identity")
        row["sources"].append(source)

    for seed in SEEDS:
        run = saved["runs"][f"raw_only_seed{seed}"]
        for case, row in run["failed_prefix_cases"].items():
            index = row["worst_index"]
            for at, board in enumerate(metadata[index]["board_indices"]):
                if at >= lengths[index]:
                    raise ValueError("r11 saved r9 prefix exceeds its active length")
                add(board, prefix[index, at],
                    {"seed": seed, "case": case, "prefix_index": index, "round": at + 1})
        for case, row in run["failed_swap_cases"].items():
            for name, item in row["boards"].items():
                board = item["board_id"]
                add(board, swap[board], {"seed": seed, "case": case,
                                         "scenario": row["scenario"], "member": name})
    return tuple(found[key] for key in sorted(found))


@torch.no_grad()
def _score_saved_r9_renderings(adapter, law: str, boards) -> dict:
    rows = _saved_r9_renderings()
    if not rows:
        raise ValueError("r11 saved r9 failing rendering panel is empty")
    records = torch.tensor([row["records"] for row in rows], dtype=torch.long)
    _, a, raw = adapter.round_interfaces(records)
    sums = np.asarray(boards.boards)[:, 0]
    anchor_ids = np.array([np.flatnonzero(sums == value)[0] for value in (0, 36)])
    anchor_records = _census_records(boards, anchor_ids, render_offset=0)
    _, anchor_a, anchor_raw = adapter.round_interfaces(torch.from_numpy(anchor_records))
    _, anchors = adapter.upper_step(anchor_a, anchor_raw)
    predicted = []
    for mode in range(2):
        logits, _ = adapter.upper_step(a, raw, anchors[mode:mode + 1].expand(len(rows), -1))
        predicted.append(torch.softmax(logits, -1).numpy())
    paired = np.stack(predicted, 1)
    truth = np.array([0 if boards.boards[row["board_id"]][0] <= 12 else
                      2 if boards.boards[row["board_id"]][0] >= 24 else 1 for row in rows])
    if law == "original":
        classified = r9.signature(paired)
        expected = np.asarray(r9.TRUTH)[np.stack((np.where(truth == 2, 1, 0),
                                                 np.where(truth == 0, 0, 1)), 1)]
    else:
        from recombination_promotion.oldgame_ext.multiround import P_EQUAL
        classified = None
        expected = np.broadcast_to(np.asarray(P_EQUAL, dtype=float), paired.shape)
    errors = r9.tv(paired, expected)
    return {"count": len(rows), "maximum_TV": float(errors.max()),
            "above_0_02_TV": int((errors.max(1) > .02).sum()),
            "categorical_misreads": (None if classified is None else
                                     int((classified != truth).sum())),
            "rows": [{**row, "exact_category": int(truth[index]),
                      "predicted_category": None if classified is None else int(classified[index]),
                      "outputs_after_L_H": paired[index].tolist(),
                      "TV_after_L_H": errors[index].tolist()}
                     for index, row in enumerate(rows)]}


def board_census(model: JaggedNetwork, law: str, device: torch.device,
                 *, smoke=False) -> dict:
    boards = enumerate_boards()
    full = np.arange(len(boards.boards), dtype=np.int64)
    if smoke:
        sums = np.asarray(boards.boards)[:, 0]
        selected = set(np.linspace(0, len(full) - 1, 128, dtype=np.int64))
        for value in (0, 10, 12, 13, 16, 20, 23, 24, 27, 36):
            selected.add(int(np.flatnonzero(sums == value)[0]))
        full = np.asarray(sorted(selected), dtype=np.int64)
    adapter = DeviceAuditAdapter(model, device)
    total = np.asarray(boards.boards, dtype=np.int64)[full, 0]
    truth = np.where(total <= 12, 0, np.where(total >= 24, 2, 1))
    low = int(np.flatnonzero(total == 0)[0])
    high = int(np.flatnonzero(total == 36)[0])
    renderings = []
    for rendering in range(4):
        records = _census_records(boards, full, render_offset=rendering)
        a, raw = [], []
        for at in range(0, len(records), 512):
            _, aa, rr = adapter.round_interfaces(torch.from_numpy(records[at:at + 512]))
            a.append(aa)
            raw.append(rr)
        a, raw = torch.cat(a), torch.cat(raw)
        _, l_state = adapter.upper_step(a[low:low + 1], raw[low:low + 1])
        _, h_state = adapter.upper_step(a[high:high + 1], raw[high:high + 1])
        rows = []
        for state in (l_state, h_state):
            predicted = []
            for at in range(0, len(records), 512):
                end = min(at + 512, len(records))
                logits, _ = adapter.upper_step(a[at:end], raw[at:end],
                                                state.expand(end - at, -1))
                predicted.append(torch.softmax(logits, -1).numpy())
            rows.append(np.concatenate(predicted))
        paired = np.stack(rows, 1)
        category = r9.signature(paired) if law == "original" else None
        if law == "original":
            expected = np.asarray(r9.TRUTH)[np.stack((np.where(truth == 2, 1, 0),
                                                        np.where(truth == 0, 0, 1)), axis=1)]
        else:
            from recombination_promotion.oldgame_ext.multiround import P_EQUAL
            expected = np.broadcast_to(np.asarray(P_EQUAL, dtype=float), paired.shape)
        errors = r9.tv(paired, expected)
        failed = errors.max(1) > .02
        if category is not None:
            failed = failed | (category != truth)
        by_sum = {}
        for value in np.unique(total):
            selected = total == value
            by_sum[str(value)] = {
                "boards": int(selected.sum()),
                "distance_to_boundary": int(min(abs(value - 12), abs(value - 24))),
                "categorical_misreads": (None if category is None else
                                         int((category[selected] != truth[selected]).sum())),
                "above_0_02_TV": int((errors[selected].max(1) > .02).sum()),
                "maximum_TV": float(errors[selected].max()),
            }
        renderings.append({"rendering": rendering, "boards": len(full),
                           "categorical_misreads": (None if category is None else
                                                    int((category != truth).sum())),
                           "category_status": ("UNDEFINED_EQUAL_LAW" if category is None
                                               else "MEASURED"),
                           "above_0_02_TV": int((errors.max(1) > .02).sum()),
                           "maximum_TV": float(errors.max()),
                           "by_slot1_sum_twelfths": by_sum,
                           "failed_board_ids": full[failed].tolist()})
    return {"registered_rendering": renderings[0],
            "additional_fixed_renderings": renderings[1:],
            "saved_r9_failed_renderings": _score_saved_r9_renderings(adapter, law, boards),
            "reduced_smoke": smoke}


def _candidate_panel(law: str):
    panel = choice.load_episodes(choice.OUTPUT / (
        "test.npz" if law == "original" else "equal_test.npz"))
    return r8.online.UnseenCandidates(panel)


def _score_b(model, law: str, candidate, *, reject_empty=False) -> dict:
    unseen = candidate.mask()
    if reject_empty and not unseen.any():
        raise ValueError("r11 unseen calibration panel is empty")
    return r8.audit_model(model, law, unseen, probes=False, require_unseen=True)


def _calibration_unseen(law: str, device: torch.device):
    candidate = _candidate_panel(law)
    stream = DeviceStream(BoardTables(device), 17, law, "uniform")
    for _ in range(16):
        _observe(candidate, stream.draw_batch())
    mask = candidate.mask()
    if not mask.any():
        raise ValueError("r11 unseen calibration panel is empty")
    return candidate, {"stream_seed": 17, "tracked_updates": 16,
                       "stream_hash": stream.rolling.hex(),
                       "mask_sha256": hashlib.sha256(mask.tobytes()).hexdigest(),
                       "composition": candidate.composition(mask)}


def audit_one(model: JaggedNetwork, law: str, device: torch.device,
              candidate, *, smoke=False) -> dict:
    start = time.monotonic()
    model.eval()
    adapter = DeviceAuditAdapter(model, device)
    with torch.no_grad():
        b = _score_b(adapter, law, candidate)
        b["route_damage"] = r8.route_damage(adapter, law)
        b["board_census"] = board_census(model, law, device, smoke=smoke)
    b["probes"] = probe_audit(model, device, smoke=smoke)
    b["elapsed_seconds"] = time.monotonic() - start
    b["evaluation_precision"] = "float32"
    return b


@torch.no_grad()
def a_accuracy(model: JaggedNetwork, device: torch.device, *, smoke=False) -> dict:
    boards = enumerate_boards()
    ids = np.arange(len(boards.boards), dtype=np.int64)
    if smoke:
        ids = ids[np.linspace(0, len(ids) - 1, 128, dtype=np.int64)]
    records = _census_records(boards, ids, render_offset=0)
    truth = torch.tensor(np.asarray(boards.boards, dtype=np.int64)[ids], device=device)
    values = torch.tensor([int(value) for value in __import__(
        "recombination_promotion.oldgame_ext.memory", fromlist=["VALUES"]).VALUES],
        device=device)
    target = torch.searchsorted(values, truth)
    predictions = []
    for at in range(0, len(records), 256):
        x = torch.from_numpy(records[at:at + 256]).to(device)
        sums, _, raw = model.round_interfaces(x)
        logits = sums if model.dual else model.raw_sum_head(raw).reshape(-1, 5, 36)
        predictions.append(logits.argmax(-1))
    predicted = torch.cat(predictions)
    correct = predicted == target
    return {"per_slot": [{"correct": int(correct[:, slot].sum()), "total": len(ids)}
                         for slot in range(5)],
            "vector": {"correct": int(correct.all(-1).sum()), "total": len(ids)},
            "reduced_smoke": smoke}


@torch.no_grad()
def local_a_accuracy(model: JaggedNetwork, device: torch.device) -> dict | None:
    if not model.dual:
        return None
    from recombination_promotion.oldgame_ext import game
    from recombination_promotion.oldgame_ext.memory import VALUE_INDEX
    histories = game.histories()
    predicted = []
    for history in histories:
        state = model.memory.start_state[None]
        for mass in history:
            state = model.memory.step(state, torch.tensor(
                [game.MASSES.index(mass)], device=device))
        predicted.append(int(model.memory.answer(state, game.KIND_SUM).argmax(-1)))
    correct = sum(predicted[index] == VALUE_INDEX[game.sigma(history)]
                  for index, history in enumerate(histories))
    return {"correct": correct, "total": len(histories)}


@lru_cache(maxsize=1)
def _old_failure_boards() -> list[int]:
    saved = json.loads((r9.OUTPUT / "results.json").read_text())
    found: set[int] = set()

    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "board_id" and isinstance(item, int):
                    found.add(item)
                else:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    for seed in SEEDS:
        visit(saved["runs"][f"raw_only_seed{seed}"]["failed_prefix_cases"])
        visit(saved["runs"][f"raw_only_seed{seed}"]["failed_swap_cases"])
    return sorted(found)


def _exposures(stream: DeviceStream, counts_path: Path | None = None) -> dict:
    board = stream.board_exposure.cpu().numpy()
    sums = stream.sum_exposure.cpu().numpy()
    rendering = stream.rendering_exposure.cpu().numpy()
    placements = stream.placement_exposure.cpu().numpy()
    if counts_path is None:
        complete = {"by_rendering_id": {str(index): int(rendering[index])
                                        for index in np.flatnonzero(rendering)},
                    "by_placement_id": {str(index): int(placements[index])
                                        for index in np.flatnonzero(placements)}}
    else:
        arrays = {"rendering_counts": rendering, "placement_counts": placements}
        if counts_path.exists():
            with np.load(counts_path) as saved:
                if any(not np.array_equal(saved[key], value) for key, value in arrays.items()):
                    raise ValueError("r11 complete rendering exposure file differs")
        else:
            np.savez_compressed(counts_path, **arrays)
        complete = {"path": str(counts_path), "file_sha256": sha(counts_path)}
    complete.update({"encoding": "sum((slot*6+mass_index)*30**position), position=0..3",
                     "total": int(rendering.sum()), "distinct": int(np.count_nonzero(rendering))})
    return {"by_slot1_sum": sums.tolist(),
            "by_board_id": board.tolist(),
            "by_render_order": stream.render_exposure.cpu().tolist(),
            "complete_rendering_counts": complete,
            "r9_failure_renderings": [{**row, "count": int(rendering[row["rendering_id"]])}
                                      for row in _saved_r9_renderings()],
            "r9_failure_boards": {str(index): int(board[index])
                                   for index in _old_failure_boards()}}


def calibrate(device: torch.device) -> dict:
    registration()
    if (OUTPUT / "calibration.json").exists():
        raise ValueError("r11 calibration already exists")
    # The same registered B predicates score both oracle and experimental rows.
    b_rows = {}
    unseen_panels = {}
    candidates = {}
    for law in LAWS:
        candidates[law], unseen_panels[law] = _calibration_unseen(law, device)
        b_rows[law] = {}
        for name, route, current_only in (("oracle_A", "a_only", False),
                                           ("oracle_raw", "raw_only", False),
                                           ("current_board_null", "a_only", True)):
            oracle = r8.ExactRowModel(route, law, current_only=current_only).eval()
            b_rows[law][name] = _score_b(oracle, law, candidates[law], reject_empty=True)
            b_rows[law][name]["route_damage"] = r8.route_damage(oracle, law)
        if not all(b_rows[law][name]["B_pass"] for name in ("oracle_A", "oracle_raw")):
            raise ValueError("r11 exact B oracle fails a registered bar")
    if (b_rows["original"]["current_board_null"]["B_pass"]
            or b_rows["original"]["current_board_null"]["mode_law"][
                "witness_excess_bits"] <= 0):
        raise ValueError("r11 original-law current-board null does not separate")
    if abs(b_rows["equal"]["current_board_null"]["natural_excess_KL_bits"] -
           b_rows["equal"]["oracle_raw"]["natural_excess_KL_bits"]) > 1e-10:
        raise ValueError("r11 equal-law null differs from its exact row")
    original_oracle = r8.ExactRowModel("raw_only", "original").eval()
    oracle_census = board_census(original_oracle, "original", torch.device("cpu"))
    if any(row["categorical_misreads"] or row["above_0_02_TV"]
           for row in (oracle_census["registered_rendering"],
                       *oracle_census["additional_fixed_renderings"],
                       oracle_census["saved_r9_failed_renderings"])):
        raise ValueError("r11 record-derived board oracle fails the census")
    equal_census = board_census(r8.ExactRowModel("raw_only", "equal").eval(),
                                "equal", torch.device("cpu"))
    if any(row["above_0_02_TV"] for row in (
            equal_census["registered_rendering"],
            *equal_census["additional_fixed_renderings"],
            equal_census["saved_r9_failed_renderings"])):
        raise ValueError("r11 equal-law record-derived oracle fails the census")
    exact_a_model = new_model(0, True, repo_root=ROOT).to(device).eval()
    exact_a_boards = a_accuracy(exact_a_model, device)
    if exact_a_boards["vector"]["correct"] != exact_a_boards["vector"]["total"]:
        raise ValueError("r11 frozen exact-A source fails legal-board sums")
    untrained = new_model(0, False).to(device).eval()
    untrained_b = _score_b(DeviceAuditAdapter(untrained, device), "original",
                           candidates["original"], reject_empty=True)
    if untrained_b["B_pass"]:
        raise ValueError("r11 untrained network passes B bars")
    untrained_census = board_census(untrained, "original", device)
    if untrained_census["registered_rendering"]["above_0_02_TV"] == 0:
        raise ValueError("r11 untrained network does not separate the board census")
    oracle_probes = probe_audit(untrained, device, oracle=True)
    untrained_probes = probe_audit(untrained, device)
    positive = all(row["accuracy"] >= .99 and row["converged"] is not False
                   for sites in oracle_probes["sites"].values()
                   for family in sites.values() for row in family["sum36"])
    if not positive:
        raise ValueError("r11 exact-A probe positive is below 99% or unconverged")
    floor_separated = any(
        oracle_probes["sites"][site][family]["sum36"][slot]["accuracy"] -
        untrained_probes["sites"][site][family]["sum36"][slot]["accuracy"] > .10
        for site in ("raw", "upper") for family in ("linear", "mlp64")
        for slot in range(5))
    if not floor_separated:
        raise ValueError("r11 untrained A probe floor does not separate")
    # One saved r8 carrier anchors the torch/sklearn equivalence test.
    saved_model, checkpoint = r9.load_model("raw_only", 0)
    split = json.loads((r8.OUTPUT / "probe_split.json").read_text())
    (train_records, train_y), (test_records, test_y) = r8._probe_data(split)
    train_raw = r8._carrier(saved_model, train_records)[0]
    test_raw = r8._carrier(saved_model, test_records)[0]
    torch_row = fit_reader(torch.tensor(train_raw, device=device),
                           torch.tensor(train_y[:, 0], device=device),
                           torch.tensor(test_raw, device=device),
                           torch.tensor(test_y[:, 0], device=device),
                           family="linear", seed=2026100802)
    sklearn_row = r8._fit_probe(train_raw, train_y[:, 0], test_raw, test_y[:, 0],
                                family="linear", seed=2026100802)
    agreement = float(np.mean(np.asarray(torch_row["predictions"]) ==
                              np.asarray(sklearn_row["predictions"])))
    if agreement < .98 or abs(torch_row["accuracy"] - sklearn_row["accuracy"]) > .02:
        raise ValueError("r11 torch probe differs from saved r8 sklearn probe")
    # A null without eligible pairs is explicitly uncalibrated, never a pass.
    null_eligible = int(b_rows["original"]["current_board_null"]["mode_law"][
        "rows"]["L_N1"]["count"])
    if null_eligible == 0:
        raise ValueError("r11 current-board null has no eligible witness rows")
    sampler_rows = {}
    tables = BoardTables(device)
    for law in LAWS:
        streams = {draw: DeviceStream(tables, 0, law, draw)
                   for draw in ("uniform", "cutoff", "decoy")}
        for _ in range(16):
            batches = {draw: stream.draw_batch() for draw, stream in streams.items()}
            if not all(torch.equal(batches["uniform"].categories, row.categories) and
                       torch.equal(batches["uniform"].targets, row.targets)
                       for row in batches.values()):
                raise ValueError("r11 paired rarity law stream differs")
        sampler_rows[law] = {draw: {"slot1_sum_counts": stream.sum_exposure.cpu().tolist(),
                                   "render_order_counts": stream.render_exposure.cpu().tolist(),
                                   "rolling_batch_hash": stream.rolling.hex(),
                                   "complete_exposure": _exposures(stream)}
                             for draw, stream in streams.items()}
        rows = sampler_rows[law]
        if (rows["cutoff"]["slot1_sum_counts"][23] <= 5 *
                rows["uniform"]["slot1_sum_counts"][23] or
                rows["decoy"]["slot1_sum_counts"][20] <= 5 *
                rows["uniform"]["slot1_sum_counts"][20]):
            raise ValueError("r11 cutoff or decoy enrichment not observed")
    historical = {}
    for law in LAWS:
        for seed in SEEDS:
            path = r8.OUTPUT / f"raw_only_{law}_seed{seed}/audit_step_020000.json"
            saved = json.loads(path.read_text())["audit"]
            historical[f"{law}_seed{seed}"] = {
                "file_sha256": sha(path),
                "natural_KL": saved["natural_excess_KL_bits"],
                "law_maximum_TV": saved["mode_law"]["maximum_TV"],
                "swaps_pass": saved["swaps"]["natural_swap_pass"]}
    row = {"B": b_rows, "untrained_B": untrained_b, "unseen_panels": unseen_panels,
           "board_census": {"oracle": oracle_census, "equal_oracle": equal_census,
                            "untrained": untrained_census},
           "frozen_A_board_accuracy": exact_a_boards,
           "sampler": sampler_rows, "historical_r8_baseline": historical,
           "probe": {"oracle": oracle_probes, "untrained": untrained_probes,
                     "torch_sklearn_saved_r8": {
                         "checkpoint": checkpoint, "prediction_agreement": agreement,
                         "torch_accuracy": torch_row["accuracy"],
                         "sklearn_accuracy": sklearn_row["accuracy"],
                         "torch_converged": torch_row["converged"],
                         "sklearn_converged": sklearn_row["converged"]}},
           "checks": {"B_oracle_both_laws": True, "unseen_calibration_nonempty": True,
                      "saved_r9_renderings_oracle_exact": True,
                      "A_probe_positive": positive,
                      "untrained_probe_floor_separates": floor_separated,
                      "board_census_oracle_exact": True,
                      "equal_board_census_oracle_exact": True,
                      "frozen_A_all_boards_exact": True,
                      "board_census_untrained_fails": True,
                      "original_current_board_null_fails": True,
                      "equal_current_board_null_exact": True,
                      "untrained_B_fails": True,
                      "null_eligible": null_eligible,
                      "torch_sklearn_probe_agrees": True},
           "device": device.type, "evaluation_precision": "float32"}
    write_json(OUTPUT / "calibration.json", row)
    return {"checks": row["checks"], "torch_sklearn_agreement": agreement,
            "oracle_probe_minimum": min(
                entry["accuracy"] for sites in oracle_probes["sites"].values()
                for family in sites.values() for entry in family["sum36"])}


def _group_identity(runs: list[RunSpec]) -> str:
    material = "\n".join(run.name for run in runs).encode()
    return runs[0].experiment + "_" + hashlib.sha256(material).hexdigest()[:12]


def _save_group(path: Path, engine: GroupEngine, streams, candidates,
                runs, curve, stopped, step, precision):
    if path.exists():
        raise ValueError("r11 grouped checkpoint already exists")
    record = {"group_runs": [run.name for run in runs], "step": step,
              "engine": engine.state(), "streams": [stream.state() for stream in streams],
              "candidate_seen": [candidate.seen for candidate in candidates],
              "curve": curve, "stopped": stopped,
              "precision": precision, "registration_sha256": sha(OUTPUT / "registration.json"),
              "calibration_sha256": sha(OUTPUT / "calibration.json")}
    torch.save(record, path)
    path.with_suffix(".sha256").write_text(sha(path) + "\n")


def _save_run_checkpoints(group_path: Path, run_dirs, engine, streams,
                          candidates, curves, stopped, step):
    bound_group = sha(group_path)
    for index, directory in enumerate(run_dirs):
        if not curves[index] or curves[index][-1]["step"] != step:
            continue
        path = directory / f"checkpoint_step_{step:06d}.pt"
        if path.exists():
            saved = torch.load(path, map_location="cpu", weights_only=False)
            if saved["group_sha256"] != bound_group or path.with_suffix(
                    ".sha256").read_text().strip() != sha(path):
                raise ValueError("r11 per-run checkpoint differs from grouped authority")
            continue
        row = {"step": step, "group_sha256": bound_group,
               "model": {key: value[index].detach().cpu().clone()
                         for key, value in engine.parameters.items()},
               "optimizer": {
                   "step": int(engine.optimizer.steps[index]),
                   "parameter_steps": {key: int(value[index])
                                       for key, value in engine.optimizer.parameter_steps.items()},
                   "first": {key: value[index].detach().cpu().clone()
                             for key, value in engine.optimizer.first.items()},
                   "second": {key: value[index].detach().cpu().clone()
                              for key, value in engine.optimizer.second.items()}},
               "stream": streams[index].state(),
               "candidate_seen": candidates[index].seen.copy(),
               "futility_stop": bool(stopped[index]),
               "registration_sha256": sha(OUTPUT / "registration.json"),
               "calibration_sha256": sha(OUTPUT / "calibration.json")}
        torch.save(row, path)
        path.with_suffix(".sha256").write_text(sha(path) + "\n")


def _restore_group(directory: Path, engine, streams, candidates, runs, precision):
    paths = sorted(directory.glob("checkpoint_step_*.pt"))
    if not paths:
        return 0, [[] for _ in runs], [False] * len(runs)
    path = paths[-1]
    if path.with_suffix(".sha256").read_text().strip() != sha(path):
        raise ValueError("r11 grouped checkpoint digest differs")
    row = torch.load(path, map_location="cpu", weights_only=False)
    if (row["group_runs"] != [run.name for run in runs]
            or row["precision"] != precision
            or not identity_matches(row["registration_sha256"], sha(OUTPUT / "registration.json"))
            or not identity_matches(row["calibration_sha256"], sha(OUTPUT / "calibration.json"))):
        raise ValueError("r11 grouped checkpoint authority differs")
    engine.restore(row["engine"])
    for stream, state in zip(streams, row["streams"], strict=True):
        stream.restore(state)
    for candidate, seen in zip(candidates, row["candidate_seen"], strict=True):
        candidate.seen = seen
    return row["step"], row["curve"], row["stopped"]


def _futility(first: dict, current: dict, run: RunSpec) -> dict:
    floor = math.log(2) * 1.5 if run.law == "original" else -sum(
        float(value) * math.log(float(value)) for value in
        __import__("recombination_promotion.oldgame_ext.multiround",
                   fromlist=["P_EQUAL"]).P_EQUAL)
    initial_gap = max(first["train_parts"]["B"] - floor, 0)
    training_closed = ((first["train_parts"]["B"] - current["train_parts"]["B"]) /
                       initial_gap if initial_gap else 0)
    initial_kl = first["audit"]["natural_excess_KL_bits"]
    kl_closed = ((initial_kl - current["audit"]["natural_excess_KL_bits"]) /
                 initial_kl if initial_kl else 0)
    a_improved = (current["A_accuracy"] > first["A_accuracy"]
                  if run.dose else False)
    a_changed = (current["A_accuracy"] != first["A_accuracy"]
                 if run.experiment == "erosion" else False)
    stop = training_closed < .10 and kl_closed < .10 and not a_improved and not a_changed
    return {"training_gap_closed": training_closed, "natural_KL_gap_closed": kl_closed,
            "A_improved": a_improved, "erosion_A_changed": a_changed, "stop": stop}


def _selection(batch, run: RunSpec, step: int, device: torch.device):
    if run.dose == 0:
        return None
    if run.experiment == "erosion":
        return batch.active
    seed = 2026101100 + run.seed + 100 * (run.law == "equal") + 10_000 * step
    return nested_dose_masks(batch.active, seed, device=device)[run.dose]


def _dose_counts(target: torch.Tensor, selected: torch.Tensor | None):
    if selected is None:
        return torch.zeros((5, 37), dtype=torch.long)
    output = []
    for slot in range(5):
        output.append(torch.bincount(target[..., slot][selected].cpu(), minlength=37))
    return torch.stack(output)


def _observe(candidate, batch):
    row = SimpleNamespace(boards=batch.board_ids.cpu().numpy(),
                          lengths=batch.lengths.cpu().numpy())
    candidate.observe(row)


def _audit_record(model, run, candidate, stream, device, step, loss, details, dose_counts,
                  *, smoke, counts_path=None):
    audit = audit_one(model, run.law, device, candidate, smoke=smoke)
    a = a_accuracy(model, device, smoke=smoke)
    local = local_a_accuracy(model, device)
    return {"step": step, "train_loss_nats": loss,
            "train_parts": details, "audit": audit, "A_board_accuracy": a,
            "A_local_history_accuracy": local,
            "A_accuracy": a["vector"]["correct"] / a["vector"]["total"],
            "dose_selected_by_slot_sum": dose_counts.tolist(),
            "exposure": _exposures(stream, counts_path),
            "stream_rolling_hash": stream.rolling.hex()}


def _erosion_readout(model, device, step: int, details: dict) -> dict:
    return {"step": step, "panel": "fixed 128-board panel, no fitting",
            "A_board_accuracy": a_accuracy(model, device, smoke=True),
            "train_parts": details, "evaluation_precision": "float32"}


def _write_progress(path: Path, message: str):
    with path.open("a") as handle:
        handle.write(message + "\n")
        handle.flush()
    print(f"{path.parent.name}: {message}", flush=True)


def _run_chunk(runs: list[RunSpec], device: torch.device, output_root: Path,
               *, steps: int, smoke: bool, precision: str):
    if len({run.dual for run in runs}) != 1:
        raise ValueError("r11 grouped model types differ")
    group_dir = output_root / "groups" / _group_identity(runs)
    group_dir.mkdir(parents=True, exist_ok=True)
    run_dirs = [output_root / "runs" / run.name for run in runs]
    for directory in run_dirs:
        directory.mkdir(parents=True, exist_ok=True)
    tables = BoardTables(device)
    engine = GroupEngine(runs, device)
    streams = [DeviceStream(tables, run.seed, run.law, run.draw,
                            batch=256, rounds=8) for run in runs]
    candidates = [_candidate_panel(run.law) for run in runs]
    start, curves, stopped = _restore_group(group_dir, engine, streams, candidates,
                                            runs, precision)
    if start:
        _save_run_checkpoints(group_dir / f"checkpoint_step_{start:06d}.pt",
                              run_dirs, engine, streams, candidates, curves,
                              stopped, start)
    dose_counts = [torch.zeros((5, 37), dtype=torch.long) for _ in runs]
    if curves[0]:
        dose_counts = [torch.tensor(curve[-1]["dose_selected_by_slot_sum"])
                       for curve in curves]
    if start >= steps or all(stopped):
        return {"group": _group_identity(runs), "last_step": start,
                "already_complete": True}
    for run, directory in zip(runs, run_dirs, strict=True):
        _write_progress(directory / "progress.log", f"START step={start} target={steps} "
                        f"device={device.type} precision={precision}")
    started = time.monotonic()
    training_seconds = 0.0
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
    preview_states = [stream.state() for stream in streams]
    preview_batches = [stream.draw_batch() for stream in streams]
    if start > 0:
        for stream, state in zip(streams, preview_states, strict=True):
            stream.restore(state)
    if start == 0 and not curves[0]:
        selections = [_selection(batch, run, 0, device) for batch, run
                      in zip(preview_batches, runs, strict=True)]
        with torch.no_grad():
            outputs = engine.forward(torch.stack([batch.records for batch in preview_batches]),
                                     torch.stack([batch.lengths for batch in preview_batches]))
            losses, details = grouped_loss(outputs, preview_batches, selections,
                                           dual=runs[0].dual)
        for stream, state in zip(streams, preview_states, strict=True):
            stream.restore(state)
        for index, run in enumerate(runs):
            row = _audit_record(engine.model_at(index), run, candidates[index],
                                streams[index], device, 0, float(losses[index]),
                                details[index], dose_counts[index], smoke=smoke,
                                counts_path=run_dirs[index] / "exposure_counts_step_000000.npz")
            if run.dual and row["A_local_history_accuracy"] != {
                    "correct": 1555, "total": 1555}:
                raise ValueError("r11 exact A erosion start differs on local histories")
            if run.dual:
                whole = a_accuracy(engine.model_at(index), device, smoke=False)
                if whole["vector"]["correct"] != whole["vector"]["total"]:
                    raise ValueError("r11 exact A erosion start differs on legal boards")
            curves[index].append(row)
            write_json(run_dirs[index] / "audit_step_000000.json", row)
            _write_progress(run_dirs[index] / "progress.log",
                            f"CHECKPOINT step=0 B_loss={details[index]['B']:.6f} "
                            f"KL={row['audit']['natural_excess_KL_bits']:.6f} "
                            f"audit_s={row['audit']['elapsed_seconds']:.2f}")
        _save_group(group_dir / "checkpoint_step_000000.pt", engine, streams,
                    candidates, runs, curves, stopped, 0, precision)
        _save_run_checkpoints(group_dir / "checkpoint_step_000000.pt", run_dirs,
                              engine, streams, candidates, curves, stopped, 0)
    last_step = start
    current_batches = list(preview_batches)
    for step in range(start + 1, steps + 1):
        update_started = time.monotonic()
        current_batches = [batch if stopped[index] else stream.draw_batch()
                           for index, (batch, stream) in enumerate(
                               zip(current_batches, streams, strict=True))]
        for index, batch in enumerate(current_batches):
            if not stopped[index]:
                _observe(candidates[index], batch)
        selections = [_selection(batch, run, step, device) if not stopped[index] else None
                      for index, (batch, run) in enumerate(
                          zip(current_batches, runs, strict=True))]
        active = torch.tensor([not value for value in stopped], device=device)
        losses, details = engine.update(current_batches, selections, active,
                                        precision=precision)
        for index, batch in enumerate(current_batches):
            if not stopped[index]:
                dose_counts[index] += _dose_counts(batch.sums, selections[index])
        if device.type == "cuda":
            torch.cuda.synchronize()
        training_seconds += time.monotonic() - update_started
        last_step = step
        if runs[0].dual and step in EROSION_READOUTS:
            for index, run in enumerate(runs):
                if stopped[index]:
                    continue
                row = _erosion_readout(engine.model_at(index), device, step, details[index])
                write_json(run_dirs[index] / f"erosion_step_{step:06d}.json", row)
                score = row["A_board_accuracy"]["vector"]
                _write_progress(run_dirs[index] / "progress.log",
                                f"EROSION_READOUT step={step} A_vector="
                                f"{score['correct']}/{score['total']}")
        audit_step = (step == steps if smoke else step in AUDITS)
        if audit_step:
            for index, run in enumerate(runs):
                if stopped[index]:
                    continue
                row = _audit_record(engine.model_at(index), run, candidates[index],
                                    streams[index], device, step, losses[index],
                                    details[index], dose_counts[index], smoke=smoke,
                                    counts_path=run_dirs[index] /
                                    f"exposure_counts_step_{step:06d}.npz")
                if step == 5000:
                    row["futility"] = _futility(curves[index][0], row, run)
                    stopped[index] = row["futility"]["stop"]
                curves[index].append(row)
                write_json(run_dirs[index] / f"audit_step_{step:06d}.json", row)
            # Persist the decision before writing the progress lines: a resumed
            # process cannot silently reverse a recorded futility stop.
            _save_group(group_dir / f"checkpoint_step_{step:06d}.pt", engine,
                        streams, candidates, runs, curves, stopped, step, precision)
            _save_run_checkpoints(group_dir / f"checkpoint_step_{step:06d}.pt",
                                  run_dirs, engine, streams, candidates,
                                  curves, stopped, step)
            for index, run in enumerate(runs):
                if curves[index][-1]["step"] != step:
                    continue
                row = curves[index][-1]
                _write_progress(run_dirs[index] / "progress.log",
                                f"CHECKPOINT step={step} B_loss={row['train_parts']['B']:.6f} "
                                f"KL={row['audit']['natural_excess_KL_bits']:.6f} "
                                f"A_vector={row['A_accuracy']:.6f} "
                                f"audit_s={row['audit']['elapsed_seconds']:.2f}")
                if stopped[index]:
                    _write_progress(run_dirs[index] / "progress.log",
                                    "FUTILITY_STOP step=5000")
            if all(stopped):
                break
        elif step % 250 == 0:
            for index, run in enumerate(runs):
                if not stopped[index]:
                    _write_progress(run_dirs[index] / "progress.log",
                                    f"PROGRESS step={step} B_loss={details[index]['B']:.6f}")
    elapsed = time.monotonic() - started
    summaries = []
    for index, run in enumerate(runs):
        final = curves[index][-1]
        summary = {"run": run.name, "last_step": final["step"],
                   "group_last_step": last_step, "futility_stop": stopped[index],
                   "elapsed_group_seconds": elapsed,
                   "group_updates_per_second": (last_step - start) / elapsed,
                   "training_seconds": training_seconds,
                   "training_seconds_per_update": training_seconds / (last_step - start),
                   "CPU_threads": torch.get_num_threads(),
                   "worker_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   "gpu_peak_bytes": (torch.cuda.max_memory_allocated() if device.type == "cuda"
                                      else None),
                   "audit_seconds": [row["audit"]["elapsed_seconds"] for row in curves[index]],
                   "curve": [{"step": row["step"],
                              "B_loss": row["train_parts"]["B"],
                              "A_loss": row["train_parts"]["A"],
                              "natural_KL": row["audit"]["natural_excess_KL_bits"],
                              "A_vector_accuracy": row["A_accuracy"]}
                             for row in curves[index]],
                   "stream_hash": streams[index].rolling.hex(),
                   "exposure": final["exposure"],
                   "early_erosion_readouts": [json.loads(path.read_text()) for path in sorted(
                       run_dirs[index].glob("erosion_step_*.json"))],
                   "precision": precision, "device": device.type,
                   "reduced_smoke": smoke}
        write_json(run_dirs[index] / "summary.json", summary)
        summaries.append(summary)
        if not stopped[index]:
            _write_progress(run_dirs[index] / "progress.log", f"COMPLETE step={final['step']}")
    return {"group": _group_identity(runs), "runs": [run.name for run in runs],
            "last_step": last_step, "elapsed_seconds": elapsed,
            "updates_per_second": (last_step - start) / elapsed,
            "training_seconds_per_update": training_seconds / (last_step - start),
            "CPU_threads": torch.get_num_threads(),
            "gpu_peak_bytes": summaries[0]["gpu_peak_bytes"],
            "worker_max_rss_kib": summaries[0]["worker_max_rss_kib"]}


def run(runs: list[RunSpec], device: torch.device, *, output_root: Path = OUTPUT,
        smoke_steps: int = 0, precision: str = "fp32", chunk_runs: int | None = None):
    registration()
    calibration = json.loads((OUTPUT / "calibration.json").read_text())
    if not all(value for value in calibration["checks"].values()):
        raise ValueError("r11 calibration gate differs")
    if smoke_steps and output_root == OUTPUT:
        raise ValueError("r11 reduced smoke requires out-of-tree output")
    if precision not in ("fp32", "bf16") or (precision == "bf16" and
                                              device.type != "cuda"):
        raise ValueError("r11 precision differs")
    if precision == "bf16" and not smoke_steps:
        path = OUTPUT / "precision_comparison.json"
        if not path.exists():
            raise ValueError("r11 bf16 study requires the GPU comparison record")
        accepted = json.loads(path.read_text())
        if (not accepted["accepted"] or
                accepted["registration_sha256"] != sha(OUTPUT / "registration.json") or
                accepted["calibration_sha256"] != sha(OUTPUT / "calibration.json")):
            raise ValueError("r11 bf16 GPU comparison is not accepted")
    if chunk_runs is None:
        chunk_runs = EXECUTION_WIDTHS[runs[0].experiment]
    if chunk_runs < 1 or (runs[0].experiment == "erosion" and chunk_runs != 1):
        raise ValueError("r11 group width differs")
    steps = smoke_steps or 20000
    if smoke_steps and not 1 <= smoke_steps <= 1000:
        raise ValueError("r11 smoke horizon differs")
    output_root.mkdir(parents=True, exist_ok=True)
    rows = []
    for offset in range(0, len(runs), chunk_runs):
        rows.append(_run_chunk(runs[offset:offset + chunk_runs], device, output_root,
                               steps=steps, smoke=bool(smoke_steps), precision=precision))
    return rows


def _compare_numeric(left: dict, right: dict, tolerance: dict) -> dict:
    failed = []
    maximum = 0.0
    if left.keys() != right.keys():
        return {"pass": False, "maximum_absolute_difference": None,
                "failed_fields": ["field inventory"]}
    for key in left:
        a, b = left[key].detach().cpu(), right[key].detach().cpu()
        if a.shape != b.shape or not torch.isfinite(a).all() or not torch.isfinite(b).all():
            failed.append(key)
            continue
        maximum = max(maximum, float((a - b).abs().max()) if a.numel() else 0.0)
        if not torch.allclose(a, b, **tolerance):
            failed.append(key)
    return {"pass": not failed, "maximum_absolute_difference": maximum,
            "failed_fields": failed}


def _equal_discrete(left, right) -> bool:
    if isinstance(left, torch.Tensor):
        return isinstance(right, torch.Tensor) and torch.equal(left.cpu(), right.cpu())
    if isinstance(left, np.ndarray):
        return isinstance(right, np.ndarray) and np.array_equal(left, right)
    if isinstance(left, dict):
        return (isinstance(right, dict) and left.keys() == right.keys() and
                all(_equal_discrete(left[key], right[key]) for key in left))
    return left == right


def _engine_run_state(engine: GroupEngine, index: int) -> dict:
    return {"parameters": {key: value[index] for key, value in engine.parameters.items()},
            "updates": int(engine.optimizer.steps[index]),
            "first": {key: value[index] for key, value in engine.optimizer.first.items()},
            "second": {key: value[index] for key, value in engine.optimizer.second.items()},
            "parameter_steps": {key: int(value[index])
                                for key, value in engine.optimizer.parameter_steps.items()},
            "buffers": {key: value[index].cpu() for key, value in engine.buffers.items()}}


def _ordinary_run_state(model, optimizer) -> dict:
    parameters = dict(model.named_parameters())
    result = {"parameters": parameters, "first": {}, "second": {},
              "parameter_steps": {}, "buffers": dict(model.named_buffers())}
    for key, value in parameters.items():
        state = optimizer.state.get(value, {})
        result["first"][key] = state.get("exp_avg", torch.zeros_like(value))
        result["second"][key] = state.get("exp_avg_sq", torch.zeros_like(value))
        result["parameter_steps"][key] = int(state.get("step", 0))
    result["updates"] = max(result["parameter_steps"].values())
    return result


def _compare_training(left: dict, right: dict, left_stream, right_stream,
                      left_dose, right_dose, left_seen, right_seen,
                      *, exact_restore: bool = False) -> dict:
    tolerance = {"atol": 0., "rtol": 0.} if exact_restore else None
    parameters = _compare_numeric(left["parameters"], right["parameters"],
                                  tolerance or EQUIVALENCE_TOLERANCE["parameters"])
    moments = {name: _compare_numeric(left[name], right[name],
                                     tolerance or EQUIVALENCE_TOLERANCE["optimizer_moments"])
               for name in ("first", "second")}
    exact = {"updates": left["updates"] == right["updates"],
             "parameter_steps": _equal_discrete(left["parameter_steps"], right["parameter_steps"]),
             "buffers": _equal_discrete(left["buffers"], right["buffers"]),
             "streams_and_exposures": _equal_discrete(left_stream.state(), right_stream.state()),
             "dose_counts": _equal_discrete(left_dose, right_dose),
             "tracked_unseen": _equal_discrete(left_seen, right_seen)}
    return {"pass": parameters["pass"] and all(row["pass"] for row in moments.values())
            and all(exact.values()), "parameters": parameters,
            "optimizer_moments": moments, "exact_state": exact}


def _difference_fields(left: dict, right: dict) -> dict:
    """Per-parameter differences, including a gradient that is absent on one side."""
    if left.keys() != right.keys():
        raise ValueError("r11 comparison trace field inventory differs")
    result = {}
    for key in left:
        a, b = left[key], right[key]
        if a is None or b is None:
            result[key] = {"left_absent": a is None, "right_absent": b is None,
                           "maximum_absolute_difference": None,
                           "difference_norm": None}
            continue
        a, b = a.detach().float().cpu(), b.detach().float().cpu()
        if a.shape != b.shape or not torch.isfinite(a).all() or not torch.isfinite(b).all():
            raise ValueError("r11 comparison trace tensor differs")
        difference = a - b
        result[key] = {"maximum_absolute_difference": float(difference.abs().max()),
                       "difference_norm": float(difference.square().sum().sqrt()),
                       "left_norm": float(a.square().sum().sqrt()),
                       "right_norm": float(b.square().sum().sqrt())}
    return result


def _hard_a_difference(left: torch.Tensor, right: torch.Tensor,
                       active: torch.Tensor) -> dict:
    """Compare the executed hard answers, excluding all padded episode rounds."""
    a, b, active = left.detach().float().cpu(), right.detach().float().cpu(), active.cpu()
    if a.shape != b.shape or a.shape[:-2] != active.shape:
        raise ValueError("r11 hard-A comparison dimensions differ")
    values_a, indices_a = a.topk(2, dim=-1)
    values_b, indices_b = b.topk(2, dim=-1)
    disagreements = (indices_a[..., 0] != indices_b[..., 0]) & active[..., None]
    rows = []
    for episode, round_index, slot in disagreements.nonzero().tolist():
        position = (episode, round_index, slot)
        row = {"episode": episode, "round": round_index, "slot": slot}
        for label, values, indices in (("left", values_a, indices_a),
                                       ("right", values_b, indices_b)):
            row[label] = {"top_two_classes": indices[position].tolist(),
                          "top_two_logits": values[position].tolist(),
                          "margin": float(values[position][0] - values[position][1])}
        rows.append(row)
    return {"active_rounds": int(active.sum()), "active_slot_answers": int(active.sum()) * 5,
            "disagreeing_rounds": int(disagreements.any(-1).sum()),
            "disagreeing_slot_answers": len(rows), "disagreements": rows,
            "minimum_active_margin": {
                label: float((values[..., 0] - values[..., 1])[active].min())
                for label, values in (("left", values_a), ("right", values_b))}}


def verify_equivalence(device: torch.device, output_root: Path, *,
                       batch_size=256, steps=8, restore_step=3,
                       trace_erosion: bool = False) -> dict:
    """Check registered widths, or trace the earlier width-three erosion comparison."""
    registration()
    if not 0 < restore_step < steps:
        raise ValueError("r11 equivalence restore step must be nonzero and precede the endpoint")
    output_root.mkdir(parents=True, exist_ok=True)
    report_path = output_root / (
        f"erosion_trace_{device.type}.json" if trace_erosion else f"verification_{device.type}.json")
    if report_path.exists():
        raise ValueError("r11 equivalence result already exists")
    groups = {
        "rarity": [RunSpec("rarity", arm, "original", 0)
                   for arm in ("uniform", "cutoff", "decoy")],
        "dose": [RunSpec("dose", f"dose{dose}", "original", 0) for dose in (1, 10, 100)],
        "erosion": [RunSpec("erosion", "b_only", "original", 0)],
    }
    if trace_erosion:
        groups = {"erosion": [RunSpec("erosion", "b_only", "original", 0),
                              RunSpec("erosion", "a_plus_b", "original", 0),
                              RunSpec("erosion", "b_only", "original", 1)]}
    tables = BoardTables(device)
    results = {}
    trace = []
    started = time.monotonic()
    for experiment, runs in groups.items():
        group = GroupEngine(runs, device)
        singles = [GroupEngine([run], device) for run in runs]
        width = len(runs)
        ordinary = [group.model_at(index).train() for index in range(width)]
        optimizers = [torch.optim.AdamW(model.parameters(), lr=.003, weight_decay=.01,
                                       foreach=False, fused=False) for model in ordinary]

        def streams():
            return [DeviceStream(tables, run.seed, run.law, run.draw,
                                 batch=batch_size, rounds=8) for run in runs]

        group_streams, single_streams, ordinary_streams = streams(), streams(), streams()
        candidates = [_candidate_panel(run.law) for run in runs]
        single_candidates = [_candidate_panel(run.law) for run in runs]
        ordinary_candidates = [_candidate_panel(run.law) for run in runs]
        counts = {name: [torch.zeros((5, 37), dtype=torch.long) for _ in runs]
                  for name in ("group", "single", "ordinary", "restored")}
        resumed = None
        restored_streams, restored_candidates = [], []
        for step in range(1, steps + 1):
            batches = [stream.draw_batch() for stream in group_streams]
            selected = [_selection(row, run, step, device)
                        for row, run in zip(batches, runs, strict=True)]
            if trace_erosion:
                with torch.no_grad():
                    output = group.forward(torch.stack([row.records for row in batches]),
                                           torch.stack([row.lengths for row in batches]))
                    reference = ordinary[0](batches[0].records, batches[0].lengths,
                                            return_all=True)
                trace_row = {"update": step, "before_update": {
                    "parameters": _difference_fields(
                        {key: value[0] for key, value in group.parameters.items()},
                        dict(ordinary[0].named_parameters())),
                    "hard_A": _hard_a_difference(output[1][0], reference[1], batches[0].active)}}
            group.update(batches, selected, torch.ones(width, dtype=torch.bool, device=device))
            for index, row in enumerate(batches):
                _observe(candidates[index], row)
                counts["group"][index] += _dose_counts(row.sums, selected[index])
            for index, run in enumerate(runs):
                row = single_streams[index].draw_batch()
                selection = _selection(row, run, step, device)
                singles[index].update([row], [selection],
                                      torch.ones(1, dtype=torch.bool, device=device))
                _observe(single_candidates[index], row)
                counts["single"][index] += _dose_counts(row.sums, selection)
                row = ordinary_streams[index].draw_batch()
                if trace_erosion and not torch.equal(row.records, batches[index].records):
                    raise ValueError("r11 comparison trace records are not paired")
                selection = _selection(row, run, step, device)
                optimizers[index].zero_grad(set_to_none=True)
                output = ordinary[index](row.records, row.lengths, return_all=True)
                loss, _ = grouped_loss(tuple(value[None] for value in output), [row],
                                        [selection], dual=run.dual)
                loss.sum().backward()
                optimizers[index].step()
                _observe(ordinary_candidates[index], row)
                counts["ordinary"][index] += _dose_counts(row.sums, selection)
            if trace_erosion:
                trace_row["after_update_gradients"] = _difference_fields(
                    {key: None if value.grad is None else value.grad[0]
                     for key, value in group.parameters.items()},
                    {key: value.grad for key, value in ordinary[0].named_parameters()})
                trace.append(trace_row)
            if resumed is not None:
                rows = [stream.draw_batch() for stream in restored_streams]
                selections = [_selection(row, run, step, device)
                              for row, run in zip(rows, runs, strict=True)]
                resumed.update(rows, selections, torch.ones(width, dtype=torch.bool, device=device))
                for index, row in enumerate(rows):
                    _observe(restored_candidates[index], row)
                    counts["restored"][index] += _dose_counts(row.sums, selections[index])
            if step == restore_step:
                directory = output_root / f"verification_{device.type}_{experiment}"
                directory.mkdir()
                curves = [[{"step": step, "dose_selected_by_slot_sum": value.tolist()}]
                          for value in counts["group"]]
                path = directory / f"checkpoint_step_{step:06d}.pt"
                _save_group(path, group, group_streams, candidates, runs, curves,
                            [False] * width, step, "fp32")
                resumed = GroupEngine(runs, device)
                restored_streams = streams()
                restored_candidates = [_candidate_panel(run.law) for run in runs]
                restored_step, saved, stopped = _restore_group(
                    directory, resumed, restored_streams, restored_candidates, runs, "fp32")
                if restored_step != step or any(stopped):
                    raise ValueError("r11 nonzero verification checkpoint differs")
                counts["restored"] = [torch.tensor(row[-1]["dose_selected_by_slot_sum"])
                                       for row in saved]
        rows = {}
        for index, run in enumerate(runs):
            baseline = _engine_run_state(group, index)
            seen = candidates[index].seen
            rows[run.name] = {
                "grouped_vs_independent": _compare_training(
                    baseline, _engine_run_state(singles[index], 0),
                    group_streams[index], single_streams[index], counts["group"][index],
                    counts["single"][index], seen, single_candidates[index].seen),
                "grouped_vs_ordinary_AdamW": _compare_training(
                    baseline, _ordinary_run_state(ordinary[index], optimizers[index]),
                    group_streams[index], ordinary_streams[index], counts["group"][index],
                    counts["ordinary"][index], seen, ordinary_candidates[index].seen),
                "uninterrupted_vs_nonzero_restore": _compare_training(
                    baseline, _engine_run_state(resumed, index),
                    group_streams[index], restored_streams[index], counts["group"][index],
                    counts["restored"][index], seen, restored_candidates[index].seen,
                    exact_restore=True),
            }
        results[experiment] = rows
    passed = all(comparison["pass"] for rows in results.values()
                 for row in rows.values() for comparison in row.values())
    report = {"pass": passed, "status": "PASS" if passed else "FAIL",
              "device": device.type, "precision": "float32", "width": max(map(len, groups.values())),
              "execution_widths": {key: len(value) for key, value in groups.items()},
              "batch": batch_size, "rounds": 8, "updates": steps,
              "restored_checkpoint_update": restore_step,
              "tolerances": EQUIVALENCE_TOLERANCE, "results": results,
              "restoration_tolerance": "exact",
              "registration_sha256": sha(OUTPUT / "registration.json"),
              "elapsed_seconds": time.monotonic() - started}
    if trace_erosion:
        report["trace"] = {"run": "erosion_b_only_original_seed0", "updates": trace,
                           "comparison": "width-three forward versus direct ordinary AdamW",
                           "gradient_observation": "after backward and optimizer update; gradients retained",
                           "purpose": "diagnostic only; not registered study execution"}
    write_json(report_path, report)
    print(f"r11 {device.type} widths {report['execution_widths']} / AdamW / "
          f"exact nonzero-restore: {report['status']}",
          flush=True)
    return report


def compare_precision(fp32_root: Path, bf16_root: Path) -> dict:
    """Gate bf16 by paired 1,000-update GPU curves, never by CPU evidence."""
    registration()
    names = [run.name for group in EXPERIMENTS
             for run in group_runs(group, smoke=True)]
    rows = {}
    accepted = True
    for name in names:
        paths = {precision: root / "runs" / name / "summary.json"
                 for precision, root in (("fp32", fp32_root), ("bf16", bf16_root))}
        saved = {precision: json.loads(path.read_text())
                 for precision, path in paths.items()}
        for precision, value in saved.items():
            if (value["precision"] != precision or value["device"] != "cuda"
                    or value["last_step"] != 1000 or not value["reduced_smoke"]
                    or [row["step"] for row in value["curve"]] != [0, 1000]):
                raise ValueError("r11 precision comparison is not a paired GPU smoke")
        differences = {}
        for key, label in (("B_loss", "B_loss_nats"),
                           ("natural_KL", "natural_KL_bits"),
                           ("A_vector_accuracy", "A_vector_accuracy")):
            differences[label] = max(abs(left[key] - right[key]) for left, right in zip(
                saved["fp32"]["curve"], saved["bf16"]["curve"], strict=True))
        passed = all(differences[key] <= limit
                     for key, limit in PRECISION_TOLERANCE.items())
        accepted &= passed
        rows[name] = {"differences": differences, "within_tolerance": passed,
                      "summary_sha256": {key: sha(path) for key, path in paths.items()}}
    report = {"accepted": accepted, "absolute_tolerances": PRECISION_TOLERANCE,
              "registration_sha256": sha(OUTPUT / "registration.json"),
              "calibration_sha256": sha(OUTPUT / "calibration.json"),
              "runs": rows, "comparison": "paired GPU smoke at updates 0 and 1000"}
    path = OUTPUT / "precision_comparison.json"
    if path.exists():
        raise ValueError("r11 precision comparison already exists")
    write_json(path, report)
    return report


def _paired_probe_changes(first: dict, last: dict, target_index: np.ndarray,
                          target_values: np.ndarray,
                          *, seed: int, oracle: dict | None = None) -> dict:
    rng = np.random.default_rng(2026100803 + seed)
    rows = {}
    for site in ("raw", "upper"):
        rows[site] = {}
        for family in ("linear", "mlp64"):
            rows[site][family] = {}
            for task in ("sum36", "category3"):
                rows[site][family][task] = []
                for slot, (before, after) in enumerate(zip(
                        first["sites"][site][family][task],
                        last["sites"][site][family][task], strict=True)):
                    truth = target_index[:, slot] if task == "sum36" else target_values[:, slot]
                    if task == "category3":
                        truth = np.where(truth <= 12, 0, np.where(truth >= 24, 2, 1))
                    old = np.asarray(before["predictions"]) == truth
                    new = np.asarray(after["predictions"]) == truth
                    difference = new.astype(float) - old.astype(float)
                    draws = rng.integers(0, len(truth), (1000, len(truth)))
                    interval = np.quantile(difference[draws].mean(1), [.025, .975]).tolist()
                    rows[site][family][task].append({
                        "slot": slot + 1, "update0_accuracy": before["accuracy"],
                        "endpoint_accuracy": after["accuracy"],
                        "gain": float(difference.mean()), "paired_CI95": interval,
                        "update0_counts": {"correct": int(old.sum()), "total": len(truth)},
                        "endpoint_counts": {"correct": int(new.sum()), "total": len(truth)},
                        "majority_floor": last["floors"][task][slot]["majority_accuracy"],
                        "shuffled_floor": last["floors"][task][slot]["shuffled_accuracy"],
                        "oracle_floor": (None if oracle is None else
                                         oracle["sites"][site][family][task][slot]["accuracy"]),
                        "fit_status": {
                            label: {key: value.get(key) for key in (
                                "converged", "n_iter", "convergence_warnings", "fit_device")}
                            for label, value in (("update0", before), ("endpoint", after))},
                        "converged": (before["converged"] and after["converged"]
                                      if family == "linear" else None),
                        "readability_gain": (interval[0] > 0 and
                                              before["converged"] and after["converged"]
                                              if family == "linear" else interval[0] > 0)})
    return rows


def _aggregate_law(law: dict) -> dict:
    cases = law["cases"]
    names = ["L_single_round", "H_single_round", *[f"N_run_{k}" for k in range(1, 9)]]
    if set(cases) != set(names) or any(cases[key]["count"] <= 0 for key in names):
        raise ValueError("r11 aggregate law case inventory or counts differ")
    panels = {}
    for panel, selected in (("short", names[:4]), ("extrapolation", names[4:])):
        count = sum(cases[key]["count"] for key in selected)
        maximum = max(cases[key]["maximum_TV"] for key in selected)
        panels[panel] = {"cases": selected, "count": count,
                         "mean_TV": sum(cases[key]["mean_TV"] * cases[key]["count"]
                                        for key in selected) / count,
                         "maximum_TV": maximum, "pass": maximum <= .02}
    maximum = max(cases[key]["maximum_TV"] for key in names)
    return {"cases": cases, "panels": panels,
            "largest_error_cases": [key for key in names if cases[key]["maximum_TV"] == maximum]}


def _aggregate_prediction_checks(audit: dict) -> dict:
    rerender = audit["rerender"]
    return {"natural_KL_bits": audit["natural_excess_KL_bits"],
            "unseen_KL_bits": audit["unseen_excess_KL_bits"],
            "unseen_count": audit["unseen_count"],
            "witness_recovery": audit["mode_law"]["witness_recovery_fraction"],
            "witness_prediction_TV": audit["mode_law"]["witness_pair_mean_prediction_TV"],
            "swaps": audit["swaps"], "rerender": rerender,
            "rerender_prediction_pass": rerender["maximum_TV"] <= .02,
            "rerender_A_answer_pass": rerender["A_answer_mismatched_components"] == 0,
            "registered_rerender_pass": rerender["pass"],
            "route_damage": audit["route_damage"]}


def _aggregate_exposure(exposure: dict, selected: list) -> dict:
    total = sum(exposure["by_slot1_sum"])
    counts = np.asarray(selected, dtype=np.int64)
    if counts.shape != (5, 37) or not np.all(counts.sum(1) == counts.sum(1)[0]):
        raise ValueError("r11 aggregate dose counts differ across slots")
    rounds = int(counts.sum(1)[0])
    if not 0 <= rounds <= total:
        raise ValueError("r11 aggregate dose exceeds active rounds")
    return {"active_rounds": total, "selected_A_rounds": rounds,
            "observed_dose": rounds / total if total else None,
            "cutoff_sum_counts": {str(k): exposure["by_slot1_sum"][k] for k in (12, 13, 23, 24)},
            "decoy_sum_counts": {str(k): exposure["by_slot1_sum"][k] for k in (10, 16, 20, 27)},
            "dose_selected_by_slot_sum": selected,
            "complete_rendering_counts": exposure["complete_rendering_counts"],
            "saved_r9_rendering_exposures": exposure["r9_failure_renderings"]}


def _aggregate_dose_counts(true_sums, head_sums, signatures) -> dict:
    true_sums, head_sums, signatures = map(np.asarray, (true_sums, head_sums, signatures))
    if (true_sums.ndim != 1 or true_sums.shape != head_sums.shape
            or true_sums.shape != signatures.shape or not len(true_sums)
            or not all(np.isfinite(v).all() for v in (true_sums, head_sums, signatures))
            or not np.isin(signatures, (0, 1, 2)).all()):
        raise ValueError("r11 dose decomposition arrays differ")
    truth = np.where(true_sums <= 12, 0, np.where(true_sums >= 24, 2, 1))
    head = np.where(head_sums <= 12, 0, np.where(head_sums >= 24, 2, 1))
    a_wrong, b_wrong = head != truth, signatures != truth
    return {"A_head_category_errors": int(a_wrong.sum()), "B_signature_errors": int(b_wrong.sum()),
            "B_errors_with_correct_A_category": int((b_wrong & ~a_wrong).sum()), "boards": len(truth)}


@torch.no_grad()
def _aggregate_dose_replay(folder: Path, expected_signature: int) -> dict:
    """Post-hoc CPU replay of the saved 20k model, with no fitting or updates."""
    if torch.get_num_threads() != 1:
        raise ValueError("r11 dose replay requires one CPU thread")
    started = time.monotonic()
    path = folder / "checkpoint_step_020000.pt"
    digest = sha(path)
    if path.with_suffix(".sha256").read_text().strip() != digest:
        raise ValueError("r11 dose replay checkpoint digest differs")
    saved = torch.load(path, map_location="cpu", weights_only=False)
    if (saved["step"] != 20000 or saved["futility_stop"]
            or not identity_matches(saved["registration_sha256"], sha(OUTPUT / "registration.json"))
            or not identity_matches(saved["calibration_sha256"], sha(OUTPUT / "calibration.json"))):
        raise ValueError("r11 dose replay checkpoint authority differs")
    with torch.random.fork_rng(devices=[]):
        model = JaggedNetwork(dual=False).cpu().float().eval()
    model.load_state_dict(saved["model"], strict=True)
    model.requires_grad_(False)
    boards = enumerate_boards()
    indices = np.arange(len(boards.boards), dtype=np.int64)
    records = _census_records(boards, indices, render_offset=0)
    from recombination_promotion.oldgame_ext.memory import VALUES
    truth = np.asarray(boards.boards, dtype=np.int64)[:, 0]
    low, high = (int(np.flatnonzero(truth == value)[0]) for value in (0, 36))
    answers, raw, head_sums = [], [], []
    with torch.autocast("cpu", enabled=False):
        for start in range(0, len(records), 512):
            _, a, r = model.round_interfaces(torch.from_numpy(records[start:start + 512]))
            answers.append(a)
            raw.append(r)
            logits = model.raw_sum_head(r).reshape(-1, 5, len(VALUES))
            head_sums.append(np.asarray(VALUES)[logits[:, 0].argmax(-1).numpy()])
        answers, raw = torch.cat(answers), torch.cat(raw)
        contexts = [model.upper_step(answers[i:i + 1], raw[i:i + 1])[1] for i in (low, high)]
        predictions = []
        for context in contexts:
            rows = []
            for start in range(0, len(records), 512):
                end = min(start + 512, len(records))
                logits, _ = model.upper_step(answers[start:end], raw[start:end],
                                              context.expand(end - start, -1))
                rows.append(torch.softmax(logits, -1).numpy())
            predictions.append(np.concatenate(rows))
    counts = _aggregate_dose_counts(truth, np.concatenate(head_sums),
                                    r9.signature(np.stack(predictions, axis=1)))
    if counts["B_signature_errors"] != expected_signature:
        raise ValueError("r11 dose replay signature differs from saved census")
    if not all(torch.equal(value, saved["model"][key]) for key, value in model.state_dict().items()):
        raise ValueError("r11 dose replay changed source parameters")
    if sha(path) != digest:
        raise ValueError("r11 dose replay source checkpoint changed")
    return {**counts, "status": "POST_HOC_CPU_CHECKPOINT_REPLAY",
            "replay": {"checkpoint": str(path), "checkpoint_sha256": digest, "step": 20000,
                       "registration_sha256": saved["registration_sha256"],
                       "calibration_sha256": saved["calibration_sha256"],
                       "device": "cpu", "CPU_threads": 1, "precision": "float32",
                       "rendering": 0, "record_sha256": hashlib.sha256(records.tobytes()).hexdigest(),
                       "anchor_board_ids": {"L": low, "H": high}, "parameter_updates": 0,
                       "source_parameters_unchanged": True, "elapsed_seconds": time.monotonic() - started}}


def _aggregate_selected_readings(sections: dict, review: str) -> dict:
    original = [row for group in sections.values() for row in group.values() if row["law"] == "original"]
    short_failures = sum(not row["law_panels"]["panels"]["short"]["pass"] for row in original)
    long_maxima = sum(any(name.startswith("N_run_") and int(name[6:]) >= 3
                          for name in row["law_panels"]["largest_error_cases"]) for row in original)
    readings = {}
    for name in EXPERIMENTS:
        readings[name] = json.loads(review)["rules"]["observed_readings"][name]
    return {"selected_applicable_reading": readings,
            "original_law_panel_counts": {"runs": len(original), "short_panel_failures": short_failures,
                                           "largest_error_on_extrapolation": long_maxima},
            "corrections": [
                f"{long_maxima}/{len(original)} original-law maxima occur on N3–N8, but "
                f"{short_failures}/{len(original)} already fail L/H or N1–N2. "
                "Long-neutral extrapolation does not explain every failure.",
                "A+B largely protects A but is not exact everywhere; inspect integer board and "
                "local-history counts rather than rounded percentages. B closure is not guaranteed.",
                "A census category misread is a two-anchor B predictive-signature error, not an "
                "auxiliary A-head category error. The dose decomposition keeps them separate.",
                "Similar slot accuracies do not establish a constant answer. The B-only erosion "
                "output alphabets describe collapsed sum computations.",
                "Prediction rerender failures and A-answer rerender failures are separate; "
                "the registered conjunctive gate is unchanged.",
                "r8 versus r11 is historical evidence across different pathways, not a matched "
                "causal comparison. Objective competition is a possibility, not an established cause.",
                "A separately registered, matched neutral-history coverage study is needed before "
                "attributing the worst-case gap cleanly to board rarity; none is run here."]}


def _aggregate_markdown(report: dict) -> str:
    def number(value):
        return "not recorded" if value is None else f"{value:.9g}"

    def count(value):
        return "not applicable" if value is None else f"{value['correct']}/{value['total']}"

    def table(headers, rows):
        return ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers),
                *["| " + " | ".join(str(item) for item in row) + " |" for row in rows], ""]

    lines = ["# r11 jagged-competence aggregate", "",
             "All saved runs are retained. No retraining, probe fitting, or checkpoint selection.", "",
             "## Registered readings (verbatim)", "", report["registered_readings_verbatim"], "",
             "## Selected applicable readings and corrections", ""]
    for experiment, reading in report["interpretation"]["selected_applicable_reading"].items():
        lines.extend((f"### {experiment}", "", reading, ""))
    lines.extend([*report["interpretation"]["corrections"], ""])
    convergence = report["linear_comparison_convergence"]
    lines.extend((f"Linear comparisons converged at both endpoints: "
                  f"{convergence['converged']}/{convergence['total']} (unique runs, no duplicated 0% controls).", ""))
    for experiment in EXPERIMENTS:
        lines.extend((f"## {experiment}", ""))
        for seed in SEEDS:
            selected = [(name, row) for name, row in sorted(report[experiment].items()) if row["seed"] == seed]
            if experiment == "dose":
                selected = [(name, row) for name, row in sorted(report["rarity"].items())
                            if row["seed"] == seed and row["arm"] == "uniform"] + selected
            if not selected:
                continue
            lines.extend((f"### Seed {seed} — original and equal laws", "",
                          "Census category errors are B-signature errors; undefined under equal law. "
                          "TV failures are still measured under equal law.", ""))
            if experiment == "dose":
                lines.extend(("The uniform rarity rows are the shared 0% dose controls, not additional runs.", ""))
            lines.extend(table(
                ["Run", "Endpoint", "Census signature errors r0/r1/r2/r3", "TV failures r0/r1/r2/r3",
                 "Saved r9 signature / TV failures", "A slot counts 1–5", "A vector", "Local histories"],
                [(name, row["fixed_endpoint_label"],
                  "; ".join("undefined" if r["categorical_misreads"] is None else
                            f"{r['categorical_misreads']}/{r['boards']}" for r in row["census_renderings"]),
                  "; ".join(f"{r['above_0_02_TV']}/{r['boards']}" for r in row["census_renderings"]),
                  f"{row['board_census']['saved_r9_failed_renderings']['categorical_misreads']} / "
                  f"{row['board_census']['saved_r9_failed_renderings']['above_0_02_TV']} "
                  f"of {row['board_census']['saved_r9_failed_renderings']['count']}",
                  ", ".join(count(v) for v in row["A_components"]["per_slot"]),
                  count(row["A_components"]["vector"]), count(row["A_local_histories"]))
                 for name, row in selected]))
            lines.extend(table(
                ["Run", "Active rounds", "A-supervised rounds / observed dose", "Cutoff 12/13/23/24 counts",
                 "Decoy 10/16/20/27 counts", "Cutoff/decoy enrichment vs paired uniform"],
                [(name, row["actual_exposure"]["active_rounds"],
                  f"{row['actual_exposure']['selected_A_rounds']} / {number(row['actual_exposure']['observed_dose'])}",
                  str(row["actual_exposure"]["cutoff_sum_counts"]), str(row["actual_exposure"]["decoy_sum_counts"]),
                  str(row["actual_exposure"].get("enrichment_vs_paired_uniform", "not applicable")))
                 for name, row in selected]))
            lines.extend(("Law cells below are mean/max TV with the number of scored predictions. "
                          "Short = L/H and N1–N2; extrapolation = N3–N8.", ""))
            names = ["L_single_round", "H_single_round", *[f"N_run_{k}" for k in range(1, 9)]]
            lines.extend(table(["Run", *names, "Short mean / max / pass", "Extrapolation mean / max / pass"],
                [(name, *[f"{number(row['law_panels']['cases'][key]['mean_TV'])}/"
                          f"{number(row['law_panels']['cases'][key]['maximum_TV'])} "
                          f"(n={row['law_panels']['cases'][key]['count']})" for key in names],
                  *[f"{number(row['law_panels']['panels'][key]['mean_TV'])} / "
                    f"{number(row['law_panels']['panels'][key]['maximum_TV'])} / "
                    f"{row['law_panels']['panels'][key]['pass']}" for key in ("short", "extrapolation")])
                 for name, row in selected]))
            lines.extend(table(
                ["Run", "Natural / unseen KL bits (unseen n)", "Witness recovery / prediction TV",
                 "Failed registered bars", "Rerender prediction TV / pass", "A rerender differences / pass"],
                [(name, f"{number(row['prediction_checks']['natural_KL_bits'])} / "
                        f"{number(row['prediction_checks']['unseen_KL_bits'])} "
                        f"(n={row['prediction_checks']['unseen_count']})",
                  f"{number(row['prediction_checks']['witness_recovery'])} / "
                  f"{number(row['prediction_checks']['witness_prediction_TV'])}",
                  ", ".join(key for key, passed in row["B_criteria"].items() if not passed) or "none",
                  f"{number(row['prediction_checks']['rerender']['maximum_TV'])} / "
                  f"{row['prediction_checks']['rerender_prediction_pass']}",
                  f"{row['prediction_checks']['rerender']['A_answer_mismatched_components']} / "
                  f"{row['prediction_checks']['rerender_A_answer_pass']}") for name, row in selected]))
            lines.extend(table(["Run", "Swap case", "Count", "Mean / max TV"],
                [(name, case, value["count"], f"{number(value['mean_TV'])} / {number(value['maximum_TV'])}")
                 for name, row in selected for case, value in row["B_swaps"]["cases"].items()]))
            lines.extend(("Probe tables use frozen saved predictions. Oracle is the calibrated "
                          "exact-A control, not a theoretical floor. MLP fits have a fixed budget "
                          "and make no convergence claim. Paired intervals retain the original seed and method.", ""))
            lines.extend(table(
                ["Run", "Carrier / reader / target / slot", "Update 0 / endpoint", "Gain [paired CI95]",
                 "Majority / shuffled / oracle", "Convergence 0 / endpoint (iterations, warnings)"],
                [(name, f"{site} / {family} / {task} / {p['slot']}",
                  f"{number(p['update0_accuracy'])} / {number(p['endpoint_accuracy'])}",
                  f"{number(p['gain'])} [{number(p['paired_CI95'][0])}, {number(p['paired_CI95'][1])}]",
                  f"{number(p['majority_floor'])} / {number(p['shuffled_floor'])} / {number(p['oracle_floor'])}",
                  " / ".join(f"{p['fit_status'][phase]['converged']} "
                             f"({p['fit_status'][phase]['n_iter']}, {p['fit_status'][phase]['convergence_warnings']})"
                             for phase in ("update0", "endpoint")))
                 for name, row in selected for site, families in row["probe_changes"].items()
                 for family, tasks in families.items() for task, probes in tasks.items() for p in probes]))
            lines.extend(table(["Run", "Update", "B loss", "A loss", "Natural KL", "A vector accuracy"],
                [(name, point["step"], number(point["B_loss"]), number(point["A_loss"]),
                  number(point["natural_KL"]), number(point["A_vector_accuracy"]))
                 for name, row in selected for point in row["B_A_curve"]]))
            early = [(name, p["step"], ", ".join(count(v) for v in p["A_board_accuracy"]["per_slot"]),
                      count(p["A_board_accuracy"]["vector"]), str(p["train_parts"]))
                     for name, row in selected for p in row["early_erosion_readouts"]]
            if early:
                lines.extend(table(["Run", "Early update", "A slot counts", "A vector", "Loss parts"], early))
    lines.extend(("## Dose category decomposition", "",
                  "A-head category errors and B predictive-signature errors are distinct measurements. "
                  "Original-law counts come from a post-hoc, one-thread float32 CPU replay of the "
                  "saved 20k checkpoints on all 24,435 boards in registered rendering 0. "
                  "No parameter updates or fits occur; seed 0 is checked against analysis's independent replay. "
                  "Equal-law B signatures are undefined.", ""))
    lines.extend(table(["Run", "A-head slot-1 category errors", "B-signature errors", "B errors with correct A category", "Source"],
        [(name, str(row["A_head_category_errors"]), row["B_signature_errors"],
          str(row["B_errors_with_correct_A_category"]), row["status"])
         for name, row in report["dose_decomposition"].items()]))
    lines.extend(("## Original-law B-only erosion output alphabets", "",
                  "Values are in twelfths. These are not one constant answer.", ""))
    lines.extend(table(["Seed", "Alphabet", "Source"],
        [(seed, str(row["twelfths"]), row["source"]) for seed, row in report["erosion_B_only_alphabets"].items()]))
    lines.extend(("## Missing runs", "", ", ".join(report["missing_runs"]) if report["missing_runs"] else "None", ""))
    return "\n".join(lines)


def aggregate(device: torch.device) -> dict:
    del device  # Scoring uses saved exact audit rows, not a new network evaluation.
    # The registered training script remains historical authority. Report-only
    # edits do not reissue that registration or authorize another training run.
    registered = json.loads((OUTPUT / "registration.json").read_text())
    identities = source_identities()
    if (registered["runs"] != [run.name for run in all_runs()]
            or registered["source_sha256"].keys() != identities.keys()
            or any(registered["source_sha256"][key] != identities[key]
                   for key in identities if key != "script")):
        raise ValueError("r11 aggregate non-report authority differs")
    if not (OUTPUT / "calibration.json").exists():
        raise ValueError("r11 calibration missing")
    calibration = json.loads((OUTPUT / "calibration.json").read_text())
    analysis_path = OUTPUT / "analysis_specification.json"
    review = analysis_path.read_text()
    scientific_rules = json.loads(review)["rules"]
    split = json.loads((r8.OUTPUT / "probe_split.json").read_text())
    target_index = r8._probe_data(split)[1][1]
    from recombination_promotion.oldgame_ext.memory import VALUES
    target_values = np.asarray(VALUES, dtype=np.int64)[target_index]
    sections = {}
    missing = []
    for experiment in EXPERIMENTS:
        sections[experiment] = {}
        for run in (entry for entry in all_runs() if entry.experiment == experiment):
            folder = OUTPUT / "runs" / run.name
            if not (folder / "summary.json").exists():
                missing.append(run.name)
                continue
            summary = json.loads((folder / "summary.json").read_text())
            rows = [json.loads(path.read_text()) for path in sorted(
                folder.glob("audit_step_*.json"))]
            if not rows or rows[0]["step"] != 0:
                raise ValueError("r11 update-zero audit missing")
            endpoint = rows[-1]
            crossing = next((row["step"] for row in rows if row["audit"]["B_pass"]), None)
            if summary["futility_stop"]:
                label = "FUTILITY_STOP"
            elif endpoint["step"] != 20000:
                label = "INCOMPLETE"
            else:
                label = "B_PASS" if endpoint["audit"]["B_pass"] else "B_INCOMPLETE"
            sections[experiment][run.name] = {
                "seed": run.seed, "law": run.law, "arm": run.arm,
                "first_audited_B_crossing": crossing,
                "fixed_endpoint_label": label,
                "fixed_endpoint_step": endpoint["step"],
                "B_criteria": endpoint["audit"]["criteria"],
                "A_components": endpoint["A_board_accuracy"],
                "A_local_histories": endpoint["A_local_history_accuracy"],
                "B_law": endpoint["audit"]["mode_law"],
                "law_panels": _aggregate_law(endpoint["audit"]["mode_law"]),
                "B_swaps": endpoint["audit"]["swaps"],
                "prediction_checks": _aggregate_prediction_checks(endpoint["audit"]),
                "board_census": endpoint["audit"]["board_census"],
                "census_renderings": [endpoint["audit"]["board_census"]["registered_rendering"],
                                      *endpoint["audit"]["board_census"]["additional_fixed_renderings"]],
                "exposure": summary["exposure"],
                "actual_exposure": _aggregate_exposure(summary["exposure"], endpoint["dose_selected_by_slot_sum"]),
                "B_A_curve": summary["curve"],
                "early_erosion_readouts": summary.get("early_erosion_readouts", []),
                "probe_changes": _paired_probe_changes(
                    rows[0]["audit"]["probes"], endpoint["audit"]["probes"],
                    target_index, target_values, seed=run.seed, oracle=calibration["probe"]["oracle"]),
                "source_files": {"summary": sha(folder / "summary.json"),
                                 "audits": {path.name: sha(path) for path in sorted(folder.glob("audit_step_*.json"))}},
            }
    for name, row in sections["rarity"].items():
        baseline = sections["rarity"].get(f"rarity_uniform_{row['law']}_seed{row['seed']}")
        if baseline is not None:
            rates = {}
            for field in ("cutoff_sum_counts", "decoy_sum_counts"):
                total = row["actual_exposure"]["active_rounds"]
                base_total = baseline["actual_exposure"]["active_rounds"]
                rates[field] = {key: ((value / total) /
                                      (baseline["actual_exposure"][field][key] / base_total)
                                      if total and baseline["actual_exposure"][field][key] else None)
                                for key, value in row["actual_exposure"][field].items()}
            row["actual_exposure"]["enrichment_vs_paired_uniform"] = rates
    # Only the missing dose decomposition is replayed. All other audit rows
    # remain saved evidence, including analysis's attributed erosion alphabets.
    reference_dose = dict(zip((1, 10, 100), scientific_rules["seed0_joint_errors"]))
    decomposition = {}
    for name, row in sections["dose"].items():
        signature = row["census_renderings"][0]["categorical_misreads"]
        entry = {"A_head_category_errors": None, "B_signature_errors": signature,
                 "B_errors_with_correct_A_category": None, "boards": row["census_renderings"][0]["boards"],
                 "status": "UNDEFINED_EQUAL_LAW_SIGNATURE"}
        if row["law"] == "original":
            entry = _aggregate_dose_replay(OUTPUT / "runs" / name, signature)
        if row["seed"] == 0 and row["law"] == "original" and int(row["arm"][4:]) in reference_dose:
            a, b, joint = reference_dose[int(row["arm"][4:])]
            if (entry["A_head_category_errors"], entry["B_signature_errors"],
                    entry["B_errors_with_correct_A_category"]) != (a, b, joint):
                raise ValueError("r11 dose replay differs from analysis seed-0 counts")
            entry.update(reference_seed0_match=True, reference_seed0_counts=[a, b, joint], analysis_spec_sha256=sha(analysis_path))
        decomposition[name] = entry
    alphabets = [",".join(map(str, values)) for values in scientific_rules["erosion_alphabets"]]
    if len(alphabets) != 3:
        raise ValueError("r11 reviewed erosion alphabet inventory differs")
    report = {"registration_sha256": sha(OUTPUT / "registration.json"),
              "calibration_sha256": sha(OUTPUT / "calibration.json"),
              "report_script_sha256": identities["script"],
              "registered_training_script_sha256": registered["source_sha256"]["script"],
              "analysis_spec_sha256": sha(analysis_path),
              "registered_readings_verbatim": registered["claims_and_readings_verbatim"],
              "rarity": sections["rarity"], "erosion": sections["erosion"],
              "dose": sections["dose"], "missing_runs": missing,
              "interpretation": _aggregate_selected_readings(sections, review),
              "dose_decomposition": decomposition,
              "erosion_B_only_alphabets": {str(seed): {"twelfths": [int(value) for value in alphabet.split(",")],
                  "source": "independent original-law checkpoint replay", "analysis_spec_sha256": sha(analysis_path)}
                  for seed, alphabet in enumerate(alphabets)},
              "shared_zero_dose": "rarity_uniform for matching seed and law",
              "historical_context": "r8 saved raw-only results are not paired r11 outcomes"}
    linear = [probe["converged"] for group in sections.values() for row in group.values()
              for site in row["probe_changes"].values() for task in site["linear"].values() for probe in task]
    report["linear_comparison_convergence"] = {"converged": sum(linear), "total": len(linear)}
    write_json(OUTPUT / "aggregate.json", report)
    (OUTPUT / "aggregate.md").write_text(_aggregate_markdown(report))
    return {"reported_runs": sum(map(len, sections.values())), "missing_runs": len(missing)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("register", "calibrate", "run", "aggregate",
                                          "compare-precision", "verify-gpu"))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--runs", choices=EXPERIMENTS)
    parser.add_argument("--run-name", action="append", default=[])
    parser.add_argument("--output-root", type=Path, default=OUTPUT)
    parser.add_argument("--smoke-steps", type=int, default=0)
    parser.add_argument("--precision", choices=("fp32", "bf16"), default="fp32")
    parser.add_argument("--chunk-runs", type=int, default=None)
    parser.add_argument("--trace-erosion", action="store_true",
                        help="verify-gpu: trace the earlier width-three erosion comparison")
    parser.add_argument("--fp32-root", type=Path,
                        default=SMOKE / "fp32")
    parser.add_argument("--bf16-root", type=Path,
                        default=SMOKE / "bf16")
    arguments = parser.parse_args()
    device = configure(arguments.device)
    if arguments.stage == "register":
        result = register(device)
    elif arguments.stage == "calibrate":
        result = calibrate(device)
    elif arguments.stage == "aggregate":
        result = aggregate(device)
    elif arguments.stage == "compare-precision":
        result = compare_precision(arguments.fp32_root, arguments.bf16_root)
    elif arguments.stage == "verify-gpu":
        result = verify_equivalence(device, arguments.output_root,
                                    trace_erosion=arguments.trace_erosion)
    else:
        selected = group_runs(arguments.runs, smoke=bool(arguments.smoke_steps),
                              explicit=tuple(arguments.run_name))
        result = run(selected, device, output_root=arguments.output_root,
                     smoke_steps=arguments.smoke_steps, precision=arguments.precision,
                     chunk_runs=arguments.chunk_runs)
    print(json.dumps(result, sort_keys=True, default=str))
    if arguments.stage == "verify-gpu" and not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
