"""Read-only diagnosis of the saved r8 original-law route networks."""

from __future__ import annotations

import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from recombination_promotion.public_paths import identity_matches

import numpy as np
import torch

from recombination_promotion.oldgame_ext.multiround import P, enumerate_boards
from scripts import multiround_panels as choice
from scripts import oldgame_multiround_route_access as r8
from scripts import multiround_scoring as prior


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/phase11/oldgame_memory/multiround/study_r9_raw_diagnosis"
SOURCE = choice.OUTPUT
ROUTES = ("raw_only", "a_only", "dual")
TRUTH = np.asarray(P, dtype=float)
LIMIT = 0.02


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tv(rows: np.ndarray, truth: np.ndarray) -> np.ndarray:
    return np.abs(rows - truth).sum(axis=-1) / 2


def signature(predictions: np.ndarray) -> np.ndarray:
    """Classify a board's action after known mode-0 and mode-1 states.

    L maps both contexts to p0, N preserves each, and H maps both to p1.
    """

    templates = TRUTH[np.asarray(((0, 0), (0, 1), (1, 1)))]
    return np.argmin(np.abs(predictions[:, None] - templates[None]).sum((2, 3)), axis=1)


def load_model(route: str, seed: int) -> tuple[r8.RouteNetwork, dict]:
    path = r8.OUTPUT / f"{route}_original_seed{seed}/checkpoint_step_020000.pt"
    if path.with_suffix(".sha256").read_text().strip() != digest(path):
        raise ValueError("saved checkpoint digest differs")
    saved = torch.load(path, map_location="cpu", weights_only=False)
    if (saved["route"], saved["law"], saved["seed"], saved["step"]) != (
            route, "original", seed, 20_000):
        raise ValueError("saved checkpoint identity differs")
    if (not identity_matches(saved["registration_sha256"], digest(r8.OUTPUT / "registration.json"))
            or not identity_matches(saved["calibration_sha256"], digest(r8.OUTPUT / "calibration.json"))):
        raise ValueError("saved checkpoint authorities differ")
    model = r8.RouteNetwork(route, seed, verify_source=False)
    model.load_state_dict(saved["model"], strict=True)
    model.eval()
    return model, {"checkpoint": str(path.relative_to(ROOT)), "sha256": digest(path)}


@torch.no_grad()
def interfaces(model: r8.RouteNetwork, records: np.ndarray, batch: int = 512):
    answers, raw = [], []
    for start in range(0, len(records), batch):
        _, a, r = model.round_interfaces(torch.from_numpy(records[start:start + batch]).long())
        answers.append(a)
        raw.append(r)
    return torch.cat(answers), torch.cat(raw)


@torch.no_grad()
def step(model, a: torch.Tensor, r: torch.Tensor, state=None):
    logits, state = model.upper_step(a, r, state)
    return torch.softmax(logits, -1).numpy(), state


def board_records(boards) -> np.ndarray:
    ids = np.arange(len(boards.boards), dtype=np.int64)
    seeds = ids + np.int64(2026100901)
    return choice.record_projection(ids, seeds, boards)


@torch.no_grad()
def board_effects(model, records: np.ndarray, boards) -> tuple[dict, np.ndarray, tuple]:
    a, r = interfaces(model, records)
    sums = np.fromiter((board[0] for board in boards.boards), dtype=np.int64)
    low = int(np.flatnonzero(sums == 0)[0])
    high = int(np.flatnonzero(sums == 36)[0])
    low_row, low_state = step(model, a[low:low + 1], r[low:low + 1])
    high_row, high_state = step(model, a[high:high + 1], r[high:high + 1])
    rows = []
    for anchor in (low_state, high_state):
        predicted = []
        for start in range(0, len(records), 512):
            end = min(start + 512, len(records))
            row, _ = step(model, a[start:end], r[start:end],
                          anchor.expand(end - start, -1))
            predicted.append(row)
        rows.append(np.concatenate(predicted))
    pair = np.stack(rows, axis=1)
    classified = signature(pair)
    truth = np.where(sums <= 12, 0, np.where(sums >= 24, 2, 1))
    target = TRUTH[np.stack((np.where(truth == 2, 1, 0),
                             np.where(truth == 0, 0, 1)), axis=1)]
    errors = tv(pair, target)
    by_sum = {}
    for value in np.unique(sums):
        selected = sums == value
        by_sum[str(value)] = {
            "boards": int(selected.sum()), "category": int(truth[selected][0]),
            "distance_to_boundary": int(min(abs(value - 12), abs(value - 24))),
            "signature_misreads": int((classified[selected] != truth[selected]).sum()),
            "above_TV_limit": int((errors[selected].max(axis=1) > LIMIT).sum()),
            "maximum_TV": float(errors[selected].max()),
        }
    confusion = [[int(((truth == i) & (classified == j)).sum())
                  for j in range(3)] for i in range(3)]
    report = {"anchors": {"L_board_id": low, "H_board_id": high,
                           "L_single_TV": float(tv(low_row[0], TRUTH[0])),
                           "H_single_TV": float(tv(high_row[0], TRUTH[1]))},
              "confusion_L_N_H": confusion, "by_slot1_sum_twelfths": by_sum,
              "above_TV_limit": int((errors.max(axis=1) > LIMIT).sum()),
              "maximum_TV": float(errors.max())}
    return report, classified, (a, r, low_state, high_state)


@torch.no_grad()
def clear_neutral_runs(model, board_data, boards, seed: int) -> dict:
    a, r, low_state, high_state = board_data
    sums = np.fromiter((board[0] for board in boards.boards), dtype=np.int64)
    clear = np.flatnonzero((sums >= 16) & (sums <= 20))
    rng = np.random.default_rng(2026100902 + seed)
    chosen = rng.choice(clear, size=(32, 8), replace=True)
    result = {}
    for mode, anchor in ((0, low_state), (1, high_state)):
        state = anchor.expand(32, -1).clone()
        rows = []
        for at in range(8):
            ids = torch.from_numpy(chosen[:, at]).long()
            predicted, state = step(model, a[ids], r[ids], state)
            error = tv(predicted, TRUTH[mode])
            rows.append({"run_length": at + 1, "mean_TV": float(error.mean()),
                         "maximum_TV": float(error.max()),
                         "above_TV_limit": int((error > LIMIT).sum())})
        result[("L", "H")[mode]] = rows
    return {"panel": "32 fixed seeded sequences; every board has slot-1 sum 16–20",
            "board_ids": chosen.tolist(), "after_L_or_H": result}


@torch.no_grad()
def rendered_effect(model, record: np.ndarray, low_state, high_state) -> dict:
    a, r = interfaces(model, record[None])
    low, _ = step(model, a, r, low_state)
    high, _ = step(model, a, r, high_state)
    pair = np.stack((low[0], high[0]))
    return {"signature": ("L", "N", "H")[int(signature(pair[None])[0])],
            "output_after_L": pair[0].tolist(), "output_after_H": pair[1].tolist()}


def prefix_failures(model, metadata, records, lengths, saved, boards,
                    board_data, panel_counts: Counter,
                    natural_counts: Counter) -> tuple[dict, list[float]]:
    probabilities, _ = choice.predict_panel(model, records, lengths)
    actual = choice.prefix_score(probabilities, lengths, metadata, equal=False)
    for case, row in actual["rows"].items():
        expected = saved["mode_law"]["rows"][case]
        if abs(row["maximum_TV"] - expected["maximum_TV"]) > 1e-6:
            raise ValueError("saved prefix audit differs from checkpoint replay")
    result = {}
    for case, row in actual["rows"].items():
        if row["maximum_TV"] <= LIMIT:
            continue
        indices = [i for i, item in enumerate(metadata)
                   if f"{('L', 'H')[item['first'] == 2]}_N{item['neutral_run']}" == case]
        mode = 0 if case.startswith("L") else 1
        scores = tv(probabilities[indices, lengths[indices] - 1], TRUTH[mode])
        index = indices[int(scores.argmax())]
        board_ids = metadata[index]["board_indices"]
        sequence = []
        for at, board_id in enumerate(board_ids):
            effect = rendered_effect(model, records[index, at],
                                     board_data[2], board_data[3])
            sequence.append({"round": at + 1, "board_id": board_id,
                             "slot1_sum_twelfths": boards.boards[board_id][0],
                             "exact_category": ("L", "N", "H")[
                                 0 if at == 0 and mode == 0 else 2 if at == 0 else 1],
                             "single_board_effect": effect,
                             "TV_after_round": float(tv(probabilities[index, at], TRUTH[mode])),
                             "prefix_panel_occurrences": panel_counts[board_id],
                             "natural_test_occurrences": natural_counts[board_id]})
        first_exceeding = next((item for item in sequence
                                if item["TV_after_round"] > LIMIT), None)
        if first_exceeding is None:
            cause = "NO_THRESHOLD_EXCEEDANCE_IN_WORST_ROW"
        elif first_exceeding["single_board_effect"]["signature"] != (
                "L", "N", "H")[0 if first_exceeding["round"] == 1 and mode == 0
                                 else 2 if first_exceeding["round"] == 1 else 1]:
            cause = "DISCRETE_CATEGORY_MISREAD"
        elif first_exceeding["round"] == 1:
            cause = "SET_OR_RESET_PROBABILITY_ERROR"
        elif min(abs(first_exceeding["slot1_sum_twelfths"] - 12),
                 abs(first_exceeding["slot1_sum_twelfths"] - 24)) <= 3:
            cause = "NEAR_BOUNDARY_NEUTRAL_RESPONSE_WITHOUT_DISCRETE_MISREAD"
        else:
            cause = "STATE_DEPENDENT_NEUTRAL_RESPONSE"
        result[case] = {"worst_index": index, "maximum_TV": float(scores.max()),
                        "sequence": sequence, "first_exceeding_round": first_exceeding,
                        "evidence_class": cause}
    final_errors = [float(tv(probabilities[index, lengths[index] - 1],
                             TRUTH[0 if item["first"] == 0 else 1]))
                    for index, item in enumerate(metadata)]
    return result, final_errors


@torch.no_grad()
def swap_failures(model, board_ids, records, scenarios, saved, boards,
                  board_data, panel_counts: Counter,
                  natural_counts: Counter) -> tuple[dict, dict]:
    _, answers, raw = model.round_interfaces(torch.from_numpy(records).long())
    lookup = {int(board): i for i, board in enumerate(board_ids)}

    def run(board, prior=None):
        i = lookup[int(board)]
        return step(model, answers[i:i + 1], raw[i:i + 1], prior)

    cases = {name: [] for name in ("neutral_N", "same_category_substitution",
                                  "upper_state_exchange_same_N", "reset_L", "set_H")}
    for i, case in enumerate(scenarios):
        l, h, n, other = (case[key] for key in ("L", "H", "N", "N_other"))
        _, ls = run(l)
        _, hs = run(h)
        nl, nls = run(n, ls)
        nh, nhs = run(n, hs)
        for mode, anchor in ((0, ls), (1, hs), (0, nls), (1, nhs)):
            row, _ = run(n, anchor)
            alt, _ = run(other, anchor)
            cases["neutral_N"].append((float(tv(row[0], TRUTH[mode])), i, n, mode))
            cases["same_category_substitution"].append(
                (float(tv(row[0], alt[0])), i, other, mode))
        cases["upper_state_exchange_same_N"].extend((
            (float(tv(nh[0], TRUTH[1])), i, n, 1),
            (float(tv(nl[0], TRUTH[0])), i, n, 0)))
        for anchor in (None, ls, hs, nls, nhs):
            for name, board, target in (("reset_L", l, TRUTH[0]),
                                         ("set_H", h, TRUTH[1])):
                row, _ = run(board, anchor)
                cases[name].append((float(tv(row[0], target)), i, board, -1))
    report = {}
    for name, values in cases.items():
        found = max(values)
        if abs(found[0] - saved["swaps"]["cases"][name]["maximum_TV"]) > 1e-6:
            raise ValueError(f"saved {name} audit differs from checkpoint replay")
        if found[0] > LIMIT:
            _, scenario, board, mode = found
            context = scenarios[scenario]
            used = {name: {"board_id": int(context[name]),
                           "slot1_sum_twelfths": int(boards.boards[context[name]][0]),
                           "single_board_effect": rendered_effect(
                               model, records[lookup[context[name]]],
                               board_data[2], board_data[3]),
                           "prefix_panel_occurrences": panel_counts[context[name]],
                           "natural_test_occurrences": natural_counts[context[name]]}
                    for name in ("L", "H", "N", "N_other")}
            report[name] = {"maximum_TV": found[0], "scenario": scenario,
                            "board_id": int(board),
                            "slot1_sum_twelfths": int(boards.boards[board][0]),
                            "prior_mode": mode, "boards": used,
                            "evidence_class": {
                                "neutral_N": "CONTEXT_DEPENDENT_NEUTRAL_PROBABILITY_ERROR",
                                "same_category_substitution": "NONINVARIANT_NEUTRAL_SUBSTITUTION",
                                "upper_state_exchange_same_N": "CONTEXT_DEPENDENT_NEUTRAL_PROBABILITY_ERROR",
                                "reset_L": "RESET_PROBABILITY_ERROR",
                                "set_H": "SET_PROBABILITY_ERROR",
                            }[name]}
    by_scenario = {name: {str(index): max(row[0] for row in values if row[1] == index)
                          for index in range(len(scenarios))}
                   for name, values in cases.items()}
    return report, by_scenario


def main() -> None:
    torch.set_num_threads(1)
    if (OUTPUT / "results.json").exists():
        raise ValueError("r9 diagnosis result already exists")
    started = time.monotonic()
    boards = enumerate_boards()
    records = board_records(boards)
    meta = json.loads((SOURCE / "prefix_metadata.json").read_text())
    prefix_records = np.load(SOURCE / "prefix_records.npy")
    prefix_lengths = np.load(SOURCE / "prefix_lengths.npy")
    with np.load(SOURCE / "swap_records.npz") as data:
        swap_board_ids, swap_records = data["board_ids"], data["records"]
    scenarios = json.loads((SOURCE / "swap_scenarios.json").read_text())
    panel_counts = Counter(board for row in meta for board in row["board_indices"])
    source_panel = choice.load_episodes(SOURCE / "test.npz")
    natural_active = prior._active(source_panel)
    natural_counts = Counter(map(int, source_panel.boards[natural_active]))
    result = {"source": {"r8_registration_sha256": digest(r8.OUTPUT / "registration.json"),
                         "board_count": len(boards.boards), "prefix_rows": len(meta),
                         "swap_scenarios": len(scenarios),
                         "natural_test_active_rounds": int(natural_active.sum()),
                         "natural_test_unique_boards": len(natural_counts)},
              "sampling": {"per_active_round_N_probability": 0.25,
                           "specific_N_board_probability": 0.25 / 1835,
                           "specific_L_board_probability_by_mode": {
                               "mode_0": 0.5 / 22491, "mode_1": 0.25 / 22491},
                           "specific_H_board_probability_by_mode": {
                               "mode_0": 0.25 / 109, "mode_1": 0.5 / 109},
                           "N_run_3_to_8_training_occurrences": 0,
                           "note": "The online sampler stops before its third consecutive N; "
                                   "each sampled category is uniform over its boards."},
              "runs": {}}
    for seed in range(3):
        for route in ROUTES:
            model, source = load_model(route, seed)
            audit = json.loads((r8.OUTPUT / f"{route}_original_seed{seed}/"
                                "audit_step_020000.json").read_text())["audit"]
            census, _, board_data = board_effects(model, records, boards)
            key = f"{route}_seed{seed}"
            failed_prefix, prefix_final = prefix_failures(
                model, meta, prefix_records, prefix_lengths, audit, boards,
                board_data, panel_counts, natural_counts)
            failed_swap, swap_per_scenario = swap_failures(
                model, swap_board_ids, swap_records, scenarios, audit, boards,
                board_data, panel_counts, natural_counts)
            result["runs"][key] = {
                "source": source, "board_effects": census,
                "clear_neutral_runs": clear_neutral_runs(model, board_data, boards, seed),
                "failed_prefix_cases": failed_prefix, "prefix_final_TV": prefix_final,
                "failed_swap_cases": failed_swap,
                "swap_per_scenario_maximum_TV": swap_per_scenario,
                "saved_r8": {"natural_KL_bits": audit["natural_excess_KL_bits"],
                             "law_maximum_TV": audit["mode_law"]["maximum_TV"]}}
            print(key, "category confusion", census["confusion_L_N_H"],
                  "failed prefix", list(result["runs"][key]["failed_prefix_cases"]),
                  "elapsed", round(time.monotonic() - started, 1), flush=True)
    for seed in range(3):
        raw = result["runs"][f"raw_only_seed{seed}"]
        raw["comparison_on_raw_worst"] = {
            "prefix": {case: {route: result["runs"][f"{route}_seed{seed}"][
                "prefix_final_TV"][row["worst_index"]] for route in ROUTES}
                for case, row in raw["failed_prefix_cases"].items()},
            "swap": {case: {route: result["runs"][f"{route}_seed{seed}"][
                "swap_per_scenario_maximum_TV"][case][str(row["scenario"])]
                for route in ROUTES}
                for case, row in raw["failed_swap_cases"].items()},
        }
    result["elapsed_seconds"] = time.monotonic() - started
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("results", OUTPUT / "results.json", "seconds", round(result["elapsed_seconds"], 1))


if __name__ == "__main__":
    main()
