"""Executed controls for the paired B-only route-access study."""

from __future__ import annotations

import json

import numpy as np
import torch

from scripts import oldgame_multiround_route_access as r8
from scripts import multiround_streams as online


def _records():
    return torch.tensor([[[0, 0], [1, 1], [2, 2], [3, 3]],
                         [[4, 5], [0, 3], [1, 2], [2, 1]]], dtype=torch.long)


def test_paired_initialization_and_streams():
    models = [r8.RouteNetwork(route, 0) for route in r8.ROUTES]
    for left, right in zip(models, models[1:]):
        assert all(torch.equal(a, b) for a, b in zip(left.state_dict().values(),
                                                       right.state_dict().values(), strict=True))
    boards = r8.enumerate_boards()
    streams = [online.OnlineStream(boards, 0) for _ in r8.ROUTES]
    first = [stream.draw() for stream in streams]
    assert len({row[0] for row in first}) == 1
    assert len({stream.rolling for stream in streams}) == 1


def test_masks_are_exact_and_inactive_route_has_zero_effect():
    records = _records()
    changed = _records().flip(0)
    for route, inactive in (("a_only", "raw"), ("raw_only", "A")):
        model = r8.RouteNetwork(route, 0).eval()
        _, a, raw = model.round_interfaces(records)
        _, other_a, other_raw = model.round_interfaces(changed)
        reference, _ = model.upper_step(a, raw)
        altered, _ = model.upper_step(other_a if inactive == "A" else a,
                                      other_raw if inactive == "raw" else raw)
        assert torch.equal(reference, altered)
        if route == "a_only":
            assert torch.equal(reference, model.upper_step(a, torch.zeros_like(raw))[0])
        else:
            assert torch.equal(reference, model.upper_step(torch.zeros_like(a), raw)[0])


def test_B_only_loss_has_no_A_gradient_or_probe_labels():
    model = r8.RouteNetwork("dual", 0)
    episode = _records()[None, :1]
    target = torch.zeros((1, 1), dtype=torch.long)
    loss = r8.b_only_loss(model, episode, torch.ones(1, dtype=torch.long), target)
    loss.backward()
    assert all(parameter.grad is None for parameter in model.memory.parameters())
    assert any(parameter.grad is not None for parameter in model.raw_encoder.parameters())
    assert "probe" not in r8.b_only_loss.__code__.co_varnames


def test_probe_split_is_by_board_identity_and_has_all_sum_values():
    split = r8.probe_split()
    assert len(split["train_board_ids"]) == 2048
    assert len(split["heldout_board_ids"]) == 512
    assert not set(split["train_board_ids"]) & set(split["heldout_board_ids"])
    train, heldout = r8._probe_data(split)
    assert all(len(np.unique(train[1][:, slot])) == 36 for slot in range(5))
    assert len(heldout[0]) == 512


def test_linear_probe_uses_training_statistics_and_records_convergence():
    rng = np.random.default_rng(11)
    labels = np.repeat(np.arange(3), 30)
    train = rng.normal(labels[:, None] * 4, .2, size=(len(labels), 2))
    heldout = np.asarray([[.1, -.1], [4., 4.], [8., 8.]])
    first = r8._fit_probe(train, labels, heldout, np.arange(3), family="linear", seed=0)
    with_extra = r8._fit_probe(train, labels, np.vstack((heldout, [[10000., -10000.]])),
                               np.asarray([0, 1, 2, 0]), family="linear", seed=0)
    assert first["predictions"] == with_extra["predictions"][:3]
    assert first["converged"]
    assert first["convergence_warnings"] == []
    assert first["n_iter"] and all(0 < value < 5000 for value in first["n_iter"])


def test_nonconverged_linear_fit_cannot_support_readability_gain():
    truth = np.zeros((40, 1), dtype=np.int64)

    def probe(prediction, converged):
        return {"accuracy": float(prediction == 0),
                "predictions": [prediction] * 40, "converged": converged}

    baseline = {"sites": {"raw": {"linear": [probe(1, True)]}}}
    oracle = {"sites": {"raw": {"linear": [probe(0, True)]}}}
    failed = {"sites": {"raw": {"linear": [probe(0, False)]}}}
    accepted = {"sites": {"raw": {"linear": [probe(0, True)]}}}
    rejected_gain = r8._probe_gain(failed, baseline, oracle, truth)["raw"]["linear"][0]
    accepted_gain = r8._probe_gain(accepted, baseline, oracle, truth)["raw"]["linear"][0]
    assert rejected_gain["gain"] == 1 and not rejected_gain["training_related_gain"]
    assert not rejected_gain["fits_converged"]
    assert accepted_gain["training_related_gain"] and accepted_gain["fits_converged"]


def test_registered_probe_settings_are_validated(tmp_path, monkeypatch):
    active = r8.registration()
    wrong = dict(active)
    wrong["linear_probe_settings"] = dict(active["linear_probe_settings"])
    wrong["linear_probe_settings"]["max_iter"] = 500
    (tmp_path / "registration.json").write_text(json.dumps(wrong))
    monkeypatch.setattr(r8, "OUTPUT", tmp_path)
    try:
        r8.registration()
    except ValueError as error:
        assert "registration authority differs" in str(error)
    else:
        raise AssertionError("changed probe settings were accepted")


def test_futility_requires_both_gaps_below_tenth():
    curve = [{"train_loss_nats": 2., "audit": {"natural_excess_KL_bits": .5}}]
    current = {"train_loss_nats": 1.99, "audit": {"natural_excess_KL_bits": .49}}
    assert r8._futile(curve, current, "original")
    assert not r8._futile(curve, {"train_loss_nats": 1.5,
                                  "audit": {"natural_excess_KL_bits": .49}}, "original")


def test_current_board_null_uses_round_index_without_past_categories():
    model = r8.ExactRowModel("raw_only", "original", current_only=True)
    answers = torch.zeros((1, 5, 36))
    raw = torch.zeros((1, 16))
    raw[:, 0] = 1  # neutral board
    first, state = model.upper_step(answers, raw)
    second, state = model.upper_step(answers, raw, state)
    assert torch.allclose(first.exp(), torch.tensor([[.5, .25, .25]]))
    assert torch.allclose(second.exp(), torch.tensor([[.4375, .25, .3125]]))
    assert state[0, 1] == 2


def test_checkpoint_restores_paired_stream_and_model(tmp_path):
    from scripts import multiround_panels as choice

    boards = r8.enumerate_boards()
    panel = choice.load_episodes(choice.OUTPUT / "test.npz")
    model = r8.RouteNetwork("a_only", 0)
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=.003)
    stream = online.OnlineStream(boards, 0)
    candidates = online.UnseenCandidates(panel)
    _, batch = stream.draw()
    candidates.observe(batch)
    path = tmp_path / "checkpoint_step_000001.pt"
    r8._save_checkpoint(path, model, optimizer, stream, candidates, 1,
                        "a_only", "original", 0, [{"step": 1}])
    restored = r8.RouteNetwork("a_only", 0)
    restored_optimizer = torch.optim.AdamW((p for p in restored.parameters()
                                             if p.requires_grad), lr=.003)
    restored_stream = online.OnlineStream(boards, 0)
    restored_candidates = online.UnseenCandidates(panel)
    step, curve = r8._restore(tmp_path, restored, restored_optimizer,
                              restored_stream, restored_candidates, "a_only", "original", 0)
    assert (step, curve) == (1, [{"step": 1}])
    assert stream.state() == restored_stream.state()
    assert np.array_equal(candidates.seen, restored_candidates.seen)
    assert stream.draw()[0] == restored_stream.draw()[0]


def test_interrupted_and_resumed_update_matches_uninterrupted(tmp_path):
    from scripts import multiround_panels as choice

    boards = r8.enumerate_boards()
    panel = choice.load_episodes(choice.OUTPUT / "test.npz")
    model = r8.RouteNetwork("raw_only", 0)
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),
                                  lr=.003, weight_decay=.01)
    stream = online.OnlineStream(boards, 0)
    candidates = online.UnseenCandidates(panel)

    def update(current_model, current_optimizer, current_stream, current_candidates):
        _, batch = current_stream.draw()
        current_candidates.observe(batch)
        records = torch.from_numpy(choice.episode_records(batch, boards))
        lengths = torch.from_numpy(batch.lengths.astype(np.int64))
        targets = torch.from_numpy(batch.targets.astype(np.int64))
        current_optimizer.zero_grad(set_to_none=True)
        r8.b_only_loss(current_model, records, lengths, targets).backward()
        current_optimizer.step()

    update(model, optimizer, stream, candidates)
    r8._save_checkpoint(tmp_path / "checkpoint_step_000001.pt", model, optimizer,
                        stream, candidates, 1, "raw_only", "original", 0, [])
    resumed = r8.RouteNetwork("raw_only", 0)
    resumed_optimizer = torch.optim.AdamW((p for p in resumed.parameters() if p.requires_grad),
                                          lr=.003, weight_decay=.01)
    resumed_stream = online.OnlineStream(boards, 0)
    resumed_candidates = online.UnseenCandidates(panel)
    r8._restore(tmp_path, resumed, resumed_optimizer, resumed_stream,
                resumed_candidates, "raw_only", "original", 0)
    update(model, optimizer, stream, candidates)
    update(resumed, resumed_optimizer, resumed_stream, resumed_candidates)
    assert stream.state() == resumed_stream.state()
    assert all(torch.equal(left, right) for left, right in zip(
        model.state_dict().values(), resumed.state_dict().values(), strict=True))


def test_aggregate_selected_reading_and_endpoint_probe_table():
    result = r8.aggregate()
    assert result["runs"] == 18
    report = json.loads((r8.OUTPUT / "aggregate.json").read_text())
    markdown = (r8.OUTPUT / "aggregate.md").read_text()
    assert report["registered_reading"] == r8.registration()["predeclared_reading"]
    assert report["registered_reading"] in markdown
    assert "raw-only is B-incomplete" in report["selected_applicable_reading"]
    assert report["selected_applicable_reading"] in markdown
    aligned = report["raw_only_endpoint_probes"]
    assert len(aligned) == 3 * 2 * 2 * 5
    assert {(row["seed"], row["carrier"], row["probe_family"], row["slot"])
            for row in aligned} == {(seed, site, family, slot)
                                    for seed in range(3) for site in ("raw", "upper")
                                    for family in ("linear", "mlp64")
                                    for slot in range(1, 6)}
    for row in aligned:
        for law in r8.LAWS:
            name = f"raw_only_{law}_seed{row['seed']}"
            first = json.loads((r8.OUTPUT / name / "audit_step_000000.json").read_text())
            final = json.loads((r8.OUTPUT / name / "audit_step_020000.json").read_text())
            site, family, slot = row["carrier"], row["probe_family"], row["slot"] - 1
            saved = row[law]
            assert saved["update0_accuracy"] == first["audit"]["probes"]["sites"][site][family][slot]["accuracy"]
            assert saved["endpoint_accuracy"] == final["audit"]["probes"]["sites"][site][family][slot]["accuracy"]
            assert saved["majority_floor"] == final["audit"]["probes"]["floors"][slot]["majority_accuracy"]
            endpoint_gain = next(item for item in report["rows"][name]["probe_table"]
                                 if item["step"] == 20000)["gain"][site][family][slot]
            assert saved["paired_gain_CI95"] == endpoint_gain["gain_CI95"]
            if family == "linear":
                assert saved["converged"] == endpoint_gain["fits_converged"]
                assert saved["fit_status"] in ("converged", "not converged")
            else:
                assert saved["converged"] is None
                assert saved["fit_status"] == "fixed budget; convergence not assessed"
            assert r8._probe_cell(saved) in markdown
    for failed in report["raw_only_failed_original_bars"]:
        assert not failed["law_TV"]["pass"] and not failed["swaps"]["pass"]
        assert failed["law_TV"]["maximum_TV"] > .02
        assert failed["swaps"]["failed_cases_maximum_TV"]
        assert f"{failed['law_TV']['maximum_TV']:.6f}" in markdown
        for value in failed["swaps"]["failed_cases_maximum_TV"].values():
            assert f"{value:.6f}" in markdown
