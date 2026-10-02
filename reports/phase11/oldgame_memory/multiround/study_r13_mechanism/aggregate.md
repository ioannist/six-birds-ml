# r13 saved-state analysis

Target noise, access and encoding affect measured errors; none alone guarantees B closure, and erosion is gradient-mediated without being uniquely Adam-specific.

Runs, endpoint labels, thresholds and the training instrument are unchanged. Equal-law runs are controls only. Access benefits and remaining recurrence defects are concurrent findings. Geometry calibration status does not imply discrimination or support in a measured row. Prediction TV errors (>0.02) and categorical misreads are different measurements. Categorical signatures are not defined in the equal-law control; its entries are None. A non-operative supplier is a diagnostic head, not an input route.

## Registered readings (verbatim)

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


## access

| Seed | Condition / law | Label | Failed B bars (values) | Categorical misreads | TV errors | Sums vector | Supplier vector |
|---|---|---|---|---|---|---|---|
| 0 | disconnected / original | INCOMPLETE | law_TV=0.0985001; swaps: neutral_N=0.114353, reset_L=0.195469, same_category_substitution=0.106702, set_H=0.113727, upper_state_exchange_same_N=0.107715 | 331 | 2717 | 21244/24435 | 19269/24435 |
| 1 | disconnected / original | INCOMPLETE | law_TV=0.100162; rerender TV=0.0530202; A differences=0; swaps: neutral_N=0.167326, reset_L=0.24556, same_category_substitution=0.151657, set_H=0.0896762, upper_state_exchange_same_N=0.069009 | 725 | 11908 | 21715/24435 | 20516/24435 |
| 2 | disconnected / original | INCOMPLETE | law_TV=0.0727516; rerender TV=0.0455147; A differences=0; swaps: neutral_N=0.0430348, reset_L=0.256236, same_category_substitution=0.077246, set_H=0.0862463, upper_state_exchange_same_N=0.0319761 | 637 | 2878 | 21545/24435 | 19544/24435 |
| 0 | frozen / original | INCOMPLETE | law_TV=0.242574; rerender TV=0.0103387; A differences=6; swaps: reset_L=0.0233119 | 259 | 469 | 21330/24435 | 19269/24435 |
| 1 | frozen / original | INCOMPLETE | rerender TV=0.0232432; A differences=4; swaps: reset_L=0.136488 | 69 | 440 | 21798/24435 | 20516/24435 |
| 2 | frozen / original | INCOMPLETE | rerender TV=0.00643389; A differences=6; swaps: set_H=0.0232469 | 58 | 61 | 21797/24435 | 19544/24435 |
| 0 | live / original | INCOMPLETE | law_TV=0.246829; rerender TV=0.00693695; A differences=4; swaps: neutral_N=0.0309766, same_category_substitution=0.0243115, set_H=0.0225196, upper_state_exchange_same_N=0.0233948 | 117 | 185 | 21258/24435 | 21258/24435 |
| 1 | live / original | INCOMPLETE | law_TV=0.251278; rerender TV=0.0183447; A differences=8 | 43 | 180 | 21733/24435 | 21733/24435 |
| 2 | live / original | INCOMPLETE | rerender TV=0.00803879; A differences=7 | 39 | 43 | 21768/24435 | 21768/24435 |
| 0 | exact / original | INCOMPLETE | law_TV=0.0227492 | 0 | 38 | 24435/24435 | 24435/24435 |
| 1 | exact / original | INCOMPLETE | swaps: neutral_N=0.0206675 | 0 | 15 | 24435/24435 | 24435/24435 |
| 2 | exact / original | PASS | none | 2 | 24 | 24435/24435 | 24435/24435 |

### access_disconnected_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 163/930 | 168/23505 | 679/930 | 2038/23505 |
| 1 | 177/930 | 166/23505 | 681/930 | 2039/23505 |
| 2 | 177/930 | 159/23505 | 684/930 | 2056/23505 |
| 3 | 185/930 | 164/23505 | 683/930 | 2029/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10252 / 1.03922 | 0.0918108 | 0.253843 | 23999 | 19269/24435 |
| 1000 | 1.0427 / 1.03842 | 0.00686873 | 0.203399 | 3303 | 19442/24435 |
| 2000 | 1.04465 / 1.04169 | 0.00497451 | 0.148299 | 952 | 19407/24435 |
| 5000 | 1.04002 / 1.03861 | 0.00393456 | 0.143231 | 843 | 20156/24435 |
| 10000 | 1.04388 / 1.04253 | 0.00254761 | 0.125499 | 520 | 20612/24435 |
| 15000 | 1.04011 / 1.03906 | 0.00229759 | 0.133918 | 753 | 21006/24435 |
| 20000 | 1.03963 / 1.03876 | 0.00210683 | 0.0985001 | 331 | 21244/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 1, 'recurrence_associated': 0, 'unresolved': 16}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_disconnected_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 478/930 | 247/23505 | 631/930 | 11277/23505 |
| 1 | 474/930 | 260/23505 | 639/930 | 11288/23505 |
| 2 | 476/930 | 258/23505 | 634/930 | 11279/23505 |
| 3 | 483/930 | 257/23505 | 635/930 | 11260/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10064 / 1.03996 | 0.0813587 | 0.264393 | 23690 | 20516/24435 |
| 1000 | 1.04238 / 1.038 | 0.00928463 | 0.182559 | 8784 | 20614/24435 |
| 2000 | 1.04103 / 1.03765 | 0.00591532 | 0.148837 | 3318 | 20715/24435 |
| 5000 | 1.04291 / 1.04095 | 0.00367863 | 0.139385 | 725 | 20972/24435 |
| 10000 | 1.03874 / 1.03737 | 0.00236561 | 0.078219 | 620 | 21307/24435 |
| 15000 | 1.04038 / 1.03919 | 0.00222518 | 0.0752674 | 929 | 21453/24435 |
| 20000 | 1.04213 / 1.04123 | 0.00182522 | 0.100162 | 725 | 21715/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 5, 'recurrence_associated': 0, 'unresolved': 13}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_disconnected_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 388/930 | 249/23505 | 659/930 | 2219/23505 |
| 1 | 377/930 | 227/23505 | 661/930 | 2200/23505 |
| 2 | 388/930 | 255/23505 | 657/930 | 2232/23505 |
| 3 | 380/930 | 238/23505 | 659/930 | 2202/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.11041 / 1.03746 | 0.103285 | 0.276965 | 1945 | 19544/24435 |
| 1000 | 1.04297 / 1.03842 | 0.00865972 | 0.117556 | 2925 | 19684/24435 |
| 2000 | 1.04114 / 1.03792 | 0.00561487 | 0.0946815 | 2096 | 19895/24435 |
| 5000 | 1.04247 / 1.04087 | 0.00336272 | 0.0627843 | 833 | 20412/24435 |
| 10000 | 1.04009 / 1.03777 | 0.00261699 | 0.0430874 | 555 | 20914/24435 |
| 15000 | 1.04178 / 1.04079 | 0.00217971 | 0.0341246 | 670 | 21341/24435 |
| 20000 | 1.04017 / 1.03919 | 0.00204593 | 0.0727516 | 637 | 21545/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 8, 'recurrence_associated': 0, 'unresolved': 9}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_frozen_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 149/930 | 110/23505 | 267/930 | 202/23505 |
| 1 | 148/930 | 117/23505 | 283/930 | 219/23505 |
| 2 | 145/930 | 95/23505 | 271/930 | 176/23505 |
| 3 | 141/930 | 113/23505 | 263/930 | 206/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10021 / 1.03922 | 0.0884734 | 0.249885 | 23883 | 19269/24435 |
| 1000 | 1.03935 / 1.03842 | 0.00129497 | 0.264385 | 255 | 19449/24435 |
| 2000 | 1.0428 / 1.04169 | 0.00149345 | 0.245271 | 648 | 19436/24435 |
| 5000 | 1.03954 / 1.03861 | 0.00135187 | 0.231343 | 275 | 20230/24435 |
| 10000 | 1.04337 / 1.04253 | 0.000740374 | 0.261288 | 316 | 20753/24435 |
| 15000 | 1.03936 / 1.03906 | 0.00110368 | 0.242234 | 237 | 21102/24435 |
| 20000 | 1.03952 / 1.03876 | 0.000621785 | 0.242574 | 259 | 21330/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 2, 'non_deviating': 16, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 2, 'NO_OBSERVED_CONSTITUENT_ERROR': 15, 'NO_SEQUENCE_DEVIATION': 1, 'PRECEDING': 0}.

### access_frozen_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 44/930 | 25/23505 | 257/930 | 183/23505 |
| 1 | 47/930 | 38/23505 | 263/930 | 220/23505 |
| 2 | 58/930 | 26/23505 | 258/930 | 212/23505 |
| 3 | 54/930 | 29/23505 | 256/930 | 210/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.0984 / 1.03996 | 0.0778911 | 0.261107 | 22830 | 20516/24435 |
| 1000 | 1.03882 / 1.038 | 0.00215895 | 0.0472966 | 45 | 20654/24435 |
| 2000 | 1.03809 / 1.03765 | 0.00049927 | 0.0340633 | 44 | 20782/24435 |
| 5000 | 1.04142 / 1.04095 | 0.00034312 | 0.0194753 | 44 | 21053/24435 |
| 10000 | 1.03771 / 1.03737 | 0.000523432 | 0.0179814 | 44 | 21324/24435 |
| 15000 | 1.03945 / 1.03919 | 0.0005232 | 0.0117984 | 44 | 21664/24435 |
| 20000 | 1.04149 / 1.04123 | 0.000548497 | 0.0147473 | 69 | 21798/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_frozen_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 19/930 | 39/23505 | 19/930 | 42/23505 |
| 1 | 19/930 | 47/23505 | 19/930 | 52/23505 |
| 2 | 15/930 | 52/23505 | 15/930 | 59/23505 |
| 3 | 21/930 | 46/23505 | 21/930 | 52/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.11117 / 1.03746 | 0.104708 | 0.272988 | 2034 | 19544/24435 |
| 1000 | 1.03968 / 1.03842 | 0.00129017 | 0.041981 | 58 | 19756/24435 |
| 2000 | 1.03876 / 1.03792 | 0.000660963 | 0.0175718 | 58 | 19963/24435 |
| 5000 | 1.04117 / 1.04087 | 0.000732614 | 0.0195908 | 58 | 20566/24435 |
| 10000 | 1.03796 / 1.03777 | 0.000290471 | 0.012951 | 61 | 21130/24435 |
| 15000 | 1.04093 / 1.04079 | 0.000185377 | 0.00700058 | 58 | 21531/24435 |
| 20000 | 1.03936 / 1.03919 | 0.000340489 | 0.015699 | 58 | 21797/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_live_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 49/930 | 68/23505 | 66/930 | 119/23505 |
| 1 | 49/930 | 74/23505 | 62/930 | 121/23505 |
| 2 | 51/930 | 59/23505 | 65/930 | 112/23505 |
| 3 | 45/930 | 64/23505 | 58/930 | 113/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10021 / 1.03922 | 0.0884734 | 0.249885 | 23883 | 19269/24435 |
| 1000 | 1.03947 / 1.03842 | 0.00139884 | 0.266818 | 317 | 19426/24435 |
| 2000 | 1.04269 / 1.04169 | 0.00120129 | 0.234508 | 441 | 19407/24435 |
| 5000 | 1.03938 / 1.03861 | 0.00160584 | 0.131376 | 309 | 20147/24435 |
| 10000 | 1.04298 / 1.04253 | 0.000610373 | 0.187961 | 150 | 20684/24435 |
| 15000 | 1.03931 / 1.03906 | 0.000760586 | 0.244138 | 125 | 21029/24435 |
| 20000 | 1.03912 / 1.03876 | 0.00031731 | 0.246829 | 117 | 21258/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage', 'Upper recurrence remains a limitation']. Counts: {'board_associated': 2, 'non_deviating': 10, 'recurrence_associated': 2, 'unresolved': 4}; chronology: {'COINCIDENT': 2, 'NO_OBSERVED_CONSTITUENT_ERROR': 16, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_live_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 22/930 | 21/23505 | 138/930 | 42/23505 |
| 1 | 21/930 | 26/23505 | 132/930 | 44/23505 |
| 2 | 24/930 | 18/23505 | 132/930 | 38/23505 |
| 3 | 21/930 | 18/23505 | 127/930 | 40/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.0984 / 1.03996 | 0.0778911 | 0.261107 | 22830 | 20516/24435 |
| 1000 | 1.03873 / 1.038 | 0.00219607 | 0.0467652 | 44 | 20645/24435 |
| 2000 | 1.03827 / 1.03765 | 0.000513265 | 0.0248829 | 42 | 20764/24435 |
| 5000 | 1.04146 / 1.04095 | 0.000292944 | 0.257382 | 38 | 21019/24435 |
| 10000 | 1.03794 / 1.03737 | 0.000483935 | 0.248485 | 31 | 21306/24435 |
| 15000 | 1.03937 / 1.03919 | 0.000473534 | 0.261753 | 35 | 21604/24435 |
| 20000 | 1.04163 / 1.04123 | 0.000410938 | 0.251278 | 43 | 21733/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 17, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_live_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 14/930 | 25/23505 | 14/930 | 29/23505 |
| 1 | 15/930 | 18/23505 | 15/930 | 24/23505 |
| 2 | 14/930 | 25/23505 | 14/930 | 29/23505 |
| 3 | 19/930 | 27/23505 | 19/930 | 32/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.11117 / 1.03746 | 0.104708 | 0.272988 | 2034 | 19544/24435 |
| 1000 | 1.03967 / 1.03842 | 0.00123896 | 0.0428151 | 51 | 19756/24435 |
| 2000 | 1.03883 / 1.03792 | 0.000689192 | 0.258361 | 60 | 19933/24435 |
| 5000 | 1.04117 / 1.04087 | 0.000698317 | 0.0237596 | 54 | 20559/24435 |
| 10000 | 1.038 / 1.03777 | 0.000250614 | 0.0132478 | 38 | 21090/24435 |
| 15000 | 1.04107 / 1.04079 | 0.00018844 | 0.00894914 | 42 | 21495/24435 |
| 20000 | 1.03944 / 1.03919 | 0.000290625 | 0.0133297 | 39 | 21768/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_exact_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 0/930 | 0/23505 | 0/930 | 38/23505 |
| 1 | 0/930 | 0/23505 | 0/930 | 36/23505 |
| 2 | 0/930 | 0/23505 | 0/930 | 40/23505 |
| 3 | 0/930 | 0/23505 | 0/930 | 40/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10021 / 1.03922 | 0.0884562 | 0.249193 | 23880 | 24435/24435 |
| 1000 | 1.03908 / 1.03842 | 0.000804984 | 0.0357178 | 1 | 24435/24435 |
| 2000 | 1.04242 / 1.04169 | 0.00053008 | 0.0412937 | 1 | 24435/24435 |
| 5000 | 1.03906 / 1.03861 | 0.000897334 | 0.0255797 | 1 | 24435/24435 |
| 10000 | 1.04293 / 1.04253 | 0.000259559 | 0.0108833 | 0 | 24435/24435 |
| 15000 | 1.0392 / 1.03906 | 0.000539339 | 0.0197669 | 0 | 24435/24435 |
| 20000 | 1.03896 / 1.03876 | 0.000113841 | 0.0227492 | 0 | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 17, 'recurrence_associated': 0, 'unresolved': 1}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_exact_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 0/930 | 0/23505 | 6/930 | 9/23505 |
| 1 | 0/930 | 0/23505 | 9/930 | 7/23505 |
| 2 | 0/930 | 0/23505 | 4/930 | 8/23505 |
| 3 | 0/930 | 0/23505 | 8/930 | 8/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09838 / 1.03996 | 0.0778817 | 0.261107 | 22807 | 24435/24435 |
| 1000 | 1.03868 / 1.038 | 0.00230612 | 0.042831 | 1 | 24435/24435 |
| 2000 | 1.03813 / 1.03765 | 0.000383946 | 0.0377987 | 0 | 24435/24435 |
| 5000 | 1.04115 / 1.04095 | 0.000271651 | 0.00984694 | 0 | 24435/24435 |
| 10000 | 1.03754 / 1.03737 | 0.000443267 | 0.0155275 | 4 | 24435/24435 |
| 15000 | 1.03929 / 1.03919 | 0.00043965 | 0.0260102 | 0 | 24435/24435 |
| 20000 | 1.04143 / 1.04123 | 0.000306666 | 0.0156897 | 0 | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### access_exact_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 0/930 | 2/23505 | 0/930 | 24/23505 |
| 1 | 0/930 | 2/23505 | 0/930 | 20/23505 |
| 2 | 0/930 | 2/23505 | 0/930 | 22/23505 |
| 3 | 0/930 | 2/23505 | 0/930 | 21/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.11117 / 1.03746 | 0.104703 | 0.272988 | 2024 | 24435/24435 |
| 1000 | 1.03954 / 1.03842 | 0.00104569 | 0.0354827 | 0 | 24435/24435 |
| 2000 | 1.03858 / 1.03792 | 0.000425702 | 0.0178565 | 0 | 24435/24435 |
| 5000 | 1.0411 / 1.04087 | 0.000306765 | 0.0103826 | 1 | 24435/24435 |
| 10000 | 1.03794 / 1.03777 | 0.000166185 | 0.0160114 | 0 | 24435/24435 |
| 15000 | 1.04096 / 1.04079 | 0.000176133 | 0.0127766 | 0 | 24435/24435 |
| 20000 | 1.03934 / 1.03919 | 0.000280613 | 0.0114539 | 2 | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

## encoding

| Seed | Condition / law | Label | Failed B bars (values) | Categorical misreads | TV errors | Sums vector | Supplier vector |
|---|---|---|---|---|---|---|---|
| 0 | numerical / original | INCOMPLETE | law_TV=0.240672; rerender TV=0.051952; A differences=0; swaps: reset_L=0.243934, set_H=0.0472565 | 317 | 852 | 24435/24435 | 24435/24435 |
| 1 | numerical / original | INCOMPLETE | law_TV=0.0698225; rerender TV=0.0394671; A differences=0; swaps: neutral_N=0.162059, reset_L=0.175102, same_category_substitution=0.0936107, set_H=0.0315674, upper_state_exchange_same_N=0.046736 | 121 | 1194 | 24435/24435 | 24435/24435 |
| 2 | numerical / original | INCOMPLETE | law_TV=0.189016; swaps: neutral_N=0.0212905, reset_L=0.0825475, set_H=0.0360131, upper_state_exchange_same_N=0.0203803 | 10 | 90 | 24435/24435 | 24435/24435 |
| 0 | onehot / equal | CONTROL_ONLY | none | None | 0 | 24435/24435 | 24435/24435 |
| 1 | onehot / equal | CONTROL_ONLY | none | None | 0 | 24435/24435 | 24435/24435 |
| 2 | onehot / equal | CONTROL_ONLY | none | None | 0 | 24435/24435 | 24435/24435 |
| 0 | numerical / equal | CONTROL_ONLY | none | None | 0 | 24435/24435 | 24435/24435 |
| 1 | numerical / equal | CONTROL_ONLY | none | None | 0 | 24435/24435 | 24435/24435 |
| 2 | numerical / equal | CONTROL_ONLY | none | None | 0 | 24435/24435 | 24435/24435 |

### encoding_numerical_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 259/930 | 58/23505 | 514/930 | 338/23505 |
| 1 | 251/930 | 58/23505 | 520/930 | 349/23505 |
| 2 | 257/930 | 56/23505 | 516/930 | 341/23505 |
| 3 | 262/930 | 70/23505 | 519/930 | 348/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10095 / 1.03922 | 0.0894591 | 0.248015 | 23766 | 24435/24435 |
| 1000 | 1.04168 / 1.03842 | 0.00445077 | 0.21879 | 1386 | 24435/24435 |
| 2000 | 1.04325 / 1.04169 | 0.00201906 | 0.0928081 | 519 | 24435/24435 |
| 5000 | 1.03953 / 1.03861 | 0.00234775 | 0.0436547 | 397 | 24435/24435 |
| 10000 | 1.04317 / 1.04253 | 0.000731569 | 0.217332 | 150 | 24435/24435 |
| 15000 | 1.03946 / 1.03906 | 0.00123062 | 0.227795 | 114 | 24435/24435 |
| 20000 | 1.03923 / 1.03876 | 0.000836684 | 0.240672 | 317 | 24435/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 7, 'recurrence_associated': 0, 'unresolved': 10}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_numerical_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 114/930 | 7/23505 | 587/930 | 607/23505 |
| 1 | 101/930 | 7/23505 | 588/930 | 612/23505 |
| 2 | 91/930 | 6/23505 | 577/930 | 592/23505 |
| 3 | 108/930 | 6/23505 | 581/930 | 594/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10088 / 1.03996 | 0.0813421 | 0.262737 | 23619 | 24435/24435 |
| 1000 | 1.03985 / 1.038 | 0.0040061 | 0.194584 | 1202 | 24435/24435 |
| 2000 | 1.03883 / 1.03765 | 0.00206495 | 0.21391 | 664 | 24435/24435 |
| 5000 | 1.04171 / 1.04095 | 0.0012129 | 0.0728152 | 167 | 24435/24435 |
| 10000 | 1.03777 / 1.03737 | 0.000910096 | 0.146342 | 306 | 24435/24435 |
| 15000 | 1.03952 / 1.03919 | 0.000646545 | 0.0190011 | 110 | 24435/24435 |
| 20000 | 1.04165 / 1.04123 | 0.000794769 | 0.0698225 | 121 | 24435/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage', 'Upper recurrence remains a limitation']. Counts: {'board_associated': 2, 'non_deviating': 9, 'recurrence_associated': 2, 'unresolved': 5}; chronology: {'COINCIDENT': 2, 'NO_OBSERVED_CONSTITUENT_ERROR': 16, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_numerical_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 10/930 | 0/23505 | 79/930 | 11/23505 |
| 1 | 7/930 | 0/23505 | 75/930 | 14/23505 |
| 2 | 8/930 | 0/23505 | 86/930 | 16/23505 |
| 3 | 6/930 | 0/23505 | 94/930 | 16/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.11053 / 1.03746 | 0.103475 | 0.275744 | 1950 | 24435/24435 |
| 1000 | 1.04111 / 1.03842 | 0.00274842 | 0.196672 | 449 | 24435/24435 |
| 2000 | 1.03927 / 1.03792 | 0.00184719 | 0.235601 | 310 | 24435/24435 |
| 5000 | 1.04161 / 1.04087 | 0.00140253 | 0.0851077 | 130 | 24435/24435 |
| 10000 | 1.03832 / 1.03777 | 0.000707404 | 0.0633592 | 165 | 24435/24435 |
| 15000 | 1.04117 / 1.04079 | 0.000310304 | 0.0329466 | 14 | 24435/24435 |
| 20000 | 1.03947 / 1.03919 | 0.000543183 | 0.189016 | 10 | 24435/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage', 'Upper recurrence remains a limitation']. Counts: {'board_associated': 1, 'non_deviating': 12, 'recurrence_associated': 2, 'unresolved': 3}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_onehot_equal_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | None/930 | None/23505 | 0/930 | 0/23505 |
| 1 | None/930 | None/23505 | 0/930 | 0/23505 |
| 2 | None/930 | None/23505 | 0/930 | 0/23505 |
| 3 | None/930 | None/23505 | 0/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10008 / 1.08203 | 0.0259509 | 0.130892 | None | 24435/24435 |
| 1000 | 1.08256 / 1.08226 | 0.00065883 | 0.0286891 | None | 24435/24435 |
| 2000 | 1.08204 / 1.08183 | 0.000319285 | 0.0150162 | None | 24435/24435 |
| 5000 | 1.08289 / 1.08276 | 8.54962e-06 | 0.00256248 | None | 24435/24435 |
| 10000 | 1.08359 / 1.08356 | 0.000104901 | 0.00496924 | None | 24435/24435 |
| 15000 | 1.0832 / 1.08316 | 8.97695e-06 | 0.0017053 | None | 24435/24435 |
| 20000 | 1.08203 / 1.08193 | 2.60272e-05 | 0.00288574 | None | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_onehot_equal_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | None/930 | None/23505 | 0/930 | 0/23505 |
| 1 | None/930 | None/23505 | 0/930 | 0/23505 |
| 2 | None/930 | None/23505 | 0/930 | 0/23505 |
| 3 | None/930 | None/23505 | 0/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10189 / 1.08104 | 0.0276796 | 0.146792 | None | 24435/24435 |
| 1000 | 1.08191 / 1.08161 | 0.000232434 | 0.0165547 | None | 24435/24435 |
| 2000 | 1.08152 / 1.08129 | 7.11784e-05 | 0.0105474 | None | 24435/24435 |
| 5000 | 1.08217 / 1.08211 | 4.91769e-05 | 0.0102877 | None | 24435/24435 |
| 10000 | 1.08204 / 1.08203 | 0.000125993 | 0.00670874 | None | 24435/24435 |
| 15000 | 1.08149 / 1.08146 | 2.16472e-05 | 0.00256963 | None | 24435/24435 |
| 20000 | 1.08258 / 1.08255 | 1.17346e-05 | 0.00191306 | None | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_onehot_equal_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | None/930 | None/23505 | 0/930 | 0/23505 |
| 1 | None/930 | None/23505 | 0/930 | 0/23505 |
| 2 | None/930 | None/23505 | 0/930 | 0/23505 |
| 3 | None/930 | None/23505 | 0/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.1102 / 1.08228 | 0.0390705 | 0.232718 | None | 24435/24435 |
| 1000 | 1.08131 / 1.08119 | 0.0001569 | 0.0213897 | None | 24435/24435 |
| 2000 | 1.08336 / 1.08326 | 0.000150552 | 0.0225404 | None | 24435/24435 |
| 5000 | 1.08142 / 1.08138 | 2.03626e-05 | 0.00764044 | None | 24435/24435 |
| 10000 | 1.08168 / 1.08166 | 2.99345e-05 | 0.00341735 | None | 24435/24435 |
| 15000 | 1.08345 / 1.08343 | 2.38646e-05 | 0.00241667 | None | 24435/24435 |
| 20000 | 1.08345 / 1.08346 | 0.000199459 | 0.00717549 | None | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_numerical_equal_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | None/930 | None/23505 | 0/930 | 0/23505 |
| 1 | None/930 | None/23505 | 0/930 | 0/23505 |
| 2 | None/930 | None/23505 | 0/930 | 0/23505 |
| 3 | None/930 | None/23505 | 0/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10098 / 1.08203 | 0.0275948 | 0.128343 | None | 24435/24435 |
| 1000 | 1.08256 / 1.08226 | 0.00062691 | 0.027806 | None | 24435/24435 |
| 2000 | 1.082 / 1.08183 | 0.000370966 | 0.0155614 | None | 24435/24435 |
| 5000 | 1.08288 / 1.08276 | 8.22116e-06 | 0.00165775 | None | 24435/24435 |
| 10000 | 1.08359 / 1.08356 | 0.000105037 | 0.00494531 | None | 24435/24435 |
| 15000 | 1.0832 / 1.08316 | 8.962e-06 | 0.00169999 | None | 24435/24435 |
| 20000 | 1.08203 / 1.08193 | 2.60023e-05 | 0.00288571 | None | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_numerical_equal_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | None/930 | None/23505 | 0/930 | 0/23505 |
| 1 | None/930 | None/23505 | 0/930 | 0/23505 |
| 2 | None/930 | None/23505 | 0/930 | 0/23505 |
| 3 | None/930 | None/23505 | 0/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10458 / 1.08104 | 0.0316564 | 0.153675 | None | 24435/24435 |
| 1000 | 1.08187 / 1.08161 | 0.000234596 | 0.0178357 | None | 24435/24435 |
| 2000 | 1.08146 / 1.08129 | 7.25643e-05 | 0.00892644 | None | 24435/24435 |
| 5000 | 1.08215 / 1.08211 | 8.93904e-05 | 0.00991061 | None | 24435/24435 |
| 10000 | 1.08205 / 1.08203 | 0.00012401 | 0.00717819 | None | 24435/24435 |
| 15000 | 1.08149 / 1.08146 | 2.15679e-05 | 0.00256342 | None | 24435/24435 |
| 20000 | 1.08258 / 1.08255 | 1.1745e-05 | 0.0019127 | None | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### encoding_numerical_equal_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | None/930 | None/23505 | 0/930 | 0/23505 |
| 1 | None/930 | None/23505 | 0/930 | 0/23505 |
| 2 | None/930 | None/23505 | 0/930 | 0/23505 |
| 3 | None/930 | None/23505 | 0/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.10943 / 1.08228 | 0.0372672 | 0.237503 | None | 24435/24435 |
| 1000 | 1.08131 / 1.08119 | 0.000154143 | 0.020919 | None | 24435/24435 |
| 2000 | 1.08336 / 1.08326 | 0.000126994 | 0.0142431 | None | 24435/24435 |
| 5000 | 1.08143 / 1.08138 | 8.86756e-06 | 0.00372642 | None | 24435/24435 |
| 10000 | 1.08168 / 1.08166 | 2.67077e-05 | 0.00291747 | None | 24435/24435 |
| 15000 | 1.08345 / 1.08343 | 2.38517e-05 | 0.00241557 | None | 24435/24435 |
| 20000 | 1.08345 / 1.08346 | 0.00019945 | 0.00717551 | None | 24435/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

## erosion

All active conditions lose exactness at update 1. Blocked is a separate decay-only control. Gradients, displacement and small answer margins are not isolated explanations.

| Seed | Arm | Onset | Update-1 correct / 1555 | Final correct / 1555 | Path | Initial margin min / median | Final margin min / median |
|---|---|---|---|---|---|---|---|
| 0 | adam | 1 | 393/1555 | 48/1555 | 17.647 | 0.37664 / 6.58318 | -229.727 / -95.3237 |
| 1 | adam | 1 | 5/1555 | 13/1555 | 17.4749 | 0.37664 / 6.58318 | -182.281 / -107.755 |
| 2 | adam | 1 | 518/1555 | 14/1555 | 20.5136 | 0.37664 / 6.58318 | -222.131 / -159.352 |
| 0 | reduced | 1 | 1554/1555 | 333/1555 | 2.5057 | 0.37664 / 6.58318 | -57.1458 / -9.36194 |
| 1 | reduced | 1 | 1468/1555 | 292/1555 | 2.44784 | 0.37664 / 6.58318 | -44.2843 / -11.9342 |
| 2 | reduced | 1 | 1553/1555 | 343/1555 | 2.54409 | 0.37664 / 6.58318 | -75.9114 / -10.893 |
| 0 | sgd | 1 | 1440/1555 | 1/1555 | 11.4239 | 0.37664 / 6.58318 | -521.125 / -161.163 |
| 1 | sgd | 1 | 89/1555 | 11/1555 | 10.2103 | 0.37664 / 6.58318 | -264.347 / -210.483 |
| 2 | sgd | 1 | 1495/1555 | 27/1555 | 36.0327 | 0.37664 / 6.58318 | -359.99 / -149.073 |
| 0 | blocked | None | 1555/1555 | 1555/1555 | 0.219588 | 0.37664 / 6.58318 | 0.316383 / 6.18193 |
| 1 | blocked | None | 1555/1555 | 1555/1555 | 0.219588 | 0.37664 / 6.58318 | 0.316383 / 6.18193 |
| 2 | blocked | None | 1555/1555 | 1555/1555 | 0.219588 | 0.37664 / 6.58318 | 0.316383 / 6.18193 |

| Seed | Active arms | Observed common path range | Recorded points: count, correct min–max |
|---|---|---|---|
| 0 | adam--reduced | [0.0, 2.505703246580978] | adam: 11, 49–1555; reduced: 201, 79–1555 |
| 0 | adam--sgd | [0.0, 11.423875334303096] | adam: 97, 7–1555; sgd: 201, 1–1555 |
| 0 | adam--sgd--reduced | [0.0, 2.505703246580978] | adam: 11, 49–1555; reduced: 201, 79–1555; sgd: 6, 87–1555 |
| 0 | sgd--reduced | [0.0, 2.505703246580978] | reduced: 201, 79–1555; sgd: 6, 87–1555 |
| 1 | adam--reduced | [0.0, 2.4478360427124897] | adam: 10, 2–1555; reduced: 201, 261–1555 |
| 1 | adam--sgd | [0.0, 10.210289210254576] | adam: 84, 2–1555; sgd: 201, 11–1555 |
| 1 | adam--sgd--reduced | [0.0, 2.4478360427124897] | adam: 10, 2–1555; reduced: 201, 261–1555; sgd: 4, 89–1555 |
| 1 | sgd--reduced | [0.0, 2.4478360427124897] | reduced: 201, 261–1555; sgd: 4, 89–1555 |
| 2 | adam--reduced | [0.0, 2.544091336970288] | adam: 11, 55–1555; reduced: 201, 251–1555 |
| 2 | adam--sgd | [0.0, 20.513627367546448] | adam: 201, 10–1555; sgd: 30, 2–1555 |
| 2 | adam--sgd--reduced | [0.0, 2.544091336970288] | adam: 11, 55–1555; reduced: 201, 251–1555; sgd: 6, 2–1555 |
| 2 | sgd--reduced | [0.0, 2.544091336970288] | reduced: 201, 251–1555; sgd: 6, 2–1555 |

All 201 recorded accuracy counts and per-tensor gradient/epsilon summaries are in compact JSON; full margin curves, per-update records and matched-range points are hash-bound below. No answer-accuracy interpolation is used.

| Seed / arm | Tensor | Gradient norm min / mean / max | Mean fraction ≤ epsilon | Mean fraction > 10 epsilon |
|---|---|---|---|---|
| 0 / adam | memory.kind_embedding.weight | 1.01448e-07 / 5.4332e-05 / 0.0011626 | 0.670859 | 0.300625 |
| 0 / adam | memory.mass_embedding.weight | 6.32386e-07 / 0.00127463 / 0.0266283 | 0.125547 | 0.777292 |
| 0 / adam | memory.readout.0.bias | 1.07284e-07 / 6.6138e-05 / 0.001565 | 0.0657812 | 0.798438 |
| 0 / adam | memory.readout.0.weight | 1.1487e-06 / 0.000689479 / 0.0133127 | 0.077702 | 0.769606 |
| 0 / adam | memory.readout.2.bias | 7.29715e-08 / 3.61194e-05 / 0.000844589 | 0.750833 | 0.204583 |
| 0 / adam | memory.readout.2.weight | 3.76843e-06 / 0.00227178 / 0.0291107 | 0.7973 | 0.160946 |
| 0 / adam | memory.start_state | 5.99756e-08 / 0.00109115 / 0.0335761 | 0.0142969 | 0.935547 |
| 0 / adam | memory.transition.0.bias | 5.78309e-07 / 0.0010664 / 0.022616 | 0.00226562 | 0.978516 |
| 0 / adam | memory.transition.0.weight | 6.1954e-06 / 0.00930882 / 0.179993 | 0.00379211 | 0.971413 |
| 0 / adam | memory.transition.2.bias | 3.26921e-07 / 0.00063892 / 0.0127868 | 0.0154687 | 0.919687 |
| 0 / adam | memory.transition.2.weight | 6.48238e-06 / 0.00786678 / 0.138989 | 0.0432837 | 0.856351 |
| 1 / adam | memory.kind_embedding.weight | 5.59687e-07 / 0.000114103 / 0.00175339 | 0.667292 | 0.325547 |
| 1 / adam | memory.mass_embedding.weight | 2.5776e-07 / 0.000978408 / 0.00977751 | 0.0325391 | 0.914974 |
| 1 / adam | memory.readout.0.bias | 1.34791e-06 / 8.02193e-05 / 0.000668161 | 0.02125 | 0.915234 |
| 1 / adam | memory.readout.0.weight | 1.70043e-05 / 0.000891139 / 0.00720955 | 0.0266296 | 0.892654 |
| 1 / adam | memory.readout.2.bias | 7.24835e-07 / 4.94054e-05 / 0.00033223 | 0.717917 | 0.239861 |
| 1 / adam | memory.readout.2.weight | 5.69251e-05 / 0.00368028 / 0.023109 | 0.759596 | 0.197231 |
| 1 / adam | memory.start_state | 4.13087e-06 / 0.00126475 / 0.0155998 | 0.000703125 | 0.995 |
| 1 / adam | memory.transition.0.bias | 2.05941e-07 / 0.000832807 / 0.00696897 | 0.00179688 | 0.989453 |
| 1 / adam | memory.transition.0.weight | 2.04197e-06 / 0.00763809 / 0.0625696 | 0.00274475 | 0.987461 |
| 1 / adam | memory.transition.2.bias | 1.11174e-07 / 0.000535033 / 0.00451249 | 0.00703125 | 0.967266 |
| 1 / adam | memory.transition.2.weight | 2.13148e-06 / 0.00613727 / 0.0562122 | 0.0142395 | 0.937485 |
| 2 / adam | memory.kind_embedding.weight | 1.19178e-07 / 0.000103223 / 0.00321226 | 0.669818 | 0.311276 |
| 2 / adam | memory.mass_embedding.weight | 8.38889e-07 / 0.00171908 / 0.04516 | 0.086224 | 0.858789 |
| 2 / adam | memory.readout.0.bias | 1.36909e-07 / 0.000124908 / 0.00580121 | 0.0353906 | 0.897891 |
| 2 / adam | memory.readout.0.weight | 1.3375e-06 / 0.00127787 / 0.048594 | 0.0458533 | 0.876771 |
| 2 / adam | memory.readout.2.bias | 8.58414e-08 / 6.63485e-05 / 0.00249921 | 0.695833 | 0.251944 |
| 2 / adam | memory.readout.2.weight | 4.84094e-06 / 0.00398651 / 0.0802031 | 0.739099 | 0.215419 |
| 2 / adam | memory.start_state | 4.23809e-07 / 0.00163894 / 0.0499561 | 0.00226562 | 0.977656 |
| 2 / adam | memory.transition.0.bias | 3.84581e-07 / 0.00128323 / 0.0366216 | 0.00242187 | 0.982734 |
| 2 / adam | memory.transition.0.weight | 5.366e-06 / 0.0109519 / 0.229541 | 0.00420837 | 0.978302 |
| 2 / adam | memory.transition.2.bias | 2.13986e-07 / 0.000699482 / 0.0202053 | 0.0107812 | 0.961328 |
| 2 / adam | memory.transition.2.weight | 2.13504e-06 / 0.00780073 / 0.146986 | 0.0203442 | 0.936511 |
| 0 / reduced | memory.kind_embedding.weight | 2.69181e-05 / 0.000182886 / 0.00104822 | 0.666823 | 0.331901 |
| 0 / reduced | memory.mass_embedding.weight | 4.60868e-05 / 0.00226515 / 0.0182111 | 0.000416667 | 0.997201 |
| 0 / reduced | memory.readout.0.bias | 5.75595e-05 / 0.000269306 / 0.00125263 | 0.0003125 | 0.996172 |
| 0 / reduced | memory.readout.0.weight | 0.000595132 / 0.00282206 / 0.0133003 | 0.000560913 | 0.993685 |
| 0 / reduced | memory.readout.2.bias | 4.94941e-05 / 0.000190318 / 0.000983678 | 0.00180556 | 0.984306 |
| 0 / reduced | memory.readout.2.weight | 0.00360889 / 0.0134041 / 0.0615532 | 0.247103 | 0.705471 |
| 0 / reduced | memory.start_state | 0.000199747 / 0.00384107 / 0.0299471 | 0 | 0.999687 |
| 0 / reduced | memory.transition.0.bias | 4.12872e-05 / 0.00261924 / 0.0217421 | 0 | 0.999453 |
| 0 / reduced | memory.transition.0.weight | 0.00045123 / 0.0221604 / 0.202993 | 0.000105591 | 0.999056 |
| 0 / reduced | memory.transition.2.bias | 5.62281e-05 / 0.00145006 / 0.00971455 | 0.00015625 | 0.997734 |
| 0 / reduced | memory.transition.2.weight | 0.000780771 / 0.0150545 / 0.0965009 | 0.000557861 | 0.995095 |
| 1 / reduced | memory.kind_embedding.weight | 2.53105e-05 / 0.000135183 / 0.000430481 | 0.666823 | 0.331589 |
| 1 / reduced | memory.mass_embedding.weight | 0.000125818 / 0.0024187 / 0.0193814 | 0.000195313 | 0.997904 |
| 1 / reduced | memory.readout.0.bias | 6.42177e-05 / 0.000246522 / 0.00101596 | 0.000546875 | 0.994844 |
| 1 / reduced | memory.readout.0.weight | 0.000712875 / 0.00275694 / 0.011545 | 0.00071167 | 0.993003 |
| 1 / reduced | memory.readout.2.bias | 4.13159e-05 / 0.000217025 / 0.000908313 | 0.000972222 | 0.987083 |
| 1 / reduced | memory.readout.2.weight | 0.00345569 / 0.0171831 / 0.0656482 | 0.251576 | 0.702724 |
| 1 / reduced | memory.start_state | 0.000172076 / 0.00431419 / 0.0418747 | 0 | 0.999687 |
| 1 / reduced | memory.transition.0.bias | 0.000126714 / 0.0030975 / 0.0292318 | 0.00015625 | 0.999453 |
| 1 / reduced | memory.transition.0.weight | 0.00112819 / 0.0254323 / 0.257887 | 7.99561e-05 | 0.999191 |
| 1 / reduced | memory.transition.2.bias | 0.000152043 / 0.00175677 / 0.0140029 | 0.000234375 | 0.998047 |
| 1 / reduced | memory.transition.2.weight | 0.00158076 / 0.0170717 / 0.11551 | 0.000537109 | 0.99525 |
| 2 / reduced | memory.kind_embedding.weight | 2.17726e-05 / 0.000124444 / 0.000405057 | 0.666875 | 0.331745 |
| 2 / reduced | memory.mass_embedding.weight | 9.61934e-05 / 0.00205254 / 0.00740526 | 0.000325521 | 0.997357 |
| 2 / reduced | memory.readout.0.bias | 6.09733e-05 / 0.000237793 / 0.000816853 | 7.8125e-05 | 0.994219 |
| 2 / reduced | memory.readout.0.weight | 0.000682833 / 0.0026001 / 0.00887539 | 0.000545044 | 0.991981 |
| 2 / reduced | memory.readout.2.bias | 5.15308e-05 / 0.000164508 / 0.000554729 | 0.00875 | 0.965139 |
| 2 / reduced | memory.readout.2.weight | 0.00390185 / 0.0124434 / 0.0412652 | 0.253685 | 0.694911 |
| 2 / reduced | memory.start_state | 0.000138644 / 0.00326232 / 0.0269485 | 7.8125e-05 | 0.999531 |
| 2 / reduced | memory.transition.0.bias | 9.25498e-05 / 0.00237135 / 0.0187912 | 7.8125e-05 | 0.999375 |
| 2 / reduced | memory.transition.0.weight | 0.000942154 / 0.0202238 / 0.114701 | 9.82666e-05 | 0.999036 |
| 2 / reduced | memory.transition.2.bias | 0.000126732 / 0.00140122 / 0.0113115 | 7.8125e-05 | 0.997812 |
| 2 / reduced | memory.transition.2.weight | 0.00134697 / 0.0144029 / 0.103815 | 0.000550537 | 0.995171 |
| 0 / sgd | memory.kind_embedding.weight | 2.33689e-12 / 3.07893e-05 / 0.00494133 | 0.98 | 0.019974 |
| 0 / sgd | memory.mass_embedding.weight | 8.95302e-12 / 5.62027e-05 / 0.00235352 | 0.940104 | 0.0591667 |
| 0 / sgd | memory.readout.0.bias | 1.44341e-12 / 5.15544e-05 / 0.00856858 | 0.940156 | 0.0592969 |
| 0 / sgd | memory.readout.0.weight | 1.68746e-11 / 0.000454728 / 0.0730214 | 0.940169 | 0.0588428 |
| 0 / sgd | memory.readout.2.bias | 4.60223e-13 / 2.9198e-05 / 0.00463428 | 0.956389 | 0.0395833 |
| 0 / sgd | memory.readout.2.weight | 3.74903e-11 / 0.00114518 / 0.150475 | 0.966899 | 0.0288216 |
| 0 / sgd | memory.start_state | 8.06253e-12 / 0.000349861 / 0.0531791 | 0.94 | 0.06 |
| 0 / sgd | memory.transition.0.bias | 6.44727e-12 / 5.54886e-05 / 0.00219088 | 0.94 | 0.0599219 |
| 0 / sgd | memory.transition.0.weight | 6.70505e-11 / 0.000523828 / 0.0179125 | 0.940023 | 0.0597589 |
| 0 / sgd | memory.transition.2.bias | 5.16773e-12 / 3.64795e-05 / 0.00172995 | 0.940234 | 0.0594531 |
| 0 / sgd | memory.transition.2.weight | 6.62606e-11 / 0.000414827 / 0.019239 | 0.940183 | 0.0584888 |
| 1 / sgd | memory.kind_embedding.weight | 6.47314e-11 / 4.96106e-06 / 0.00015341 | 0.971719 | 0.0255208 |
| 1 / sgd | memory.mass_embedding.weight | 5.4538e-21 / 7.15387e-05 / 0.0023445 | 0.920078 | 0.0791016 |
| 1 / sgd | memory.readout.0.bias | 3.91711e-11 / 6.50199e-06 / 0.000240997 | 0.918203 | 0.0753906 |
| 1 / sgd | memory.readout.0.weight | 3.33707e-10 / 7.10891e-05 / 0.00261372 | 0.918862 | 0.0738898 |
| 1 / sgd | memory.readout.2.bias | 1.64563e-11 / 4.71802e-06 / 0.000218634 | 0.955 | 0.0391667 |
| 1 / sgd | memory.readout.2.weight | 5.29412e-10 / 0.000340191 / 0.0175431 | 0.965087 | 0.0294162 |
| 1 / sgd | memory.start_state | 2.25454e-10 / 9.27775e-05 / 0.00312511 | 0.914297 | 0.0848437 |
| 1 / sgd | memory.transition.0.bias | 3.53864e-21 / 6.13467e-05 / 0.00185244 | 0.915 | 0.0848437 |
| 1 / sgd | memory.transition.0.weight | 5.47034e-20 / 0.00049188 / 0.0142434 | 0.915126 | 0.0839447 |
| 1 / sgd | memory.transition.2.bias | 3.34882e-21 / 3.36083e-05 / 0.00119768 | 0.917188 | 0.0808594 |
| 1 / sgd | memory.transition.2.weight | 5.89076e-20 / 0.000358639 / 0.0135503 | 0.917161 | 0.0799744 |
| 2 / sgd | memory.kind_embedding.weight | 4.85579e-11 / 4.29933e-05 / 0.00222928 | 0.786667 | 0.184167 |
| 2 / sgd | memory.mass_embedding.weight | 2.38612e-09 / 0.000484413 / 0.0150762 | 0.408854 | 0.504076 |
| 2 / sgd | memory.readout.0.bias | 9.93479e-11 / 4.93113e-05 / 0.00247257 | 0.42 | 0.466875 |
| 2 / sgd | memory.readout.0.weight | 1.08446e-09 / 0.00053729 / 0.0280351 | 0.43064 | 0.448062 |
| 2 / sgd | memory.readout.2.bias | 4.64701e-11 / 2.42684e-05 / 0.000911256 | 0.838333 | 0.133889 |
| 2 / sgd | memory.readout.2.weight | 3.27047e-09 / 0.00159106 / 0.077926 | 0.868422 | 0.105228 |
| 2 / sgd | memory.start_state | 7.2393e-10 / 0.000342537 / 0.011631 | 0.302578 | 0.577344 |
| 2 / sgd | memory.transition.0.bias | 1.1211e-09 / 0.000322013 / 0.00917173 | 0.286875 | 0.643203 |
| 2 / sgd | memory.transition.0.weight | 1.08556e-08 / 0.00303059 / 0.088723 | 0.297998 | 0.636124 |
| 2 / sgd | memory.transition.2.bias | 5.26481e-10 / 0.000200345 / 0.00909308 | 0.369844 | 0.543125 |
| 2 / sgd | memory.transition.2.weight | 8.51696e-09 / 0.00268002 / 0.0925137 | 0.387368 | 0.499462 |
| 0 / blocked | memory.kind_embedding.weight | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.mass_embedding.weight | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.readout.0.bias | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.readout.0.weight | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.readout.2.bias | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.readout.2.weight | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.start_state | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.transition.0.bias | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.transition.0.weight | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.transition.2.bias | 0 / 0 / 0 | 1 | 0 |
| 0 / blocked | memory.transition.2.weight | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.kind_embedding.weight | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.mass_embedding.weight | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.readout.0.bias | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.readout.0.weight | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.readout.2.bias | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.readout.2.weight | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.start_state | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.transition.0.bias | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.transition.0.weight | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.transition.2.bias | 0 / 0 / 0 | 1 | 0 |
| 1 / blocked | memory.transition.2.weight | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.kind_embedding.weight | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.mass_embedding.weight | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.readout.0.bias | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.readout.0.weight | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.readout.2.bias | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.readout.2.weight | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.start_state | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.transition.0.bias | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.transition.0.weight | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.transition.2.bias | 0 / 0 / 0 | 1 | 0 |
| 2 / blocked | memory.transition.2.weight | 0 / 0 / 0 | 1 | 0 |

Epsilon = 1e-8. Component fractions are averaged over the 200 recorded updates, separately for each tensor, not weighted across tensors. True-class logit margins at update 0, update 1 and update 200 are retained in JSON; negative margins mean an incorrect answer.

## noise

| Seed | Condition / law | Label | Failed B bars (values) | Categorical misreads | TV errors | Sums vector | Supplier vector |
|---|---|---|---|---|---|---|---|
| 0 | raw_sampled / original | INCOMPLETE | law_TV=0.0333845; rerender TV=0.091887; A differences=0; swaps: neutral_N=0.131186, reset_L=0.224259, same_category_substitution=0.105307, set_H=0.0261197, upper_state_exchange_same_N=0.109132 | 58 | 237 | 0/24435 | 0/24435 |
| 1 | raw_sampled / original | INCOMPLETE | law_TV=0.171739; rerender TV=0.0387325; A differences=0; swaps: neutral_N=0.0238081, reset_L=0.249686, same_category_substitution=0.0209796 | 328 | 4047 | 0/24435 | 0/24435 |
| 2 | raw_sampled / original | INCOMPLETE | law_TV=0.0664272; rerender TV=0.033427; A differences=0; swaps: neutral_N=0.0215478, reset_L=0.251961, set_H=0.0826416 | 87 | 613 | 0/24435 | 0/24435 |
| 0 | raw_probability / original | INCOMPLETE | law_TV=0.0221688; rerender TV=0.0506461; A differences=0 | 2 | 12 | 0/24435 | 0/24435 |
| 1 | raw_probability / original | INCOMPLETE | swaps: reset_L=0.0227315 | 1 | 8 | 0/24435 | 0/24435 |
| 2 | raw_probability / original | INCOMPLETE | law_TV=0.1404; rerender TV=0.0377659; A differences=0; swaps: reset_L=0.248175, set_H=0.0363104 | 149 | 324 | 0/24435 | 0/24435 |
| 0 | sums_sampled / original | INCOMPLETE | law_TV=0.0649652; rerender TV=0.082753; A differences=0; swaps: neutral_N=0.0729794, reset_L=0.226858, same_category_substitution=0.0812623, set_H=0.0722587, upper_state_exchange_same_N=0.0729794 | 473 | 1888 | 19269/24435 | 0/24435 |
| 1 | sums_sampled / original | INCOMPLETE | law_TV=0.132952; rerender TV=0.059102; A differences=0; swaps: neutral_N=0.0353215, reset_L=0.239461, same_category_substitution=0.0694649, set_H=0.119447, upper_state_exchange_same_N=0.0249793 | 648 | 2786 | 20516/24435 | 0/24435 |
| 2 | sums_sampled / original | INCOMPLETE | law_TV=0.0447989; rerender TV=0.05526; A differences=0; swaps: neutral_N=0.0332057, reset_L=0.248785, same_category_substitution=0.0589354, set_H=0.130668, upper_state_exchange_same_N=0.0332057 | 815 | 4272 | 19544/24435 | 0/24435 |
| 0 | sums_probability / original | INCOMPLETE | law_TV=0.0370325; rerender TV=0.0225977; A differences=0; swaps: neutral_N=0.0828235, reset_L=0.216276, same_category_substitution=0.080489, set_H=0.0403577, upper_state_exchange_same_N=0.0828235 | 473 | 2897 | 19921/24435 | 0/24435 |
| 1 | sums_probability / original | INCOMPLETE | law_TV=0.0352656; swaps: neutral_N=0.0208988, reset_L=0.21818, same_category_substitution=0.0489362, set_H=0.0480071 | 400 | 2361 | 19527/24435 | 0/24435 |
| 2 | sums_probability / original | INCOMPLETE | law_TV=0.0237418; rerender TV=0.0249389; A differences=0; swaps: reset_L=0.226175, set_H=0.0203439 | 523 | 2910 | 19513/24435 | 0/24435 |

### noise_raw_sampled_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 57/930 | 1/23505 | 212/930 | 25/23505 |
| 1 | 60/930 | 0/23505 | 211/930 | 21/23505 |
| 2 | 59/930 | 0/23505 | 232/930 | 19/23505 |
| 3 | 60/930 | 0/23505 | 215/930 | 23/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09978 / 1.03922 | 0.087358 | 0.216547 | 24326 | 0/24435 |
| 1000 | 1.0409 / 1.03842 | 0.00359243 | 0.23986 | 1018 | 0/24435 |
| 2000 | 1.04378 / 1.04169 | 0.00295734 | 0.0955303 | 521 | 0/24435 |
| 5000 | 1.03947 / 1.03861 | 0.00250568 | 0.108577 | 224 | 0/24435 |
| 10000 | 1.04313 / 1.04253 | 0.00188115 | 0.235272 | 366 | 0/24435 |
| 15000 | 1.03954 / 1.03906 | 0.00116048 | 0.0363184 | 253 | 0/24435 |
| 20000 | 1.03912 / 1.03876 | 0.000529208 | 0.0333845 | 58 | 0/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 14, 'recurrence_associated': 0, 'unresolved': 4}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

Geometry update 0: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 4/6 | 0.666667 | 0.895787 | 0.955128 | True | False | [1.134452, 1.168728, 1.37725] | 0.840998 |
| [0, 9] | 11 / 1 | 1/2 | 0.5 | 0.880587 | 5.3551 | True | False | [2.051162, 2.051162, 2.051162] | 1.04385 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.0717982 | 0.00157313 | True | False | [1.608514, 1.608514, 1.608514] | 1.01837 |
| [0, 17] | 4 / 1 | 1/2 | 0.5 | 2.25931 | 0.0744683 | True | False | [1.240709, 1.240709, 1.240709] | 0.688191 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.0424525 | 0.905078 | True | True | [1.339795, 1.339795, 1.339795] | 0.525062 |
| [2, 6] | 13 / 1 | 1/2 | 0.5 | 4.22832 | 0.815448 | True | False | [1.073914, 1.073914, 1.073914] | 0.884173 |
| [2, 14] | 2 / 1 | 1/2 | 0.5 | 1.8019 | 5.86295 | True | False | [1.277372, 1.277372, 1.277372] | 0.675015 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.148106 | 0.540367 | True | True | [1.247568, 1.247568, 1.247568] | 0.756113 |
| [3, 8] | 8 / 3 | 4/6 | 0.666667 | 0.928824 | 0.833973 | True | False | [0.687204, 1.134637, 1.370659] | 0.708158 |
| [4, 8] | 12 / 2 | 3/4 | 0.75 | 2.19783 | 1.59764 | True | False | [1.420333, 1.430125, 1.439918] | 0.899993 |
| [4, 11] | 2 / 1 | 1/2 | 0.5 | 3.53824 | 1.95413 | True | False | [1.568651, 1.568651, 1.568651] | 1.15403 |
| [4, 17] | 3 / 2 | 3/4 | 0.75 | 3.17177 | 7.39739 | True | False | [0.553632, 1.045477, 1.537322] | 0.885426 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 1.33366 | 5.75422 | True | False | [1.039575, 1.039575, 1.039575] | 1.11355 |
| [6, 13] | 1 / 1 | 0/2 | 0 | 192.538 | 0 | True | False | [1.187406, 1.187406, 1.187406] | 1.07062 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.266692 | 0.266692 | True | False | [1.215903, 1.215903, 1.215903] | 1.05753 |
| [8, 9] | 9 / 1 | 1/2 | 0.5 | 4.92791 | 1.3848 | True | False | [0.902435, 0.902435, 0.902435] | 0.96547 |
| [8, 14] | 2 / 1 | 1/2 | 0.5 | 0.789695 | 3.34822 | True | False | [0.722873, 0.722873, 0.722873] | 1.2194 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.0933378 | 0.06345 | True | False | [1.205501, 1.205501, 1.205501] | 0.678195 |
| [13, 17] | 5 / 1 | 1/2 | 0.5 | 5.17502 | 0.0297856 | True | False | [0.823121, 0.823121, 0.823121] | 0.783473 |

Geometry update 5000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00571799 | 1.18539 | True | True | [1.078305, 1.118589, 1.393211] | 0.402448 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00890045 | 0.738913 | True | True | [1.536239, 1.536239, 1.536239] | 0.614781 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.0633822 | 0.329205 | True | False | [1.330184, 1.330184, 1.330184] | 0.683465 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00725787 | 0.344927 | True | False | [2.365373, 2.365373, 2.365373] | 0.5439 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.00371057 | 0.635015 | True | True | [2.683331, 2.683331, 2.683331] | 0.384271 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.0367073 | 1.46578 | True | True | [0.971873, 0.971873, 0.971873] | 0.35087 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.0270775 | 3.84124 | True | True | [2.090125, 2.090125, 2.090125] | 0.411451 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00166864 | 0.0115152 | True | False | [0.75173, 0.75173, 0.75173] | 0.26142 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0384915 | 0.617202 | True | False | [0.562474, 0.594004, 0.818044] | 0.333175 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00119552 | 1.33509 | True | True | [1.143095, 1.178913, 1.21473] | 0.633029 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.122183 | 5.87301 | True | True | [1.191607, 1.191607, 1.191607] | 0.761357 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00334561 | 0.518644 | True | True | [1.946267, 2.205624, 2.464981] | 0.78717 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 1.04935 | 2.60805 | True | False | [2.067702, 2.067702, 2.067702] | 0.760135 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 10.7389 | 8.95003 | True | False | [1.923342, 1.923342, 1.923342] | 1.0024 |
| [7, 8] | 1 / 1 | 1/2 | 0.5 | 7.1683 | 7.1683 | True | False | [1.093238, 1.093238, 1.093238] | 0.831419 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.005304 | 2.20837 | True | True | [0.873057, 0.873057, 0.873057] | 0.721666 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.069463 | 2.81148 | True | True | [1.289557, 1.289557, 1.289557] | 0.939482 |
| [10, 14] | 3 / 1 | 1/2 | 0.5 | 1.06387 | 1.00971 | True | False | [1.069303, 1.069303, 1.069303] | 0.511848 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.152828 | 0.406638 | True | True | [1.315683, 1.315683, 1.315683] | 0.979172 |

Geometry update 20000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00325266 | 1.03395 | True | True | [1.052057, 1.227359, 1.276248] | 0.275418 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00420609 | 0.916811 | True | True | [1.477171, 1.477171, 1.477171] | 0.626521 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.0103458 | 3.65736 | True | True | [1.243564, 1.243564, 1.243564] | 0.490236 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.0642092 | 0.669243 | True | True | [2.315503, 2.315503, 2.315503] | 0.667689 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.0153061 | 0.888575 | True | True | [2.163528, 2.163528, 2.163528] | 0.499444 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.000646107 | 0.269343 | True | False | [1.335619, 1.335619, 1.335619] | 0.448799 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.00895432 | 0.112215 | True | False | [2.271212, 2.271212, 2.271212] | 0.467984 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00171407 | 0.0323041 | True | False | [1.061537, 1.061537, 1.061537] | 0.403131 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0127964 | 1.40964 | True | True | [0.672066, 1.008467, 1.503936] | 0.422343 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00457632 | 0.384832 | True | True | [1.231188, 1.428118, 1.625048] | 0.540645 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.112139 | 3.46169 | True | True | [1.334001, 1.334001, 1.334001] | 0.849838 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.0100096 | 0.967714 | True | True | [2.306896, 2.378411, 2.449926] | 0.872458 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 0.520914 | 3.20883 | True | False | [2.243208, 2.243208, 2.243208] | 0.970559 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 453.029 | 105.522 | True | False | [2.173357, 2.173357, 2.173357] | 1.24213 |
| [7, 8] | 1 / 1 | 1/2 | 0.5 | 5.14533 | 5.14533 | True | False | [1.306081, 1.306081, 1.306081] | 0.825374 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.0116549 | 0.412626 | True | True | [1.362809, 1.362809, 1.362809] | 0.821293 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.0737727 | 2.64668 | True | True | [1.468995, 1.468995, 1.468995] | 1.10138 |
| [10, 14] | 3 / 1 | 1/2 | 0.5 | 0.389902 | 1.372 | True | False | [1.501522, 1.501522, 1.501522] | 0.547885 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.0104393 | 0.125393 | True | False | [1.868441, 1.868441, 1.868441] | 1.34836 |

### noise_raw_sampled_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 289/930 | 39/23505 | 573/930 | 3474/23505 |
| 1 | 294/930 | 47/23505 | 573/930 | 3505/23505 |
| 2 | 287/930 | 43/23505 | 573/930 | 3522/23505 |
| 3 | 275/930 | 37/23505 | 574/930 | 3564/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.08859 / 1.03996 | 0.0671472 | 0.206921 | 23817 | 0/24435 |
| 1000 | 1.04013 / 1.038 | 0.00384834 | 0.2214 | 990 | 0/24435 |
| 2000 | 1.03935 / 1.03765 | 0.00219312 | 0.117717 | 590 | 0/24435 |
| 5000 | 1.04166 / 1.04095 | 0.00126522 | 0.0658261 | 167 | 0/24435 |
| 10000 | 1.03777 / 1.03737 | 0.000687119 | 0.138164 | 120 | 0/24435 |
| 15000 | 1.03941 / 1.03919 | 0.000648226 | 0.0255374 | 207 | 0/24435 |
| 20000 | 1.04161 / 1.04123 | 0.000542557 | 0.171739 | 328 | 0/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 16, 'recurrence_associated': 0, 'unresolved': 1}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

Geometry update 0: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 4/6 | 0.666667 | 0.619432 | 0.360189 | True | False | [1.10463, 1.315478, 1.442413] | 0.885242 |
| [0, 9] | 11 / 1 | 1/2 | 0.5 | 1.10397 | 2.56826 | True | False | [1.254778, 1.254778, 1.254778] | 1.13128 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.308432 | 0.0364723 | True | False | [1.670705, 1.670705, 1.670705] | 0.790128 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00447195 | 0.704098 | True | True | [1.43509, 1.43509, 1.43509] | 0.688557 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.155452 | 1.16853 | True | True | [1.726676, 1.726676, 1.726676] | 0.629646 |
| [2, 6] | 13 / 1 | 1/2 | 0.5 | 2.24277 | 1.8586 | True | False | [1.190346, 1.190346, 1.190346] | 0.972077 |
| [2, 14] | 2 / 1 | 1/2 | 0.5 | 1.17389 | 0.0832449 | True | False | [0.888175, 0.888175, 0.888175] | 0.869838 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00105993 | 0.134084 | True | False | [1.567079, 1.567079, 1.567079] | 0.85511 |
| [3, 8] | 8 / 3 | 4/6 | 0.666667 | 0.548217 | 2.03218 | True | False | [0.758073, 1.164194, 1.271011] | 0.788796 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.0659835 | 1.02224 | True | True | [1.144007, 1.159507, 1.175007] | 0.78428 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.355672 | 1.83221 | True | True | [1.059908, 1.059908, 1.059908] | 0.955426 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.0774318 | 1.64131 | True | True | [0.907198, 1.212593, 1.517988] | 0.725521 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 3.56247 | 5.87577 | True | False | [0.903418, 0.903418, 0.903418] | 1.07291 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 0.382188 | 4.15969 | True | False | [1.197203, 1.197203, 1.197203] | 1.18571 |
| [7, 8] | 1 / 1 | 1/2 | 0.5 | 15.7097 | 15.7097 | True | False | [1.110225, 1.110225, 1.110225] | 0.97057 |
| [8, 9] | 9 / 1 | 1/2 | 0.5 | 5.44418 | 3.13656 | True | False | [0.676475, 0.676475, 0.676475] | 0.980368 |
| [8, 14] | 2 / 1 | 1/2 | 0.5 | 4.0181 | 2.94043 | True | False | [0.423279, 0.423279, 0.423279] | 0.788909 |
| [10, 14] | 3 / 1 | 1/2 | 0.5 | 4.32921 | 1.98098 | True | False | [0.625481, 0.625481, 0.625481] | 0.601174 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.016931 | 0.0146049 | True | False | [1.336739, 1.336739, 1.336739] | 0.972161 |

Geometry update 5000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00144873 | 1.06857 | True | True | [0.904201, 1.127869, 1.508189] | 0.337955 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00241345 | 0.465016 | True | True | [1.178902, 1.178902, 1.178902] | 0.435403 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00902458 | 4.65889 | True | True | [1.1935, 1.1935, 1.1935] | 0.597245 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00470947 | 0.279154 | True | False | [2.358954, 2.358954, 2.358954] | 0.505777 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.0035529 | 2.42468 | True | True | [2.649862, 2.649862, 2.649862] | 0.337868 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.00189777 | 1.58931 | True | True | [0.720437, 0.720437, 0.720437] | 0.440737 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.0133914 | 0.602824 | True | False | [1.770349, 1.770349, 1.770349] | 0.481005 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.0017113 | 0.0660084 | True | False | [0.735874, 0.735874, 0.735874] | 0.212738 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0410587 | 0.349402 | True | False | [0.86084, 0.917754, 1.409423] | 0.374278 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.0318569 | 2.13041 | True | True | [0.822329, 1.109111, 1.395893] | 0.626361 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.131899 | 2.95545 | True | True | [0.963934, 0.963934, 0.963934] | 0.671746 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.0153802 | 0.176646 | True | False | [1.926453, 2.041834, 2.157214] | 0.73261 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 1.61227 | 7.1456 | True | False | [1.831788, 1.831788, 1.831788] | 0.846664 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 11.6542 | 19.576 | True | False | [1.531799, 1.531799, 1.531799] | 0.910042 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.00208441 | 0.00208441 | True | False | [1.726433, 1.726433, 1.726433] | 0.998688 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.00556802 | 0.961425 | True | True | [1.149769, 1.149769, 1.149769] | 0.701274 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.0152666 | 4.40153 | True | True | [1.392145, 1.392145, 1.392145] | 1.03198 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.0880271 | 0.0147885 | True | False | [1.361366, 1.361366, 1.361366] | 0.420953 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00572426 | 0.00951338 | True | False | [1.610874, 1.610874, 1.610874] | 0.982406 |

Geometry update 20000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00114549 | 1.29238 | True | True | [1.017599, 1.256152, 1.480656] | 0.298217 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00233661 | 0.807365 | True | True | [1.075515, 1.075515, 1.075515] | 0.390215 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00673809 | 1.48183 | True | True | [1.052755, 1.052755, 1.052755] | 0.425236 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.0705164 | 3.83063 | True | True | [2.358771, 2.358771, 2.358771] | 0.640949 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.00401437 | 4.30397 | True | True | [2.441556, 2.441556, 2.441556] | 0.215695 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.000858821 | 3.35639 | True | True | [1.158484, 1.158484, 1.158484] | 0.391512 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.00405284 | 2.01963 | True | True | [2.0099, 2.0099, 2.0099] | 0.417301 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.000733105 | 0.0990714 | True | False | [0.87523, 0.87523, 0.87523] | 0.288777 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0167124 | 2.5076 | True | True | [0.835168, 0.879984, 1.270093] | 0.353982 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00506842 | 0.055361 | True | False | [0.845684, 0.931364, 1.017044] | 0.603385 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.2189 | 2.95038 | True | True | [1.143816, 1.143816, 1.143816] | 0.65484 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00748178 | 0.766426 | True | True | [2.088896, 2.223958, 2.35902] | 0.909973 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 3.09416 | 4.34061 | True | False | [1.972335, 1.972335, 1.972335] | 0.995608 |
| [6, 13] | 1 / 1 | 2/2 | 1 | 3.40927e-05 | 14.5129 | True | True | [1.896598, 1.896598, 1.896598] | 1.19184 |
| [7, 8] | 1 / 1 | 0/2 | 0 | 7.63114 | 7.63114 | True | False | [1.278206, 1.278206, 1.278206] | 0.904526 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.00672347 | 3.12949 | True | True | [0.997325, 0.997325, 0.997325] | 0.57911 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.00481864 | 5.75906 | True | True | [1.644307, 1.644307, 1.644307] | 1.02767 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.0666583 | 0.144643 | True | False | [1.406095, 1.406095, 1.406095] | 0.692379 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00235092 | 0.292398 | True | False | [1.688344, 1.688344, 1.688344] | 1.19627 |

### noise_raw_sampled_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 87/930 | 0/23505 | 412/930 | 201/23505 |
| 1 | 83/930 | 1/23505 | 421/930 | 212/23505 |
| 2 | 85/930 | 0/23505 | 450/930 | 196/23505 |
| 3 | 89/930 | 1/23505 | 430/930 | 190/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09801 / 1.03746 | 0.0838734 | 0.219704 | 1944 | 0/24435 |
| 1000 | 1.04098 / 1.03842 | 0.00416519 | 0.204417 | 1727 | 0/24435 |
| 2000 | 1.03942 / 1.03792 | 0.00243135 | 0.0862231 | 772 | 0/24435 |
| 5000 | 1.0416 / 1.04087 | 0.00146666 | 0.0715554 | 154 | 0/24435 |
| 10000 | 1.03836 / 1.03777 | 0.0010893 | 0.240449 | 222 | 0/24435 |
| 15000 | 1.04119 / 1.04079 | 0.000799959 | 0.236202 | 207 | 0/24435 |
| 20000 | 1.03984 / 1.03919 | 0.00095705 | 0.0664272 | 87 | 0/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 2, 'non_deviating': 10, 'recurrence_associated': 0, 'unresolved': 6}; chronology: {'COINCIDENT': 2, 'NO_OBSERVED_CONSTITUENT_ERROR': 16, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

Geometry update 0: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 5/6 | 0.833333 | 1.27673 | 1.56441 | True | False | [1.346246, 1.679678, 1.731386] | 1.03636 |
| [0, 9] | 11 / 1 | 1/2 | 0.5 | 4.39138 | 6.24405 | True | False | [1.211836, 1.211836, 1.211836] | 0.694701 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.297547 | 0.119481 | True | False | [1.778968, 1.778968, 1.778968] | 1.07224 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.494929 | 4.11428 | True | True | [0.770839, 0.770839, 0.770839] | 0.62218 |
| [0, 18] | 2 / 1 | 1/2 | 0.5 | 0.872779 | 3.4263 | True | False | [0.751063, 0.751063, 0.751063] | 0.629517 |
| [2, 6] | 13 / 1 | 1/2 | 0.5 | 0.539338 | 0.552786 | True | False | [1.140025, 1.140025, 1.140025] | 0.964331 |
| [2, 14] | 2 / 1 | 1/2 | 0.5 | 3.95328 | 2.80571 | True | False | [1.512306, 1.512306, 1.512306] | 0.897433 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.0215694 | 1.19701 | True | True | [1.006227, 1.006227, 1.006227] | 0.743299 |
| [3, 8] | 8 / 3 | 4/6 | 0.666667 | 1.80627 | 3.31532 | True | False | [0.449837, 0.822673, 1.13276] | 0.641845 |
| [4, 8] | 12 / 2 | 2/4 | 0.5 | 1.42785 | 1.05419 | True | False | [1.137567, 1.194474, 1.25138] | 0.826751 |
| [4, 11] | 2 / 1 | 1/2 | 0.5 | 8.13259 | 4.50872 | True | False | [0.638306, 0.638306, 0.638306] | 0.829677 |
| [4, 17] | 3 / 2 | 3/4 | 0.75 | 0.736376 | 2.80407 | True | False | [0.843669, 0.978339, 1.113009] | 0.735421 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 6.69699 | 15.7326 | True | False | [0.870327, 0.870327, 0.870327] | 0.954495 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 16.5321 | 29.9554 | True | False | [1.77879, 1.77879, 1.77879] | 1.32927 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.0210535 | 0.0210535 | True | False | [1.059384, 1.059384, 1.059384] | 0.812214 |
| [8, 9] | 9 / 1 | 1/2 | 0.5 | 4.31905 | 1.37121 | True | False | [0.474966, 0.474966, 0.474966] | 0.952046 |
| [8, 14] | 2 / 1 | 1/2 | 0.5 | 0.828668 | 1.19246 | True | False | [0.694765, 0.694765, 0.694765] | 0.933905 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.149754 | 1.9337 | True | True | [0.878752, 0.878752, 0.878752] | 0.677429 |
| [13, 17] | 5 / 1 | 1/2 | 0.5 | 1.76244 | 6.90772 | True | False | [0.896102, 0.896102, 0.896102] | 0.820072 |

Geometry update 5000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00442721 | 0.847184 | True | True | [0.848225, 1.342014, 1.425529] | 0.437648 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.000715284 | 0.7748 | True | True | [1.479383, 1.479383, 1.479383] | 0.430258 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00417528 | 3.73669 | True | True | [1.472395, 1.472395, 1.472395] | 0.671786 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.006037 | 5.61515 | True | True | [2.050197, 2.050197, 2.050197] | 0.45852 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.0123864 | 2.57849 | True | True | [2.444191, 2.444191, 2.444191] | 0.381571 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.00635727 | 1.40062 | True | True | [0.772536, 0.772536, 0.772536] | 0.557564 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.0196916 | 3.79074 | True | True | [1.750409, 1.750409, 1.750409] | 0.552363 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00200328 | 0.402371 | True | False | [0.59734, 0.59734, 0.59734] | 0.237017 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0107523 | 1.50743 | True | True | [0.869336, 1.014641, 1.148964] | 0.363433 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00831757 | 2.10044 | True | True | [1.260306, 1.289425, 1.318543] | 0.618941 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.0324077 | 3.74144 | True | True | [1.461246, 1.461246, 1.461246] | 0.902677 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00538073 | 0.741853 | True | True | [2.076729, 2.090716, 2.104704] | 0.730889 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 1.77045 | 3.3164 | True | False | [1.695151, 1.695151, 1.695151] | 0.822515 |
| [6, 13] | 1 / 1 | 2/2 | 1 | 0.000592877 | 7.69836 | True | True | [2.066188, 2.066188, 2.066188] | 0.988 |
| [7, 8] | 1 / 1 | 1/2 | 0.5 | 2.23512 | 2.23512 | True | False | [1.456251, 1.456251, 1.456251] | 1.06296 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.0958625 | 1.88291 | True | True | [1.020448, 1.020448, 1.020448] | 0.603913 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.185657 | 2.02665 | True | True | [1.288741, 1.288741, 1.288741] | 0.947013 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.178313 | 0.0337492 | True | False | [1.589149, 1.589149, 1.589149] | 0.632665 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00850373 | 0.00393603 | True | False | [1.492085, 1.492085, 1.492085] | 0.773055 |

Geometry update 20000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00192386 | 1.83775 | True | True | [1.012817, 1.17179, 1.275621] | 0.299722 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00310506 | 0.568 | True | True | [1.371615, 1.371615, 1.371615] | 0.481591 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00253198 | 5.20496 | True | True | [1.320887, 1.320887, 1.320887] | 0.429174 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.027327 | 1.68426 | True | True | [2.206346, 2.206346, 2.206346] | 0.619944 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.0216652 | 5.37814 | True | True | [2.557117, 2.557117, 2.557117] | 0.313168 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.0017048 | 6.95249 | True | True | [1.116325, 1.116325, 1.116325] | 0.471814 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.00852451 | 1.9649 | True | True | [1.775523, 1.775523, 1.775523] | 0.321451 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00202914 | 4.14753 | True | True | [0.720191, 0.720191, 0.720191] | 0.175546 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0036217 | 2.39794 | True | True | [0.967599, 1.159646, 1.179523] | 0.288394 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00971284 | 0.889251 | True | True | [1.064255, 1.169759, 1.275263] | 0.560245 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.00743496 | 4.90598 | True | True | [1.813447, 1.813447, 1.813447] | 0.904769 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00475683 | 3.33037 | True | True | [2.274584, 2.373832, 2.473081] | 0.775229 |
| [5, 15] | 1 / 1 | 2/2 | 1 | 0.00979988 | 4.63217 | True | True | [1.963613, 1.963613, 1.963613] | 0.910892 |
| [6, 13] | 1 / 1 | 0/2 | 0 | 24.0788 | 0.000146606 | True | False | [2.053022, 2.053022, 2.053022] | 1.00909 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.0305319 | 0.0305319 | True | False | [1.312799, 1.312799, 1.312799] | 0.866164 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.00792831 | 2.33994 | True | True | [1.203943, 1.203943, 1.203943] | 0.587741 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.0185069 | 4.06476 | True | True | [1.659941, 1.659941, 1.659941] | 0.938523 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.00143979 | 1.83124 | True | True | [1.712655, 1.712655, 1.712655] | 0.579154 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.0172828 | 0.877768 | True | True | [1.902956, 1.902956, 1.902956] | 1.08193 |

### noise_raw_probability_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 2/930 | 0/23505 | 12/930 | 0/23505 |
| 1 | 1/930 | 0/23505 | 15/930 | 0/23505 |
| 2 | 0/930 | 0/23505 | 9/930 | 0/23505 |
| 3 | 2/930 | 0/23505 | 16/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09968 / 1.03972 | 0.087358 | 0.216547 | 24326 | 0/24435 |
| 1000 | 1.04 / 1.03972 | 0.000654721 | 0.157874 | 326 | 0/24435 |
| 2000 | 1.03982 / 1.03972 | 0.000243515 | 0.049831 | 59 | 0/24435 |
| 5000 | 1.03975 / 1.03972 | 6.68546e-05 | 0.00954078 | 13 | 0/24435 |
| 10000 | 1.03982 / 1.03972 | 0.000124201 | 0.0287076 | 89 | 0/24435 |
| 15000 | 1.03974 / 1.03972 | 1.30782e-05 | 0.0181874 | 2 | 0/24435 |
| 20000 | 1.03972 / 1.03972 | 7.82475e-06 | 0.0221688 | 2 | 0/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 17, 'recurrence_associated': 0, 'unresolved': 1}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

Geometry update 0: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 4/6 | 0.666667 | 0.895787 | 0.955128 | True | False | [1.134452, 1.168728, 1.37725] | 0.840998 |
| [0, 9] | 11 / 1 | 1/2 | 0.5 | 0.880587 | 5.3551 | True | False | [2.051162, 2.051162, 2.051162] | 1.04385 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.0717982 | 0.00157313 | True | False | [1.608514, 1.608514, 1.608514] | 1.01837 |
| [0, 17] | 4 / 1 | 1/2 | 0.5 | 2.25931 | 0.0744683 | True | False | [1.240709, 1.240709, 1.240709] | 0.688191 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.0424525 | 0.905078 | True | True | [1.339795, 1.339795, 1.339795] | 0.525062 |
| [2, 6] | 13 / 1 | 1/2 | 0.5 | 4.22832 | 0.815448 | True | False | [1.073914, 1.073914, 1.073914] | 0.884173 |
| [2, 14] | 2 / 1 | 1/2 | 0.5 | 1.8019 | 5.86295 | True | False | [1.277372, 1.277372, 1.277372] | 0.675015 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.148106 | 0.540367 | True | True | [1.247568, 1.247568, 1.247568] | 0.756113 |
| [3, 8] | 8 / 3 | 4/6 | 0.666667 | 0.928824 | 0.833973 | True | False | [0.687204, 1.134637, 1.370659] | 0.708158 |
| [4, 8] | 12 / 2 | 3/4 | 0.75 | 2.19783 | 1.59764 | True | False | [1.420333, 1.430125, 1.439918] | 0.899993 |
| [4, 11] | 2 / 1 | 1/2 | 0.5 | 3.53824 | 1.95413 | True | False | [1.568651, 1.568651, 1.568651] | 1.15403 |
| [4, 17] | 3 / 2 | 3/4 | 0.75 | 3.17177 | 7.39739 | True | False | [0.553632, 1.045477, 1.537322] | 0.885426 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 1.33366 | 5.75422 | True | False | [1.039575, 1.039575, 1.039575] | 1.11355 |
| [6, 13] | 1 / 1 | 0/2 | 0 | 192.538 | 0 | True | False | [1.187406, 1.187406, 1.187406] | 1.07062 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.266692 | 0.266692 | True | False | [1.215903, 1.215903, 1.215903] | 1.05753 |
| [8, 9] | 9 / 1 | 1/2 | 0.5 | 4.92791 | 1.3848 | True | False | [0.902435, 0.902435, 0.902435] | 0.96547 |
| [8, 14] | 2 / 1 | 1/2 | 0.5 | 0.789695 | 3.34822 | True | False | [0.722873, 0.722873, 0.722873] | 1.2194 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.0933378 | 0.06345 | True | False | [1.205501, 1.205501, 1.205501] | 0.678195 |
| [13, 17] | 5 / 1 | 1/2 | 0.5 | 5.17502 | 0.0297856 | True | False | [0.823121, 0.823121, 0.823121] | 0.783473 |

Geometry update 5000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00216914 | 0.934552 | True | True | [0.916704, 1.066506, 1.26075] | 0.303727 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00232207 | 0.284114 | True | False | [1.584688, 1.584688, 1.584688] | 0.417778 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00284698 | 0.0053569 | True | False | [1.439147, 1.439147, 1.439147] | 0.510579 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00245949 | 0.292629 | True | False | [2.255836, 2.255836, 2.255836] | 0.48626 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.00740603 | 0.0276994 | True | False | [2.727359, 2.727359, 2.727359] | 0.36401 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.0130785 | 1.11462 | True | True | [1.073089, 1.073089, 1.073089] | 0.230996 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.0116257 | 6.60386 | True | True | [2.030447, 2.030447, 2.030447] | 0.386574 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00142702 | 0.283085 | True | False | [0.956265, 0.956265, 0.956265] | 0.261099 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0119645 | 2.0749 | True | True | [0.899851, 0.927673, 0.995379] | 0.339622 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00568482 | 0.0441988 | True | False | [1.051776, 1.213837, 1.375898] | 0.599301 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.238829 | 2.68322 | True | True | [1.380579, 1.380579, 1.380579] | 0.686789 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00468569 | 1.2271 | True | True | [2.209941, 2.239758, 2.269574] | 0.776403 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 0.800631 | 3.16328 | True | False | [1.69107, 1.69107, 1.69107] | 0.791103 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 0.500231 | 2.18937 | True | False | [1.775366, 1.775366, 1.775366] | 0.818661 |
| [7, 8] | 1 / 1 | 0/2 | 0 | 33.4426 | 33.4426 | True | False | [1.025503, 1.025503, 1.025503] | 0.79151 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.0135099 | 2.25807 | True | True | [1.113624, 1.113624, 1.113624] | 0.579411 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.0262509 | 4.61387 | True | True | [1.263581, 1.263581, 1.263581] | 0.951591 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.107768 | 0.136496 | True | False | [1.164521, 1.164521, 1.164521] | 0.429275 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00959272 | 0.0119079 | True | False | [1.336416, 1.336416, 1.336416] | 0.926149 |

Geometry update 20000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00131249 | 1.27964 | True | True | [1.028583, 1.096428, 1.195224] | 0.212046 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00282354 | 0.749713 | True | True | [1.242488, 1.242488, 1.242488] | 0.350634 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.005445 | 1.83643 | True | True | [1.059159, 1.059159, 1.059159] | 0.362166 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.0139852 | 0.164479 | True | False | [2.210181, 2.210181, 2.210181] | 0.511851 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.00469056 | 4.55902 | True | True | [2.682959, 2.682959, 2.682959] | 0.211612 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.000656382 | 0.0956095 | True | False | [1.240128, 1.240128, 1.240128] | 0.250316 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.00717365 | 7.82068 | True | True | [2.079304, 2.079304, 2.079304] | 0.256315 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00140789 | 1.37109 | True | True | [0.895236, 0.895236, 0.895236] | 0.284923 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.00298315 | 1.3172 | True | True | [1.092987, 1.175491, 1.504616] | 0.346963 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00620043 | 0.266592 | True | True | [0.711779, 0.791108, 0.870438] | 0.572891 |
| [4, 11] | 2 / 1 | 1/2 | 0.5 | 1.14911 | 2.39895 | True | False | [1.073944, 1.073944, 1.073944] | 0.739242 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00609916 | 0.85217 | True | True | [1.970136, 1.995954, 2.021772] | 0.77933 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 6.0588 | 1.42483 | True | False | [1.970457, 1.970457, 1.970457] | 1.01126 |
| [6, 13] | 1 / 1 | 2/2 | 1 | 0.000458924 | 56.8336 | True | True | [1.689895, 1.689895, 1.689895] | 0.919099 |
| [7, 8] | 1 / 1 | 1/2 | 0.5 | 6.36561 | 6.36561 | True | False | [1.305069, 1.305069, 1.305069] | 0.918137 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.00417302 | 0.271867 | True | False | [1.17509, 1.17509, 1.17509] | 0.632123 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.0910473 | 3.13534 | True | True | [1.345197, 1.345197, 1.345197] | 0.99492 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.28136 | 0.158171 | True | False | [1.386428, 1.386428, 1.386428] | 0.586846 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00235603 | 0.103035 | True | False | [1.823361, 1.823361, 1.823361] | 1.03367 |

### noise_raw_probability_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 1/930 | 0/23505 | 8/930 | 0/23505 |
| 1 | 1/930 | 0/23505 | 12/930 | 1/23505 |
| 2 | 2/930 | 0/23505 | 10/930 | 0/23505 |
| 3 | 1/930 | 0/23505 | 14/930 | 0/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.08859 / 1.03972 | 0.0671472 | 0.206921 | 23817 | 0/24435 |
| 1000 | 1.03989 / 1.03972 | 0.000330919 | 0.0684324 | 152 | 0/24435 |
| 2000 | 1.03976 / 1.03972 | 6.36844e-05 | 0.148488 | 19 | 0/24435 |
| 5000 | 1.03975 / 1.03972 | 1.85924e-05 | 0.00848132 | 5 | 0/24435 |
| 10000 | 1.03973 / 1.03972 | 2.12322e-05 | 0.0101988 | 1 | 0/24435 |
| 15000 | 1.03973 / 1.03972 | 1.30742e-05 | 0.0148469 | 1 | 0/24435 |
| 20000 | 1.03973 / 1.03972 | 8.29438e-06 | 0.0136854 | 1 | 0/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 18, 'recurrence_associated': 0, 'unresolved': 0}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

Geometry update 0: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 4/6 | 0.666667 | 0.619432 | 0.360189 | True | False | [1.10463, 1.315478, 1.442413] | 0.885242 |
| [0, 9] | 11 / 1 | 1/2 | 0.5 | 1.10397 | 2.56826 | True | False | [1.254778, 1.254778, 1.254778] | 1.13128 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.308432 | 0.0364723 | True | False | [1.670705, 1.670705, 1.670705] | 0.790128 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00447195 | 0.704098 | True | True | [1.43509, 1.43509, 1.43509] | 0.688557 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.155452 | 1.16853 | True | True | [1.726676, 1.726676, 1.726676] | 0.629646 |
| [2, 6] | 13 / 1 | 1/2 | 0.5 | 2.24277 | 1.8586 | True | False | [1.190346, 1.190346, 1.190346] | 0.972077 |
| [2, 14] | 2 / 1 | 1/2 | 0.5 | 1.17389 | 0.0832449 | True | False | [0.888175, 0.888175, 0.888175] | 0.869838 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00105993 | 0.134084 | True | False | [1.567079, 1.567079, 1.567079] | 0.85511 |
| [3, 8] | 8 / 3 | 4/6 | 0.666667 | 0.548217 | 2.03218 | True | False | [0.758073, 1.164194, 1.271011] | 0.788796 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.0659835 | 1.02224 | True | True | [1.144007, 1.159507, 1.175007] | 0.78428 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.355672 | 1.83221 | True | True | [1.059908, 1.059908, 1.059908] | 0.955426 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.0774318 | 1.64131 | True | True | [0.907198, 1.212593, 1.517988] | 0.725521 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 3.56247 | 5.87577 | True | False | [0.903418, 0.903418, 0.903418] | 1.07291 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 0.382188 | 4.15969 | True | False | [1.197203, 1.197203, 1.197203] | 1.18571 |
| [7, 8] | 1 / 1 | 1/2 | 0.5 | 15.7097 | 15.7097 | True | False | [1.110225, 1.110225, 1.110225] | 0.97057 |
| [8, 9] | 9 / 1 | 1/2 | 0.5 | 5.44418 | 3.13656 | True | False | [0.676475, 0.676475, 0.676475] | 0.980368 |
| [8, 14] | 2 / 1 | 1/2 | 0.5 | 4.0181 | 2.94043 | True | False | [0.423279, 0.423279, 0.423279] | 0.788909 |
| [10, 14] | 3 / 1 | 1/2 | 0.5 | 4.32921 | 1.98098 | True | False | [0.625481, 0.625481, 0.625481] | 0.601174 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.016931 | 0.0146049 | True | False | [1.336739, 1.336739, 1.336739] | 0.972161 |

Geometry update 5000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00164686 | 1.22096 | True | True | [0.584096, 0.723974, 0.820951] | 0.215837 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00184436 | 1.3208 | True | True | [1.355493, 1.355493, 1.355493] | 0.558342 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00300109 | 0.251101 | True | False | [1.14909, 1.14909, 1.14909] | 0.369237 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00212469 | 1.23624 | True | True | [2.466549, 2.466549, 2.466549] | 0.486194 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.00635765 | 4.03015 | True | True | [2.656983, 2.656983, 2.656983] | 0.208787 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.00377331 | 1.70084 | True | True | [0.570858, 0.570858, 0.570858] | 0.300141 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.00999802 | 1.84078 | True | True | [1.717801, 1.717801, 1.717801] | 0.478987 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00240365 | 0.400457 | True | False | [0.902282, 0.902282, 0.902282] | 0.173029 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.00698023 | 0.762892 | True | True | [0.82847, 1.047186, 1.488149] | 0.312343 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.015964 | 0.329035 | True | True | [0.447184, 0.643405, 0.839626] | 0.486059 |
| [4, 11] | 2 / 1 | 1/2 | 0.5 | 0.572752 | 2.26912 | True | False | [0.990034, 0.990034, 0.990034] | 0.625625 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00666371 | 0.216075 | True | True | [1.971845, 2.199266, 2.426688] | 0.831833 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 2.29877 | 8.58222 | True | False | [1.821895, 1.821895, 1.821895] | 0.83116 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 1.44405 | 1.47363 | True | False | [1.438817, 1.438817, 1.438817] | 0.816239 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.000824329 | 0.000824329 | True | False | [1.219586, 1.219586, 1.219586] | 0.921512 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.205622 | 3.63138 | True | True | [1.025024, 1.025024, 1.025024] | 0.710689 |
| [8, 14] | 2 / 1 | 1/2 | 0.5 | 1.27692 | 3.44434 | True | False | [1.315596, 1.315596, 1.315596] | 0.837648 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.0720824 | 0.873842 | True | True | [1.408032, 1.408032, 1.408032] | 0.532628 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00527129 | 0.0152187 | True | False | [1.545526, 1.545526, 1.545526] | 0.858286 |

Geometry update 20000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.000986837 | 1.59999 | True | True | [0.876069, 1.064207, 1.28886] | 0.210689 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.0025009 | 1.0154 | True | True | [1.50323, 1.50323, 1.50323] | 0.5867 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00323564 | 0.683339 | True | True | [1.171527, 1.171527, 1.171527] | 0.364288 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00194566 | 0.140909 | True | False | [2.599275, 2.599275, 2.599275] | 0.620779 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.0010703 | 2.19394 | True | True | [3.123384, 3.123384, 3.123384] | 0.298648 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.00286026 | 2.19648 | True | True | [0.950217, 0.950217, 0.950217] | 0.36225 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.00613262 | 2.72612 | True | True | [1.955549, 1.955549, 1.955549] | 0.418125 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00100239 | 0.586193 | True | True | [0.763351, 0.763351, 0.763351] | 0.156714 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.0199513 | 1.91111 | True | True | [0.497225, 0.85764, 1.239167] | 0.296878 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.00635299 | 0.639359 | True | True | [0.427592, 0.603835, 0.780077] | 0.49634 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.0171329 | 4.67559 | True | True | [1.238315, 1.238315, 1.238315] | 0.596533 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00547956 | 0.234167 | True | True | [2.005119, 2.195311, 2.385503] | 0.865364 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 22.8 | 15.6704 | True | False | [1.843131, 1.843131, 1.843131] | 0.934231 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 3.1311 | 0.5921 | True | False | [1.738777, 1.738777, 1.738777] | 1.00529 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.0587375 | 0.0587375 | True | False | [1.366853, 1.366853, 1.366853] | 0.887635 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.00566417 | 1.26129 | True | True | [0.97453, 0.97453, 0.97453] | 0.782051 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.107133 | 3.03236 | True | True | [1.316592, 1.316592, 1.316592] | 0.945761 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.110579 | 0.787089 | True | True | [1.248086, 1.248086, 1.248086] | 0.414532 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00464809 | 0.0169885 | True | False | [2.043064, 2.043064, 2.043064] | 1.09424 |

### noise_raw_probability_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 120/930 | 29/23505 | 248/930 | 76/23505 |
| 1 | 145/930 | 31/23505 | 264/930 | 76/23505 |
| 2 | 126/930 | 35/23505 | 236/930 | 94/23505 |
| 3 | 129/930 | 25/23505 | 267/930 | 85/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09847 / 1.03972 | 0.0838734 | 0.219704 | 1944 | 0/24435 |
| 1000 | 1.03998 / 1.03972 | 0.000510075 | 0.0458169 | 142 | 0/24435 |
| 2000 | 1.03981 / 1.03972 | 0.00016033 | 0.0423217 | 17 | 0/24435 |
| 5000 | 1.03974 / 1.03972 | 8.27599e-05 | 0.07037 | 3 | 0/24435 |
| 10000 | 1.03974 / 1.03972 | 7.39233e-06 | 0.00624785 | 2 | 0/24435 |
| 15000 | 1.03972 / 1.03972 | 6.16516e-06 | 0.00517453 | 2 | 0/24435 |
| 20000 | 1.03996 / 1.03972 | 0.000348789 | 0.1404 | 149 | 0/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 15, 'recurrence_associated': 0, 'unresolved': 2}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

Geometry update 0: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 5/6 | 0.833333 | 1.27673 | 1.56441 | True | False | [1.346246, 1.679678, 1.731386] | 1.03636 |
| [0, 9] | 11 / 1 | 1/2 | 0.5 | 4.39138 | 6.24405 | True | False | [1.211836, 1.211836, 1.211836] | 0.694701 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.297547 | 0.119481 | True | False | [1.778968, 1.778968, 1.778968] | 1.07224 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.494929 | 4.11428 | True | True | [0.770839, 0.770839, 0.770839] | 0.62218 |
| [0, 18] | 2 / 1 | 1/2 | 0.5 | 0.872779 | 3.4263 | True | False | [0.751063, 0.751063, 0.751063] | 0.629517 |
| [2, 6] | 13 / 1 | 1/2 | 0.5 | 0.539338 | 0.552786 | True | False | [1.140025, 1.140025, 1.140025] | 0.964331 |
| [2, 14] | 2 / 1 | 1/2 | 0.5 | 3.95328 | 2.80571 | True | False | [1.512306, 1.512306, 1.512306] | 0.897433 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.0215694 | 1.19701 | True | True | [1.006227, 1.006227, 1.006227] | 0.743299 |
| [3, 8] | 8 / 3 | 4/6 | 0.666667 | 1.80627 | 3.31532 | True | False | [0.449837, 0.822673, 1.13276] | 0.641845 |
| [4, 8] | 12 / 2 | 2/4 | 0.5 | 1.42785 | 1.05419 | True | False | [1.137567, 1.194474, 1.25138] | 0.826751 |
| [4, 11] | 2 / 1 | 1/2 | 0.5 | 8.13259 | 4.50872 | True | False | [0.638306, 0.638306, 0.638306] | 0.829677 |
| [4, 17] | 3 / 2 | 3/4 | 0.75 | 0.736376 | 2.80407 | True | False | [0.843669, 0.978339, 1.113009] | 0.735421 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 6.69699 | 15.7326 | True | False | [0.870327, 0.870327, 0.870327] | 0.954495 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 16.5321 | 29.9554 | True | False | [1.77879, 1.77879, 1.77879] | 1.32927 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.0210535 | 0.0210535 | True | False | [1.059384, 1.059384, 1.059384] | 0.812214 |
| [8, 9] | 9 / 1 | 1/2 | 0.5 | 4.31905 | 1.37121 | True | False | [0.474966, 0.474966, 0.474966] | 0.952046 |
| [8, 14] | 2 / 1 | 1/2 | 0.5 | 0.828668 | 1.19246 | True | False | [0.694765, 0.694765, 0.694765] | 0.933905 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.149754 | 1.9337 | True | True | [0.878752, 0.878752, 0.878752] | 0.677429 |
| [13, 17] | 5 / 1 | 1/2 | 0.5 | 1.76244 | 6.90772 | True | False | [0.896102, 0.896102, 0.896102] | 0.820072 |

Geometry update 5000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00268727 | 1.59647 | True | True | [0.928917, 1.174718, 1.187554] | 0.358471 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.00175307 | 1.83414 | True | True | [1.936984, 1.936984, 1.936984] | 0.596265 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.00440795 | 2.30117 | True | True | [1.042009, 1.042009, 1.042009] | 0.503804 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.00225634 | 4.77762 | True | True | [2.128563, 2.128563, 2.128563] | 0.380873 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.00452282 | 1.29257 | True | True | [2.902352, 2.902352, 2.902352] | 0.302765 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.00342062 | 2.91008 | True | True | [0.879384, 0.879384, 0.879384] | 0.398315 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.0113874 | 3.9202 | True | True | [1.82466, 1.82466, 1.82466] | 0.396117 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.0152571 | 0.543364 | True | True | [0.689911, 0.689911, 0.689911] | 0.235081 |
| [3, 8] | 8 / 3 | 5/6 | 0.833333 | 0.187643 | 0.354574 | True | False | [0.581616, 0.768059, 1.184249] | 0.353779 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.0208064 | 2.27944 | True | True | [0.705698, 0.721077, 0.736456] | 0.523055 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.0293686 | 3.75338 | True | True | [1.645137, 1.645137, 1.645137] | 0.826752 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.00991247 | 1.97986 | True | True | [2.114654, 2.142107, 2.169561] | 0.647562 |
| [5, 15] | 1 / 1 | 2/2 | 1 | 0.0437694 | 3.34255 | True | True | [1.868247, 1.868247, 1.868247] | 0.819211 |
| [6, 13] | 1 / 1 | 2/2 | 1 | 0.140721 | 3.83473 | True | True | [1.556376, 1.556376, 1.556376] | 0.793463 |
| [7, 8] | 1 / 1 | 1/2 | 0.5 | 34.3464 | 34.3464 | True | False | [1.066689, 1.066689, 1.066689] | 0.793592 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.0126522 | 1.12202 | True | True | [1.213066, 1.213066, 1.213066] | 0.628519 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.084414 | 2.86196 | True | True | [1.586262, 1.586262, 1.586262] | 0.762555 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.269574 | 0.156023 | True | False | [1.586737, 1.586737, 1.586737] | 0.534133 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.0207431 | 0.0090337 | True | False | [1.33415, 1.33415, 1.33415] | 0.77207 |

Geometry update 20000: calibration CALIBRATED; 19 measured, 578 missing. Critical absent support: [{'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [12, 13], 'train_pairs': 4}, {'heldout_pairs': 0, 'status': 'MISSING_SUPPORT', 'sums': [23, 24], 'train_pairs': 1}]. The complete missing pair inventory is in the hash-bound detailed JSON.

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [0, 6] | 18 / 3 | 6/6 | 1 | 0.00153842 | 0.822837 | True | True | [0.87193, 1.030887, 1.213582] | 0.226865 |
| [0, 9] | 11 / 1 | 2/2 | 1 | 0.0013632 | 0.474391 | True | False | [1.983395, 1.983395, 1.983395] | 0.703069 |
| [0, 10] | 4 / 1 | 2/2 | 1 | 0.0152684 | 4.17076 | True | True | [1.153184, 1.153184, 1.153184] | 0.426298 |
| [0, 17] | 4 / 1 | 2/2 | 1 | 0.0156922 | 2.50132 | True | True | [2.116194, 2.116194, 2.116194] | 0.573568 |
| [0, 18] | 2 / 1 | 2/2 | 1 | 0.00580168 | 1.35901 | True | True | [2.830781, 2.830781, 2.830781] | 0.266425 |
| [2, 6] | 13 / 1 | 2/2 | 1 | 0.000542844 | 1.89657 | True | True | [0.897274, 0.897274, 0.897274] | 0.383349 |
| [2, 14] | 2 / 1 | 2/2 | 1 | 0.0830581 | 5.94798 | True | True | [1.813879, 1.813879, 1.813879] | 0.238836 |
| [3, 4] | 15 / 1 | 2/2 | 1 | 0.00232846 | 0.501915 | True | True | [1.008647, 1.008647, 1.008647] | 0.259112 |
| [3, 8] | 8 / 3 | 6/6 | 1 | 0.00654668 | 1.05259 | True | False | [0.77687, 0.833408, 1.496501] | 0.370294 |
| [4, 8] | 12 / 2 | 4/4 | 1 | 0.0174532 | 0.119921 | True | False | [0.781091, 0.854198, 0.927305] | 0.57579 |
| [4, 11] | 2 / 1 | 2/2 | 1 | 0.00296155 | 7.62082 | True | True | [1.758828, 1.758828, 1.758828] | 0.920929 |
| [4, 17] | 3 / 2 | 4/4 | 1 | 0.0189858 | 0.683374 | True | True | [2.040509, 2.149144, 2.25778] | 0.857901 |
| [5, 15] | 1 / 1 | 1/2 | 0.5 | 20.875 | 7.07961 | True | False | [1.788324, 1.788324, 1.788324] | 0.995021 |
| [6, 13] | 1 / 1 | 1/2 | 0.5 | 2.34964 | 1.90565 | True | False | [1.812023, 1.812023, 1.812023] | 0.924489 |
| [7, 8] | 1 / 1 | 2/2 | 1 | 0.170386 | 0.170386 | True | False | [1.560613, 1.560613, 1.560613] | 0.956407 |
| [8, 9] | 9 / 1 | 2/2 | 1 | 0.00430938 | 2.56393 | True | True | [1.200786, 1.200786, 1.200786] | 0.883806 |
| [8, 14] | 2 / 1 | 2/2 | 1 | 0.0343749 | 3.49979 | True | True | [1.447498, 1.447498, 1.447498] | 1.1654 |
| [10, 14] | 3 / 1 | 2/2 | 1 | 0.0320591 | 0.164334 | True | False | [1.678391, 1.678391, 1.678391] | 0.585238 |
| [13, 17] | 5 / 1 | 2/2 | 1 | 0.00380306 | 0.14619 | True | False | [2.193099, 2.193099, 2.193099] | 1.14702 |

### noise_sums_sampled_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 241/930 | 232/23505 | 641/930 | 1247/23505 |
| 1 | 231/930 | 248/23505 | 640/930 | 1258/23505 |
| 2 | 229/930 | 221/23505 | 641/930 | 1236/23505 |
| 3 | 230/930 | 229/23505 | 650/930 | 1269/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09978 / 1.03922 | 0.087358 | 0.216547 | 24326 | 0/24435 |
| 1000 | 1.04571 / 1.03842 | 0.0127277 | 0.17672 | 12609 | 4764/24435 |
| 2000 | 1.04596 / 1.04169 | 0.0072585 | 0.123806 | 4689 | 8744/24435 |
| 5000 | 1.04029 / 1.03861 | 0.00489496 | 0.185429 | 1405 | 14185/24435 |
| 10000 | 1.04387 / 1.04253 | 0.00234008 | 0.0996994 | 635 | 17161/24435 |
| 15000 | 1.03997 / 1.03906 | 0.00199364 | 0.143839 | 861 | 18506/24435 |
| 20000 | 1.03963 / 1.03876 | 0.00158984 | 0.0649652 | 473 | 19269/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 6, 'recurrence_associated': 0, 'unresolved': 11}; chronology: {'COINCIDENT': 1, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### noise_sums_sampled_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 476/930 | 172/23505 | 644/930 | 2142/23505 |
| 1 | 469/930 | 209/23505 | 648/930 | 2140/23505 |
| 2 | 473/930 | 166/23505 | 645/930 | 2182/23505 |
| 3 | 460/930 | 191/23505 | 651/930 | 2143/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.08859 / 1.03996 | 0.0671472 | 0.206921 | 23817 | 0/24435 |
| 1000 | 1.04398 / 1.038 | 0.0128634 | 0.153937 | 6186 | 3929/24435 |
| 2000 | 1.04122 / 1.03765 | 0.00639988 | 0.164567 | 1397 | 7269/24435 |
| 5000 | 1.04295 / 1.04095 | 0.00366104 | 0.0907466 | 787 | 14322/24435 |
| 10000 | 1.03849 / 1.03737 | 0.00239937 | 0.189056 | 459 | 17938/24435 |
| 15000 | 1.0402 / 1.03919 | 0.00215209 | 0.0798246 | 631 | 19578/24435 |
| 20000 | 1.04231 / 1.04123 | 0.00200439 | 0.132952 | 648 | 20516/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage', 'Upper recurrence remains a limitation']. Counts: {'board_associated': 2, 'non_deviating': 0, 'recurrence_associated': 2, 'unresolved': 14}; chronology: {'COINCIDENT': 2, 'NO_OBSERVED_CONSTITUENT_ERROR': 16, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### noise_sums_sampled_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 442/930 | 373/23505 | 921/930 | 3351/23505 |
| 1 | 435/930 | 375/23505 | 925/930 | 3309/23505 |
| 2 | 445/930 | 386/23505 | 923/930 | 3320/23505 |
| 3 | 445/930 | 387/23505 | 921/930 | 3326/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09801 / 1.03746 | 0.0838734 | 0.219704 | 1944 | 0/24435 |
| 1000 | 1.04568 / 1.03842 | 0.0139055 | 0.110382 | 5786 | 3762/24435 |
| 2000 | 1.04152 / 1.03792 | 0.00669563 | 0.220833 | 2108 | 7933/24435 |
| 5000 | 1.04258 / 1.04087 | 0.0030356 | 0.137254 | 695 | 13483/24435 |
| 10000 | 1.03907 / 1.03777 | 0.00257817 | 0.14153 | 540 | 16608/24435 |
| 15000 | 1.04178 / 1.04079 | 0.00207876 | 0.0710088 | 848 | 17913/24435 |
| 20000 | 1.04022 / 1.03919 | 0.00229812 | 0.0447989 | 815 | 19544/24435 |

Concurrent diagnosis: ['Board computation remains a candidate limitation after history coverage']. Counts: {'board_associated': 1, 'non_deviating': 1, 'recurrence_associated': 0, 'unresolved': 16}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 1}.

### noise_sums_probability_original_seed0

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 293/930 | 180/23505 | 571/930 | 2326/23505 |
| 1 | 284/930 | 197/23505 | 576/930 | 2261/23505 |
| 2 | 292/930 | 175/23505 | 571/930 | 2242/23505 |
| 3 | 288/930 | 190/23505 | 575/930 | 2260/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09968 / 1.03972 | 0.087358 | 0.216547 | 24326 | 0/24435 |
| 1000 | 1.04322 / 1.03972 | 0.00707033 | 0.226532 | 5444 | 5270/24435 |
| 2000 | 1.04147 / 1.03972 | 0.00377712 | 0.167105 | 2493 | 8418/24435 |
| 5000 | 1.04041 / 1.03972 | 0.00144145 | 0.22389 | 831 | 14041/24435 |
| 10000 | 1.04 / 1.03972 | 0.000602151 | 0.0783921 | 401 | 17714/24435 |
| 15000 | 1.03999 / 1.03972 | 0.000599215 | 0.0439092 | 631 | 19118/24435 |
| 20000 | 1.03997 / 1.03972 | 0.000585088 | 0.0370325 | 473 | 19921/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 11, 'recurrence_associated': 0, 'unresolved': 7}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### noise_sums_probability_original_seed1

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 76/930 | 324/23505 | 508/930 | 1853/23505 |
| 1 | 68/930 | 328/23505 | 502/930 | 1834/23505 |
| 2 | 71/930 | 325/23505 | 512/930 | 1897/23505 |
| 3 | 64/930 | 330/23505 | 514/930 | 1889/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.08859 / 1.03972 | 0.0671472 | 0.206921 | 23817 | 0/24435 |
| 1000 | 1.04236 / 1.03972 | 0.00559014 | 0.163681 | 3434 | 4072/24435 |
| 2000 | 1.04132 / 1.03972 | 0.00322073 | 0.12086 | 1324 | 7662/24435 |
| 5000 | 1.04019 / 1.03972 | 0.00114045 | 0.0434754 | 1048 | 13462/24435 |
| 10000 | 1.03996 / 1.03972 | 0.000628615 | 0.0264986 | 505 | 17038/24435 |
| 15000 | 1.03996 / 1.03972 | 0.000554381 | 0.0577738 | 403 | 18624/24435 |
| 20000 | 1.03993 / 1.03972 | 0.0005186 | 0.0352656 | 400 | 19527/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 16, 'recurrence_associated': 0, 'unresolved': 2}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 18, 'NO_SEQUENCE_DEVIATION': 0, 'PRECEDING': 0}.

### noise_sums_probability_original_seed2

| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |
|---|---|---|---|---|
| 0 | 319/930 | 204/23505 | 566/930 | 2344/23505 |
| 1 | 324/930 | 184/23505 | 569/930 | 2331/23505 |
| 2 | 314/930 | 187/23505 | 557/930 | 2328/23505 |
| 3 | 316/930 | 190/23505 | 565/930 | 2326/23505 |

| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |
|---|---|---|---|---|---|
| 0 | 1.09847 / 1.03972 | 0.0838734 | 0.219704 | 1944 | 0/24435 |
| 1000 | 1.04274 / 1.03972 | 0.00613379 | 0.142962 | 4303 | 3975/24435 |
| 2000 | 1.04108 / 1.03972 | 0.00290242 | 0.151058 | 1789 | 7891/24435 |
| 5000 | 1.04031 / 1.03972 | 0.00134984 | 0.188 | 813 | 13466/24435 |
| 10000 | 1.04004 / 1.03972 | 0.000746743 | 0.103788 | 558 | 16619/24435 |
| 15000 | 1.04 / 1.03972 | 0.000556688 | 0.0362601 | 583 | 17777/24435 |
| 20000 | 1.03991 / 1.03972 | 0.000379914 | 0.0237418 | 523 | 19513/24435 |

Concurrent diagnosis: ['Cause unresolved']. Counts: {'board_associated': 0, 'non_deviating': 16, 'recurrence_associated': 0, 'unresolved': 2}; chronology: {'COINCIDENT': 0, 'NO_OBSERVED_CONSTITUENT_ERROR': 17, 'NO_SEQUENCE_DEVIATION': 1, 'PRECEDING': 0}.

## Concurrent selected readings

Seed 0: Target noise contributes; probability targets do not uniformly repair B or the sums-loss disadvantage. Connection improves categorical responses and natural KL; live beats frozen on those two measures. Keep law and swap defects alongside access evidence; exact supplied sums pass B only in seed 2. Numerical versus one-hot differences support encoding sensitivity at this budget, including seeds 0–1 where both fail B; not a precision ceiling.

Seed 1: Target noise contributes; probability targets do not uniformly repair B or the sums-loss disadvantage. Connection improves categorical responses and natural KL; live beats frozen on those two measures. Keep law and swap defects alongside access evidence; exact supplied sums pass B only in seed 2. Numerical versus one-hot differences support encoding sensitivity at this budget, including seeds 0–1 where both fail B; not a precision ceiling.

Seed 2: Target noise contributes; probability targets do not uniformly repair B or the sums-loss disadvantage. Connection improves categorical responses and natural KL; live beats frozen on those two measures. Keep law and swap defects alongside access evidence; exact supplied sums pass B only in seed 2. Numerical versus one-hot differences support encoding sensitivity at this budget, including seeds 0–1 where both fail B; not a precision ceiling.

| Seed | Encoding | Categorical misreads | Natural KL | Long-panel TV | Endpoint label |
|---|---|---|---|---|---|
| 0 | numerical | 317 | 0.000836684 | 0.240672 | INCOMPLETE |
| 0 | onehot | 0 | 0.000113841 | 0.0133052 | INCOMPLETE |
| 1 | numerical | 121 | 0.000794769 | 0.0698225 | INCOMPLETE |
| 1 | onehot | 0 | 0.000306666 | 0.0156897 | INCOMPLETE |
| 2 | numerical | 10 | 0.000543183 | 0.189016 | INCOMPLETE |
| 2 | onehot | 2 | 0.000280613 | 0.0106611 | PASS |

| Seed | Access condition | Categorical misreads | Natural KL | Long-panel TV | Endpoint label |
|---|---|---|---|---|---|
| 0 | disconnected | 331 | 0.00210683 | 0.0985001 | INCOMPLETE |
| 0 | exact | 0 | 0.000113841 | 0.0133052 | INCOMPLETE |
| 0 | frozen | 259 | 0.000621785 | 0.242574 | INCOMPLETE |
| 0 | live | 117 | 0.00031731 | 0.246829 | INCOMPLETE |
| 1 | disconnected | 725 | 0.00182522 | 0.100162 | INCOMPLETE |
| 1 | exact | 0 | 0.000306666 | 0.0156897 | INCOMPLETE |
| 1 | frozen | 69 | 0.000548497 | 0.0113042 | INCOMPLETE |
| 1 | live | 43 | 0.000410938 | 0.251278 | INCOMPLETE |
| 2 | disconnected | 637 | 0.00204593 | 0.0727516 | INCOMPLETE |
| 2 | exact | 2 | 0.000280613 | 0.0106611 | PASS |
| 2 | frozen | 58 | 0.000340489 | 0.015699 | INCOMPLETE |
| 2 | live | 39 | 0.000290625 | 0.0119966 | INCOMPLETE |

## Supplementary cutoff geometry

Panel identities and fixed rendering hashes were bound before checkpoint states were read. Fitting excludes every existing probe-held-out identity. No resampling or network training. Distances are descriptive; a failed discrimination decision remains a failed decision.

### noise_raw_sampled_original_seed0, update 0

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 202/300 | 0.673333 | 0.594749 | 0.777948 | True | False | [0.263184, 1.094548, 1.910882] | 0.960617 |
| [23, 24] | 12 / 13 | 18/26 | 0.692308 | 0.675979 | 1.4115 | True | False | [0.380276, 1.113068, 1.591718] | 0.904754 |
### noise_raw_sampled_original_seed0, update 5000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 292/300 | 0.973333 | 0.0842998 | 0.813296 | True | False | [0.518225, 1.172727, 1.816248] | 0.89863 |
| [23, 24] | 12 / 13 | 22/26 | 0.846154 | 0.51536 | 1.63032 | True | False | [0.761261, 1.1908, 1.801419] | 0.76977 |
### noise_raw_sampled_original_seed0, update 20000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 295/300 | 0.983333 | 0.054223 | 0.875791 | True | False | [0.649075, 1.236019, 1.613986] | 0.896068 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.0156633 | 0.752684 | True | True | [1.401956, 1.837408, 2.502165] | 1.19418 |
### noise_raw_sampled_original_seed1, update 0

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 201/300 | 0.67 | 0.629311 | 0.761042 | True | False | [0.155533, 1.145866, 1.918386] | 1.00087 |
| [23, 24] | 12 / 13 | 17/26 | 0.653846 | 1.68673 | 2.89502 | True | False | [0.258827, 1.166765, 1.590977] | 0.973489 |
### noise_raw_sampled_original_seed1, update 5000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 293/300 | 0.976667 | 0.0719337 | 0.81785 | True | False | [0.525853, 1.141426, 1.804846] | 0.895423 |
| [23, 24] | 12 / 13 | 25/26 | 0.961538 | 0.15205 | 1.88361 | True | False | [1.075386, 1.568516, 2.098519] | 0.963174 |
### noise_raw_sampled_original_seed1, update 20000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 298/300 | 0.993333 | 0.0128017 | 0.808357 | True | True | [0.550631, 1.235282, 1.753858] | 0.914745 |
| [23, 24] | 12 / 13 | 25/26 | 0.961538 | 0.0425382 | 1.86046 | True | False | [1.403554, 2.057277, 2.543759] | 1.21467 |
### noise_raw_sampled_original_seed2, update 0

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 203/300 | 0.676667 | 0.609682 | 0.777342 | True | False | [0.184897, 1.015966, 2.285033] | 0.952491 |
| [23, 24] | 12 / 13 | 15/26 | 0.576923 | 2.64611 | 1.56588 | True | False | [0.306659, 0.939651, 1.772597] | 0.955253 |
### noise_raw_sampled_original_seed2, update 5000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 287/300 | 0.956667 | 0.112251 | 0.780003 | True | False | [0.355424, 1.090214, 1.865645] | 0.900353 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.0369323 | 3.21113 | True | True | [1.099805, 1.50048, 1.905778] | 0.963766 |
### noise_raw_sampled_original_seed2, update 20000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 293/300 | 0.976667 | 0.0607471 | 0.81881 | True | False | [0.580827, 1.153057, 1.787191] | 0.89782 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.0303147 | 1.88543 | True | True | [1.251214, 1.932063, 2.630694] | 1.26043 |
### noise_raw_probability_original_seed0, update 0

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 202/300 | 0.673333 | 0.594749 | 0.777948 | True | False | [0.263184, 1.094548, 1.910882] | 0.960617 |
| [23, 24] | 12 / 13 | 18/26 | 0.692308 | 0.675979 | 1.4115 | True | False | [0.380276, 1.113068, 1.591718] | 0.904754 |
### noise_raw_probability_original_seed0, update 5000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 299/300 | 0.996667 | 0.0172301 | 0.836024 | True | True | [0.591212, 1.213305, 1.789895] | 0.864013 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.00725013 | 1.38998 | True | True | [0.987717, 1.53925, 2.069577] | 0.82394 |
### noise_raw_probability_original_seed0, update 20000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 300/300 | 1 | 0.00182634 | 0.886804 | True | True | [0.44874, 1.221099, 1.785712] | 0.915837 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.00252161 | 1.25322 | True | True | [1.747465, 2.126493, 2.412659] | 1.07141 |
### noise_raw_probability_original_seed1, update 0

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 201/300 | 0.67 | 0.629311 | 0.761042 | True | False | [0.155533, 1.145866, 1.918386] | 1.00087 |
| [23, 24] | 12 / 13 | 17/26 | 0.653846 | 1.68673 | 2.89502 | True | False | [0.258827, 1.166765, 1.590977] | 0.973489 |
### noise_raw_probability_original_seed1, update 5000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 300/300 | 1 | 0.00154619 | 0.858427 | True | True | [0.526815, 1.181709, 1.759708] | 0.821821 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.00585022 | 1.10193 | True | True | [1.092415, 1.551311, 1.718913] | 0.858818 |
### noise_raw_probability_original_seed1, update 20000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 300/300 | 1 | 0.00160179 | 0.878585 | True | True | [0.609533, 1.259078, 1.807962] | 0.885443 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.00403182 | 0.976395 | True | True | [1.310964, 1.491442, 2.006984] | 0.869331 |
### noise_raw_probability_original_seed2, update 0

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 203/300 | 0.676667 | 0.609682 | 0.777342 | True | False | [0.184897, 1.015966, 2.285033] | 0.952491 |
| [23, 24] | 12 / 13 | 15/26 | 0.576923 | 2.64611 | 1.56588 | True | False | [0.306659, 0.939651, 1.772597] | 0.955253 |
### noise_raw_probability_original_seed2, update 5000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 300/300 | 1 | 0.0020065 | 0.807425 | True | True | [0.549991, 1.083851, 1.978804] | 0.842798 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.00768938 | 1.95353 | True | True | [1.202797, 1.496171, 1.85366] | 0.825365 |
### noise_raw_probability_original_seed2, update 20000

| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |
|---|---|---|---|---|---|---|---|---|---|
| [12, 13] | 135 / 150 | 300/300 | 1 | 0.00216501 | 0.824288 | True | True | [0.679669, 1.287913, 1.767453] | 0.910465 |
| [23, 24] | 12 / 13 | 26/26 | 1 | 0.0241562 | 1.39062 | True | True | [1.22028, 1.526808, 1.980844] | 0.907939 |

## Storage and bindings

Details: `bulk/study_r13_mechanism_bulk/report_revision/aggregate_details.json`, SHA-256 `6b80cf9e3ab8cd6e7e0bcf4f4d86ba26d82b2b3aeec05638d33ae222002a1d5a`.

Earlier reports and detailed numerical artifacts are hash-bound in JSON. The bulk artifact directory is configurable through SBML_DATA.
