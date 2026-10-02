"""Instrumented record-level A and cross-round predictive recurrence."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

from . import game
from .memory import MemoryCore, VALUES


class ChoiceNetwork(nn.Module):
    """Only hard A answers and a separate raw vector reach the upper state."""

    def __init__(self, *, memory_width: int = 64, raw_width: int = 16,
                 upper_width: int = 32) -> None:
        super().__init__()
        self.memory = MemoryCore(memory_width)
        self.raw_embedding = nn.Embedding(30, raw_width)
        self.raw_encoder = nn.GRU(raw_width, raw_width, batch_first=True)
        self.answer_embedding = nn.Linear(5 * len(VALUES), upper_width, bias=False)
        self.upper = nn.GRUCell(upper_width + raw_width, upper_width)
        self.category_head = nn.Linear(upper_width, 3)

    def round_interfaces(self, records: torch.Tensor) -> tuple[torch.Tensor, ...]:
        """Resolve one round from its four ordered (slot, mass-index) records."""

        if records.ndim != 3 or records.shape[1:] != (4, 2):
            raise ValueError("record input must have four ordered slot/mass pairs")
        if bool(((records[..., 0] < 0) | (records[..., 0] >= 5)
                 | (records[..., 1] < 0) | (records[..., 1] >= 6)).any()):
            raise ValueError("record slot or mass index differs")
        rows = len(records)
        state = self.memory.start_state.expand(rows, 5, -1)
        for at in range(4):
            slot = records[:, at, 0]
            mass = records[:, at, 1]
            old = state.gather(1, slot[:, None, None].expand(-1, 1, state.shape[-1]))[:, 0]
            changed = self.memory.step(old, mass)
            selected = F.one_hot(slot, 5).bool()[..., None]
            state = torch.where(selected, changed[:, None, :], state)
        sum_logits = self.memory.answer(state.reshape(rows * 5, -1), game.KIND_SUM)
        sum_logits = sum_logits.reshape(rows, 5, len(VALUES))
        soft = torch.softmax(sum_logits, -1)
        hard = F.one_hot(sum_logits.argmax(-1), len(VALUES)).to(soft.dtype)
        # The executed interface is exactly one hot; its training gradient is soft.
        answers = hard + (soft - soft.detach())
        raw_symbols = records[..., 0] * 6 + records[..., 1]
        _, raw_state = self.raw_encoder(self.raw_embedding(raw_symbols))
        return sum_logits, answers, raw_state[0]

    def upper_step(self, answers: torch.Tensor, raw: torch.Tensor,
                   previous: torch.Tensor | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        if answers.shape[-2:] != (5, len(VALUES)) or raw.shape[-1] != self.raw_encoder.hidden_size:
            raise ValueError("upper interface shape differs")
        if previous is None:
            previous = raw.new_zeros((len(raw), self.upper.hidden_size))
        input_values = torch.cat((self.answer_embedding(answers.flatten(1)), raw), -1)
        state = self.upper(input_values, previous)
        return self.category_head(state), state

    def forward(self, records: torch.Tensor, lengths: torch.Tensor, *,
                answer_override: torch.Tensor | None = None,
                raw_override: torch.Tensor | None = None,
                initial_upper: torch.Tensor | None = None,
                return_trace: bool = False):
        if records.ndim != 4 or records.shape[2:] != (4, 2):
            raise ValueError("episode records have the wrong shape")
        if lengths.shape != records.shape[:1] or bool((lengths < 1).any()) or bool(
                (lengths > records.shape[1]).any()):
            raise ValueError("episode lengths differ")
        batch, rounds = records.shape[:2]
        flat = records.reshape(batch * rounds, 4, 2)
        sum_logits, answers, raw = self.round_interfaces(flat)
        sum_logits = sum_logits.reshape(batch, rounds, 5, -1)
        answers = answers.reshape(batch, rounds, 5, -1)
        raw = raw.reshape(batch, rounds, -1)
        effective_answers = answers if answer_override is None else answer_override
        effective_raw = raw if raw_override is None else raw_override
        if effective_answers.shape != answers.shape or effective_raw.shape != raw.shape:
            raise ValueError("intervention interface shape differs")
        state = initial_upper
        logits, states = [], []
        for at in range(rounds):
            predicted, state = self.upper_step(effective_answers[:, at], effective_raw[:, at],
                                               state)
            logits.append(predicted)
            states.append(state)
        category_logits = torch.stack(logits, 1)
        if return_trace:
            return {"sum_logits": sum_logits, "hard_answers": answers,
                    "raw_vectors": raw, "category_logits": category_logits,
                    "upper_states": torch.stack(states, 1)}
        return sum_logits, category_logits
