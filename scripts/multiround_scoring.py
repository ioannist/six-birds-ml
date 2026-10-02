"""Shared scientific sampling and scoring utilities for r8–r13."""
from __future__ import annotations
import numpy as np
from recombination_promotion.oldgame_ext.multiround import Episodes

def _active(data: Episodes) -> np.ndarray:
    return np.arange(data.boards.shape[1])[None, :] < data.lengths[:, None]
