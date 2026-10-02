# Public scientific registration

This is a public projection. Complete numerical settings, source identities and registered criteria are recorded in `registration_build_v4.json`.

## r13: mechanisms of prediction error and sums erosion


Use the version names consistently:

- **records → prediction**
- **records+sums → prediction**
- **records → prediction+sums**

### Common design

Use r12’s original records game, law, uniform board sampler and history coverage:

- 128 untruncated nine-round natural episodes per update; prediction loss at every round.
- 128 coverage prefixes: eight per L/H × N¹–N⁸ stratum; prediction loss only at the endpoint.
- Prediction loss is half natural-position mean and half coverage-endpoint mean.
- Sums loss, where present, has coefficient one and is averaged over active rounds and all five slots.
- AdamW: lr 0.003, wd 0.01; fp32; batch 256; seeds 0–2; fixed 20k endpoint.
- Paired initialization, records, category streams and sampled targets within each comparison. Retain target draws even when an arm uses probability targets, so streams remain identical.
- Mode and exact probability rows are used only to construct loss targets and audits, never as network inputs.

Reuse r12’s panels, deciding functions and thresholds: KL ≤0.01 bits, law/swap TV ≤0.02, witness recovery ≥0.8, and the registered rendering criterion. N³–N⁸ is the **long panel**, not unseen-length extrapolation.

At each scheduled audit—0/1k/2k/5k/10k/15k/20k—report:

- All prediction criteria, continuous values and first audited crossing.
- Census by every slot-1 sum, all four fixed renderings and saved r9 cases.
- Cutoff band **11–13 and 23–25** versus its complement: boards, errors, error rates and predictive TV. These are counts and rates, not interchangeable.
- Sums-head per-slot/vector accuracy and slot-1 category errors.
- Joint A-head/B-signature errors.
- Raw/upper probes, where specified, with untrained baselines, paired CIs, coverage and convergence.
- Prefix diagnosis and clear-neutral hold results, preserving concurrent findings.

The census reads prediction signatures; it does not read the sums head.

## 1. Early erosion mechanism

**Question:** Does Adam normalization explain rapid erosion through the straight-through sums route?

Start from the same exact sums checkpoint used in r11 erosion. Reproduce the **r11 erosion setting**, including its original sampler, for this short experiment. This preserves the phenomenon being diagnosed; it is not a new full prediction study.

Use the same fresh prediction network and stream within each seed. Run **200 updates**, with direct width-one execution:

| Condition | Sums-network update | Other parameters |
|---|---|---|
| Ordinary AdamW | lr 0.003, ε=10⁻⁸, wd 0.01 | Ordinary AdamW |
| Reduced sums lr | AdamW lr 0.0003; otherwise identical | Unchanged AdamW |
| Movement-matched SGD | SGD, momentum zero | Unchanged AdamW |
| Prediction-gradient blocked | Block prediction gradient into sums network; retain AdamW decay | Unchanged AdamW |

For SGD, choose its fixed learning rate from the common **first batch**, before observing accuracy: match the norm of its sums-network gradient displacement to the ordinary AdamW first displacement, excluding decay. Apply the same first-arm decay multiplier to the SGD sums parameters; record this explicitly. This isolates update direction and normalization better than arbitrary small SGD steps. Do not retune the rate.

Record at every update:

- Per-tensor gradient norms and fractions with `|g|=0`, `|g|≤ε`, `ε<|g|≤10ε`, and `|g|>10ε`.
- Actual parameter displacement, gradient displacement and decay displacement.
- Cumulative path length and displacement from initialization, globally and by tensor.
- True-answer versus strongest-alternative margins.
- First answer flips, their histories, margins and preceding gradient/displacement.
- Exact sums accuracy on the 1,555 local histories and completed boards.

Compare accuracy against both update number and cumulative sums-parameter path length. Compare movement curves only over their observed common range; do not extrapolate or train further to manufacture a match.

**Interpretation:** slower erosion per update but similar erosion per movement supports Adam amplification of speed. Better SGD preservation at comparable movement supports a directional contribution. Similar damage across optimizers weakens Adam-specific attribution and supports destructive prediction gradients or vulnerable margins. Erosion under the blocked-gradient condition points to decay or an implementation defect.

**Calibration:** update zero must be exact; zero-update replay must preserve parameters and answers; a planted logit perturbation must cause detected flips; measured first AdamW displacement must agree with the ordinary optimizer equation. The blocked-gradient condition is a measured decay floor, not assumed invariant.

No scientific futility stop in this fixed 200-update replay. Abort only on failed initial exactness, nonfinite values or broken pairing. **12 short runs.**

## 2. Category-sampling noise

Run the factorial comparison:

| Version | Prediction target |
|---|---|
| records → prediction | Sampled category |
| records → prediction | Exact probability row |
| records → prediction+sums | Sampled category |
| records → prediction+sums | Exact probability row |

Use `−Σc p(c) log q(c)` for probability-target cross-entropy. Preserve histories, prediction masks and half/half normalization exactly. Sums supervision is unchanged.

Record excess loss relative to each target’s measured oracle floor, rather than comparing raw stochastic training losses. Add shared-encoder gradient measurements on fixed audit batches:

- Separate prediction and sums gradients.
- Their norms and cosine.
- Each gradient’s first-order directional effect on the other loss.

These measurements require sums labels for audit calculations even in prediction-only arms; they never enter their optimizer.

**Interpretation:** probability targets improving both versions supports target noise as a contributor to fluctuations and residual error. A sums-loss disadvantage that survives probability targets refutes noise as its sufficient explanation. Conflicting shared gradients support interference, but cosine alone does not establish cumulative damage. Little improvement weakens noise’s ranking.

**12 full runs.** The two sampled conditions are fresh r13 baselines, not historical r12 substitutes.

## 3. Access versus interference

Use each seed’s **fixed r12 A-target 20k checkpoint**, selected by endpoint rather than accuracy. Load its raw encoder and sums head identically into every condition. Initialize the upper network identically.

Run three **records → prediction+sums** conditions:

1. **Disconnected:** live sums head receives sums loss; prediction receives only raw state.
2. **Connected, frozen supplier:** prediction also receives hard sums from a frozen copy of that checkpoint.
3. **Connected, trainable supplier:** prediction receives hard sums from the live sums head, with the declared straight-through gradient.

All three retain the same trainable raw encoder, live sums head and prediction-plus-sums losses. Instantiate the frozen supplier in all three; use it only in condition 2. Freeze **that copy**, not the common raw route.

Add **records+sums → prediction**, using exact frozen A answers, with the same initial raw encoder and upper network. It has no sums loss; this reference therefore differs explicitly in supervision as well as supplier accuracy.

Use hard answers of the same width in all supplied conditions. Mask the sums route in the disconnected condition. Execute these runs at width one.

Measure supplier accuracy separately from live-head accuracy, including supplier rerendering errors. Record prediction/sums gradient conflict as in experiment 2 and the prediction-gradient norm through the live sums route.

**Interpretation:**

- Frozen connection improves prediction while its supplier remains unchanged: supports an access contribution.
- Frozen connection outperforms trainable connection while the live sums output deteriorates or gradients conflict: supports supplier instability/interference.
- Both connections improve similarly: access matters more than freezing under these conditions.
- Neither connection improves, but exact sums do: supplier error remains a candidate.
- Exact sums also fail: downstream recurrence/readout remains a limitation.

This comparison does not uniquely identify an abstract internal A layer; records and sums retain their deterministic overlap.

**12 full runs**, including the exact reference.

## 4. Encoding and measured geometry

Reuse experiment 3’s exact one-hot reference. Add **records+sums → prediction** with numerical encoding.

For each slot, supply a 36-vector:

- One-hot: the exact answer vocabulary.
- Numerical: `(s/36, 1−s/36, 0,…,0)`, where `s` is the sum in twelfths.

Preserve the answer projection, interface width, raw route, initialization and downstream architecture. The normalized scale is fixed before training. Do not rescale based on results.

Add equal-law controls for these two encodings only: they test whether encoding creates irrelevant predictive dependence.

On saved experiment-2 raw-only states at 0/5k/20k, measure neighbouring-sum geometry:

- Pair legal boards with identical slots 2–5 and differing slot-1 sums.
- Report every supported adjacent pair, especially 12/13 and 23/24.
- Compare with supported nonadjacent pairs of separation ≥4.
- Separate between-board distances from same-board rerendering distances.
- Report normalized Euclidean distances and held-out discrimination accuracy; fit normalization/readers on probe-training boards only.
- Use fixed pairs and label permutations selected before reading states. Report missing support.

**Interpretation:** numerical encoding succeeding weakens continuous encoding as a sufficient explanation. A consistent one-hot advantage supports encoding sensitivity, not a precision ceiling. Close neighbouring raw states support the geometry hypothesis only if separation is small relative to rendering variation and held-out discrimination is impaired. Proximity alone does not establish causal error.

**Nine additional full runs:** three original-law numerical runs plus six equal-law encoding controls. The three original-law one-hot runs are shared with experiment 3.

## Calibration and stopping

For every deciding bar, run the **same deciding function** on a measured positive and floor:

| Measurement | Positive | Floor/negative |
|---|---|---|
| Prediction criteria and signatures | Executed exact-mode oracle | Board-only predictor and untrained network |
| Sums accuracy and margins | Executed exact A | Untrained head; majority predictor |
| Probe gains | Exact-A carrier | Untrained carrier, majority and shuffled labels |
| Gradient/movement measurements | Analytic first-step optimizer calculation | Zero-gradient replay |
| Geometry/discrimination | Ordered exact numerical carrier | Label permutation; one-hot carrier as a non-ordered comparison |
| Rendering and recurrence diagnosis | Exact oracle | Planted board error and planted delayed drift |
| Supplier-gradient access | Connected straight-through reference | Detached supplier |

A failed or empty calibration blocks its associated conclusion. Do not demand that one-hot distances exhibit numerical ordering.

For full runs, apply r12’s **5k futility rule**: less than 10% closure of both prediction-loss and natural-KL gaps, with no supervised sums improvement where applicable. Use the preceding 100 prediction losses and the correct measured target floor; exclude sums loss.

The **first-hour read** must show pairing, 160k projected endpoints per stratum, target normalization, frozen supplier immobility, live-route gradients, update-zero checkpoint fidelity, initial erosion trajectories and the available 1k prediction curves. It is a sanity read, not checkpoint selection.

## Execution, files and outputs

Total: **33 full runs plus 12 short replays**. Equal-law runs are controls only.

Use **selected GPU, fp32, at most three single-core processes**. Set all numerical CPU thread limits to one. Linear probes run on CPU. Width three for experiment 2; width one for erosion and all hard-answer supplied/connected conditions. Verify batching and nonzero-step restoration before production.

At r12’s rate, the full study represents approximately **11–22 hours of serial training execution**, plus full audits. With three processes sharing selected GPU, budget **roughly 8–16 hours elapsed**, revised from the measured first-hour rates. Avoid repeating exhaustive probes at every audit: use 0/5k/20k; keep inexpensive prediction and census learning curves at every registered audit.

implementation’s files:

- `src/recombination_promotion/oldgame_ext/multiround_mechanism.py`
- `scripts/oldgame_multiround_mechanism.py`
- `tests/test_oldgame_multiround_mechanism.py`
- `reports/phase11/oldgame_memory/multiround/study_r13_mechanism/`

Bulk: `bulk/study_r13_mechanism_bulk/`.

Keep compact registration, calibration, comparisons and references in the repository. Put checkpoints, optimizer/stream states, per-update erosion records, detailed audits, geometry arrays and detailed aggregates in bulk. Report the four experiments separately, with measured positives/floors, learning curves and the corresponding outcome interpretation.
