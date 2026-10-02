"""Exact coverage, interface, objective, continuation and reporting checks."""

import copy

import numpy as np
import pytest
import torch

from scripts import oldgame_multiround_coverage as study
from recombination_promotion.oldgame_ext import game
from recombination_promotion.oldgame_ext.memory import VALUES


@pytest.fixture(scope="module")
def tables():
    torch.set_num_threads(1)
    return study.r11.BoardTables(torch.device("cpu"))


@pytest.mark.parametrize("law", ("original", "equal"))
def test_strata_and_endpoint_supervision(tables, law):
    stream = study.CoverageStream(tables, 0, law, "uniform")
    batch = stream.draw_batch()
    assert batch.records.shape == (256, 9, 4, 2)
    assert int(batch.active.sum()) == 1856
    assert int(batch.b_active.sum()) == 1280
    assert batch.active[:128].all() and batch.b_active[:128].all()
    assert torch.equal(stream.stratum_exposure, torch.full((2, 8), 8))
    for anchor in (0, 1):
        for k in range(1, 9):
            selected = (batch.anchor == anchor) & (batch.neutral_length == k)
            assert int(selected.sum()) == 8
            assert (batch.categories[selected, 0] == 2 * anchor).all()
            assert (batch.categories[selected, 1:k + 1] == 1).all()
            assert not batch.b_active[selected, :k].any()
            assert batch.b_active[selected, k].all()
            assert not batch.active[selected, k + 1:].any()
    # Independent record-derived sums and categories, not retained labels.
    sums = torch.zeros((256, 9, 5), dtype=torch.long)
    masses = torch.tensor(game.MASSES)
    for at in range(4):
        sums.scatter_add_(-1, batch.records[:, :, at, :1], masses[batch.records[:, :, at, 1:2]])
    category = torch.where(sums[..., 0] <= 12, 0, torch.where(sums[..., 0] >= 24, 2, 1))
    assert torch.equal(category[batch.active], batch.categories[batch.active])
    assert torch.equal(sums[batch.active], batch.sums[batch.active])
    assert int(stream.rendering_exposure.sum()) == 1856
    assert int(stream.placement_exposure.sum()) == 1856


def test_paired_streams_and_restoration(tables):
    streams = [study.CoverageStream(tables, 2, "original", draw)
               for draw in ("uniform", "cutoff", "decoy", "uniform", "uniform")]
    for _ in range(3):
        batches = [stream.draw_batch() for stream in streams]
        for batch in batches:
            assert torch.equal(batch.targets, batches[0].targets)
            assert torch.equal(batch.categories, batches[0].categories)
        for batch in batches[3:]:
            assert torch.equal(batch.records, batches[0].records)
    saved = streams[0].state()
    expected = streams[0].draw_batch()
    restored = study.CoverageStream(tables, 2, "original", "uniform")
    restored.restore(saved)
    actual = restored.draw_batch()
    assert torch.equal(actual.records, expected.records)
    assert torch.equal(actual.targets, expected.targets)
    study._check_stream(streams[0], restored)


@pytest.mark.parametrize("law", ("original", "equal"))
def test_conditional_target_frequencies(tables, law):
    stream = study.CoverageStream(tables, 0, law, "uniform")
    for _ in range(128):
        stream.draw_batch()
    expected = (np.asarray(study.P, dtype=float)[:, None] if law == "original" else
                np.asarray(study.P_EQUAL, dtype=float))
    actual = stream.endpoint_targets.numpy() / stream.stratum_exposure.numpy()[..., None]
    assert np.abs(actual - expected).max() < .075


def test_loss_ignores_intermediate_coverage_targets(tables):
    batch = study.CoverageStream(tables, 0, "original", "uniform").draw_batch()
    logits = torch.randn(1, 256, 9, 3, requires_grad=True)
    a_logits = torch.randn(1, 256, 9, 5, 36, requires_grad=True)
    output = (logits, None, a_logits, None, None)
    expected, _ = study.coverage_loss(output, [batch], ["uniform"])
    altered = copy.deepcopy(batch)
    altered.targets[128:][~altered.b_active[128:]] = 2
    actual, _ = study.coverage_loss(output, [altered], ["uniform"])
    assert torch.equal(actual, expected)
    actual.sum().backward()
    assert logits.grad[0, 128:][~batch.b_active[128:]].count_nonzero() == 0
    assert a_logits.grad is None


def test_only_a_target_has_a_loss_and_all_active_normalization(tables):
    batch = study.CoverageStream(tables, 0, "original", "uniform").draw_batch()
    b_logits = torch.zeros(1, 256, 9, 3, requires_grad=True)
    a_logits = torch.zeros(1, 256, 9, 5, 36, requires_grad=True)
    output = (b_logits, None, a_logits, None, None)
    for arm in study.ARMS:
        loss, details = study.coverage_loss(output, [batch], [arm])
        assert (details[0]["A"] > 0) == (arm == "a_target")
        if arm == "a_target":
            expected = torch.nn.functional.cross_entropy(
                a_logits[0][batch.active].flatten(0, 1),
                torch.searchsorted(torch.tensor(VALUES), batch.sums[batch.active]).flatten())
            assert details[0]["A"] == float(expected.detach())
            assert torch.allclose(loss, b_logits.new_tensor([np.log(3) + np.log(36)]))


def test_matched_initialization_masking_and_frozen_a(tables):
    models = [study.new_model(0, arm, study.ROOT) for arm in study.ARMS]
    for model in models:
        for key, value in model.state_dict().items():
            assert torch.equal(value, models[0].state_dict()[key])
        assert all(not p.requires_grad for p in model.memory.parameters())
    batch = study.CoverageStream(tables, 0, "original", "uniform").draw_batch()
    for model in models[:4]:
        x = batch.records[:4]
        before, _ = model(x, batch.lengths[:4])
        changed, _ = model(x, batch.lengths[:4], answer_override=torch.randn(4, 9, 5, 36))
        assert torch.equal(before, changed)
    model = models[-1]
    loss, _ = study.coverage_loss(tuple(x[None] for x in model(
        batch.records, batch.lengths, return_all=True)), [batch], ["a_supplied"])
    loss.sum().backward()
    assert all(p.grad is None for p in model.memory.parameters())


def test_probe_labels_and_metadata_do_not_reach_forward(tables):
    batch = study.CoverageStream(tables, 0, "original", "uniform").draw_batch()
    engine = study.Engine([study.Run("uniform", "original", 0)], torch.device("cpu"))
    expected = engine.forward(batch.records[None], batch.lengths[None])[0]
    batch.sums[:] = 0
    batch.anchor[:] = 1
    batch.modes[:] = 1
    actual = engine.forward(batch.records[None], batch.lengths[None])[0]
    assert torch.equal(expected, actual)


def test_futility_uses_b_not_a():
    run = study.Run("a_target", "original", 0)
    first = {"train_parts": {"B": 1.2, "A": 10}, "A_accuracy": .1,
             "audit": {"natural_excess_KL_bits": .2}}
    current = copy.deepcopy(first)
    current["train_parts"]["A"] = .1
    assert study.futility(first, current, run)["stop"]
    current["train_parts"]["B"] = 1.05
    assert not study.futility(first, current, run)["stop"]
    current = copy.deepcopy(first)
    current["A_accuracy"] = .2
    assert not study.futility(first, current, run)["stop"]


def test_direct_and_batched_ordinary_adamw_and_disk_restore(tmp_path, monkeypatch):
    study.r11.write_json(tmp_path / "registration.json", {
        "source_sha256": study.identities(), "settings": study.settings(),
        "runs": [r.name for r in study.all_runs()]})
    monkeypatch.setattr(study, "OUTPUT", tmp_path)
    result = study.verification(torch.device("cpu"), trace=True,
                                destination=tmp_path / "verification.json")
    assert result["pass"]
    assert result["registration_sha256"] == study.r11.sha(study.OUTPUT / "registration.json")
    assert result["source_sha256"] == study.identities()
    assert len(result["comparisons"]) == 3
    for row in result["comparisons"].values():
        assert row["restoration"] == "exact"
        assert len(row["trace"]) == 8


def test_checkpoint_digest_refuses_mutation(tmp_path):
    path = tmp_path / "record.pt"
    study._save(path, {"step": 3})
    assert study._bound_load(path)["step"] == 3
    with path.open("ab") as handle:
        handle.write(b"alteration")
    with pytest.raises(ValueError, match="checkpoint digest differs"):
        study._bound_load(path)


def test_unseen_empty_refuses():
    candidate = study._candidate("original")
    candidate.seen[:] = True
    with pytest.raises(ValueError, match="unseen calibration panel is empty"):
        study.r11._score_b(study.r11.r8.ExactRowModel("raw_only", "original"), "original",
                           candidate, reject_empty=True)


def test_run_resume_and_saved_futility(tmp_path, tables, monkeypatch):
    authority = tmp_path / "authority"
    authority.mkdir()
    for filename in ("registration.json", "calibration.json"):
        (authority / filename).write_text("{}")
    monkeypatch.setattr(study, "OUTPUT", authority)
    monkeypatch.setattr(study, "registration", lambda: {})
    def reduced_audit(model, run, candidate, stream, device, step, details, bulk, *, smoke):
        return {"step": step, "train_parts": details, "A_accuracy": .1,
                "audit": {"B_pass": False, "natural_excess_KL_bits": .1},
                "elapsed_seconds": 0}
    monkeypatch.setattr(study, "audit_record", reduced_audit)
    runs = [study.Run("uniform", "original", 0)]
    output, bulk = tmp_path / "resumed", tmp_path / "bulk"
    first = study.run_chunk(runs, torch.device("cpu"), output, bulk, steps=3, smoke=True)
    final = study.run_chunk(runs, torch.device("cpu"), output, bulk, steps=8, smoke=True)
    direct = study.run_chunk(runs, torch.device("cpu"), tmp_path / "direct",
                             tmp_path / "direct_bulk", steps=8, smoke=True)
    assert first[0]["step"] == 3 and final[0]["resumed_from"] == 3
    group = next(bulk.glob("group_*/checkpoint_step_000008.pt"))
    other = next((tmp_path / "direct_bulk").glob("group_*/checkpoint_step_000008.pt"))
    a, b = study._bound_load(group), study._bound_load(other)
    study._check_numeric(a["engine"]["parameters"], b["engine"]["parameters"], exact=True)
    assert a["streams"][0]["rolling"] == b["streams"][0]["rolling"]
    assert direct[0]["step"] == final[0]["step"] == 8


@pytest.mark.parametrize("reduced", (True, False))
def test_aggregate_has_all_registered_measurements(tmp_path, monkeypatch, reduced):
    import json
    monkeypatch.setattr(study, "OUTPUT", tmp_path)
    spec = study.SPEC.read_text()
    monkeypatch.setattr(study, "aggregate_registration", lambda: {"specification_verbatim": spec})
    monkeypatch.setattr(study.r11, "_paired_probe_changes", lambda *args, **kwargs: {"status": "TEST_READER"})
    (tmp_path / "calibration.json").write_text(json.dumps({"probes": {"oracle": {}}}))
    (tmp_path / "registration.json").write_text("{}")
    run = study.Run("uniform", "original", 0)
    runs = [run] if reduced else [run, study.Run("decoy", "original", 0),
        *[study.Run("a_target", "original", seed) for seed in (0, 1, 2)],
        study.Run("a_supplied", "original", 2)]
    for entry in runs:
        (tmp_path / entry.name).mkdir()
        summary = {"curve": [{"step": step, "run": entry.name} for step in (0, 200)],
                   "first_audited_crossing": None, "futility_stop": False}
        (tmp_path / entry.name / "summary.json").write_text(json.dumps(summary))
    census_row = {"boards": 128, "categorical_misreads": 1, "above_0_02_TV": 1, "maximum_TV": .1}
    cases = {name: {"count": 1, "mean_TV": .1, "maximum_TV": .1}
             for name in ("L_single_round", "H_single_round", *[f"N_run_{k}" for k in range(1, 9)])}
    def fake_audit(ref):
        diagnosis = diagnostic_panel(diagnostic_sequence())
        diagnosis["worst_histories"]["H_N4"]["maximum_TV"] = 0.
        if ref["run"] == "decoy_original_seed0":
            diagnosis["worst_histories"] = {}
            for key, sequence in (("H_N4", diagnostic_sequence(error=4, deviation=4)),
                                  ("L_N4", diagnostic_sequence(deviation=4))):
                diagnosis["worst_histories"][key] = {
                    "maximum_TV": .1, "prefixes": sequence,
                    **study.failure_chronology(sequence, anchor_responses_valid=True)}
        joint = {0: (237, 473, 326), 1: (44, 648, 617), 2: (58, 815, 770)}
        counts = joint[int(ref["run"][-1])] if ref["run"].startswith("a_target") else (10, 1, 1)
        swaps = {name: {"count": 1, "mean_TV": .01, "maximum_TV": .01} for name in (
            "reset_L", "set_H", "neutral_N", "same_category_substitution", "upper_state_exchange_same_N")}
        if ref["run"] == "a_supplied_original_seed2":
            swaps["reset_L"]["maximum_TV"] = .05903680622577667
        return {"step": ref["step"], "reduced_smoke": reduced,
                "A_board_accuracy": {"per_slot": [{"correct": 10, "total": 128}] * 5,
                                     "vector": {"correct": 1, "total": 128}},
                "A_local_history_accuracy": None,
                "frozen_A_local_history_counts": {"correct": 1555, "total": 1555, "operative": False},
                "exposure": {}, "stratum_endpoints": [[0] * 8] * 2,
                "conditional_endpoint_target_counts": [], "A_supervised_counts_by_slot_sum": [],
                "unseen_composition": {"unmarked_test_positions": 50000},
                "prefix_diagnosis": diagnosis,
                "train_parts": {"B": 1.1, "coverage_endpoint_KL_bits": .1},
                "category_error_decomposition": [{"rendering": k, "boards": 128,
                    "A_head_category_errors": counts[0], "B_signature_errors": counts[1],
                    "B_errors_with_correct_A_category": counts[2]} for k in range(4)],
                "audit": {"B_pass": False, "criteria": {"witness": True},
                    "natural_excess_KL_bits": .1, "unseen_excess_KL_bits": .1, "unseen_count": 50000,
                    "mode_law": {"cases": cases, "witness_recovery_fraction": 0,
                                 "witness_pair_mean_prediction_TV": 0},
                    "rerender": {"maximum_TV": 0, "A_answer_mismatched_components": 0, "pass": True},
                    "swaps": {"natural_swap_pass": False, "cases": swaps}, "route_damage": {}, "probes": {},
                    "board_census": {"registered_rendering": census_row,
                        "additional_fixed_renderings": [census_row] * 3,
                        "saved_r9_failed_renderings": {**census_row, "count": 101}}}}
    monkeypatch.setattr(study, "_load_audit", fake_audit)
    study.aggregate(tmp_path)
    report = json.loads((tmp_path / "aggregate.json").read_text())
    row = report["runs"][run.name]
    assert set(row["law_panels"]["panels"]) == {"short", "long"}
    assert len(row["learning_curve"][-1]["category_errors"]) == 4
    assert "worst_history_prefix_diagnosis" in row and "probes" in row
    text = (tmp_path / "aggregate.md").read_text()
    for required in ("A rerender differences", "N_run_8", "Coverage endpoint KL",
                     "B errors with A category correct", "Local A histories"):
        assert required in text
    assert ("Reduced smoke is not evidence" if reduced else "Cause unresolved") in text
    assert "Earliest incorrect constituent" in text and "Chronology" in text
    for required in ("Comparison across arms and seeds", "Short mean TV", "Long max TV",
                     "Swap max TV", "Clear-N recurrence panels", "clear-neutral", "Coincident",
                     "Supplied A is exact; A-target is approximate", "curriculum and loss weighting changed",
                     "does not test unseen lengths", "Competition within the encoder is a hypothesis"):
        assert required.lower() in text.lower()
    assert report["registered_readings_verbatim"] == spec[
        spec.index("Predeclare these readings:"):spec.index("All pathway conclusions")]
    assert len(report["comparison_table"]) == len(runs)
    if not reduced:
        d = report["runs"]["decoy_original_seed0"]["diagnosis_summary"]
        assert d["board_association_observed"] and d["recurrence_evidence_observed"]
        assert len(d["concurrent_findings"]) == 2
        assert [(r["A_head_category_errors"], r["B_signature_errors"], r["B_errors_with_correct_A_category"])
                for r in report["A_target_joint_errors"]] == [(237, 473, 326), (44, 648, 617), (58, 815, 770)]
        assert "reset_L maximum TV 0.05903680622577667" in text


def diagnostic_sequence(*, error=None, deviation=None, response_error=None):
    return [{"round": at, "TV": .1 if at == deviation else 0., "exact_category": 1,
             "board_signature": 0 if at == error else 1,
             "constituent_response_maximum_TV": .1 if at == response_error else 0.}
            for at in range(1, 6)]


def diagnostic_panel(sequence, *, anchors=True):
    return {"worst_histories": {"H_N4": {"prefixes": sequence,
                **study.failure_chronology(sequence, anchor_responses_valid=anchors)}},
            "anchor_responses": {"count": 2, "valid": anchors},
            "clear_neutral_hold": [{"boards": [1], "response_count": 1,
                "anchor": 0,
                "per_length_maximum_TV": [0.] * 9, "constituent_response_maximum_TV": 0.,
                "correct_N_signatures": 1}]}


@pytest.mark.parametrize("error,deviation,relation", [
    (2, 4, "PRECEDING"), (4, 4, "COINCIDENT"),
    (None, 4, "NO_OBSERVED_CONSTITUENT_ERROR"),
    (5, 4, "NO_OBSERVED_CONSTITUENT_ERROR")])
def test_failure_chronology_tracks_earliest_signature_through_failure(error, deviation, relation):
    sequence = diagnostic_sequence(error=error, deviation=deviation)
    result = study.failure_chronology(sequence, anchor_responses_valid=True)
    assert result["first_deviation"] == deviation
    assert result["constituent_error_relation"] == relation
    assert result["earliest_incorrect_constituent_signature"] == (
        error if error is not None and error <= deviation else None)
    assert result["descriptive_hypothesis"] == (
        "BOARD_ASSOCIATED_FAILURE" if relation in ("PRECEDING", "COINCIDENT") else
        "RECURRENCE_ASSOCIATED_FAILURE")


def test_failure_chronology_retains_first_of_multiple_errors():
    sequence = diagnostic_sequence(error=2, deviation=4)
    sequence[3]["board_signature"] = 0
    result = study.failure_chronology(sequence, anchor_responses_valid=True)
    assert result["earliest_incorrect_constituent_signature"] == 2
    assert result["constituent_error_relation"] == "PRECEDING"


def test_recurrence_reading_requires_observed_failure_correct_responses_and_anchors():
    # B may fail another bar; passing neutral sequences do not identify its cause.
    assert study.select_failure_reading(diagnostic_panel(diagnostic_sequence())) == "Cause unresolved"
    failing = diagnostic_sequence(deviation=4)
    assert study.select_failure_reading(diagnostic_panel(failing)) == "Upper recurrence remains a limitation"
    assert study.select_failure_reading(diagnostic_panel(failing, anchors=False)) == "Cause unresolved"
    assert study.select_failure_reading(diagnostic_panel(
        diagnostic_sequence(deviation=4, response_error=2))) == "Cause unresolved"
    assert study.select_failure_reading(diagnostic_panel(
        diagnostic_sequence(error=2, deviation=4))) == (
            "Board computation remains a candidate limitation after history coverage")
    panel = diagnostic_panel(diagnostic_sequence())
    panel["clear_neutral_hold"][0]["per_length_maximum_TV"][4] = .1
    assert study.select_failure_reading(panel) == "Upper recurrence remains a limitation"
    panel["anchor_responses"]["valid"] = False
    assert study.select_failure_reading(panel) == "Cause unresolved"


@pytest.mark.parametrize("empty", ("worst_histories", "clear_neutral_hold", "prefixes", "boards", "anchors"))
def test_diagnostic_selection_refuses_empty_panels(empty):
    panel = diagnostic_panel(diagnostic_sequence(deviation=4))
    if empty in ("worst_histories", "clear_neutral_hold"):
        panel[empty] = {} if empty == "worst_histories" else []
    elif empty == "prefixes":
        panel["worst_histories"]["H_N4"]["prefixes"] = []
    elif empty == "boards":
        panel["clear_neutral_hold"][0]["boards"] = []
    else:
        panel["anchor_responses"]["count"] = 0
    with pytest.raises(ValueError, match="requires nonempty"):
        study.select_failure_reading(panel)


def test_diagnostic_calibration_executes_deciding_functions():
    calibrated = study.calibrate_diagnostics()
    for law, controls in calibrated.items():
        for control in controls.values():
            assert control["pass"]
            assert control["diagnosis"]["anchor_responses"]["count"] == 2
        assert controls["oracle"]["classification_counts"] == {"NO_DEVIATION": 18}
        if law == "original":
            assert controls["board_error"]["classification_counts"]["BOARD_ASSOCIATED_FAILURE"] > 0
            assert controls["delayed_drift"]["classification_counts"]["RECURRENCE_ASSOCIATED_FAILURE"] > 0
        else:
            assert all(c["classification_counts"] == {"NO_DEVIATION": 18} for c in controls.values())


def test_prefix_diagnosis_refuses_empty_panel(tables, monkeypatch):
    monkeypatch.setattr(study.r11.r8, "_panels", lambda law: (None, None, np.empty((0, 9, 4, 2)), [], []))
    stream = study.CoverageStream(tables, 0, "original", "uniform")
    with pytest.raises(ValueError, match="prefix panel is empty"):
        study.prefix_diagnosis(study.DiagnosticControl("oracle", "original"), "original", stream,
                              torch.device("cpu"))


def test_report_diagnoses_retain_board_recurrence_and_clear_neutral_evidence():
    panel = diagnostic_panel(diagnostic_sequence(error=4, deviation=4))
    for key, sequence in (("recurrence", diagnostic_sequence(deviation=4)),
                          ("unresolved", diagnostic_sequence(deviation=4, response_error=2)),
                          ("non_deviating", diagnostic_sequence())):
        panel["worst_histories"][key] = {"prefixes": sequence,
            **study.failure_chronology(sequence, anchor_responses_valid=True)}
    panel["clear_neutral_hold"][0]["per_length_maximum_TV"][5] = .1
    result = study.aggregate_diagnosis(panel)
    assert result["counts"] == {"board_associated": 1, "recurrence_associated": 1,
                                "unresolved": 1, "non_deviating": 1}
    assert result["chronology"]["COINCIDENT"] == 1
    assert result["chronology"]["PRECEDING"] == 0
    assert result["board_association_observed"] and result["recurrence_evidence_observed"]
    assert len(result["concurrent_findings"]) == 2
    assert result["clear_neutral"][0]["recurrence_evidence"]
    assert result["clear_neutral"][0]["violating_N_lengths"] == [5]
    # No selected-prefix recurrence, but a correctly anchored clear-N failure still counts.
    del panel["worst_histories"]["recurrence"]
    assert study.aggregate_diagnosis(panel)["recurrence_evidence_observed"]
    panel["anchor_responses"]["valid"] = False
    assert not study.aggregate_diagnosis(panel)["recurrence_evidence_observed"]


def test_report_swap_summary_excludes_nondeciding_interventions():
    cases = {key: {"count": 2 if key == "reset_L" else 1,
                   "mean_TV": .01, "maximum_TV": .01} for key in (
        "reset_L", "set_H", "neutral_N", "same_category_substitution", "upper_state_exchange_same_N")}
    cases["reset_L"].update(mean_TV=.02, maximum_TV=.059)
    cases["A_swap_effect"] = {"count": 100, "mean_TV": .25, "maximum_TV": .9}
    result = study.aggregate_swaps({"cases": cases, "natural_swap_pass": False})
    assert result["count"] == 6
    assert result["mean_TV"] == pytest.approx(.08 / 6)
    assert result["maximum_TV"] == .059
    assert set(result["failed_cases"]) == {"reset_L"}


def test_report_reader_keeps_historical_registration_and_authenticates_other_sources(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(study, "OUTPUT", tmp_path)
    monkeypatch.setattr(study, "identities", lambda: {"script": "report_revision", "module": "unchanged"})
    monkeypatch.setattr(study, "settings", lambda: {})
    monkeypatch.setattr(study, "all_runs", lambda: [])
    note = {"source_sha256": {"script": "trained_revision", "module": "unchanged"},
            "settings": {}, "runs": []}
    path = tmp_path / "registration.json"
    original = json.dumps(note)
    path.write_text(original)
    assert study.aggregate_registration() == note
    assert path.read_text() == original
    with pytest.raises(ValueError, match="registration differs"):
        study.registration()  # The training reader is unchanged and still refuses.
    note["source_sha256"]["module"] = "altered"
    path.write_text(json.dumps(note))
    with pytest.raises(ValueError, match="non-report authority differs"):
        study.aggregate_registration()
