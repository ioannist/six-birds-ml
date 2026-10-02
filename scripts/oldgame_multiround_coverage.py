"""Registered r12 history-coverage experiment; no automatic study launch."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import time
from dataclasses import dataclass
from pathlib import Path
from recombination_promotion.public_paths import public_path, metadata_matches

import numpy as np
import torch
from torch.func import stack_module_state

from recombination_promotion.oldgame_ext import game
from recombination_promotion.oldgame_ext.memory import VALUES
from recombination_promotion.oldgame_ext.multiround import (
    A_CHECKPOINT, P, P_EQUAL, enumerate_boards, load_frozen_A,
)
from recombination_promotion.oldgame_ext.multiround_coverage import (
    ARMS, CoverageStream, coverage_loss, new_model,
)
from scripts import oldgame_multiround_jagged as r11


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/phase11/oldgame_memory/multiround/study_r12_coverage"
BULK = public_path("bulk/study_r12_coverage_bulk")
SPEC = OUTPUT / "specification.md"
AUDITS = r11.AUDITS
GROUPS = {"rarity": ("uniform", "cutoff", "decoy"), "a_target": ("a_target",),
          "a_supplied": ("a_supplied",)}
WIDTHS = {"rarity": 3, "a_target": 3, "a_supplied": 1}


@dataclass(frozen=True)
class Run:
    arm: str
    law: str
    seed: int

    @property
    def name(self):
        return f"{self.arm}_{self.law}_seed{self.seed}"

    @property
    def dual(self):
        return self.arm == "a_supplied"

    @property
    def draw(self):
        return self.arm if self.arm in ("cutoff", "decoy") else "uniform"


def all_runs():
    return [Run(arm, law, seed) for arm in ARMS for law in r11.LAWS for seed in (0, 1, 2)]


def identities():
    paths = {"design": SPEC, "script": Path(__file__),
             "module": ROOT / "src/recombination_promotion/oldgame_ext/multiround_coverage.py",
             "A_source": ROOT / A_CHECKPOINT,
             "r11_registration": r11.OUTPUT / "registration.json",
             "r11_script": Path(r11.__file__),
             "r11_module": ROOT / "src/recombination_promotion/oldgame_ext/multiround_jagged.py",
             "probes": ROOT / "src/recombination_promotion/oldgame_ext/jagged_probes.py",
             "r8_panels": r11.choice.OUTPUT / "manifest.json",
             "probe_split": r11.r8.OUTPUT / "probe_split.json",
             "r9": r11.r9.OUTPUT / "results.json"}
    return {key: r11.sha(path) for key, path in paths.items()}


def settings():
    return {"steps": 20000, "batch": 256, "rounds": 9, "lr": .003, "weight_decay": .01,
            "precision": "float32", "audits": list(AUDITS), "execution_widths": WIDTHS,
            "maximum_processes": 5, "CPU_threads_per_process": 1,
            "natural_episodes": 128, "coverage_episodes": 128, "examples_per_stratum": 8,
            "B_weights": [0.5, 0.5], "A_target_coefficient": 1,
            "linear_fit_device": "cpu", "MLP_fit_device": "audit device",
            "probe_settings": {"linear": r11.LINEAR_SETTINGS, "mlp64": r11.MLP_SETTINGS},
            "equivalence_tolerances": r11.EQUIVALENCE_TOLERANCE,
            "stream_seeds": [202610110000, 202610120000, 202610130000],
            "diagnostic_rules": {
                "version": 2, "TV_limit": .02,
                "constituent_chronology": "earliest incorrect signature through first sequence violation",
                "recurrence": "observed sequence violation, correct constituent responses through it, valid anchors",
                "empty_panels": "refused", "scope": "descriptive, not a unique causal explanation"}}


def registration():
    row = json.loads((OUTPUT / "registration.json").read_text())
    if (row["source_sha256"] != identities() or row["settings"] != settings()
            or row["runs"] != [run.name for run in all_runs()]):
        raise ValueError("r12 registration differs from executed sources or settings")
    return row


def register(device):
    if (OUTPUT / "registration.json").exists():
        return registration()
    _, source = load_frozen_A(ROOT)
    spec = SPEC.read_text()
    row = {"study": "study_r12_coverage", "specification_verbatim": spec,
           "source_sha256": identities(), "settings": settings(), "frozen_A": source,
           "runs": [run.name for run in all_runs()], "registration_device": device.type,
           "choices": [
               "Reuse the r11 network, optimizer, enrichment, probe splits and B decision functions unchanged.",
               "All arms load the same frozen exact learned-A core; raw arms mask its interface exactly.",
               "New independent stream seeds are offset by seed, law (10000), and enrichment (100); category and target streams have no enrichment offset.",
               "Fixed stratum row positions have eight examples each; boards, placements and record orders are independently drawn on the selected device.",
               "Intermediate coverage targets are unused sampler values, never training targets: only the endpoint contributes B cross-entropy.",
               "Update-zero B loss is the mean over 100 independent preview batches with streams restored afterwards. Later training losses use the preceding 100 updates.",
               "Clear-neutral tests use first-slot sums 16–20; verify single-board responses before describing errors as recurrence evidence.",
               "Failure chronology distinguishes earlier and simultaneous constituent errors. A recurrence reading requires an observed sequence violation, correct responses through that prefix and valid anchors; otherwise its cause is unresolved. Diagnostic panels must be nonempty.",
               "Raw local-memory scores refer to the unused frozen A source, not to an executed local raw-encoder carrier.",
               "Bulk checkpoint, exposure and audit paths are configurable; the repository retains summaries, registrations, calibration, logs and aggregate reports.",
               "Reduced CPU smoke probe/census panels are marked inadmissible as study endpoints; all B panels and decision functions remain unchanged.",
               "The full prompt route remains the previously audited Stage-1 route; this matched experiment trains on routed ordered records.",
           ]}
    r11.write_json(OUTPUT / "registration.json", row)
    (OUTPUT / "registration.md").write_text("# r12 registration\n\n" + spec +
        "\n## Implementation choices\n\n" + "\n".join(f"- {s}" for s in row["choices"]) + "\n")
    return row


class Engine(r11.GroupEngine):
    def __init__(self, runs, device):
        if len({run.dual for run in runs}) != 1:
            raise ValueError("r12 execution batch mixes supplied and masked interfaces")
        self.runs, self.device = runs, device
        self.models = [new_model(run.seed, run.arm, ROOT).to(device) for run in runs]
        self.parameters, self.buffers = stack_module_state(self.models)
        self.optimizer = r11.StackedAdamW(self.parameters, len(runs))

    def update(self, batches, active):
        self.optimizer.zero_grad()
        output = self.forward(torch.stack([b.records for b in batches]),
                              torch.stack([b.lengths for b in batches]))
        loss, details = coverage_loss(output, batches, [run.arm for run in self.runs])
        if not torch.isfinite(loss).all():
            raise ValueError("r12 non-finite training loss")
        (loss * active).sum().backward()
        used = torch.tensor([run.arm == "a_target" for run in self.runs], device=self.device)
        self.optimizer.step(active, {key: used for key in self.parameters
                                     if key.startswith("raw_sum_head.")})
        return details

    def model_at(self, index, *, cpu=False):
        model = new_model(self.runs[index].seed, self.runs[index].arm, ROOT)
        model.load_state_dict({key: value[index].detach().cpu()
                               for key, value in self.parameters.items()}, strict=True)
        return model.to("cpu" if cpu else self.device).eval()


def futility(first, current, run):
    floor = math.log(2) * 1.5 if run.law == "original" else -sum(p * math.log(p) for p in P_EQUAL)
    gap = max(first["train_parts"]["B"] - floor, 0)
    closed = ((first["train_parts"]["B"] - current["train_parts"]["B"]) / gap if gap else 0)
    kl = first["audit"]["natural_excess_KL_bits"]
    kl_closed = (kl - current["audit"]["natural_excess_KL_bits"]) / kl if kl else 0
    improved = run.arm == "a_target" and current["A_accuracy"] > first["A_accuracy"]
    return {"B_gap_closed": closed, "natural_KL_gap_closed": kl_closed,
            "supervised_A_improved": improved,
            "stop": closed < .1 and kl_closed < .1 and not improved}


def _candidate(law):
    return r11._candidate_panel(law)


def calibration(device):
    registration()
    destination = OUTPUT / "calibration.json"
    if destination.exists():
        saved = json.loads(destination.read_text())
        if saved["registration_sha256"] != r11.sha(OUTPUT / "registration.json"):
            raise ValueError("r12 calibration registration differs")
        return saved
    tables = r11.BoardTables(device)
    b_rows, sampler, unseen = {}, {}, {}
    for law in r11.LAWS:
        streams = {draw: CoverageStream(tables, 17, law, draw)
                   for draw in ("uniform", "cutoff", "decoy")}
        candidate = _candidate(law)
        for _ in range(128):
            batches = {draw: stream.draw_batch() for draw, stream in streams.items()}
            reference = batches["uniform"]
            for batch in batches.values():
                if not torch.equal(reference.categories, batch.categories) or not \
                        torch.equal(reference.targets, batch.targets):
                    raise ValueError("r12 paired target stream differs")
                totals = torch.zeros_like(batch.sums)
                masses = torch.tensor(game.MASSES, device=device)
                for at in range(4):
                    totals.scatter_add_(-1, batch.records[:, :, at, :1],
                                        masses[batch.records[:, :, at, 1:2]])
                categories = torch.where(totals[..., 0] <= 12, 0,
                                         torch.where(totals[..., 0] >= 24, 2, 1))
                if not torch.equal(categories[batch.active], batch.categories[batch.active]) or not \
                        torch.equal(totals[batch.active], batch.sums[batch.active]):
                    raise ValueError("r12 record-derived board category differs")
                if int(batch.active.sum()) != 1856 or int(batch.b_active.sum()) != 1280:
                    raise ValueError("r12 endpoint or active-round counts differ")
            r11._observe(candidate, reference)
        sampler[law] = {}
        for draw, stream in streams.items():
            if not torch.equal(stream.stratum_exposure, torch.full_like(stream.stratum_exposure, 1024)):
                raise ValueError("r12 stratum exposure differs")
            frequencies = stream.endpoint_targets.float() / stream.stratum_exposure[..., None]
            exact = frequencies.new_tensor(list(map(float, P_EQUAL)) if law == "equal" else
                                            [list(map(float, row)) for row in P])
            if law == "original":
                exact = exact[:, None]
            if float((frequencies - exact).abs().max()) > .075:
                raise ValueError("r12 conditional endpoint target frequencies differ")
            sampler[law][draw] = {"stratum_endpoints": stream.stratum_exposure.tolist(),
                                  "conditional_target_counts": stream.endpoint_targets.tolist(),
                                  "maximum_frequency_error": float((frequencies - exact).abs().max()),
                                  "slot1_sum_counts": stream.sum_exposure.tolist(),
                                  "rendering_total": int(stream.rendering_exposure.sum()),
                                  "rolling_hash": stream.rolling.hex()}
        mask = candidate.mask()
        if not mask.any():
            raise ValueError("r12 unseen calibration panel is empty")
        unseen[law] = {"count": int(mask.sum()), "updates_observed": 128}
        b_rows[law] = {}
        for name, current in (("oracle", False), ("current_board_null", True)):
            model = r11.r8.ExactRowModel("raw_only", law, current_only=current).eval()
            b_rows[law][name] = r11._score_b(model, law, candidate, reject_empty=True)
            b_rows[law][name]["route_damage"] = r11.r8.route_damage(model, law)
        if not b_rows[law]["oracle"]["B_pass"]:
            raise ValueError("r12 oracle fails a registered B bar")
        if law == "original" and b_rows[law]["current_board_null"]["B_pass"]:
            raise ValueError("r12 original current-board null passes B")
        if law == "equal" and not b_rows[law]["current_board_null"]["B_pass"]:
            raise ValueError("r12 equal current-board null is not law-aware")
        # The route scorer itself refuses any nonzero inactive-route effect.
        forced_a = r11.r8.ExactRowModel("a_only", law).eval()
        b_rows[law]["forced_A_oracle"] = r11._score_b(forced_a, law, candidate, reject_empty=True)
        b_rows[law]["forced_A_oracle"]["route_damage"] = r11.r8.route_damage(forced_a, law)
        if not b_rows[law]["forced_A_oracle"]["B_pass"]:
            raise ValueError("r12 forced-A oracle fails B")
    supplied = new_model(0, "a_supplied", ROOT).to(device).eval()
    exact_a = r11.a_accuracy(supplied, device)
    local = r11.local_a_accuracy(supplied, device)
    if exact_a["vector"]["correct"] != 24435 or local["correct"] != 1555:
        raise ValueError("r12 frozen A source is not exact")
    untrained = new_model(0, "uniform", ROOT).to(device).eval()
    untrained_b = r11._score_b(r11.DeviceAuditAdapter(untrained, device), "original",
                              _candidate("original"), reject_empty=True)
    if untrained_b["B_pass"]:
        raise ValueError("r12 untrained network passes B")
    census = {}
    for law in r11.LAWS:
        census[law] = r11.board_census(r11.r8.ExactRowModel("raw_only", law).eval(), law,
                                     torch.device("cpu"))
        if any(row["above_0_02_TV"] for row in (census[law]["registered_rendering"],
                *census[law]["additional_fixed_renderings"], census[law]["saved_r9_failed_renderings"])):
            raise ValueError("r12 exact predictive census fails")
    untrained_census = {law: r11.board_census(untrained, law, device) for law in r11.LAWS}
    if untrained_census["original"]["registered_rendering"]["above_0_02_TV"] == 0:
        raise ValueError("r12 untrained census does not separate")
    probes = {"oracle": r11.probe_audit(untrained, device, oracle=True),
              "untrained": r11.probe_audit(untrained, device)}
    minimum = min(row["accuracy"] for sites in probes["oracle"]["sites"].values()
                  for family in sites.values() for row in family["sum36"])
    if minimum < .99 or any(row["converged"] is False
            for sites in probes["oracle"]["sites"].values()
            for family in sites.values() for row in family["sum36"]):
        raise ValueError("r12 exact-A probe calibration fails")
    diagnostics = calibrate_diagnostics()
    result = {"registration_sha256": r11.sha(OUTPUT / "registration.json"),
              "B": b_rows, "untrained_B": untrained_b, "unseen": unseen,
              "sampler": sampler, "census": census, "untrained_census": untrained_census,
              "probes": probes,
              "frozen_A_boards": exact_a, "frozen_A_local": local,
              "diagnostic_calibration": diagnostics,
              "checks": {"oracle_B_both_laws": True, "original_null_fails": True,
                         "equal_null_passes": True, "untrained_B_fails": True,
                         "unseen_nonempty": True, "strata_exact": True,
                         "target_frequencies_preserved": True, "frozen_A_exact": True,
                         "oracle_census_exact": True, "oracle_probe_minimum": minimum,
                         "inactive_routes_zero_effect": True, "untrained_census_fails": True,
                         "diagnostic_decisions_separate": True},
              "device": device.type, "linear_fit_device": "cpu"}
    r11.write_json(destination, result)
    return result


@torch.no_grad()
def category_counts(model, device, *, smoke=False, render_offset=0, law="original"):
    boards = enumerate_boards()
    ids = np.arange(len(boards.boards))
    if smoke:
        ids = ids[np.linspace(0, len(ids) - 1, 128, dtype=int)]
    records = r11._census_records(boards, ids, render_offset=render_offset)
    truth = np.asarray(boards.boards)[ids, 0]
    anchor_ids = [int(np.flatnonzero(np.asarray(boards.boards)[:, 0] == value)[0])
                  for value in (0, 36)]
    adapter = r11.DeviceAuditAdapter(model, device)
    aa, rr = adapter.round_interfaces(torch.from_numpy(r11._census_records(
        boards, np.asarray(anchor_ids), render_offset=0)))[1:]
    _, anchors = adapter.upper_step(aa, rr)
    predicted_head, signatures, vector_predictions = [], [], []
    for start in range(0, len(records), 256):
        x = torch.from_numpy(records[start:start + 256]).to(device)
        logits, a, raw = model.round_interfaces(x)
        head = logits if model.dual else model.raw_sum_head(raw).reshape(-1, 5, 36)
        vector_predictions.append(np.asarray(VALUES)[head.argmax(-1).cpu().numpy()])
        predicted_head.extend(np.asarray(VALUES)[head[:, 0].argmax(-1).cpu().numpy()].tolist())
        paired = []
        for anchor in anchors:
            answer, _ = model.upper_step(a, raw, anchor.to(device)[None].expand(len(x), -1))
            paired.append(answer.softmax(-1).cpu().numpy())
        signatures.extend(r11.r9.signature(np.stack(paired, 1)).tolist())
    correct = np.concatenate(vector_predictions) == np.asarray(boards.boards)[ids]
    head_counts = {"per_slot": [{"correct": int(correct[:, k].sum()), "total": len(ids)}
                                 for k in range(5)],
                   "vector": {"correct": int(correct.all(1).sum()), "total": len(ids)}}
    if law == "equal":
        categories = lambda x: np.where(x <= 12, 0, np.where(x >= 24, 2, 1))
        result = {"A_head_category_errors": int((categories(truth) !=
                    categories(np.asarray(predicted_head))).sum()), "boards": len(ids),
                  "B_signature_errors": None, "B_errors_with_correct_A_category": None,
                  "status": "EQUAL_LAW_HAS_NO_DISTINCT_B_CATEGORY_SIGNATURE"}
    else:
        result = r11._aggregate_dose_counts(truth, np.asarray(predicted_head), np.asarray(signatures))
    return {**result, "A_exact_counts": head_counts, "rendering": render_offset}


def failure_chronology(sequence, *, anchor_responses_valid):
    """Separate time ordering from descriptive association with a sequence failure."""
    if not sequence or [row["round"] for row in sequence] != list(range(1, len(sequence) + 1)):
        raise ValueError("r12 diagnostic prefix is empty or has invalid round order")
    if any(not np.isfinite(row[key]) or row[key] < 0 for row in sequence
           for key in ("TV", "constituent_response_maximum_TV")):
        raise ValueError("r12 diagnostic response TV is invalid")
    first_bad = next((s for s in sequence if s["TV"] > .02), None)
    observed = sequence if first_bad is None else sequence[:first_bad["round"]]
    first_error = next((s for s in observed if s["board_signature"] is not None and
                        s["board_signature"] != s["exact_category"]), None)
    relation = ("NO_OBSERVED_CONSTITUENT_ERROR" if first_error is None else
                "PRECEDING" if first_bad is not None and first_error["round"] < first_bad["round"] else
                "COINCIDENT" if first_bad is not None else "NO_SEQUENCE_DEVIATION")
    correct_responses = all(s["constituent_response_maximum_TV"] <= .02 and
                            (s["board_signature"] is None or
                             s["board_signature"] == s["exact_category"]) for s in observed)
    # The actual history's first response must also be a valid set/reset.
    anchors_valid = bool(anchor_responses_valid and sequence[0]["TV"] <= .02)
    hypothesis = ("NO_DEVIATION" if first_bad is None else
                  "BOARD_ASSOCIATED_FAILURE" if first_error is not None else
                  "RECURRENCE_ASSOCIATED_FAILURE" if correct_responses and anchors_valid else
                  "CAUSE_UNRESOLVED")
    return {"first_deviation": None if first_bad is None else first_bad["round"],
            "earliest_incorrect_constituent_signature": None if first_error is None else first_error["round"],
            "constituent_error_relation": relation,
            "correct_constituent_responses_through_failure": correct_responses,
            "anchor_responses_valid": anchors_valid, "descriptive_hypothesis": hypothesis}


def select_failure_reading(diagnoses):
    """Use observed failures, not a passing clear-neutral test, for attribution."""
    histories, clear = diagnoses["worst_histories"], diagnoses["clear_neutral_hold"]
    if (not histories or not clear or any(not row["prefixes"] for row in histories.values()) or
            any(row["response_count"] <= 0 or not row["boards"] or
                not row["per_length_maximum_TV"] for row in clear) or
            diagnoses["anchor_responses"]["count"] <= 0):
        raise ValueError("r12 diagnostic selection requires nonempty prefix, neutral and anchor panels")
    if any(row["first_deviation"] is not None and
           row["descriptive_hypothesis"] == "BOARD_ASSOCIATED_FAILURE" for row in histories.values()):
        return "Board computation remains a candidate limitation after history coverage"
    if any(row["first_deviation"] is not None and
           row["descriptive_hypothesis"] == "RECURRENCE_ASSOCIATED_FAILURE" and
           row["correct_constituent_responses_through_failure"] and row["anchor_responses_valid"]
           for row in histories.values()):
        return "Upper recurrence remains a limitation"
    # A clear-neutral violation is usable only with correct constituents and anchors.
    for row in clear:
        if (max(row["per_length_maximum_TV"]) > .02 and
                row["per_length_maximum_TV"][0] <= .02 and
                row["constituent_response_maximum_TV"] <= .02 and
                (row["correct_N_signatures"] is None or
                 row["correct_N_signatures"] == row["response_count"]) and
                diagnoses["anchor_responses"]["valid"]):
            return "Upper recurrence remains a limitation"
    return "Cause unresolved"


@torch.no_grad()
def prefix_diagnosis(model, law, stream, device):
    adapter = r11.DeviceAuditAdapter(model, device)
    _, _, records, lengths, meta = r11.r8._panels(law)
    if not len(records) or len(records) != len(lengths) or len(records) != len(meta):
        raise ValueError("r12 diagnostic prefix panel is empty or misaligned")
    probabilities, _ = r11.choice.predict_panel(adapter, records, lengths)
    boards = enumerate_boards()
    truths = np.asarray(P_EQUAL if law == "equal" else P, dtype=float)
    sums = np.asarray(boards.boards)[:, 0]
    anchor_ids = np.asarray([int(np.flatnonzero(sums == value)[0]) for value in (0, 36)])
    a0, r0 = adapter.round_interfaces(torch.from_numpy(r11._census_records(
        boards, anchor_ids, render_offset=0)))[1:]
    anchor_logits, anchor_states = adapter.upper_step(a0, r0)
    anchor_predictions = anchor_logits.softmax(-1).numpy()
    anchor_truth = np.broadcast_to(truths, (2, 3)) if law == "equal" else truths
    anchor_tv = r11.r9.tv(anchor_predictions, anchor_truth)
    anchors = {"count": 2, "board_ids": anchor_ids.tolist(), "TV": anchor_tv.tolist(),
               "predictions": anchor_predictions.tolist(), "exact_rows": anchor_truth.tolist(),
               "valid": bool((anchor_tv <= .02).all())}
    worst = {}
    for k in range(9):
        for anchor in (0, 2):
            indices = [i for i, item in enumerate(meta)
                       if item["first"] == anchor and item["neutral_run"] == k]
            if not indices:
                raise ValueError("r12 diagnostic prefix stratum is empty")
            expected = truths if law == "equal" else truths[int(anchor == 2)]
            errors = r11.r9.tv(probabilities[indices, lengths[indices] - 1], expected)
            index = indices[int(errors.argmax())]
            sequence = []
            # Independent low/high anchors define each constituent board signature.
            for at, board_id in enumerate(meta[index]["board_indices"]):
                x = torch.from_numpy(records[index, at:at + 1])
                a, r = adapter.round_interfaces(x)[1:]
                responses = np.stack([adapter.upper_step(a, r, s[None])[0].softmax(-1).numpy()[0]
                                      for s in anchor_states])
                category = 0 if sums[board_id] <= 12 else 2 if sums[board_id] >= 24 else 1
                modes_after = (0, 0) if category == 0 else (1, 1) if category == 2 else (0, 1)
                response_truth = (np.broadcast_to(truths, (2, 3)) if law == "equal" else
                                  truths[list(modes_after)])
                record_id = int(r11.rendering_ids(x)[0])
                sequence.append({"round": at + 1, "board_id": board_id,
                                 "slot1_sum": boards.boards[board_id][0],
                                 "exact_category": (0 if boards.boards[board_id][0] <= 12 else
                                                     2 if boards.boards[board_id][0] >= 24 else 1),
                                 "records": x[0].tolist(), "rendering_id": record_id,
                                 "training_board_count": int(stream.board_exposure[board_id]),
                                 "training_rendering_count": int(stream.rendering_exposure[record_id]),
                                 "exact_row": expected.tolist(),
                                 "prediction": probabilities[index, at].tolist(),
                                 "TV": float(r11.r9.tv(probabilities[index, at], expected)),
                                 "constituent_response_maximum_TV": float(r11.r9.tv(responses, response_truth).max()),
                                 "board_signature": (None if law == "equal" else
                                     int(r11.r9.signature(responses[None])[0])),
                                 "board_responses_after_L_H": responses.tolist()})
            chronology = failure_chronology(sequence, anchor_responses_valid=anchors["valid"])
            worst[f"{('L', 'H')[anchor == 2]}_N{k}"] = {
                "panel_index": index, "maximum_TV": float(errors.max()), "prefixes": sequence,
                **chronology}
    # Repeated clear-N records, selected without looking at predictions.
    sums = np.asarray(boards.boards)[:, 0]
    neutral_ids = np.flatnonzero((sums >= 16) & (sums <= 20))[:64]
    if not len(neutral_ids):
        raise ValueError("r12 diagnostic clear-neutral panel is empty")
    clear = []
    for anchor in (0, 2):
        anchor_id = int(np.flatnonzero(sums == (0 if anchor == 0 else 36))[0])
        x = r11._census_records(boards, neutral_ids, render_offset=0)
        first = r11._census_records(boards, np.asarray([anchor_id]), render_offset=0)
        panel = np.concatenate((np.repeat(first[:, None], len(x), axis=0),
                                np.repeat(x[:, None], 8, axis=1)), axis=1)
        preds, _ = r11.choice.predict_panel(adapter, panel, np.full(len(x), 9))
        expected = truths if law == "equal" else truths[int(anchor == 2)]
        # Measure both anchor responses for each clear-neutral rendering.
        aa, rr = adapter.round_interfaces(torch.from_numpy(x))[1:]
        anchors_x = r11._census_records(boards, np.asarray([
            int(np.flatnonzero(sums == value)[0]) for value in (0, 36)]), render_offset=0)
        anchor_a, anchor_r = adapter.round_interfaces(torch.from_numpy(anchors_x))[1:]
        _, states = adapter.upper_step(anchor_a, anchor_r)
        responses = np.stack([adapter.upper_step(aa, rr, state[None].expand(len(x), -1))[0]
                              .softmax(-1).numpy() for state in states], 1)
        response_truth = (truths if law == "equal" else truths[None])
        clear.append({"anchor": anchor, "boards": neutral_ids.tolist(),
                      "per_length_maximum_TV": r11.r9.tv(preds, expected).max(0).tolist(),
                      "clear_N_verified_by_sum": True,
                      "constituent_response_maximum_TV": float(r11.r9.tv(responses, response_truth).max()),
                      "correct_N_signatures": (None if law == "equal" else
                          int((r11.r9.signature(responses) == 1).sum())),
                      "response_count": len(x),
                      "board_responses_after_L_H": responses.tolist()})
    return {"worst_histories": worst, "clear_neutral_hold": clear, "anchor_responses": anchors,
            "interpretation_limit": "Board errors preceding failure and drift after correct responses are descriptive evidence, not a unique causal explanation."}


class DiagnosticControl(r11.r8.ExactRowModel):
    """Record-derived oracle with a planted neutral misread or delayed mode error."""

    def __init__(self, kind, law):
        super().__init__("raw_only", law)
        self.kind = kind

    def round_interfaces(self, records):
        logits, answers, raw = super().round_interfaces(records)
        if self.kind == "board_error":
            raw[:, 0] = torch.where(raw[:, 0] == 1, 0, raw[:, 0])
        return logits, answers, raw

    def upper_step(self, answers, raw, previous=None):
        logits, state = super().upper_step(answers, raw, previous)
        if self.kind != "delayed_drift" or self.law == "equal":
            return logits, state
        old_count = torch.zeros(len(raw)) if previous is None else previous[:, 1]
        count = torch.where(raw[:, 0] == 1, old_count + 1, 0)
        state[:, 1] = count
        state[:, 0] = torch.where(count == 3, 1 - state[:, 0], state[:, 0])
        rows = torch.tensor(np.asarray(P, dtype=np.float32))[state[:, 0].long()]
        return rows.log(), state


def calibrate_diagnostics():
    device = torch.device("cpu")
    stream = CoverageStream(r11.BoardTables(device), 17, "original", "uniform")
    result = {}
    expected = {"oracle": ("NO_DEVIATION", "Cause unresolved"),
                "board_error": ("BOARD_ASSOCIATED_FAILURE",
                                "Board computation remains a candidate limitation after history coverage"),
                "delayed_drift": ("RECURRENCE_ASSOCIATED_FAILURE", "Upper recurrence remains a limitation")}
    for law in r11.LAWS:
        result[law] = {}
        for kind, (hypothesis, reading) in expected.items():
            model = DiagnosticControl(kind, law).eval()
            diagnosis = prefix_diagnosis(model, law, stream, device)
            selected = select_failure_reading(diagnosis)
            categories = [row["descriptive_hypothesis"] for row in diagnosis["worst_histories"].values()]
            if law == "equal" or kind == "oracle":
                if set(categories) != {"NO_DEVIATION"} or selected != "Cause unresolved":
                    raise ValueError("r12 exact diagnostic oracle has a deviation or a causal reading")
            elif hypothesis not in categories or selected != reading:
                raise ValueError(f"r12 planted diagnostic {kind} does not separate")
            result[law][kind] = {"diagnosis": diagnosis, "selected_failure_reading": selected,
                                "classification_counts": {key: categories.count(key) for key in set(categories)},
                                "pass": True}
    return result


def audit_record(model, run, candidate, stream, device, step, details, bulk, *, smoke):
    started = time.monotonic()
    audit = r11.audit_one(model, run.law, device, candidate, smoke=smoke)
    a = r11.a_accuracy(model, device, smoke=smoke)
    return {"step": step, "train_parts": details, "audit": audit,
            "A_board_accuracy": a, "A_accuracy": a["vector"]["correct"] / a["vector"]["total"],
            "frozen_A_local_history_counts": {"correct": 1555, "total": 1555,
                                              "operative": run.dual},
            "A_local_history_accuracy": r11.local_a_accuracy(model, device),
            "category_error_decomposition": [category_counts(model, device, smoke=smoke,
                                               render_offset=k, law=run.law) for k in range(4)],
            "prefix_diagnosis": prefix_diagnosis(model, run.law, stream, device),
            "exposure": r11._exposures(stream, bulk / f"exposure_step_{step:06d}.npz"),
            "stratum_endpoints": stream.stratum_exposure.tolist(),
            "conditional_endpoint_target_counts": stream.endpoint_targets.tolist(),
            "A_supervised_counts_by_slot_sum": (stream.slot_sum_exposure if run.arm == "a_target"
                                                else torch.zeros_like(stream.slot_sum_exposure)).tolist(),
            "unseen_composition": candidate.composition(candidate.mask()),
            "stream_rolling_hash": stream.rolling.hex(), "reduced_smoke": smoke,
            "elapsed_seconds": time.monotonic() - started}


def _mean(rows):
    return {key: sum(row[key] for row in rows) / len(rows) for key in rows[0]}


def _bound_load(path):
    if path.with_suffix(".sha256").read_text().strip() != r11.sha(path):
        raise ValueError("r12 checkpoint digest differs")
    return torch.load(path, map_location="cpu", weights_only=False)


def _save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError("r12 checkpoint destination is nonempty")
    pending = path.with_suffix(".pending")
    torch.save(value, pending)
    path.with_suffix(".sha256").write_text(r11.sha(pending) + "\n")
    pending.rename(path)


def run_chunk(runs, device, output, bulk, *, steps=20000, smoke=False):
    registration()
    calibration_sha = r11.sha(OUTPUT / "calibration.json")
    identity = hashlib.sha256("\n".join(r.name for r in runs).encode()).hexdigest()[:16]
    group = bulk / ("group_" + identity)
    group.mkdir(parents=True, exist_ok=True)
    tables = r11.BoardTables(device)
    engine = Engine(runs, device)
    streams = [CoverageStream(tables, r.seed, r.law, r.draw) for r in runs]
    candidates = [_candidate(r.law) for r in runs]
    curves, windows, stopped = [[] for _ in runs], [[] for _ in runs], [False] * len(runs)
    authority = {"registration_sha256": r11.sha(OUTPUT / "registration.json"),
                 "calibration_sha256": calibration_sha, "runs": [r.name for r in runs],
                 "smoke": smoke, "precision": "float32"}
    paths = sorted(group.glob("checkpoint_step_*.pt"))
    start = 0
    if paths:
        saved = _bound_load(paths[-1])
        if not metadata_matches(saved["authority"], authority):
            raise ValueError("r12 checkpoint authority differs")
        engine.restore(saved["engine"])
        for stream, state, candidate, seen in zip(streams, saved["streams"], candidates,
                                                  saved["candidate_seen"], strict=True):
            stream.restore(state)
            candidate.seen = seen
        start, curves, windows, stopped = (saved[key] for key in ("step", "curves", "windows", "stopped"))
    for run in runs:
        directory = output / run.name
        directory.mkdir(parents=True, exist_ok=True)
        settings_path = directory / "settings.json"
        binding = {"authority": authority, "group": identity, "bulk": str(bulk),
                   "run": run.__dict__}
        if settings_path.exists():
            if json.loads(settings_path.read_text()) != binding:
                raise ValueError("r12 run directory has different settings or execution batch")
        else:
            r11.write_json(settings_path, binding)
        r11._write_progress(directory / "progress.log", f"START step={start} target={steps} precision=float32")
    if not paths:
        states = [s.state() for s in streams]
        preview = [[] for _ in runs]
        with torch.no_grad():
            for _ in range(100):
                batches = [s.draw_batch() for s in streams]
                out = engine.forward(torch.stack([b.records for b in batches]),
                                     torch.stack([b.lengths for b in batches]))
                _, details = coverage_loss(out, batches, [r.arm for r in runs])
                for index, d in enumerate(details):
                    preview[index].append(d)
        for stream, state in zip(streams, states, strict=True):
            stream.restore(state)
        windows = [[_mean(p)] for p in preview]
    update_seconds = 0.
    audit_seconds = 0.
    schedule = {0, steps} if smoke else set(AUDITS)
    for step in range(start, steps + 1):
        if step > start:
            if all(stopped):
                break
            before = time.monotonic()
            batches = [s.draw_batch() if not stopped[i] else None for i, s in enumerate(streams)]
            reference = next(b for b in batches if b is not None)
            details = engine.update([b or reference for b in batches],
                                    torch.tensor([not s for s in stopped], device=device))
            update_seconds += time.monotonic() - before
            for index, batch in enumerate(batches):
                if batch is None:
                    continue
                r11._observe(candidates[index], batch)
                windows[index] = (windows[index] + [details[index]])[-100:]
        if step not in schedule or (paths and step == start):
            continue
        for index, run in enumerate(runs):
            if stopped[index]:
                continue
            folder = bulk / run.name
            folder.mkdir(parents=True, exist_ok=True)
            row = audit_record(engine.model_at(index), run, candidates[index], streams[index],
                               device, step, _mean(windows[index]), folder, smoke=smoke)
            if step == 5000:
                row["futility"] = futility(curves[index][0], row, run)
                stopped[index] = row["futility"]["stop"]
            path = folder / f"audit_step_{step:06d}.json"
            r11.write_json(path, row)
            curves[index].append({"step": step, "path": str(path), "sha256": r11.sha(path),
                                   "train_parts": row["train_parts"], "A_accuracy": row["A_accuracy"],
                                   "audit": {"B_pass": row["audit"]["B_pass"],
                                             "natural_excess_KL_bits": row["audit"]["natural_excess_KL_bits"]}})
            # Futility state is retained in the checkpoint before progress is published.
            audit_seconds += row["elapsed_seconds"]
            per_run = folder / f"checkpoint_step_{step:06d}.pt"
            record = {
                "model": {k: v[index].detach().cpu() for k, v in engine.parameters.items()},
                "authority": authority, "step": step, "futility_stop": stopped[index]}
            if per_run.exists():
                old = _bound_load(per_run)
                if not metadata_matches(old["authority"], authority) or old["futility_stop"] != stopped[index]:
                    raise ValueError("r12 partial per-run checkpoint binding differs")
                _check_numeric(old["model"], record["model"], exact=True)
            else:
                _save(per_run, record)
        _save(group / f"checkpoint_step_{step:06d}.pt", {
            "authority": authority, "step": step, "engine": engine.state(),
            "streams": [s.state() for s in streams], "candidate_seen": [c.seen for c in candidates],
            "curves": curves, "windows": windows, "stopped": stopped})
        for index, run in enumerate(runs):
            if curves[index] and curves[index][-1]["step"] == step:
                row = curves[index][-1]
                r11._write_progress(output / run.name / "progress.log",
                    f"CHECKPOINT step={step} B={row['train_parts']['B']:.8g} natural_KL={row['audit']['natural_excess_KL_bits']:.8g} A_vector={row['A_accuracy']:.8g}")
    summaries = []
    for index, run in enumerate(runs):
        note = {"run": run.__dict__, "authority": authority, "curve": curves[index],
                "futility_stop": stopped[index], "step": int(engine.optimizer.steps[index]),
                "bulk_directory": str(bulk / run.name), "resumed_from": start,
                "performance": {"batch_width": len(runs), "updates_seconds": update_seconds,
                                "completed_updates_this_execution": max(0, int(engine.optimizer.steps[index]) - start),
                                "audit_seconds": audit_seconds,
                                "maximum_RSS_MiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
                                "GPU_peak_MiB": (torch.cuda.max_memory_allocated() / 2**20
                                                 if device.type == "cuda" else None),
                                "CPU_threads": torch.get_num_threads()},
                "first_audited_crossing": next((r["step"] for r in curves[index]
                                                if r["audit"]["B_pass"]), None)}
        r11.write_json(output / run.name / "summary.json", note)
        r11._write_progress(output / run.name / "progress.log",
                           ("FUTILITY_STOP" if stopped[index] else "COMPLETE") + f" step={note['step']}")
        summaries.append(note)
    return summaries


def _check_numeric(first, second, *, exact=False):
    tolerance = 0. if exact else 3e-5
    maximum = 0.
    for key, value in first.items():
        other = second[key].to(value.device)
        if not torch.is_floating_point(value):
            if not torch.equal(value, other):
                raise ValueError(f"r12 discrete comparison differs: {key}")
        else:
            maximum = max(maximum, float((value - other).detach().abs().max()))
            if not torch.allclose(value, other, atol=tolerance, rtol=tolerance):
                raise ValueError(f"r12 numeric comparison differs: {key}; max={maximum}")
    return maximum


def _check_stream(first, second):
    for key, value in first.state().items():
        other = second.state()[key]
        equal = torch.equal(value.cpu(), other.cpu()) if isinstance(value, torch.Tensor) else value == other
        if not equal:
            raise ValueError(f"r12 stream comparison differs: {key}")


def verification(device, *, trace=False, destination=None):
    """Width-three and direct width-one against ordinary AdamW and disk restoration."""
    import tempfile
    registration()
    registration_hash = r11.sha(OUTPUT / "registration.json")
    source_hashes = identities()
    tables = r11.BoardTables(device)
    records = {}
    for arms in (("uniform", "cutoff", "decoy"), ("a_target",) * 3, ("a_supplied",)):
        runs = [Run(arm, "original", index if arm == "a_target" else 0)
                for index, arm in enumerate(arms)]
        engine = Engine(runs, device)
        separate = [Engine([r], device) for r in runs]
        ordinary = [new_model(r.seed, r.arm, ROOT).to(device) for r in runs]
        optimizers = [torch.optim.AdamW(m.parameters(), lr=.003, weight_decay=.01) for m in ordinary]
        streams = [CoverageStream(tables, r.seed, r.law, r.draw) for r in runs]
        independent_streams = [CoverageStream(tables, r.seed, r.law, r.draw) for r in runs]
        restored, restored_streams = None, None
        trace_rows = []
        for step in range(1, 9):
            batches = [s.draw_batch() for s in streams]
            independents = [s.draw_batch() for s in independent_streams]
            if trace:
                differences = []
                for i, m in enumerate(ordinary):
                    candidate = engine.model_at(i)
                    p = {key: value[i].detach() for key, value in engine.parameters.items()}
                    delta = r11._difference_fields(p, dict(m.named_parameters()))
                    with torch.no_grad():
                        active = batches[i].active
                        x = batches[i].records[active]
                        before = candidate.round_interfaces(x)[0]
                        comparison = m.round_interfaces(x)[0]
                        wrong = before.argmax(-1) != comparison.argmax(-1)
                        margins = before.topk(2, -1).values
                        other_margins = comparison.topk(2, -1).values
                    differences.append({"parameters": delta,
                        "hard_A_disagreements": int(wrong.sum()),
                        "top_two_logits": margins[wrong].cpu().tolist(),
                        "ordinary_top_two_logits": other_margins[wrong].cpu().tolist()})
            engine.update(batches, torch.ones(len(runs), dtype=torch.bool, device=device))
            for i, (reference, optimizer, batch, alone) in enumerate(zip(
                    ordinary, optimizers, independents, separate, strict=True)):
                alone.update([batch], torch.ones(1, dtype=torch.bool, device=device))
                optimizer.zero_grad(set_to_none=True)
                output = tuple(value[None] for value in reference(batch.records, batch.lengths, return_all=True))
                loss, _ = coverage_loss(output, [batch], [runs[i].arm])
                loss.sum().backward()
                optimizer.step()
            if trace:
                gradients = [{key: float((value.grad[i] - dict(ordinary[i].named_parameters())[key].grad)
                                        .abs().max()) for key, value in engine.parameters.items()
                              if value.grad is not None and
                              dict(ordinary[i].named_parameters())[key].grad is not None}
                             for i in range(len(runs))]
                trace_rows.append({"step": step, "before": differences, "gradient_maximum_differences": gradients})
            if restored is not None:
                resumed = [s.draw_batch() for s in restored_streams]
                restored.update(resumed, torch.ones(len(runs), dtype=torch.bool, device=device))
            if step == 3:
                # Actual serialization, not just a copy of in-memory tensors.
                with tempfile.TemporaryDirectory(prefix="r12_restore_") as directory:
                    path = Path(directory) / "step3.pt"
                    torch.save({"engine": engine.state(), "streams": [s.state() for s in streams]}, path)
                    saved = torch.load(path, map_location="cpu", weights_only=False)
                restored = Engine(runs, device)
                restored.restore(saved["engine"])
                restored_streams = [CoverageStream(tables, r.seed, r.law, r.draw) for r in runs]
                for stream, state in zip(restored_streams, saved["streams"], strict=True):
                    stream.restore(state)
        maxima, failures = [], []
        def checked(first, second, *, exact=False):
            try:
                value = _check_numeric(first, second, exact=exact)
                maxima.append(value)
                return value
            except ValueError as error:
                failures.append(str(error))
                return None
        for i, (alone, model, optimizer) in enumerate(zip(separate, ordinary, optimizers, strict=True)):
            parameters = {k: v[i] for k, v in engine.parameters.items()}
            checked(parameters, {k: v[0] for k, v in alone.parameters.items()})
            checked(parameters, dict(model.named_parameters()))
            for name, ordinary_name in (("first", "exp_avg"), ("second", "exp_avg_sq")):
                expected = {key: optimizer.state[value].get(ordinary_name, torch.zeros_like(value))
                            for key, value in model.named_parameters()}
                checked({k: v[i] for k, v in getattr(engine.optimizer, name).items()}, expected)
                checked({k: v[i] for k, v in getattr(engine.optimizer, name).items()},
                        {k: v[0] for k, v in getattr(alone.optimizer, name).items()})
            for key, parameter in model.named_parameters():
                expected_step = int(optimizer.state[parameter].get("step", 0))
                if (int(engine.optimizer.parameter_steps[key][i]) != expected_step or
                        int(alone.optimizer.parameter_steps[key][0]) != expected_step):
                    failures.append(f"optimizer step differs: {key}")
            for stream in (independent_streams[i], restored_streams[i]):
                try:
                    _check_stream(streams[i], stream)
                except ValueError as error:
                    failures.append(str(error))
        checked(engine.parameters, restored.parameters, exact=True)
        for name in ("first", "second", "parameter_steps"):
            checked(getattr(engine.optimizer, name), getattr(restored.optimizer, name), exact=True)
        records["_".join(arms)] = {"width": len(runs), "pass": not failures,
            "failures": failures, "updates": 8, "restoration_update": 3,
            "maximum_numeric_difference": max(maxima, default=None),
            "streams_exposures_strata_targets": "exact", "restoration": "exact",
            "trace": trace_rows if trace else None}
    result = {"device": device.type, "pass": all(row["pass"] for row in records.values()),
              "registration_sha256": registration_hash, "source_sha256": source_hashes,
              "comparisons": records,
              "tolerances": r11.EQUIVALENCE_TOLERANCE}
    if destination:
        r11.write_json(destination, result)
    return result


def _load_audit(row):
    path = public_path(row["path"])
    if r11.sha(path) != row["sha256"]:
        raise ValueError("r12 saved audit digest differs")
    return json.loads(path.read_text())


def aggregate_registration():
    """Read historical training authority without reissuing it for report edits."""
    note = json.loads((OUTPUT / "registration.json").read_text())
    current = identities()
    if (note["settings"] != settings() or note["runs"] != [r.name for r in all_runs()] or
            note["source_sha256"].keys() != current.keys() or
            any(note["source_sha256"][key] != current[key] for key in current if key != "script")):
        raise ValueError("r12 aggregate non-report authority differs")
    return note


def aggregate_diagnosis(diagnosis):
    """Retain concurrent associations instead of selecting a single explanation."""
    histories = diagnosis["worst_histories"]
    kinds = {"BOARD_ASSOCIATED_FAILURE": "board_associated",
             "RECURRENCE_ASSOCIATED_FAILURE": "recurrence_associated",
             "CAUSE_UNRESOLVED": "unresolved", "NO_DEVIATION": "non_deviating"}
    counts = {name: 0 for name in kinds.values()}
    chronology = {name: 0 for name in ("PRECEDING", "COINCIDENT",
                                     "NO_OBSERVED_CONSTITUENT_ERROR", "NO_SEQUENCE_DEVIATION")}
    for history in histories.values():
        counts[kinds[history["descriptive_hypothesis"]]] += 1
        chronology[history["constituent_error_relation"]] += 1
    clear = []
    for row in diagnosis["clear_neutral_hold"]:
        values = row["per_length_maximum_TV"]
        correct = (row["constituent_response_maximum_TV"] <= .02 and
                   (row["correct_N_signatures"] is None or
                    row["correct_N_signatures"] == row["response_count"]))
        valid_anchor = values[0] <= .02 and diagnosis["anchor_responses"]["valid"]
        violations = [k for k, value in enumerate(values) if value > .02]
        clear.append({"anchor": row["anchor"], "boards": len(row["boards"]),
                      "response_count": row["response_count"],
                      "correct_N_signatures": row["correct_N_signatures"],
                      "constituent_response_maximum_TV": row["constituent_response_maximum_TV"],
                      "valid_anchor": bool(valid_anchor), "correct_constituent_responses": bool(correct),
                      "per_length_maximum_TV": values, "violating_N_lengths": violations,
                      "recurrence_evidence": bool(violations and correct and valid_anchor)})
    board = counts["board_associated"] > 0
    recurrence = counts["recurrence_associated"] > 0 or any(r["recurrence_evidence"] for r in clear)
    readings = []
    if board:
        readings.append("Board computation remains a candidate limitation after history coverage")
    if recurrence:
        readings.append("Upper recurrence remains a limitation")
    return {"selected_histories": len(histories), "counts": counts, "chronology": chronology,
            "clear_neutral": clear, "board_association_observed": board,
            "recurrence_evidence_observed": recurrence,
            "concurrent_findings": readings or ["Cause unresolved"],
            "scope": "Descriptive associations, not unique causal explanations."}


def aggregate_swaps(swaps):
    """Summarize only the five cases that decide the registered swap criterion."""
    names = ("reset_L", "set_H", "neutral_N", "same_category_substitution",
             "upper_state_exchange_same_N")
    cases = {name: swaps["cases"][name] for name in names}
    count = sum(row["count"] for row in cases.values())
    if count <= 0 or any(row["count"] <= 0 for row in cases.values()):
        raise ValueError("r12 aggregate swap panel is empty")
    return {"cases": cases, "count": count,
            "mean_TV": sum(row["count"] * row["mean_TV"] for row in cases.values()) / count,
            "maximum_TV": max(row["maximum_TV"] for row in cases.values()),
            "failed_cases": {name: row for name, row in cases.items() if row["maximum_TV"] > .02},
            "pass": swaps["natural_swap_pass"]}


def aggregate(output=OUTPUT):
    note = aggregate_registration()
    calibration = json.loads((OUTPUT / "calibration.json").read_text())
    report = {"registration_verbatim": note["specification_verbatim"], "runs": {},
              "comparison_scope": "Within r12; r11 comparisons are historical: curriculum and loss weighting changed.",
              "qualifications": [
                  "Supplied A is exact; A-target is approximate. This is an operational comparison, not a matched comparison of equally exact A interfaces.",
                  "r11 comparisons are historical: curriculum and loss weighting changed.",
                  "The long panel (N³–N⁸), formerly labelled extrapolation, is explicitly trained and does not test unseen lengths.",
                  "Competition within the encoder is a hypothesis, not an established mechanism.",
                  "Board and recurrence associations can coexist; three seeds do not establish population variability around the threshold."],
              "report_authority": {"registration_sha256": r11.sha(OUTPUT / "registration.json"),
                                   "calibration_sha256": r11.sha(OUTPUT / "calibration.json"),
                                   "report_script_sha256": r11.sha(Path(__file__))}}
    split = json.loads((r11.r8.OUTPUT / "probe_split.json").read_text())
    (_, _), (_, targets) = r11.r8._probe_data(split)
    for run in all_runs():
        path = output / run.name / "summary.json"
        if not path.exists():
            continue
        summary = json.loads(path.read_text())
        if "authority" in summary and any(summary["authority"][key] != report["report_authority"][key]
                for key in ("registration_sha256", "calibration_sha256")):
            raise ValueError("r12 aggregate run authority differs")
        first, last = (_load_audit(summary["curve"][i]) for i in (0, -1))
        audit = last["audit"]
        if last["reduced_smoke"]:
            probes = {"status": "REDUCED_SMOKE_NOT_A_STUDY_ENDPOINT",
                      "start": first["audit"]["probes"], "end": audit["probes"]}
        else:
            probes = r11._paired_probe_changes(first["audit"]["probes"], audit["probes"],
                targets, np.asarray(VALUES)[targets], seed=run.seed,
                oracle=calibration["probes"]["oracle"])
        row = {"arm": run.arm, "law": run.law, "seed": run.seed, "step": last["step"],
               "B_pass": audit["B_pass"], "criteria": audit["criteria"],
               "prediction_checks": r11._aggregate_prediction_checks(audit),
               "law_panels": r11._aggregate_law(audit["mode_law"]),
               "census_all_four_renderings_and_r9": audit["board_census"],
               "A_exact_counts": last["A_board_accuracy"],
               "local_history_counts": last["A_local_history_accuracy"],
               "unused_or_supplied_frozen_A_counts": last["frozen_A_local_history_counts"],
               "exposure": last["exposure"], "stratum_endpoints": last["stratum_endpoints"],
               "conditional_endpoint_target_counts": last["conditional_endpoint_target_counts"],
               "A_supervised_counts_by_slot_sum": last["A_supervised_counts_by_slot_sum"],
               "unseen_composition": last["unseen_composition"],
               "probes": probes, "worst_history_prefix_diagnosis": last["prefix_diagnosis"],
               "learning_curve": [{"step": a["step"], "train_parts": a["train_parts"],
                   "B_pass": a["audit"]["B_pass"], "criteria": a["audit"]["criteria"],
                   "category_errors": a["category_error_decomposition"],
                   "natural_KL_bits": a["audit"]["natural_excess_KL_bits"],
                   "A_exact_counts": a["A_board_accuracy"]}
                   for a in map(_load_audit, summary["curve"])],
               "first_audited_crossing": summary["first_audited_crossing"],
               "endpoint_status": ("REDUCED_SMOKE" if last["reduced_smoke"] else
                   "FUTILITY_STOP" if summary["futility_stop"] else
                   "PASS" if audit["B_pass"] and last["step"] == 20000 else "B_INCOMPLETE")}
        row["law_panels"]["panels"]["long"] = row["law_panels"]["panels"].pop("extrapolation")
        row["diagnosis_summary"] = aggregate_diagnosis(last["prefix_diagnosis"])
        row["registered_swap_summary"] = aggregate_swaps(audit["swaps"])
        report["runs"][run.name] = row
    report["comparison_table"] = [{"run": name, "arm": row["arm"], "law": row["law"],
            "seed": row["seed"], "step": row["step"], "endpoint_status": row["endpoint_status"],
            "law_panels": row["law_panels"]["panels"],
            "rerender": row["prediction_checks"]["rerender"],
            "registered_swaps": row["registered_swap_summary"]}
        for name, row in report["runs"].items()]
    report["A_target_joint_errors"] = [{"run": name, "seed": row["seed"], **counts}
        for name, row in report["runs"].items() if row["arm"] == "a_target" and row["law"] == "original"
        for counts in row["learning_curve"][-1]["category_errors"] if counts["rendering"] == 0]
    raw = [r["diagnosis_summary"] for r in report["runs"].values()
           if r["arm"] in GROUPS["rarity"] and r["law"] == "original"]
    report["raw_original_diagnosis_totals"] = {
        "runs": len(raw), "selected_histories": sum(r["selected_histories"] for r in raw),
        "counts": {key: sum(r["counts"][key] for r in raw)
                   for key in ("board_associated", "recurrence_associated", "unresolved", "non_deviating")},
        "chronology": {key: sum(r["chronology"][key] for r in raw)
                       for key in ("PRECEDING", "COINCIDENT", "NO_OBSERVED_CONSTITUENT_ERROR", "NO_SEQUENCE_DEVIATION")}}
    spec = note["specification_verbatim"]
    report["registered_readings_verbatim"] = spec[spec.index("Predeclare these readings:"):
                                                  spec.index("All pathway conclusions")]
    selected = {}
    for seed in (0, 1, 2):
        rows = {arm: report["runs"].get(Run(arm, "original", seed).name) for arm in ARMS}
        choices = []
        if any(row and row["endpoint_status"] == "REDUCED_SMOKE" for row in rows.values()):
            choices.append("Reduced smoke is not evidence for a registered reading.")
        elif rows["uniform"]:
            uniform = rows["uniform"]
            if uniform["B_pass"]:
                choices.append("Raw B-only training can realize B under this history distribution; r11 does not isolate board rarity as the cause")
            else:
                choices.extend(uniform["diagnosis_summary"]["concurrent_findings"])
        if all(rows[arm] for arm in ("uniform", "cutoff", "decoy")) and not any(
                rows[arm]["endpoint_status"] == "REDUCED_SMOKE" for arm in ("uniform", "cutoff", "decoy")):
            def errors(row):
                census = row["census_all_four_renderings_and_r9"]
                return sum(r["categorical_misreads"] for r in (
                    census["registered_rendering"], *census["additional_fixed_renderings"]))
            cutoff = rows["cutoff"]
            better_census = all(errors(cutoff) < errors(rows[a]) for a in ("uniform", "decoy"))
            better_b = all(cutoff["prediction_checks"]["natural_KL_bits"] <
                           rows[a]["prediction_checks"]["natural_KL_bits"] and
                           max(v["maximum_TV"] for v in cutoff["law_panels"]["cases"].values()) <
                           max(v["maximum_TV"] for v in rows[a]["law_panels"]["cases"].values())
                           for a in ("uniform", "decoy"))
            if better_census:
                choices.append("Targeted boundary exposure supports a rarity contribution" if better_b else
                               "Board repair is insufficient for predictive closure")
        if rows["a_supplied"] and rows["a_target"]:
            if rows["a_supplied"]["B_pass"] and not rows["a_target"]["B_pass"]:
                choices.append("Exact A access helps under these matched conditions; inspect learned-A errors before attributing the difference to pathway")
            elif rows["a_supplied"]["B_pass"] and rows["a_target"]["B_pass"]:
                choices.append("Either supplied access or auxiliary supervision can support B here")
        if rows["a_target"] and rows["a_target"]["endpoint_status"] != "REDUCED_SMOKE":
            curve = rows["a_target"]["learning_curve"]
            if (curve[-1]["A_exact_counts"]["vector"]["correct"] >
                    curve[0]["A_exact_counts"]["vector"]["correct"] and not rows["a_target"]["B_pass"]):
                choices.append("Readable/computable A does not ensure its predictive use")
        equal_rows = [report["runs"].get(Run(arm, "equal", seed).name) for arm in ARMS]
        if any(r and r["endpoint_status"] != "REDUCED_SMOKE" and
               not r["criteria"]["witness"] for r in equal_rows):
            choices.append("Control failure; interpret affected comparisons separately")
        selected[str(seed)] = choices or ["Endpoint evidence not yet available."]
    report["selected_reading"] = selected
    r11.write_json(output / "aggregate.json", report)
    (output / "aggregate.md").write_text(aggregate_markdown(report))
    return {"runs": len(report["runs"]), "selected_reading": selected}


def aggregate_markdown(report):
    def table(headers, rows):
        return ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers),
                *["| " + " | ".join(str(x) for x in row) + " |" for row in rows], ""]
    def count(row):
        return "not operative" if row is None else f"{row['correct']}/{row['total']}"
    text = ["# r12 aggregate", "", report["comparison_scope"], "",
            "Detailed predictions, exposures and prefix observations are retained in the hash-bound audit JSON files and aggregate.json.", "",
            "## Qualifications", "", *[f"- {value}" for value in report["qualifications"]], "",
            "## Registered readings (verbatim)", "", report["registered_readings_verbatim"], "",
            "## Selected reading", "", json.dumps(report["selected_reading"], indent=2), ""]
    text += ["## Comparison across arms and seeds", "",
             "Continuous TV values, not just threshold decisions. Swap summaries use only the five registered deciding cases.", ""]
    text += table(["Arm", "Law", "Seed", "Update", "Endpoint", "Short mean TV", "Short max TV",
                   "Long mean TV", "Long max TV", "Rerender TV", "A rerender differences",
                   "Swap mean TV", "Swap max TV", "Failed swap cases (max TV)"],
        [[r["arm"], r["law"], r["seed"], r["step"], r["endpoint_status"],
          r["law_panels"]["short"]["mean_TV"], r["law_panels"]["short"]["maximum_TV"],
          r["law_panels"]["long"]["mean_TV"], r["law_panels"]["long"]["maximum_TV"],
          r["rerender"]["maximum_TV"], r["rerender"]["A_answer_mismatched_components"],
          r["registered_swaps"]["mean_TV"], r["registered_swaps"]["maximum_TV"],
          "; ".join(f"{key}: {value['maximum_TV']}" for key, value in
                    r["registered_swaps"]["failed_cases"].items()) or "none"]
         for r in report["comparison_table"]])
    text += ["## Diagnosis counts and concurrent findings", "",
             "Counts describe selected worst-prefix histories, not a random sample. Board and recurrence evidence are both retained when concurrent.", ""]
    text += table(["Run", "Histories", "Board-associated", "Recurrence-associated", "Unresolved",
                   "Non-deviating", "Preceding", "Coincident", "Clear-N recurrence panels", "Concurrent findings"],
        [[name, d["selected_histories"], *[d["counts"][key] for key in (
             "board_associated", "recurrence_associated", "unresolved", "non_deviating")],
          d["chronology"]["PRECEDING"], d["chronology"]["COINCIDENT"],
          sum(c["recurrence_evidence"] for c in d["clear_neutral"]),
          "; ".join(d["concurrent_findings"])]
         for name, row in report["runs"].items() for d in [row["diagnosis_summary"]]])
    text += ["Original-law raw totals: " + json.dumps(report["raw_original_diagnosis_totals"]), "",
             "## A-target joint errors (registered rendering, original law)", ""]
    text += table(["Seed", "Boards", "A-head category errors", "B-signature errors", "B errors with correct A category"],
        [[r["seed"], r["boards"], r["A_head_category_errors"], r["B_signature_errors"],
          r["B_errors_with_correct_A_category"]] for r in report["A_target_joint_errors"]])
    supplied2 = report["runs"].get("a_supplied_original_seed2")
    if supplied2:
        reset = supplied2["registered_swap_summary"]["cases"]["reset_L"]
        text += [f"A-supplied original-law seed 2: reset_L maximum TV {reset['maximum_TV']} "
                 f"on {reset['count']} cases; endpoint {supplied2['endpoint_status']}. "
                 f"Short and long law panels pass: {all(p['pass'] for p in supplied2['law_panels']['panels'].values())}.", ""]
    for name, row in report["runs"].items():
        text += [f"## {name}", "", f"Endpoint: {row['endpoint_status']}; first crossing: {row['first_audited_crossing']}", ""]
        checks = row["prediction_checks"]
        text += table(["Natural KL bits", "Unseen KL bits", "Unseen count", "Witness recovery", "Swap pass", "Prediction rerender TV", "A rerender differences"],
            [[checks["natural_KL_bits"], checks["unseen_KL_bits"], checks["unseen_count"],
              checks["witness_recovery"], checks["swaps"]["natural_swap_pass"],
              checks["rerender"]["maximum_TV"], checks["rerender"]["A_answer_mismatched_components"]]])
        census = row["census_all_four_renderings_and_r9"]
        text += table(["Rendering", "Boards/cases", "B category errors", "TV > .02", "Maximum TV"],
            [[str(value.get("rendering", "saved r9")), value.get("boards", value.get("count")),
              value["categorical_misreads"], value["above_0_02_TV"], value["maximum_TV"]]
             for value in (census["registered_rendering"], *census["additional_fixed_renderings"],
                           census["saved_r9_failed_renderings"])])
        text += table(["A slot 1", "A slot 2", "A slot 3", "A slot 4", "A slot 5", "A vector", "Local A histories"],
            [[*[count(v) for v in row["A_exact_counts"]["per_slot"]],
              count(row["A_exact_counts"]["vector"]), count(row["local_history_counts"])]])
        text += table(["Law case", "Count", "Mean TV", "Max TV"],
            [[name, v["count"], v["mean_TV"], v["maximum_TV"]]
             for name, v in row["law_panels"]["cases"].items()])
        text += table(["Law panel", "Count", "Mean TV", "Max TV", "Pass"],
            [[name, v["count"], v["mean_TV"], v["maximum_TV"], v["pass"]]
             for name, v in row["law_panels"]["panels"].items()])
        text += table(["Anchor", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"],
                       [[anchor, *values] for anchor, values in zip(("L", "H"), row["stratum_endpoints"], strict=True)])
        text += table(["Update", "B loss", "Coverage endpoint KL", "Natural KL", "B pass", "A vector"],
            [[v["step"], v["train_parts"]["B"], v["train_parts"]["coverage_endpoint_KL_bits"],
              v["natural_KL_bits"], v["B_pass"], count(v["A_exact_counts"]["vector"])] for v in row["learning_curve"]])
        text += table(["Update", "Rendering", "Boards", "A-head category errors", "B-signature errors", "B errors with A category correct"],
            [[v["step"], c["rendering"], c["boards"], c["A_head_category_errors"],
              c["B_signature_errors"], c["B_errors_with_correct_A_category"]]
             for v in row["learning_curve"] for c in v["category_errors"]])
        if "status" not in row["probes"]:
            text += table(["Carrier", "Reader", "Target", "Slot", "Start", "End", "Gain (95% CI)", "Majority", "Oracle", "Converged"],
                [[site, family, target, p["slot"], p["update0_accuracy"], p["endpoint_accuracy"],
                  f"{p['gain']} {p['paired_CI95']}", p["majority_floor"], p["oracle_floor"], p["converged"]]
                 for site, families in row["probes"].items() for family, targets in families.items()
                 for target, values in targets.items() for p in values])
        else:
            text += ["Probes: reduced smoke; complete fitting records retained, no readability conclusion.", ""]
        text += table(["Worst prefix", "TV", "First deviation", "Earliest incorrect constituent",
                       "Chronology", "Descriptive hypothesis"],
            [[name, value["maximum_TV"], value["first_deviation"],
              value["earliest_incorrect_constituent_signature"], value["constituent_error_relation"],
              value["descriptive_hypothesis"]]
             for name, value in row["worst_history_prefix_diagnosis"]["worst_histories"].items()])
        text += table(["Clear-N anchor", "Boards", "Correct N signatures", "Response TV", "Valid anchor",
                       "N0–N8 maximum TVs", "Violating N lengths", "Recurrence evidence"],
            [[c["anchor"], c["boards"], c["correct_N_signatures"], c["constituent_response_maximum_TV"],
              c["valid_anchor"], c["per_length_maximum_TV"], c["violating_N_lengths"],
              c["recurrence_evidence"]] for c in row["diagnosis_summary"]["clear_neutral"]])
        text += table(["Registered swap case", "Count", "Mean TV", "Max TV"],
            [[key, v["count"], v["mean_TV"], v["maximum_TV"]]
             for key, v in row["registered_swap_summary"]["cases"].items()])
        text += ["Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.", ""]
    return "\n".join(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("register", "calibrate", "run", "aggregate", "verify-gpu"), required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--runs", choices=tuple(GROUPS), default="rarity")
    parser.add_argument("--run-name", action="append", default=[])
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--chunk-runs", type=int)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-root", type=Path, default=OUTPUT)
    parser.add_argument("--bulk-root", type=Path, default=BULK)
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--verification-output", type=Path)
    args = parser.parse_args()
    device = r11.configure(args.device)
    if args.stage == "register":
        result = register(device)
        result = {"runs": len(result["runs"]), "frozen_A": result["frozen_A"]}
    elif args.stage == "calibrate":
        result = calibration(device)["checks"]
    elif args.stage == "verify-gpu":
        result = verification(device, trace=args.trace, destination=args.verification_output)
    elif args.stage == "aggregate":
        result = aggregate(args.output_root)
    else:
        if not 0 <= args.steps <= 20000 or (args.steps != 20000 and not args.smoke):
            raise ValueError("r12 only smoke may change the registered horizon")
        selected = [r for r in all_runs() if r.arm in GROUPS[args.runs]]
        if args.run_name:
            selected = [r for r in selected if r.name in args.run_name]
            if len(selected) != len(set(args.run_name)):
                raise ValueError("r12 explicit run identity differs")
        elif args.smoke:
            selected = [r for r in selected if r.law == "original" and
                        (r.seed == 0 if args.runs == "rarity" else True)]
        width = args.chunk_runs or WIDTHS[args.runs]
        if width != WIDTHS[args.runs]:
            raise ValueError("r12 execution width differs from registration")
        result = []
        for start in range(0, len(selected), width):
            result += run_chunk(selected[start:start + width], device, args.output_root,
                                args.bulk_root, steps=args.steps, smoke=args.smoke)
    print(json.dumps(result, indent=2), flush=True)
    if args.stage == "verify-gpu" and not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
