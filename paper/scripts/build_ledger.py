"""Build the write-up evidence index and numbers; never train or alter study files.

The explicit --pin step records the evidence present at preparation time. A normal
build/check cannot update those pins. Numeric assertions below are independent of
the artifact hashes: replacing a source and re-pinning cannot change an outline
claim unnoticed. Archive copies work with --archive-root and need no /mnt paths.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import statistics
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger_contract as contract

ROOT = Path(__file__).resolve().parents[2]
BASE = Path("reports/phase11/oldgame_memory/multiround")
STUDIES = {8: "r8_route_access", 9: "r9_raw_diagnosis", 10: "r10_allslots",
           11: "r11_jagged", 12: "r12_coverage", 13: "r13_mechanism"}
MANIFEST = Path("paper/notes/evidence_manifest.json")
JI = Path("paper/notes/interpretation.md")
SUPPORT_CACHE = {}
PATH_CACHE = {}
BULK = ROOT / "evidence/bulk/paper_data_bulk"
STAGED_BULK = BULK
PUBLIC_STAGE = ROOT / "evidence/public"


def portable_path(path, root):
    value = str(path)
    for prefix, base in (("repo/", root), ("repo/", root),
                         ("bulk/", root / "evidence/bulk"),
                         ("build/", root / "evidence/bulk"),
                         ("bulk/", root / "evidence/bulk")):
        if value.startswith(prefix):
            return base / value[len(prefix):]
    path = Path(value)
    return path if path.is_absolute() else root / path


def small_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")) + "\n"


def paper_table(value, pointer="", depth=0):
    """Keep compact report cells; bind large detailed subtrees, without rounding."""
    if depth >= 3 and len(small_json(value).encode()) > 1_500 and (
            isinstance(value, list) or isinstance(value, dict) and len(value) > 100):
        return {"detail_pointer": pointer,
                "sha256": hashlib.sha256(canonical(value).encode()).hexdigest(),
                "detail": "Hash-bound owning source; report-level receipts use report_table_sources.json"}
    if isinstance(value, dict):
        return {k: paper_table(v, pointer + "/" + str(k), depth + 1)
                for k, v in value.items()}
    if isinstance(value, list):
        return [paper_table(v, pointer + "/" + str(i), depth + 1)
                for i, v in enumerate(value)]
    return value


def reported_probe_cells(value, pointer=""):
    """Actual appendix probe counts/intervals, separate from detailed fit arrays."""
    rows = []
    if isinstance(value, dict):
        if "paired_CI95" in value and any(k in value for k in ("endpoint", "endpoint_accuracy")):
            keys = {"before", "update0_accuracy", "endpoint", "endpoint_accuracy", "correct",
                    "total", "update0_counts", "endpoint_counts", "gain", "paired_CI95",
                    "majority_floor", "oracle_floor", "positive_accuracy", "shuffled_floor",
                    "converged", "fits_converged", "family", "site", "slot", "task"}
            rows.append({"full_table_pointer": pointer,
                         **{k: v for k, v in value.items() if k in keys}})
        else:
            for k, v in value.items():
                rows.extend(reported_probe_cells(v, pointer + "/" + str(k)))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            rows.extend(reported_probe_cells(v, pointer + "/" + str(i)))
    return rows


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False,
                      allow_nan=False) + "\n"


def publish(path: Path, content: str, check: bool) -> None:
    if check:
        if not path.exists() or path.read_text() != content:
            raise ValueError(f"rebuild differs: {path}")
    else:
        # Artifact outputs, not source-code edits. Keep all study inputs read-only.
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def study_path(study: int) -> Path:
    return BASE / f"study_{STUDIES[study]}"


def archive_path(path: Path, root: Path) -> str:
    path = path.resolve()
    layout = root / "paper/notes/public_layout.json"
    if layout.is_file() and path.is_relative_to(root.resolve()):
        relative = path.relative_to(root.resolve()).as_posix()
        mapped = json.loads(layout.read_text())["archive_map"].get(relative)
        if mapped:
            return mapped
    if path.is_relative_to(root.resolve()):
        return "repo/" + path.relative_to(root.resolve()).as_posix()
    for marker in ("/runs/", "/tmp/"):
        if marker in str(path):
            return "bulk/" + str(path).split(marker, 1)[1]
    return "external/" + path.name


def evidence_id(path: str) -> str:
    return "E-" + hashlib.sha256(path.encode()).hexdigest()[:16]


def references(value: Any):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
            yield value
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def role(path: Path) -> str:
    name = path.name.lower()
    if "checkpoint" in name or path.suffix == ".pt":
        return "checkpoint"
    if "registration" in name:
        return "registration"
    if "calibration" in name:
        return "calibration"
    if "review" in name or "specification" in name:
        return "reproduction_authority"
    if "command" in name or "launch" in name:
        return "command_record_not_proof_of_execution"
    if "summary" in name:
        return "run_summary"
    if "aggregate" in name or "report" in name:
        return "report_correction"
    return "evidence"


def pin(root: Path) -> dict:
    files: dict[str, dict] = {}
    unresolved = []
    aliases = {}

    def add(path: Path, study=None, expected=None):
        path = portable_path(path, root)
        if not path.is_file():
            if expected:
                unresolved.append({"archive_path": archive_path(path, root),
                                   "expected_sha256": expected,
                                   "status": "HISTORICAL_REFERENCE_NOT_AVAILABLE_AT_THIS_PATH"})
            return
        public = archive_path(path, root)
        if path.absolute().is_relative_to(root):
            alias = "repo/" + path.absolute().relative_to(root).as_posix()
            if alias != public:
                aliases[alias] = public
        if public in files:
            return
        actual = sha(path)
        if expected and actual != expected:
            # A historical authority can have the same name as a later correction.
            matches = [p for p in path.parent.glob(path.stem + "*" + path.suffix)
                       if p.is_file() and sha(p) == expected]
            if matches:
                add(matches[0], study, expected)
            else:
                unresolved.append({"archive_path": public, "expected_sha256": expected,
                                   "current_sha256": actual,
                                   "status": "HISTORICAL_VERSION_DIFFERS_FROM_CURRENT"})
            # Still pin the current report; do not represent it as the executed version.
        files[public] = {"id": evidence_id(public), "archive_path": public,
                         "sha256": actual, "bytes": path.stat().st_size,
                         "study": study, "role": role(path),
                         "internal": {"path": "repo/" + path.relative_to(root).as_posix()}}
        if path.suffix == ".json" and path.stat().st_size < 80_000_000:
            try:
                for ref in references(json.loads(path.read_text())):
                    add(Path(ref["path"]), study, ref["sha256"])
            except (json.JSONDecodeError, UnicodeError):
                pass

    for number in STUDIES:
        folder = root / study_path(number)
        for path in sorted(folder.rglob("*")):
            if path.is_file() and path.suffix in {".json", ".md", ".log", ".pt"}:
                add(path, number)
        # Endpoint/source checkpoints need not occur in a compact report reference.
    # Only the numerical evidence distributed with this public copy is pinned.
    layout = json.loads((root / "paper/notes/public_layout.json").read_text())
    for relative in layout["archive_map"]:
        path = root / relative
        number = next((n for n in STUDIES if f"study_r{n}_" in relative), None)
        add(path, number)
    for path in (root / 'evidence/gate_A').rglob('*'):
        if path.is_file():
            add(path)
    for path in (root / 'evidence/panels').rglob('*'):
        if path.is_file():
            add(path)
    add(Path('evidence/identity_projections.json'))
    for directory in ('study_r12_coverage_bulk', 'study_r13_mechanism_bulk/report_revision'):
        for path in (root / 'evidence/bulk' / directory).rglob('*'):
            if path.is_file():
                add(path)
    add(Path("paper/notes/public_layout.json"))
    for relative in (JI, Path("paper/notes/outline.md"),
                     Path("paper/notes/notation_and_terminology.md"),
Path("paper/style/source_pins_verbatim.md"),
                     Path("paper/style/CORPUS.md"), Path("paper/style/VENUE_FORMAT.md")):
        add(relative)
    for pattern in ("scripts/multiround_scoring*.py", "scripts/oldgame_*report.py",
                    "src/recombination_promotion/oldgame_ext/multiround*.py",
                    "src/recombination_promotion/oldgame_ext/jagged_probes.py",
                    "src/recombination_promotion/oldgame_ext/game.py",
                    "src/recombination_promotion/serialization/minimal_recombination.py"):
        for path in sorted(root.glob(pattern)):
            add(path)
    for path in ("paper/scripts/build_ledger.py", "paper/scripts/check_package.py",
                 "paper/requirements.txt", "paper/references.bib", "LICENSE", "LICENSE-CC-BY-4.0",
                 "paper/notes/licensing.md", "paper/main.tex", "paper/includes/release_metadata.tex",
                 "paper/supplement/supplement.tex",
                 "paper/scripts/ledger_contract.py",
                 "paper/notes/outline_claims.json", "paper/notes/measurement_metadata.json",
                 "paper/requirements-analysis.txt", "paper/notes/bibliography_verification.md"):
        add(Path(path))
    # Package initializers import further exact-task modules. Pin the source tree;
    # only the modules actually executed enter the numerical public subset.
    for path in sorted((root / "src").rglob("*.py")):
        add(path)
    for path in sorted((root / "paper/notes").glob("measurement_metadata_*.json")):
        add(path)
    for path in sorted((root / 'paper/scripts').glob('*.py')):
        add(path)
    # Prose is an input, unlike generated figure/table TeX. Bind late additions
    # (including end matter) without creating an asset/ledger hash cycle.
    for directory in ('sections', 'appendices', 'includes'):
        for path in sorted((root / 'paper' / directory).glob('*.tex')):
            add(path)
    add(Path("reports/phase11/oldgame_memory/continuous/continuous_seed0_r7/"
             "trajectories/parent_A_step_002000.pt"))
    # Explicit pin preparation rebuilds only derived full appendix outputs.
    full_controls, full_calibration = {}, {}
    for number in STUDIES:
        value = json.loads((root / study_path(number) / ("results.json" if number == 9 else "aggregate.json")).read_text())
        rows = value.get("rows", value.get("runs"))
        if number == 11:
            rows = {k: r for group in ("rarity", "dose", "erosion") for k, r in value[group].items()}
        if number == 13:
            rows = {f"{group}_{i}": r for group, rr in value["experiments"].items() for i, r in enumerate(rr)}
        full_controls[number] = contract.sanitize(compact(rows))
        if number != 9:
            path = root / study_path(number) / "calibration.json"
            public = archive_path(path, root)
            full_calibration[number] = {"evidence_id": evidence_id(public),
                                       "calibration": contract.sanitize(compact(json.loads(path.read_text())))}
    for name, value in (("control_tables.json", full_controls), ("calibration_tables.json", full_calibration)):
        staged = STAGED_BULK / name
        if staged.exists() and staged.read_text() != canonical(value):
            previous = staged.with_name(staged.stem + "_build_r2.json")
            if not previous.exists():
                publish(previous, staged.read_text(), False)
        publish(staged, canonical(value), False)
        target = BULK / name
        source = target if target.exists() else staged
        if source.read_text() != canonical(value):
            raise ValueError(f"Host bulk table differs from rebuilt evidence: {name}")
        public = "bulk/paper_data_bulk/" + name
        files[public] = {"id": evidence_id(public), "archive_path": public,
                         "sha256": sha(source), "bytes": source.stat().st_size,
                         "study": None, "role": "full_appendix_table",
                         "internal": {"path": "repo/" + source.relative_to(root).as_posix(),
                                      "destination": "repo/" + target.relative_to(root).as_posix()}}
    numerical_ids = set()
    subset_path = root / "paper/notes/public_evidence_subset.json"
    if subset_path.exists():
        numerical_ids = {a["id"] for a in json.loads(subset_path.read_text())["files"]}
    for entry in files.values():
        path = portable_path(entry["internal"]["path"], root)
        if (path.suffix in {".json", ".md", ".log"} or ".json." in path.name) and (entry["id"] in numerical_ids or
                entry["role"] in {"registration", "calibration", "full_appendix_table"} or
                entry["archive_path"].startswith("repo/paper/notes/")):
            entry["public_projection"] = contract.publish_projection(entry, path, PUBLIC_STAGE)
            entry["internal"]["public_projection_path"] = "repo/" + (
                PUBLIC_STAGE / Path(entry["public_projection"]["path"]).name).relative_to(root).as_posix()
    histories = []
    for number in STUDIES:
        subset = [v for v in files.values() if v["study"] == number]
        histories.append({"study": number, "hardware": (
            "CPU-era; processor model not recorded in saved per-run summaries"
            if number < 10 else "selected GPU / CUDA fp32 execution recorded in summaries and host "
            "verification; GPU model and driver not recorded in the public study artifacts"),
            "commands": [v["id"] for v in subset if v["role"].startswith("command")],
            "execution_records": [v["id"] for v in subset if v["role"] == "run_summary"],
            "exact_shell_invocation": "NOT_RECORDED_IN_RUN_SUMMARIES; archived host commands "
            "are instruction records, not proof of the shell invocation actually used",
            "versions_and_specifications": [v["id"] for v in subset if v["role"] in
                {"registration", "calibration", "archived_review", "report_correction"}],
            "interpretation": "Registered endpoints retained; corrected audits and "
            "supplementary analyses are separate from training authority. Command "
            "instructions alone do not establish the hardware or command actually used."})
    return {"schema": "writeup_evidence_v1", "hash_algorithm": "sha256",
            "archive_layout": "repo/<repository-relative>; bulk/<bulk-relative>",
            "artifacts": sorted(files.values(), key=lambda v: v["archive_path"]),
            "aliases": aliases,
            "study_history": histories, "historical_unresolved_references": unresolved,
            "public_exclusions": {"excluded_correspondence_files": layout["excluded_correspondence_files_excluded"],
                                  "note": "Private correspondence is not distributed or counted as public evidence."}}


class Evidence:
    def __init__(self, root: Path, manifest: dict, archive: Path | None = None):
        self.root, self.archive = root, archive
        self.entries = {x["archive_path"]: x for x in manifest["artifacts"]}
        for key, entry in list(self.entries.items()):
            if key.startswith("bulk/"):
                self.entries["bulk/" + key.removeprefix("bulk/")] = entry
        for alias, target in manifest.get("aliases", {}).items():
            self.entries[alias] = self.entries[target]
        self.cache = {}
        self.verified = set()

    def path(self, entry: dict) -> Path:
        if self.archive:
            return self.archive / entry.get("public_projection", {}).get("path", entry["archive_path"])
        if "internal" not in entry:
            return self.root.parent / entry.get("public_projection", {}).get("path", entry["archive_path"])
        path = portable_path(entry["internal"]["path"], self.root)
        if not path.exists() and "staged_path" in entry["internal"]:
            return portable_path(entry["internal"]["staged_path"], self.root)
        return path

    def verify(self, entry: dict):
        if entry["id"] not in self.verified:
            path = self.path(entry)
            projection = entry.get("public_projection") if self.archive or "internal" not in entry else None
            if projection and projection["original_sha256"] != entry["sha256"]:
                raise ValueError("public projection original identity differs")
            expected = projection["sha256"] if projection else entry["sha256"]
            if not path.is_file() or sha(path) != expected:
                raise ValueError(f"evidence hash differs: {entry['archive_path']}")
            self.verified.add(entry["id"])

    def load(self, relative: str | Path):
        key = "repo/" + str(relative)
        entry = self.entries[key]
        self.verify(entry)
        if key not in self.cache:
            self.cache[key] = json.loads(self.path(entry).read_text())
        return self.cache[key]

    def id(self, relative: str | Path):
        return self.entries["repo/" + str(relative)]["id"]


def walk_numbers(value: Any, path=()):
    """Inventory reported scalar measurements, not a replacement for their support."""
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_numbers(child, path + (key,))
    elif isinstance(value, list):
        # Large exposure/board arrays stay in referenced evidence, not in the ledger.
        if len(value) <= 210:
            for key, child in enumerate(value):
                yield from walk_numbers(child, path + (key,))
    elif isinstance(value, (int, float, bool)):
        yield path, value


def measurements(value: Any):
    """One ledger entry per reported measurement vector, not per array element.

    The vector's scalar counts and intervals live in the rendered appendix data;
    its complete value is checksum-bound by the entry. This avoids millions of
    duplicated metadata records for the same experimental panel.
    """
    for run, row in value.items():
        if isinstance(row, dict):
            for field, child in row.items():
                if isinstance(child, (int, float, bool, list, dict)):
                    yield (run, field), child


def at(value: Any, path):
    for key in path:
        value = value[key]
    return value


def validate_rates(value: Any, path=""):
    """Check numerator/denominator algebra where artifacts supply both counts."""
    if isinstance(value, dict):
        if {"correct", "total"} <= value.keys():
            n, d = value["correct"], value["total"]
            if not 0 <= n <= d:
                raise ValueError(f"count outside support: {path}")
            for key in ("accuracy", "endpoint"):
                if key in value and d and not math.isclose(value[key], n / d, abs_tol=1e-12):
                    raise ValueError(f"count/rate mismatch: {path}/{key}")
        for key, child in value.items():
            validate_rates(child, path + "/" + key)
    elif isinstance(value, list):
        for key, child in enumerate(value):
            validate_rates(child, path + f"/{key}")


def computations(artifacts: dict[int, dict], evidence=None) -> dict[str, Any]:
    """Recompute outline quantities, never parse numbers out of the outline."""
    game, law = contract.exact_task_sources(evidence)
    P, P_EQUAL = law["P"], law["P_EQUAL"]
    boards, _ = game["whole_endpoints"]()
    counts = [sum((0 if b[0] <= 12 else 2 if b[0] >= 24 else 1) == k
                  for b in boards) for k in range(3)]
    task = {"boards": len(boards), "category_counts": counts,
            "histories": len(game["histories"]()), "sums": len({sum(h) for h in game["histories"]()}),
            "cutoff_band": sum(b[0] in (11, 12, 13, 23, 24, 25) for b in boards),
            "masses": len(game["MASSES"]), "slots": len(next(iter(boards))),
            "records": max(map(len, game["histories"]())),
            "renderings": 1 + len(next(iter(artifacts[12]["runs"].values()))
                                  ["census_all_four_renderings_and_r9"]["additional_fixed_renderings"]),
            "p0": [float(p) for p in P[0]], "p1": [float(p) for p in P[1]],
            "equal_law": [float(p) for p in P_EQUAL]}
    task["complement"] = task["boards"] - task["cutoff_band"]
    task["ideal_loss_bits"] = -sum(p * math.log2(p) for p in task["p0"])
    task["witness_JS_bits"] = sum(p * math.log2(p / q) for p, q in
        zip(task["p0"], task["equal_law"]))
    out = {"task": task}
    anchors = [min(b for b in boards if law["board_category"](b) == c) for c in range(3)]
    off_history, on_history = [anchors[0], anchors[1]], [anchors[2], anchors[1]]
    def endpoint_mode(history):
        mode = 0
        for board in history:
            mode = law["update_mode"](mode, law["board_category"](board))
        return mode
    off, on = endpoint_mode(off_history), endpoint_mode(on_history)
    require_equal([off, on], [0, 1], "task non-factorization witness modes")
    out["theory_nonfactorization"] = {"off_history": off_history, "on_history": on_history,
        "same_neutral_board": off_history[-1] == on_history[-1],
        "off_law": [float(p) for p in P[off]], "on_law": [float(p) for p in P[on]],
        "different_laws": P[off] != P[on], "scope": "Strictness (of the task), not an internal layer."}
    r8, r10, r11, r12, r13 = (artifacts[n] for n in (8, 10, 11, 12, 13))
    out["r8_probes"] = [v for v in r8["raw_only_endpoint_probes"] if v["carrier"] == "raw"]
    mlp = [v["original"]["endpoint_accuracy"] for v in out["r8_probes"]
           if v["probe_family"] == "mlp64" and v["slot"] > 1]
    out["r8_mlp_pooled"] = {"mean": statistics.mean(mlp), "median": statistics.median(mlp),
                            "minimum": min(mlp), "maximum": max(mlp), "slot_seed_cells": len(mlp),
                            "boards_per_cell": 512}
    out["r8_raw_KL"] = [r8["rows"][f"raw_only_original_seed{s}"]["loss_KL_curve"][-1]
                        ["natural_excess_KL_bits"] for s in range(3)]
    out["r8_passes"] = {arm: sum(r8["rows"][f"{arm}_original_seed{s}"]
                                    ["endpoint_label"] == "B_PASS" for s in range(3))
                         for arm in ("raw_only", "a_only", "dual")}
    out["r8_law_TV"] = [r["law_TV"]["maximum_TV"] for r in r8["raw_only_failed_original_bars"]]
    out["r10_free_probes"] = [dict(seed=s, **v) for s in range(3)
        for v in r10["rows"][f"free_original_seed{s}"]["probe_summary"]
        if v["site"] == "raw" and v["family"] == "linear" and v["task"] == "sum"]
    out["r10_spillover"] = [v["other_slot_probe_changes"]
        for k, r in r10["rows"].items() if r["law"] == "original" and r["arm"] in ("free", "free_a")
        for v in r["interchange_summary"].values()]
    out["r10_supplied_pass"] = sum(r10["rows"][f"a_forced_original_seed{s}"]["endpoint_B_pass"]
                                       for s in range(3))
    raw12 = [r for r in r12["runs"].values() if r["law"] == "original"
             and r["arm"] in ("uniform", "cutoff", "decoy")]
    out["r12_raw"] = {"runs": len(raw12), "passes": sum(r["B_pass"] for r in raw12),
        "short": [r["law_panels"]["panels"]["short"]["maximum_TV"] for r in raw12],
        "long": [r["law_panels"]["panels"]["long"]["maximum_TV"] for r in raw12],
        "diagnosis": r12["raw_original_diagnosis_totals"]}
    out["r12_unresolved_prefixes"] = out["r12_raw"]["diagnosis"]["counts"]["unresolved"]
    out["r12_passes"] = {arm: sum(r12["runs"][f"{arm}_original_seed{s}"]["B_pass"]
                                for s in range(3)) for arm in ("a_supplied", "a_target")}
    out["r12_joint"] = r12["A_target_joint_errors"]
    out["r12_supplied_misreads"] = [r12["runs"][f"a_supplied_original_seed{s}"]
        ["census_all_four_renderings_and_r9"]["registered_rendering"]["categorical_misreads"] for s in range(3)]
    selected = r13["selected_readings"]
    out["r13_noise"] = {kind: [selected[str(s)]["noise"]["measurements"][kind]
                                ["categorical_misreads"] for s in range(3)]
                       for kind in ("raw_sampled", "raw_probability", "sums_sampled", "sums_probability")}
    out["r13_access"] = {kind: [selected[str(s)]["access"]["measurements"][kind]
                                for s in range(3)]
                        for kind in ("disconnected", "frozen", "live", "exact")}
    out["r13_encoding"] = {kind: [selected[str(s)]["encoding"]["measurements"][kind]
                                  ["categorical_misreads"] for s in range(3)]
                          for kind in ("numerical", "onehot")}
    out["r13_onehot_passes"] = sum(selected[str(s)]["encoding"]["measurements"]["onehot"]
                                  ["endpoint_label"] == "PASS" for s in range(3))
    out["r13_noise_passes"] = sum(row["endpoint_status"] == "PASS" for row in r13["experiments"]["noise"])
    out["r13_connected_passes"] = sum(row["endpoint_label"] == "PASS" for kind in ("frozen", "live")
                                     for row in out["r13_access"][kind])
    out["r11_AplusB_vectors"] = [r11["erosion"][f"erosion_a_plus_b_original_seed{s}"]
                                 ["A_components"]["vector"]["correct"] for s in range(3)]
    out["r13_erosion"] = [{"run": r["run"], "onset": next((step for step, n in
        r["accuracy_curve"] if n < 1555), None), "minimum_correct": min(n for _, n in
        r["accuracy_curve"]), "last_step": r["accuracy_curve"][-1][0]}
        for r in r13["experiments"]["erosion"]]
    out["supplementary_support"] = sorted({(tuple(m["sums"]), m["train_pairs"], m["heldout_pairs"])
        for r in r13["supplementary"]["rows"] for m in r["measured"]})
    out["r13_supplementary_decisions"] = [{"seed": r["run"]["seed"], "step": r["step"],
        "pairs": [{"sums": m["sums"], "correct": m["reader"]["correct"],
                   "total": m["reader"]["total"], "passes": m["discrimination"]["pass"]}
                  for m in r["measured"]]} for r in r13["supplementary"]["rows"]
        if r["run"]["condition"] == "raw_probability" and r["step"] == 20000]
    return out


def require_equal(actual, expected, name):
    if actual != expected:
        raise ValueError(f"stated value mismatch: {name}: expected {expected!r}, rebuilt {actual!r}")


def check_outline(v: dict):
    expected = {"boards": 24435, "category_counts": [22491, 1835, 109], "histories": 1555,
                "sums": 36, "cutoff_band": 930, "complement": 23505,
                "masses": 6, "slots": 5, "records": 4, "renderings": 4, "ideal_loss_bits": 1.5,
                "p0": [0.5, 0.25, 0.25], "p1": [0.25, 0.25, 0.5],
                "equal_law": [0.375, 0.25, 0.375]}
    for key, value in expected.items():
        require_equal(v["task"][key], value, "task/" + key)
    for key, expected in (("r8_passes", {"raw_only": 0, "dual": 3, "a_only": 2}),
                          ("r12_passes", {"a_supplied": 2, "a_target": 0}),
                          ("r13_noise", {"raw_sampled": [58, 328, 87], "raw_probability": [2, 1, 149],
                             "sums_sampled": [473, 648, 815], "sums_probability": [473, 400, 523]}),
                          ("r13_encoding", {"onehot": [0, 0, 2], "numerical": [317, 121, 10]}),
                          ("r11_AplusB_vectors", [24434, 24435, 24419]), ("r10_supplied_pass", 0)):
        require_equal(v[key], expected, key)
    require_equal([r["B_errors_with_correct_A_category"] for r in v["r12_joint"]],
                  [326, 617, 770], "r12 correct-category prediction errors")
    require_equal([min(v["r10_spillover"]), max(v["r10_spillover"])], [188, 436], "r10 spillover")
    require_equal([v["r12_raw"]["runs"], v["r12_raw"]["passes"]], [9, 0], "r12 raw runs")
    require_equal(v["r12_raw"]["diagnosis"]["counts"],
        {"board_associated": 20, "recurrence_associated": 3, "unresolved": 19,
         "non_deviating": 120}, "r12 diagnosis")
    require_equal(v["r12_unresolved_prefixes"], 19, "r12 unexplained prefix cases")
    require_equal([v["r12_raw"]["diagnosis"]["chronology"]["COINCIDENT"],
                   v["r12_raw"]["diagnosis"]["chronology"]["PRECEDING"]],
                  [20, 0], "r12 board-associated chronology")
    require_equal([round(min(v["r12_raw"]["short"]), 3), round(max(v["r12_raw"]["short"]), 3),
                   round(max(v["r12_raw"]["long"]), 3)], [0.020, 0.066, 0.172], "r12 panels")
    for row in v["r13_erosion"]:
        require_equal(row["onset"], None if row["run"]["condition"] == "blocked" else 1,
                      "erosion onset " + str(row["run"]))
        if row["run"]["condition"] == "blocked":
            require_equal([row["minimum_correct"], row["last_step"]], [1555, 200], "blocked")
    require_equal(v["r13_onehot_passes"], 1, "r13 one-hot endpoint passes")
    require_equal(v["r13_noise_passes"], 0, "r13 noise endpoint passes")
    require_equal(v["r13_connected_passes"], 0, "r13 connected endpoint passes")
    require_equal([min(v["r12_supplied_misreads"]), max(v["r12_supplied_misreads"])], [0, 1], "r12 supplied misreads")
    require_equal([round(min(v["r8_raw_KL"]), 4), round(max(v["r8_raw_KL"]), 4)],
                  [0.0001, 0.0003], "r8 KL rounded to four decimals")
    require_equal(all(abs(tv - 0.25) <= 0.01 for tv in v["r8_law_TV"]), True,
                  "r8 law TV approximately one quarter (within 0.01)")
    for family, slots, stated in (("linear", [1], 0.3), ("linear", [2, 3, 4, 5], 0.3),
                                  ("mlp64", [2, 3, 4, 5], 0.6)):
        initial = [p["original"]["update0_accuracy"] for p in v["r8_probes"]
                   if p["probe_family"] == family and p["slot"] in slots]
        require_equal(round(statistics.mean(initial), 1), stated,
                      f"r8 initial pooled {family} slots {slots}")
    slot1 = [p["original"]["endpoint_accuracy"] for p in v["r8_probes"]
             if p["slot"] == 1 and p["probe_family"] == "linear"]
    require_equal([round(min(slot1), 2), round(max(slot1), 2)], [0.97, 0.98], "r8 slot-1 probes")
    other = [p["original"]["endpoint_accuracy"] for p in v["r8_probes"]
             if p["slot"] > 1 and p["probe_family"] == "linear"]
    # The distribution approved the rebuilt two-decimal range in round 2.
    require_equal(round(max(other), 2), 0.10, "r8 other-slot upper endpoint")
    for field, expected in (("before", [0.20, 0.37]), ("endpoint", [0.88, 0.95])):
        require_equal([round(min(p[field] for p in v["r10_free_probes"]), 2),
                       round(max(p[field] for p in v["r10_free_probes"]), 2)], expected, "r10 " + field)
    require_equal(all(p["paired_CI95"][0] > 0 for p in v["r10_free_probes"]), True, "r10 paired gains")
    require_equal(round(v["r13_access"]["live"][1]["long_TV"], 3), 0.251, "r13 live seed-1 TV")
    require_equal(v["supplementary_support"], [((12, 13), 135, 150), ((23, 24), 12, 13)], "supplementary support")
    require_equal(len(v["r13_supplementary_decisions"]), 3, "probability-target geometry seeds")
    require_equal(all(p["passes"] for r in v["r13_supplementary_decisions"] for p in r["pairs"]),
                  True, "supplementary cutoff discrimination")
    for kind, expected in (("frozen", [1.3, 11]), ("live", [2.8, 17])):
        ratios = [d["categorical_misreads"] / c["categorical_misreads"]
                  for d, c in zip(v["r13_access"]["disconnected"], v["r13_access"][kind])]
        require_equal([round(min(ratios), 1), round(max(ratios))], expected, "r13 " + kind + " reduction")



def public_value(value: Any, root: Path, manifest: dict):
    """Machine-local paths are allowed only in the manifest's internal field."""
    return contract.sanitize(value)


def compact(value: Any):
    """Detailed board/pair arrays remain available in the hash-bound source."""
    if isinstance(value, list):
        if len(value) > 210:
            return {"detailed_array_length": len(value), "location": "hash-bound source artifact"}
        return [compact(v) for v in value]
    if isinstance(value, dict):
        return {k: compact(v) for k, v in value.items()}
    return value


def metadata(study, manifest, source, computation, scope="sampled", comparison="matched"):
    cache_key = (id(manifest), study)
    if cache_key not in SUPPORT_CACHE:
        keys = set()
        if study in STUDIES:
            for name in ("calibration.json", "registration.json"):
                key = "repo/" + str(study_path(study) / name)
                keys.add(manifest.get("aliases", {}).get(key, key))
        SUPPORT_CACHE[cache_key] = [a["id"] for a in manifest["artifacts"]
                                  if a["archive_path"] in keys]
    supporting = SUPPORT_CACHE[cache_key]
    return {"evidence_ids": [source], "counterevidence": {"evidence_id": source,
            "data": f"control_tables.json#{study}"},
        "controls_and_calibration": supporting, "study": study, "version": "committed corrected report",
        "computation": computation}


def signal(study: int, run: str, row: dict) -> str:
    if study == 8:
        return "next-category CE only; a_only/dual use frozen exact A, raw_only masks A"
    if study == 9:
        return "none; saved r8 update-20,000 networks, read-only diagnosis"
    if study == 10:
        return "all-slots next-category CE" + (" plus five-sum CE, coefficient 1" if row.get("arm") == "free_a" else " only")
    if study == 11:
        if "a_plus_b" in run:
            return "next-category CE plus five-sum CE, coefficient 1"
        if "dose" in run:
            return "next-category CE plus seed-fixed nested masked sums exposure; recorded dose and all-round normalization"
        return "next-category CE only"
    if study == 12:
        return "half natural-position CE plus half coverage-endpoint CE" + (
            "; five-sum CE coefficient 1" if row.get("arm") == "a_target" else
            "; frozen exact A supplied, no sums loss" if row.get("arm") == "a_supplied" else "; no sums loss")
    if study == 13:
        context = row.get("run", {})
        condition, experiment = context.get("condition", ""), context.get("experiment", "")
        if experiment == "erosion":
            return "prediction CE continuation; " + ("prediction gradient blocked into A, decay retained"
                if condition == "blocked" else condition + " active optimizer; no sums loss")
        target = "probability-target CE" if "probability" in condition else "sampled next-category CE"
        aux = experiment == "access" and condition != "exact" or condition.startswith("sums_")
        return "half natural-position and half coverage-endpoint " + target + (
            "; five-sum CE coefficient 1" if aux else "; no sums loss")
    return "See hash-bound registration"


def build(root: Path, manifest: dict, archive: Path | None, check: bool):
    evidence = Evidence(root, manifest, archive)
    inputs = {n: evidence.load(study_path(n) / ("results.json" if n == 9 else "aggregate.json"))
              for n in STUDIES}
    for v in inputs.values():
        validate_rates(v)
    evidence.verify(evidence.entries["repo/paper/notes/outline.md"])
    evidence.verify(evidence.entries["repo/" + str(JI)])
    # The game enumeration is itself source-pinned.
    for path in ("src/recombination_promotion/oldgame_ext/game.py",
                 "src/recombination_promotion/oldgame_ext/multiround.py",
                 "src/recombination_promotion/serialization/minimal_recombination.py"):
        evidence.verify(evidence.entries["repo/" + path])
    for path in ("paper/scripts/build_ledger.py", "paper/scripts/check_package.py",
                 "paper/scripts/ledger_contract.py",
                 "paper/requirements.txt", "paper/requirements-analysis.txt", "paper/references.bib",
                 "paper/notes/bibliography_verification.md", "paper/notes/notation_and_terminology.md"):
        if "repo/" + path in evidence.entries:
            evidence.verify(evidence.entries["repo/" + path])
    values = computations(inputs, evidence)
    executed_source = []
    for loaded in tuple(sys.modules.values()):
        file = getattr(loaded, "__file__", None)
        if not file:
            continue
        path = Path(file).resolve()
        if path.is_relative_to(root / "src") and path.suffix == ".py":
            relative = path.relative_to(root).as_posix()
            entry = evidence.entries["repo/" + relative]
            evidence.verify(entry)
            if sha(path) != entry["sha256"]:
                raise ValueError(f"executed source differs from archived source: {relative}")
            executed_source.append(relative)
    check_outline(values)
    values["study_inventory"] = {"seeds": [0, 1, 2], "versions": 3, "mechanism_experiments": 4,
        "figures": 5, "tables": 2, "appendices": 6,
        "runs": {8: len(inputs[8]["rows"]), 9: len(inputs[9]["runs"]),
                 10: len(inputs[10]["rows"]),
                 11: sum(len(inputs[11][k]) for k in ("rarity", "dose", "erosion")),
                 12: len(inputs[12]["runs"]),
                 13: sum(len(v) for v in inputs[13]["experiments"].values())}}
    other8 = [p["original"]["endpoint_accuracy"] for p in values["r8_probes"]
              if p["slot"] > 1 and p["probe_family"] == "linear"]
    require_equal([round(min(other8), 2), round(max(other8), 2)], [0.05, 0.10],
                  "distribution-approved r8 linear endpoint range")
    require_equal(round(values["r8_mlp_pooled"]["mean"], 2), 0.38,
                  "distribution-approved r8 MLP pooled mean")
    unresolved = []
    claims = []
    for name, value in values["task"].items():
        entry = metadata(None, manifest, evidence.id("src/recombination_promotion/oldgame_ext/game.py"),
                         {"operation": "exact endpoint/history enumeration or stated law arithmetic",
                          "field": name}, "exhaustive census")
        entry.update(id="TASK-" + name, approved_wording=f"Task {name}: {value}",
                     rebuilt_value=value, category="task_measurement", numerator=value,
                     denominator=1, units="bits" if "bits" in name else "count or law probability",
                     seeds=[], endpoint="task definition; no training", training_signal="none",
                     permitted_inference="Exact property of the declared finite task, not an internal network layer.")
        claims.append(entry)
    outline = evidence.path(evidence.entries["repo/paper/notes/outline.md"]).read_text()
    registry = evidence.load("paper/notes/outline_claims.json")
    ji_paragraphs = evidence.path(evidence.entries["repo/" + str(JI)]).read_text().split("\n\n")[2:]
    for i, paragraph in enumerate(ji_paragraphs, 1):
        values[f"interpretation_{i}"] = {"paragraph": i, "approved_interpretation": contract.sanitize(paragraph)}
    values["r12_target_misreads"] = [inputs[12]["runs"][f"a_target_original_seed{s}"]
        ["census_all_four_renderings_and_r9"]["registered_rendering"]["categorical_misreads"] for s in range(3)]
    require_equal([min(values["r12_target_misreads"]), max(values["r12_target_misreads"])],
                  [473, 815], "r12 approximate sums output misreads")
    values["calibration_inventory"] = {str(n): evidence.load(study_path(n) / "calibration.json")
                                      for n in STUDIES if n != 9}
    values["report_inventory"] = {str(n): {k: v for k, v in a.items() if k not in
        {"rows", "runs", "rarity", "dose", "erosion", "experiments"}} for n, a in inputs.items()}
    contract.validate_outline(outline, registry, values)
    for row in registry["lines"]:
        source = Path("paper/notes/outline.md") if row["kind"] == "editorial" else JI
        entry = metadata(row["metadata"]["study"], manifest, evidence.id(source),
                         {"operation": "explicit claim registry", "names": row["computations"]})
        entry.update(row["metadata"])
        entry.update(id=f"O-{row['line']:03d}", approved_wording=row["approved_wording"],
                     outline_line=row["line"], category=row["kind"],
                     claim_key=row.get("claim_key", f"legacy-{row['line']}"),
                     editorial_reason=row["editorial_reason"],
                     rebuilt_value={k: ({"paragraph": values[k]["paragraph"], "table": "joint_interpretation.paragraphs"}
                                        if k.startswith("interpretation_") else
                                        {"sha256": hashlib.sha256(canonical(public_value(values[k], root, manifest)).encode()).hexdigest(),
                                         "computation": k, "table": "paper/data/report_tables.json" if k == "report_inventory" else "paper/data/calibration_tables.json"}
                                        if k in {"report_inventory", "calibration_inventory"} else
                                        {"field": k, "table": "paper/data/reported_outline_quantities.json",
                                         "sha256": hashlib.sha256(canonical(public_value(values[k], root, manifest)).encode()).hexdigest()}
                                        if isinstance(values[k], (dict, list)) else
                                        public_value(values[k], root, manifest)) for k in row["computations"]})
        entry["evidence_ids"] = [evidence.id("paper/notes/outline_claims.json"), evidence.id(source)]
        for n in ([entry["study"]] if entry["study"] else STUDIES):
            entry["evidence_ids"].append(evidence.id(study_path(n) / ("results.json" if n == 9 else "aggregate.json")))
        if row.get("claim_key") == "legacy-65":
            entry["mlp_pooled_mean"] = values["r8_mlp_pooled"]["mean"]
            entry["aggregation"] = "Initial accuracies: equal-cell means rounded to one decimal. Linear endpoint range across slots 2–5 and three seeds; MLP arithmetic mean over the same 12 cells, equal cell weights, 512 boards per cell."
        if row.get("claim_key") == "legacy-64":
            entry["aggregation"] = "Initial: equal-cell mean across three seeds, rounded to one decimal; endpoint: per-seed range rounded to two decimals."
        # All stable keys remain in the pinned registry. Retain in the compact
        # ledger only keys used by publication-angle or cross-revision checks.
        if entry["claim_key"].startswith("legacy-") and entry["claim_key"] not in {
                "legacy-64", "legacy-65", "legacy-74", "legacy-77", "legacy-98", "legacy-103"}:
            del entry["claim_key"]
        claims.append(entry)
    # Numerical appendix inventory: actual counts/rates/intervals/negative controls,
    # not hashes alone. Each pointer is evaluated again on every rebuild.
    tables = {}
    for n, artifact in inputs.items():
        rows = artifact.get("rows", artifact.get("runs"))
        if n == 11:
            rows = {k: row for group in ("rarity", "dose", "erosion")
                    for k, row in artifact[group].items()}
        if n == 13:
            rows = {f"{group}_{index}": row for group, rr in artifact["experiments"].items()
                    for index, row in enumerate(rr)}
        tables[n] = public_value(compact(rows), root, manifest)
        path = study_path(n) / ("results.json" if n == 9 else "aggregate.json")
        for pointer, value in measurements(tables[n]):
            entry = metadata(n, manifest, evidence.id(path), {"operation": "JSON pointer lookup",
                             "table": f"study_{n}", "pointer": list(pointer)})
            text_pointer = "/".join(map(str, pointer))
            entry.update(id=f"N-{n}-" + hashlib.sha256(text_pointer.encode()).hexdigest()[:12],
                         approved_wording=f"Study r{n}: {text_pointer} = " +
                         (str(value) if isinstance(value, (int, float, bool)) else
                          "measurement vector in the hash-bound appendix table"),
                         rebuilt_value=value if isinstance(value, (int, float, bool)) else
                         {"table": f"bulk/paper_data_bulk/control_tables.json#{n}/" + text_pointer,
                          "sha256": hashlib.sha256(canonical(value).encode()).hexdigest()},
                         category="appendix_measurement")
            context = tables[n][pointer[0]]
            entry["training_signal"] = signal(n, str(pointer[0]), context)
            if isinstance(context.get("seed"), int):
                entry["seeds"] = [context["seed"]]
            elif isinstance(context.get("run"), dict):
                entry["seeds"] = [context["run"]["seed"]]
            elif re.search(r"seed(\d+)", str(pointer[0])):
                entry["seeds"] = [int(re.search(r"seed(\d+)", str(pointer[0])).group(1))]
            if n == 13 and context.get("run", {}).get("experiment") == "erosion":
                entry["endpoint"] = "200 updates; every update reported"
            elif n == 9:
                entry["endpoint"] = "read-only r8 update-20,000 networks"
            else:
                entry["endpoint"] = "registered fixed endpoint, 20,000 updates; no best-checkpoint selection"
            if any(k in text_pointer for k in ("census", "by_slot1", "local_hist", "A_exact", "A_components")):
                entry["scope"] = "exhaustive census"
            elif any(k in text_pointer for k in ("law", "swap", "diagnos")):
                entry["scope"] = "constructed"
            if "correct" in text_pointer or "count" in text_pointer:
                entry["numerator"] = value if isinstance(value, (int, float, bool)) else "counts in measurement vector"
                entry["units"] = "count (support at adjacent table pointer)"
                parent = at(tables[n], pointer[:-1])
                if isinstance(parent, dict):
                    entry["denominator"] = next((parent[k] for k in ("total", "boards", "count", "evaluated_pairs")
                                                  if isinstance(parent.get(k), (int, float))), None)
            if ("total" in text_pointer or "boards" in text_pointer or "denominator" in text_pointer) and isinstance(value, (int, float)):
                entry["denominator"] = value
            if "CI95" in text_pointer or "CI95" in str(pointer) or "CI" in text_pointer:
                entry["aggregation"] = "saved paired 95% interval, not seed variability"
            claims.append(entry)
    study_tables = {}
    runtimes = []
    calibration_tables = {}
    for n in STUDIES:
        if n != 9:
            regpath = study_path(n) / "registration.json"
            calpath = study_path(n) / "calibration.json"
            reg, cal = evidence.load(regpath), evidence.load(calpath)
            study_tables[n] = {"registration_evidence_id": evidence.id(regpath),
                              "settings_and_criteria": public_value(reg, root, manifest)}
            calibration_tables[n] = {"evidence_id": evidence.id(calpath),
                                     "calibration": public_value(compact(cal), root, manifest)}
            for pointer, value in measurements({"calibration": public_value(compact(cal), root, manifest)}):
                entry = metadata(n, manifest, evidence.id(calpath), {"operation": "JSON pointer lookup",
                                  "source": "calibration", "pointer": list(pointer)}, "constructed")
                text = "/".join(map(str, pointer))
                entry.update(id=f"C-{n}-" + hashlib.sha256(text.encode()).hexdigest()[:12],
                             approved_wording=f"Calibration r{n}: {text} = " +
                             (str(value) if isinstance(value, (int, float, bool)) else
                              "calibration vector in the hash-bound appendix table"),
                             rebuilt_value=value if isinstance(value, (int, float, bool)) else
                             {"table": f"bulk/paper_data_bulk/calibration_tables.json#{n}/" + text,
                              "sha256": hashlib.sha256(canonical(value).encode()).hexdigest()},
                             category="calibration_not_measured_result")
                entry.update(training_signal="none; calibration positives/nulls and probe fitting only",
                             endpoint="pre-launch calibration or separately recorded repaired analysis calibration",
                             seeds=[], permitted_inference="The deciding test separates its declared positive and null "
                             "on recorded nonempty support; this does not establish a measured network result.")
                claims.append(entry)
        else:
            study_tables[n] = {"scope": "Read-only diagnosis of saved r8 update-20,000 networks",
                "training": None, "source": public_value(inputs[n]["source"], root, manifest),
                "sampling": public_value(inputs[n]["sampling"], root, manifest),
                "evidence_id": evidence.id(study_path(n) / "results.json")}
            row = {"study": n, "evidence_id": evidence.id(study_path(n) / "results.json"),
                   "measurements": {"elapsed_seconds": inputs[n]["elapsed_seconds"]},
                   "aggregation": "One read-only CPU diagnosis; not training runtime"}
            runtimes.append(row)
            entry = metadata(n, manifest, row["evidence_id"], {"operation": "results field", "key": "elapsed_seconds"})
            entry.update(id="T-r9-diagnosis", approved_wording=f"r9 diagnosis elapsed seconds: {inputs[n]['elapsed_seconds']}",
                         rebuilt_value=inputs[n]["elapsed_seconds"], category="compute_measurement", units="seconds")
            claims.append(entry)
        for artifact in manifest["artifacts"]:
            if artifact["study"] != n or artifact["role"] != "run_summary":
                continue
            evidence.verify(artifact)
            summary = json.loads(evidence.path(artifact).read_text())
            fields = {k: v for k, v in summary.items() if any(t in k for t in
                ("seconds", "per_second", "threads", "GPU_peak", "rss", "device", "precision"))}
            if fields:
                row = {"study": n, "evidence_id": artifact["id"], "run": artifact["archive_path"],
                       "measurements": fields,
                       "aggregation": "group elapsed time is not summed over batched run summaries"}
                runtimes.append(row)
                for key, value in fields.items():
                    if not isinstance(value, (int, float)):
                        continue
                    entry = metadata(n, manifest, artifact["id"], {"operation": "summary field", "key": key})
                    entry.update(id="T-" + artifact["id"][2:] + "-" + key,
                                 approved_wording=f"{artifact['archive_path']}: {key} = {value}",
                                 rebuilt_value=value, category="compute_measurement",
                                 units="seconds" if "seconds" in key else key)
                    claims.append(entry)
    # Scientific metadata is an explicitly prepared, hash-pinned authority.
    metadata_index = evidence.load("paper/notes/measurement_metadata.json")
    metadata_shards = {}
    for entry in claims:
        if entry["id"].startswith("O-"):
            continue
        path = metadata_index.get(entry["id"])
        if path is None:
            raise ValueError(f"measurement metadata not specified: {entry['id']}")
        if path not in metadata_shards:
            metadata_shards[path] = evidence.load(path)
        specified = contract.metadata_for(entry["id"], metadata_shards[path])
        entry.update({k: v for k, v in specified.items() if k != "support"})
        entry["support"] = {"authority": path + "#" + entry["id"]}
        entry["evidence_ids"].append(evidence.id(path))
    # Review and correction authorities are actual package inputs, not dangling IDs.
    by_id = {a["id"]: a for a in manifest["artifacts"]}
    for entry in claims:
        for identifier in entry["evidence_ids"] + entry["controls_and_calibration"]:
            evidence.verify(by_id[identifier])
    for artifact in manifest["artifacts"]:
        if artifact["role"] == "archived_review":
            evidence.verify(artifact)
    # Retain report-level tables, not just run rows. Originals remain untouched.
    report_tables = {n: public_value(compact({k: v for k, v in artifact.items() if k not in
        {"rows", "runs", "rarity", "dose", "erosion", "experiments"}}), root, manifest)
                    for n, artifact in inputs.items()}
    curves = {n: {run: {field: row[field] for field in (
        "loss_KL_curve", "route_damage_curve", "B_curve", "B_A_curve", "learning_curve",
        "accuracy_curve", "early_erosion_readouts") if field in row}
        for run, row in rows.items()} for n, rows in tables.items()}
    summaries = {k: public_value(v, root, manifest) for k, v in values.items()
                 if k not in {"calibration_inventory", "report_inventory"}}
    # Pin every used source before any output; no partial successful build on mismatch.
    ji_text = evidence.path(evidence.entries["repo/" + str(JI)]).read_text()
    ji_paragraphs = ji_text.split("\n\n")[2:]
    ledger = {"schema": "claims_ledger_v1", "source_manifest_sha256": manifest.get("original_manifest_sha256", sha(root / MANIFEST)),
              "joint_interpretation": {"evidence_id": evidence.id(JI),
                  "paragraphs": {str(i): contract.sanitize(text) for i, text in enumerate(ji_paragraphs, 1)}},
              "outline_sha256": evidence.entries["repo/paper/notes/outline.md"]["sha256"],
              "unreproduced_outline_numbers": unresolved, "claims": claims,
              "wording_support_exceptions": [
                  {"id": c["id"], "assessment_field": "wording_assessment in the indexed claim"}
                  for c in claims if c.get("wording_assessment")],
              "recomputed_outline_quantities": summaries,
              "scope_notice": "Probe intervals are not seed intervals. Calibration is not a measured "
              "network result. Misreads are not TV errors. Long panels in r12/r13 include trained lengths."}
    markdown = ["# Claim–evidence ledger", "", ledger["scope_notice"], "",
                "## Outline statements", "", "| ID | Approved wording | Computation |", "|---|---|---|"]
    for row in claims:
        if row["id"].startswith("O-"):
            markdown.append(f"| {row['id']} | {row['approved_wording'].replace('|', '/')} | {row['computation']} |")
    markdown += ["", f"The JSON contains {len(claims)} individually indexed outline, appendix, "
                 "calibration and compute measurements with evidence pointers and scope.", "",
                 "## Unreproduced outline numbers", "", canonical(unresolved).strip()]
    markdown += ["", "## Wording support limits", "",
                 "Zero numerical mismatches is not a finding that every causal wording is supported."]
    for item in ledger["wording_support_exceptions"]:
        assessed = next(c for c in claims if c["id"] == item["id"])
        markdown += ["", f"{item['id']}: {assessed['wording_assessment']}"]
    markdown += ["", "## Complete measurement index", "",
                 "Every remaining JSON entry is rendered below. Measurement vectors retain "
                 "their actual counts and intervals in the linked appendix data; the JSON "
                 "records the complete scope, support, recipe and permitted/prohibited inference.", "",
                 "| ID | Statement | Category | Evidence | Scope |",
                 "|---|---|---|---|---|"]
    for row in claims:
        if not row["id"].startswith("O-"):
            markdown.append(f"| {row['id']} | {row['approved_wording'].replace('|', '/')} | "
                            f"{row['category']} | {', '.join(row['evidence_ids'])} | {row['scope']} |")
    for name, full in (("control_tables.json", tables), ("calibration_tables.json", calibration_tables)):
        artifact = evidence.entries["bulk/paper_data_bulk/" + name]
        evidence.verify(artifact)
        if json.loads(evidence.path(artifact).read_text()) != json.loads(canonical(full)):
            raise ValueError(f"full appendix rebuild differs: {name}")
    outputs = {"paper/notes/claims_ledger.json": small_json(ledger),
               "paper/notes/claims_ledger.md": "\n".join(markdown) + "\n",
               "paper/data/control_tables.json": small_json(paper_table(tables)),
               "paper/data/calibration_tables.json": small_json(paper_table(calibration_tables)),
               "paper/data/readability_tables.json": small_json(reported_probe_cells(tables)),
               "paper/data/reported_outline_quantities.json": small_json(summaries),
               "paper/data/report_tables.json": small_json(paper_table(report_tables)),
               "paper/data/report_table_sources.json": canonical({str(n): {
                   "evidence_id": evidence.id(study_path(n) / ("results.json" if n == 9 else "aggregate.json")),
                   "source": str(study_path(n) / ("results.json" if n == 9 else "aggregate.json")),
                   "receipt_rule": "Remove the /study prefix; resolve the JSON pointer in the source, apply compact and public path sanitization, then check canonical SHA-256."}
                   for n in STUDIES}),
               "paper/data/learning_curves.json": small_json(curves),
               "paper/data/supplementary_and_movement_tables.json": small_json(public_value(
                   {k: inputs[13][k] for k in ("supplementary", "erosion_comparisons", "geometry_calibration")}, root, manifest)),
               "paper/data/appendix_inventory.json": canonical({
                   "A": ["paper/notes/evidence_manifest.json"],
                   "B": ["paper/data/control_tables.json", "paper/data/report_tables.json"],
                   "C": ["paper/data/calibration_tables.json", "paper/data/supplementary_and_movement_tables.json"],
                   "D": ["paper/data/learning_curves.json"],
                   "E": ["paper/data/readability_tables.json", "paper/data/report_tables.json", "paper/data/supplementary_and_movement_tables.json"],
                   "F": ["paper/data/compute_records.json", "paper/notes/evidence_manifest.json"],
                   "Fig1": ["paper/data/reported_outline_quantities.json"],
                   "Fig2": ["paper/data/sampling_training_criteria.json"],
                   "Fig3": ["paper/data/readability_tables.json", "paper/data/control_tables.json"],
                   "Fig4": ["paper/data/reported_outline_quantities.json"],
                   "Fig5": ["paper/data/learning_curves.json", "paper/data/supplementary_and_movement_tables.json"],
                   "Table1": ["paper/data/control_tables.json", "paper/notes/outline_claims.json"],
                   "Table2": ["paper/data/control_tables.json", "paper/data/reported_outline_quantities.json"]}),
               "paper/data/sampling_training_criteria.json": canonical(study_tables),
               "paper/data/compute_records.json": canonical(runtimes)}
    for number, table in study_tables.items():
        outputs[f"paper/data/study_r{number}_sampling_training_criteria.json"] = canonical(table)
    # Exact asset inputs beyond the compact aggregate: saved local update
    # records, access update-0 long-law floors and case-wise endpoint laws.
    # No checkpoint is read and no new neural evaluation is performed.
    for row in tables[13].values():
        records = [row['records']] if row.get('records') else []
        if row.get('audit_references'):
            records.append(row['audit_references'][-1])
            if row['run']['experiment'] == 'access':
                records.append(row['audit_references'][0])
        for record in records:
            entry = evidence.entries[record['path']]
            if entry['sha256'] != record['sha256']:
                raise ValueError('paper asset reference identity differs: ' + record['path'] +
                                 ' saved=' + record['sha256'] + ' current=' + entry['sha256'])
            evidence.verify(entry)
    # Minimal numerical/figure rebuild subset: only inputs actually read by this build,
    # plus artifact-backed planned figure sources (no copying in this phase).
    subset = [a for a in manifest["artifacts"] if a["id"] in evidence.verified]
    public = [{k: v for k, v in a.items() if k != "internal"} for a in subset]
    outputs["paper/notes/public_evidence_subset.json"] = canonical({
        "copied": False, "purpose": "Rebuild all ledger numbers and planned figure data; "
        "not a package for model re-training or new neural inference",
        "bytes": sum(a["bytes"] for a in subset), "files": public,
        "code_required": ["paper/scripts/build_ledger.py", "paper/scripts/check_package.py",
                          "paper/scripts/ledger_contract.py",
                          *sorted(set(executed_source))],
        "manifest_required": "paper/notes/evidence_manifest.json",
        "verification": "Numerical subset builds use only these entries; --verify-all "
        "also verifies the extended provenance archive, including checkpoints."})
    for path, content in outputs.items():
        publish(root / path, content, check)
    print(f"ledger: {len(claims)} entries; {len(subset)} hash-verified numerical inputs; "
          f"public evidence {sum(a['bytes'] for a in subset):,} bytes; outline mismatches {len(unresolved)}")


def public_package(root, target):
    """Export an independently executable numerical package, never alter originals."""
    if target.exists():
        raise ValueError("public package destination already exists")
    manifest = json.loads((root / MANIFEST).read_text())
    subset = json.loads((root / "paper/notes/public_evidence_subset.json").read_text())
    evidence = Evidence(root, manifest)
    wanted = {a["id"] for a in subset["files"]}
    entries = [a for a in manifest["artifacts"] if a["id"] in wanted]
    for entry in entries:
        evidence.verify(entry)
        projection = entry.get("public_projection")
        source = portable_path(entry["internal"]["public_projection_path"], root) if projection else evidence.path(entry)
        if projection and sha(source) != projection["sha256"]:
            raise ValueError("public projection hash differs")
        destination = target / (projection["path"] if projection else entry["archive_path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    # Rebuild outputs and executable scaffold are public derived files, not inputs.
    for source in (root / "paper").rglob("*"):
        if source.is_file() and not any(p in {"build", "__pycache__"} for p in source.parts):
            destination = target / "repo" / source.relative_to(root)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix == ".md" and source.name not in {"outline.md", "claims_ledger.md"}:
                destination.write_text(contract.sanitize(source.read_text()))
            else:
                shutil.copyfile(source, destination)
    for name in ("LICENSE", "LICENSE-CC-BY-4.0"):
        shutil.copyfile(root / name, target / "repo" / name)
    public = {k: v for k, v in manifest.items() if k not in {"artifacts", "aliases"}}
    public["artifacts"] = [{k: v for k, v in a.items() if k != "internal"} for a in entries]
    public["aliases"] = {k: v for k, v in manifest.get("aliases", {}).items()
                         if v in {a["archive_path"] for a in entries}}
    public["original_manifest_sha256"] = sha(root / MANIFEST)
    publish(target / "repo" / MANIFEST, canonical(contract.sanitize(public)), False)
    print(f"standalone public package: {len(entries)} inputs at {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--archive-root", type=Path)
    parser.add_argument("--pin", action="store_true", help="explicit initial evidence inventory")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-all", action="store_true")
    parser.add_argument("--public-package", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    sys.path.insert(0, str(root / "src"))
    if args.pin:
        if args.check or args.archive_root:
            parser.error("--pin is a separate preparation operation")
        publish(root / MANIFEST, canonical(pin(root)), False)
    manifest = json.loads((root / MANIFEST).read_text())
    if args.verify_all:
        evidence = Evidence(root, manifest, args.archive_root)
        for entry in manifest["artifacts"]:
            evidence.verify(entry)
        print(f"extended provenance verified: {len(evidence.verified)} artifacts")
    build(root, manifest, args.archive_root, args.check)
    if args.public_package:
        public_package(root, args.public_package.resolve())


if __name__ == "__main__":
    main()
