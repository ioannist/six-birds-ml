#!/usr/bin/env python3
"""Regenerate deterministic package integrity files."""

from __future__ import annotations

import argparse
import hashlib
import json
import fnmatch
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INTEGRITY_ROOTS = (
    "src",
    "tests",
    "reports",
    "scripts",
    "paper",
    "evidence",
)
TOP_LEVEL_FILES = (
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "LICENSE",
    "LICENSE-CC-BY-4.0",
)
PRESERVED_MANIFEST_FIELDS = (
    "package",
    "purpose",
    "smoke_tests",
    "source_bundle_alignment",
    "version",
)


def discover_integrity_files(repo_root: Path = REPO_ROOT) -> list[Path]:
    paths: list[Path] = []
    for root_name in INTEGRITY_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if _is_integrity_file(path):
                paths.append(path)
    for file_name in TOP_LEVEL_FILES:
        path = repo_root / file_name
        if path.exists():
            paths.append(path)
    return sorted(set(paths), key=lambda path: path.relative_to(repo_root).as_posix())


def build_file_records(repo_root: Path = REPO_ROOT) -> list[dict[str, object]]:
    records = []
    for path in discover_integrity_files(repo_root):
        data = path.read_bytes()
        records.append(
            {
                "bytes": len(data),
                "path": path.relative_to(repo_root).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return records


def build_checksums_text(repo_root: Path = REPO_ROOT) -> str:
    lines = [
        f"{record['sha256']}  {record['path']}"
        for record in build_file_records(repo_root)
    ]
    return "\n".join(lines) + "\n"


def build_manifest(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    existing = _load_existing_manifest(repo_root)
    manifest = {
        field: existing[field]
        for field in PRESERVED_MANIFEST_FIELDS
        if field in existing
    }
    manifest.update(
        {
            "files": build_file_records(repo_root),
        }
    )
    manifest.setdefault(
        "smoke_tests",
        {
            "command": "pytest -q tests/",
            "status": "not run",
            "status_at_packaging": "not run",
        },
    )
    return manifest


def build_manifest_text(repo_root: Path = REPO_ROOT) -> str:
    return json.dumps(build_manifest(repo_root), indent=2, sort_keys=True) + "\n"


def write_integrity_files(repo_root: Path = REPO_ROOT) -> None:
    (repo_root / "CHECKSUMS.txt").write_text(
        build_checksums_text(repo_root),
        encoding="utf-8",
    )
    (repo_root / "manifest.json").write_text(
        build_manifest_text(repo_root),
        encoding="utf-8",
    )


def check_integrity_files(repo_root: Path = REPO_ROOT) -> bool:
    expected_checksums = build_checksums_text(repo_root)
    expected_manifest = build_manifest_text(repo_root)
    return (
        (repo_root / "CHECKSUMS.txt").read_text(encoding="utf-8")
        == expected_checksums
        and (repo_root / "manifest.json").read_text(encoding="utf-8")
        == expected_manifest
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit nonzero if CHECKSUMS.txt or manifest.json is stale",
    )
    args = parser.parse_args()
    if args.check:
        if check_integrity_files(REPO_ROOT):
            return 0
        print("CHECKSUMS.txt or manifest.json is stale")
        return 1
    write_integrity_files(REPO_ROOT)
    return 0


def _is_integrity_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if _is_review_envelope_report(path):
        return False
    parts = set(path.parts)
    if "__pycache__" in parts or ".pytest_cache" in parts or "build" in parts:
        return False
    if path.suffix in {".pyc", ".pyo"}:
        return False
    return True


def _is_review_envelope_report(path: Path) -> bool:
    return path.parent.name == "reports" and (
        fnmatch.fnmatch(path.name, "external_review_request_*.md")
        or fnmatch.fnmatch(path.name, "*_signoff_request.md")
    )


def _load_existing_manifest(repo_root: Path) -> dict[str, object]:
    manifest_path = repo_root / "manifest.json"
    if not manifest_path.exists():
        return {}
    return json.loads(manifest_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
