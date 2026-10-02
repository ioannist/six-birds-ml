# r10 amended calibration

Pre-launch calibration passes. This is not a trained-network internal-use
result: each seed still needs its fixed update-20,000 a_forced positive and
its evaluated network's supported shuffled-alignment negative.

Calibration completed on CPU in 115.45 seconds. All ten essential checks
and all five deciding pre-launch use checks pass. The executed oracle
passes B under both laws; the original-law mode-blind and untrained networks
fail, while the equal-law mode-blind predictor passes. Oracle readability
passes the registered 0.99 bar. Equal-law interventions have zero prediction
effect. The untrained conditional donor-follow result is descriptive only:
accurate-pair supports are 0, 0, 1, 0, 0, hence unsupported in all slots.

Every condition uses the identical registered 1,024 distinct pairs per slot.
Eligible populations are 2,695 / 2,724 / 2,765 / 2,665 / 2,687. The pair
list was selected without predictions; it is not resampled. Per-pair
predictions, both endpoint values, per-value coverage, denominators and
Wilson 95% intervals are saved in calibration.json.

| Slot | Hard-answer positive | Rotated positive | No-op negative | Shuffled negative | Shuffled 95% interval | Deciding other-slot changes |
|---|---|---|---|---|---|---|
| 0 | 1024/1024 | 1024/1024 | 0/1024 | 115/1024 | [0.09440, 0.13311] | 0 |
| 1 | 1024/1024 | 1024/1024 | 0/1024 | 55/1024 | [0.04150, 0.06926] | 0 |
| 2 | 1024/1024 | 1024/1024 | 0/1024 | 0/1024 | [0, 0.00374] | 0 |
| 3 | 1024/1024 | 1024/1024 | 0/1024 | 186/1024 | [0.15923, 0.20643] | 0 |
| 4 | 1024/1024 | 1024/1024 | 0/1024 | 186/1024 | [0.15923, 0.20643] | 0 |

Each positive's interval is [0.99626, 1]. Each no-op interval is
[0, 0.00374]. The registered bars compare point estimates; intervals are
reported without changing those bars.

Oracle semantic integrity uses the known inverse rotation and nearest
prototype. Donor-slot errors and other-slot errors are zero on every pair.
Maximum coordinate reconstruction error is 9.894e-8; the smallest positive
decision margin exceeds 0.264879. These reconstruction values do not excuse
any decoded disagreement.

The independent affine least-squares reader is fitted on training boards
only, in float64, separately from alignment. It maps the complete 16-vector
to 15 oracle coordinates, with relative rank cutoff 1e-7 and then nearest
prototype decoding. The oracle fit has rank 16 and rotated training RMSE
1.426e-8. It reports zero other-slot changes for both positives and the
no-op. The planted contamination produces 949 / 950 / 926 / 968 / 959
other-slot changes and is detected in every slot.

Supplementary logistic decoding still changes other slots: 3 / 4 / 5 / 5 / 3
for the rotated oracle, and 3 / 5 / 3 / 4 / 1 for the hard-answer oracle.
Those results are retained as sensitivity measurements, not substituted
for the amended deciding reader.

The unchanged earlier 64-pair files are registration_pairs64.json/md and
calibration_pairs64.json. Their hashes remain 07cf5c2c… and c0f3be62….
The amended file hashes are:

- registration.json: `2f4ade1845e7d684503bc7dbb8859f7d899c9d574a6301d701554597a85f92bc`
- calibration.json: `ae5db2a582caeea2ca855f8dbdd084e43ed036de09c180b4d5fb715e28ef3ac6`
- interchange_pairs.json: `100f1807021218a359ac0d5668439b472e7456a009580b020bb618bdbd3609c9`
