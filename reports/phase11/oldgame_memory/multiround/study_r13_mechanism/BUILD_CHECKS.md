# r13 checks

## FIX FIRST: futility and the separate geometry amendment

The optimizer code and fixed endpoints are unchanged. Futility now uses
`E0 = B0 - F0` and the last-100 mean of the recorded per-batch
`excess_prediction_loss`. Its closure is `(E0 - Et) / E0`. A nonpositive `E0`
makes this criterion unavailable and cannot cause a stop. The natural-KL
condition and supervised-sums exception are retained.

The corrected training registration/calibration are separate from
`geometry_amendment.json` / `geometry_calibration.json`. Replaying the analysis
registration and calibration left both training hashes unchanged. The previous
training records remain byte-identical as `registration_build_v7.json` and
`calibration_build_v7.json`. All earlier smoke records below retain their
original authority, not the corrected authority.

Geometry now uses the same pair-discrimination scorer in calibration and
`geometry_audit`, with training-only standardization and disjoint identities.
The positive uses 16 legal 12/13 board pairs for fitting and eight different
pairs for scoring, selected by board ID before features are read. There are
285 eligible legal pairs. The negative labels are exactly class balanced
within each repeated training encoding; no permutation search is performed.

| Pair calibration | Correct / held-out endpoints | Cross-entropy (nats) | Converged |
|---|---:|---:|---|
| Ordered numerical positive | 16/16 | 0.004271194 | Yes |
| Balanced constant carrier | 8/16 | 0.693147302 | Yes |
| Class-balanced repeated encoding | 8/16 | 0.693147302 | Yes |
| One-hot comparison | 16/16 | 0.004271194 | Yes |

The analysis retains the accuracy bars (positive at least 0.99; negatives below
0.8), requires convergence, and declares a minimum **0.1-nat** held-out
cross-entropy separation. The measured separation is 0.688876107 nats.
Both negative values agree with accuracy 0.5 and log-loss `ln(2)` to within
1e-6. Geometry is therefore **unblocked for analysis**, not established as a
causal explanation. Distances remain descriptive.

The original fixed permutation result remains in
`geometry_failure_build_v1.json`, with the original calibration and detailed
prediction hashes. Its 72/72 accuracy and failed original calibration are
preserved; its saved cross-entropy is 0.674954414 nats. It is not treated as
evidence of contamination or replaced by the repaired controls.

A read-only analysis of the earlier raw-sampled seed-0 CPU smoke at update 200
records cross-entropy in all 19 supported sum-pair rows; 578 rows lack support,
and seven pass the discrimination bars. This is not a 20k study result.
The record is `build/oldgame_ext/r13_futility_v2_bulk/earlier_smoke_geometry/geometry.json`,
SHA-256 `a22aee2a5c7e79e128ec4c840a0749805511032aa4be221c96783a63604f1009`.

Executed checks:

- Full affected suite: **160 passed**, no skips, one observational warning,
  in **454.46 seconds** (`PYTHONPATH=src`, `tests/test_oldgame_multiround*.py`).
- Final r13 test file, including the additional real-batch oracle check:
  **22 passed**, one observational warning, in **37.17 seconds**. Only sampled
  targets change in that check; oracle excess remains zero and cannot stop.
- Training calibration: **146.02 seconds**; all training checks pass, including
  floor-only variation, nonpositive initial excess and the sums exception.
- Ruff F/E9 and whitespace checks pass. No GPU runs, launches or commits.

Current SHA-256 identities:

- Training registration: `b0876ea3cc9fd03831e4406a6f33f8650b54df7cd2294e446308b2c034bc8411`.
- Training calibration: `9e6b63b539ba13a42c522d0cae71b80587453d069589504f58b59116d89028b5`.
- Geometry amendment: `2a6decfe1afeba8a33f4eca7999c47c68366a65c6eed7ca496767f365c690228`.
- Geometry calibration: `7720bd25584ae0df50a6b411ee0bc8afa3d8e638dddc0d68a572a69b53d4f965`.

`HOST_COMMANDS.md` uses fresh smoke/verification paths and documents the
independent geometry stages. The repository aggregate has no study endpoints;
it binds the geometry amendment separately and keeps the readings verbatim.

## Earlier build record (prior authority)

No GPU runs or study runs were launched. The four experiments are registered
separately, with analysis's specification and readings copied verbatim before the
CPU smoke. The manifest contains 33 full runs and 12 short erosion replays.
The original r8–r12 instruments and r10 files are unchanged.

## Implementation

- `src/recombination_promotion/oldgame_ext/multiround_mechanism.py`: condition
  definitions, paired models, hard supplied answers, numerical encoding,
  probability-target loss, gradient diagnostics and fixed geometry pairs.
- `scripts/oldgame_multiround_mechanism.py`: registration, calibration,
  direct-width-one and width-three training, restoration, per-update erosion,
  audits, verification and the four separate aggregate sections.
- `tests/test_oldgame_multiround_mechanism.py`: 18 checks covering pairing,
  normalization, optimizer scope, first-batch SGD, frozen suppliers, live
  gradients, encoding, fixed geometry, calibration exclusions and restoration.
- `HOST_COMMANDS.md`: GPU verification, the 1k smoke, three pinned study
  processes and the aggregate command. These commands have not been executed.

All training and evaluation are float32. The linear readers reuse the existing
one-thread CPU implementation; the MLP readers use the selected device. The
blocked erosion condition keeps zero Adam moments and explicit decay. The SGD
rate is fixed from the common first batch, excluding decay; its decay multiplier
is 0.99997. Geometry is descriptive, never a causal criterion.

## Calibration

The final CPU calibration took 141.42 seconds. The actual prediction, census,
unseen and diagnosis functions were exercised, including nonempty unseen sets.

| Check | Measured result |
|---|---|
| Original-law executed oracle | All six prediction bars pass; natural KL 0 bits, maximum law TV 0; 42,067 unseen positions |
| Original-law board-only floor | Fails natural/unseen KL, witness, law and swaps; natural KL 0.0135139165 bits; law TV 0.187500015 |
| Equal-law oracle and board-only control | Both pass the law-aware bars; maximum TV 2.98e-8 |
| Exact frozen A | 1,555/1,555 local histories; 24,435/24,435 complete boards |
| Exact-A readers | Minimum accuracy 511/512 = 0.998046875 |
| Full oracle census | Per rendering: 930 cutoff-band boards and 23,505 complement boards; zero errors across four renderings |
| Untrained original-law census | 24,435/24,435 registered-rendering boards fail the signature bar |
| Analytic first Adam step | Maximum discrepancy 0; zero-gradient decay displacement 6.864347e-5 |
| Supplier access | Connected prediction-gradient norm 0.0001468421; detached supplier 0 |
| Diagnosis | Exact oracle, planted board error and delayed drift give distinct intended readings |

**Geometry calibration failed.** The ordered numerical reader scored 72/72,
but its fixed shuffled-label negative also scored 72/72. The one-hot reader
scored 72/72 and its shuffled floor 40/72. The fixed pairs, labels and seeds
were retained. `checks.geometry` is false, and geometry conclusions are
`BLOCKED_FAILED_CALIBRATION`. This is not an all-calibration pass and must not
be interpreted as one. No resampling or threshold change was used.

The tiny negative equal-law KL (-8.60e-8 bits) is float32 roundoff around zero.
Detailed positives, floors, predictions and deciding-function outputs are
hash-bound from `calibration.json`.

## CPU smoke

The final smoke contains 23 runs at 200 updates: every condition at least once,
with all three seeds in each noise condition. Each full-run condition retains
1,600 endpoints per L/H × N1–N8 stratum, projecting to the registered 160,000
per stratum at 20k. Within each seed and law, the final rolling stream hash is
identical across conditions. Census and reader panels are explicitly reduced;
the prediction panels and thresholds are unchanged. These are not 20k endpoints.

Noise entries below are prediction training loss in nats / natural KL in bits.

| Condition | Seed 0 | Seed 1 | Seed 2 |
|---|---|---|---|
| Records, sampled | 1.054120 / 0.015642 | 1.059011 / 0.021402 | 1.056883 / 0.023426 |
| Records, probability | 1.042690 / 0.003767 | 1.042760 / 0.003476 | 1.043705 / 0.004498 |
| Records + sums loss, sampled | 1.071131 / 0.027671 | 1.064899 / 0.033907 | 1.064771 / 0.027436 |
| Records + sums loss, probability | 1.061754 / 0.031371 | 1.058423 / 0.024828 | 1.059018 / 0.028882 |

| Seed-0 condition | Prediction loss (nats) | Natural KL (bits) |
|---|---:|---:|
| Disconnected | 1.053943 | 0.022990 |
| Frozen supplier | 1.045354 | 0.007202 |
| Live supplier | 1.045351 | 0.007417 |
| Exact A, one-hot | 1.045277 | 0.006502 |
| Exact A, numerical | 1.052601 | 0.020254 |
| Equal law, one-hot | 1.082958 | 0.000988 |
| Equal law, numerical | 1.082943 | 0.000961 |

Every non-erosion smoke still fails at least one prediction bar. Equal-law rows
remain controls only. Of 156 linear-reader fits in the reduced smoke audits,
122 converged; non-converged fits cannot support a readability gain.

| Seed-0 erosion condition | Correct local sums at update 200 / 1,555 | Cumulative parameter path |
|---|---:|---:|
| Ordinary AdamW | 123 | 18.718461 |
| Reduced sums rate | 489 | 2.708869 |
| Movement-matched SGD | 17 | 27.974886 |
| Prediction gradient blocked | 1,555 | 0.219588 |

The SGD rate is 48.72925567626953, fixed before observing accuracy. All four
erosion runs restored at update 100, preserving per-update observations; live
access also restored at update 100. Compare optimizer trajectories only over
their common observed movement range, not from these endpoint counts alone.

Width-three training measured 6.6–8.4 group updates/s. Direct-width-one training
measured 11.5–19.0 updates/s. Reduced audits took about 30–36 seconds per model.
Peak recorded resident memory was 950–975 MiB per process. Each process used one
numerical CPU thread, with no more than three processes active. GPU timings and
memory remain unmeasured and require the host smoke.

## Tests and continuation verification

```text
PYTHONPATH=src:. python -m pytest tests/test_oldgame_multiround*.py -q
157 passed, 1 warning in 444.65s (0:07:24)
```

No skips. The warning is an observational tensor-to-scalar conversion in the
erosion displacement record; it does not enter the training loss.
`ruff check --select F,E9` passed on all three new Python files;
`git diff --check` passed.

The standalone CPU `verify-gpu --trace` stage passed width three and direct
width one against independent runs and ordinary AdamW. Maximum parameter
difference was zero; restoration from update 3 was exact, including optimizer,
stream and exposure state. The host check declares parameter/moment tolerances
`atol=rtol=3e-5`; discrete state must be exact.

## Records and identities

- Registration SHA-256: `73caba4ab7a26479881f206e2118f68ae764af9f58b0c9ab3352b3cfb4178b8f`.
- Calibration SHA-256: `06303c07bc5b0f75de44c91b51e0cd4d15a45889b94291348b8beeb76f907a6f`.
- Script SHA-256: `5e9490dc33352d9d24e9512d952bbde30fe0487241ed12bc5a969faf5528db43`.
- Module SHA-256: `e2f743496b383339dd63d311e6d1e8d5cb231599913294f7da3d02b434ec876f`.
- Calibration details: `build/oldgame_ext/r13_final_bulk/calibration_details.json`, SHA-256 `2881f8eb576005ab5c422852d3cd34ef64f320f78668471b822c8b7007ef3abe`.
- CPU verification: `build/oldgame_ext/r13_final_bulk/verification/verification_cpu.json`, SHA-256 `d9801991674c7e376b6aaa469e4c120c6efd7aa8635abbb84f237b6fa017fbfd`.
- Smoke aggregate: `build/oldgame_ext/r13_smoke_final/aggregate.json`, SHA-256 `51c16410703e1cebb274bdef4e29625140a72ce8e7d3bb009069f918fade927d`.
- Smoke detailed aggregate: `build/oldgame_ext/r13_smoke_final/bulk/aggregate_details.json`, SHA-256 `903fcbac9e0981ecd73e833e9698257edbd5bc17e0db40803c079b9df24f9736`.

The repository aggregate has no study endpoints and retains all registered
readings verbatim. The smoke aggregate has separate erosion/noise/access/encoding
sections and marks all full-run results as reduced smoke.

The sandbox cannot write the requested `runs/study_r13_mechanism_bulk/` path;
CPU details and checkpoints use the explicit permitted temporary paths above.
Host commands use the prescribed bulk path. Earlier registration/calibration
versions are retained. The two larger earlier calibration-v2 files were moved
recoverably to `build/oldgame_ext/r13_calibration_final_bytes/earlier_calibration/`,
with their original repository names retained as symbolic links. No study data
was deleted. No commit was made.
