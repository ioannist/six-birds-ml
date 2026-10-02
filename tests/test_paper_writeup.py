"""Read-only write-up rebuild and clean-location scaffold regressions."""
from __future__ import annotations

import importlib.util
import hashlib
import json
import re
import shutil
import subprocess
import sys
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "paper/scripts" / f"{name}.py")
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


ledger = module("build_ledger")
package = module("check_package")


def test_evidence_refuses_hash_mutation(tmp_path):
    source = tmp_path / "count.json"
    source.write_text('{"correct": 2, "total": 3}')
    manifest = {"artifacts": [{"id": "E-example", "archive_path": "repo/count.json",
        "sha256": ledger.sha(source), "internal": {"path": str(source)}}]}
    source.write_text('{"correct": 3, "total": 3}')
    with pytest.raises(ValueError, match="evidence hash differs"):
        ledger.Evidence(tmp_path, manifest).load("count.json")


def test_portable_archive_needs_no_internal_path(tmp_path):
    source = tmp_path / "repo/count.json"
    source.parent.mkdir()
    source.write_text('{"correct": 2, "total": 3}')
    manifest = {"artifacts": [{"id": "E-example", "archive_path": "repo/count.json",
        "sha256": ledger.sha(source), "internal": {"path": "/missing/private/count.json"}}]}
    assert ledger.Evidence(ROOT, manifest, tmp_path).load("count.json")["correct"] == 2


def test_stated_value_mismatch_is_not_silently_changed():
    with pytest.raises(ValueError, match="stated value mismatch.*expected 24.*rebuilt 25"):
        ledger.require_equal(25, 24, "test board count")


def test_initial_probe_claim_is_checked_against_the_computation():
    values = json.loads((ROOT / "paper/data/reported_outline_quantities.json").read_text())
    values["supplementary_support"] = [(tuple(row[0]), row[1], row[2])
                                       for row in values["supplementary_support"]]
    ledger.check_outline(values)
    for row in values["r8_probes"]:
        if row["probe_family"] == "linear" and row["slot"] == 1:
            row["original"]["update0_accuracy"] = 0.8
    with pytest.raises(ValueError, match="stated value mismatch: r8 initial pooled"):
        ledger.check_outline(values)


def test_rate_is_recomputed_from_counts():
    ledger.validate_rates({"correct": 2, "total": 3, "accuracy": 2 / 3})
    with pytest.raises(ValueError, match="count/rate mismatch"):
        ledger.validate_rates({"correct": 2, "total": 3, "accuracy": 0.7})
    with pytest.raises(ValueError, match="count outside support"):
        ledger.validate_rates({"correct": 4, "total": 3})


def test_ledger_rebuilds_from_pinned_sources():
    result = subprocess.run([sys.executable, "paper/scripts/build_ledger.py", "--check"],
                            cwd=ROOT, capture_output=True, text=True, timeout=300,
                            env={k: v for k, v in os.environ.items() if k != "PYTHONPATH"})
    assert result.returncode == 0, result.stdout + result.stderr
    assert "hash-verified numerical inputs" in result.stdout


def test_every_numeric_outline_line_is_accounted_for():
    content = json.loads((ROOT / "paper/notes/claims_ledger.json").read_text())
    covered = {r["outline_line"] for r in content["claims"] if "outline_line" in r}
    for number, line in enumerate((ROOT / "paper/notes/outline.md").read_text().splitlines(), 1):
        if re.search(r"\d|\b(five|four|three|Six)\b", line):
            assert number in covered, (number, line)
    assert len(content["unreproduced_outline_numbers"]) == 0
    assert content["recomputed_outline_quantities"]["r12_raw"]["passes"] == 0
    assert content["recomputed_outline_quantities"]["r12_passes"]["a_supplied"] == 2


def test_claim_entries_keep_support_and_inference_fields():
    content = json.loads((ROOT / "paper/notes/claims_ledger.json").read_text())
    fields = {"id", "approved_wording", "joint_interpretation_paragraph", "evidence_ids",
              "counterevidence", "controls_and_calibration", "study", "version", "training_signal",
              "endpoint", "seeds", "numerator", "denominator", "units", "aggregation", "rounding",
              "computation", "scope", "comparison", "permitted_inference", "prohibited_stronger_inference"}
    assert all(fields <= c.keys() for c in content["claims"])
    assert len({c["id"] for c in content["claims"]}) == len(content["claims"])
    rendered = (ROOT / "paper/notes/claims_ledger.md").read_text()
    assert all(c["id"] in rendered for c in content["claims"])


def test_measurement_vectors_match_their_appendix_data():
    content = json.loads((ROOT / "paper/notes/claims_ledger.json").read_text())
    manifest = json.loads((ROOT / ledger.MANIFEST).read_text())
    evidence = ledger.Evidence(ROOT, manifest)
    def full(name):
        entry = evidence.entries["bulk/paper_data_bulk/" + name]
        evidence.verify(entry)
        return json.loads(evidence.path(entry).read_text())
    controls = full("control_tables.json")
    calibration = full("calibration_tables.json")
    for c in content["claims"]:
        value = c["rebuilt_value"]
        if not isinstance(value, dict) or "sha256" not in value or "table" not in value:
            continue
        pointer = c["computation"]["pointer"]
        if c["category"] == "appendix_measurement":
            rebuilt = ledger.at(controls[str(c["study"])], pointer)
        else:
            rebuilt = ledger.at(calibration[str(c["study"])], pointer)
        assert hashlib.sha256(ledger.canonical(rebuilt).encode()).hexdigest() == value["sha256"]


def test_public_subset_is_listed_not_copied():
    subset = json.loads((ROOT / "paper/notes/public_evidence_subset.json").read_text())
    assert not subset["copied"]
    assert subset["bytes"] == sum(a["bytes"] for a in subset["files"])
    assert all(not a["archive_path"].startswith("/") for a in subset["files"])
    assert all("internal" not in a for a in subset["files"])


def test_compact_outputs_meet_size_limits_and_keep_reported_counts():
    for path in (ROOT / "paper").rglob("*"):
        if path.is_file():
            assert path.stat().st_size < 5_000_000, path
    assert sum(p.stat().st_size for p in (ROOT / "paper/data").rglob("*")
               if p.is_file()) < 10_000_000
    value = {"8": {"run": {"correct": 500, "total": 512,
                           "large_detail": list(range(10000))}}}
    compact = ledger.paper_table(value)
    assert compact["8"]["run"]["correct"] == 500
    receipt = compact["8"]["run"]["large_detail"]
    assert receipt["detail_pointer"] == "/8/run/large_detail"
    assert receipt["sha256"] == hashlib.sha256(
        ledger.canonical(value["8"]["run"]["large_detail"]).encode()).hexdigest()


def test_pooled_mean_and_stated_values_are_explicit():
    content = json.loads((ROOT / "paper/notes/claims_ledger.json").read_text())
    rows = [c for c in content["claims"] if "mean over slots 2–5" in c["approved_wording"]]
    assert len(rows) == 1
    assert rows[0]["mlp_pooled_mean"] == 0.38037109375
    assert "equal cell weights" in rows[0]["aggregation"]


def test_compact_probe_table_contains_actual_counts_and_intervals():
    rows = json.loads((ROOT / "paper/data/readability_tables.json").read_text())
    assert len(rows) > 100
    assert all("paired_CI95" in r for r in rows)
    assert any("endpoint_counts" in r for r in rows)
    assert any("majority_floor" in r for r in rows)
    assert all(r["full_table_pointer"].startswith("/") for r in rows)


def test_full_archive_rebuild_uses_archive_bulk_without_private_paths(tmp_path):
    target = tmp_path / "standalone"
    ledger.public_package(ROOT, target)
    script = target / "repo/paper/scripts/build_ledger.py"
    result = subprocess.run([sys.executable, "-I", str(script), "--check", "--verify-all"], cwd=tmp_path,
                            capture_output=True, text=True, timeout=300,
                            env={k: v for k, v in os.environ.items() if k != "PYTHONPATH"})
    assert result.returncode == 0, result.stdout + result.stderr
    assert "outline mismatches 0" in result.stdout
    manifest = json.loads((target / "repo" / ledger.MANIFEST).read_text())
    assert all("internal" not in a for a in manifest["artifacts"])
    for a in manifest["artifacts"]:
        if "public_projection" in a:
            assert a["public_projection"]["original_sha256"] == a["sha256"]
            text = (target / a["public_projection"]["path"]).read_text()
            assert not ledger.contract.PRIVATE.search(text), a["archive_path"]
        else:
            path = target / a["archive_path"]
            if path.suffix in {".json", ".md", ".log", ".saved"}:
                assert not ledger.contract.PRIVATE.search(path.read_text()), a["archive_path"]
    # No original repository supplies the executable code or the expected outputs.
    assert script.is_file()
    original = target / "repo/paper/notes/claims_ledger.json"
    original.unlink()
    result = subprocess.run([sys.executable, "-I", str(script)], cwd=tmp_path,
                            capture_output=True, text=True, timeout=300)
    assert result.returncode == 0, result.stdout + result.stderr
    assert original.exists()


def test_outline_number_change_refused_with_source_hashes_unchanged():
    registry = json.loads((ROOT / "paper/notes/outline_claims.json").read_text())
    outline = (ROOT / "paper/notes/outline.md").read_text()
    values = {k: None for r in registry["lines"] for k in r["computations"]}
    before = ledger.sha(ROOT / ledger.MANIFEST)
    ledger.contract.validate_outline(outline, registry, values)
    scientific = next(r for r in registry["lines"] if r["claim_key"] == "legacy-88")
    with pytest.raises(ValueError, match=f"stated outline wording/number mismatch: O-{scientific['line']:03d}"):
        ledger.contract.validate_outline(outline.replace("0/3, with 473–815", "1/3, with 473–815"), registry, values)
    assert ledger.sha(ROOT / ledger.MANIFEST) == before
    scientific["computations"] = []
    with pytest.raises(ValueError, match="scientific claim has no named computation"):
        ledger.contract.validate_outline(outline, registry, values)


def test_metadata_scopes_are_explicit_and_unknown_entries_refuse():
    rows = {c["claim_key"]: c for c in json.loads((ROOT / "paper/notes/claims_ledger.json").read_text())["claims"] if "claim_key" in c}
    assert rows["legacy-77"]["scope"] == "constructed"
    assert rows["legacy-103"]["scope"] == "exhaustive census"
    assert rows["legacy-98"]["scope"] == "supplementary"
    assert rows["legacy-98"]["joint_interpretation_paragraph"] == 6
    assert rows["legacy-74"]["comparison"] == "historical"
    with pytest.raises(ValueError, match="measurement metadata not specified"):
        ledger.contract.metadata_for("missing", {})


def test_scientific_angle_has_explicit_effects_and_unresolved_wording_limits():
    data = json.loads((ROOT / "paper/notes/claims_ledger.json").read_text())
    rows = {c["claim_key"]: c for c in data["claims"] if "claim_key" in c}
    for line in (11, 34, 44, 130):
        row = rows[f"publication-angle-{line}"]
        assert "r12_raw" in row["computation"]["names"]
        assert "wording_assessment" not in row
        assert row["support"]["unexplained_cases"] == "r12_unresolved_prefixes"
        assert row["support"]["missing_achievements"] == {
            "access": "r13_access", "preservation": "r13_erosion"}
        assert "historical" in row["comparison_confounds"]
        assert "complete causal attribution" in row["prohibited_stronger_inference"]
    assert len(data["wording_support_exceptions"]) == 2
    assert data["recomputed_outline_quantities"]["r12_unresolved_prefixes"] == 19
    assert data["unreproduced_outline_numbers"] == []
    assert {"r13_noise", "r13_access", "r13_encoding", "r13_erosion", "r12_raw"} <= set(
        rows["publication-angle-11"]["computation"]["names"])


def test_unexplained_count_is_not_silently_changed():
    registry = json.loads((ROOT / "paper/notes/outline_claims.json").read_text())
    outline = (ROOT / "paper/notes/outline.md").read_text()
    values = {k: None for r in registry["lines"] for k in r["computations"]}
    with pytest.raises(ValueError, match="stated outline wording/number mismatch: O-011"):
        ledger.contract.validate_outline(outline.replace("19 r12 cases", "18 r12 cases"), registry, values)


def test_scientific_title_matches_tex_and_pdf_metadata():
    text = (ROOT / "paper/main.tex").read_text()
    title = "Where Does Jagged Competence Come From?"
    assert "\\title{" + title + "}" in text
    assert "pdftitle={" + title + "}" in text


def test_appendix_and_asset_inventory_has_report_level_results():
    inventory = json.loads((ROOT / "paper/data/appendix_inventory.json").read_text())
    assert set("ABCDEF") <= inventory.keys()
    assert {f"Fig{i}" for i in range(1, 6)} <= inventory.keys()
    for paths in inventory.values():
        assert paths
        assert all((ROOT / p).is_file() for p in paths)
    reports = json.loads((ROOT / "paper/data/report_tables.json").read_text())
    assert "raw_only_endpoint_probes" in reports["8"]
    extra = json.loads((ROOT / "paper/data/supplementary_and_movement_tables.json").read_text())
    assert {"supplementary", "erosion_comparisons", "geometry_calibration"} <= extra.keys()
    sources = json.loads((ROOT / "paper/data/report_table_sources.json").read_text())
    evidence = ledger.Evidence(ROOT, json.loads((ROOT / ledger.MANIFEST).read_text()))
    def check_receipts(value):
        if isinstance(value, dict):
            if "detail_pointer" in value:
                components = value["detail_pointer"].strip("/").split("/")
                original = evidence.load(sources[components[0]]["source"])
                for k in components[1:]:
                    original = original[int(k)] if isinstance(original, list) else original[k]
                rebuilt = ledger.contract.sanitize(ledger.compact(original))
                assert hashlib.sha256(ledger.canonical(rebuilt).encode()).hexdigest() == value["sha256"]
            else:
                for child in value.values():
                    check_receipts(child)
        elif isinstance(value, list):
            for child in value:
                check_receipts(child)
    check_receipts(reports)


@pytest.mark.parametrize("filename", ["original.json", "calibration.json.abc.saved"])
def test_embedded_private_paths_are_projected_without_original_mutation(tmp_path, filename):
    source = tmp_path / filename
    source.write_text(json.dumps({"correspondence": "See /home/person/private/item.md and /mnt/disk/runs/x.json"}))
    original = source.read_bytes()
    entry = {"id": "E-test", "sha256": ledger.sha(source)}
    projection = ledger.contract.publish_projection(entry, source, tmp_path / "projections")
    projected = (tmp_path / "projections/E-test.json").read_text()
    assert not ledger.contract.PRIVATE.search(projected)
    assert source.read_bytes() == original
    assert projection["original_sha256"] == entry["sha256"]


@pytest.mark.skipif(shutil.which("latexmk") is None, reason="requires latexmk")
@pytest.mark.parametrize("missing", [r"\input{includes/absent}", r"\includegraphics{figures/absent.pdf}"])
def test_package_refuses_missing_project_dependencies(tmp_path, missing):
    paper = tmp_path / "paper"
    shutil.copytree(ROOT / "paper", paper, ignore=shutil.ignore_patterns("build", "__pycache__"))
    main = paper / "main.tex"
    main.write_text(main.read_text().replace(r"\end{document}", missing + "\n" + r"\end{document}"))
    with pytest.raises(ValueError, match="clean TeX build failed"):
        package.check_package(paper)


@pytest.mark.skipif(shutil.which("latexmk") is None, reason="requires latexmk")
def test_package_copies_local_style_table_and_figure(tmp_path):
    paper = tmp_path / "paper"
    shutil.copytree(ROOT / "paper", paper, ignore=shutil.ignore_patterns("build", "__pycache__"))
    (paper / "localnotice.sty").write_text(r"\ProvidesPackage{localnotice}" + "\n")
    (paper / "tables/local.tex").write_text("A local table dependency.\n")
    # Produce a genuine vector PDF fixture, not a missing-file stand-in.
    drawing = tmp_path / "drawing.tex"
    drawing.write_text(r"\documentclass{article}\begin{document}Fixture\end{document}")
    result = subprocess.run(["pdflatex", "-interaction=nonstopmode", drawing.name],
                            cwd=tmp_path, capture_output=True, timeout=30)
    assert result.returncode == 0
    shutil.copyfile(tmp_path / "drawing.pdf", paper / "figures/local.pdf")
    main = paper / "main.tex"
    main.write_text(main.read_text().replace(r"\begin{document}", r"\usepackage{localnotice}" + "\n" +
        r"\begin{document}\input{tables/local}\includegraphics[width=1cm]{figures/local.pdf}"))
    result = package.check_package(paper)
    sources = {r["path"] for r in result["dependencies"] if r["kind"] == "project_source"}
    assert {"localnotice.sty", "tables/local.tex", "figures/local.pdf"} <= sources


def test_public_correspondence_exclusions_and_licence_decisions_are_recorded():
    manifest = json.loads((ROOT / ledger.MANIFEST).read_text())
    assert manifest["public_exclusions"]["excluded_correspondence_files"] == 22
    assert not any(a["role"] == "archived_review" for a in manifest["artifacts"])
    assert "NOT_RECORDED_IN_RUN_SUMMARIES" in manifest["study_history"][0]["exact_shell_invocation"]
    assert len(re.findall(r"^MIT License$", (ROOT / "LICENSE").read_text(), re.M)) == 1
    assert "no licence grant" not in (ROOT / "paper/notes/licensing.md").read_text().lower()
    assert (ROOT / "paper/requirements-analysis.txt").is_file()
    assert "10.5281/zenodo.19189353" in (ROOT / "paper/references.bib").read_text()
    assert "Section 3.5" in (ROOT / "paper/notes/bibliography_verification.md").read_text()
    key = "repo/" + str(ledger.study_path(10) / "calibration.json")
    target = manifest["aliases"].get(key, key)
    calibration_id = next(a["id"] for a in manifest["artifacts"] if a["archive_path"] == target)
    claims = json.loads((ROOT / "paper/notes/claims_ledger.json").read_text())["claims"]
    assert all(calibration_id in c["controls_and_calibration"] for c in claims
               if c["id"].startswith("N-10-"))


@pytest.mark.skipif(shutil.which("latexmk") is None, reason="requires latexmk and TeX distribution")
def test_scaffold_builds_from_clean_location():
    result = package.check_package(ROOT / "paper")
    assert result["clean_location_build"] == "PASS"
    assert set(result['pdfs'])=={'main','supplement'}
    assert result['pdfs']['supplement']['pages']<=60
    assert result['pdfs']['supplement']['heading_only_pages']==[]
    # The approved 14-page main-text budget (publication, 2026-10-02) also bounds the approximately
    # equally long appendix; the old 12-page ceiling predates that decision.
    assert 'at most 14 pages' in (ROOT/'paper/style/VENUE_FORMAT.md').read_text()
    assert 8<=result['pdfs']['main']['appendix_pages']<=14
    assert all(r['overfull_boxes_over_10_pt']==0 for r in result['pdfs'].values())
    assert result["pdf_bytes"] > 0
    sources = {r["path"] for r in result["dependencies"] if r["kind"] == "project_source"}
    assert {"main.tex", "references.bib", "includes/release_metadata.tex"} <= sources
    assert len([s for s in sources if s.startswith("sections/")]) == 9
    assert 'sections/09_endmatter.tex' in sources
    # Six primary appendices; the distribution's measurement/training subsections
    # are additional transitive inputs, not additional primary appendices.
    assert len([s for s in sources if re.fullmatch(r"appendices/[A-F]_[^/]+\.tex",s)]) == 6


def test_main_text_page_budget():
    result=package.check_package(ROOT / "paper")
    pages=result['pdfs']['main']['main_text_pages']
    assert pages<=14


def test_scaffold_has_no_inherited_release_or_licence():
    metadata = (ROOT / "paper/includes/release_metadata.tex").read_text()
    tex = (ROOT / "paper/main.tex").read_text()
    assert r'\paperhasdoitrue' in metadata
    assert r'\newcommand{\paperdoi}{10.5281/zenodo.23094485}' in metadata
    assert "10.5281" not in tex
    assert r"\author{Ioannis Tsiokos\,\orcidlink{0009-0009-7659-5964}}" in tex
    assert "Automorph Inc." in tex
    assert "CC-BY 4.0" in tex
    assert r'\newcommand{\manuscriptversion}{Preprint v1.0}' in metadata
    assert "Copyright (c) 2026 Ioannis Tsiokos" in (ROOT / "LICENSE").read_text()


def test_submission_inventory_and_supplement_share_release_identity():
    supplement = (ROOT / 'paper/supplement/supplement.tex').read_text()
    assert r'\input{includes/release_metadata}' in supplement
    assert r'\title{Supplement to: Where Does Jagged Competence Come From?\\DOI \paperdoi}' in supplement
    assert r'\date{\manuscriptdate\quad\manuscriptversion}' in supplement
    assert 'UNRELEASED' not in supplement
    readme = (ROOT / 'paper/submission/README.md').read_text()
    assert '10.5281/zenodo.23094485' in readme
    assert 'reserved but unpublished' in readme
    assert 'immutable historical artifacts' in readme
    for name in ('zenodo-metadata.json', 'zenodo-description.html', 'zenodo-release.json',
                 'arxiv_package_receipt.json', 'ARXIV_CHECKS.md',
                 'Tsiokos_2026_Where_Does_Jagged_Competence_Come_From.pdf',
                 'Tsiokos_2026_Where_Does_Jagged_Competence_Come_From_Supplement.pdf'):
        assert name in readme
        assert (ROOT / 'paper/submission' / name).is_file() or (
            ROOT / 'paper/submission/artifacts' / name).is_file()
    # Source archives are excluded from this distribution. Their portable
    # compilation and figure coverage are tested through the public-source mode.
    assert not (ROOT / 'paper/submission/arxiv_source.zip').exists()
    assert 'distribution does not include source archives' in readme
    assert 'build_arxiv.py' in readme
    for command in ('check_package.py',
                    'build_ledger.py --check --verify-all'):
        assert command in readme
    assert '/home/' not in readme and '/mnt/' not in readme


@pytest.mark.skipif(shutil.which('pdflatex') is None, reason='requires pdflatex and Poppler')
@pytest.mark.skipif(not (ROOT / "paper/submission/arxiv_source.zip").is_file(),
                    reason="arXiv source ZIP is a separate release artifact, excluded from this public repository")
def test_arxiv_source_archive_compiles_against_release():
    arxiv = module('build_arxiv')
    result = arxiv.check(ROOT / 'paper')
    assert result['result']=='PASS' and 2<=result['passes']<=4
    assert result['bibtex_invocations']==0
    assert result['pages']==result['release_pages']
    assert result['undefined_references']==result['undefined_citations']==0
    assert result['paper_identifier_check'].startswith('PASS:')
    assert result['graphic_stem_check'].startswith('PASS:')
    graphics = {name for name in result['files'] if Path(name).suffix == '.pdf'}
    assert len(graphics) == 10 and graphics == set(result['included_graphics'])
    tex_stems = {Path(name).stem for name in result['files'] if Path(name).suffix == '.tex'}
    assert not {Path(name).stem for name in graphics} & tex_stems
    assert 'except the release title-page DOI' in result['text_match']
    required={'main.tex','main.bbl','references.bib','sections/09_endmatter.tex',
              'appendices/training_details.tex','appendices/measurement_details.tex'}
    assert required<=set(result['files'])
    assert not any('supplement' in Path(p).parts for p in result['files'])


@pytest.mark.parametrize('extra',['main.aux','main.pdf','supplement/supplement.tex'])
def test_arxiv_package_refuses_auxiliary_and_supplement_inputs(tmp_path,extra):
    arxiv = module('build_arxiv')
    for name in ('main.tex','main.bbl','references.bib'):
        (tmp_path/name).write_text('fixture')
    target=tmp_path/extra
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('fixture')
    with pytest.raises(ValueError,match='extraneous|compiled manuscript'):
        arxiv.validate_tree(tmp_path)


def test_arxiv_package_refuses_absolute_dependencies(tmp_path):
    arxiv = module('build_arxiv')
    for name in ('main.bbl','references.bib'):
        (tmp_path/name).write_text('fixture')
    (tmp_path/'main.tex').write_text(r'\input{/private/external}')
    with pytest.raises(ValueError,match='nonportable dependency'):
        arxiv.validate_tree(tmp_path)


@pytest.mark.skipif(not (ROOT / "paper/submission/arxiv_source.zip").is_file(),
                    reason="arXiv source ZIP is a separate release artifact, excluded from this public repository")
def test_arxiv_archive_rebuild_is_byte_identical(tmp_path):
    arxiv = module('build_arxiv')
    source=ROOT/'paper/submission/arxiv'
    first,second=tmp_path/'first.zip',tmp_path/'second.zip'
    arxiv.write_archive(source,first)
    arxiv.write_archive(source,second)
    assert first.read_bytes()==second.read_bytes()
    assert arxiv.sha(first)==arxiv.sha(ROOT/'paper/submission/arxiv_source.zip')


@pytest.mark.parametrize('tex_name', ['figures/figure.tex', 'other/figure.tex'])
def test_arxiv_package_refuses_pdf_tex_stem_conflict(tmp_path, tex_name):
    arxiv = module('build_arxiv')
    for name in ('main.tex', 'main.bbl', 'references.bib', tex_name, 'figures/figure.pdf'):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('fixture')
    with pytest.raises(ValueError, match='PDF/TeX stem conflict'):
        arxiv.validate_tree(tmp_path)


@pytest.mark.skipif(not (ROOT / "paper/submission/arxiv_source.zip").is_file(),
                    reason="arXiv source ZIP is a separate release artifact, excluded from this public repository")
def test_arxiv_graphic_paths_rewritten_without_source_renames():
    arxiv = module('build_arxiv')
    files = ['figures/figure.pdf', 'other/figure-graphic.tex', 'figures/figure.tex']
    renamed = arxiv.graphic_names(files)
    assert renamed == {'figures/figure.pdf': 'figures/figure-graphic-2.pdf'}
    text = r'\includegraphics[width=\textwidth]{figures/figure.pdf}'
    assert arxiv.rewrite_graphics(text, renamed) == (
        r'\includegraphics[width=\textwidth]{figures/figure-graphic-2.pdf}')
    assert arxiv.rewrite_graphics(r'\includegraphics{figures/figure}', renamed) == (
        r'\includegraphics{figures/figure-graphic-2.pdf}')
    receipt = json.loads((ROOT / 'paper/submission/arxiv_package_receipt.json').read_text())
    assert len(receipt['graphic_renames']) == 10
    for source, bundled in receipt['graphic_renames'].items():
        assert arxiv.sha(ROOT / 'paper' / source) == arxiv.sha(ROOT / 'paper/submission/arxiv' / bundled)
        assert not (ROOT / 'paper/submission/arxiv' / source).exists()
        assert bundled not in (ROOT / 'paper' / Path(source).with_suffix('.tex')).read_text()


@pytest.mark.skipif(shutil.which('pdflatex') is None, reason='requires pdflatex and Poppler')
@pytest.mark.skipif(not (ROOT / "paper/submission/arxiv_source.zip").is_file(),
                    reason="arXiv source ZIP is a separate release artifact, excluded from this public repository")
def test_arxiv_archive_refuses_unconsumed_graphic(tmp_path):
    arxiv = module('build_arxiv')
    folder = tmp_path / 'source'
    shutil.copytree(ROOT / 'paper/submission/arxiv', folder)
    graphic = next(folder.rglob('*.pdf'))
    shutil.copyfile(graphic, folder / 'unused-graphic.pdf')
    archive = tmp_path / 'unused.zip'
    arxiv.write_archive(folder, archive)
    release = ROOT / 'paper/submission/artifacts' / (arxiv.RELEASE_NAME + '.pdf')
    with pytest.raises(ValueError, match='graphics not included.*unused-graphic'):
        arxiv.verify_archive(archive, release)


@pytest.mark.parametrize('token', ['zenodo.23094485', '10.5281/zenodo.23094485', 'Zenodo record'])
@pytest.mark.parametrize('name', ['main.tex', 'references.bib', 'figure.pdf'])
def test_arxiv_package_refuses_paper_identifier_in_any_file(tmp_path, token, name):
    arxiv = module('build_arxiv')
    for required in ('main.tex', 'main.bbl', 'references.bib'):
        (tmp_path / required).write_text('fixture')
    (tmp_path / name).write_text(token)
    with pytest.raises(ValueError, match='paper identifier forbidden'):
        arxiv.validate_tree(tmp_path)
    with pytest.raises(ValueError, match='paper identifier forbidden'):
        arxiv.verify_identifier_text(token, 'compiled arXiv PDF text')


def test_arxiv_metadata_omits_only_this_paper_doi():
    arxiv = module('build_arxiv')
    source = (ROOT / 'paper/includes/release_metadata.tex').read_text()
    modified = arxiv.arxiv_metadata(source)
    assert r'\paperhasdoifalse' in modified and r'\paperdoi' not in modified
    assert arxiv.PAPER_DOI in source
    for macro in ('manuscriptversion', 'manuscriptdate', 'manuscriptyear'):
        pattern = r'\\newcommand\{\\' + macro + r'\}\{[^}]*\}'
        assert re.search(pattern, source).group() == re.search(pattern, modified).group()
    arxiv.verify_identifier_text('10.5281/zenodo.1234567', 'cited other paper')


def test_writeup_refresh_order_is_serial_and_local_only():
    refresh=module('refresh_writeup')
    commands=refresh.planned_commands(ROOT,sys.executable,Path('/fixture/paper_build_release.py'))
    names=[name for name,command,cwd in commands]
    assert names.index('pin')<names.index('figures')<names.index('tables')<names.index('release')<names.index('arxiv')<names.index('writeup_tests')
    assert names.index('writeup_tests')<names.index('multiround_tests')
    release=next(command for name,command,cwd in commands if name=='release')
    assert release==[sys.executable,'/fixture/paper_build_release.py','--build']
    # A publication directory is not a remote action. Inspect executable names
    # and argument tokens, not their parent-directory names.
    assert not any(any(word in (Path(part).name if Path(part).is_absolute() else str(part)).lower()
                       for word in ('upload','deposit','publish','curl'))
                   for name,command,cwd in commands for part in command)


def test_writeup_refresh_refuses_stale_inventory(tmp_path,monkeypatch):
    refresh=module('refresh_writeup')
    notes=tmp_path/'paper/notes'
    notes.mkdir(parents=True)
    (notes/'figure_assets.json').write_text(json.dumps({'ledger_sha256':'old','assets':[]}))
    class Fixture:
        ledger_sha256='current'
    monkeypatch.setattr(refresh,'Inputs',lambda root:Fixture())
    with pytest.raises(ValueError,match='stale ledger identity'):
        refresh.check_assets(tmp_path)


def test_writeup_refresh_rejects_authority_change(tmp_path,monkeypatch):
    refresh=module('refresh_writeup')
    frozen={'manifest':'old','ledger':'old','sources':{}}
    monkeypatch.setattr(refresh,'source_snapshot',lambda root:{'manifest':'new','ledger':'new','sources':{}})
    with pytest.raises(ValueError,match='authority changed during refresh'):
        refresh.check_snapshot(tmp_path,frozen)


def test_corpus_titles_are_metadata_titles():
    pins = (ROOT / "paper/style/source_pins_verbatim.md").read_text()
    bibliography = (ROOT / "paper/references.bib").read_text()
    rows = [line.split("|") for line in pins.splitlines() if re.match(r"\| \d{4}\.\d{4,5}", line)]
    assert len(rows) == 12
    for row in rows:
        assert row[1].strip() in bibliography
        assert row[2].strip() in bibliography
