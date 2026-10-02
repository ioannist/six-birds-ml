"""Shared scientific sampling and scoring utilities for r8–r13."""
from __future__ import annotations
import hashlib
import numpy as np
from recombination_promotion.oldgame_ext.multiround import episodes
from scripts import multiround_scoring as prior
BATCH = 256
STREAM_SEED_BASE = 202609290000

def _pair_ids(data, active: np.ndarray) -> np.ndarray:
    positions = active[:, 2:]
    left = data.boards[:, :-2][positions].astype(np.int64)
    right = data.boards[:, 1:-1][positions].astype(np.int64)
    return left * 24435 + right

class UnseenCandidates:

    def __init__(self, test) -> None:
        self.test = test
        self.test_active = prior._active(test)
        eligible = self.test_active.copy()
        eligible[:, :2] = False
        self.eligible = eligible
        self.candidates = np.unique(_pair_ids(test, eligible))
        self.seen = np.zeros(len(self.candidates), dtype=bool)

    def observe(self, batch) -> None:
        active = prior._active(batch)
        active[:, :2] = False
        values = np.unique(_pair_ids(batch, active))
        at = np.searchsorted(self.candidates, values)
        valid = at < len(self.candidates)
        matched = valid.copy()
        matched[valid] = self.candidates[at[valid]] == values[valid]
        self.seen[at[matched]] = True

    def mask(self) -> np.ndarray:
        result = np.zeros_like(self.eligible)
        ids = _pair_ids(self.test, self.eligible)
        at = np.searchsorted(self.candidates, ids)
        if np.any(at == len(self.candidates)) or not np.array_equal(self.candidates[at], ids):
            raise ValueError('test candidate ID lookup differs')
        result[self.eligible] = ~self.seen[at]
        return result

    def composition(self, mask: np.ndarray) -> dict:
        categories = self.test.categories[mask]
        modes = self.test.modes[mask]
        return {'active_test_pair_positions': int(self.eligible.sum()), 'unique_candidate_pair_ids': len(self.candidates), 'encountered_pair_ids': int(self.seen.sum()), 'unmarked_test_positions': int(mask.sum()), 'by_category': {name: int((categories == category).sum()) for category, name in enumerate(('L', 'N', 'H'))}, 'by_mode': {str(mode): int((modes == mode).sum()) for mode in (0, 1)}, 'by_mode_category': {f'{mode}_{name}': int(((modes == mode) & (categories == category)).sum()) for mode in (0, 1) for category, name in enumerate(('L', 'N', 'H'))}}

class OnlineStream:

    def __init__(self, boards, seed: int, *, equal_p: bool=False) -> None:
        self.boards = boards
        self.stream_seed = STREAM_SEED_BASE + seed
        self.rng = np.random.default_rng(self.stream_seed)
        self.equal_p = equal_p
        self.rolling = bytes(32)
        self.draws = 0

    def draw(self):
        batch_seed = int(self.rng.integers(0, 2 ** 63 - 1))
        batch = episodes(self.boards, BATCH, 8, batch_seed, equal_p=self.equal_p, stop_third_N=True)
        active = prior._active(batch)
        third = (batch.categories[:, 2:] == 1) & (batch.categories[:, 1:-1] == 1) & (batch.categories[:, :-2] == 1)
        if np.any(third & active[:, 2:]):
            raise ValueError('online batch includes third consecutive N input')
        digest = hashlib.sha256()
        digest.update(self.rolling)
        digest.update(batch_seed.to_bytes(8, 'little'))
        for array in (batch.boards, batch.categories, batch.modes, batch.targets, batch.lengths, batch.rendering_seeds):
            digest.update(array.tobytes())
        self.rolling = digest.digest()
        self.draws += 1
        return (batch_seed, batch)

    def state(self) -> dict:
        return {'stream_seed': self.stream_seed, 'numpy_rng_state': self.rng.bit_generator.state, 'rolling_batch_sha256': self.rolling.hex(), 'draws': self.draws, 'equal_p': self.equal_p}
