"""Read-only checks for the saved-network r9 diagnosis."""

from __future__ import annotations

import numpy as np

from scripts import oldgame_multiround_raw_diagnosis as diagnosis


def test_category_signature_uses_both_previous_modes() -> None:
    p0, p1 = diagnosis.TRUTH
    rows = np.asarray(((p0, p0), (p0, p1), (p1, p1)))
    assert diagnosis.signature(rows).tolist() == [0, 1, 2]
    assert diagnosis.tv(rows[1, 0], p0) == 0
    assert diagnosis.tv(rows[1, 1], p1) == 0


def test_saved_boundary_board_has_rendered_raw_misread() -> None:
    from scripts import multiround_panels as choice

    records = np.load(choice.OUTPUT / "prefix_records.npy")
    for seed in (0, 1, 2):
        raw, _ = diagnosis.load_model("raw_only", seed)
        a_only, _ = diagnosis.load_model("a_only", seed)
        for model, expected in ((raw, "H"), (a_only, "N")):
            board_records = diagnosis.board_records(diagnosis.enumerate_boards())
            _, _, low, high = diagnosis.board_effects(
                model, board_records, diagnosis.enumerate_boards())[2]
            assert diagnosis.rendered_effect(model, records[348, 1], low, high)[
                "signature"] == expected


def test_saved_prefix_replay_identifies_same_worst_row() -> None:
    import json

    result = json.loads((diagnosis.OUTPUT / "results.json").read_text())
    for seed in (0, 1, 2):
        row = result["runs"][f"raw_only_seed{seed}"]["failed_prefix_cases"]["L_N5"]
        assert row["worst_index"] == 348
        assert row["sequence"][1]["slot1_sum_twelfths"] == 23
        assert row["sequence"][1]["single_board_effect"]["signature"] == "H"
