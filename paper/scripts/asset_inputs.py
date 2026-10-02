"""Verified, ledger-bound inputs and receipts shared by every paper asset."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import build_ledger as ledger

ROOT = Path(__file__).resolve().parents[2]


def digest(value):
    return hashlib.sha256(ledger.canonical(value).encode()).hexdigest()


class Inputs:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.ledger_sha256 = ledger.sha(self.root / "paper/notes/claims_ledger.json")
        self.manifest_file_sha256 = ledger.sha(self.root / ledger.MANIFEST)
        self.ledger = json.loads((self.root / "paper/notes/claims_ledger.json").read_text())
        self.manifest = json.loads((self.root / ledger.MANIFEST).read_text())
        if self.manifest.get('original_manifest_sha256', ledger.sha(self.root / ledger.MANIFEST)) != self.ledger["source_manifest_sha256"]:
            raise ValueError("asset ledger/manifest identity differs")
        self.evidence = ledger.Evidence(self.root, self.manifest)
        self.by_id = {r["id"]: r for r in self.manifest["artifacts"]}
        self.sources = {}
        self.source_artifacts = {}
        self.bindings = {}
        self.receipts = []
        self.assert_current()
        self.quantities = self.ledger["recomputed_outline_quantities"]
        reported = json.loads((self.root / "paper/data/reported_outline_quantities.json").read_text())
        if reported != self.quantities:
            raise ValueError("plotted text quantities differ from ledger")
        self.sources["quantities"] = self.quantities
        for name in ("control", "calibration"):
            entry = self.evidence.entries[f"bulk/paper_data_bulk/{name}_tables.json"]
            self.evidence.verify(entry)
            self.source_artifacts[name] = entry['id']
            self.sources[name] = json.loads(self.evidence.path(entry).read_text())
        for c in self.ledger["claims"]:
            comp = c["computation"]
            if c["id"].startswith("N-"):
                key = ("control", str(c["study"]), *comp["pointer"])
                self.bindings[key] = c
            elif c["id"].startswith("C-"):
                key = ("calibration", str(c["study"]), *comp["pointer"])
                self.bindings[key] = c
        # Every measured control/calibration field must still match its ledger
        # vector, not just the current file name or a derived plotting cache.
        for path, c in self.bindings.items():
            v = self.at(path)
            expected = c["rebuilt_value"]
            if isinstance(expected, dict) and "sha256" in expected:
                if digest(v) != expected["sha256"]:
                    raise ValueError(f"asset measurement vector differs: {c['id']}")
            elif v != expected:
                raise ValueError(f"asset scalar differs: {c['id']}")

    def at(self, path):
        value = self.sources[path[0]]
        for key in path[1:]:
            value = value[key]
        return value

    def assert_current(self):
        """Never bind values loaded earlier to a newer on-disk authority."""
        if (ledger.sha(self.root / 'paper/notes/claims_ledger.json') != self.ledger_sha256 or
                ledger.sha(self.root / ledger.MANIFEST) != self.manifest_file_sha256):
            raise ValueError('asset authority changed during build; rebuild all assets after pinning')

    def begin(self):
        self.receipts = []

    def ref(self, *path):
        value = self.at(path)
        parents = [self.bindings[tuple(path[:n])]["id"]
                   for n in range(len(path), 0, -1) if tuple(path[:n]) in self.bindings]
        if path[0] == "quantities":
            parents = [c["id"] for c in self.ledger["claims"] if
                       path[1] in c["computation"].get("names", [])]
            if path[1] == "task":
                parents += [c["id"] for c in self.ledger["claims"] if c["id"].startswith("TASK-")]
        if not parents and path[0] not in self.by_id and path[0] not in self.source_artifacts:
            raise ValueError(f"asset value lacks ledger or manifest support: {path}")
        self.receipts.append({"source": path[0], "pointer": list(path[1:]),
                              "value": value, "sha256": digest(value), "ledger_ids": parents,
                              "manifest_id": self.source_artifacts.get(path[0], path[0] if path[0] in self.by_id else None)})
        return value

    def registered(self, number):
        entry = self.evidence.entries["repo/" + str(ledger.study_path(number) / "registration.json")]
        return self.manifest_json(entry)

    def manifest_json(self, entry):
        self.evidence.verify(entry)
        if entry["id"] not in self.sources:
            self.sources[entry["id"]] = json.loads(self.evidence.path(entry).read_text())
        self.receipts.append({"source": entry["id"], "pointer": [],
                              "sha256": entry["sha256"], "manifest_only": True})
        return self.sources[entry["id"]]

    def referenced(self, record):
        key = record["path"]
        if not key.startswith(("repo/", "bulk/", "bulk/")):
            key = "repo/" + key
        entry = self.evidence.entries[key]
        if entry["sha256"] != record["sha256"]:
            raise ValueError("referenced asset source hash differs")
        return self.manifest_json(entry), entry["id"]

    def save_receipts(self, name, folder, description, extra=None):
        self.assert_current()
        path = self.root / "paper" / folder / f"{name}.values.json"
        value = {"asset": name, "description": description,
                 "ledger_sha256": self.ledger_sha256,
                 "manifest_sha256": self.ledger['source_manifest_sha256'],
                 "receipts": self.receipts, **(extra or {})}
        path.write_text(ledger.small_json(value))
        return path


def tex(value):
    """Escape prose, preserving no caller-supplied TeX commands."""
    text = str(value).replace("×", " x ")
    text = text.replace("–", "--").replace("—", "---").replace("≈", "approx.")
    chars = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_\allowbreak{}",
             "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
             "\\": r"\textbackslash{}", "/":r"/\allowbreak{}",
             "→":r"$\to$", "≥":r"$\geq$", "≤":r"$\leq$"}
    return "".join(chars.get(c, c) for c in text)


def number(value):
    if value is None:
        return "not recorded"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return f'{value:,}'
    if isinstance(value, float):
        return f"{value:.5g}"
    if isinstance(value, list):
        return "/".join(number(x) for x in value)
    return str(value)


def verify_receipts(ctx, receipt):
    """Refuse stale/tampered plotted values independently of the image bytes."""
    ctx.assert_current()
    if receipt['ledger_sha256'] != ledger.sha(ctx.root/'paper/notes/claims_ledger.json'):
        raise ValueError('asset ledger identity differs')
    if receipt['manifest_sha256'] != ctx.ledger['source_manifest_sha256']:
        raise ValueError('asset manifest identity differs')
    claims={c['id'] for c in ctx.ledger['claims']}
    for r in receipt['receipts']:
        if r.get('manifest_only'):
            entry=ctx.by_id[r['source']];ctx.evidence.verify(entry)
            if r['sha256']!=entry['sha256']:raise ValueError('asset source identity differs')
            if r['source'] not in ctx.sources and not r.get('non_json'):ctx.manifest_json(entry)
            continue
        if r['source']=='claims_ledger':
            if not set(r['ledger_ids'])<=claims:raise ValueError('asset entry not in ledger')
            continue
        if r['source']=='evidence_manifest':
            value=ctx.manifest
        else:
            if r['source'] not in ctx.sources:
                ctx.manifest_json(ctx.by_id[r['source']])
            value=ctx.sources[r['source']]
        for k in r['pointer']:value=value[k]
        if r['sha256']!=digest(value) or r.get('value')!=value:
            raise ValueError('asset plotted value differs from verified evidence')
        if r['source'] in ('control','calibration','quantities'):
            valid_ids=set(r.get('ledger_ids',[]))
            if valid_ids and not valid_ids<=claims:raise ValueError('asset entry not in ledger')
            if not valid_ids and r.get('manifest_id') not in ctx.by_id:
                raise ValueError('asset metadata lacks manifest binding')
