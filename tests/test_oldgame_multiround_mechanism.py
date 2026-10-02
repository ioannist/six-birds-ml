"""CPU regressions for the separately registered r13 mechanisms."""

import copy
import json
from types import SimpleNamespace

import pytest
import torch
from torch.nn import functional as F

from recombination_promotion.oldgame_ext.memory import VALUES
from recombination_promotion.oldgame_ext.multiround_coverage import CoverageStream
from recombination_promotion.oldgame_ext.multiround_mechanism import (
    MechanismNetwork, Run, all_runs, encode_answers, exact_rows,
    cutoff_summary, fixed_geometry_pairs, gradient_conflict, hard_answers, histories_logits,
    loss_parts, margin_counts, matched_sgd_rate, prediction_loss,
)
from scripts import oldgame_multiround_mechanism as study
from recombination_promotion.oldgame_ext import mechanism_geometry as geometry


@pytest.fixture(scope="module")
def tables():
    torch.set_num_threads(1)
    return study.r11.BoardTables(torch.device("cpu"))


@pytest.fixture
def batch(tables):
    return CoverageStream(tables, 0, "original", "uniform").draw_batch()


def test_declared_run_counts_and_pairing(tables):
    runs = all_runs()
    assert sum(r.experiment == "erosion" for r in runs) == 12
    assert sum(r.experiment != "erosion" for r in runs) == 33
    streams = [CoverageStream(tables, 0, "original", "uniform") for _ in range(4)]
    batches = [s.draw_batch() for s in streams]
    assert all(torch.equal(b.records, batches[0].records) for b in batches)
    assert all(torch.equal(b.targets, batches[0].targets) for b in batches)
    assert len({s.rolling.hex() for s in streams}) == 1
    assert torch.equal(streams[0].stratum_exposure, torch.full((2, 8), 8))


@pytest.mark.parametrize("probability", [False, True])
def test_loss_normalization_and_floor(batch, probability):
    p = exact_rows(batch)
    assert torch.equal(p.sum(-1), torch.ones_like(batch.targets).float())
    logits = p.log()
    loss, floor = prediction_loss(logits, batch, probability=probability)
    assert torch.equal(loss, floor)
    q = torch.randn_like(logits)
    loss, _ = prediction_loss(q, batch, probability=probability)
    ce = -(p * q.log_softmax(-1)).sum(-1) if probability else F.cross_entropy(
        q.flatten(0, 1), batch.targets.flatten(), reduction="none").reshape_as(batch.targets)
    assert torch.equal(loss, .5 * (ce[:128].mean() + ce[128:][batch.b_active[128:]].mean()))


def test_first_batch_sgd_rate_is_norm_matched():
    g = [torch.tensor([1., .0001, 0.]), torch.tensor([-.2])]
    rate = matched_sgd_rate(g)
    sgd = torch.cat([rate * x for x in g]).norm()
    adam = torch.cat([.003 * x / (x.abs() + 1e-8) for x in g]).norm()
    assert torch.allclose(sgd, adam)
    with pytest.raises(ValueError, match="zero"):
        matched_sgd_rate([torch.zeros(1)])


def test_probability_only_optimizer_has_no_sum_labels(batch):
    model = MechanismNetwork("raw_probability")
    r = Run("noise", "raw_probability", 0)
    out = model(batch.records, batch.lengths, return_all=True)
    original = loss_parts(out, batch, r)[0]
    corrupt = copy.copy(batch)
    corrupt.sums = torch.full_like(batch.sums, 999)
    assert torch.equal(original, loss_parts(out, corrupt, r)[0])
    original.backward()
    assert all(p.grad is None for p in model.raw_sum_head.parameters())
    assert all(p.grad is None for p in model.memory.parameters())


def test_frozen_supplier_and_live_head(batch):
    model = MechanismNetwork("frozen")
    old = {n: p.clone() for n, p in model.named_parameters() if n.startswith("supplier_")}
    head = model.raw_sum_head.weight.detach().clone()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=.003)
    loss_parts(model(batch.records, batch.lengths, return_all=True), batch,
               Run("access", "frozen", 0))[0].backward()
    opt.step()
    assert all(torch.equal(old[n], p) for n, p in model.named_parameters() if n in old)
    assert not torch.equal(head, model.raw_sum_head.weight)


def test_live_route_gradients_and_detached_negative(batch):
    live = MechanismNetwork("live")
    detached = MechanismNetwork("frozen")
    assert gradient_conflict(live, batch)["live_sums_route_prediction_gradient_norm"] > 0
    assert gradient_conflict(detached, batch)["live_sums_route_prediction_gradient_norm"] == 0
    x = torch.randn(4, 5, 36, requires_grad=True)
    assert torch.equal(hard_answers(x).detach(), F.one_hot(x.argmax(-1), 36).float())


def test_numerical_encoding_same_width():
    onehot = F.one_hot(torch.arange(36), 36).float()
    numerical = encode_answers(onehot, "numerical")
    assert numerical.shape == onehot.shape
    assert torch.equal(numerical[:, 0], torch.tensor(VALUES).float() / 36)
    assert torch.equal(numerical[:, 1], 1 - numerical[:, 0])
    assert torch.count_nonzero(numerical[:, 2:]) == 0


def test_geometry_panel_precedes_states():
    boards = SimpleNamespace(boards=[(0, 0, 0, 0, 0), (1, 0, 0, 0, 0),
                                    (5, 0, 0, 0, 0), (1, 1, 0, 0, 0)])
    allocation = {"train": [0, 1, 2], "heldout": [3]}
    first = fixed_geometry_pairs(boards, allocation)
    assert first == fixed_geometry_pairs(boards, allocation)
    assert first["train"]["pairs"] == [[0, 1, 0, 1], [0, 2, 0, 5], [1, 2, 1, 5]]
    assert first["heldout"]["pairs"] == []


def test_erosion_blocked_gradient_preserves_only_decay(tables):
    model = study.new_model(0, True, repo_root=study.ROOT)
    s = study.DeviceStream(tables, 0, "original", "uniform", batch=8)
    batch = s.draw_batch()
    sums = [p for n, p in model.named_parameters() if n.startswith("memory.")]
    other = [p for n, p in model.named_parameters() if not n.startswith("memory.")]
    old = [p.clone() for p in sums]
    record, _ = study.erosion_step(model, batch,
        torch.optim.AdamW(sums, lr=.003, weight_decay=.01),
        torch.optim.AdamW(other, lr=.003, weight_decay=.01), blocked=True)
    assert all(torch.equal(p, q * .99997) for p, q in zip(sums, old, strict=True))
    assert all(r["gradient"]["norm"] == 0 for r in record["tensors"].values())


def test_exact_local_a_and_planted_flip():
    model = study.new_model(0, True, repo_root=study.ROOT)
    logits = histories_logits(model.memory)
    assert margin_counts(logits)["correct"] == 1555
    changed = logits.detach().clone()
    changed[0, (int(changed[0].argmax()) + 1) % 36] = changed[0].max() + 1
    assert margin_counts(changed)["correct"] == 1554


def test_noise_init_paired_and_access_checkpoint_identity():
    a = study.make_model(Run("noise", "raw_sampled", 0), torch.device("cpu"))
    b = study.make_model(Run("noise", "sums_probability", 0), torch.device("cpu"))
    assert all(torch.equal(v, b.state_dict()[n]) for n, v in a.state_dict().items())
    models = [study.make_model(Run("access", c, 0), torch.device("cpu"))
              for c in ("disconnected", "frozen", "live", "exact")]
    assert all(torch.equal(v, model.state_dict()[n]) for model in models[1:]
               for n, v in models[0].state_dict().items())


def test_futility_uses_prediction_only():
    first = {"train_parts": {"B": 2., "A": 20., "target_floor": 1.},
             "audit": {"natural_excess_KL_bits": .2}, "A_accuracy": 0.}
    current = {"train_parts": {"B": 2., "A": 0., "excess_prediction_loss": 1.},
               "audit": {"natural_excess_KL_bits": .2}, "A_accuracy": 0.}
    run = Run("noise", "sums_probability", 0)
    assert study.futility(first, current, run)["stop"]
    current["train_parts"]["B"] = 1.5
    current["train_parts"]["excess_prediction_loss"] = .5
    assert not study.futility(first, current, run)["stop"]


def test_futility_sampled_floor_changes_are_not_learning():
    first = {"train_parts": {"B": 1.2, "target_floor": 1.},
             "audit": {"natural_excess_KL_bits": .2}, "A_accuracy": 0.}
    # A hundred different sampled-target floors; the model's excess is constant.
    rows = [{"B": i / 100 + .4, "target_floor": i / 100 + .2,
             "excess_prediction_loss": .2} for i in range(100)]
    current = {"train_parts": study.r12._mean(rows), "audit": first["audit"], "A_accuracy": 0.}
    result = study.futility(first, current, Run("noise", "raw_sampled", 0))
    assert abs(result["prediction_loss_gap_closed"]) < 1e-12
    assert result["stop"]
    first["train_parts"]["B"] = .9  # initial excess is negative
    result = study.futility(first, current, Run("noise", "raw_sampled", 0))
    assert result["prediction_loss_gap_closed"] is None
    assert not result["stop"]
    assert study.futility_calibration()["pass"]


def test_oracle_futility_changes_only_sampled_targets(batch):
    logits = exact_rows(batch).log()
    rows = []
    for target in ([0, 2] * 50):
        changed = copy.copy(batch)
        changed.targets = torch.full_like(batch.targets, target)
        loss, floor = prediction_loss(logits, changed, probability=False)
        rows.append({"B": float(loss), "target_floor": float(floor),
                     "excess_prediction_loss": float(loss - floor)})
    assert rows[0]["target_floor"] != rows[1]["target_floor"]
    first = {"train_parts": rows[0], "audit": {"natural_excess_KL_bits": 0.}, "A_accuracy": 0.}
    current = {**first, "train_parts": study.r12._mean(rows)}
    result = study.futility(first, current, Run("noise", "raw_sampled", 0))
    assert result["current_excess_prediction_loss"] == 0.
    assert result["prediction_loss_gap_closed"] is None
    assert not result["stop"]


def test_batch_direct_and_nonzero_restore(tmp_path, monkeypatch):
    from scripts.oldgame_mechanism_report import recorded_registration
    monkeypatch.setattr(study, "registration", recorded_registration)
    # Host stage uses precisely this executable check, including optimizer moments.
    result = study.verification(torch.device("cpu"), tmp_path, trace=True)
    assert result["pass"]
    assert result["comparisons"]["sums_probability"]["width"] == 3
    assert result["comparisons"]["live"]["width"] == 1
    assert all(r["restoration_exact"] for r in result["comparisons"].values())


def test_reduced_and_equal_rows_cannot_support_study_readings():
    experiments = {k: [] for k in ("erosion", "noise", "access", "encoding")}
    experiments["encoding"] = [{"run": Run("encoding", "numerical", 0).__dict__,
                               "endpoint_status": "REDUCED_SMOKE"},
                              {"run": Run("encoding", "numerical", 0, "equal").__dict__,
                               "endpoint_status": "CONTROL_ONLY"}]
    readings = study.comparison_readings(experiments, {"geometry": False})
    assert readings["encoding"]["selected_reading"] == "NO_STUDY_ENDPOINTS"


def test_geometry_pair_calibration_and_original_failure():
    calibration = geometry.calibration()
    assert calibration["pass"]
    assert calibration["readers"]["numerical"]["accuracy"] == 1.
    for name in ("constant", "encoding_balanced"):
        row = calibration["readers"][name]
        assert row["accuracy"] == .5
        assert abs(row["cross_entropy_nats"] - geometry.math.log(2)) < 1e-6
        assert row["converged"]
    failure = json.loads((study.OUTPUT / "geometry_failure_build_v1.json").read_text())
    assert not failure["geometry"]["pass"]
    assert failure["geometry"]["readers"]["numerical_permuted"]["correct"] == 72


def test_geometry_accuracy_alone_is_insufficient():
    positive = {"accuracy": 1., "converged": True, "cross_entropy_nats": .69}
    negative = {"accuracy": .5, "converged": True, "cross_entropy_nats": geometry.math.log(2)}
    assert not geometry.discrimination_decision(positive, [negative])["pass"]
    positive["cross_entropy_nats"] = .01
    assert geometry.discrimination_decision(positive, [negative])["pass"]
    positive["converged"] = False
    assert not geometry.discrimination_decision(positive, [negative])["pass"]
    with pytest.raises(ValueError, match="identities overlap"):
        geometry.score_pair_discrimination(torch.zeros(2, 3), torch.tensor([0, 1]),
            torch.zeros(2, 3), torch.tensor([0, 1]), train_ids=[0, 1], heldout_ids=[1, 2])


def test_geometry_amendment_separate_from_training(tmp_path, monkeypatch):
    training_sources = study.identities()
    training_settings = study.settings()
    for filename in ("geometry_pairs.json", "geometry_failure_build_v1.json"):
        (tmp_path / filename).write_bytes((study.OUTPUT / filename).read_bytes())
    monkeypatch.setattr(study, "OUTPUT", tmp_path)
    before = study.geometry_amendment(rebuild=True)
    revised = copy.deepcopy(geometry.SETTINGS)
    revised["minimum_cross_entropy_separation_nats"] = .2
    monkeypatch.setattr(geometry, "SETTINGS", revised)
    after = study.geometry_amendment(rebuild=True)
    assert before != after
    assert (tmp_path / "geometry_amendment_v1.json").exists()
    assert study.settings() == training_settings
    assert study.identities() == training_sources


def test_cutoff_band_counts_and_complement():
    rendering = {"rendering": 0, "by_slot1_sum_twelfths": {
        str(s): {"boards": 2, "above_0_02_TV": 1, "maximum_TV": .1}
        for s in (10, 11, 12, 13, 14, 22, 23, 24, 25, 26)}}
    census = {"registered_rendering": rendering, "additional_fixed_renderings": []}
    measured = cutoff_summary(census)[0]
    assert measured["cutoff"]["boards"] == 12
    assert measured["complement"]["boards"] == 8
    assert measured["cutoff"]["prediction_TV_errors"] == 6


def test_erosion_observations_persist_and_resume(tmp_path, monkeypatch):
    from scripts.oldgame_mechanism_report import recorded_registration
    # The completed instrument is archived; only its aggregate entry changed.
    # Verify the unchanged training body, then exercise it in temporary outputs.
    monkeypatch.setattr(study, "registration", recorded_registration)
    run = Run("erosion", "blocked", 0)
    first = study.erosion(run, torch.device("cpu"), tmp_path / "repo",
                          tmp_path / "bulk", steps=1)
    second = study.erosion(run, torch.device("cpu"), tmp_path / "repo",
                           tmp_path / "bulk", steps=2)
    assert first["step"] == 1 and second["resumed_from"] == 1
    assert second["final_correct"] == 1555
    for step in (1, 2):
        assert (tmp_path / "bulk" / run.name / f"erosion_update_{step:06d}.json").exists()
