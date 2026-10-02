"""Resolve portable repository and optional external-data references."""
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def public_path(value):
    text = str(value)
    if text.startswith('repo/'):
        return ROOT / text.removeprefix('repo/')
    if text.startswith('bulk/'):
        suffix = text.removeprefix('bulk/')
        return data_root() / suffix
    if text.startswith('build/'):
        suffix = text.removeprefix('build/')
        return ROOT / 'build' / suffix
    return Path(os.path.expandvars(text))


def data_root():
    """Bulk artifact directory, configurable without machine-local defaults."""
    return Path(os.environ.get('SBML_DATA', ROOT / 'evidence/bulk')).expanduser()


def identity_matches(recorded, current):
    """Accept only an explicitly hash-bound portable metadata projection."""
    if recorded == current:
        return True
    path = ROOT / 'evidence/identity_projections.json'
    if not path.exists():
        return False
    bindings = json.loads(path.read_text())['bindings']
    seen = set()
    while recorded in bindings and recorded not in seen:
        seen.add(recorded)
        recorded = bindings[recorded]
    return recorded == current


def metadata_matches(recorded, current):
    """Compare scientific metadata, permitting declared hash projections only."""
    if isinstance(recorded, dict) and isinstance(current, dict):
        return recorded.keys() == current.keys() and all(metadata_matches(recorded[k], current[k]) for k in recorded)
    if isinstance(recorded, (list, tuple)) and isinstance(current, (list, tuple)):
        return len(recorded) == len(current) and all(metadata_matches(a,b) for a,b in zip(recorded,current))
    if isinstance(recorded, str) and isinstance(current,str):
        return identity_matches(recorded,current)
    return recorded == current
