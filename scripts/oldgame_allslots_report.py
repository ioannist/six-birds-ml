"""Report-only scoring of recorded r10 audits; no model evaluation or fitting."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from recombination_promotion.public_paths import public_path


LARGE_FILE_BYTES = 1_000_000
CONCLUSION = ("All-slot B supervision improves all-slot sum readability, but neither "
              "robust B nor selective A-mediated use was established.")


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def reference(path):
    return {"path": str(Path(path).resolve()), "sha256": digest(path),
            "bytes": Path(path).stat().st_size}


def positive_validity(positive, *, step):
    support = 0 if positive is None else positive["accurate_unpatched_pairs"]
    rate = None if positive is None else positive["donor_follow_rate_among_accurate"]
    valid = step == 20000 and support >= 20 and rate is not None and rate >= .95
    return {"valid": valid, "status": "VALID" if valid else "INVALID_OR_MISSING",
            "step": step, "accurate_pairs": support, "donor_follow_rate": rate,
            "CI95": None if positive is None else positive["donor_follow_CI95"]}


def patch_components(study, observed, positive, prelaunch, shuffled, *, arm, law, positive_step):
    """Calibration, selectivity, and use are separate propositions."""
    positive_result = positive_validity(positive, step=positive_step)
    support = observed["accurate_unpatched_pairs"]
    rate = observed["donor_follow_rate_among_accurate"]
    selectivity = {"passes": observed["other_slot_probe_changes"] == 0,
                   "other_slot_decoded_changes": observed["other_slot_probe_changes"],
                   "evaluated_pairs": observed["evaluated_pairs"]}
    if law == "equal":
        control = study.intervention_gate(observed, None, None, None, equal=True)
        return {"status": "EQUAL_LAW_CONTROL_ONLY", "trained_positive": {
                    "status": "NOT_APPLICABLE", "valid": None},
                "negative_calibration": {"status": "NOT_APPLICABLE", "valid": None},
                "selectivity": {**selectivity, "role": "DESCRIPTIVE_ONLY"},
                "use_test": {"status": "NOT_APPLICABLE", "passes": None},
                "equal_law_control": control, "passes": control["passes"]}
    if arm == "a_forced":
        negative = {"status": "NOT_APPLICABLE", "valid": None,
                    "reason": "Shuffling raw alignment does not change the hard-answer patch."}
        return {"status": "KNOWN_USE_POSITIVE_VALID" if positive_result["valid"] else "KNOWN_USE_POSITIVE_INVALID",
                "trained_positive": positive_result, "negative_calibration": negative,
                "selectivity": selectivity,
                "use_test": {"status": "KNOWN_USE_POSITIVE_NOT_FREE_NETWORK_TEST", "passes": None},
                "passes": positive_result["valid"] and selectivity["passes"]}
    null_support = 0 if shuffled is None else shuffled["accurate_unpatched_pairs"]
    null_rate = None if shuffled is None else shuffled["donor_follow_rate_among_accurate"]
    null_valid = null_support >= 20 and null_rate is not None and null_rate <= .20
    negative = {"status": "CALIBRATED" if null_valid else "UNCALIBRATED",
                "valid": null_valid, "accurate_pairs": null_support, "donor_follow_rate": null_rate,
                "CI95": None if shuffled is None else shuffled["donor_follow_CI95"]}
    calibrated = positive_result["valid"] and prelaunch["passes"] and null_valid
    follow_pass = support >= 20 and rate is not None and rate >= .80
    use_pass = calibrated and follow_pass and selectivity["passes"]
    return {"status": "CALIBRATED" if calibrated else "UNCALIBRATED",
            "trained_positive": positive_result, "negative_calibration": negative,
            "prelaunch_calibration_valid": prelaunch["passes"], "selectivity": selectivity,
            "use_test": {"passes": use_pass, "accurate_pairs": support,
                "donor_follow_rate": rate, "donor_follow_bar_pass": follow_pass,
                "CI95": observed["donor_follow_CI95"]}, "passes": use_pass}


def endpoint_label(study, row, rows):
    if row["smoke"]:
        return "SMOKE_NOT_ENDPOINT"
    if row["futility_stop"]:
        return "EQUAL_LAW_CONTROL_FUTILITY_STOP" if row["law"] == "equal" else "FUTILITY_STOP"
    if row["law"] == "equal":
        control_pass = row["endpoint_B_pass"] and all(p["passes"] for p in row["patches"].values())
        return "EQUAL_LAW_CONTROL_PASS" if control_pass else "EQUAL_LAW_CONTROL_INCOMPLETE"
    if row["arm"] == "a_forced":
        return "SUPPLIED_A_REFERENCE_B_PASS" if row["endpoint_B_pass"] else "B_INCOMPLETE"
    result = study.endpoint_claim(row["endpoint_B_pass"], row["five_sum_readability"],
                                 all(p["use_test"]["passes"] for p in row["patches"].values()))
    if row["arm"] == "free" and not row["endpoint_B_pass"]:
        counterparts = [rows.get(study._name(arm, "original", row["seed"]))
                        for arm in ("free_a", "a_forced")]
        if any(r and r["last_step"] == row["last_step"] and r["endpoint_B_pass"] for r in counterparts):
            result = "ACCESS_TO_A_HELPS_SPONTANEOUS_USE_NOT_ESTABLISHED"
    return result


def failed_b_bars(row):
    measured, bars = row["law_cases"], row["endpoint_B_bars"]
    failures = {}
    for key, field in (("natural_KL", "KL_bits"), ("covered_value_KL", "covered_value_KL_bits")):
        if not bars[key]:
            failures[key] = {"value": measured["natural"][field], "bound": bars["bounds"][key],
                             "relation": "<="}
    if not bars["constructed_law_TV"]:
        bound = .02 if row["law"] == "equal" else .05
        failures["constructed_law_TV"] = {"bound": bound, "relation": "<=", "cases": {
            name: {"value": measured[name]["maximum_TV"],
                   "passes": measured[name]["maximum_TV"] <= bound}
            for name in ("law_rows", "witness", "eight_hold")}}
    if not bars["same_board_witness"]:
        key = "maximum_prediction_pair_TV" if row["law"] == "equal" else "minimum_prediction_pair_TV"
        value = measured["witness"][key]
        bound = .02 if row["law"] == "equal" else .05
        separation_pass = value <= bound if row["law"] == "equal" else value >= bound
        failures["same_board_witness"] = {
            "exact_row_maximum_TV": {"value": measured["witness"]["maximum_TV"], "bound": .05,
                                     "relation": "<=", "passes": measured["witness"]["maximum_TV"] <= .05},
            key: {"value": value, "bound": bound,
                  "relation": "<=" if row["law"] == "equal" else ">=", "passes": separation_pass}}
    return failures


def probe_summary(study, gains):
    result = []
    for site, families in gains.items():
        for family, tasks in families.items():
            for task, entries in tasks.items():
                for entry in entries:
                    rare = entry["rare_rendering"]["per_value"]
                    selected = [str(study.VALUE_INDEX[v]) for v in study.VALUES36 if v >= 28] if task == "sum" else list(rare)
                    selected_counts = [rare[k] for k in selected]
                    result.append({"site": site, "family": family, "task": task, "slot": entry["slot"],
                        **{k: entry[k] for k in ("before", "endpoint", "gain", "paired_CI95", "correct", "total",
                                               "majority_floor", "positive_accuracy", "fits_converged",
                                               "readability_gain", "rare_readable")},
                        "shuffled_accuracy": entry["shuffled_floor"]["accuracy"],
                        "heldout_values_covered": sum(v["total"] > 0 for v in entry["per_value"].values()),
                        "heldout_values_missing": [k for k,v in entry["per_value"].items() if v["total"] == 0],
                        "rare_shared_identity_correct": sum(v["correct"] for v in selected_counts),
                        "rare_shared_identity_total": sum(v["total"] for v in selected_counts),
                        "rare_minimum_value_support": min(v["total"] for v in selected_counts),
                        "rare_scope": "SHARED_IDENTITY_HELDOUT_RENDERINGS_NOT_BOARD_DISJOINT"})
    return result


def compact_report(study, detailed, details_reference, relocated):
    report = {k:v for k,v in detailed.items() if k != "rows"}
    report["detailed_artifact"] = details_reference
    report["relocated_artifacts"] = relocated
    report["rows"] = {}
    for name,row in detailed["rows"].items():
        selected = {k:v for k,v in row.items() if k not in (
            "endpoint_probe_gains", "endpoint_interchange", "endpoint_shuffled_interchange", "law_cases")}
        selected["probe_summary"] = probe_summary(study, row["endpoint_probe_gains"])
        selected["law_cases"] = {case: {k:value[k] for k in (
            "rounds", "KL_bits", "covered_value_KL_bits", "maximum_TV", "covered_rounds", "uncovered_cells",
            "minimum_prediction_pair_TV", "maximum_prediction_pair_TV", "prediction_rerender_maximum_TV") if k in value}
            for case,value in row["law_cases"].items()}
        selected["interchange_summary"] = {slot: {k:p[k] for k in (
            "evaluated_pairs", "eligible_pairs", "accurate_unpatched_pairs", "donor_follow_count",
            "donor_follow_rate_among_accurate", "donor_follow_CI95", "other_slot_probe_changes")}
            for slot,p in row["endpoint_interchange"]["slots"].items()}
        report["rows"][name] = selected
    return report


def markdown(report):
    lines = ["# r10 saved-audit aggregate", "", report["conclusion"], "",
             "The probes establish increased decoding on sampled support, not exact full-A computation. "
             "Rare values are missing from ordinary held-out probes; the shared-identity rendering panel "
             "does not meet the rare-readability bar. The r8 comparison is historical, not matched.", "",
             "The trained a_forced positives pass. Calibrated negatives and passed use tests are different "
             "statements: original-law raw arms fail selectivity. Equal-law runs are controls only.", "",
             "## Registered readings (verbatim)", "", report["registered_readings_verbatim"], "",
             "## Endpoint B results", "",
             "| Run | Label | First crossing | Natural KL | B pass |",
             "|---|---|---|---|---|"]
    for name,row in report["rows"].items():
        lines.append(f"| {name} | {row['same_checkpoint_label']} | {row['first_audited_B_crossing']} | "
                     f"{row['law_cases']['natural']['KL_bits']:.8g} | {row['endpoint_B_pass']} |")
    lines += ["", "## Failed B bars (unchanged thresholds)", "",
              "| Run | Bar | Measured values and bounds |", "|---|---|---|"]
    for name,row in report["rows"].items():
        for bar,values in row["failed_B_bars"].items():
            lines.append(f"| {name} | {bar} | {json.dumps(values, sort_keys=True)} |")
    lines += ["", "## Fixed-endpoint trained positives", "",
              "| Seed | Slot | Accurate pairs | Donor-follow | CI95 | Positive valid |",
              "|---|---|---|---|---|---|"]
    for row in report["rows"].values():
        if row["arm"] == "a_forced" and row["law"] == "original":
            for slot,p in row["patches"].items():
                v = p["trained_positive"]
                lines.append(f"| {row['seed']} | {slot} | {v['accurate_pairs']} | {v['donor_follow_rate']} | {v['CI95']} | {v['valid']} |")
    lines += ["", "## Calibration, spillover and use-test results", "",
              "| Run | Slot | Positive valid | Negative status / rate / support | Other-slot decoded changes | Selectivity | Use-test pass |",
              "|---|---|---|---|---|---|---|"]
    for name,row in report["rows"].items():
        for slot,p in row["patches"].items():
            n = p["negative_calibration"]
            lines.append(f"| {name} | {slot} | {p['trained_positive']['valid']} | "
                         f"{n['status']} / {n.get('donor_follow_rate')} / {n.get('accurate_pairs')} | "
                         f"{p['selectivity']['other_slot_decoded_changes']} | {p['selectivity']['passes']} | "
                         f"{p['use_test']['passes']} |")
    lines += ["", "## All-slot sum probes", "",
              "| Run | Site | Reader | Slot | Start → end | Gain CI95 | Correct / held-out | Values covered / 36 | Rare correct / total | Rare min support | Converged | Rare bar |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name,row in report["rows"].items():
        for p in row["probe_summary"]:
            if p["task"] != "sum":
                continue
            lines.append(f"| {name} | {p['site']} | {p['family']} | {p['slot']} | "
                f"{p['before']:.6f} → {p['endpoint']:.6f} | {p['paired_CI95']} | {p['correct']}/{p['total']} | "
                f"{p['heldout_values_covered']}/36 | {p['rare_shared_identity_correct']}/{p['rare_shared_identity_total']} | "
                f"{p['rare_minimum_value_support']} | {p['fits_converged']} | {p['rare_readable']} |")
    lines += ["", "## Detailed artifacts", "", "Paths, byte counts and SHA-256 values:", "",
              json.dumps({"details": report["detailed_artifact"], "relocated": report["relocated_artifacts"],
                          "storage_status": report["storage_status"]}, indent=2), "",
              report["scope_verbatim"], ""]
    return "\n".join(lines)


def relocate_large_files(output, destination):
    """Preserve exact bytes and logical calibration paths; never overwrite details."""
    destination.mkdir(parents=True, exist_ok=True)
    moved = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.stat().st_size < LARGE_FILE_BYTES:
            continue
        checksum = digest(path)
        target = destination / (path.name + "." + checksum + ".saved")
        if path.is_symlink() and path.resolve() == target.resolve():
            continue
        if target.exists():
            if digest(target) != checksum:
                raise ValueError("r10 relocated artifact digest differs")
        else:
            temporary = target.with_suffix(target.suffix + ".pending")
            shutil.copyfile(path, temporary)
            if digest(temporary) != checksum:
                raise ValueError("r10 relocation copy differs")
            os.replace(temporary, target)
        # Replacing a source by a symlink preserves its logical path and file hash.
        # Aggregate paths will subsequently be replaced by compact regular files.
        link = path.with_name(path.name + ".relocation-link")
        link.symlink_to(target.resolve())
        os.replace(link, path)
        moved.append({"original_path": str(path), **reference(target)})
    return moved


def publish_reports(study, report, output, bulk_root, requested_root):
    details = bulk_root / "report_details"
    details.mkdir(parents=True, exist_ok=True)
    report["storage_status"] = ("REQUESTED_BULK_ROOT" if bulk_root.resolve() == requested_root.resolve()
                                else "STAGED_MANAGER_RELOCATION_REQUIRED")
    report["requested_bulk_root"] = str(requested_root)
    report["actual_bulk_root"] = str(bulk_root)
    temporary = details / "aggregate_detailed.pending.json"
    study.write_json(temporary, report)
    checksum = digest(temporary)
    detailed_path = details / f"aggregate_detailed.{checksum}.json"
    if detailed_path.exists() and digest(detailed_path) != checksum:
        raise ValueError("r10 detailed aggregate digest differs")
    os.replace(temporary, detailed_path)
    manifest_path = output / "bulk_artifact_references.json"
    prior = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    # A later distribution invocation can copy staged immutable files into the requested
    # destination without evaluating models or changing any measurements.
    preserved = details / "preserved"
    preserved.mkdir(parents=True, exist_ok=True)
    migrated = []
    for item in prior:
        source = public_path(item["path"])
        if digest(source) != item["sha256"]:
            raise ValueError("r10 preserved artifact digest differs")
        target = preserved / source.name
        if source.resolve() != target.resolve():
            if target.exists() and digest(target) != item["sha256"]:
                raise ValueError("r10 preserved destination differs")
            if not target.exists():
                shutil.copyfile(source,target)
            if digest(target) != item["sha256"]:
                raise ValueError("r10 preserved migration copy differs")
        migrated.append({**item, **reference(target)})
    moved = relocate_large_files(output, preserved)
    moved = list({(r["original_path"],r["sha256"]):r for r in migrated+moved}.values())
    study.write_json(manifest_path,moved)
    compact = compact_report(study, report, reference(detailed_path), moved)
    # Do not write through symlinks to preserved detailed records.
    compact_path = output / "aggregate.compact.pending.json"
    compact_path.write_text(json.dumps(compact, sort_keys=True, separators=(",", ":")) + "\n")
    os.replace(compact_path, output / "aggregate.json")
    text_path = output / "aggregate.compact.pending.md"
    text_path.write_text(markdown(compact))
    os.replace(text_path, output / "aggregate.md")
    return compact


def aggregate_saved(study, output, bulk_root):
    """The saved registration describes training; report source identities are separate."""
    from scripts.oldgame_allslots_execution import BULK

    requested = BULK
    bulk_root = requested if bulk_root is None else Path(bulk_root)
    registered = json.loads((study.OUTPUT / "registration.json").read_text())
    calibration = json.loads((study.OUTPUT / "calibration.json").read_text())
    if calibration["registration_sha256"] != study.sha(study.OUTPUT / "registration.json"):
        raise ValueError("r10 recorded calibration binding differs")
    if registered["outcome_table_verbatim"] != study.text_rules()["outcome_table_verbatim"]:
        raise ValueError("r10 registered readings differ")
    if registered["spec_sha256"] != study.sha(study.SPEC):
        raise ValueError("r10 registered specification differs")
    for filename,key in (("board_split.json","board_split_sha256"),
                         ("probe_split.json","probe_split_sha256"),
                         ("interchange_pairs.json","interchange_pairs_sha256")):
        if digest(study.OUTPUT / filename) != registered[key]:
            raise ValueError("r10 recorded allocation or pair list differs")
    boards = study.enumerate_boards()
    split = json.loads((study.OUTPUT / "probe_split.json").read_text())
    rows, references = {}, {}
    for arm in study.ARMS:
        for law in study.LAWS:
            for seed in study.SEEDS:
                name = study._name(arm,law,seed)
                path = output / name / "summary.json"
                if not path.exists():
                    continue
                summary = json.loads(path.read_text())
                if (summary["authority"]["registration_sha256"] != study.sha(study.OUTPUT / "registration.json") or
                    summary["authority"]["calibration_sha256"] != study.sha(study.OUTPUT / "calibration.json")):
                    raise ValueError("r10 saved run authority differs")
                checkpoints = {}
                for ref in summary["curve"]:
                    source = public_path(ref["path"])
                    if digest(source) != ref["sha256"]:
                        raise ValueError("r10 aggregate audit digest differs")
                    checkpoints[ref["step"]] = json.loads(source.read_text())["audit"]
                if 0 not in checkpoints or summary["last_step"] not in checkpoints:
                    raise ValueError("r10 saved audit series incomplete")
                final = checkpoints[summary["last_step"]]
                bars = study._b_pass(final,calibration,law)
                gains = study._probe_gain(final["probes"], checkpoints[0]["probes"],
                                           calibration["probe"]["oracle"],split,boards)
                readable = all(any(gains[site][family]["sum"][slot]["readability_gain"] and
                    gains[site][family]["sum"][slot]["rare_readable"]
                    for site in ("raw","upper") for family in ("linear","mlp64")) for slot in range(5))
                rows[name] = {"arm":arm,"law":law,"seed":seed,"last_step":summary["last_step"],
                    "smoke":summary["smoke"],"futility_stop":summary["futility_stop"],
                    "first_audited_B_crossing":next((step for step,audit in checkpoints.items()
                        if all(v for k,v in study._b_pass(audit,calibration,law).items() if k != "bounds")),None),
                    "endpoint_B_bars":bars,"endpoint_B_pass":not summary["smoke"] and
                        summary["last_step"] == 20000 and all(v for k,v in bars.items() if k != "bounds"),
                    "endpoint_probe_gains":gains,"five_sum_readability":readable,
                    "A_interface":final["A_interface"],"law_cases":final["B"],
                    "endpoint_interchange":final["interchange"],
                    "endpoint_shuffled_interchange":final["shuffled_interchange"],
                    **{k:summary[k] for k in ("observed_current_slot_value_counts","observed_current_by_Q_counts",
                        "observed_current_query_value_counts","observed_remembered_query_value_counts")},
                    "B_curve":[{"step":step,"natural_KL":a["B"]["natural"]["KL_bits"],
                                "bars":study._b_pass(a,calibration,law)} for step,a in checkpoints.items()]}
                references[name] = {"summary":reference(path),"audits":summary["curve"]}
                del checkpoints
    for name,row in rows.items():
        positive_row = rows.get(study._name("a_forced",row["law"],row["seed"]))
        eligible = positive_row is not None and not positive_row["smoke"] and positive_row["last_step"] == 20000
        row["patches"] = {str(slot):patch_components(study,
            row["endpoint_interchange"]["slots"][str(slot)],
            positive_row["endpoint_interchange"]["slots"][str(slot)] if eligible else None,
            calibration["intervention_calibration_status"][str(slot)],
            row["endpoint_shuffled_interchange"]["slots"][str(slot)],
            arm=row["arm"],law=row["law"],positive_step=20000 if eligible else None) for slot in range(5)}
        row["same_checkpoint_positive_step"] = 20000 if eligible and row["law"] == "original" else None
        row["failed_B_bars"] = failed_b_bars(row)
        row["internal_use_scope"] = ("CONTROL_ONLY" if row["law"] == "equal" else
                                     "KNOWN_USE_REFERENCE" if row["arm"] == "a_forced" else
                                     "USE_TEST_PASS" if all(p["use_test"]["passes"] for p in row["patches"].values())
                                     else "USE_TEST_NOT_ESTABLISHED")
    for row in rows.values():
        row["same_checkpoint_label"] = endpoint_label(study,row,rows)
    report = {"registration_sha256":study.sha(study.OUTPUT / "registration.json"),
              "calibration_sha256":study.sha(study.OUTPUT / "calibration.json"),
              "registered_readings_verbatim":registered["outcome_table_verbatim"],
              "scope_verbatim":study.text_rules()["scope_verbatim"],"conclusion":CONCLUSION,
              "report_scope":"SAVED_AUDITS_ONLY_NO_TRAINING_NO_MODEL_EVALUATION_NO_PROBE_REFITS",
              "training_source_identities":registered["source_identities"],
              "report_source_identities":{str(p):digest(p) for p in (Path(__file__), Path(study.__file__))},
              "source_artifacts":references,"rows":rows}
    compact = publish_reports(study,report,output,bulk_root,requested)
    return {"run_count":len(rows),"storage_status":compact["storage_status"],
            "detailed_artifact":compact["detailed_artifact"],
            "same_checkpoint_labels":{name:r["same_checkpoint_label"] for name,r in rows.items()}}
