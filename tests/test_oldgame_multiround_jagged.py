"""Exact controls for the grouped r11 jagged-competence study."""

from __future__ import annotations

import inspect
import json
from dataclasses import replace

import numpy as np
import pytest
import torch

from recombination_promotion.oldgame_ext.jagged_probes import fit_reader
from recombination_promotion.oldgame_ext.multiround_jagged import (
    BoardTables, DeviceStream, JaggedNetwork, batch_digest, grouped_loss,
    nested_dose_masks, rendering_ids,
)
from scripts import oldgame_multiround_jagged as study
from scripts import oldgame_multiround_raw_diagnosis as r9
from scripts import oldgame_multiround_route_access as r8


def _tables():
    return BoardTables(torch.device("cpu"))


def test_rarity_preserves_category_and_target_stream():
    tables = _tables()
    streams = [DeviceStream(tables, 0, "original", draw, batch=256, rounds=8)
               for draw in ("uniform", "cutoff", "decoy")]
    rows = [stream.draw_batch() for stream in streams]
    for row in rows[1:]:
        assert torch.equal(row.categories, rows[0].categories)
        assert torch.equal(row.targets, rows[0].targets)
        assert torch.equal(row.active, rows[0].active)
    assert not torch.equal(rows[0].board_ids, rows[1].board_ids)
    for stream, row in zip(streams, rows, strict=True):
        assert int(stream.board_exposure.sum()) == int(row.active.sum())
        assert int(stream.sum_exposure.sum()) == int(row.active.sum())
        assert int(stream.render_exposure.sum()) == int(row.active.sum())
        assert int(stream.rendering_exposure.sum()) == int(row.active.sum())
        assert int(stream.placement_exposure.sum()) == int(row.active.sum())
    assert [len(tables.by_sum[value]) for value in (12, 13, 23, 24)] == [
        285, 285, 25, 25]


def test_device_stream_resume_is_exact():
    tables = _tables()
    first = DeviceStream(tables, 1, "equal", "cutoff", batch=16)
    first.draw_batch()
    state = first.state()
    expected = first.draw_batch()
    second = DeviceStream(tables, 1, "equal", "cutoff", batch=16)
    second.restore(state)
    actual = second.draw_batch()
    assert torch.equal(actual.records, expected.records)
    assert torch.equal(actual.targets, expected.targets)
    assert second.rolling == first.rolling
    assert torch.equal(second.board_exposure, first.board_exposure)
    assert torch.equal(second.rendering_exposure, first.rendering_exposure)
    assert torch.equal(second.placement_exposure, first.placement_exposure)


def test_hash_binds_executed_records_and_placements(tmp_path):
    stream = DeviceStream(_tables(), 0, "original", "uniform", batch=4)
    row = stream.draw_batch()
    original = batch_digest(bytes(32), row)
    for name in ("records", "placements", "placement_indices"):
        altered = getattr(row, name).clone()
        altered.reshape(-1)[0] += 1
        assert batch_digest(bytes(32), replace(row, **{name: altered})) != original
    ids = rendering_ids(row.records)[row.active].numpy()
    assert np.array_equal(np.bincount(ids, minlength=30 ** 4),
                          stream.rendering_exposure.numpy())
    path = tmp_path / "counts.npz"
    exposure = study._exposures(stream, path)
    with np.load(path) as saved:
        assert np.array_equal(saved["rendering_counts"], stream.rendering_exposure.numpy())
        assert np.array_equal(saved["placement_counts"], stream.placement_exposure.numpy())
    for saved in exposure["r9_failure_renderings"]:
        assert saved["count"] == int(stream.rendering_exposure[saved["rendering_id"]])
    assert study._exposures(stream, path) == exposure


def test_futility_measures_B_loss_even_when_A_loss_changes():
    run = study.RunSpec("dose", "dose100", "original", 0)

    def point(b, a, accuracy=0.0):
        return {"train_loss_nats": a + b, "train_parts": {"A": a, "B": b},
                "A_accuracy": accuracy, "audit": {"natural_excess_KL_bits": 1.0}}

    first = point(2.0, 5.0)
    # A loss improves, but neither B loss nor A accuracy improves.
    unchanged_B = study._futility(first, point(2.0, 0.0), run)
    assert unchanged_B["stop"] and unchanged_B["training_gap_closed"] == 0
    # B improves while the A loss increases: combined loss would obscure this.
    improved_B = study._futility(first, point(1.7, 7.0), run)
    assert not improved_B["stop"] and improved_B["training_gap_closed"] > .1
    assert not study._futility(first, point(2.0, 0.0, accuracy=.1), run)["stop"]


def test_unseen_calibration_requires_nonempty_tracked_examples(monkeypatch):
    candidate, evidence = study._calibration_unseen("original", torch.device("cpu"))
    assert evidence["tracked_updates"] == 16
    assert evidence["composition"]["unmarked_test_positions"] > 0
    oracle = r8.ExactRowModel("raw_only", "original")
    score = study._score_b(oracle, "original", candidate, reject_empty=True)
    assert score["unseen_count"] == int(candidate.mask().sum()) > 0
    assert score["criteria"]["unseen_KL"] and score["unseen_excess_KL_bits"] < 1e-6
    candidate.seen[:] = True
    with pytest.raises(ValueError, match="unseen calibration panel is empty"):
        study._score_b(oracle, "original", candidate, reject_empty=True)
    # The training scorer keeps an empty exhausted panel failing the same bar.
    score = study._score_b(oracle, "original", candidate)
    assert score["unseen_count"] == 0 and not score["criteria"]["unseen_KL"]


def test_grouped_and_single_training_are_identical():
    tables = _tables()
    run0 = study.RunSpec("rarity", "uniform", "original", 0)
    run1 = study.RunSpec("rarity", "uniform", "original", 1)
    grouped = study.GroupEngine([run0, run1], torch.device("cpu"))
    singles = [study.GroupEngine([run], torch.device("cpu")) for run in (run0, run1)]
    group_streams = [DeviceStream(tables, run.seed, run.law, run.draw,
                                  batch=8, rounds=4) for run in (run0, run1)]
    solo_streams = [DeviceStream(tables, run.seed, run.law, run.draw,
                                 batch=8, rounds=4) for run in (run0, run1)]
    for _ in range(3):
        batches = [stream.draw_batch() for stream in group_streams]
        single_batches = [stream.draw_batch() for stream in solo_streams]
        assert all(torch.equal(left.records, right.records) for left, right in
                   zip(batches, single_batches, strict=True))
        grouped.update(batches, [None, None], torch.ones(2, dtype=torch.bool))
        for engine, batch in zip(singles, single_batches, strict=True):
            engine.update([batch], [None], torch.ones(1, dtype=torch.bool))
    for index, single in enumerate(singles):
        for key, value in grouped.parameters.items():
            assert torch.equal(value[index], single.parameters[key][0]), key
        assert grouped.optimizer.steps[index] == single.optimizer.steps[0]


def test_unselected_auxiliary_head_skips_AdamW_state_and_decay():
    runs = [study.RunSpec("dose", f"dose{dose}", "original", 0) for dose in (1, 10, 100)]
    grouped = study.GroupEngine(runs, torch.device("cpu"))
    single = study.GroupEngine([runs[0]], torch.device("cpu"))
    batch = DeviceStream(_tables(), 0, "original", "uniform", batch=4).draw_batch()
    original = grouped.parameters["raw_sum_head.weight"][0].clone()
    grouped.update([batch] * 3, [None, batch.active, batch.active],
                   torch.ones(3, dtype=torch.bool))
    single.update([batch], [None], torch.ones(1, dtype=torch.bool))
    assert torch.equal(grouped.parameters["raw_sum_head.weight"][0], original)
    assert torch.equal(single.parameters["raw_sum_head.weight"][0], original)
    assert grouped.optimizer.parameter_steps["raw_sum_head.weight"].tolist() == [0, 1, 1]


def test_width_three_AdamW_and_nonzero_disk_resume(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "OUTPUT", tmp_path / "authority")
    study.OUTPUT.mkdir()
    (study.OUTPUT / "registration.json").write_text("{}\n")
    (study.OUTPUT / "calibration.json").write_text("{}\n")
    monkeypatch.setattr(study, "registration", lambda: {})
    report = study.verify_equivalence(torch.device("cpu"), tmp_path / "verification",
                                      batch_size=8, steps=4, restore_step=2)
    assert report["pass"] and report["width"] == 3
    assert report["execution_widths"] == {"rarity": 3, "dose": 3, "erosion": 1}
    assert report["restoration_tolerance"] == "exact"
    assert report["restored_checkpoint_update"] == 2
    for rows in report["results"].values():
        for row in rows.values():
            assert all(comparison["pass"] for comparison in row.values())
            assert all(row["uninterrupted_vs_nonzero_restore"]["exact_state"].values())
            assert row["uninterrupted_vs_nonzero_restore"]["parameters"][
                "maximum_absolute_difference"] == 0
            assert all(value["maximum_absolute_difference"] == 0 for value in
                       row["uninterrupted_vs_nonzero_restore"]["optimizer_moments"].values())


def test_width_one_erosion_is_direct_without_vmap(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("width one must not use vmap")

    monkeypatch.setattr(study, "vmap", forbidden)
    run = study.RunSpec("erosion", "b_only", "original", 0)
    engine = study.GroupEngine([run], torch.device("cpu"))
    ordinary = engine.model_at(0)
    row = DeviceStream(_tables(), 0, "original", "uniform", batch=8).draw_batch()
    output = engine.forward(row.records[None], row.lengths[None])
    reference = ordinary(row.records, row.lengths, return_all=True)
    assert all(torch.equal(left[0], right) for left, right in zip(output, reference, strict=True))
    engine.update([row], [None], torch.ones(1, dtype=torch.bool))


def test_hard_A_trace_records_disagreement_margins_and_excludes_padding():
    left = torch.zeros((1, 2, 5, 36))
    right = left.clone()
    left[0, :, 3, 4], left[0, :, 3, 5] = 1.0001, 1.
    right[0, :, 3, 4], right[0, :, 3, 5] = 1., 1.0002
    row = study._hard_a_difference(left, right, torch.tensor([[True, False]]))
    assert row["active_slot_answers"] == 5
    assert row["disagreeing_rounds"] == row["disagreeing_slot_answers"] == 1
    difference, = row["disagreements"]
    assert (difference["episode"], difference["round"], difference["slot"]) == (0, 0, 3)
    assert difference["left"]["top_two_classes"] == [4, 5]
    assert difference["right"]["top_two_classes"] == [5, 4]
    assert difference["left"]["margin"] == pytest.approx(.0001, abs=1e-7)
    assert difference["right"]["margin"] == pytest.approx(.0002, abs=1e-7)
    differences = study._difference_fields({"weight": torch.tensor([1., 2.]), "bias": None},
                                           {"weight": torch.tensor([1., 3.]), "bias": None})
    assert differences["weight"]["difference_norm"] == 1.
    assert differences["weight"]["maximum_absolute_difference"] == 1.
    assert differences["bias"]["left_absent"] and differences["bias"]["right_absent"]


def test_erosion_comparison_trace_persists_every_update(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "OUTPUT", tmp_path / "authority")
    study.OUTPUT.mkdir()
    (study.OUTPUT / "registration.json").write_text("{}\n")
    (study.OUTPUT / "calibration.json").write_text("{}\n")
    monkeypatch.setattr(study, "registration", lambda: {})
    output = tmp_path / "trace"
    result = study.verify_equivalence(torch.device("cpu"), output, batch_size=8,
                                      steps=4, restore_step=2, trace_erosion=True)
    assert result["pass"] and result["execution_widths"] == {"erosion": 3}
    saved = json.loads((output / "erosion_trace_cpu.json").read_text())
    assert saved["trace"]["run"] == "erosion_b_only_original_seed0"
    assert [row["update"] for row in saved["trace"]["updates"]] == [1, 2, 3, 4]
    for row in saved["trace"]["updates"]:
        assert row["before_update"]["hard_A"]["active_rounds"] > 0
        assert row["before_update"]["hard_A"]["disagreeing_slot_answers"] == 0
        assert row["before_update"]["parameters"].keys() == row["after_update_gradients"].keys()
        assert all(value["maximum_absolute_difference"] in (None, 0.) for value in
                   row["after_update_gradients"].values())


def test_erosion_starts_share_exact_A_and_B_only_has_no_A_loss():
    runs = [study.RunSpec("erosion", arm, "original", 0)
            for arm in ("b_only", "a_plus_b")]
    engine = study.GroupEngine(runs, torch.device("cpu"))
    assert all(torch.equal(value[0], value[1]) for value in engine.parameters.values())
    assert study.local_a_accuracy(engine.model_at(0), torch.device("cpu")) == {
        "correct": 1555, "total": 1555}
    tables = _tables()
    batches = [DeviceStream(tables, 0, "original", "uniform", batch=4,
                            rounds=3).draw_batch() for _ in runs]
    outputs = engine.forward(torch.stack([row.records for row in batches]),
                             torch.stack([row.lengths for row in batches]))
    _, details = grouped_loss(outputs, batches, [None, batches[1].active], dual=True)
    assert details[0]["A"] == 0.0
    assert details[1]["A"] > 0
    assert details[1]["A_selected_rounds"] == details[1]["active_rounds"]


def test_dose_masks_are_nested_and_loss_uses_all_active_rounds():
    active = torch.ones((256, 8), dtype=torch.bool)
    masks = nested_dose_masks(active, 400, device=torch.device("cpu"))
    assert not masks[0].any()
    assert torch.all(masks[1] <= masks[10])
    assert torch.all(masks[10] <= masks[100])
    assert torch.equal(masks[1], nested_dose_masks(
        active, 400, device=torch.device("cpu"))[1])
    runs = [study.RunSpec("dose", "dose1", "original", 0)]
    engine = study.GroupEngine(runs, torch.device("cpu"))
    batch = DeviceStream(_tables(), 0, "original", "uniform", batch=8,
                         rounds=4).draw_batch()
    outputs = engine.forward(batch.records[None], batch.lengths[None])
    selected = torch.zeros_like(batch.active)
    selected[0, 0] = True
    losses, details = grouped_loss(outputs, [batch], [selected], dual=False)
    assert details[0]["A"] > 0
    assert details[0]["A_selected_rounds"] == 1
    # A single selected round is divided by every active round, not by one.
    assert details[0]["A"] < 6 / details[0]["active_rounds"]
    assert torch.isfinite(losses).all()


def test_probe_labels_do_not_enter_network_and_splits_by_board():
    signature = inspect.signature(JaggedNetwork.forward)
    assert "targets" not in signature.parameters
    assert "categories" not in signature.parameters
    split = r8.probe_split()
    assert not set(split["train_board_ids"]) & set(split["heldout_board_ids"])
    model = JaggedNetwork().eval()
    records = torch.zeros((2, 3, 4, 2), dtype=torch.long)
    lengths = torch.full((2,), 3)
    before = model(records, lengths)[1]
    changed_labels = torch.randint(0, 3, (2, 3))
    del changed_labels
    assert torch.equal(before, model(records, lengths)[1])


def test_torch_linear_probe_matches_saved_r8_sklearn():
    model, _ = r9.load_model("raw_only", 0)
    split = r8.probe_split()
    (train_records, train_y), (heldout_records, heldout_y) = r8._probe_data(split)
    x = r8._carrier(model, train_records)[0]
    z = r8._carrier(model, heldout_records)[0]
    torch_row = fit_reader(torch.from_numpy(x), torch.from_numpy(train_y[:, 0]),
                           torch.from_numpy(z), torch.from_numpy(heldout_y[:, 0]),
                           family="linear", seed=0)
    reference = r8._fit_probe(x, train_y[:, 0], z, heldout_y[:, 0],
                              family="linear", seed=0)
    assert torch_row["converged"] and reference["converged"]
    assert (torch_row["fit_device"], torch_row["score_device"],
            torch_row["fit_threads"]) == ("cpu", "cpu", 1)
    assert np.mean(np.asarray(torch_row["predictions"]) ==
                   np.asarray(reference["predictions"])) >= .98


def test_group_census_and_audit_path_reduced():
    run = study.RunSpec("rarity", "uniform", "original", 0)
    engine = study.GroupEngine([run], torch.device("cpu"))
    audit = study.audit_one(engine.model_at(0), "original", torch.device("cpu"),
                            study._candidate_panel("original"), smoke=True)
    assert audit["evaluation_precision"] == "float32"
    assert audit["probes"]["probe_fit_devices"] == {
        "linear": "cpu", "mlp64": "cpu"}
    assert audit["board_census"]["registered_rendering"]["boards"] >= 128
    saved = audit["board_census"]["saved_r9_failed_renderings"]
    assert saved["count"] > 0 and all(row["records"] for row in saved["rows"])
    assert audit["unseen_count"] > 0
    assert audit["probes"]["sites"]["raw"]["linear"]["sum36"][0]["total"] == 64
    assert audit["probes"]["sites"]["raw"]["linear"]["sum36"][0][
        "fit_device"] == "cpu"


def test_early_erosion_readouts_are_executed(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "OUTPUT", tmp_path / "authority")
    study.OUTPUT.mkdir()
    (study.OUTPUT / "registration.json").write_text("{}\n")
    (study.OUTPUT / "calibration.json").write_text("{}\n")
    a = {"per_slot": [{"correct": 128, "total": 128}] * 5,
         "vector": {"correct": 128, "total": 128}, "reduced_smoke": True}
    monkeypatch.setattr(study, "a_accuracy", lambda *args, **kwargs: a)
    monkeypatch.setattr(study, "local_a_accuracy", lambda *args: {"correct": 1555, "total": 1555})

    def minimal_audit(model, run, candidate, stream, device, step, loss, details, counts,
                      **kwargs):
        return {"step": step, "train_parts": details, "A_accuracy": 1.0,
                "A_local_history_accuracy": {"correct": 1555, "total": 1555},
                "audit": {"elapsed_seconds": 0.0, "natural_excess_KL_bits": .1},
                "dose_selected_by_slot_sum": counts.tolist(), "exposure": {}}

    monkeypatch.setattr(study, "_audit_record", minimal_audit)
    run = study.RunSpec("erosion", "b_only", "original", 0)
    study._run_chunk([run], torch.device("cpu"), tmp_path / "run",
                     steps=5, smoke=True, precision="fp32")
    folder = tmp_path / "run" / "runs" / run.name
    assert sorted(path.name for path in folder.glob("erosion_step_*.json")) == [
        "erosion_step_000001.json", "erosion_step_000005.json"]
    assert study.EROSION_READOUTS == (1, 5, 10, 50, 100)


def test_group_and_per_run_checkpoint_resume(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "OUTPUT", tmp_path)
    (tmp_path / "registration.json").write_text("{}\n")
    (tmp_path / "calibration.json").write_text("{}\n")
    runs = [study.RunSpec("rarity", "uniform", "original", 0),
            study.RunSpec("rarity", "uniform", "original", 1)]
    tables = _tables()
    engine = study.GroupEngine(runs, torch.device("cpu"))
    streams = [DeviceStream(tables, run.seed, run.law, run.draw, batch=8, rounds=4)
               for run in runs]
    candidates = [study._candidate_panel(run.law) for run in runs]
    curves = [[{"step": 0}], [{"step": 0}]]
    group = tmp_path / "checkpoint_step_000000.pt"
    study._save_group(group, engine, streams, candidates, runs, curves,
                      [False, False], 0, "fp32")
    folders = [tmp_path / run.name for run in runs]
    for folder in folders:
        folder.mkdir()
    study._save_run_checkpoints(group, folders, engine, streams, candidates,
                                curves, [False, False], 0)
    for folder in folders:
        path = folder / "checkpoint_step_000000.pt"
        assert path.with_suffix(".sha256").read_text().strip() == study.sha(path)
    restored = study.GroupEngine(runs, torch.device("cpu"))
    new_streams = [DeviceStream(tables, run.seed, run.law, run.draw,
                                batch=8, rounds=4) for run in runs]
    new_candidates = [study._candidate_panel(run.law) for run in runs]
    step, saved_curve, stopped = study._restore_group(
        tmp_path, restored, new_streams, new_candidates, runs, "fp32")
    assert (step, saved_curve, stopped) == (0, curves, [False, False])
    assert all(torch.equal(engine.parameters[key], restored.parameters[key])
               for key in engine.parameters)


def test_bf16_requires_paired_gpu_smoke(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "OUTPUT", tmp_path / "authority")
    study.OUTPUT.mkdir()
    (study.OUTPUT / "registration.json").write_text("{}\n")
    (study.OUTPUT / "calibration.json").write_text("{}\n")
    monkeypatch.setattr(study, "registration", lambda: {})
    names = [run.name for group in study.EXPERIMENTS
             for run in study.group_runs(group, smoke=True)]
    for precision in ("fp32", "bf16"):
        for name in names:
            folder = tmp_path / precision / "runs" / name
            folder.mkdir(parents=True)
            study.write_json(folder / "summary.json", {
                "precision": precision, "device": "cuda", "last_step": 1000,
                "reduced_smoke": True,
                "curve": [{"step": step, "B_loss": 1.0,
                           "natural_KL": .1, "A_vector_accuracy": .25}
                          for step in (0, 1000)]})
    result = study.compare_precision(tmp_path / "fp32", tmp_path / "bf16")
    assert result["accepted"]
    assert len(result["runs"]) == 8
    assert (study.OUTPUT / "precision_comparison.json").exists()


def test_aggregate_short_and_extrapolation_panels_and_A_rerender_failures():
    names = ["L_single_round", "H_single_round", *[f"N_run_{k}" for k in range(1, 9)]]
    law = {"cases": {key: {"count": 32 if i < 2 else 64,
                            "mean_TV": .001, "maximum_TV": .01}
                     for i, key in enumerate(names)}}
    law["cases"]["N_run_2"]["maximum_TV"] = .04
    law["cases"]["N_run_8"]["maximum_TV"] = .25
    result = study._aggregate_law(law)
    assert result["panels"]["short"]["count"] == 192
    assert result["panels"]["extrapolation"]["count"] == 384
    assert not result["panels"]["short"]["pass"]
    assert result["panels"]["extrapolation"]["maximum_TV"] == .25
    assert result["largest_error_cases"] == ["N_run_8"]
    audit = {"rerender": {"maximum_TV": 1.1920928955078125e-7,
                          "A_answer_mismatched_components": 35, "pass": False},
             "natural_excess_KL_bits": .00001, "unseen_excess_KL_bits": .00002,
             "unseen_count": 12, "swaps": {}, "route_damage": {},
             "mode_law": {"witness_recovery_fraction": 1., "witness_pair_mean_prediction_TV": 0.}}
    checks = study._aggregate_prediction_checks(audit)
    assert checks["rerender_prediction_pass"]
    assert not checks["rerender_A_answer_pass"]
    assert not checks["registered_rerender_pass"]


def test_aggregate_exposure_keeps_selected_counts():
    exposure = {"by_slot1_sum": [100] + [0] * 36,
                "complete_rendering_counts": {"total": 100}, "r9_failure_renderings": []}
    selected = [[10] + [0] * 36] * 5
    row = study._aggregate_exposure(exposure, selected)
    assert row["selected_A_rounds"] == 10 and row["active_rounds"] == 100
    assert row["observed_dose"] == .1 and row["dose_selected_by_slot_sum"] == selected
    with pytest.raises(ValueError, match="dose counts differ across slots"):
        study._aggregate_exposure(exposure, [[11] + [0] * 36, *selected[1:]])


def test_dose_joint_counts_are_not_marginal_errors():
    row = study._aggregate_dose_counts([0, 13, 24, 36], [13, 13, 12, 36], [1, 0, 2, 2])
    assert row == {"A_head_category_errors": 2, "B_signature_errors": 2,
                   "B_errors_with_correct_A_category": 1, "boards": 4}
    with pytest.raises(ValueError, match="dose decomposition arrays differ"):
        study._aggregate_dose_counts([0], [0], [3])


def test_posthoc_dose_replay_authenticates_and_preserves_checkpoint(tmp_path, monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr(study, "OUTPUT", tmp_path)
    (tmp_path / "registration.json").write_text("{}\n")
    (tmp_path / "calibration.json").write_text("{}\n")
    boards = study.enumerate_boards()
    sums = np.asarray(boards.boards)[:, 0]
    indices = np.asarray([np.flatnonzero(sums == value)[0] for value in (0, 13, 36)])
    records = study._census_records(boards, indices, render_offset=0).copy()
    monkeypatch.setattr(study, "enumerate_boards", lambda: SimpleNamespace(
        boards=[boards.boards[index] for index in indices]))
    monkeypatch.setattr(study, "_census_records", lambda *args, **kwargs: records)
    model = JaggedNetwork(dual=False)
    with torch.no_grad():
        model.raw_sum_head.weight.zero_()
        model.raw_sum_head.bias.zero_()
        model.category_head.weight.zero_()
        model.category_head.bias.copy_(torch.tensor(r9.TRUTH[0]).float().log())
    path = tmp_path / "checkpoint_step_020000.pt"
    torch.save({"step": 20000, "futility_stop": False, "model": model.state_dict(),
                "registration_sha256": study.sha(tmp_path / "registration.json"),
                "calibration_sha256": study.sha(tmp_path / "calibration.json")}, path)
    digest = study.sha(path)
    path.with_suffix(".sha256").write_text(digest + "\n")
    row = study._aggregate_dose_replay(tmp_path, expected_signature=2)
    assert (row["A_head_category_errors"], row["B_signature_errors"],
            row["B_errors_with_correct_A_category"]) == (2, 2, 0)
    assert row["replay"]["CPU_threads"] == 1
    assert row["replay"]["source_parameters_unchanged"]
    assert row["replay"]["parameter_updates"] == 0
    assert row["status"] == "POST_HOC_CPU_CHECKPOINT_REPLAY"
    assert study.sha(path) == digest
    with pytest.raises(ValueError, match="signature differs from saved census"):
        study._aggregate_dose_replay(tmp_path, expected_signature=1)
    path.with_suffix(".sha256").write_text("different digest\n")
    with pytest.raises(ValueError, match="checkpoint digest differs"):
        study._aggregate_dose_replay(tmp_path, expected_signature=2)


def test_aggregate_contains_saved_counts_controls_curves_and_scientific_specification(tmp_path, monkeypatch):
    from copy import deepcopy

    review = (study.OUTPUT / "analysis_specification.json").read_text()
    root = tmp_path / "report"
    root.mkdir()
    monkeypatch.setattr(study, "OUTPUT", root)
    runs = [study.RunSpec("rarity", "uniform", "original", 1),
            study.RunSpec("dose", "dose1", "original", 0),
            study.RunSpec("erosion", "b_only", "equal", 2),
            study.RunSpec("erosion", "a_plus_b", "original", 2)]
    monkeypatch.setattr(study, "all_runs", lambda: runs)
    monkeypatch.setattr(study, "source_identities", lambda: {"script": "report revision", "module": "unchanged"})
    study.write_json(root / "registration.json", {
        "runs": [r.name for r in runs], "source_sha256": {"script": "training revision", "module": "unchanged"},
        "claims_and_readings_verbatim": "REGISTERED READINGS UNCHANGED"})
    (root / "analysis_specification.json").write_text(review)
    split = tmp_path / "probe_split.json"
    split.write_text("{}\n")
    monkeypatch.setattr(r8, "OUTPUT", tmp_path)
    monkeypatch.setattr(r8, "_probe_data", lambda _: (None, (None, np.zeros((4, 5), dtype=np.int64))))

    def no_evaluation(*args, **kwargs):
        raise AssertionError("aggregate must not rerun model audits")

    monkeypatch.setattr(study, "new_model", no_evaluation)
    monkeypatch.setattr(study, "audit_one", no_evaluation)
    monkeypatch.setattr(study, "_aggregate_dose_replay", lambda folder, signature: {
        "A_head_category_errors": 552, "B_signature_errors": signature,
        "B_errors_with_correct_A_category": 24, "boards": 24435,
        "status": "POST_HOC_CPU_CHECKPOINT_REPLAY", "replay": {"CPU_threads": 1, "parameter_updates": 0}})

    def probe(prediction, converged=True):
        row = {"predictions": [prediction] * 4, "accuracy": float(prediction == 0),
               "correct": 4 if prediction == 0 else 0, "total": 4,
               "converged": converged, "n_iter": [4], "convergence_warnings": [], "fit_device": "cpu"}
        return {"floors": {task: [{"majority_accuracy": .5, "shuffled_accuracy": .25}] * 5
                           for task in ("sum36", "category3")},
                "sites": {site: {family: {task: [deepcopy(row) for _ in range(5)]
                          for task in ("sum36", "category3")} for family in ("linear", "mlp64")}
                          for site in ("raw", "upper")}}

    study.write_json(root / "calibration.json", {"probe": {"oracle": probe(0)}})
    cases = {key: {"count": 32, "mean_TV": .001, "maximum_TV": .01}
             for key in ["L_single_round", "H_single_round", *[f"N_run_{k}" for k in range(1, 9)]]}
    rerender = {"maximum_TV": 1.1920928955078125e-7, "A_answer_mismatched_components": 35,
                "pass": False}
    rendering = {"boards": 24435, "categorical_misreads": 81, "above_0_02_TV": 2}
    endpoint = {"step": 20000, "A_board_accuracy": {
        "per_slot": [{"correct": 24434, "total": 24435}] * 5,
        "vector": {"correct": 24419, "total": 24435}},
        "A_local_history_accuracy": {"correct": 1447, "total": 1555},
        "dose_selected_by_slot_sum": [[10] + [0] * 36] * 5,
        "audit": {"B_pass": False, "criteria": {"rerender": False},
            "mode_law": {"cases": cases, "witness_recovery_fraction": 1., "witness_pair_mean_prediction_TV": 0.},
            "swaps": {"cases": {"neutral_N": {"count": 64, "mean_TV": .01, "maximum_TV": .02}}},
            "board_census": {"registered_rendering": rendering,
                "additional_fixed_renderings": [{**rendering, "categorical_misreads": i} for i in (3, 4, 5)],
                "saved_r9_failed_renderings": {"count": 101, "categorical_misreads": 2, "above_0_02_TV": 7}},
            "natural_excess_KL_bits": .00001, "unseen_excess_KL_bits": .00002,
            "unseen_count": 12, "rerender": rerender, "route_damage": {}, "probes": probe(0, False)}}
    early = {"step": 1, "A_board_accuracy": endpoint["A_board_accuracy"], "train_parts": {"B": 1.}}
    for run in runs:
        folder = root / "runs" / run.name
        study.write_json(folder / "audit_step_020000.json", endpoint)
        study.write_json(folder / "audit_step_000000.json", {
            **endpoint, "step": 0, "audit": {**endpoint["audit"], "probes": probe(1)}})
        study.write_json(folder / "summary.json", {"futility_stop": False,
            "exposure": {"by_slot1_sum": [100] + [0] * 36,
                         "complete_rendering_counts": {"total": 100}, "r9_failure_renderings": []},
            "curve": [{"step": 20000, "B_loss": 1., "A_loss": .1,
                       "natural_KL": .00001, "A_vector_accuracy": .9}], "early_erosion_readouts": [early]})
    assert study.aggregate(torch.device("cpu")) == {"reported_runs": 4, "missing_runs": 0}
    report = json.loads((root / "aggregate.json").read_text())
    assert report["registered_readings_verbatim"] == "REGISTERED READINGS UNCHANGED"
    row = report["erosion"]["erosion_b_only_equal_seed2"]
    assert row["prediction_checks"]["rerender_prediction_pass"]
    assert not row["prediction_checks"]["rerender_A_answer_pass"]
    assert row["A_components"]["vector"]["correct"] == 24419
    p = row["probe_changes"]["raw"]["linear"]["sum36"][0]
    assert (p["majority_floor"], p["oracle_floor"], p["paired_CI95"]) == (.5, 1., [1., 1.])
    assert not p["converged"] and not p["readability_gain"]
    assert report["dose_decomposition"]["dose_dose1_original_seed0"]["A_head_category_errors"] == 552
    assert report["dose_decomposition"]["dose_dose1_original_seed0"]["reference_seed0_match"]
    assert report["dose_decomposition"]["dose_dose1_original_seed0"]["status"] == "POST_HOC_CPU_CHECKPOINT_REPLAY"
    assert report["erosion_B_only_alphabets"]["1"]["twelfths"] == [0, 8]
    assert report["linear_comparison_convergence"] == {"converged": 0, "total": 80}
    md = (root / "aggregate.md").read_text()
    for text in ("24419/24435", "1447/1555", "N_run_8", "Short mean / max", "Extrapolation mean / max",
                 "raw / linear / sum36 / 1", "upper / mlp64 / category3 / 5", "Early update",
                 "dose1_original_seed0", "552", "not a matched causal comparison", "post-hoc"):
        assert text in md
