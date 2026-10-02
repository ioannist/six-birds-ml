# study_r11_jagged: execution commands

Run from the repository root. Use one visible CUDA device, selected through
`SBML_CUDA_DEVICES`. Numerical CPU threads are limited to one. Training and
evaluation use float32; linear readers fit on CPU. Raw arms use width three;
hard-answer supplied arms use direct width one. `SBML_DATA` optionally names
the bulk artifact directory; the default is `evidence/bulk/`.

```sh
export CUDA_VISIBLE_DEVICES="${SBML_CUDA_DEVICES:?set accelerator visibility}"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=src:.
export TMPDIR="${TMPDIR:-$PWD/build/tmp}"
mkdir -p "$TMPDIR"
python -m scripts.oldgame_multiround_jagged verify-gpu --device cuda --trace-erosion
python -m scripts.oldgame_multiround_jagged run --device cuda --runs rarity --chunk-runs 3
python -m scripts.oldgame_multiround_jagged aggregate --device cpu
```

Use repeated `--run-name` to select fixed registered runs. All arms and laws are
listed in `registration.json`. Existing output is restored only when settings,
source identities and saved streams agree. Verify batching and nonzero-step
restoration before training. These commands do not select checkpoints by score.
