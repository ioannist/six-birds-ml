# r13 saved-state report revision

No model training, run selection, endpoint relabelling or threshold change occurred. The original training script is archived by its registered SHA-256. Reporting checks that every non-aggregate syntax tree is unchanged, alongside settings and dependency hashes. Registration and calibration bytes remain fixed. The aggregate entry now calls the separate saved-state analysis; it does not refresh training authority.

The supplementary panel was declared before checkpoint states were opened. It contains all 285 legal 12/13 pairs (135 fitting, 150 evaluation) and all 25 legal 23/24 pairs (12 fitting, 13 evaluation). All other slot sums match within each pair. Fitting/evaluation identities are disjoint, and every existing probe-held-out identity is excluded from fitting. The four executed renderings have fixed record-array hashes. There was no resampling based on discrimination results.

The extraction used CPU float32, one thread, and no model gradients or updates. It took 10.949 seconds. Only the declared logistic readers were fitted. At 20k the probability-target readers pass both cutoff discrimination checks for all seeds. Sampled-target passes are mixed: 12/13 passes only seed 1; 23/24 passes seeds 0 and 2. These are supplementary readability findings, not predictive closure or a causal result.

## Rebuild the compact report

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONPATH=src:. TMPDIR="${TMPDIR:-$PWD/build/tmp}" CUDA_VISIBLE_DEVICES='' python scripts/oldgame_multiround_mechanism.py --stage aggregate --device cpu
```

The detailed JSON contains the full missing-support inventory, all observed movement-range points, and references to every saved audit and per-update record. The earlier 9.9 MB Markdown and 12 MB JSON remain byte-preserved outside the repository. The compact repository report contains all numbers needed for the comparison tables.

## Host copy to the requested bulk destination

The sandbox cannot write the requested bulk directory. All new details, feature arrays and the two archived source files are staged under `build/oldgame_ext/r13_report_details/`. Their references include the intended host bulk path and SHA-256. The actual staged paths remain valid until the host copy; no source is deleted. The older 418 MB detailed audit aggregate already resides in the requested bulk directory and is unchanged.

Run on the host, not in this sandbox:

```bash
mkdir bulk/study_r13_mechanism_bulk/report_revision
cp -p build/oldgame_ext/r13_report_details/* bulk/study_r13_mechanism_bulk/report_revision/
cd bulk/study_r13_mechanism_bulk/report_revision
sha256sum -c SHA256SUMS
```

The `mkdir` deliberately refuses an existing destination. If it already exists, verify its hashes rather than overwriting it. Log files are informational and are excluded from the checksum list. Compact JSON retains hash-bound staged references with their matching `host_bulk_path` values; the copy needs no alteration of the scientific records.

## Narrow conclusion

Target noise, access and encoding affect measured errors; none alone guarantees B closure, and erosion is gradient-mediated without being uniquely Adam-specific.

## Completed on the host (2026-10-01, distribution)

The copy above was run; `sha256sum -c SHA256SUMS` reported OK for every file. The compact reports' detail references were then updated from the staging path to `bulk/study_r13_mechanism_bulk/report_revision/`. File contents and hashes are unchanged.
