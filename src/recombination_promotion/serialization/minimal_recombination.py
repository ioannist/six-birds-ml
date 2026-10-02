"""Shared scientific functions used by r8–r13."""
from __future__ import annotations


import json


import random


from dataclasses import dataclass


from fractions import Fraction




from hashlib import sha256








from typing import Mapping, Sequence




DEFAULT_P = 3


DEFAULT_TEMPLATE_NAMES = ("mass_at", "slot_gets", "put_on")


DEFAULT_MASS_VOCAB = (
    "one_sixth",
    "one_fourth",
    "one_third",
    "half",
    "two_thirds",
    "three_fourths",
)


MASS_VALUE = {
    "zero": Fraction(0, 1),
    "one_sixth": Fraction(1, 6),
    "one_fourth": Fraction(1, 4),
    "one_third": Fraction(1, 3),
    "half": Fraction(1, 2),
    "two_thirds": Fraction(2, 3),
    "three_fourths": Fraction(3, 4),
}


@dataclass(frozen=True)
class MinimalConfig:
    config_id: str
    placements: tuple[tuple[str, str], ...]
    query_order: tuple[str, ...] = ()
    template: str = "mass_at"
    underlying_id: str = ""
    nonce_binding: str = "none"

    @property
    def k_class(self) -> tuple[str, ...]:
        return tuple(sorted(mass for mass, _slot in self.placements))

    @property
    def r_class(self) -> tuple[str, ...]:
        return answer_for_config(self, p=_slot_count(self.placements, self.query_order))


def serialize_config(config: MinimalConfig, *, p: int = DEFAULT_P) -> tuple[str, ...]:
    tokens: list[str] = []
    template = config.template
    bindings, record_targets = _nonce_bindings_for_config(config, p=p)
    for source, target, kind in bindings:
        tokens.extend((kind, source, "eq", target, "sep"))
    for index, (mass, _slot) in enumerate(config.placements):
        target = record_targets[index]
        if template == "mass_at":
            tokens.extend(("mass", mass, "at", target, "sep"))
        elif template == "slot_gets":
            tokens.extend(("slot", target, "gets", mass, "sep"))
        elif template == "put_on":
            tokens.extend(("put", mass, "on", target, "sep"))
        else:
            raise ValueError(f"unknown minimal template {template}")
    marker = {"mass_at": "query", "slot_gets": "ask", "put_on": "read"}[template]
    tokens.append(marker)
    tokens.extend(config.query_order or tuple(f"h{index}" for index in range(p)))
    return tuple(tokens)


def answer_for_config(config: MinimalConfig, *, p: int = DEFAULT_P) -> tuple[str, ...]:
    by_slot = {f"h{index}": Fraction(0, 1) for index in range(p)}
    for mass, slot in config.placements:
        by_slot[slot] += MASS_VALUE[mass]
    order = config.query_order or tuple(f"h{index}" for index in range(p))
    return tuple(_fraction_to_mass_token(by_slot[slot]) for slot in order)


def solve_from_visible_tokens(tokens: Sequence[str], *, p: int = DEFAULT_P) -> tuple[str, ...]:
    placements, query_order, _template = _parse_visible_prompt(tokens, p=p)
    by_slot = {f"h{index}": Fraction(0, 1) for index in range(p)}
    for mass, slot in placements:
        by_slot[slot] += MASS_VALUE[mass]
    return tuple(_fraction_to_mass_token(by_slot[slot]) for slot in query_order)


def _parse_visible_prompt(
    tokens: Sequence[str],
    *,
    p: int = DEFAULT_P,
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...], str]:
    placements: list[tuple[str, str]] = []
    slots = {f"h{index}" for index in range(p)}
    bindings: dict[str, str] = {}
    index = 0
    template = "mass_at"
    while index < len(tokens):
        token = tokens[index]
        if token in {"query", "ask", "read"}:
            query_order = tuple(tokens[index + 1 :])
            if set(query_order) != slots or len(query_order) != p:
                raise ValueError("query order must list every screen slot exactly once")
            return tuple(placements), query_order, template
        if token in {"bind", "link"}:
            source = tokens[index + 1]
            if tokens[index + 2] != "eq":
                raise ValueError("binding marker missing")
            bindings[source] = tokens[index + 3]
            index += 5
            continue
        if token == "mass":
            template = "mass_at"
            mass = tokens[index + 1]
            if tokens[index + 2] != "at":
                raise ValueError("placement marker missing")
            slot = tokens[index + 3]
            step = 5
        elif token == "slot":
            template = "slot_gets"
            slot = tokens[index + 1]
            if tokens[index + 2] != "gets":
                raise ValueError("slot_gets marker missing")
            mass = tokens[index + 3]
            step = 5
        elif token == "put":
            template = "put_on"
            mass = tokens[index + 1]
            if tokens[index + 2] != "on":
                raise ValueError("put_on marker missing")
            slot = tokens[index + 3]
            step = 5
        else:
            raise ValueError(f"expected record at token {index}")
        slot = _resolve_slot_reference(slot, bindings, slots)
        if slot not in slots:
            raise ValueError(f"unknown slot {slot}")
        if mass not in MASS_VALUE:
            raise ValueError(f"unknown mass {mass}")
        placements.append((mass, slot))
        index += step
    raise ValueError("query marker missing")


def _fraction_to_mass_token(value: Fraction) -> str:
    known = {fraction: token for token, fraction in MASS_VALUE.items()}
    if value in known:
        return known[value]
    if value == 1:
        return "one"
    return f"{value.numerator}_over_{value.denominator}"


def _nonce_vocab(nonce_binding: str) -> tuple[str, ...]:
    if nonce_binding == "one_hop":
        return tuple(f"v{index}" for index in range(64))
    if nonce_binding == "random":
        return tuple(f"c{index}" for index in range(64)) + tuple(
            f"u{index}" for index in range(64)
        )
    if nonce_binding == "none":
        return ()
    raise ValueError(f"unknown nonce binding mode {nonce_binding}")


def _nonce_bindings_for_config(
    config: MinimalConfig,
    *,
    p: int,
) -> tuple[tuple[tuple[str, str, str], ...], tuple[str, ...]]:
    if config.nonce_binding == "none":
        return (), tuple(slot for _mass, slot in config.placements)
    rng = random.Random(
        int(
            sha256(
                json.dumps(
                    {
                        "config_id": config.config_id,
                        "underlying_id": config.underlying_id,
                        "template": config.template,
                        "placements": config.placements,
                        "query_order": config.query_order,
                        "mode": config.nonce_binding,
                        "p": p,
                    },
                    sort_keys=True,
                ).encode("utf-8")
            ).hexdigest()[:16],
            16,
        )
    )
    if config.nonce_binding == "one_hop":
        pool = list(_nonce_vocab("one_hop"))
        rng.shuffle(pool)
        record_targets = tuple(pool[index] for index in range(len(config.placements)))
        bindings = tuple(
            ("bind", record_targets[index], slot)
            for index, (_mass, slot) in enumerate(config.placements)
        )
        return tuple((source, target, kind) for kind, source, target in bindings), record_targets
    if config.nonce_binding == "random":
        carriers = [token for token in _nonce_vocab("random") if token.startswith("c")]
        histories = [token for token in _nonce_vocab("random") if token.startswith("u")]
        rng.shuffle(carriers)
        rng.shuffle(histories)
        record_targets = tuple(carriers[index] for index in range(len(config.placements)))
        binding_rows: list[tuple[str, str, str]] = []
        for index, (_mass, slot) in enumerate(config.placements):
            binding_rows.append((record_targets[index], histories[index], "link"))
            binding_rows.append((histories[index], slot, "bind"))
        return tuple(binding_rows), record_targets
    raise ValueError(f"unknown nonce binding mode {config.nonce_binding}")


def _resolve_slot_reference(
    token: str,
    bindings: Mapping[str, str],
    slots: set[str],
) -> str:
    seen = set()
    current = token
    while current not in slots:
        if current in seen:
            raise ValueError("cycle in nonce binding")
        seen.add(current)
        if current not in bindings:
            raise ValueError(f"unbound placement token {current}")
        current = bindings[current]
    return current


def _slot_count(
    placements: Sequence[tuple[str, str]],
    query_order: Sequence[str] = (),
) -> int:
    slots = [slot for _mass, slot in placements]
    slots.extend(query_order)
    return 1 + max(int(slot[1:]) for slot in slots)

