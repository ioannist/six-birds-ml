"""Shared scientific functions used by r8–r13."""
from __future__ import annotations


import hashlib


import json










from . import game






def history_digest(histories: tuple[game.History, ...]) -> str:
    encoded = json.dumps(histories, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()

