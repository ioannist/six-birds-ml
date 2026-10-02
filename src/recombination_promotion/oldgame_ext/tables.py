"""Shared per-cell table and its five-cell routed composition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import hashlib
import json

from . import game


@dataclass(frozen=True)
class CellTable:
    transition: tuple[tuple[int, ...], ...]
    answer: tuple[tuple[int, int, int], ...]
    start: int

    def __post_init__(self) -> None:
        n = len(self.transition)
        if (not n or len(self.answer) != n or not 0 <= self.start < n
                or any(len(row) != 6 or any(not 0 <= code < n for code in row)
                       for row in self.transition)
                or any(len(row) != 3 or any(value < 0 for value in row)
                       for row in self.answer)):
            raise ValueError("per-cell table has malformed dimensions or values")

    @property
    def n_codes(self) -> int:
        return len(self.transition)

    def code_after(self, history: game.History) -> int:
        code = self.start
        for mass in history:
            code = self.transition[code][game.MASSES.index(mass)]
        return code

    def answer_after(self, history: game.History, kind: int) -> int:
        return self.answer[self.code_after(history)][kind]


def table_record(table: CellTable) -> dict[str, object]:
    """Canonical, content-addressed finite transition and answer tables."""

    body = {"start": table.start,
            "transition": [list(row) for row in table.transition],
            "answer": [list(row) for row in table.answer]}
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return {**body, "sha256": hashlib.sha256(encoded).hexdigest()}


def verified_table(record: dict[str, object]) -> CellTable:
    if not isinstance(record, dict) or set(record) != {"start", "transition", "answer", "sha256"}:
        raise ValueError("saved table record schema differs")
    table = CellTable(
        transition=tuple(tuple(int(value) for value in row)
                         for row in record["transition"]),
        answer=tuple(tuple(int(value) for value in row)
                     for row in record["answer"]),
        start=int(record["start"]),
    )
    if table_record(table) != record:
        raise ValueError("saved table hash or values differ")
    return table


def five_cell_codes(table: CellTable, records: Sequence[game.Record]) -> tuple[int, ...]:
    if len(records) > 4:
        raise ValueError("four-record game has at most four routed records")
    codes = [table.start] * 5
    for slot, mass in records:
        if not 0 <= slot < 5 or mass not in game.MASSES:
            raise ValueError("routed record is outside the game")
        codes[slot] = table.transition[codes[slot]][game.MASSES.index(mass)]
    return tuple(codes)


def five_cell_answer(table: CellTable, records: Sequence[game.Record],
                     query_slot: int, kind: int) -> int:
    if not 0 <= query_slot < 5 or kind not in (0, 1, 2):
        raise ValueError("query is outside the five-cell game")
    return table.answer[five_cell_codes(table, records)[query_slot]][kind]
