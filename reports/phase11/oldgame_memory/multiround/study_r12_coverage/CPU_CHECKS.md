# r12 CPU build checks

## Diagnostic corrections after analysis's build review

The following checks supersede the diagnostic rules and identities of the earlier
build below. Training, thresholds and endpoint settings are unchanged. All new
execution used CPU, one thread per process, with no GPU run or study launch.

- Earliest incorrect constituent signatures are recorded through the first sequence
  violation, distinguishing preceding, coincident and no observed constituent error.
- A recurrence reading requires an actual TV violation above 0.02, correct constituent
  responses through the failure, and valid anchor responses. Passing sequence tests
  do not explain a failure of another B criterion: the selected failure reading is
  `Cause unresolved`. Empty diagnostic panels are refused.
- Both the diagnostic and aggregate selection functions were calibrated. These are
  descriptive associations, not unique causal explanations.

| Original-law control | No deviation | Board-associated failure | Recurrence-associated failure | Maximum prefix TV |
|---|---|---|---|---|
| Record-derived exact oracle | 18 | 0 | 0 | 0 |
| Planted board error | 10 | 8 | 0 | 0.25 |
| Planted delayed mode drift | 6 | 0 | 12 | 0.25 |

Under the equal law all three controls have 18 no-deviation cases; maximum TV is
2.98e-8. With no sequence violation the failure-selection function makes no recurrence
attribution. All original B, census, probe, sampling and nonempty-unseen calibrations
still pass. Full calibration elapsed time: **101.68 s**.

- Full `tests/test_oldgame_multiround*.py`: **116 passed in 242.45 s**, no skips;
  command elapsed **244.13 s**. Includes aggregate selection, chronology, empty-panel
  refusal, calibration and hash-bound verification regressions.
- CPU verification: **PASS**, **17.72 s**, eight updates at widths 3 and 1;
  all parameter and optimizer differences are zero. Restoration from update 3,
  streams, exposures and stratum/target counts are exact. The output binds the
  current registration and source hashes.
- `ruff check --select F,E9`: passed on the coverage script, module and tests.
- `git diff --check` and whitespace checks for the untracked changed files: passed.

Current registration SHA-256:
`e44f53554ca19e98a85b419bee72bfeb4c4fcc9aeb1cd336802858df926fdb00`.

Current calibration SHA-256:
`a30df0768b2ced3a935c7d9e88f844fae3bdb8a41cb9827edc01a2a511e3e267`.

CPU verification SHA-256:
`5bc0f237f69db9966707cd239cc75242b30a7e82fa6011800d083c6f17c5daf3`.

Earlier registration, calibration, CPU verification and aggregate files are retained
as `*_build_v1`. The earlier host `verification_cuda.json` is byte-identical (SHA-256
`b729b015c33763f6cb44c5c688531492e0cced4c7e112ee072afb22182e47374`).
It does not verify the refreshed sources. `HOST_COMMANDS.md` writes the new host
verification to `verification_cuda_fixfirst.json`; the five production commands are
unchanged. The refreshed repository aggregate has zero production runs.

## Earlier build evidence (retained)

No GPU run or study launch was performed. The registered 20,000-update endpoints are
not available. CPU smoke results are reduced diagnostic evidence, not study endpoints.
The r11 sources and recorded runs are unchanged.

## Executed checks

- `tests/test_oldgame_multiround*.py`: **102 passed in 230.61 s**, no skips.
  Command elapsed time: 232.33 s. This includes 15 new coverage tests.
- `ruff check --select F,E9` on the three new Python files: passed.
- `git diff --check`, plus untracked-file whitespace checks: passed.
- Traced CPU equivalence: passed at widths three (rarity and A-target) and one
  (A-supplied); zero parameter and optimizer-moment differences against independent
  execution and ordinary AdamW. Restoration from update three is exact, including
  random streams, complete exposures and stratum/target counts. Elapsed: 18.97 s.
- Final calibration elapsed: 86.00 s. Both exact record-derived B oracles pass all
  registered bars; the original-law current-board null and untrained model fail.
  The equal-law current-board null passes its law-aware bars. Inactive routes have
  zero effect. Oracle census errors are zero across four renderings and saved r9 cases.
- Lowest exact-A oracle probe accuracy: **0.998046875**; no unconverged positive fit
  is admitted. Majority and shuffled floors and untrained probes are retained.
- Tracked unseen calibration positions: **42,067 original**, **43,949 equal**.
- Sampling calibration: 128 updates give **1,024 endpoints in every stratum**.
  Uniform conditional-frequency maximum errors are 0.0302734375 (original) and
  0.0400390625 (equal), against the independently specified law. Categories and
  sums are reconstructed from executed records; paired targets are exact.
- Frozen A: **1,555/1,555 local histories** and **24,435/24,435 board vectors**.

## Smoke at update 200

Outputs: `build/oldgame_ext/r12_smoke_cpu/`.
Every run has **1,600 endpoints per stratum** and **371,200 active renderings**.
Rarity was interrupted after update 100 and restored for updates 101–200. Both the
direct continuation tests and grouped restoration checks also compare uninterrupted
and resumed parameters exactly. All nine smoke runs remain **B-incomplete**.

| Arm | Seed | B loss (nats, last 100 updates) | Natural KL bits | Coverage endpoint KL bits | Maximum law TV | A vector correct / 128 |
|---|---|---|---|---|---|---|
| Uniform | 0 | 1.0541201 | 0.0156422 | 0.0229531 | 0.1852864 | 0/128 |
| Cutoff | 0 | 1.0586732 | 0.0210422 | 0.0330613 | 0.1576975 | 0/128 |
| Decoy | 0 | 1.0539262 | 0.0167652 | 0.0224383 | 0.1609847 | 0/128 |
| A-target | 0 | 1.0711309 | 0.0276708 | 0.0605414 | 0.2601663 | 0/128 |
| A-target | 1 | 1.0648986 | 0.0339065 | 0.0377854 | 0.2491583 | 0/128 |
| A-target | 2 | 1.0647711 | 0.0274357 | 0.0462101 | 0.2207594 | 0/128 |
| A-supplied | 0 | 1.0449887 | 0.00728655 | 0.00828052 | 0.0843463 | 128/128 |
| A-supplied | 1 | 1.0493707 | 0.00610006 | 0.00837968 | 0.0945429 | 128/128 |
| A-supplied | 2 | 1.0462089 | 0.00788556 | 0.00757030 | 0.0613058 | 128/128 |

| Execution group | Width | Updates/s (training only) | Audit time | Peak resident memory |
|---|---|---|---|---|
| Rarity, resumed 100-update segment | 3 | 12.08 | 55.47 s for three endpoint audits | 909.0 MiB |
| A-target, 200 updates | 3 | 10.35 | 105.23 s for six audits | 932.1 MiB |
| A-supplied, seeds 0–2 | 1 | 15.06–19.11 | 41.76–46.53 s for two audits per run | 805.3–831.0 MiB |

Each process used one CPU thread; training excludes preview and audit work in these
rates. CPU command elapsed times: rarity 146.54 + 73.09 s, A-target 137.95 s,
A-supplied 192.46 s. Groups ran concurrently. No GPU memory or GPU time has been
measured; the host verification and smoke remain required.

The smoke aggregate contains census, exact A counts, short/extrapolation law panels,
route damage, every audit's A-head/B-signature decomposition, reduced probe fitting
records, exposures, and worst-prefix/clear-neutral diagnoses. Its selected reading
explicitly excludes smoke evidence. The repository aggregate retains the registration
and reports that study endpoints are not yet available.

## Authority identities

Registration SHA-256:
`f1130c00b84265658420a03ec3d5dde0a79274c5e939d9e4eec5954088222410`.

Calibration SHA-256:
`019293e7f1ef6c6d6abf3f19ad6469cfdc41fc1669d20453b50e43c3de0b6d04`.

Frozen A checkpoint SHA-256:
`0d14e7a2b63459d9e6c392d57d55cca02059ca0131f6225f18fafa2a3d38b5b9`.

An initial calibration was rebuilt after adding the explicit untrained census
floor and independent record-derived sampler check. Its recoverable preliminary
files are under `build/r12_initial_calibration_w2mA1U/`.

Exact host commands are in [HOST_COMMANDS.md](HOST_COMMANDS.md). Production bulk
storage defaults to `bulk/study_r12_coverage_bulk/`; the CPU
smoke used a writable temporary override. No commits were made.
