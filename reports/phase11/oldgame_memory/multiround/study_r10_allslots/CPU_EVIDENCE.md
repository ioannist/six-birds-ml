# Amended r10 CPU evidence

No GPU run, host process launch, fleet launch or commit was performed.
All execution used float32 with OMP, MKL, OpenBLAS, NumExpr and PyTorch
threads set to one. Production learning settings and pass thresholds are
unchanged.

Registration and calibration were rerun. See calibration_amended.md for
the deciding calibration results. Registration validates against current
source identities and the frozen pair manifest. Earlier 64-pair bytes are
unchanged. Verification_cpu.json binds the new registration and sources:
width-three raw groups and direct width-one hard-A runs agree with independent
runs and ordinary AdamW, maximum parameter difference zero. Restoration
from update 3 preserves parameters, moments, streams and exposures exactly.

The CPU smoke is under
`build/oldgame_ext/r10_smoke_amended/`, with bulk artifacts
in its `bulk/` directory. Seven original-law runs reached update 200.
These reduced audits are diagnostics, not fixed-endpoint study results.

| Arm | Seed | B loss, nats | Natural KL, bits | Group updates/s | Final audit, s | process peak RSS, MiB |
|---|---|---|---|---|---|---|
| free | 0 | 0.940016 | 0.0751154 | 8.493 | 23.870 | 1029.5 |
| free | 1 | 0.940275 | 0.0755175 | 8.493 | 25.032 | 1029.5 |
| free | 2 | 0.940562 | 0.0750912 | 8.493 | 24.882 | 1029.5 |
| free+A | 0 | 0.940999 | 0.0770237 | 7.535 | 26.422 | 1240.8 |
| free+A | 1 | 0.941035 | 0.0762042 | 7.535 | 21.709 | 1240.8 |
| free+A | 2 | 0.941601 | 0.0770660 | 7.535 | 24.843 | 1240.8 |
| a_forced | 0 | 0.936141 | 0.0697847 | 13.699 | 30.222 | 969.2 |

Raw group rates are width-three updates, not per-model updates. Timing was
measured while other CPU checks were running; it is not a GPU estimate.
For resumed arms, rates and peak RSS describe the resumed process.
All forty linear probe fits in each final audit (including shuffled-label
fits) converged. MLP fits use a fixed update budget and have no convergence
claim. The supplied A interface is correct on 3,072/3,072 rounds in each
slot. Trained internal-use calibration is deliberately deferred to 20k.

free+A and a_forced were restarted at update 100. Uninterrupted comparison
runs are under `r10_smoke_amended_reference/`. At update 200, their model
parameters, complete optimizer state, random streams, exposure arrays and
rolling hashes are bit-identical. The smoke aggregate contains seven
`SMOKE_NOT_ENDPOINT` labels, never a calibrated-use endpoint claim.

The full affected test command is:

```bash
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONPATH=src:. TMPDIR="${TMPDIR:-$PWD/build/tmp}" python -m pytest tests/test_oldgame_multiround*.py -q
```

The final run passed all 135 tests in 433.16 seconds, with no skips
(the initial run also passed, in 416.17 seconds).
Ruff F,E9 and tracked/untracked whitespace checks are clean.
HOST_COMMANDS.md provides the GPU verification, amended 1k smoke and the
distribution's five-process execution commands; none were launched here.
