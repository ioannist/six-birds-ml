"""Analysis-only pair discrimination for r13; never a training authority."""

from __future__ import annotations

import math

import torch

from .jagged_probes import LINEAR_SETTINGS, fit_reader
from .memory import VALUES
from .multiround_mechanism import encode_answers
from .multiround import enumerate_boards


SETTINGS = {
    "reader": LINEAR_SETTINGS,
    "positive_accuracy_minimum": .99,
    "negative_accuracy_maximum_exclusive": .8,
    "minimum_cross_entropy_separation_nats": .1,
    "constant_negative_accuracy": .5,
    "constant_negative_cross_entropy_nats": math.log(2),
    "negative_tolerance": 1e-6,
    "calibration_sums_twelfths": [12, 13],
    "training_repetitions_per_encoding": 16,
    "heldout_repetitions_per_encoding": 8,
    "identities": "first 16 legal 12/13 board pairs by board ID train; next 8 heldout",
    "seed": 130014,
    "distances": "descriptive only",
}


def score_pair_discrimination(train_x, train_y, heldout_x, heldout_y, *,
                              train_ids, heldout_ids, seed=130014):
    """The one scorer for calibration and saved-network geometry rows."""
    if not len(train_ids) or not len(heldout_ids):
        raise ValueError("pair discrimination panel is empty")
    if len(train_ids) != len(train_y) or len(heldout_ids) != len(heldout_y):
        raise ValueError("pair discrimination identity coverage differs")
    if set(train_ids) & set(heldout_ids):
        raise ValueError("pair discrimination training/heldout identities overlap")
    for labels in (train_y, heldout_y):
        if set(labels.tolist()) != {0, 1}:
            raise ValueError("pair discrimination lacks both classes")
    row = fit_reader(train_x, train_y, heldout_x, heldout_y,
                     family="linear", seed=seed)
    row["training_identities"] = list(train_ids)
    row["heldout_identities"] = list(heldout_ids)
    row["training_class_counts"] = torch.bincount(train_y, minlength=2).tolist()
    row["heldout_class_counts"] = torch.bincount(heldout_y, minlength=2).tolist()
    return row


def discrimination_decision(positive, negatives):
    """Tiny-confidence argmax success alone cannot pass the discrimination bar."""
    if not negatives:
        raise ValueError("pair discrimination negative panel is empty")
    accuracy = positive["accuracy"] >= SETTINGS["positive_accuracy_minimum"] and all(
        r["accuracy"] < SETTINGS["negative_accuracy_maximum_exclusive"] for r in negatives)
    converged = positive["converged"] is True and all(
        r["converged"] is True for r in negatives)
    separation = min(r["cross_entropy_nats"] for r in negatives) - positive["cross_entropy_nats"]
    finite = math.isfinite(separation) and all(math.isfinite(r["cross_entropy_nats"])
                                              for r in [positive, *negatives])
    return {"accuracy_bars": accuracy, "convergence": converged,
            "cross_entropy_separation_nats": separation,
            "log_loss_bar": finite and separation >= SETTINGS["minimum_cross_entropy_separation_nats"],
            "pass": accuracy and converged and finite and
                    separation >= SETTINGS["minimum_cross_entropy_separation_nats"]}


def calibration():
    # Different configuration identities share a legal numerical encoding.
    # Labels are the endpoints of the actual 12/13 pair, not a vocabulary threshold.
    train_y = torch.tensor([0, 1] * 16)
    heldout_y = torch.tensor([0, 1] * 8)
    boards = enumerate_boards().boards
    lookup = {b: i for i, b in enumerate(boards)}
    pairs = [(i, lookup[(13, *b[1:])]) for i, b in enumerate(boards)
             if b[0] == 12 and (13, *b[1:]) in lookup]
    if len(pairs) < 24:
        raise ValueError("geometry calibration legal pair support is insufficient")
    train_ids = [i for pair in pairs[:16] for i in pair]
    heldout_ids = [i for pair in pairs[16:24] for i in pair]
    indices = torch.tensor([VALUES.index(s) for s in SETTINGS["calibration_sums_twelfths"]])
    onehot_train = torch.nn.functional.one_hot(indices[train_y], 36).float()
    onehot_heldout = torch.nn.functional.one_hot(indices[heldout_y], 36).float()
    train = encode_answers(onehot_train, "numerical")
    heldout = encode_answers(onehot_heldout, "numerical")

    def score(x, y, z):
        return score_pair_discrimination(x, y, z, heldout_y,
            train_ids=train_ids, heldout_ids=heldout_ids, seed=SETTINGS["seed"])

    positive = score(train, train_y, heldout)
    constant = score(torch.zeros_like(train), train_y, torch.zeros_like(heldout))
    # Exactly eight labels of each class at *each* repeated training encoding.
    # This is fixed algebraically, not selected by a search over permutations.
    balanced_labels = torch.tensor([0, 0, 1, 1] * 8)
    balanced = score(train, balanced_labels, heldout)
    for code in (0, 1):
        if torch.bincount(balanced_labels[train_y == code], minlength=2).tolist() != [8, 8]:
            raise ValueError("repeated-encoding negative is not class balanced")
    decision = discrimination_decision(positive, [constant, balanced])
    expected = all(abs(r["accuracy"] - .5) <= SETTINGS["negative_tolerance"] and
        abs(r["cross_entropy_nats"] - math.log(2)) <= SETTINGS["negative_tolerance"]
        for r in (constant, balanced))
    return {"legal_pair_support": len(pairs),
            "training_pairs": pairs[:16], "heldout_pairs": pairs[16:24],
            "readers": {"numerical": positive, "constant": constant,
                         "encoding_balanced": balanced,
                         "onehot": score(onehot_train, train_y, onehot_heldout)},
            "balanced_labels": balanced_labels.tolist(), "decision": decision,
            "negative_expected_values": expected, "pass": decision["pass"] and expected,
            "onehot_scope": "non-ordered comparison; no numerical-order distance gate"}
