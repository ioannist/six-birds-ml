"""Fail-closed write-up contracts, public projections and standalone exact arithmetic."""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import re
from fractions import Fraction


PRIVATE = re.compile(r"/(?:home|mnt|tmp|root|Users)/[^\s\]\)\"'<>`,;]+")


def sanitize(value):
    """Sanitize embedded paths, including correspondence and command strings."""
    if isinstance(value, dict):
        return {sanitize(k): sanitize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize(v) for v in value]
    if isinstance(value, str):
        def public(match):
            path = match.group()
            for marker in ("/runs/", "/tmp/"):
                if marker in path and path.startswith("/mnt/"):
                    return "bulk/" + path.split(marker, 1)[1]
            if "/six-birds-ml/" in path:
                return "repo/" + path.split("/six-birds-ml/", 1)[1]
            return "[private-path]"
        return PRIVATE.sub(public, value)
    return value


def exact_task_sources(evidence):
    """Use the pinned mass vocabulary, enumeration functions and law constants only.

    No package initializer, torch or neural code is imported by the analysis.
    """
    paths = ["src/recombination_promotion/serialization/minimal_recombination.py",
             "src/recombination_promotion/oldgame_ext/game.py",
             "src/recombination_promotion/oldgame_ext/multiround.py"]
    sources = []
    for path in paths:
        entry = evidence.entries["repo/" + path]
        evidence.verify(entry)
        sources.append(ast.parse(evidence.path(entry).read_text()))
    def constants(tree, names):
        values = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in names:
                    if any(not isinstance(n, (ast.Tuple, ast.Dict, ast.List, ast.Constant,
                        ast.Load, ast.Call, ast.Name)) for n in ast.walk(node.value)):
                        raise ValueError("unsupported task constant expression")
                    if any(isinstance(n, ast.Name) and n.id != "Fraction" for n in ast.walk(node.value)):
                        raise ValueError("unsupported task constant name")
                    values[node.targets[0].id] = eval(compile(ast.Expression(node.value), "task", "eval"),
                                                   {"__builtins__": {}, "Fraction": Fraction})
        if set(values) != set(names):
            raise ValueError("task constants missing")
        return values
    mass = constants(sources[0], {"DEFAULT_MASS_VOCAB", "MASS_VALUE"})
    namespace = {"MASSES": tuple(int(12 * mass["MASS_VALUE"][t]) for t in mass["DEFAULT_MASS_VOCAB"]),
                 "History": tuple, "product": itertools.product}
    functions = [n for n in sources[1].body if isinstance(n, ast.FunctionDef) and
                 n.name in {"histories", "whole_endpoints"}]
    exec(compile(ast.Module(body=functions, type_ignores=[]), "pinned_game", "exec"), namespace)
    law = constants(sources[2], {"P", "P_EQUAL"})
    functions = [n for n in sources[2].body if isinstance(n, ast.FunctionDef) and
                 n.name in {"board_category", "update_mode"}]
    exec(compile(ast.Module(body=functions, type_ignores=[]), "pinned_law", "exec"), law)
    return namespace, law


def validate_outline(text, registry, values):
    lines = {i: line.strip() for i, line in enumerate(text.splitlines(), 1) if line.strip()}
    entries = registry["lines"]
    if set(lines) != {r["line"] for r in entries}:
        raise ValueError("outline line coverage differs from explicit registry")
    for row in entries:
        if lines[row["line"]] != row["approved_wording"]:
            raise ValueError(f"stated outline wording/number mismatch: O-{row['line']:03d}")
        if row["kind"] == "editorial":
            if not row["editorial_reason"]:
                raise ValueError("editorial label needs an explicit reason")
        else:
            if not row["computations"]:
                raise ValueError("scientific claim has no named computation")
            for name in row["computations"]:
                if name not in values:
                    raise ValueError(f"unregistered computation: {name}")
        if not row["metadata"]:
            raise ValueError("outline metadata missing")


def publish_projection(entry, source, folder):
    """Original bytes are immutable; projections bind their original SHA-256."""
    is_json = source.suffix == ".json" or ".json." in source.name
    path = folder / (entry["id"] + (".json" if is_json else source.suffix))
    content = source.read_text()
    value = json.loads(content) if is_json else content
    value = sanitize(value)
    data = (json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                       separators=(",", ":")) + "\n") if is_json else value
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
    return {"path": "public/" + path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size, "original_sha256": entry["sha256"],
            "transform": "Public projection: portable scientific evidence; original SHA-256 retained; numerical values unchanged"}


def metadata_for(identifier, authority):
    if identifier not in authority:
        raise ValueError(f"measurement metadata not specified: {identifier}")
    return dict(authority[identifier])
