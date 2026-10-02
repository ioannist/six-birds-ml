# r10 report storage

The report was rebuilt from saved audits only. No network evaluation,
probe fitting, training, calibration rerun or checkpoint selection occurred.
All 18 runs' B bars, endpoint pass values, learning curves, law measurements,
probe results (including paired intervals) and both interchange records are
numerically identical to the earlier detailed aggregate: canonical hashes
match for all 126 run–field groups. Only interpretation and reporting changed.

**Relocation is complete.** It was run on the host on 2026-10-01 by the distribution
with the report-only command below. implementation's sandbox could not write the bulk directory,
so the files were first staged under the temporary area; that staging copy is
superseded.

- Bulk directory: `bulk/study_r10_allslots_bulk/report_details/`
- Detailed aggregate: `aggregate_detailed.0e91fae19919ba0b85b30ca61d3684b35d22e1560f0641c0f19816b8a0f2f7ff.json`,
  **407,292,024 bytes**, SHA-256
  **`0e91fae19919ba0b85b30ca61d3684b35d22e1560f0641c0f19816b8a0f2f7ff`**
- Large calibration files are preserved byte for byte under `report_details/preserved/`.
  The repository keeps symlinks at the original calibration paths, so their hashes
  and saved-audit bindings remain valid.
- `bulk_artifact_references.json` lists original paths, actual paths, byte counts
  and SHA-256 values. The compact `aggregate.json` records `storage_status:
  REQUESTED_BULK_ROOT`.

The repository study directory decreased from 503 MB to 7.7 MB.

Command used (report-only; it neither trains, evaluates networks nor fits probes):

```bash
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONPATH=src:. TMPDIR="${TMPDIR:-$PWD/build/tmp}" python -m scripts.oldgame_multiround_allslots aggregate --device cpu --bulk-root "${SBML_DATA:-evidence/bulk}/study_r10_allslots_bulk/"
```
