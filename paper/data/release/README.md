# Detailed analytical-table records — unreleased

These stable, losslessly gzip-compressed JSON files retain every row underlying
Supplement Tables S1–S28. Gzip timestamps are fixed at zero for byte-identical
rebuilds. Read a file with `gzip.open(path, "rt")` then `json.load`, or `gzip -dc`.
They are built from the hash-verified ledger and source records; no original
study artifacts are edited. `index.json` records the filename, SHA-256, byte
size and row count of each file. A supplement table names its detailed file.

Schema `jagged-table-rows-v1`:

- `table`: stable table identifier, matching its filename.
- `headers`: the ordered column names for the exhaustive records.
- `rows`: ordered arrays aligned with those headers. Integers are exact counts;
  floats retain source precision; null means not recorded, never zero. Nested
  lists retain per-slot values or saved confidence intervals. Booleans are saved
  decisions, not claims of universal correctness.
- `ledger_sha256`: identity of the claims ledger used for the build.
- `source_bindings`: source IDs, field pointers, hashes and relevant ledger IDs.
  IDs resolve through `paper/notes/evidence_manifest.json`; no machine-local
  path is needed.

The analytical table receipts additionally retain `displayed_rows`, identifying
the exact printed reduction, and the detailed-file hash. Named reduction rules
are in `paper/scripts/table_summaries.py`; they do not select by row position.
Start/end probe counts retain each slot's denominator. A range of paired gain
interval endpoints is an envelope, not a new confidence interval. Full
per-slot intervals, floors and solver status are retained in the detailed rows.
Compute examples are not study totals; batched group times are never summed.
Study registrations and original per-presentation arrays remain manifest-bound
release inputs, separate from these table projections.
