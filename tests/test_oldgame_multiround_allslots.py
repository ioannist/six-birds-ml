"""Finite-law, route, stream, and intervention checks for r10."""

from __future__ import annotations

import inspect
from pathlib import Path

import numpy as np
import pytest
import torch

from recombination_promotion.oldgame_ext.multiround import enumerate_boards
from recombination_promotion.oldgame_ext.multiround_allslots import (
    AllSlotsNetwork, CoverageSampler, ROW, check_law, eligible_pairs, law_row,
    sample_episodes, update,
)
from scripts import oldgame_multiround_allslots as study
from scripts import oldgame_allslots_execution as execution
from scripts import oldgame_allslots_report as reporting

torch.set_num_threads(1)


def test_exact_recursion_law_and_coverage() -> None:
    assert check_law() == {"rows": 36, "minimum_pairwise_TV": "7/100"}
    assert len(set(ROW)) == 36
    state = update(np.zeros(5, dtype=np.int64), (2, 0, 3, 0, 0))
    assert state.tolist() == [2, 0, 3, 0, 0]
    assert update(state, (0, 4, 0, 0, 0)).tolist() == [2, 4, 3, 0, 0]
    assert np.array_equal(law_row(state, 0), np.asarray(ROW[1], dtype=float))
    boards = enumerate_boards()
    sampler = CoverageSampler(boards)
    assert [len(x) for x in sampler.by_q] == [8115, 8140, 8180]
    assert [len(x) for x in sampler.pairs] == [150, 150, 150]
    assert all(len(eligible_pairs(boards, np.arange(len(boards.boards)))[k]) > 1000
               for k in range(5))


def test_paired_initialization_stream_and_no_hidden_inputs() -> None:
    names = tuple(inspect.signature(AllSlotsNetwork.forward).parameters)
    assert names == ("self", "records", "queries", "lengths", "return_trace")
    models = [study._new_model(arm, 0) for arm in study.ARMS]
    for key in ("raw_embedding.weight", "upper.weight_ih", "category_head.weight"):
        assert all(torch.equal(models[0].state_dict()[key], model.state_dict()[key])
                   for model in models[1:])
    boards = enumerate_boards()
    sampler = CoverageSampler(boards)
    streams = [study.EpisodeStream(0, False) for _ in study.ARMS]
    first = [stream.draw(sampler, 3, 8, False) for stream in streams]
    assert all(np.array_equal(first[0].boards, value.boards) and
               np.array_equal(first[0].queries, value.queries) and
               np.array_equal(first[0].rendering_seeds, value.rendering_seeds)
               for value in first[1:])
    held = streams[0].state()
    second = streams[0].draw(sampler, 3, 8, False)
    streams[1].restore(held)
    replay = streams[1].draw(sampler, 3, 8, False)
    assert np.array_equal(second.boards, replay.boards)


def test_loss_scopes_and_forced_raw_inactivity() -> None:
    boards = enumerate_boards()
    panel = sample_episodes(CoverageSampler(boards), 2, 2, 19)
    records = torch.from_numpy(study.records_for(panel, boards)).long()
    free, free_a, forced = (study._new_model(arm, 0) for arm in study.ARMS)
    for model in (free, free_a, forced):
        model.zero_grad(set_to_none=True)
        loss, parts = study.train_loss(model, records, panel, boards)
        loss.backward()
        assert not any(parameter.grad is not None for parameter in model.memory.parameters())
        if model.arm == "free_a":
            assert parts["A"] > 0
            assert model.raw_sum_head.weight.grad is not None
        else:
            assert parts["A"] == 0
            assert model.raw_sum_head.weight.grad is None
    with torch.no_grad():
        _, answers, raw = forced.round_interfaces(records[:, 0])
        query = torch.tensor([0, 1])
        first = forced.upper_step(answers, raw, query)[0]
        changed = forced.upper_step(answers, raw + 10, query)[0]
        assert torch.equal(first, changed)


def test_probe_labels_are_external_and_board_split_is_disjoint() -> None:
    boards = enumerate_boards()
    split = study._board_split(boards)
    probe = study._probe_split(boards, split)
    assert not set(probe["train_board_ids"]) & set(probe["heldout_board_ids"])
    assert set(probe["train_board_ids"]) <= set(split["train_board_ids"])
    assert set(probe["heldout_board_ids"]) <= set(split["heldout_board_ids"])
    model = study._new_model("free", 0)
    before = {key: value.clone() for key, value in model.state_dict().items()}
    x = np.arange(96, dtype=float).reshape(6, 16)
    labels = np.tile(np.arange(5), (6, 1))
    fitted = study.fit_alignment(x, labels)
    assert fitted["train_rows"] == 6
    assert all(torch.equal(value, model.state_dict()[key]) for key, value in before.items())
    assert "last_nonzero" not in inspect.signature(AllSlotsNetwork.forward).parameters
    assert "targets" not in inspect.signature(AllSlotsNetwork.forward).parameters


def test_patch_changes_only_selected_block() -> None:
    base = np.arange(16, dtype=float)
    donor = base + 100
    for slot in range(5):
        patched = study.patch_block(base, donor, slot)
        assert np.array_equal(patched[3 * slot:3 * slot + 3],
                              donor[3 * slot:3 * slot + 3])
        assert np.array_equal(np.delete(patched, slice(3 * slot, 3 * slot + 3)),
                              np.delete(base, slice(3 * slot, 3 * slot + 3)))


def test_executed_oracle_reads_records_not_scoring_memory():
    from recombination_promotion.oldgame_ext.multiround_allslots import ExecutedOracle, oracle_rows
    boards = enumerate_boards()
    panel = sample_episodes(CoverageSampler(boards), 8, 12, 75)
    records = torch.as_tensor(study.records_for(panel, boards)).long()
    logits, _ = ExecutedOracle()(records, torch.as_tensor(panel.queries), torch.as_tensor(panel.lengths))
    assert np.allclose(logits.softmax(-1).numpy(), oracle_rows(panel), atol=1e-7)
    panel.last_nonzero[:] = 0
    assert not np.allclose(logits.softmax(-1).numpy(), oracle_rows(panel))


def test_rare_renderings_and_recurrent_queries():
    from recombination_promotion.oldgame_ext.multiround_allslots import VALUES36
    boards = enumerate_boards()
    split = study._board_split(boards)
    probe = study._probe_split(boards, split)
    rare = np.asarray(boards.boards)[probe["rare_board_ids"]]
    for slot in range(5):
        for value in VALUES36:
            if value >= 28:
                assert (rare[:,slot] == value).sum() >= 20
    records = study._probe_data(probe, boards)[0][0]
    context, queries = study._probe_context(records[:4], split, boards, 18)
    assert context.shape == (4, 12, 4, 2)
    assert np.array_equal(context[:,-1], records[:4])
    assert len(set(queries.flatten())) > 1


def test_persisted_readers_training_only_standardization():
    x = np.arange(60,dtype=float).reshape(20,3)
    y = np.repeat([0,1],10)
    held = x[::-1].copy()+100
    for family in ("linear","mlp64"):
        fitted = study.fit_probe(x,y,held,y,family,2,1,smoke=True)
        assert np.array_equal(study.apply_probe(fitted["fitted"],held),fitted["predictions"])
        assert np.allclose(fitted["fitted"]["mean"],x.mean(0))


def test_interchange_support_and_equal_law_decisions():
    row = {"accurate_unpatched_pairs": 24, "donor_follow_rate_among_accurate":1.,
           "other_slot_probe_changes":0, "maximum_unwanted_prediction_change_TV":0.,
           "donor_follow_CI95":[.8,1.]}
    null = {**row,"donor_follow_rate_among_accurate":0.}
    prelaunch = {"passes":True}
    assert study.intervention_gate(row,row,prelaunch,null,positive_step=20000)["passes"]
    empty = {**null,"accurate_unpatched_pairs":0}
    assert study.intervention_gate(row,row,prelaunch,empty,positive_step=20000)["status"] == "UNCALIBRATED"
    assert not study.intervention_gate(row,row,prelaunch,null,positive_step=1000)["passes"]
    assert not study.intervention_gate(row,row,{"passes":False},null,positive_step=20000)["passes"]
    assert not study.intervention_gate(row,{**row,"accurate_unpatched_pairs":19},prelaunch,null,
                                       positive_step=20000)["passes"]
    assert not study.intervention_gate(row,{**row,"donor_follow_rate_among_accurate":.94},prelaunch,null,
                                       positive_step=20000)["passes"]
    assert study.intervention_gate(row,None,None,None,equal=True)["passes"]
    assert study.intervention_gate({**row,"maximum_unwanted_prediction_change_TV":.03},None,None,None,
                                   equal=True)["control_failure"]


def test_same_checkpoint_claim_not_historical_crossing():
    assert study.endpoint_claim(False,True,True) == "B_INCOMPLETE"
    assert study.endpoint_claim(True,True,True) == "A_MEDIATED_UNDER_REGISTERED_ALIGNMENT"


def test_independent_other_slot_reader_detects_contamination():
    boards = enumerate_boards()
    clean = study.interchange(None,boards,smoke=True,oracle=True)
    dirty = study.interchange(None,boards,smoke=True,oracle=True,contaminate=True)
    assert len(clean["independent_other_slot_decoders"]) == 5
    assert all(row["other_slot_probe_changes"] == 0 for row in clean["slots"].values())
    assert all(row["other_slot_probe_changes"] > 0 for row in dirty["slots"].values())
    assert all(len(row["per_pair"]) == row["evaluated_pairs"] for row in clean["slots"].values())
    assert all(clean["slots"][k]["pair_ids"] == dirty["slots"][k]["pair_ids"]
               for k in clean["slots"])
    assert all(row["oracle_semantic_integrity"]["donor_slot_errors"] == 0 and
               row["oracle_semantic_integrity"]["other_slot_errors"] == 0 and
               row["oracle_semantic_integrity"]["minimum_decision_margin"] > 0
               for row in clean["slots"].values())


def test_fixed_pairs_are_prediction_independent_and_shared():
    boards = enumerate_boards()
    split = study._board_split(boards)
    selected = study.select_pair_ids(boards,split)
    assert selected == study.select_pair_ids(boards,split)
    assert selected["prediction_independent"]
    for slot,row in selected["slots"].items():
        assert len(row["pairs"]) == min(1024,row["eligible_count"])
        assert len(set(map(tuple,row["pairs"]))) == len(row["pairs"])
        for a,b in row["pairs"]:
            assert boards.boards[a][int(slot)] != boards.boards[b][int(slot)]
            assert all(boards.boards[a][k] == boards.boards[b][k] for k in range(5) if k != int(slot))


def test_coordinate_decoder_training_only_and_oracle_noop_supported():
    rng = np.random.default_rng(10)
    labels = rng.integers(0,36,(2048,5))
    rotation,_ = np.linalg.qr(rng.normal(size=(16,16)))
    states = study.oracle_features(labels) @ rotation
    decoder = study.fit_coordinate_decoder(states,labels)
    assert decoder["rank"] == 16
    assert decoder["training_maximum_absolute_error"] < 1e-12
    assert np.array_equal(study.decode_coordinates(states,decoder),labels)
    held = rng.integers(0,36,(512,5))
    assert np.array_equal(study.decode_coordinates(study.oracle_features(held) @ rotation,decoder),held)
    noop = study.interchange(None,enumerate_boards(),oracle=True,noop=True)
    assert all(r["accurate_unpatched_pairs"] >= 20 and r["donor_follow_count"] == 0 and
               r["other_slot_probe_changes"] == 0 for r in noop["slots"].values())


def test_prelaunch_gates_do_not_use_unsupported_untrained_and_preserve_selectivity():
    positive = {"accurate_unpatched_pairs":1024,"donor_follow_rate_among_accurate":1.,
                "donor_follow_CI95":[.99,1.],"other_slot_probe_changes":0,
                "oracle_semantic_integrity":{"donor_slot_errors":0,"other_slot_errors":0}}
    null = {**positive,"donor_follow_rate_among_accurate":0.}
    assert study.prelaunch_use_gate(positive,positive,null,null)["passes"]
    assert not study.prelaunch_use_gate({**positive,"other_slot_probe_changes":1},positive,null,null)["passes"]
    assert not study.prelaunch_use_gate(positive,positive,null,{**null,"donor_follow_rate_among_accurate":.21})["passes"]
    assert study.intervention_settings()["untrained_conditional_status"] == "UNSUPPORTED_DESCRIPTIVE_ONLY"


def _reported_pair(*, rate=.99, support=875, changes=0):
    return {"accurate_unpatched_pairs":support,"donor_follow_rate_among_accurate":rate,
            "donor_follow_CI95":[.98,1.],"other_slot_probe_changes":changes,
            "evaluated_pairs":1024,"maximum_unwanted_prediction_change_TV":0.}


def test_report_separates_positive_negative_selectivity_and_use():
    positive = _reported_pair()
    forced = reporting.patch_components(study,positive,positive,{"passes":True},positive,
        arm="a_forced",law="original",positive_step=20000)
    assert forced["trained_positive"]["valid"]
    assert forced["negative_calibration"]["status"] == "NOT_APPLICABLE"
    assert forced["use_test"]["passes"] is None
    result = reporting.patch_components(study,_reported_pair(changes=200),positive,{"passes":True},
        _reported_pair(rate=.10),arm="free",law="original",positive_step=20000)
    assert result["trained_positive"]["valid"] and result["negative_calibration"]["valid"]
    assert not result["selectivity"]["passes"] and not result["use_test"]["passes"]
    missing = reporting.patch_components(study,_reported_pair(),_reported_pair(support=19),
        {"passes":True},_reported_pair(rate=.10),arm="free",law="original",positive_step=20000)
    assert not missing["trained_positive"]["valid"] and missing["negative_calibration"]["valid"]


def test_equal_report_labels_are_control_only_even_when_other_arms_pass():
    row = {"law":"equal","arm":"free","seed":1,"smoke":False,"futility_stop":False,
           "last_step":20000,"endpoint_B_pass":False,"five_sum_readability":True,
           "patches":{"0":{"passes":True}}}
    assert reporting.endpoint_label(study,row,{"a_forced_equal_seed1":{"endpoint_B_pass":True}}) == "EQUAL_LAW_CONTROL_INCOMPLETE"
    row["endpoint_B_pass"] = True
    assert reporting.endpoint_label(study,row,{}) == "EQUAL_LAW_CONTROL_PASS"
    p = reporting.patch_components(study,_reported_pair(),None,{},None,
        arm="free",law="equal",positive_step=None)
    assert p["use_test"]["status"] == "NOT_APPLICABLE"
    assert p["trained_positive"]["valid"] is None


def _saved_report_row():
    cases = {name:{"maximum_TV":.1,"KL_bits":.002,"covered_value_KL_bits":.002,
                  "minimum_prediction_pair_TV":.07,"maximum_prediction_pair_TV":.08}
             for name in ("natural","law_rows","witness","eight_hold")}
    entry = {"slot":0,"before":.25,"endpoint":.9,"gain":.65,"paired_CI95":[.60,.70],
        "correct":18,"total":20,"majority_floor":.1,"positive_accuracy":1.,
        "fits_converged":True,"readability_gain":True,"rare_readable":False,
        "shuffled_floor":{"accuracy":.1},"per_value":{str(k):{"correct":1,"total":1} for k in range(36)},
        "rare_rendering":{"per_value":{str(k):{"correct":1,"total":20} for k in range(36)}}}
    row = {"arm":"free","law":"original","seed":0,"smoke":False,"futility_stop":False,
        "last_step":20000,"same_checkpoint_label":"B_INCOMPLETE","endpoint_B_pass":False,
        "first_audited_B_crossing":None,"law_cases":cases,
        "endpoint_B_bars":{"natural_KL":True,"covered_value_KL":True,"constructed_law_TV":False,
                           "same_board_witness":False,"bounds":{"natural_KL":.008,"covered_value_KL":.008}},
        "endpoint_probe_gains":{"raw":{"linear":{"sum":[entry]}}},
        "endpoint_interchange":{"slots":{}},"endpoint_shuffled_interchange":{},"patches":{}}
    row["failed_B_bars"] = reporting.failed_b_bars(row)
    return row


def test_report_failed_b_values_distinguish_witness_separation_from_row_error():
    failures = reporting.failed_b_bars(_saved_report_row())
    assert failures["same_board_witness"]["minimum_prediction_pair_TV"]["passes"]
    assert not failures["same_board_witness"]["exact_row_maximum_TV"]["passes"]
    row = _saved_report_row()
    row["law"] = "equal"
    row["law_cases"]["law_rows"]["maximum_TV"] = .042784
    values = reporting.failed_b_bars(row)["constructed_law_TV"]
    assert values["bound"] == .02 and values["cases"]["law_rows"]["value"] == .042784


def test_compact_report_preserves_details_hashes_and_small_repository(tmp_path,monkeypatch):
    import json
    output,bulk = tmp_path/"repo",tmp_path/"bulk"
    output.mkdir()
    old = b"original detailed aggregate"*100000
    (output/"aggregate.json").write_bytes(old)
    calibration = b"original large calibration"*50000
    (output/"calibration.json").write_bytes(calibration)
    detailed = {"rows":{"free_original_seed0":_saved_report_row()},"conclusion":reporting.CONCLUSION,
        "registered_readings_verbatim":"REGISTERED READINGS UNCHANGED","scope_verbatim":"SCOPE UNCHANGED"}
    result = reporting.publish_reports(study,detailed,output,bulk,bulk)
    assert result["storage_status"] == "REQUESTED_BULK_ROOT"
    assert reporting.digest(result["detailed_artifact"]["path"]) == result["detailed_artifact"]["sha256"]
    assert (output/"calibration.json").is_symlink() and (output/"calibration.json").read_bytes() == calibration
    assert not (output/"aggregate.json").is_symlink()
    assert (output/"aggregate.json").stat().st_size < 100000
    saved = json.loads((output/"aggregate.json").read_text())
    assert saved["registered_readings_verbatim"] == "REGISTERED READINGS UNCHANGED"
    assert "per_pair" not in (output/"aggregate.json").read_text()
    text = (output/"aggregate.md").read_text()
    assert "Failed B bars" in text and "All-slot sum probes" in text and "Gain CI95" in text
    assert any(Path(r["path"]).read_bytes() == old for r in result["relocated_artifacts"])
    second_bulk = tmp_path/"requested_bulk"
    second = reporting.publish_reports(study,detailed,output,second_bulk,second_bulk)
    assert all(Path(r["path"]).is_relative_to(second_bulk) for r in second["relocated_artifacts"])
    assert (output/"calibration.json").resolve().is_relative_to(second_bulk)


def test_saved_futility_does_not_resume_updates(tmp_path,monkeypatch):
    runs = [execution.Run("free","original",0)]
    device = torch.device("cpu")
    monkeypatch.setattr(study,"registration",lambda: {})
    # Smoke is diagnostic and may run despite a rejected calibration; production may not.
    authority = {"registration_sha256":study.sha(study.OUTPUT/"registration.json"),
                 "calibration_sha256":study.sha(study.OUTPUT/"registration_build_v1.json"),
                 "runs":[runs[0].name],"device":"cpu","precision":"float32","smoke":True}
    # The run loader reads the current calibration hash; isolate that binding here.
    original_sha = study.sha
    monkeypatch.setattr(study,"sha",lambda p: authority["calibration_sha256"]
        if p.name == "calibration.json" else original_sha(p))
    engine = execution.Engine(study,runs,device)
    streams = execution.make_streams(study,runs,device)
    group_id = __import__("hashlib").sha256(runs[0].name.encode()).hexdigest()[:16]
    bulk = tmp_path/"bulk"
    group = bulk/("group_"+group_id)
    execution.publish(group/"checkpoint_step_005000.pt",{
        "authority":authority,"step":5000,"engine":engine.state(),
        "streams":[s.state() for s in streams],"stopped":[False],"windows":[[]],
        "curves":[[{"step":5000,"path":"unused","sha256":"unused",
                    "record":{"futility":{"stop":True}}}]]})
    monkeypatch.setattr(execution.Engine,"update",lambda *args: pytest.fail("futile run updated"))
    result = execution.run_chunk(study,runs,device,tmp_path/"reports",bulk,steps=6000,smoke=True)
    assert result[0]["last_step"] == 5000 and result[0]["futility_stop"]
    assert result[0]["updates_per_second"] == 0


@pytest.mark.parametrize("interruption",["payload", "digest"])
def test_checkpoint_publication_recovers_at_both_boundaries(tmp_path,monkeypatch,interruption):
    path = tmp_path/"checkpoint_step_000003.pt"
    original = Path.rename
    def interrupted(source,target):
        if (source.suffix == ".pending" and interruption == "payload") or (
                source.name.endswith(".pending.sha256") and interruption == "digest"):
            raise RuntimeError("simulated interruption")
        return original(source,target)
    monkeypatch.setattr(Path,"rename",interrupted)
    with pytest.raises(RuntimeError,match="simulated interruption"):
        execution.publish(path,{"step":3,"value":torch.arange(4)})
    monkeypatch.setattr(Path,"rename",original)
    execution.recover(tmp_path)
    saved = execution.bound_load(path)
    assert saved["step"] == 3 and torch.equal(saved["value"],torch.arange(4))
    with pytest.raises(ValueError,match="nonempty"):
        execution.publish(path,{"step":3})


def test_futility_persists_and_uses_only_B():
    first = {"loss_parts":{"A":10.,"B":2.},"oracle_B_loss_floor_nats":1.,
             "audit":{"B":{"natural":{"KL_bits":1.}}}}
    current = {"loss_parts":{"A":0.,"B":2.},"audit":{"B":{"natural":{"KL_bits":1.}}}}
    assert execution.futility(first,current)["stop"]
    current["loss_parts"] = {"A":10.,"B":1.5}
    assert not execution.futility(first,current)["stop"]
    assert execution.stopped_on_restore({"stopped":[False],"curves":[[{"record":{"futility":{"stop":True}}}]]}) == [True]


def test_device_stream_pairing_counts_and_restore():
    runs = [execution.Run(arm,"original",0) for arm in study.ARMS]
    streams = execution.make_streams(study,runs,torch.device("cpu"))
    batches = [s.draw(6,3) for s in streams]
    for batch in batches[1:]:
        assert all(torch.equal(getattr(batch,k),getattr(batches[0],k)) for k in vars(batch))
    assert streams[0].current.sum() == 6*3*5
    assert streams[0].current_by_Q.sum() == 6*3*5
    assert streams[0].current_queried.sum() == streams[0].remembered_queried.sum() == 18
    assert streams[0].rendering_counts.sum() == 18
    saved = streams[0].state()
    second = streams[0].draw(6,3)
    streams[1].restore(saved)
    replay = streams[1].draw(6,3)
    assert torch.equal(second.records,replay.records)
    assert streams[0].rolling == streams[1].rolling


def test_batch_direct_AdamW_and_nonzero_resume(monkeypatch):
    monkeypatch.setattr(study,"registration",lambda: {})
    result = execution.verification(study,torch.device("cpu"),trace=True)
    assert result["pass"] and all(row["pass"] for row in result["comparisons"].values())
    assert result["comparisons"]["a_forced"]["width"] == 1
    assert result["comparisons"]["free"]["width"] == 3
    assert result["comparisons"]["free"]["restore_step"] == 3


def test_failed_calibration_blocks_production(tmp_path,monkeypatch):
    import json
    monkeypatch.setattr(study,"registration",lambda: {})
    monkeypatch.setattr(study,"OUTPUT",tmp_path)
    study.write_json(tmp_path/"calibration.json",{"checks":{"positive":False}})
    assert json.loads((tmp_path/"calibration.json").read_text())["checks"]["positive"] is False
    with pytest.raises(ValueError,match="calibration failed"):
        execution.run_chunk(study,[execution.Run("free","original",0)],torch.device("cpu"),
                            tmp_path,tmp_path/"bulk")
