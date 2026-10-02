"""Per-slot game in integer twelfths, exactly representing the inherited masses."""

from __future__ import annotations

from collections import defaultdict
from itertools import product

from recombination_promotion.serialization.minimal_recombination import (
    DEFAULT_MASS_VOCAB, MASS_VALUE,
)

MASS_TOKENS = tuple(DEFAULT_MASS_VOCAB)
MASSES = tuple(int(12 * MASS_VALUE[token]) for token in MASS_TOKENS)
if tuple(MASS_VALUE[token] for token in MASS_TOKENS) != tuple(
    MASS_VALUE[token] for token in DEFAULT_MASS_VOCAB
):
    raise AssertionError("mass vocabulary differs from the inherited game")
History = tuple[int, ...]
Record = tuple[int, int]  # slot, mass in twelfths
KIND_SUM, KIND_MAX, KIND_CTL = range(3)


def histories() -> tuple[History, ...]:
    return tuple(history for count in range(5)
                 for history in product(MASSES, repeat=count))


def sigma(history: History) -> int:
    return sum(history)


def tau(history: History) -> tuple[int, int]:
    return sigma(history), max(history, default=0)


def ctl(sum_twelfths: int) -> int:
    return max((mass for mass in MASSES if mass <= sum_twelfths), default=0)


def whole_endpoints() -> tuple[set[tuple[int, ...]], set[tuple[tuple[int, int], ...]]]:
    """Dynamic enumeration of all routed four-record endpoints, without sampling."""

    states = {((0, 0),) * 5}
    for _ in range(4):
        after = set()
        for cells in states:
            for slot in range(5):
                for mass in MASSES:
                    updated = list(cells)
                    old_sum, old_max = updated[slot]
                    updated[slot] = (old_sum + mass, max(old_max, mass))
                    after.add(tuple(updated))
        states = after
    return {tuple(value[0] for value in cells) for cells in states}, states


def enumerate_facts() -> dict[str, object]:
    all_histories = histories()
    sums = {sigma(history) for history in all_histories}
    pairs = {tau(history) for history in all_histories}
    by_sum: dict[int, set[int]] = defaultdict(set)
    for total, maximum in pairs:
        by_sum[total].add(maximum)
    stage_sum = sum(len({sigma(history) for history in all_histories if len(history) == k})
                    for k in range(5))
    stage_tau = sum(len({tau(history) for history in all_histories if len(history) == k})
                    for k in range(5))
    endpoint_sums, endpoint_pairs = whole_endpoints()
    first = (3, 3)
    second = (2, 4)
    middle_first = first + (2,)
    middle_second = second + (2,)
    padded_first = first + (2, 2)
    padded_second = second + (2, 2)
    witness = (sigma(first) == sigma(second) and tau(first) != tau(second)
               and sigma(middle_first) == sigma(middle_second)
               and tau(middle_first) != tau(middle_second)
               and sigma(padded_first) == sigma(padded_second)
               and tau(padded_first) != tau(padded_second))
    # The same other-slot records make a whole four-record endpoint witness.
    endpoint_witness = (
        ((tau(first), (4, 2), (0, 0), (0, 0), (0, 0))),
        ((tau(second), (4, 2), (0, 0), (0, 0), (0, 0))),
    )
    endpoint_witness_ok = (all(cells in endpoint_pairs for cells in endpoint_witness)
                           and tuple(cell[0] for cell in endpoint_witness[0])
                           == tuple(cell[0] for cell in endpoint_witness[1]))
    observed = {
        "histories": len(all_histories), "stationary_sum_classes": len(sums),
        "stationary_sum_max_classes": len(pairs),
        "split_sum_fibers": sum(len(values) > 1 for values in by_sum.values()),
        "largest_split_fiber": max(map(len, by_sum.values())),
        "stagewise_sum_classes": stage_sum, "stagewise_sum_max_classes": stage_tau,
        "whole_sum_vectors": len(endpoint_sums), "whole_sum_max_vectors": len(endpoint_pairs),
        "T4_T5b_witness": witness, "whole_endpoint_witness": endpoint_witness_ok,
    }
    expected = {
        "histories": 1555, "stationary_sum_classes": 36,
        "stationary_sum_max_classes": 92, "split_sum_fibers": 26,
        "largest_split_fiber": 5, "stagewise_sum_classes": 73,
        "stagewise_sum_max_classes": 134, "whole_sum_vectors": 24435,
        "whole_sum_max_vectors": 39045, "T4_T5b_witness": True,
        "whole_endpoint_witness": True,
    }
    if observed != expected:
        raise AssertionError(f"old-game exact enumeration differs: {observed}")
    return observed
