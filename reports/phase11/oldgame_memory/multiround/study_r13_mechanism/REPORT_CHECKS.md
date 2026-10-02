# r13 report-revision checks

No training or GPU execution. All 45 saved runs, endpoint labels, registered readings and thresholds are preserved. Registration SHA-256 remains `b0876ea3cc9fd03831e4406a6f33f8650b54df7cd2294e446308b2c034bc8411`.

- Full affected suite: `tests/test_oldgame_multiround*.py`, 172 passed in 460.43 seconds; no skips. One pre-existing observational tensor-conversion warning in the erosion test.
- Report-specific tests: 11 passed in 7.27 seconds.
- Ruff, `--select F,E9`: clean on the four changed Python files.
- `git diff --check`: clean. No commits.
- All staged detail checksums pass `sha256sum -c SHA256SUMS`.

The supplementary panel was bound before state capture: SHA-256 `7d85caac9a1240e6ce21176bed1f1bec2256a109d456e2f6b4b9b7cf06d8137c`. Capture and fixed reader scoring took 10.949 seconds on one CPU thread. All 18 saved checkpoints (six raw-only runs, updates 0/5k/20k) were checked against their saved hashes and authorities. Panel support: 12/13 = 135 fitting and 150 evaluation pairs; 23/24 = 12 fitting and 13 evaluation pairs. At 20k:

| Seed | Sampled 12/13 | Sampled 23/24 | Probability 12/13 | Probability 23/24 |
|---|---|---|---|---|
| 0 | 295/300, fail | 26/26, pass | 300/300, pass | 26/26, pass |
| 1 | 298/300, pass | 25/26, fail | 300/300, pass | 26/26, pass |
| 2 | 293/300, fail | 26/26, pass | 300/300, pass | 26/26, pass |

Pass here means the unchanged calibrated discrimination decision, including convergence and log-loss separation; it does not mean B closure. The original geometry's 19 measured and 578 missing-support rows are retained at every scheduled geometry checkpoint.

Erosion's three-active-arm common path upper limits are 2.505703, 2.447836 and 2.544091 for seeds 0–2. AdamW–SGD upper limits are 11.423875, 10.210289 and 20.513627. Blocked is excluded and reported separately. All active arms first lose exactness at update 1. Recorded points, without accuracy interpolation, are bound in the detailed JSON.

Compact report sizes: Markdown approximately 138 KB; JSON approximately 982 KB. No ordinary file above 1 MB remains in the repository study directory. Earlier reports and new details are recoverably staged outside the repository; the exact host copy and verification commands are in REPORT_COMMANDS.md.
