# r11 jagged-competence aggregate

All saved runs are retained. No retraining, probe fitting, or checkpoint selection.

## Registered readings (verbatim)

## r11 registered design: jagged competence on the original B task

Run **three separately reported experiments** under one registration. Keep the original records game, its slot-1 L/N/H mode law, r8’s online sampler, AdamW \(3\times10^{-3}\), weight decay .01, batch 256, 20,000 updates, seeds 0–2, original and equal laws, and the saved r8 test panels. Audit at **0, 1k, 2k, 5k, 10k, 15k, and 20k**. Report first crossing and the fixed endpoint; select no best checkpoint.

The common outcomes are r8’s natural and unseen KL, witness recovery, maximum L/H and \(N^1\)–\(N^8\) law TV, causal swaps, rerendering, and per-slot A probes. Add r9’s **24,435-board category census**, using its deterministic rendering and three additional fixed renderings per board; score the exact saved r8 renderings separately. Report both categorical misreads and boards exceeding 0.02 TV. For every bar, walk the exact A/B oracle through the panel as the positive, and measure the untrained model and appropriate r8 baseline as floors. For A readability, retain the converged r8 probes, exact-A carrier, untrained carrier, majority floor, paired confidence intervals, and the distinction between probe accuracy and information loss. The equal-law control must have no predictive witness split.

### 1. Rarity: change board frequency, preserve the B law

**Training signal:** next-category B cross-entropy only. Keep the sampled L/N/H category sequence and next-category targets identical across paired arms. Change only the choice of **legal board within its already drawn category**. Thus \(P(Q_{t+1}\mid e_t)\) remains exactly the registered law, although the distribution of record boards changes.

| Arm | Within-category board draw |
|---|---|
| Uniform | Original r8 uniform draw |
| Cutoff | With probability .25 draw from a boundary sum, otherwise uniformly; boundary sums are L: **12**, N: **13 or 23** with equal probability, H: **24** |
| Matched decoy | Same .25 mixture and numbers of eligible boards; L: **10**, N: **16 or 20**, H: **27** |

Each paired sum has the same number of legal boards: L 285, N 285/25, H 25. A particular sum-23 N board receives roughly **ten times** its uniform within-N probability in the cutoff arm. Use shared category/target random draws and independent declared within-category draws. Log actual exposures for every slot-1 sum, board ID, and rendering, including the r9 failure boards; rarity is a measured exposure, not inferred from five appearances in the 60k-round test.

**Reading:** If cutoff enrichment reduces categorical misreads and rare-sequence failures more than both uniform and decoy, with ordinary KL retained, training exposure supports the rare-case part of the thesis. Similar improvement under decoy points to a general distribution or optimization effect. No improvement despite verified enrichment weakens the simple rarity explanation; r9’s context-dependent recurrence errors may remain.

### 2. Erosion: continue from an exact A network

Use the **existing exact per-slot continuous A core**, which was verified on all 1,555 legal local histories, inside the shared `ChoiceNetwork`. For each seed, initialize the raw and upper parts identically, load that A core, and verify five-sum accuracy on the full legal-board audit at update 0. Continue two paired **dual-route** arms:

- **B only:** next-category loss; every parameter remains trainable. The hard A-answer route retains its straight-through gradient, so B can change the A core.
- **A+B:** the same start and B loss, plus coefficient-1 five-sum cross-entropy.

Start fresh, identical optimizer states at continuation. Track exact A components and vectors **per slot**, all-history A accuracy, raw and upper probes, A-route accuracy, and B curves. Compare with r11’s uniform raw-only scratch run and show r8’s saved result as historical context. This erosion test uses an A-exposed dual architecture; its result must not be presented as a matched raw-only architectural effect.

**Reading:** A declining exact A computation in B-only, prevented by A+B, supports erosion without continued A supervision. If A remains exact while raw/upper probes decline, report a change in accessibility, not loss of the A computation. If both continuations erode A, the proposed protection failed. If neither erodes, erosion is not supported in this A-exposed architecture.

### 3. Dose: fraction of rounds with A supervision

Use the same raw-only B network and an auxiliary five-sum readout from its **shared raw encoder state**. The B head always sees only raw state. Arms receive A loss on nested, seed-fixed random fractions **0%, 1%, 10%, 100%** of active training rounds, independent of board and label. Compute
\[
L=L_B+\frac{\sum_{\text{selected rounds}} L_A}{\#\text{all active rounds}},
\]
so expected A gradient genuinely scales with dose; record selected counts by sum and slot. The **0% uniform arm is shared with experiment 1**, not rerun under a different definition. Compare both gaps: the r9 census and worst-case B law, and exact per-slot A accuracy/readability. The 100% arm is a measured positive for whether this architecture can learn A; the 0% arm is the floor.

**Reading:** A graded reduction in boundary errors and recovery of all-slot A with increasing dose supports the thesis that task reward and A supervision determine which pieces become reliable. A small dose closing the rare-case gap without restoring other slots separates the two gaps. All-slot A improving without rare-case B improving shows that A learning alone did not repair the upper law. No dose response, after verified exposure and a successful 100% positive, weakens the proposed A-supervision mechanism.

### Calibration, stopping, and first-hour read

Before fleet training, require the exact oracle to pass every B panel, its A readout to score 100%, the current-board-only null to retain a positive witness deficit, and the untrained probe and prediction floors to separate from their positives. Preserve r8’s numerical B bars; do not relax the 0.02 worst-case limit after seeing results.

At **5k**, stop an arm as futile only if *both* training B loss and natural-test excess KL have closed less than 10% of their measured update-0-to-oracle gaps **and**, where A loss is present, A accuracy has not improved. Keep erosion continuations running if A changes, even when B learning is slow. Record the stop as a result. The first-hour read checks oracle/null separation, shared category streams, actual cutoff and decoy exposures, exact erosion starts, nested dose masks, and the 1k learning curves.

### Build, outputs, and compute

Add `scripts/oldgame_multiround_jagged.py` and `tests/test_oldgame_multiround_jagged.py`; put the within-category sampler and auxiliary raw-state A head in `src/recombination_promotion/oldgame_ext/` beside the existing multiround code. Save `reports/phase11/oldgame_memory/multiround/study_r11_jagged/registration.md/json`, sampler frequencies and paired-stream checks, per-arm checkpoints and audits, r9-style board-level failures, A/probe curves with intervals, and **three separate aggregate sections** for rarity, erosion, and dose.

There are 48 runs: 18 rarity, 18 dose and 12 erosion. Device selection is configurable. Recorded timings are in the run summaries; launch settings are in `HOST_COMMANDS.md`.

There are 48 runs: 18 rarity, 18 dose and 12 erosion. Device selection is configurable. Recorded timings are in the run summaries; launch settings are in `HOST_COMMANDS.md`.


## Selected applicable readings and corrections

### dose

A computation and readability improve across all slots, while operational category errors increase and B remains incomplete. This supports “A improves without repairing the upper law,” rather than the predicted joint repair. Competition between objectives is a possible mechanism, not an established cause.

### erosion

B-only severely erodes the supplied sum computation. Continued A supervision largely protects it, but does not preserve exactness everywhere or guarantee B closure. This supports the scoped erosion result.

### rarity

Cutoff enrichment gives mixed improvement versus uniform: misreads **2/25/7 versus 21/5/9**, and consistently fewer than decoy **54/29/17**. It does not repair B. This weakens the simple rarity explanation under this training distribution; it does not establish that enrichment has no effect.

22/24 original-law maxima occur on N3–N8, but 16/24 already fail L/H or N1–N2. Long-neutral extrapolation does not explain every failure.
A+B largely protects A but is not exact everywhere; inspect integer board and local-history counts rather than rounded percentages. B closure is not guaranteed.
A census category misread is a two-anchor B predictive-signature error, not an auxiliary A-head category error. The dose decomposition keeps them separate.
Similar slot accuracies do not establish a constant answer. The B-only erosion output alphabets describe collapsed sum computations.
Prediction rerender failures and A-answer rerender failures are separate; the registered conjunctive gate is unchanged.
r8 versus r11 is historical evidence across different pathways, not a matched causal comparison. Objective competition is a possibility, not an established cause.
A separately registered, matched neutral-history coverage study is needed before attributing the worst-case gap cleanly to board rarity; none is run here.

Linear comparisons converged at both endpoints: 960/960 (unique runs, no duplicated 0% controls).

## rarity

### Seed 0 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| rarity_cutoff_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 0/24435, 3/24435, 1930/24435, 21/24435, 564/24435 | 0/24435 | not applicable |
| rarity_cutoff_original_seed0 | B_INCOMPLETE | 2/24435; 2/24435; 1/24435; 2/24435 | 46/24435; 31/24435; 35/24435; 35/24435 | 1 / 7 of 101 | 56/24435, 387/24435, 5225/24435, 447/24435, 833/24435 | 0/24435 | not applicable |
| rarity_decoy_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 9/24435, 18/24435, 1790/24435, 9/24435, 96/24435 | 0/24435 | not applicable |
| rarity_decoy_original_seed0 | B_INCOMPLETE | 54/24435; 48/24435; 40/24435; 52/24435 | 200/24435; 183/24435; 198/24435; 199/24435 | 1 / 2 of 101 | 88/24435, 794/24435, 5934/24435, 382/24435, 225/24435 | 0/24435 | not applicable |
| rarity_uniform_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 124/24435, 45/24435, 1685/24435, 127/24435, 789/24435 | 0/24435 | not applicable |
| rarity_uniform_original_seed0 | B_INCOMPLETE | 21/24435; 22/24435; 17/24435; 18/24435 | 105/24435; 114/24435; 95/24435; 115/24435 | 1 / 2 of 101 | 134/24435, 686/24435, 6380/24435, 252/24435, 657/24435 | 0/24435 | not applicable |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed0 | 39581042 | 0 / 0 | {'12': 3889344, '13': 2319563, '23': 1298234, '24': 6319127} | {'10': 142767, '16': 1119731, '20': 97368, '27': 2579953} | {'cutoff_sum_counts': {'12': 20.458279636633335, '13': 1.5529650818305676, '23': 9.888895659724867, '24': 1.8380032919929064}, 'decoy_sum_counts': {'10': 0.7528316810799408, '16': 0.7493132433450688, '20': 0.7444833544874834, '27': 0.7504479499599171}} |
| rarity_cutoff_original_seed0 | 39584565 | 0 / 0 | {'12': 4214833, '13': 2322868, '23': 1301041, '24': 5794810} | {'10': 154457, '16': 1120213, '20': 98770, '27': 2363004} | {'cutoff_sum_counts': {'12': 20.498764675557112, '13': 1.5555756459220238, '23': 9.905448205503022, '24': 1.840444871866536}, 'decoy_sum_counts': {'10': 0.74951474213397, '16': 0.7499248544116986, '20': 0.7535495487247564, '27': 0.7505910537194217}} |
| rarity_decoy_equal_seed0 | 39581042 | 0 / 0 | {'12': 142943, '13': 1120136, '23': 98498, '24': 2576785} | {'10': 3888687, '16': 2321564, '20': 1299190, '27': 6322964} | {'cutoff_sum_counts': {'12': 0.7518923155419729, '13': 0.7499395769381408, '23': 0.7502780274523544, '24': 0.7494926613688792}, 'decoy_sum_counts': {'10': 20.505626450116008, '16': 1.5535683574654546, '20': 9.933708500909882, '27': 1.8392022534791752}} |
| rarity_decoy_original_seed0 | 39584565 | 0 / 0 | {'12': 154165, '13': 1119213, '23': 98782, '24': 2361855} | {'10': 4214741, '16': 2324076, '20': 1301489, '27': 5787409} | {'cutoff_sum_counts': {'12': 0.749778711566333, '13': 0.7495133108723036, '23': 0.7520746730010812, '24': 0.7501305345373425}, 'decoy_sum_counts': {'10': 20.452362235291833, '16': 1.5558490715084747, '20': 9.92949730302961, '27': 1.8383284241648616}} |
| rarity_uniform_equal_seed0 | 39581042 | 0 / 0 | {'12': 190111, '13': 1493635, '23': 131282, '24': 3438039} | {'10': 189640, '16': 1494343, '20': 130786, '27': 3437884} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| rarity_uniform_original_seed0 | 39584565 | 0 / 0 | {'12': 205614, '13': 1493253, '23': 131346, '24': 3148592} | {'10': 206076, '16': 1493767, '20': 131073, '27': 3148191} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rarity_cutoff_equal_seed0 | 0.0027951533/0.00284326077 (n=32) | 0.00279016932/0.00284260511 (n=32) | 0.00280827074/0.00286540389 (n=64) | 0.00283577759/0.00290983915 (n=64) | 0.00284810457/0.00293053687 (n=64) | 0.00287013594/0.00296501815 (n=64) | 0.00288544968/0.00296767056 (n=64) | 0.00289327535/0.0030028522 (n=64) | 0.00290450826/0.00299264491 (n=64) | 0.00290999794/0.00301468372 (n=64) | 0.00281223655 / 0.00290983915 / True | 0.00288524529 / 0.00301468372 / True |
| rarity_cutoff_original_seed0 | 0.00330699096/0.00410604477 (n=32) | 0.0066383651/0.0116181374 (n=32) | 0.00534778007/0.036285609 (n=64) | 0.00585025328/0.0408259928 (n=64) | 0.00909134641/0.123872802 (n=64) | 0.0112056293/0.113123491 (n=64) | 0.0162322673/0.251858346 (n=64) | 0.0169820969/0.245955631 (n=64) | 0.0214143967/0.251530603 (n=64) | 0.0233967472/0.249872282 (n=64) | 0.00539023712 / 0.0408259928 / False | 0.0163870806 / 0.251858346 / False |
| rarity_decoy_equal_seed0 | 0.00284725614/0.00302684307 (n=32) | 0.00280029839/0.0028423816 (n=32) | 0.00285080611/0.00306938589 (n=64) | 0.00286065391/0.00311656296 (n=64) | 0.00286270468/0.00304880738 (n=64) | 0.00288691069/0.00310134888 (n=64) | 0.00289010745/0.00306513906 (n=64) | 0.00289497687/0.0030926913 (n=64) | 0.00296045048/0.00318463147 (n=64) | 0.00293831993/0.0032287091 (n=64) | 0.00284507909 / 0.00311656296 / True | 0.00290557835 / 0.0032287091 / True |
| rarity_decoy_original_seed0 | 0.00310584018/0.0034493953 (n=32) | 0.00637071719/0.009963274 (n=32) | 0.00428498187/0.00745344162 (n=64) | 0.00437689596/0.00958544016 (n=64) | 0.0050221968/0.0151097029 (n=64) | 0.00509696652/0.017076388 (n=64) | 0.0121052311/0.24965699 (n=64) | 0.00477854453/0.0117339343 (n=64) | 0.00537675503/0.012681067 (n=64) | 0.00619641785/0.0768731385 (n=64) | 0.00446671884 / 0.009963274 / True | 0.00642935196 / 0.24965699 / False |
| rarity_uniform_equal_seed0 | 0.00278943544/0.00279712677 (n=32) | 0.00278866664/0.00279562175 (n=32) | 0.00279151765/0.00280442834 (n=64) | 0.00279415282/0.00281070173 (n=64) | 0.00279749837/0.00281715393 (n=64) | 0.00280166883/0.00282619894 (n=64) | 0.0028044146/0.00282207131 (n=64) | 0.0028041515/0.00283180177 (n=64) | 0.00281133549/0.0028372854 (n=64) | 0.0028104973/0.00283369422 (n=64) | 0.00279157384 / 0.00281070173 / True | 0.00280492768 / 0.0028372854 / True |
| rarity_uniform_original_seed0 | 0.00285869162/0.00300101191 (n=32) | 0.00597489811/0.00766710937 (n=32) | 0.00460545917/0.00754839182 (n=64) | 0.00567261502/0.0559804291 (n=64) | 0.00965221541/0.233786002 (n=64) | 0.00808832247/0.0951221734 (n=64) | 0.015495737/0.250123315 (n=64) | 0.0103035322/0.060670957 (n=64) | 0.0286126832/0.249943078 (n=64) | 0.0170383909/0.249137938 (n=64) | 0.00489828968 / 0.0559804291 / False | 0.0148651469 / 0.250123315 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed0 | 3.74925819e-05 / 3.78919143e-05 (n=22305) | not recorded / 2.41766684e-05 | none | 3.68058681e-05 / True | 0 / True |
| rarity_cutoff_original_seed0 | 0.00014218672 / 0.000112132065 (n=25474) | 0.997284045 / 0.246335208 | law_TV, swaps | 0.0100155175 / True | 0 / True |
| rarity_decoy_equal_seed0 | 3.71707497e-05 / 3.75464872e-05 (n=22341) | not recorded / 0.000102169346 | none | 0.000189691782 / True | 0 / True |
| rarity_decoy_original_seed0 | 0.000135525674 / 0.000115997163 (n=25702) | 0.998700088 / 0.248652279 | law_TV, swaps | 0.0104890913 / True | 0 / True |
| rarity_uniform_equal_seed0 | 3.56903549e-05 / 3.57095082e-05 (n=20282) | not recorded / 3.77963297e-05 | none | 9.23424959e-05 / True | 0 / True |
| rarity_uniform_original_seed0 | 0.000215068465 / 0.000285757449 (n=24185) | 0.998397113 / 0.248876572 | law_TV, rerender, swaps | 0.0336352661 / False | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| rarity_cutoff_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_cutoff_equal_seed0 | A_swap_exact_row | 64 | 0.00278994837 / 0.00285865366 |
| rarity_cutoff_equal_seed0 | both_swap_exact_row | 64 | 0.00278994837 / 0.00285865366 |
| rarity_cutoff_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_cutoff_equal_seed0 | neutral_N | 192 | 0.00281366217 / 0.00293210149 |
| rarity_cutoff_equal_seed0 | neutral_raw_swap_stability | 128 | 1.86735997e-05 / 7.12871552e-05 |
| rarity_cutoff_equal_seed0 | raw_swap_effect | 64 | 1.80150382e-05 / 7.12126493e-05 |
| rarity_cutoff_equal_seed0 | raw_swap_exact_row | 64 | 0.00278994837 / 0.00285865366 |
| rarity_cutoff_equal_seed0 | raw_swap_stability | 128 | 0.0014039817 / 0.00285865366 |
| rarity_cutoff_equal_seed0 | reset_L | 160 | 0.00281753372 / 0.00294315815 |
| rarity_cutoff_equal_seed0 | same_category_substitution | 128 | 1.86735997e-05 / 7.12871552e-05 |
| rarity_cutoff_equal_seed0 | set_H | 160 | 0.00280715544 / 0.00287738442 |
| rarity_cutoff_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00280816155 / 0.00287210941 |
| rarity_cutoff_original_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_cutoff_original_seed0 | A_swap_exact_row | 64 | 0.25002725 / 0.251323968 |
| rarity_cutoff_original_seed0 | both_swap_exact_row | 64 | 0.0047519973 / 0.0105335414 |
| rarity_cutoff_original_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_cutoff_original_seed0 | neutral_N | 192 | 0.00722327095 / 0.130606294 |
| rarity_cutoff_original_seed0 | neutral_raw_swap_stability | 128 | 0.00539497688 / 0.124216124 |
| rarity_cutoff_original_seed0 | raw_swap_effect | 64 | 0.246794677 / 0.248661667 |
| rarity_cutoff_original_seed0 | raw_swap_exact_row | 64 | 0.0047519973 / 0.0105335414 |
| rarity_cutoff_original_seed0 | raw_swap_stability | 128 | 0.248410964 / 0.251323968 |
| rarity_cutoff_original_seed0 | reset_L | 160 | 0.00296888002 / 0.00375558436 |
| rarity_cutoff_original_seed0 | same_category_substitution | 128 | 0.00539497688 / 0.124216124 |
| rarity_cutoff_original_seed0 | set_H | 160 | 0.00608876785 / 0.0110661536 |
| rarity_cutoff_original_seed0 | upper_state_exchange_same_N | 64 | 0.00583705667 / 0.0299006104 |
| rarity_decoy_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_decoy_equal_seed0 | A_swap_exact_row | 64 | 0.00281651388 / 0.00295351446 |
| rarity_decoy_equal_seed0 | both_swap_exact_row | 64 | 0.00281651388 / 0.00295351446 |
| rarity_decoy_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_decoy_equal_seed0 | neutral_N | 192 | 0.00283651838 / 0.00311760604 |
| rarity_decoy_equal_seed0 | neutral_raw_swap_stability | 128 | 5.42392954e-05 / 0.000230446458 |
| rarity_decoy_equal_seed0 | raw_swap_effect | 64 | 5.60912304e-05 / 0.00022418797 |
| rarity_decoy_equal_seed0 | raw_swap_exact_row | 64 | 0.00281651388 / 0.00295351446 |
| rarity_decoy_equal_seed0 | raw_swap_stability | 128 | 0.00143630255 / 0.00295351446 |
| rarity_decoy_equal_seed0 | reset_L | 160 | 0.00284651229 / 0.00312240422 |
| rarity_decoy_equal_seed0 | same_category_substitution | 128 | 5.42392954e-05 / 0.000230446458 |
| rarity_decoy_equal_seed0 | set_H | 160 | 0.00282957666 / 0.00303202868 |
| rarity_decoy_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00283173658 / 0.0029809922 |
| rarity_decoy_original_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_decoy_original_seed0 | A_swap_exact_row | 64 | 0.249963118 / 0.251854107 |
| rarity_decoy_original_seed0 | both_swap_exact_row | 64 | 0.00487069576 / 0.0116839707 |
| rarity_decoy_original_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_decoy_original_seed0 | neutral_N | 192 | 0.00458729481 / 0.0241171867 |
| rarity_decoy_original_seed0 | neutral_raw_swap_stability | 128 | 0.000850136625 / 0.0150878727 |
| rarity_decoy_original_seed0 | raw_swap_effect | 64 | 0.246818617 / 0.248449042 |
| rarity_decoy_original_seed0 | raw_swap_exact_row | 64 | 0.00487069576 / 0.0116839707 |
| rarity_decoy_original_seed0 | raw_swap_stability | 128 | 0.248390867 / 0.251854107 |
| rarity_decoy_original_seed0 | reset_L | 160 | 0.00688734222 / 0.194939956 |
| rarity_decoy_original_seed0 | same_category_substitution | 128 | 0.000850136625 / 0.0150878727 |
| rarity_decoy_original_seed0 | set_H | 160 | 0.00619332376 / 0.0116839707 |
| rarity_decoy_original_seed0 | upper_state_exchange_same_N | 64 | 0.00436336501 / 0.0102694184 |
| rarity_uniform_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_equal_seed0 | A_swap_exact_row | 64 | 0.00278815464 / 0.00279918313 |
| rarity_uniform_equal_seed0 | both_swap_exact_row | 64 | 0.00278815464 / 0.00279918313 |
| rarity_uniform_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_equal_seed0 | neutral_N | 192 | 0.00279403625 / 0.00281150639 |
| rarity_uniform_equal_seed0 | neutral_raw_swap_stability | 128 | 2.92410841e-05 / 8.37743282e-05 |
| rarity_uniform_equal_seed0 | raw_swap_effect | 64 | 2.51145102e-05 / 7.14808702e-05 |
| rarity_uniform_equal_seed0 | raw_swap_exact_row | 64 | 0.00278815464 / 0.00279918313 |
| rarity_uniform_equal_seed0 | raw_swap_stability | 128 | 0.00140663458 / 0.00279918313 |
| rarity_uniform_equal_seed0 | reset_L | 160 | 0.002791523 / 0.00281581283 |
| rarity_uniform_equal_seed0 | same_category_substitution | 128 | 2.92410841e-05 / 8.37743282e-05 |
| rarity_uniform_equal_seed0 | set_H | 160 | 0.00279245777 / 0.00281183422 |
| rarity_uniform_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00279259984 / 0.00280271471 |
| rarity_uniform_original_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_original_seed0 | A_swap_exact_row | 64 | 0.250536802 / 0.251687922 |
| rarity_uniform_original_seed0 | both_swap_exact_row | 64 | 0.00436772651 / 0.0062135011 |
| rarity_uniform_original_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_original_seed0 | neutral_N | 192 | 0.00501435017 / 0.0383397788 |
| rarity_uniform_original_seed0 | neutral_raw_swap_stability | 128 | 0.00112070044 / 0.0373269543 |
| rarity_uniform_original_seed0 | raw_swap_effect | 64 | 0.248218665 / 0.249134906 |
| rarity_uniform_original_seed0 | raw_swap_exact_row | 64 | 0.00436772651 / 0.0062135011 |
| rarity_uniform_original_seed0 | raw_swap_stability | 128 | 0.249377734 / 0.251687922 |
| rarity_uniform_original_seed0 | reset_L | 160 | 0.00290810904 / 0.00535829365 |
| rarity_uniform_original_seed0 | same_category_substitution | 128 | 0.00112070044 / 0.0373269543 |
| rarity_uniform_original_seed0 | set_H | 160 | 0.00602366868 / 0.00727634132 |
| rarity_uniform_original_seed0 | upper_state_exchange_same_N | 64 | 0.00473039935 / 0.0124557763 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.794921875 | 0.029296875 [-0.0176269531, 0.07421875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([106], []) |
| rarity_cutoff_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.8046875 | 0.025390625 [-0.017578125, 0.0664550781] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([106], []) |
| rarity_cutoff_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.88671875 | 0.11328125 [0.072265625, 0.154296875] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([108], []) |
| rarity_cutoff_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.9375 | 0.13671875 [0.103515625, 0.171875] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([106], []) |
| rarity_cutoff_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.84765625 | 0.05078125 [0.013671875, 0.0859863281] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([95], []) |
| rarity_cutoff_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.498046875 | 0.134765625 [0.087890625, 0.18359375] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([331], []) |
| rarity_cutoff_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.48828125 | 0.1640625 [0.1171875, 0.218798828] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([193], []) |
| rarity_cutoff_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.587890625 | 0.3515625 [0.302734375, 0.400390625] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([623], []) |
| rarity_cutoff_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.6953125 | 0.396484375 [0.34375, 0.445361328] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([348], []) |
| rarity_cutoff_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.4765625 | 0.1796875 [0.12890625, 0.232421875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([524], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.923828125 | 0.015625 [-0.0078125, 0.04296875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.919921875 | 0.001953125 [-0.0234375, 0.0254394531] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.958984375 | 0.033203125 [0.013671875, 0.052734375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.98046875 | 0.05859375 [0.0390625, 0.078125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.939453125 | 0.00390625 [-0.017578125, 0.0234375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.646484375 | 0.0859375 [0.0390625, 0.13671875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.68359375 | 0.12109375 [0.072265625, 0.168017578] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.779296875 | 0.150390625 [0.10546875, 0.193359375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.875 | 0.25 [0.20703125, 0.291015625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.740234375 | 0.181640625 [0.128857422, 0.234375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.759765625 | -0.033203125 [-0.0742675781, 0.015625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([112], []) |
| rarity_cutoff_equal_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.78515625 | -0.01171875 [-0.0547363281, 0.03125] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([144], []) |
| rarity_cutoff_equal_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.845703125 | 0.04296875 [-4.8828125e-05, 0.083984375] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([158], []) |
| rarity_cutoff_equal_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.923828125 | 0.08984375 [0.0546875, 0.125] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([113], []) |
| rarity_cutoff_equal_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.833984375 | 0.029296875 [-0.00981445312, 0.068359375] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([113], []) |
| rarity_cutoff_equal_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.40234375 | 0.021484375 [-0.0293457031, 0.0703125] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([552], []) |
| rarity_cutoff_equal_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.34375 | 0.00390625 [-0.044921875, 0.05859375] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([338], []) |
| rarity_cutoff_equal_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.494140625 | 0.21875 [0.167919922, 0.271484375] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([950], []) |
| rarity_cutoff_equal_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.6484375 | 0.3515625 [0.302685547, 0.400390625] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([655], []) |
| rarity_cutoff_equal_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.421875 | 0.11328125 [0.05859375, 0.164111328] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([922], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.921875 | 0.01171875 [-0.013671875, 0.0352050781] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.916015625 | -0.001953125 [-0.0234375, 0.0234375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.939453125 | 0.013671875 [-0.0078125, 0.03515625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.962890625 | 0.029296875 [0.009765625, 0.05078125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.9375 | 0.015625 [-0.009765625, 0.041015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.55859375 | -0.001953125 [-0.046875, 0.046875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.63671875 | 0.078125 [0.029296875, 0.130859375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.681640625 | 0.080078125 [0.0292480469, 0.13671875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.83984375 | 0.2578125 [0.212890625, 0.302783203] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.6484375 | 0.099609375 [0.041015625, 0.15234375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 1 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([59], []) |
| rarity_cutoff_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.59765625 | -0.181640625 [-0.23046875, -0.130859375] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([80], []) |
| rarity_cutoff_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.6640625 | -0.109375 [-0.16015625, -0.05859375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([86], []) |
| rarity_cutoff_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.681640625 | -0.119140625 [-0.16796875, -0.06640625] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([106], []) |
| rarity_cutoff_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.64453125 | -0.15234375 [-0.201171875, -0.10546875] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([88], []) |
| rarity_cutoff_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.986328125 | 0.623046875 [0.578125, 0.6640625] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([571], []) |
| rarity_cutoff_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.072265625 | -0.251953125 [-0.29296875, -0.206982422] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([216], []) |
| rarity_cutoff_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.060546875 | -0.17578125 [-0.21484375, -0.1328125] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([260], []) |
| rarity_cutoff_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.0703125 | -0.228515625 [-0.275390625, -0.179638672] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([265], []) |
| rarity_cutoff_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.091796875 | -0.205078125 [-0.251953125, -0.162109375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([236], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 1 | 0.091796875 [0.068359375, 0.117236328] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.91015625 | -0.0078125 [-0.03125, 0.015625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.92578125 | 0 [-0.017578125, 0.01953125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.939453125 | 0.017578125 [0.001953125, 0.03515625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.935546875 | 0 [-0.017578125, 0.01953125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.984375 | 0.423828125 [0.380859375, 0.466796875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.380859375 | -0.181640625 [-0.228515625, -0.134716797] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.42578125 | -0.203125 [-0.251953125, -0.15625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.419921875 | -0.205078125 [-0.2578125, -0.15625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.44921875 | -0.109375 [-0.162109375, -0.0546875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / linear / category3 / 1 | 0.79296875 / 1 | 0.20703125 [0.173828125, 0.244140625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([59], []) |
| rarity_cutoff_original_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.6953125 | -0.1015625 [-0.15234375, -0.05078125] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([112], []) |
| rarity_cutoff_original_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.677734375 | -0.125 [-0.17578125, -0.076171875] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([154], []) |
| rarity_cutoff_original_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.734375 | -0.099609375 [-0.1484375, -0.052734375] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([170], []) |
| rarity_cutoff_original_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.740234375 | -0.064453125 [-0.111328125, -0.015625] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([161], []) |
| rarity_cutoff_original_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.984375 | 0.603515625 [0.562451172, 0.64453125] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([271], []) |
| rarity_cutoff_original_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.08984375 | -0.25 [-0.29296875, -0.199169922] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([348], []) |
| rarity_cutoff_original_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.0859375 | -0.189453125 [-0.232421875, -0.144482422] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([528], []) |
| rarity_cutoff_original_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.07421875 | -0.22265625 [-0.267578125, -0.177734375] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([416], []) |
| rarity_cutoff_original_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.099609375 | -0.208984375 [-0.25390625, -0.166015625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([392], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.998046875 | 0.087890625 [0.0625, 0.11328125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.90625 | -0.01171875 [-0.03515625, 0.01171875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.93359375 | 0.0078125 [-0.009765625, 0.025390625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.93359375 | 0 [-0.01953125, 0.01953125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.935546875 | 0.013671875 [-0.0078125, 0.0352050781] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.990234375 | 0.4296875 [0.38671875, 0.472705078] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.369140625 | -0.189453125 [-0.236328125, -0.14453125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.412109375 | -0.189453125 [-0.23828125, -0.142578125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.3984375 | -0.18359375 [-0.236376953, -0.132763672] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.41796875 | -0.130859375 [-0.185546875, -0.078125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.796875 | 0.03125 [-0.009765625, 0.072265625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([110], []) |
| rarity_decoy_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.740234375 | -0.0390625 [-0.083984375, 0.005859375] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([113], []) |
| rarity_decoy_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.705078125 | -0.068359375 [-0.111328125, -0.0234375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([83], []) |
| rarity_decoy_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.89453125 | 0.09375 [0.05859375, 0.128955078] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([125], []) |
| rarity_decoy_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.8671875 | 0.0703125 [0.0351074219, 0.109423828] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([108], []) |
| rarity_decoy_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.375 | 0.01171875 [-0.037109375, 0.0625] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([261], []) |
| rarity_decoy_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.33984375 | 0.015625 [-0.03515625, 0.0684082031] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([399], []) |
| rarity_decoy_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.310546875 | 0.07421875 [0.0234375, 0.127001953] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([267], []) |
| rarity_decoy_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.595703125 | 0.296875 [0.2421875, 0.349609375] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([817], []) |
| rarity_decoy_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.572265625 | 0.275390625 [0.224609375, 0.326171875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([284], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.931640625 | 0.0234375 [-0.00390625, 0.05078125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.92578125 | 0.0078125 [-0.015625, 0.029296875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.939453125 | 0.013671875 [-0.005859375, 0.033203125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.96875 | 0.046875 [0.0234375, 0.068359375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.958984375 | 0.0234375 [0.00190429688, 0.044921875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.51171875 | -0.048828125 [-0.099609375, 0.00200195312] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.748046875 | 0.185546875 [0.136669922, 0.23046875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.669921875 | 0.041015625 [-0.001953125, 0.0859375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.80078125 | 0.17578125 [0.132763672, 0.220751953] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.791015625 | 0.232421875 [0.1796875, 0.283251953] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.775390625 | -0.017578125 [-0.0625, 0.029296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([121], []) |
| rarity_decoy_equal_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.791015625 | -0.005859375 [-0.048828125, 0.037109375] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([111], []) |
| rarity_decoy_equal_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.736328125 | -0.06640625 [-0.115234375, -0.0234375] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([129], []) |
| rarity_decoy_equal_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.90234375 | 0.068359375 [0.03125, 0.10546875] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([154], []) |
| rarity_decoy_equal_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.86328125 | 0.05859375 [0.017578125, 0.095703125] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([103], []) |
| rarity_decoy_equal_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.3125 | -0.068359375 [-0.119140625, -0.0175292969] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([568], []) |
| rarity_decoy_equal_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.2265625 | -0.11328125 [-0.162109375, -0.064453125] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([626], []) |
| rarity_decoy_equal_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.248046875 | -0.02734375 [-0.083984375, 0.0215332031] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([293], []) |
| rarity_decoy_equal_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.48046875 | 0.18359375 [0.12890625, 0.23828125] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([1494], []) |
| rarity_decoy_equal_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.53125 | 0.22265625 [0.16796875, 0.273486328] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([495], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.91796875 | 0.0078125 [-0.017578125, 0.033203125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.919921875 | 0.001953125 [-0.021484375, 0.02734375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.9296875 | 0.00390625 [-0.013671875, 0.021484375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.966796875 | 0.033203125 [0.0078125, 0.056640625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.931640625 | 0.009765625 [-0.013671875, 0.03515625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.462890625 | -0.09765625 [-0.142626953, -0.048828125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.595703125 | 0.037109375 [-0.0156738281, 0.091796875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.619140625 | 0.017578125 [-0.03125, 0.068359375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.720703125 | 0.138671875 [0.08203125, 0.189453125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.67578125 | 0.126953125 [0.072265625, 0.18359375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 1 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([93], []) |
| rarity_decoy_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.6484375 | -0.130859375 [-0.185546875, -0.08203125] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([113], []) |
| rarity_decoy_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.611328125 | -0.162109375 [-0.216845703, -0.109375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([100], []) |
| rarity_decoy_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.583984375 | -0.216796875 [-0.263671875, -0.166015625] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([82], []) |
| rarity_decoy_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.623046875 | -0.173828125 [-0.220703125, -0.126953125] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([102], []) |
| rarity_decoy_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.978515625 | 0.615234375 [0.5703125, 0.65625] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([919], []) |
| rarity_decoy_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.103515625 | -0.220703125 [-0.263671875, -0.173828125] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([241], []) |
| rarity_decoy_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.087890625 | -0.1484375 [-0.19140625, -0.107373047] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([285], []) |
| rarity_decoy_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.072265625 | -0.2265625 [-0.271484375, -0.1796875] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([200], []) |
| rarity_decoy_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.0703125 | -0.2265625 [-0.269580078, -0.183544922] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([216], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.06640625, 0.115283203] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.91015625 | -0.0078125 [-0.03125, 0.013671875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.927734375 | 0.001953125 [-0.01171875, 0.017578125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.93359375 | 0.01171875 [-0.00390625, 0.029296875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.9375 | 0.001953125 [-0.01953125, 0.025390625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.98828125 | 0.427734375 [0.384716797, 0.470703125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.3984375 | -0.1640625 [-0.21484375, -0.115234375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.443359375 | -0.185546875 [-0.236328125, -0.13671875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.404296875 | -0.220703125 [-0.271533203, -0.166015625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.412109375 | -0.146484375 [-0.201171875, -0.0917480469] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / linear / category3 / 1 | 0.79296875 / 1 | 0.20703125 [0.173828125, 0.244140625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([108], []) |
| rarity_decoy_original_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.66796875 | -0.12890625 [-0.181640625, -0.080078125] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([161], []) |
| rarity_decoy_original_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.69140625 | -0.111328125 [-0.166064453, -0.0604980469] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([142], []) |
| rarity_decoy_original_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.654296875 | -0.1796875 [-0.224609375, -0.130859375] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([133], []) |
| rarity_decoy_original_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.62109375 | -0.18359375 [-0.234375, -0.1328125] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([115], []) |
| rarity_decoy_original_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.97265625 | 0.591796875 [0.55078125, 0.6328125] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([692], []) |
| rarity_decoy_original_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.09375 | -0.24609375 [-0.29296875, -0.201171875] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([577], []) |
| rarity_decoy_original_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.087890625 | -0.1875 [-0.232470703, -0.144482422] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([472], []) |
| rarity_decoy_original_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.060546875 | -0.236328125 [-0.283203125, -0.19140625] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([438], []) |
| rarity_decoy_original_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.064453125 | -0.244140625 [-0.287109375, -0.201171875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([406], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 1 | 0.08984375 [0.06640625, 0.115234375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.91015625 | -0.0078125 [-0.03125, 0.015625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.9296875 | 0.00390625 [-0.013671875, 0.021484375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.935546875 | 0.001953125 [-0.017578125, 0.021484375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.92578125 | 0.00390625 [-0.0156738281, 0.02734375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.98828125 | 0.427734375 [0.384765625, 0.470703125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.3671875 | -0.19140625 [-0.238330078, -0.142578125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.4296875 | -0.171875 [-0.220703125, -0.124951172] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.373046875 | -0.208984375 [-0.2578125, -0.16015625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.41015625 | -0.138671875 [-0.1953125, -0.0878417969] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.818359375 | 0.052734375 [0.013671875, 0.09765625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([90], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.83203125 | 0.052734375 [0.0116699219, 0.09375] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([104], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.7890625 | 0.015625 [-0.029296875, 0.0605957031] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([102], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.857421875 | 0.056640625 [0.021484375, 0.0957519531] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([99], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.83203125 | 0.03515625 [-0.001953125, 0.07421875] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([110], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.50390625 | 0.140625 [0.091796875, 0.189501953] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([249], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.58203125 | 0.2578125 [0.20703125, 0.3203125] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([257], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.26953125 | 0.033203125 [-0.017578125, 0.0820800781] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([271], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.541015625 | 0.2421875 [0.183544922, 0.300830078] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([306], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.564453125 | 0.267578125 [0.212890625, 0.322265625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([418], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.91796875 | 0.009765625 [-0.0137207031, 0.037109375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.935546875 | 0.017578125 [-0.01171875, 0.04296875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.94140625 | 0.015625 [-0.00390625, 0.037109375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.953125 | 0.03125 [0.009765625, 0.052734375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.955078125 | 0.01953125 [-0.001953125, 0.041015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.6640625 | 0.103515625 [0.05859375, 0.15234375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.720703125 | 0.158203125 [0.111328125, 0.201220703] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.576171875 | -0.052734375 [-0.0996582031, -0.00385742188] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.751953125 | 0.126953125 [0.076171875, 0.173828125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.740234375 | 0.181640625 [0.134716797, 0.23046875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.794921875 | 0.001953125 [-0.037109375, 0.04296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([142], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.8359375 | 0.0390625 [-0.00390625, 0.0781738281] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([121], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.783203125 | -0.01953125 [-0.06640625, 0.0234375] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([119], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.85546875 | 0.021484375 [-0.01953125, 0.064453125] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([132], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.830078125 | 0.025390625 [-0.015625, 0.064453125] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([165], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.439453125 | 0.05859375 [0.0078125, 0.109375] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([528], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.41015625 | 0.0703125 [0.017578125, 0.125] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([337], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.1875 | -0.087890625 [-0.13671875, -0.0390625] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([572], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.41796875 | 0.12109375 [0.068359375, 0.177734375] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([322], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.42578125 | 0.1171875 [0.05859375, 0.169921875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([682], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.912109375 | 0.001953125 [-0.02734375, 0.03125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.93359375 | 0.015625 [-0.0078125, 0.0390625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.939453125 | 0.013671875 [-0.005859375, 0.033203125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.93359375 | 0 [-0.021484375, 0.021484375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.939453125 | 0.017578125 [-0.001953125, 0.0390625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.5625 | 0.001953125 [-0.044921875, 0.0488769531] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.5859375 | 0.02734375 [-0.02734375, 0.080078125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.4765625 | -0.125 [-0.171875, -0.07421875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.580078125 | -0.001953125 [-0.05078125, 0.05078125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.6328125 | 0.083984375 [0.033203125, 0.136767578] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 1 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([44], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.59375 | -0.185546875 [-0.232470703, -0.13671875] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([81], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.58203125 | -0.19140625 [-0.24609375, -0.140625] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([85], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.533203125 | -0.267578125 [-0.318359375, -0.216796875] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([94], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.75390625 | -0.04296875 [-0.0859375, 0] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([86], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.96875 | 0.60546875 [0.560546875, 0.646484375] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([784], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.0859375 | -0.23828125 [-0.28125, -0.189453125] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([212], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.0625 | -0.173828125 [-0.21484375, -0.12890625] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([216], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.083984375 | -0.21484375 [-0.26171875, -0.171875] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([218], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.11328125 | -0.18359375 [-0.23046875, -0.138671875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([207], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 1 | 0.091796875 [0.068359375, 0.117236328] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.91796875 | 0 [-0.025390625, 0.0234375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.9296875 | 0.00390625 [-0.009765625, 0.01953125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.9375 | 0.015625 [0, 0.033203125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.951171875 | 0.015625 [-0.001953125, 0.033203125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.984375 | 0.423828125 [0.380859375, 0.466796875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.4140625 | -0.1484375 [-0.197314453, -0.099609375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.388671875 | -0.240234375 [-0.29296875, -0.191357422] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.396484375 | -0.228515625 [-0.279345703, -0.1796875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.439453125 | -0.119140625 [-0.169921875, -0.06640625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 1 | 0.79296875 / 1 | 0.20703125 [0.173828125, 0.244140625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([39], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.642578125 | -0.154296875 [-0.201171875, -0.10546875] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([134], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.544921875 | -0.2578125 [-0.312548828, -0.205078125] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([122], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.611328125 | -0.22265625 [-0.269580078, -0.17578125] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([168], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.7890625 | -0.015625 [-0.056640625, 0.0234375] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([133], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.982421875 | 0.6015625 [0.55859375, 0.642578125] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([428], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.052734375 | -0.287109375 [-0.328173828, -0.2421875] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([280], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.048828125 | -0.2265625 [-0.271484375, -0.18359375] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([266], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.064453125 | -0.232421875 [-0.275390625, -0.189453125] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([330], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.103515625 | -0.205078125 [-0.250048828, -0.158203125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([288], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.998046875 | 0.087890625 [0.0625, 0.11328125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.90625 | -0.01171875 [-0.0390625, 0.013671875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.9296875 | 0.00390625 [-0.013671875, 0.021484375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.9296875 | -0.00390625 [-0.0234375, 0.015625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.9375 | 0.015625 [-0.0078125, 0.041015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.984375 | 0.423828125 [0.382763672, 0.46875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.365234375 | -0.193359375 [-0.23828125, -0.146435547] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.41015625 | -0.19140625 [-0.238330078, -0.14453125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.38671875 | -0.1953125 [-0.24609375, -0.148388672] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.42578125 | -0.123046875 [-0.173828125, -0.0703125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed0 | 0 | 1.09376431 | 0 | 0.0236851002 | 0 |
| rarity_cutoff_equal_seed0 | 1000 | 1.08645713 | 0 | 4.96149292e-05 | 0 |
| rarity_cutoff_equal_seed0 | 2000 | 1.08370388 | 0 | 0.000310981958 | 0 |
| rarity_cutoff_equal_seed0 | 5000 | 1.081617 | 0 | 3.78441689e-06 | 0 |
| rarity_cutoff_equal_seed0 | 10000 | 1.07646418 | 0 | 3.631321e-05 | 0 |
| rarity_cutoff_equal_seed0 | 15000 | 1.08152664 | 0 | 5.8036281e-07 | 0 |
| rarity_cutoff_equal_seed0 | 20000 | 1.08533049 | 0 | 3.74925819e-05 | 0 |
| rarity_cutoff_original_seed0 | 0 | 1.10009861 | 0 | 0.0873579579 | 0 |
| rarity_cutoff_original_seed0 | 1000 | 1.03906131 | 0 | 0.00184112662 | 0 |
| rarity_cutoff_original_seed0 | 2000 | 1.04367423 | 0 | 0.00112853683 | 0 |
| rarity_cutoff_original_seed0 | 5000 | 1.03842735 | 0 | 0.000550739307 | 0 |
| rarity_cutoff_original_seed0 | 10000 | 1.03366482 | 0 | 0.000238395239 | 0 |
| rarity_cutoff_original_seed0 | 15000 | 1.03755569 | 0 | 0.000151670595 | 0 |
| rarity_cutoff_original_seed0 | 20000 | 1.03373873 | 0 | 0.00014218672 | 0 |
| rarity_decoy_equal_seed0 | 0 | 1.0947262 | 0 | 0.0236851002 | 0 |
| rarity_decoy_equal_seed0 | 1000 | 1.08656287 | 0 | 3.72614637e-05 | 0 |
| rarity_decoy_equal_seed0 | 2000 | 1.08389747 | 0 | 0.000334800503 | 0 |
| rarity_decoy_equal_seed0 | 5000 | 1.0815711 | 0 | 4.03804724e-06 | 0 |
| rarity_decoy_equal_seed0 | 10000 | 1.0764544 | 0 | 3.68722155e-05 | 0 |
| rarity_decoy_equal_seed0 | 15000 | 1.08152497 | 0 | 6.32176476e-07 | 0 |
| rarity_decoy_equal_seed0 | 20000 | 1.08532846 | 0 | 3.71707497e-05 | 0 |
| rarity_decoy_original_seed0 | 0 | 1.10058057 | 0 | 0.0873579579 | 0 |
| rarity_decoy_original_seed0 | 1000 | 1.03786647 | 0 | 0.00167104684 | 0 |
| rarity_decoy_original_seed0 | 2000 | 1.04305398 | 0 | 0.00154644098 | 0 |
| rarity_decoy_original_seed0 | 5000 | 1.03919125 | 0 | 0.000388767631 | 0 |
| rarity_decoy_original_seed0 | 10000 | 1.03399813 | 0 | 0.000187690868 | 0 |
| rarity_decoy_original_seed0 | 15000 | 1.03752303 | 0 | 0.000128084986 | 0 |
| rarity_decoy_original_seed0 | 20000 | 1.03408134 | 0 | 0.000135525674 | 0 |
| rarity_uniform_equal_seed0 | 0 | 1.09447777 | 0 | 0.0236851002 | 0 |
| rarity_uniform_equal_seed0 | 1000 | 1.0863483 | 0 | 4.06273224e-05 | 0 |
| rarity_uniform_equal_seed0 | 2000 | 1.08389795 | 0 | 0.000349846015 | 0 |
| rarity_uniform_equal_seed0 | 5000 | 1.08151126 | 0 | 9.17710046e-06 | 0 |
| rarity_uniform_equal_seed0 | 10000 | 1.07647598 | 0 | 3.87934484e-05 | 0 |
| rarity_uniform_equal_seed0 | 15000 | 1.08152711 | 0 | 3.12007738e-06 | 0 |
| rarity_uniform_equal_seed0 | 20000 | 1.08533144 | 0 | 3.56903549e-05 | 0 |
| rarity_uniform_original_seed0 | 0 | 1.10110247 | 0 | 0.0873579579 | 0 |
| rarity_uniform_original_seed0 | 1000 | 1.03980613 | 0 | 0.00164242641 | 0 |
| rarity_uniform_original_seed0 | 2000 | 1.04436517 | 0 | 0.00111866426 | 0 |
| rarity_uniform_original_seed0 | 5000 | 1.03869855 | 0 | 0.000314945679 | 0 |
| rarity_uniform_original_seed0 | 10000 | 1.03412378 | 0 | 0.000258404587 | 0 |
| rarity_uniform_original_seed0 | 15000 | 1.03774488 | 0 | 0.000207039825 | 0 |
| rarity_uniform_original_seed0 | 20000 | 1.03391683 | 0 | 0.000215068465 | 0 |

### Seed 1 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| rarity_cutoff_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 270/24435, 249/24435, 1933/24435, 2290/24435, 32/24435 | 0/24435 | not applicable |
| rarity_cutoff_original_seed1 | B_INCOMPLETE | 25/24435; 21/24435; 21/24435; 31/24435 | 95/24435; 74/24435; 99/24435; 87/24435 | 1 / 3 of 101 | 1/24435, 238/24435, 1478/24435, 279/24435, 340/24435 | 0/24435 | not applicable |
| rarity_decoy_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 309/24435, 281/24435, 1875/24435, 1890/24435, 22/24435 | 0/24435 | not applicable |
| rarity_decoy_original_seed1 | B_INCOMPLETE | 29/24435; 30/24435; 26/24435; 30/24435 | 77/24435; 86/24435; 89/24435; 88/24435 | 2 / 8 of 101 | 35/24435, 88/24435, 489/24435, 199/24435, 1020/24435 | 0/24435 | not applicable |
| rarity_uniform_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 172/24435, 129/24435, 1764/24435, 4245/24435, 20/24435 | 0/24435 | not applicable |
| rarity_uniform_original_seed1 | B_INCOMPLETE | 5/24435; 10/24435; 7/24435; 12/24435 | 49/24435; 54/24435; 64/24435; 47/24435 | 1 / 2 of 101 | 50/24435, 60/24435, 657/24435, 286/24435, 458/24435 | 0/24435 | not applicable |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed1 | 39580462 | 0 / 0 | {'12': 3890884, '13': 2323419, '23': 1299289, '24': 6325150} | {'10': 142166, '16': 1120431, '20': 97875, '27': 2578112} | {'cutoff_sum_counts': {'12': 20.516670621424243, '13': 1.556434525312788, '23': 9.922932991186668, '24': 1.840506774795694}, 'decoy_sum_counts': {'10': 0.7484351227421809, '16': 0.7497671262577189, '20': 0.7455552339310471, '27': 0.7497251175793015}} |
| rarity_cutoff_original_seed1 | 39586743 | 0 / 0 | {'12': 4211170, '13': 2320407, '23': 1302493, '24': 5800701} | {'10': 153980, '16': 1118625, '20': 97012, '27': 2361091} | {'cutoff_sum_counts': {'12': 20.40018795899781, '13': 1.5531027826452466, '23': 9.927084127250279, '24': 1.8416338652048823}, 'decoy_sum_counts': {'10': 0.7522190902829003, '16': 0.7494653495595498, '20': 0.741999632870342, '27': 0.7492282706789822}} |
| rarity_decoy_equal_seed1 | 39580462 | 0 / 0 | {'12': 142204, '13': 1121648, '23': 97956, '24': 2577403} | {'10': 3886239, '16': 2322722, '20': 1298558, '27': 6322184} | {'cutoff_sum_counts': {'12': 0.7498431279495901, '13': 0.7513804752599674, '23': 0.7481097924208404, '24': 0.749978685545599}, 'decoy_sum_counts': {'10': 20.459165784860307, '16': 1.5543131161451098, '20': 9.89166501622511, '27': 1.8385159926170698}} |
| rarity_decoy_original_seed1 | 39586743 | 0 / 0 | {'12': 154006, '13': 1121401, '23': 98024, '24': 2362438} | {'10': 4213137, '16': 2320620, '20': 1298143, '27': 5800480} | {'cutoff_sum_counts': {'12': 0.7460518921851687, '13': 0.7505799687559821, '23': 0.7470999801838331, '24': 0.7500379394226477}, 'decoy_sum_counts': {'10': 20.581907269627408, '16': 1.5547876003977048, '20': 9.92889157437435, '27': 1.8406252022933562}} |
| rarity_uniform_equal_seed1 | 39580462 | 0 / 0 | {'12': 189645, '13': 1492783, '23': 130938, '24': 3436635} | {'10': 189951, '16': 1494372, '20': 131278, '27': 3438743} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| rarity_uniform_original_seed1 | 39586743 | 0 / 0 | {'12': 206428, '13': 1494046, '23': 131206, '24': 3149758} | {'10': 204701, '16': 1492564, '20': 130744, '27': 3151364} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rarity_cutoff_equal_seed1 | 0.00447240751/0.00464442372 (n=32) | 0.00441298308/0.00451289117 (n=32) | 0.00468535861/0.00485379994 (n=64) | 0.0048926943/0.00519067049 (n=64) | 0.00513163977/0.00543938577 (n=64) | 0.00530739757/0.00569015741 (n=64) | 0.00549086439/0.0059556812 (n=64) | 0.00562067656/0.0060851723 (n=64) | 0.00576780853/0.00622931123 (n=64) | 0.00592514593/0.00647866726 (n=64) | 0.00467358273 / 0.00519067049 / True | 0.00554058879 / 0.00647866726 / True |
| rarity_cutoff_original_seed1 | 0.00400029542/0.00453825295 (n=32) | 0.00645454321/0.0130945444 (n=32) | 0.00502529112/0.0100331306 (n=64) | 0.00488573709/0.00582835823 (n=64) | 0.00660347333/0.119492024 (n=64) | 0.00495939387/0.0249450952 (n=64) | 0.0135266213/0.247698128 (n=64) | 0.00738583761/0.118356943 (n=64) | 0.0126042295/0.218153641 (n=64) | 0.0113608746/0.256366491 (n=64) | 0.00504614917 / 0.0130945444 / True | 0.00940673837 / 0.256366491 / False |
| rarity_decoy_equal_seed1 | 0.00461206166/0.00468538702 (n=32) | 0.0045932224/0.00463011861 (n=32) | 0.00482496689/0.00492015481 (n=64) | 0.00501360069/0.00510789454 (n=64) | 0.00521759363/0.00529542565 (n=64) | 0.00540041388/0.00553381443 (n=64) | 0.00556951459/0.0056887418 (n=64) | 0.00574147981/0.00584569573 (n=64) | 0.00589452335/0.00605404377 (n=64) | 0.00605839211/0.00619658828 (n=64) | 0.00481373654 / 0.00510789454 / True | 0.00564698623 / 0.00619658828 / True |
| rarity_decoy_original_seed1 | 0.00458018249/0.00501196086 (n=32) | 0.00647997414/0.0447176397 (n=32) | 0.00769742439/0.118159413 (n=64) | 0.0219270056/0.257099561 (n=64) | 0.0261004168/0.256859213 (n=64) | 0.0118979053/0.255124658 (n=64) | 0.0319400791/0.25643409 (n=64) | 0.0263633793/0.255280837 (n=64) | 0.028053169/0.256588161 (n=64) | 0.0479525304/0.256234542 (n=64) | 0.0117181694 / 0.257099561 / False | 0.0287179133 / 0.256859213 / False |
| rarity_uniform_equal_seed1 | 0.00482098013/0.00489571691 (n=32) | 0.00479944749/0.00486731529 (n=32) | 0.00491968263/0.00505003333 (n=64) | 0.00502422568/0.00519685447 (n=64) | 0.00512485066/0.00527951121 (n=64) | 0.00519888685/0.00537875295 (n=64) | 0.00528851757/0.00544086099 (n=64) | 0.00535332924/0.00563085079 (n=64) | 0.00542388042/0.0056540668 (n=64) | 0.00552316569/0.00574155152 (n=64) | 0.00491804071 / 0.00519685447 / True | 0.00531877174 / 0.00574155152 / True |
| rarity_uniform_original_seed1 | 0.00558635732/0.00613420457 (n=32) | 0.00484022009/0.00547485054 (n=32) | 0.00567690434/0.00781795382 (n=64) | 0.00556325691/0.0110847205 (n=64) | 0.00626961479/0.0533820391 (n=64) | 0.0051453074/0.0142772496 (n=64) | 0.00920776278/0.25216084 (n=64) | 0.00497917144/0.01282911 (n=64) | 0.00514214789/0.0139665753 (n=64) | 0.00489244959/0.0247732699 (n=64) | 0.00548448332 / 0.0110847205 / True | 0.00593940898 / 0.25216084 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed1 | 0.000120219445 / 0.000129249809 (n=22344) | not recorded / 0.000159331597 | none | 0.000309765339 / True | 0 / True |
| rarity_cutoff_original_seed1 | 0.000276470155 / 0.000268904036 (n=25563) | 0.998141056 / 0.257937193 | law_TV | 0.00726541132 / True | 0 / True |
| rarity_decoy_equal_seed1 | 0.000124968766 / 0.000133089108 (n=22305) | not recorded / 8.64821486e-05 | none | 9.43243504e-05 / True | 0 / True |
| rarity_decoy_original_seed1 | 0.00069372827 / 0.000351884271 (n=25524) | 0.982671462 / 0.249022394 | law_TV, rerender, swaps | 0.0626077801 / False | 0 / True |
| rarity_uniform_equal_seed1 | 0.000106416154 / 0.000109995794 (n=20222) | not recorded / 8.24881718e-05 | none | 0.000114187598 / True | 0 / True |
| rarity_uniform_original_seed1 | 0.000167032181 / 0.000178754335 (n=24118) | 0.997861334 / 0.255261242 | law_TV, swaps | 0.0134377033 / True | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| rarity_cutoff_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_cutoff_equal_seed1 | A_swap_exact_row | 64 | 0.00444594421 / 0.00471065938 |
| rarity_cutoff_equal_seed1 | both_swap_exact_row | 64 | 0.00444594421 / 0.00471065938 |
| rarity_cutoff_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_cutoff_equal_seed1 | neutral_N | 192 | 0.00476752703 / 0.00533360243 |
| rarity_cutoff_equal_seed1 | neutral_raw_swap_stability | 128 | 0.000124320737 / 0.000366836786 |
| rarity_cutoff_equal_seed1 | raw_swap_effect | 64 | 0.00021411432 / 0.000452741981 |
| rarity_cutoff_equal_seed1 | raw_swap_exact_row | 64 | 0.00444594421 / 0.00471065938 |
| rarity_cutoff_equal_seed1 | raw_swap_stability | 128 | 0.00233002927 / 0.00471065938 |
| rarity_cutoff_equal_seed1 | reset_L | 160 | 0.00479048984 / 0.00550058484 |
| rarity_cutoff_equal_seed1 | same_category_substitution | 128 | 0.000124320737 / 0.000366836786 |
| rarity_cutoff_equal_seed1 | set_H | 160 | 0.00469821692 / 0.0053204 |
| rarity_cutoff_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00469327159 / 0.00502415001 |
| rarity_cutoff_original_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_cutoff_original_seed1 | A_swap_exact_row | 64 | 0.254011662 / 0.254784979 |
| rarity_cutoff_original_seed1 | both_swap_exact_row | 64 | 0.00511729612 / 0.00687502325 |
| rarity_cutoff_original_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_cutoff_original_seed1 | neutral_N | 192 | 0.00500354578 / 0.0116252303 |
| rarity_cutoff_original_seed1 | neutral_raw_swap_stability | 128 | 0.00102007441 / 0.0122735202 |
| rarity_cutoff_original_seed1 | raw_swap_effect | 64 | 0.256296184 / 0.257643193 |
| rarity_cutoff_original_seed1 | raw_swap_exact_row | 64 | 0.00511729612 / 0.00687502325 |
| rarity_cutoff_original_seed1 | raw_swap_stability | 128 | 0.255153923 / 0.257643193 |
| rarity_cutoff_original_seed1 | reset_L | 160 | 0.00612848904 / 0.0132021904 |
| rarity_cutoff_original_seed1 | same_category_substitution | 128 | 0.00102007441 / 0.0122735202 |
| rarity_cutoff_original_seed1 | set_H | 160 | 0.00637725587 / 0.0089211762 |
| rarity_cutoff_original_seed1 | upper_state_exchange_same_N | 64 | 0.00499787868 / 0.00591751188 |
| rarity_decoy_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_decoy_equal_seed1 | A_swap_exact_row | 64 | 0.00459913234 / 0.00467254221 |
| rarity_decoy_equal_seed1 | both_swap_exact_row | 64 | 0.00459913234 / 0.00467254221 |
| rarity_decoy_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_decoy_equal_seed1 | neutral_N | 192 | 0.00489115335 / 0.0051548928 |
| rarity_decoy_equal_seed1 | neutral_raw_swap_stability | 128 | 4.11189394e-05 / 0.000138089061 |
| rarity_decoy_equal_seed1 | raw_swap_effect | 64 | 4.77680005e-05 / 0.000155419111 |
| rarity_decoy_equal_seed1 | raw_swap_exact_row | 64 | 0.00459913234 / 0.00467254221 |
| rarity_decoy_equal_seed1 | raw_swap_stability | 128 | 0.00232345017 / 0.00467254221 |
| rarity_decoy_equal_seed1 | reset_L | 160 | 0.00486771809 / 0.00518316031 |
| rarity_decoy_equal_seed1 | same_category_substitution | 128 | 4.11189394e-05 / 0.000138089061 |
| rarity_decoy_equal_seed1 | set_H | 160 | 0.00484872768 / 0.00511391461 |
| rarity_decoy_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00482128118 / 0.0049173981 |
| rarity_decoy_original_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_decoy_original_seed1 | A_swap_exact_row | 64 | 0.253860238 / 0.255105652 |
| rarity_decoy_original_seed1 | both_swap_exact_row | 64 | 0.00524982635 / 0.0104569122 |
| rarity_decoy_original_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_decoy_original_seed1 | neutral_N | 192 | 0.0113033199 / 0.25480555 |
| rarity_decoy_original_seed1 | neutral_raw_swap_stability | 128 | 0.0149109017 / 0.203408465 |
| rarity_decoy_original_seed1 | raw_swap_effect | 64 | 0.254729849 / 0.255858622 |
| rarity_decoy_original_seed1 | raw_swap_exact_row | 64 | 0.00524982635 / 0.0104569122 |
| rarity_decoy_original_seed1 | raw_swap_stability | 128 | 0.254295043 / 0.255858622 |
| rarity_decoy_original_seed1 | reset_L | 160 | 0.00599598708 / 0.00995514542 |
| rarity_decoy_original_seed1 | same_category_substitution | 128 | 0.0149109017 / 0.203408465 |
| rarity_decoy_original_seed1 | set_H | 160 | 0.00568253426 / 0.0104569122 |
| rarity_decoy_original_seed1 | upper_state_exchange_same_N | 64 | 0.00822376704 / 0.130425379 |
| rarity_uniform_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_equal_seed1 | A_swap_exact_row | 64 | 0.0048162553 / 0.00499030948 |
| rarity_uniform_equal_seed1 | both_swap_exact_row | 64 | 0.0048162553 / 0.00499030948 |
| rarity_uniform_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_equal_seed1 | neutral_N | 192 | 0.00495139052 / 0.0052318871 |
| rarity_uniform_equal_seed1 | neutral_raw_swap_stability | 128 | 6.29846472e-05 / 0.000159934163 |
| rarity_uniform_equal_seed1 | raw_swap_effect | 64 | 6.38510101e-05 / 0.000208899379 |
| rarity_uniform_equal_seed1 | raw_swap_exact_row | 64 | 0.0048162553 / 0.00499030948 |
| rarity_uniform_equal_seed1 | raw_swap_stability | 128 | 0.00244005315 / 0.00499030948 |
| rarity_uniform_equal_seed1 | reset_L | 160 | 0.00494260173 / 0.00537262857 |
| rarity_uniform_equal_seed1 | same_category_substitution | 128 | 6.29846472e-05 / 0.000159934163 |
| rarity_uniform_equal_seed1 | set_H | 160 | 0.00492679868 / 0.005215168 |
| rarity_uniform_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00491883536 / 0.00511404872 |
| rarity_uniform_original_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_original_seed1 | A_swap_exact_row | 64 | 0.254448437 / 0.25613457 |
| rarity_uniform_original_seed1 | both_swap_exact_row | 64 | 0.00519835844 / 0.00650531054 |
| rarity_uniform_original_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_original_seed1 | neutral_N | 192 | 0.00644388186 / 0.0613576323 |
| rarity_uniform_original_seed1 | neutral_raw_swap_stability | 128 | 0.00223508442 / 0.054870218 |
| rarity_uniform_original_seed1 | raw_swap_effect | 64 | 0.255657386 / 0.257126391 |
| rarity_uniform_original_seed1 | raw_swap_exact_row | 64 | 0.00519835844 / 0.00650531054 |
| rarity_uniform_original_seed1 | raw_swap_stability | 128 | 0.255052911 / 0.257126391 |
| rarity_uniform_original_seed1 | reset_L | 160 | 0.00629907753 / 0.0271157622 |
| rarity_uniform_original_seed1 | same_category_substitution | 128 | 0.00223508442 / 0.054870218 |
| rarity_uniform_original_seed1 | set_H | 160 | 0.00555046895 / 0.0315754414 |
| rarity_uniform_original_seed1 | upper_state_exchange_same_N | 64 | 0.00609618751 / 0.0166018456 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.78515625 | -0.017578125 [-0.05859375, 0.025390625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([112], []) |
| rarity_cutoff_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.890625 | 0.158203125 [0.11328125, 0.205078125] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([115], []) |
| rarity_cutoff_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.85546875 | 0.10546875 [0.06640625, 0.146533203] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([110], []) |
| rarity_cutoff_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.892578125 | 0.126953125 [0.0859375, 0.166015625] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([99], []) |
| rarity_cutoff_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.83203125 | 0.06640625 [0.025390625, 0.103515625] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([101], []) |
| rarity_cutoff_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.458984375 | 0.150390625 [0.101513672, 0.203173828] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([290], []) |
| rarity_cutoff_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.515625 | 0.251953125 [0.19921875, 0.302783203] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([446], []) |
| rarity_cutoff_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.57421875 | 0.2734375 [0.224609375, 0.326171875] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([283], []) |
| rarity_cutoff_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.744140625 | 0.484375 [0.437451172, 0.533251953] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([377], []) |
| rarity_cutoff_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.556640625 | 0.189453125 [0.125, 0.25] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([361], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.921875 | 0.013671875 [-0.00981445312, 0.0391113281] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.966796875 | 0.0546875 [0.033203125, 0.076171875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.95703125 | 0.048828125 [0.025390625, 0.072265625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.962890625 | 0.0234375 [0.00390625, 0.04296875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.94140625 | 0.015625 [-0.00390625, 0.03515625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.68359375 | 0.076171875 [0.02734375, 0.123046875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.791015625 | 0.189453125 [0.140625, 0.236328125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.80078125 | 0.2265625 [0.1796875, 0.271533203] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.83984375 | 0.271484375 [0.222607422, 0.3203125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.783203125 | 0.0859375 [0.03515625, 0.128955078] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.76953125 | -0.041015625 [-0.080078125, 0] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([125], []) |
| rarity_cutoff_equal_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.87890625 | 0.11328125 [0.072265625, 0.150390625] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([137], []) |
| rarity_cutoff_equal_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.841796875 | 0.08984375 [0.046875, 0.130908203] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([107], []) |
| rarity_cutoff_equal_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.865234375 | 0.119140625 [0.0780761719, 0.162109375] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([132], []) |
| rarity_cutoff_equal_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.79296875 | 0.001953125 [-0.0390625, 0.044921875] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([144], []) |
| rarity_cutoff_equal_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.255859375 | -0.08984375 [-0.138671875, -0.037109375] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([303], []) |
| rarity_cutoff_equal_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.384765625 | 0.083984375 [0.0331542969, 0.130859375] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([609], []) |
| rarity_cutoff_equal_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.44921875 | 0.125 [0.076171875, 0.173876953] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([493], []) |
| rarity_cutoff_equal_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.599609375 | 0.314453125 [0.255859375, 0.369140625] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([661], []) |
| rarity_cutoff_equal_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.466796875 | 0.064453125 [0.005859375, 0.12109375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([415], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.919921875 | -0.00390625 [-0.03125, 0.01953125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.939453125 | 0.037109375 [0.013671875, 0.0625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.927734375 | 0.0078125 [-0.0117675781, 0.025390625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.947265625 | 0.015625 [-0.00590820312, 0.0390625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.9375 | 0.013671875 [-0.0078125, 0.03515625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.458984375 | -0.142578125 [-0.189453125, -0.0956542969] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.615234375 | 0.068359375 [0.0194824219, 0.12109375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.611328125 | 0.048828125 [-0.001953125, 0.099609375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.63671875 | 0.056640625 [0.005859375, 0.105517578] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.6484375 | -0.0390625 [-0.08203125, 0.00390625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 1 | 0.197265625 [0.162109375, 0.232421875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([52], []) |
| rarity_cutoff_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.572265625 | -0.16015625 [-0.21484375, -0.10546875] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([88], []) |
| rarity_cutoff_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.49609375 | -0.25390625 [-0.310595703, -0.199169922] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([94], []) |
| rarity_cutoff_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.51171875 | -0.25390625 [-0.302734375, -0.205029297] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([86], []) |
| rarity_cutoff_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.646484375 | -0.119140625 [-0.171923828, -0.0663574219] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([79], []) |
| rarity_cutoff_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.974609375 | 0.666015625 [0.626953125, 0.708984375] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([381], []) |
| rarity_cutoff_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.099609375 | -0.1640625 [-0.2109375, -0.119140625] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([208], []) |
| rarity_cutoff_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.05859375 | -0.2421875 [-0.285205078, -0.201171875] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([182], []) |
| rarity_cutoff_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.0625 | -0.197265625 [-0.236328125, -0.154296875] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([204], []) |
| rarity_cutoff_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.078125 | -0.2890625 [-0.337890625, -0.2421875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([186], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.068359375, 0.1171875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.90625 | -0.005859375 [-0.02734375, 0.013671875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.9296875 | 0.021484375 [0.001953125, 0.041015625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.93359375 | -0.005859375 [-0.01953125, 0.0078125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.921875 | -0.00390625 [-0.025390625, 0.015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.98828125 | 0.380859375 [0.33984375, 0.421923828] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.38671875 | -0.21484375 [-0.26953125, -0.167919922] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.427734375 | -0.146484375 [-0.19921875, -0.09375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.400390625 | -0.16796875 [-0.21875, -0.119091797] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.40625 | -0.291015625 [-0.33984375, -0.23828125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / linear / category3 / 1 | 0.810546875 / 1 | 0.189453125 [0.154248047, 0.224609375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([60], []) |
| rarity_cutoff_original_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.572265625 | -0.193359375 [-0.242236328, -0.138671875] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([121], []) |
| rarity_cutoff_original_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.611328125 | -0.140625 [-0.19140625, -0.08984375] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([117], []) |
| rarity_cutoff_original_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.6171875 | -0.12890625 [-0.1796875, -0.078125] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([125], []) |
| rarity_cutoff_original_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.6328125 | -0.158203125 [-0.2109375, -0.103515625] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([114], []) |
| rarity_cutoff_original_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.974609375 | 0.62890625 [0.587890625, 0.669970703] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([311], []) |
| rarity_cutoff_original_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.08984375 | -0.2109375 [-0.255859375, -0.162060547] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([232], []) |
| rarity_cutoff_original_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.056640625 | -0.267578125 [-0.308642578, -0.22265625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([231], []) |
| rarity_cutoff_original_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.06640625 | -0.21875 [-0.26171875, -0.171875] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([211], []) |
| rarity_cutoff_original_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.052734375 | -0.349609375 [-0.392626953, -0.306640625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([216], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 1 | 0.076171875 [0.052734375, 0.09765625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.90625 | 0.00390625 [-0.0234375, 0.02734375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.9296875 | 0.009765625 [-0.009765625, 0.029296875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.927734375 | -0.00390625 [-0.01953125, 0.013671875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.92578125 | 0.001953125 [-0.01953125, 0.0234375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.984375 | 0.3828125 [0.343701172, 0.423828125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.357421875 | -0.189453125 [-0.236328125, -0.140625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.421875 | -0.140625 [-0.189453125, -0.091796875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.388671875 | -0.19140625 [-0.23828125, -0.140625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.4140625 | -0.2734375 [-0.318359375, -0.224609375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.69921875 | -0.103515625 [-0.150390625, -0.05859375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([77], []) |
| rarity_decoy_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.8671875 | 0.134765625 [0.09375, 0.1796875] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([95], []) |
| rarity_decoy_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.826171875 | 0.076171875 [0.0370605469, 0.12109375] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([101], []) |
| rarity_decoy_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.9140625 | 0.1484375 [0.111328125, 0.18359375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([95], []) |
| rarity_decoy_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.880859375 | 0.115234375 [0.0780761719, 0.15625] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([95], []) |
| rarity_decoy_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.390625 | 0.08203125 [0.029296875, 0.130908203] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([166], []) |
| rarity_decoy_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.501953125 | 0.23828125 [0.1875, 0.291015625] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([314], []) |
| rarity_decoy_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.546875 | 0.24609375 [0.193359375, 0.30078125] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([357], []) |
| rarity_decoy_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.74609375 | 0.486328125 [0.44140625, 0.533251953] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([398], []) |
| rarity_decoy_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.541015625 | 0.173828125 [0.119140625, 0.228515625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([336], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.90234375 | -0.005859375 [-0.033203125, 0.0234375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.943359375 | 0.03125 [0.0078125, 0.052734375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.947265625 | 0.0390625 [0.013671875, 0.0625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.962890625 | 0.0234375 [0.001953125, 0.04296875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.953125 | 0.02734375 [0.005859375, 0.046875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.654296875 | 0.046875 [-0.001953125, 0.0957519531] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.701171875 | 0.099609375 [0.048828125, 0.15234375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.78515625 | 0.2109375 [0.162109375, 0.257861328] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.822265625 | 0.25390625 [0.208984375, 0.298828125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.84765625 | 0.150390625 [0.10546875, 0.193408203] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.705078125 | -0.10546875 [-0.14453125, -0.0625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([113], []) |
| rarity_decoy_equal_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.859375 | 0.09375 [0.0546386719, 0.130859375] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([120], []) |
| rarity_decoy_equal_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.814453125 | 0.0625 [0.017578125, 0.1015625] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([114], []) |
| rarity_decoy_equal_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.912109375 | 0.166015625 [0.126953125, 0.20703125] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([143], []) |
| rarity_decoy_equal_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.8515625 | 0.060546875 [0.0234375, 0.095703125] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([120], []) |
| rarity_decoy_equal_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.376953125 | 0.03125 [-0.021484375, 0.083984375] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([387], []) |
| rarity_decoy_equal_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.423828125 | 0.123046875 [0.0703125, 0.17578125] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([491], []) |
| rarity_decoy_equal_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.453125 | 0.12890625 [0.078125, 0.181640625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([635], []) |
| rarity_decoy_equal_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.658203125 | 0.373046875 [0.3203125, 0.423828125] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([683], []) |
| rarity_decoy_equal_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.482421875 | 0.080078125 [0.02734375, 0.134765625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([347], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.916015625 | -0.0078125 [-0.033203125, 0.017578125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.916015625 | 0.013671875 [-0.013671875, 0.0390625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.931640625 | 0.01171875 [-0.009765625, 0.0332519531] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.955078125 | 0.0234375 [0.00390625, 0.046875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.953125 | 0.029296875 [0.0078125, 0.052734375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.548828125 | -0.052734375 [-0.1015625, -0.0078125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.62109375 | 0.07421875 [0.0234375, 0.126953125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.658203125 | 0.095703125 [0.046875, 0.142578125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.72265625 | 0.142578125 [0.0956542969, 0.187548828] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.69140625 | 0.00390625 [-0.04296875, 0.0488769531] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 1 | 0.197265625 [0.162109375, 0.232421875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([73], []) |
| rarity_decoy_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.703125 | -0.029296875 [-0.078125, 0.01953125] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([94], []) |
| rarity_decoy_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.60546875 | -0.14453125 [-0.19921875, -0.0917480469] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([84], []) |
| rarity_decoy_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.7109375 | -0.0546875 [-0.0996582031, -0.009765625] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([82], []) |
| rarity_decoy_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.603515625 | -0.162109375 [-0.216796875, -0.107421875] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([98], []) |
| rarity_decoy_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.966796875 | 0.658203125 [0.6171875, 0.701171875] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([588], []) |
| rarity_decoy_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.138671875 | -0.125 [-0.169970703, -0.08203125] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([232], []) |
| rarity_decoy_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.11328125 | -0.1875 [-0.232470703, -0.142578125] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([234], []) |
| rarity_decoy_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.07421875 | -0.185546875 [-0.228515625, -0.140625] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([226], []) |
| rarity_decoy_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.07421875 | -0.29296875 [-0.34375, -0.24609375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([215], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.068359375, 0.1171875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.8984375 | -0.013671875 [-0.033203125, 0.005859375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.92578125 | 0.017578125 [-0.001953125, 0.03515625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.935546875 | -0.00390625 [-0.01953125, 0.01171875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.9296875 | 0.00390625 [-0.017578125, 0.0234375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.98046875 | 0.373046875 [0.333984375, 0.416015625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.431640625 | -0.169921875 [-0.224658203, -0.119140625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.447265625 | -0.126953125 [-0.177734375, -0.076171875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.40234375 | -0.166015625 [-0.216796875, -0.115234375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.427734375 | -0.26953125 [-0.3203125, -0.21875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / linear / category3 / 1 | 0.810546875 / 1 | 0.189453125 [0.154248047, 0.224609375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([60], []) |
| rarity_decoy_original_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.744140625 | -0.021484375 [-0.0625488281, 0.021484375] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([152], []) |
| rarity_decoy_original_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.65234375 | -0.099609375 [-0.150390625, -0.044921875] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([135], []) |
| rarity_decoy_original_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.662109375 | -0.083984375 [-0.134765625, -0.033203125] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([125], []) |
| rarity_decoy_original_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.58984375 | -0.201171875 [-0.25390625, -0.146435547] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([143], []) |
| rarity_decoy_original_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.9609375 | 0.615234375 [0.57421875, 0.658203125] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([436], []) |
| rarity_decoy_original_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.130859375 | -0.169921875 [-0.216796875, -0.126953125] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([379], []) |
| rarity_decoy_original_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.126953125 | -0.197265625 [-0.2421875, -0.15234375] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([346], []) |
| rarity_decoy_original_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.076171875 | -0.208984375 [-0.253955078, -0.1640625] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([289], []) |
| rarity_decoy_original_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.0703125 | -0.33203125 [-0.377001953, -0.28515625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([422], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 1 | 0.076171875 [0.052734375, 0.09765625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.90625 | 0.00390625 [-0.021484375, 0.029296875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.927734375 | 0.0078125 [-0.0117675781, 0.02734375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.93359375 | 0.001953125 [-0.01171875, 0.017578125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.92578125 | 0.001953125 [-0.01953125, 0.0234375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.982421875 | 0.380859375 [0.341796875, 0.421923828] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.3828125 | -0.1640625 [-0.212890625, -0.115234375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.419921875 | -0.142578125 [-0.1875, -0.095703125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.38671875 | -0.193359375 [-0.240234375, -0.146484375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.35546875 | -0.33203125 [-0.384765625, -0.283154297] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.83203125 | 0.029296875 [-0.0078125, 0.064453125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([103], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.861328125 | 0.12890625 [0.0859375, 0.173828125] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([100], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.91796875 | 0.16796875 [0.130859375, 0.208984375] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([113], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.884765625 | 0.119140625 [0.076171875, 0.166015625] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([95], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.83203125 | 0.06640625 [0.0331542969, 0.1015625] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([93], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.546875 | 0.23828125 [0.185546875, 0.294921875] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([351], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.458984375 | 0.1953125 [0.14453125, 0.24609375] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([345], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.658203125 | 0.357421875 [0.310498047, 0.408203125] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([533], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.576171875 | 0.31640625 [0.26171875, 0.369189453] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([338], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.447265625 | 0.080078125 [0.01953125, 0.13671875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([406], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.923828125 | 0.015625 [-0.00786132812, 0.04296875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.953125 | 0.041015625 [0.021484375, 0.060546875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.9609375 | 0.052734375 [0.02734375, 0.076171875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.958984375 | 0.01953125 [0, 0.0390625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.9453125 | 0.01953125 [-0.00390625, 0.04296875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.75 | 0.142578125 [0.0976074219, 0.19140625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.751953125 | 0.150390625 [0.103515625, 0.201171875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.794921875 | 0.220703125 [0.17578125, 0.261767578] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.771484375 | 0.203125 [0.150390625, 0.25390625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.72265625 | 0.025390625 [-0.0254394531, 0.0703613281] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.828125 | 0.017578125 [-0.01953125, 0.05078125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([129], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.87890625 | 0.11328125 [0.07421875, 0.15234375] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([123], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.8984375 | 0.146484375 [0.109375, 0.185546875] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([138], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.861328125 | 0.115234375 [0.0703125, 0.1640625] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([118], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.8359375 | 0.044921875 [0.009765625, 0.0781738281] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([159], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.46484375 | 0.119140625 [0.0663574219, 0.171875] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([497], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.3671875 | 0.06640625 [0.01171875, 0.119189453] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([624], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.568359375 | 0.244140625 [0.19140625, 0.296875] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([780], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.4375 | 0.15234375 [0.0976074219, 0.208984375] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([448], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.353515625 | -0.048828125 [-0.103515625, 0.00390625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([583], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.923828125 | 0 [-0.02734375, 0.0234375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.91796875 | 0.015625 [-0.009765625, 0.041015625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.951171875 | 0.03125 [0.009765625, 0.052734375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.94921875 | 0.017578125 [0, 0.037109375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.93359375 | 0.009765625 [-0.01171875, 0.03125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.607421875 | 0.005859375 [-0.046875, 0.0566894531] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.55078125 | 0.00390625 [-0.0508300781, 0.056640625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.63671875 | 0.07421875 [0.0233886719, 0.12109375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.58203125 | 0.001953125 [-0.041015625, 0.05078125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.59375 | -0.09375 [-0.142578125, -0.046875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 1 | 0.197265625 [0.162109375, 0.232421875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([38], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.45703125 | -0.275390625 [-0.330078125, -0.21875] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([90], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.640625 | -0.109375 [-0.158203125, -0.05859375] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([91], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.671875 | -0.09375 [-0.14453125, -0.0448730469] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([84], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.7109375 | -0.0546875 [-0.0996582031, -0.0116699219] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([99], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.982421875 | 0.673828125 [0.634765625, 0.714892578] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([507], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.0546875 | -0.208984375 [-0.25390625, -0.166015625] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([193], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.064453125 | -0.236328125 [-0.28125, -0.195263672] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([215], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.087890625 | -0.171875 [-0.2109375, -0.126953125] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([209], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.09375 | -0.2734375 [-0.322265625, -0.226513672] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([203], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.068359375, 0.1171875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.90625 | -0.005859375 [-0.025390625, 0.01171875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.923828125 | 0.015625 [-0.00390625, 0.03515625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.939453125 | 0 [-0.013671875, 0.013671875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.93359375 | 0.0078125 [-0.01171875, 0.02734375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.994140625 | 0.38671875 [0.34765625, 0.427734375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.396484375 | -0.205078125 [-0.251953125, -0.158203125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.388671875 | -0.185546875 [-0.234375, -0.134716797] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.38671875 | -0.181640625 [-0.23046875, -0.130859375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.4609375 | -0.236328125 [-0.283203125, -0.187451172] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 1 | 0.810546875 / 1 | 0.189453125 [0.154248047, 0.224609375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([32], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.552734375 | -0.212890625 [-0.263671875, -0.1640625] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([113], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.6796875 | -0.072265625 [-0.121142578, -0.0234375] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([145], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.732421875 | -0.013671875 [-0.05859375, 0.037109375] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([154], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.6328125 | -0.158203125 [-0.20703125, -0.111328125] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([157], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.982421875 | 0.63671875 [0.597607422, 0.677734375] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([453], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.04296875 | -0.2578125 [-0.30078125, -0.21484375] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([237], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.0546875 | -0.26953125 [-0.3125, -0.2265625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([299], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.09375 | -0.19140625 [-0.23828125, -0.14453125] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([365], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.0625 | -0.33984375 [-0.38671875, -0.291015625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([224], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.998046875 | 0.07421875 [0.0526855469, 0.095703125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.896484375 | -0.005859375 [-0.03125, 0.01953125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.923828125 | 0.00390625 [-0.015625, 0.0234375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.9375 | 0.005859375 [-0.009765625, 0.0234375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.92578125 | 0.001953125 [-0.01953125, 0.0234375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.986328125 | 0.384765625 [0.345703125, 0.423876953] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.349609375 | -0.197265625 [-0.244140625, -0.154296875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.3984375 | -0.1640625 [-0.2109375, -0.119140625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.400390625 | -0.1796875 [-0.22265625, -0.136669922] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.41796875 | -0.26953125 [-0.31640625, -0.220703125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed1 | 0 | 1.09361207 | 0 | 0.0125658394 | 0 |
| rarity_cutoff_equal_seed1 | 1000 | 1.08327711 | 0 | 5.33130546e-05 | 0 |
| rarity_cutoff_equal_seed1 | 2000 | 1.08061135 | 0 | 3.11097417e-05 | 0 |
| rarity_cutoff_equal_seed1 | 5000 | 1.08285391 | 0 | 9.17701973e-05 | 0 |
| rarity_cutoff_equal_seed1 | 10000 | 1.09015334 | 0 | 1.54959346e-05 | 0 |
| rarity_cutoff_equal_seed1 | 15000 | 1.07939839 | 0 | 2.06853354e-05 | 0 |
| rarity_cutoff_equal_seed1 | 20000 | 1.08116865 | 0 | 0.000120219445 | 0 |
| rarity_cutoff_original_seed1 | 0 | 1.09105206 | 0 | 0.0671472389 | 0 |
| rarity_cutoff_original_seed1 | 1000 | 1.03776085 | 0 | 0.00230101926 | 0 |
| rarity_cutoff_original_seed1 | 2000 | 1.04924893 | 0 | 0.00146679207 | 0 |
| rarity_cutoff_original_seed1 | 5000 | 1.03895569 | 0 | 0.00060609329 | 0 |
| rarity_cutoff_original_seed1 | 10000 | 1.03461623 | 0 | 0.000476390187 | 0 |
| rarity_cutoff_original_seed1 | 15000 | 1.0417068 | 0 | 0.000138348872 | 0 |
| rarity_cutoff_original_seed1 | 20000 | 1.03552771 | 0 | 0.000276470155 | 0 |
| rarity_decoy_equal_seed1 | 0 | 1.09152126 | 0 | 0.0125658394 | 0 |
| rarity_decoy_equal_seed1 | 1000 | 1.08315611 | 0 | 3.11316845e-05 | 0 |
| rarity_decoy_equal_seed1 | 2000 | 1.08049941 | 0 | 4.43878619e-05 | 0 |
| rarity_decoy_equal_seed1 | 5000 | 1.08289993 | 0 | 6.4010006e-05 | 0 |
| rarity_decoy_equal_seed1 | 10000 | 1.09017229 | 0 | 1.84381113e-05 | 0 |
| rarity_decoy_equal_seed1 | 15000 | 1.07939911 | 0 | 2.00213097e-05 | 0 |
| rarity_decoy_equal_seed1 | 20000 | 1.08112729 | 0 | 0.000124968766 | 0 |
| rarity_decoy_original_seed1 | 0 | 1.0912627 | 0 | 0.0671472389 | 0 |
| rarity_decoy_original_seed1 | 1000 | 1.03688467 | 0 | 0.00186442455 | 0 |
| rarity_decoy_original_seed1 | 2000 | 1.05037487 | 0 | 0.00138669447 | 0 |
| rarity_decoy_original_seed1 | 5000 | 1.03969729 | 0 | 0.000456009704 | 0 |
| rarity_decoy_original_seed1 | 10000 | 1.03432298 | 0 | 0.000372262164 | 0 |
| rarity_decoy_original_seed1 | 15000 | 1.04092729 | 0 | 0.000213047395 | 0 |
| rarity_decoy_original_seed1 | 20000 | 1.03500283 | 0 | 0.00069372827 | 0 |
| rarity_uniform_equal_seed1 | 0 | 1.09032154 | 0 | 0.0125658394 | 0 |
| rarity_uniform_equal_seed1 | 1000 | 1.0831995 | 0 | 4.24726329e-05 | 0 |
| rarity_uniform_equal_seed1 | 2000 | 1.08072841 | 0 | 3.92188169e-05 | 0 |
| rarity_uniform_equal_seed1 | 5000 | 1.08291638 | 0 | 9.29171385e-05 | 0 |
| rarity_uniform_equal_seed1 | 10000 | 1.09012055 | 0 | 1.28598429e-05 | 0 |
| rarity_uniform_equal_seed1 | 15000 | 1.0794034 | 0 | 2.10849057e-05 | 0 |
| rarity_uniform_equal_seed1 | 20000 | 1.08105695 | 0 | 0.000106416154 | 0 |
| rarity_uniform_original_seed1 | 0 | 1.09025669 | 0 | 0.0671472389 | 0 |
| rarity_uniform_original_seed1 | 1000 | 1.03739917 | 0 | 0.001836219 | 0 |
| rarity_uniform_original_seed1 | 2000 | 1.05037534 | 0 | 0.00170006547 | 0 |
| rarity_uniform_original_seed1 | 5000 | 1.04044962 | 0 | 0.00063713864 | 0 |
| rarity_uniform_original_seed1 | 10000 | 1.03420663 | 0 | 0.000397725397 | 0 |
| rarity_uniform_original_seed1 | 15000 | 1.04124963 | 0 | 0.000184900387 | 0 |
| rarity_uniform_original_seed1 | 20000 | 1.03548837 | 0 | 0.000167032181 | 0 |

### Seed 2 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| rarity_cutoff_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 191/24435, 1081/24435, 173/24435, 200/24435, 2/24435 | 0/24435 | not applicable |
| rarity_cutoff_original_seed2 | B_INCOMPLETE | 7/24435; 4/24435; 6/24435; 3/24435 | 74/24435; 66/24435; 69/24435; 69/24435 | 0 / 2 of 101 | 54/24435, 249/24435, 2008/24435, 1554/24435, 39/24435 | 0/24435 | not applicable |
| rarity_decoy_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 141/24435, 878/24435, 127/24435, 313/24435, 134/24435 | 0/24435 | not applicable |
| rarity_decoy_original_seed2 | B_INCOMPLETE | 17/24435; 14/24435; 14/24435; 18/24435 | 106/24435; 106/24435; 119/24435; 117/24435 | 1 / 3 of 101 | 47/24435, 37/24435, 303/24435, 1574/24435, 54/24435 | 0/24435 | not applicable |
| rarity_uniform_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 48/24435, 684/24435, 290/24435, 172/24435, 21/24435 | 0/24435 | not applicable |
| rarity_uniform_original_seed2 | B_INCOMPLETE | 9/24435; 7/24435; 7/24435; 13/24435 | 41/24435; 34/24435; 41/24435; 40/24435 | 1 / 3 of 101 | 50/24435, 65/24435, 944/24435, 615/24435, 39/24435 | 0/24435 | not applicable |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed2 | 39580797 | 0 / 0 | {'12': 3886860, '13': 2318943, '23': 1301420, '24': 6324404} | {'10': 141446, '16': 1119529, '20': 98188, '27': 2575505} | {'cutoff_sum_counts': {'12': 20.406785356147196, '13': 1.5560566582274744, '23': 9.933290590462233, '24': 1.8407289100257145}, 'decoy_sum_counts': {'10': 0.7432477877966245, '16': 0.7497886983416001, '20': 0.7510460091023827, '27': 0.7494946631893052}} |
| rarity_cutoff_original_seed2 | 39584144 | 0 / 0 | {'12': 4214650, '13': 2322271, '23': 1298442, '24': 5796370} | {'10': 154648, '16': 1119476, '20': 98513, '27': 2362475} | {'cutoff_sum_counts': {'12': 20.40478910879585, '13': 1.5559896601075265, '23': 9.911544010442508, '24': 1.8401659472297203}, 'decoy_sum_counts': {'10': 0.754288501402268, '16': 0.7491972475529267, '20': 0.7514741443097648, '27': 0.7502426207101546}} |
| rarity_decoy_equal_seed2 | 39580797 | 0 / 0 | {'12': 142681, '13': 1117959, '23': 98953, '24': 2578336} | {'10': 3888966, '16': 2321634, '20': 1300638, '27': 6324012} | {'cutoff_sum_counts': {'12': 0.749103528658207, '13': 0.7501726198424579, '23': 0.7552741649874825, '24': 0.7504292285818649}, 'decoy_sum_counts': {'10': 20.435115707169434, '16': 1.5548815036373353, '20': 9.948659502046125, '27': 1.8403432507198105}} |
| rarity_decoy_original_seed2 | 39584144 | 0 / 0 | {'12': 153839, '13': 1118906, '23': 98431, '24': 2364129} | {'10': 4211346, '16': 2322256, '20': 1300227, '27': 5798610} | {'cutoff_sum_counts': {'12': 0.7447954994383981, '13': 0.7496998268644236, '23': 0.7513644725693305, '24': 0.7505369189092919}, 'decoy_sum_counts': {'10': 20.540646262650895, '16': 1.55414479927508, '20': 9.918355671164745, '27': 1.8414435551174548}} |
| rarity_uniform_equal_seed2 | 39580797 | 0 / 0 | {'12': 190469, '13': 1490269, '23': 131016, '24': 3435815} | {'10': 190308, '16': 1493126, '20': 130735, '27': 3436322} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| rarity_uniform_original_seed2 | 39584144 | 0 / 0 | {'12': 206552, '13': 1492472, '23': 131003, '24': 3149917} | {'10': 205025, '16': 1494234, '20': 131093, '27': 3148948} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rarity_cutoff_equal_seed2 | 0.00324054994/0.00325743854 (n=32) | 0.00324470596/0.00325199962 (n=32) | 0.00324322702/0.00325769186 (n=64) | 0.00324655068/0.00326897204 (n=64) | 0.00325046806/0.00327380002 (n=64) | 0.00324724359/0.00327807665 (n=64) | 0.00325233885/0.00328433514 (n=64) | 0.00325209368/0.00327937305 (n=64) | 0.0032523009/0.00328657031 (n=64) | 0.00325399567/0.00328317285 (n=64) | 0.00324413522 / 0.00326897204 / True | 0.00325140679 / 0.00328657031 / True |
| rarity_cutoff_original_seed2 | 0.00236386061/0.00481005758 (n=32) | 0.00556766544/0.00992257893 (n=32) | 0.00560362614/0.0203850791 (n=64) | 0.00673047651/0.0206844434 (n=64) | 0.00666410686/0.0215765983 (n=64) | 0.00711060781/0.0154377744 (n=64) | 0.0102101546/0.117352486 (n=64) | 0.00872033136/0.0220696852 (n=64) | 0.0125070793/0.208426684 (n=64) | 0.0106376598/0.0227249414 (n=64) | 0.00543328856 / 0.0206844434 / False | 0.00930832328 / 0.208426684 / False |
| rarity_decoy_equal_seed2 | 0.00287322141/0.00365425646 (n=32) | 0.00280321576/0.00329190493 (n=32) | 0.00304193143/0.00402359664 (n=64) | 0.00285443978/0.00394825637 (n=64) | 0.00309904816/0.00414448977 (n=64) | 0.00319284433/0.00444166362 (n=64) | 0.00293631363/0.00404722989 (n=64) | 0.00323691405/0.00458558649 (n=64) | 0.00319082325/0.00442704558 (n=64) | 0.00316325331/0.00455908477 (n=64) | 0.00291152993 / 0.00402359664 / True | 0.00313653279 / 0.00458558649 / True |
| rarity_decoy_original_seed2 | 0.00635288772/0.00849692523 (n=32) | 0.00545404432/0.00698241591 (n=32) | 0.00449172466/0.007229954 (n=64) | 0.00511455827/0.011653021 (n=64) | 0.00766957947/0.112215996 (n=64) | 0.00694688631/0.0473769307 (n=64) | 0.013429419/0.253878422 (n=64) | 0.00854871247/0.0980196148 (n=64) | 0.00907372579/0.129097909 (n=64) | 0.0103312901/0.171463758 (n=64) | 0.00516991632 / 0.011653021 / True | 0.00933326886 / 0.253878422 / False |
| rarity_uniform_equal_seed2 | 0.00325377379/0.00333186984 (n=32) | 0.00320759043/0.00334812701 (n=32) | 0.00323788309/0.0033608675 (n=64) | 0.00323368493/0.00333601236 (n=64) | 0.00323852082/0.00333894789 (n=64) | 0.00324331364/0.00337997079 (n=64) | 0.00324333156/0.0033659488 (n=64) | 0.00323970825/0.0033544153 (n=64) | 0.00323828473/0.00340111554 (n=64) | 0.00324460375/0.00336408615 (n=64) | 0.00323408338 / 0.0033608675 / True | 0.00324129379 / 0.00340111554 / True |
| rarity_uniform_original_seed2 | 0.00429638568/0.00554978102 (n=32) | 0.00665977993/0.0148282051 (n=32) | 0.00546126894/0.0227398053 (n=64) | 0.00520684046/0.0143512636 (n=64) | 0.00532702729/0.0179997236 (n=64) | 0.00593012967/0.0430342108 (n=64) | 0.00985496596/0.249877714 (n=64) | 0.00706158788/0.0204183608 (n=64) | 0.0096109506/0.0298115611 (n=64) | 0.0106212745/0.0241098702 (n=64) | 0.00538206407 / 0.0227398053 / False | 0.00806765598 / 0.249877714 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed2 | 3.95486304e-05 / 3.95753278e-05 (n=22364) | not recorded / 1.01299956e-05 | none | 1.16974115e-05 / True | 0 / True |
| rarity_cutoff_original_seed2 | 0.000159978744 / 0.000191464701 (n=25454) | 0.99758103 / 0.249769166 | law_TV, swaps | 0.0104634464 / True | 0 / True |
| rarity_decoy_equal_seed2 | 4.09071455e-05 / 4.21117747e-05 (n=22251) | not recorded / 0.00104949251 | none | 0.00264771283 / True | 0 / True |
| rarity_decoy_original_seed2 | 0.000220278626 / 0.000209118158 (n=25535) | 0.998571671 / 0.252581477 | law_TV | 0.00677154958 / True | 0 / True |
| rarity_uniform_equal_seed2 | 3.89530277e-05 / 3.919014e-05 (n=20211) | not recorded / 7.4217096e-05 | none | 0.000219479203 / True | 0 / True |
| rarity_uniform_original_seed2 | 0.000174531007 / 0.000189056231 (n=24131) | 0.997650538 / 0.252513766 | law_TV, swaps | 0.00793328136 / True | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| rarity_cutoff_equal_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_cutoff_equal_seed2 | A_swap_exact_row | 64 | 0.00324447313 / 0.00325609744 |
| rarity_cutoff_equal_seed2 | both_swap_exact_row | 64 | 0.00324447313 / 0.00325609744 |
| rarity_cutoff_equal_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_cutoff_equal_seed2 | neutral_N | 192 | 0.0032468494 / 0.00327883661 |
| rarity_cutoff_equal_seed2 | neutral_raw_swap_stability | 128 | 6.71797898e-06 / 2.13831663e-05 |
| rarity_cutoff_equal_seed2 | raw_swap_effect | 64 | 8.30739737e-06 / 3.0502677e-05 |
| rarity_cutoff_equal_seed2 | raw_swap_exact_row | 64 | 0.00324447313 / 0.00325609744 |
| rarity_cutoff_equal_seed2 | raw_swap_stability | 128 | 0.00162639027 / 0.00325609744 |
| rarity_cutoff_equal_seed2 | reset_L | 160 | 0.00324692037 / 0.00328063965 |
| rarity_cutoff_equal_seed2 | same_category_substitution | 128 | 6.71797898e-06 / 2.13831663e-05 |
| rarity_cutoff_equal_seed2 | set_H | 160 | 0.00324704805 / 0.00327017903 |
| rarity_cutoff_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00324626872 / 0.00326761603 |
| rarity_cutoff_original_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_cutoff_original_seed2 | A_swap_exact_row | 64 | 0.251400129 / 0.254958384 |
| rarity_cutoff_original_seed2 | both_swap_exact_row | 64 | 0.00411301269 / 0.00890785456 |
| rarity_cutoff_original_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_cutoff_original_seed2 | neutral_N | 192 | 0.00668148398 / 0.110706598 |
| rarity_cutoff_original_seed2 | neutral_raw_swap_stability | 128 | 0.00290373329 / 0.0985116586 |
| rarity_cutoff_original_seed2 | raw_swap_effect | 64 | 0.25058996 / 0.255020842 |
| rarity_cutoff_original_seed2 | raw_swap_exact_row | 64 | 0.00411301269 / 0.00890785456 |
| rarity_cutoff_original_seed2 | raw_swap_stability | 128 | 0.250995044 / 0.255020842 |
| rarity_cutoff_original_seed2 | reset_L | 160 | 0.00369651625 / 0.0104769617 |
| rarity_cutoff_original_seed2 | same_category_substitution | 128 | 0.00290373329 / 0.0985116586 |
| rarity_cutoff_original_seed2 | set_H | 160 | 0.00609650896 / 0.0150798559 |
| rarity_cutoff_original_seed2 | upper_state_exchange_same_N | 64 | 0.00613391655 / 0.0421254039 |
| rarity_decoy_equal_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_decoy_equal_seed2 | A_swap_exact_row | 64 | 0.00288021495 / 0.00408025086 |
| rarity_decoy_equal_seed2 | both_swap_exact_row | 64 | 0.00288021495 / 0.00408025086 |
| rarity_decoy_equal_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_decoy_equal_seed2 | neutral_N | 192 | 0.00293554051 / 0.00537216663 |
| rarity_decoy_equal_seed2 | neutral_raw_swap_stability | 128 | 0.00131997204 / 0.00437260419 |
| rarity_decoy_equal_seed2 | raw_swap_effect | 64 | 0.000841479283 / 0.00256037712 |
| rarity_decoy_equal_seed2 | raw_swap_exact_row | 64 | 0.00288021495 / 0.00408025086 |
| rarity_decoy_equal_seed2 | raw_swap_stability | 128 | 0.00186084711 / 0.00408025086 |
| rarity_decoy_equal_seed2 | reset_L | 160 | 0.00304168034 / 0.00526714325 |
| rarity_decoy_equal_seed2 | same_category_substitution | 128 | 0.00131997204 / 0.00437260419 |
| rarity_decoy_equal_seed2 | set_H | 160 | 0.00298753763 / 0.00392776728 |
| rarity_decoy_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00288211217 / 0.00470021367 |
| rarity_decoy_original_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_decoy_original_seed2 | A_swap_exact_row | 64 | 0.25340015 / 0.260572188 |
| rarity_decoy_original_seed2 | both_swap_exact_row | 64 | 0.0055191993 / 0.0105721876 |
| rarity_decoy_original_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_decoy_original_seed2 | neutral_N | 192 | 0.00463815445 / 0.0125678927 |
| rarity_decoy_original_seed2 | neutral_raw_swap_stability | 128 | 0.00200841093 / 0.00844258815 |
| rarity_decoy_original_seed2 | raw_swap_effect | 64 | 0.254901221 / 0.260465316 |
| rarity_decoy_original_seed2 | raw_swap_exact_row | 64 | 0.0055191993 / 0.0105721876 |
| rarity_decoy_original_seed2 | raw_swap_stability | 128 | 0.254150685 / 0.260572188 |
| rarity_decoy_original_seed2 | reset_L | 160 | 0.00642030239 / 0.0133218169 |
| rarity_decoy_original_seed2 | same_category_substitution | 128 | 0.00200841093 / 0.00844258815 |
| rarity_decoy_original_seed2 | set_H | 160 | 0.00588034107 / 0.00918518752 |
| rarity_decoy_original_seed2 | upper_state_exchange_same_N | 64 | 0.00450949068 / 0.00755182654 |
| rarity_uniform_equal_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_equal_seed2 | A_swap_exact_row | 64 | 0.00321744406 / 0.00333410501 |
| rarity_uniform_equal_seed2 | both_swap_exact_row | 64 | 0.00321744406 / 0.00333410501 |
| rarity_uniform_equal_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_equal_seed2 | neutral_N | 192 | 0.00322136446 / 0.00339455903 |
| rarity_uniform_equal_seed2 | neutral_raw_swap_stability | 128 | 9.16725257e-05 / 0.000249415636 |
| rarity_uniform_equal_seed2 | raw_swap_effect | 64 | 0.000109301414 / 0.000231802464 |
| rarity_uniform_equal_seed2 | raw_swap_exact_row | 64 | 0.00321744406 / 0.00333410501 |
| rarity_uniform_equal_seed2 | raw_swap_stability | 128 | 0.00166337274 / 0.00333410501 |
| rarity_uniform_equal_seed2 | reset_L | 160 | 0.00324777476 / 0.00339499116 |
| rarity_uniform_equal_seed2 | same_category_substitution | 128 | 9.16725257e-05 / 0.000249415636 |
| rarity_uniform_equal_seed2 | set_H | 160 | 0.00318467971 / 0.00326183438 |
| rarity_uniform_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00322115142 / 0.00333410501 |
| rarity_uniform_original_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_original_seed2 | A_swap_exact_row | 64 | 0.253982547 / 0.257066146 |
| rarity_uniform_original_seed2 | both_swap_exact_row | 64 | 0.0054668379 / 0.0080999732 |
| rarity_uniform_original_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_original_seed2 | neutral_N | 192 | 0.00526839599 / 0.013760522 |
| rarity_uniform_original_seed2 | neutral_raw_swap_stability | 128 | 0.00249371753 / 0.0228154361 |
| rarity_uniform_original_seed2 | raw_swap_effect | 64 | 0.254539587 / 0.258692071 |
| rarity_uniform_original_seed2 | raw_swap_exact_row | 64 | 0.0054668379 / 0.0080999732 |
| rarity_uniform_original_seed2 | raw_swap_stability | 128 | 0.254261067 / 0.258692071 |
| rarity_uniform_original_seed2 | reset_L | 160 | 0.00445461641 / 0.0101616457 |
| rarity_uniform_original_seed2 | same_category_substitution | 128 | 0.00249371753 / 0.0228154361 |
| rarity_uniform_original_seed2 | set_H | 160 | 0.006547292 / 0.0115155876 |
| rarity_uniform_original_seed2 | upper_state_exchange_same_N | 64 | 0.00524523901 / 0.00873918086 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.693359375 | -0.05078125 [-0.0977050781, -0.00390625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([86], []) |
| rarity_cutoff_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.845703125 | 0.087890625 [0.04296875, 0.128955078] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([96], []) |
| rarity_cutoff_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.85546875 | 0.107421875 [0.0702636719, 0.14453125] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([100], []) |
| rarity_cutoff_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.94921875 | 0.1328125 [0.099609375, 0.16796875] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([124], []) |
| rarity_cutoff_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.96484375 | 0.244140625 [0.203125, 0.283203125] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([96], []) |
| rarity_cutoff_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.431640625 | 0.177734375 [0.126953125, 0.230517578] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([186], []) |
| rarity_cutoff_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.51171875 | 0.189453125 [0.140576172, 0.240234375] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([343], []) |
| rarity_cutoff_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.416015625 | 0.123046875 [0.07421875, 0.175830078] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([215], []) |
| rarity_cutoff_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.744140625 | 0.384765625 [0.333935547, 0.433642578] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([779], []) |
| rarity_cutoff_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.833984375 | 0.564453125 [0.515625, 0.61328125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([518], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.91796875 | -0.005859375 [-0.0273925781, 0.017578125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.947265625 | 0.0234375 [0, 0.046875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.943359375 | 0.013671875 [-0.0078125, 0.033203125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.974609375 | 0.041015625 [0.01953125, 0.0625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9765625 | 0.064453125 [0.041015625, 0.0898925781] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.666015625 | 0.109375 [0.060546875, 0.158251953] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.748046875 | 0.14453125 [0.0976074219, 0.193359375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.66015625 | 0.09375 [0.048828125, 0.14453125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.87890625 | 0.2578125 [0.212890625, 0.3046875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.912109375 | 0.267578125 [0.21875, 0.310546875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.689453125 | -0.083984375 [-0.130859375, -0.0370605469] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([99], []) |
| rarity_cutoff_equal_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.853515625 | 0.052734375 [0.013671875, 0.087890625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([148], []) |
| rarity_cutoff_equal_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.841796875 | 0.0703125 [0.033203125, 0.109375] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([126], []) |
| rarity_cutoff_equal_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.947265625 | 0.103515625 [0.068359375, 0.138671875] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([158], []) |
| rarity_cutoff_equal_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.916015625 | 0.173828125 [0.134765625, 0.212890625] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([143], []) |
| rarity_cutoff_equal_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.34765625 | 0.080078125 [0.02734375, 0.130859375] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([265], []) |
| rarity_cutoff_equal_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.513671875 | 0.16015625 [0.109326172, 0.21484375] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([526], []) |
| rarity_cutoff_equal_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.3359375 | 0.02734375 [-0.029296875, 0.076171875] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([263], []) |
| rarity_cutoff_equal_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.72265625 | 0.341796875 [0.291015625, 0.394580078] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([1191], []) |
| rarity_cutoff_equal_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.669921875 | 0.3828125 [0.326171875, 0.435546875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([532], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.91796875 | 0.009765625 [-0.01171875, 0.03125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.923828125 | 0.0078125 [-0.017578125, 0.033203125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.89453125 | -0.021484375 [-0.048828125, 0.0078125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.962890625 | 0.021484375 [0.001953125, 0.041015625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.94140625 | 0.0390625 [0.013671875, 0.064453125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.5390625 | 0.025390625 [-0.02734375, 0.0781738281] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.654296875 | 0.0546875 [0.0078125, 0.099609375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.564453125 | -0.01171875 [-0.05859375, 0.0390625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.80078125 | 0.16015625 [0.115234375, 0.203125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.76953125 | 0.134765625 [0.091796875, 0.18359375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 1 | 0.255859375 [0.21875, 0.29296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([64], []) |
| rarity_cutoff_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.515625 | -0.2421875 [-0.293017578, -0.189453125] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([98], []) |
| rarity_cutoff_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.677734375 | -0.0703125 [-0.123095703, -0.01953125] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([98], []) |
| rarity_cutoff_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.51171875 | -0.3046875 [-0.35546875, -0.25] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([90], []) |
| rarity_cutoff_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.544921875 | -0.17578125 [-0.228515625, -0.125] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([88], []) |
| rarity_cutoff_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.984375 | 0.73046875 [0.695263672, 0.767626953] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([494], []) |
| rarity_cutoff_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.060546875 | -0.26171875 [-0.3046875, -0.220654297] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([201], []) |
| rarity_cutoff_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.10546875 | -0.1875 [-0.236328125, -0.142529297] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([225], []) |
| rarity_cutoff_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.046875 | -0.3125 [-0.357421875, -0.265625] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([189], []) |
| rarity_cutoff_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.052734375 | -0.216796875 [-0.2578125, -0.171875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([213], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.998046875 | 0.07421875 [0.05078125, 0.0977050781] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.90625 | -0.017578125 [-0.0390625, 0.00390625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.935546875 | 0.005859375 [-0.0117675781, 0.0234863281] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.931640625 | -0.001953125 [-0.017578125, 0.013671875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.927734375 | 0.015625 [-0.005859375, 0.037109375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.994140625 | 0.4375 [0.3984375, 0.480517578] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.376953125 | -0.2265625 [-0.277392578, -0.179638672] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.40234375 | -0.1640625 [-0.212890625, -0.1171875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.44140625 | -0.1796875 [-0.228515625, -0.130859375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.419921875 | -0.224609375 [-0.279296875, -0.171875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / linear / category3 / 1 | 0.7734375 / 1 | 0.2265625 [0.189453125, 0.263671875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([74], []) |
| rarity_cutoff_original_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.591796875 | -0.208984375 [-0.26171875, -0.156201172] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([113], []) |
| rarity_cutoff_original_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.6953125 | -0.076171875 [-0.125, -0.021484375] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([114], []) |
| rarity_cutoff_original_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.580078125 | -0.263671875 [-0.3125, -0.212841797] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([122], []) |
| rarity_cutoff_original_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.53515625 | -0.20703125 [-0.259765625, -0.150390625] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([122], []) |
| rarity_cutoff_original_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.98828125 | 0.720703125 [0.683544922, 0.76171875] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([301], []) |
| rarity_cutoff_original_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.044921875 | -0.30859375 [-0.3515625, -0.263671875] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([304], []) |
| rarity_cutoff_original_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.05859375 | -0.25 [-0.29296875, -0.20703125] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([340], []) |
| rarity_cutoff_original_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.037109375 | -0.34375 [-0.390625, -0.296875] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([246], []) |
| rarity_cutoff_original_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.037109375 | -0.25 [-0.29296875, -0.20703125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([219], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.064453125, 0.115234375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.90625 | -0.009765625 [-0.033203125, 0.01171875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.9375 | 0.021484375 [0.00385742188, 0.0391113281] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.93359375 | -0.0078125 [-0.025390625, 0.009765625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.927734375 | 0.025390625 [0, 0.048828125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.990234375 | 0.4765625 [0.43359375, 0.521484375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.365234375 | -0.234375 [-0.28125, -0.1875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.404296875 | -0.171875 [-0.220703125, -0.124951172] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.390625 | -0.25 [-0.298828125, -0.19921875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_cutoff_original_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.42578125 | -0.208984375 [-0.255859375, -0.16015625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.66796875 | -0.076171875 [-0.125, -0.02734375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([97], []) |
| rarity_decoy_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.875 | 0.1171875 [0.076171875, 0.158203125] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([113], []) |
| rarity_decoy_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.841796875 | 0.09375 [0.05078125, 0.1328125] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([129], []) |
| rarity_decoy_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.767578125 | -0.048828125 [-0.095703125, 4.8828125e-05] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([92], []) |
| rarity_decoy_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.919921875 | 0.19921875 [0.158154297, 0.240234375] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([126], []) |
| rarity_decoy_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.296875 | 0.04296875 [-0.00390625, 0.08984375] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([226], []) |
| rarity_decoy_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.689453125 | 0.3671875 [0.318359375, 0.41796875] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([725], []) |
| rarity_decoy_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.375 | 0.08203125 [0.029296875, 0.130859375] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([238], []) |
| rarity_decoy_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.447265625 | 0.087890625 [0.03125, 0.14453125] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([194], []) |
| rarity_decoy_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.62109375 | 0.3515625 [0.296875, 0.40625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([959], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.916015625 | -0.0078125 [-0.029296875, 0.013671875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.962890625 | 0.0390625 [0.015625, 0.0625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.93359375 | 0.00390625 [-0.01953125, 0.02734375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.92578125 | -0.0078125 [-0.025390625, 0.009765625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9609375 | 0.048828125 [0.025390625, 0.072265625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.625 | 0.068359375 [0.01953125, 0.119140625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.8359375 | 0.232421875 [0.1875, 0.275390625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.62109375 | 0.0546875 [0.009765625, 0.10546875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.75 | 0.12890625 [0.0839355469, 0.173876953] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.77734375 | 0.1328125 [0.08203125, 0.1796875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.6328125 | -0.140625 [-0.1953125, -0.08984375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([130], []) |
| rarity_decoy_equal_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.861328125 | 0.060546875 [0.021484375, 0.1015625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([132], []) |
| rarity_decoy_equal_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.84375 | 0.072265625 [0.033203125, 0.113330078] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([115], []) |
| rarity_decoy_equal_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.75 | -0.09375 [-0.140625, -0.05078125] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([108], []) |
| rarity_decoy_equal_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.8984375 | 0.15625 [0.1171875, 0.197265625] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([175], []) |
| rarity_decoy_equal_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.240234375 | -0.02734375 [-0.078125, 0.0234375] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([307], []) |
| rarity_decoy_equal_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.662109375 | 0.30859375 [0.255859375, 0.357421875] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([1293], []) |
| rarity_decoy_equal_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.271484375 | -0.037109375 [-0.08984375, 0.009765625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([288], []) |
| rarity_decoy_equal_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.283203125 | -0.09765625 [-0.150439453, -0.04296875] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([234], []) |
| rarity_decoy_equal_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.513671875 | 0.2265625 [0.16796875, 0.281298828] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([1923], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.921875 | 0.013671875 [-0.0078125, 0.037109375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.935546875 | 0.01953125 [-0.005859375, 0.046875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.9296875 | 0.013671875 [-0.0078125, 0.03515625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.93359375 | -0.0078125 [-0.025390625, 0.009765625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.94921875 | 0.046875 [0.01953125, 0.07421875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.595703125 | 0.08203125 [0.0351074219, 0.130859375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.78125 | 0.181640625 [0.1328125, 0.226611328] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.494140625 | -0.08203125 [-0.12890625, -0.03515625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.55078125 | -0.08984375 [-0.140625, -0.04296875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.626953125 | -0.0078125 [-0.060546875, 0.04296875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 1 | 0.255859375 [0.21875, 0.29296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([74], []) |
| rarity_decoy_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.55078125 | -0.20703125 [-0.261767578, -0.150390625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([95], []) |
| rarity_decoy_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.689453125 | -0.05859375 [-0.115234375, -0.00390625] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([92], []) |
| rarity_decoy_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.59375 | -0.22265625 [-0.279296875, -0.169873047] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([95], []) |
| rarity_decoy_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.474609375 | -0.24609375 [-0.298828125, -0.193359375] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([75], []) |
| rarity_decoy_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.974609375 | 0.720703125 [0.68359375, 0.759765625] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([451], []) |
| rarity_decoy_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.08203125 | -0.240234375 [-0.28515625, -0.1953125] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([216], []) |
| rarity_decoy_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.072265625 | -0.220703125 [-0.265625, -0.17578125] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([240], []) |
| rarity_decoy_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.068359375 | -0.291015625 [-0.337890625, -0.244140625] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([200], []) |
| rarity_decoy_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.1015625 | -0.16796875 [-0.212890625, -0.125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([201], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.99609375 | 0.072265625 [0.048828125, 0.095703125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.916015625 | -0.0078125 [-0.03125, 0.013671875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.92578125 | -0.00390625 [-0.0234375, 0.017578125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.9296875 | -0.00390625 [-0.021484375, 0.013671875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9296875 | 0.017578125 [-0.001953125, 0.041015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.990234375 | 0.43359375 [0.39453125, 0.478515625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.4453125 | -0.158203125 [-0.216796875, -0.103515625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.419921875 | -0.146484375 [-0.193359375, -0.09765625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.4140625 | -0.20703125 [-0.265625, -0.154248047] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.443359375 | -0.201171875 [-0.25390625, -0.1484375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.998046875 | 0.224609375 [0.1875, 0.26171875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([68], []) |
| rarity_decoy_original_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.640625 | -0.16015625 [-0.210986328, -0.103515625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([122], []) |
| rarity_decoy_original_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.7265625 | -0.044921875 [-0.0937988281, 0.01171875] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([135], []) |
| rarity_decoy_original_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.68359375 | -0.16015625 [-0.2109375, -0.109326172] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([141], []) |
| rarity_decoy_original_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.541015625 | -0.201171875 [-0.253955078, -0.1484375] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([109], []) |
| rarity_decoy_original_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.978515625 | 0.7109375 [0.671875, 0.751953125] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([422], []) |
| rarity_decoy_original_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.095703125 | -0.2578125 [-0.306689453, -0.208984375] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([346], []) |
| rarity_decoy_original_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.08203125 | -0.2265625 [-0.2734375, -0.181640625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([268], []) |
| rarity_decoy_original_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.0859375 | -0.294921875 [-0.341796875, -0.25] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([299], []) |
| rarity_decoy_original_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.1171875 | -0.169921875 [-0.220703125, -0.12109375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([279], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.064453125, 0.115234375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.912109375 | -0.00390625 [-0.02734375, 0.01953125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.9296875 | 0.013671875 [-0.0078125, 0.033203125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.9296875 | -0.01171875 [-0.03125, 0.0078125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.9296875 | 0.02734375 [0.00390625, 0.0508300781] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.994140625 | 0.48046875 [0.439404297, 0.5234375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.443359375 | -0.15625 [-0.208984375, -0.107421875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.3828125 | -0.193359375 [-0.2421875, -0.14453125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.388671875 | -0.251953125 [-0.302734375, -0.201171875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_decoy_original_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.46484375 | -0.169921875 [-0.220703125, -0.1171875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.67578125 | -0.068359375 [-0.115234375, -0.015625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([96], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.884765625 | 0.126953125 [0.0859375, 0.166015625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([79], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.87109375 | 0.123046875 [0.080078125, 0.1640625] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([113], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.890625 | 0.07421875 [0.037109375, 0.115234375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([79], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.798828125 | 0.078125 [0.0351074219, 0.123046875] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([73], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.365234375 | 0.111328125 [0.056640625, 0.1640625] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([321], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.5078125 | 0.185546875 [0.134765625, 0.238330078] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([365], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.556640625 | 0.263671875 [0.212890625, 0.3125] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([625], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.5546875 | 0.1953125 [0.142529297, 0.248046875] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([340], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.462890625 | 0.193359375 [0.138671875, 0.25] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([356], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.9140625 | -0.009765625 [-0.0332519531, 0.01171875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.947265625 | 0.0234375 [-0.001953125, 0.0488769531] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.955078125 | 0.025390625 [0.005859375, 0.044921875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.953125 | 0.01953125 [0, 0.0390625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9296875 | 0.017578125 [-0.005859375, 0.044921875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.708984375 | 0.15234375 [0.103515625, 0.201171875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.66796875 | 0.064453125 [0.015625, 0.115234375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.79296875 | 0.2265625 [0.177734375, 0.2734375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.814453125 | 0.193359375 [0.148388672, 0.240234375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.669921875 | 0.025390625 [-0.0312988281, 0.076171875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.7109375 | -0.0625 [-0.109423828, -0.01171875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([111], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.8828125 | 0.08203125 [0.044921875, 0.119140625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([113], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.87109375 | 0.099609375 [0.060546875, 0.140625] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([146], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.87109375 | 0.02734375 [-0.01171875, 0.0625] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([152], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.81640625 | 0.07421875 [0.03515625, 0.115234375] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([114], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.33203125 | 0.064453125 [0.009765625, 0.1171875] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([567], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.478515625 | 0.125 [0.072265625, 0.17578125] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([643], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.513671875 | 0.205078125 [0.154296875, 0.257861328] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([821], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.5078125 | 0.126953125 [0.0703125, 0.181640625] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([788], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.4140625 | 0.126953125 [0.0663574219, 0.18359375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([660], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.91015625 | 0.001953125 [-0.021484375, 0.025390625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.9375 | 0.021484375 [-0.00390625, 0.0469238281] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.9296875 | 0.013671875 [-0.01171875, 0.037109375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.947265625 | 0.005859375 [-0.017578125, 0.02734375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.939453125 | 0.037109375 [0.01171875, 0.0625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.630859375 | 0.1171875 [0.068359375, 0.164111328] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.5859375 | -0.013671875 [-0.0684082031, 0.0390625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.71875 | 0.142578125 [0.095703125, 0.19140625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.748046875 | 0.107421875 [0.05859375, 0.15625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.623046875 | -0.01171875 [-0.0625, 0.041015625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 1 | 0.255859375 [0.21875, 0.29296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([97], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.548828125 | -0.208984375 [-0.263671875, -0.150390625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([92], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.619140625 | -0.12890625 [-0.18359375, -0.07421875] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([96], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.72265625 | -0.09375 [-0.14453125, -0.04296875] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([91], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.580078125 | -0.140625 [-0.193359375, -0.08984375] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([76], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.966796875 | 0.712890625 [0.677685547, 0.75] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([556], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.0703125 | -0.251953125 [-0.29296875, -0.208935547] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([206], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.072265625 | -0.220703125 [-0.26171875, -0.17578125] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([226], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.111328125 | -0.248046875 [-0.294921875, -0.19921875] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([244], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.09765625 | -0.171875 [-0.216796875, -0.130859375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([210], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 1 | 0.076171875 [0.052734375, 0.099609375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.90234375 | -0.021484375 [-0.04296875, 0] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.931640625 | 0.001953125 [-0.015625, 0.021484375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.931640625 | -0.001953125 [-0.017578125, 0.013671875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.923828125 | 0.01171875 [-0.0078125, 0.03515625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.9765625 | 0.419921875 [0.382763672, 0.462890625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.431640625 | -0.171875 [-0.220703125, -0.12109375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.384765625 | -0.181640625 [-0.228515625, -0.136669922] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.482421875 | -0.138671875 [-0.19140625, -0.083984375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.4296875 | -0.21484375 [-0.269580078, -0.162109375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 1 | 0.7734375 / 1 | 0.2265625 [0.189453125, 0.263671875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([56], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.5234375 | -0.27734375 [-0.328173828, -0.22265625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([120], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.69140625 | -0.080078125 [-0.126953125, -0.025390625] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([123], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.705078125 | -0.138671875 [-0.1875, -0.08984375] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([132], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.611328125 | -0.130859375 [-0.1796875, -0.08203125] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([129], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.97265625 | 0.705078125 [0.666015625, 0.748046875] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([484], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.056640625 | -0.296875 [-0.33984375, -0.251953125] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([336], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.087890625 | -0.220703125 [-0.265625, -0.177734375] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([367], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.0859375 | -0.294921875 [-0.33984375, -0.248046875] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([302], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.0546875 | -0.232421875 [-0.28125, -0.1875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([306], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 1 | 0.091796875 [0.06640625, 0.117236328] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.900390625 | -0.015625 [-0.0390625, 0.005859375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.927734375 | 0.01171875 [-0.0078125, 0.029296875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.931640625 | -0.009765625 [-0.029296875, 0.0078125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.92578125 | 0.0234375 [-0.001953125, 0.046875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.974609375 | 0.4609375 [0.416015625, 0.505859375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.37890625 | -0.220703125 [-0.273486328, -0.165966797] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.37890625 | -0.197265625 [-0.242236328, -0.148388672] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.43359375 | -0.20703125 [-0.255908203, -0.15625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.384765625 | -0.25 [-0.29296875, -0.19921875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| rarity_cutoff_equal_seed2 | 0 | 1.09972191 | 0 | 0.0265623486 | 0 |
| rarity_cutoff_equal_seed2 | 1000 | 1.08467722 | 0 | 1.76147275e-05 | 0 |
| rarity_cutoff_equal_seed2 | 2000 | 1.08040416 | 0 | 5.73102134e-05 | 0 |
| rarity_cutoff_equal_seed2 | 5000 | 1.07707095 | 0 | 1.70211538e-05 | 0 |
| rarity_cutoff_equal_seed2 | 10000 | 1.08139515 | 0 | 3.21231235e-05 | 0 |
| rarity_cutoff_equal_seed2 | 15000 | 1.08399677 | 0 | 9.86769831e-05 | 0 |
| rarity_cutoff_equal_seed2 | 20000 | 1.07795596 | 0 | 3.95486304e-05 | 0 |
| rarity_cutoff_original_seed2 | 0 | 1.08940065 | 0 | 0.0838733646 | 0 |
| rarity_cutoff_original_seed2 | 1000 | 1.03078699 | 0 | 0.00232477897 | 0 |
| rarity_cutoff_original_seed2 | 2000 | 1.05905712 | 0 | 0.00147201363 | 0 |
| rarity_cutoff_original_seed2 | 5000 | 1.04869461 | 0 | 0.00055781389 | 0 |
| rarity_cutoff_original_seed2 | 10000 | 1.05538893 | 0 | 0.000440402813 | 0 |
| rarity_cutoff_original_seed2 | 15000 | 1.03411603 | 0 | 0.000281937246 | 0 |
| rarity_cutoff_original_seed2 | 20000 | 1.03889287 | 0 | 0.000159978744 | 0 |
| rarity_decoy_equal_seed2 | 0 | 1.10086131 | 0 | 0.0265623486 | 0 |
| rarity_decoy_equal_seed2 | 1000 | 1.08484268 | 0 | 4.58909718e-05 | 0 |
| rarity_decoy_equal_seed2 | 2000 | 1.08058619 | 0 | 7.05267186e-05 | 0 |
| rarity_decoy_equal_seed2 | 5000 | 1.07710302 | 0 | 1.70143135e-05 | 0 |
| rarity_decoy_equal_seed2 | 10000 | 1.0813936 | 0 | 3.1675864e-05 | 0 |
| rarity_decoy_equal_seed2 | 15000 | 1.08401215 | 0 | 0.000104819604 | 0 |
| rarity_decoy_equal_seed2 | 20000 | 1.07793856 | 0 | 4.09071455e-05 | 0 |
| rarity_decoy_original_seed2 | 0 | 1.08999085 | 0 | 0.0838733646 | 0 |
| rarity_decoy_original_seed2 | 1000 | 1.02914441 | 0 | 0.00237787253 | 0 |
| rarity_decoy_original_seed2 | 2000 | 1.05745494 | 0 | 0.00190774591 | 0 |
| rarity_decoy_original_seed2 | 5000 | 1.04930544 | 0 | 0.000537749419 | 0 |
| rarity_decoy_original_seed2 | 10000 | 1.05541873 | 0 | 0.000439599482 | 0 |
| rarity_decoy_original_seed2 | 15000 | 1.03358853 | 0 | 0.000464843394 | 0 |
| rarity_decoy_original_seed2 | 20000 | 1.03911269 | 0 | 0.000220278626 | 0 |
| rarity_uniform_equal_seed2 | 0 | 1.0997026 | 0 | 0.0265623486 | 0 |
| rarity_uniform_equal_seed2 | 1000 | 1.08439505 | 0 | 2.08760651e-05 | 0 |
| rarity_uniform_equal_seed2 | 2000 | 1.08031869 | 0 | 6.71052083e-05 | 0 |
| rarity_uniform_equal_seed2 | 5000 | 1.07717252 | 0 | 2.42738406e-05 | 0 |
| rarity_uniform_equal_seed2 | 10000 | 1.08139765 | 0 | 3.51278999e-05 | 0 |
| rarity_uniform_equal_seed2 | 15000 | 1.08397639 | 0 | 0.000111015225 | 0 |
| rarity_uniform_equal_seed2 | 20000 | 1.07795656 | 0 | 3.89530277e-05 | 0 |
| rarity_uniform_original_seed2 | 0 | 1.09055185 | 0 | 0.0838733646 | 0 |
| rarity_uniform_original_seed2 | 1000 | 1.02808809 | 0 | 0.0020011176 | 0 |
| rarity_uniform_original_seed2 | 2000 | 1.05817652 | 0 | 0.00139650043 | 0 |
| rarity_uniform_original_seed2 | 5000 | 1.04873502 | 0 | 0.000674115571 | 0 |
| rarity_uniform_original_seed2 | 10000 | 1.0559504 | 0 | 0.000426274364 | 0 |
| rarity_uniform_original_seed2 | 15000 | 1.03420711 | 0 | 0.000262472113 | 0 |
| rarity_uniform_original_seed2 | 20000 | 1.0387516 | 0 | 0.000174531007 | 0 |

## dose

### Seed 0 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

The uniform rarity rows are the shared 0% dose controls, not additional runs.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| rarity_uniform_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 124/24435, 45/24435, 1685/24435, 127/24435, 789/24435 | 0/24435 | not applicable |
| rarity_uniform_original_seed0 | B_INCOMPLETE | 21/24435; 22/24435; 17/24435; 18/24435 | 105/24435; 114/24435; 95/24435; 115/24435 | 1 / 2 of 101 | 134/24435, 686/24435, 6380/24435, 252/24435, 657/24435 | 0/24435 | not applicable |
| dose_dose100_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 23211/24435, 23480/24435, 23061/24435, 23470/24435, 23309/24435 | 18963/24435 | not applicable |
| dose_dose100_original_seed0 | B_INCOMPLETE | 298/24435; 291/24435; 304/24435; 296/24435 | 2944/24435; 2966/24435; 2955/24435; 2975/24435 | 0 / 22 of 101 | 23861/24435, 23618/24435, 23357/24435, 23287/24435, 23517/24435 | 20012/24435 | not applicable |
| dose_dose10_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 23581/24435, 22785/24435, 23092/24435, 23011/24435, 22662/24435 | 17692/24435 | not applicable |
| dose_dose10_original_seed0 | B_INCOMPLETE | 160/24435; 156/24435; 156/24435; 152/24435 | 669/24435; 670/24435; 638/24435; 661/24435 | 1 / 10 of 101 | 23488/24435, 22882/24435, 23270/24435, 22784/24435, 22770/24435 | 17653/24435 | not applicable |
| dose_dose1_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 22485/24435, 21807/24435, 21806/24435, 21630/24435, 21908/24435 | 12780/24435 | not applicable |
| dose_dose1_original_seed0 | B_INCOMPLETE | 81/24435; 75/24435; 82/24435; 70/24435 | 449/24435; 457/24435; 460/24435; 464/24435 | 2 / 7 of 101 | 22466/24435, 22020/24435, 21917/24435, 21143/24435, 21645/24435 | 12495/24435 | not applicable |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed0 | 39581042 | 0 / 0 | {'12': 190111, '13': 1493635, '23': 131282, '24': 3438039} | {'10': 189640, '16': 1494343, '20': 130786, '27': 3437884} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| rarity_uniform_original_seed0 | 39584565 | 0 / 0 | {'12': 205614, '13': 1493253, '23': 131346, '24': 3148592} | {'10': 206076, '16': 1493767, '20': 131073, '27': 3148191} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| dose_dose100_equal_seed0 | 39581042 | 39581042 / 1 | {'12': 190111, '13': 1493635, '23': 131282, '24': 3438039} | {'10': 189640, '16': 1494343, '20': 130786, '27': 3437884} | not applicable |
| dose_dose100_original_seed0 | 39584565 | 39584565 / 1 | {'12': 205614, '13': 1493253, '23': 131346, '24': 3148592} | {'10': 206076, '16': 1493767, '20': 131073, '27': 3148191} | not applicable |
| dose_dose10_equal_seed0 | 39581042 | 3956238 / 0.0999528512 | {'12': 190111, '13': 1493635, '23': 131282, '24': 3438039} | {'10': 189640, '16': 1494343, '20': 130786, '27': 3437884} | not applicable |
| dose_dose10_original_seed0 | 39584565 | 3957692 / 0.0999806869 | {'12': 205614, '13': 1493253, '23': 131346, '24': 3148592} | {'10': 206076, '16': 1493767, '20': 131073, '27': 3148191} | not applicable |
| dose_dose1_equal_seed0 | 39581042 | 394846 / 0.00997563429 | {'12': 190111, '13': 1493635, '23': 131282, '24': 3438039} | {'10': 189640, '16': 1494343, '20': 130786, '27': 3437884} | not applicable |
| dose_dose1_original_seed0 | 39584565 | 395368 / 0.00998793343 | {'12': 205614, '13': 1493253, '23': 131346, '24': 3148592} | {'10': 206076, '16': 1493767, '20': 131073, '27': 3148191} | not applicable |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rarity_uniform_equal_seed0 | 0.00278943544/0.00279712677 (n=32) | 0.00278866664/0.00279562175 (n=32) | 0.00279151765/0.00280442834 (n=64) | 0.00279415282/0.00281070173 (n=64) | 0.00279749837/0.00281715393 (n=64) | 0.00280166883/0.00282619894 (n=64) | 0.0028044146/0.00282207131 (n=64) | 0.0028041515/0.00283180177 (n=64) | 0.00281133549/0.0028372854 (n=64) | 0.0028104973/0.00283369422 (n=64) | 0.00279157384 / 0.00281070173 / True | 0.00280492768 / 0.0028372854 / True |
| rarity_uniform_original_seed0 | 0.00285869162/0.00300101191 (n=32) | 0.00597489811/0.00766710937 (n=32) | 0.00460545917/0.00754839182 (n=64) | 0.00567261502/0.0559804291 (n=64) | 0.00965221541/0.233786002 (n=64) | 0.00808832247/0.0951221734 (n=64) | 0.015495737/0.250123315 (n=64) | 0.0103035322/0.060670957 (n=64) | 0.0286126832/0.249943078 (n=64) | 0.0170383909/0.249137938 (n=64) | 0.00489828968 / 0.0559804291 / False | 0.0148651469 / 0.250123315 / False |
| dose_dose100_equal_seed0 | 0.00267488649/0.00307805836 (n=32) | 0.0028224336/0.00332091749 (n=32) | 0.00280399923/0.00345279276 (n=64) | 0.0028491558/0.0035675317 (n=64) | 0.00294759893/0.00421655178 (n=64) | 0.00299264025/0.00524799526 (n=64) | 0.00307167298/0.00498390198 (n=64) | 0.00310781086/0.0042437911 (n=64) | 0.00311355456/0.00462703407 (n=64) | 0.00323305535/0.00432547927 (n=64) | 0.00280060503 / 0.0035675317 / True | 0.00307772215 / 0.00524799526 / True |
| dose_dose100_original_seed0 | 0.00382910762/0.00973947346 (n=32) | 0.0169020363/0.0367555469 (n=32) | 0.0113370887/0.047837615 (n=64) | 0.0142678565/0.232106373 (n=64) | 0.0180934191/0.256146908 (n=64) | 0.0200667862/0.243248463 (n=64) | 0.0194099616/0.252034433 (n=64) | 0.0158447704/0.127415627 (n=64) | 0.0251976425/0.265897684 (n=64) | 0.0148869697/0.160604984 (n=64) | 0.0119901724 / 0.232106373 / False | 0.0189165916 / 0.265897684 / False |
| dose_dose10_equal_seed0 | 0.00278223958/0.00298543274 (n=32) | 0.00292257871/0.00333236158 (n=32) | 0.0029028866/0.00469492376 (n=64) | 0.00285951607/0.0032171458 (n=64) | 0.00298657292/0.00397773087 (n=64) | 0.00304682925/0.00366204977 (n=64) | 0.00305705704/0.00446312129 (n=64) | 0.00309240585/0.00417816639 (n=64) | 0.00323664444/0.00528986752 (n=64) | 0.00326223392/0.00428366661 (n=64) | 0.00287160394 / 0.00469492376 / True | 0.0031136239 / 0.00528986752 / True |
| dose_dose10_original_seed0 | 0.00743879308/0.013866663 (n=32) | 0.0136029907/0.0359167755 (n=32) | 0.00766357209/0.016657576 (n=64) | 0.00992813695/0.0765210241 (n=64) | 0.0193686645/0.248212874 (n=64) | 0.0093113418/0.0577840358 (n=64) | 0.0177280636/0.248595312 (n=64) | 0.0218452769/0.248450026 (n=64) | 0.0264066545/0.261849299 (n=64) | 0.0288636108/0.250875056 (n=64) | 0.00937086697 / 0.0765210241 / False | 0.0205872687 / 0.261849299 / False |
| dose_dose1_equal_seed0 | 0.00268447539/0.00285199285 (n=32) | 0.00291100284/0.00354494154 (n=32) | 0.00282099913/0.00343051553 (n=64) | 0.00285602384/0.00369548798 (n=64) | 0.00287738792/0.00395336747 (n=64) | 0.00285009318/0.00370573997 (n=64) | 0.00289419829/0.00372439623 (n=64) | 0.00289155054/0.0036637485 (n=64) | 0.00287081744/0.00369051099 (n=64) | 0.00291457563/0.00460581481 (n=64) | 0.0028249207 / 0.00369548798 / True | 0.00288310383 / 0.00460581481 / True |
| dose_dose1_original_seed0 | 0.00525162276/0.00777484477 (n=32) | 0.00893151038/0.016618669 (n=32) | 0.00652098714/0.0160438418 (n=64) | 0.00872339495/0.161262125 (n=64) | 0.0120045928/0.252606645 (n=64) | 0.00859903207/0.0542719066 (n=64) | 0.018777089/0.251413047 (n=64) | 0.0144470315/0.250249505 (n=64) | 0.0135894185/0.217733324 (n=64) | 0.010345615/0.0705872476 (n=64) | 0.00744531622 / 0.161262125 / False | 0.0129604631 / 0.252606645 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed0 | 3.56903549e-05 / 3.57095082e-05 (n=20282) | not recorded / 3.77963297e-05 | none | 9.23424959e-05 / True | 0 / True |
| rarity_uniform_original_seed0 | 0.000215068465 / 0.000285757449 (n=24185) | 0.998397113 / 0.248876572 | law_TV, rerender, swaps | 0.0336352661 / False | 0 / True |
| dose_dose100_equal_seed0 | 4.13875029e-05 / 3.88910666e-05 (n=20282) | not recorded / 0.000566266943 | none | 0.00128781796 / True | 0 / True |
| dose_dose100_original_seed0 | 0.0010227144 / 0.00104855427 (n=24185) | 0.98931094 / 0.255900502 | law_TV, rerender, swaps | 0.0415359586 / False | 0 / True |
| dose_dose10_equal_seed0 | 3.98721604e-05 / 3.84366012e-05 (n=20282) | not recorded / 0.000577118713 | none | 0.00172042847 / True | 0 / True |
| dose_dose10_original_seed0 | 0.000632161075 / 0.000566660681 (n=24185) | 0.995803432 / 0.25081268 | law_TV, rerender, swaps | 0.0229448006 / False | 0 / True |
| dose_dose1_equal_seed0 | 3.7348076e-05 / 3.44197739e-05 (n=20282) | not recorded / 0.000797496643 | none | 0.000946685672 / True | 0 / True |
| dose_dose1_original_seed0 | 0.000369042989 / 0.000365287369 (n=24185) | 0.997172701 / 0.247192487 | law_TV, rerender, swaps | 0.0221762657 / False | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| rarity_uniform_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_equal_seed0 | A_swap_exact_row | 64 | 0.00278815464 / 0.00279918313 |
| rarity_uniform_equal_seed0 | both_swap_exact_row | 64 | 0.00278815464 / 0.00279918313 |
| rarity_uniform_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_equal_seed0 | neutral_N | 192 | 0.00279403625 / 0.00281150639 |
| rarity_uniform_equal_seed0 | neutral_raw_swap_stability | 128 | 2.92410841e-05 / 8.37743282e-05 |
| rarity_uniform_equal_seed0 | raw_swap_effect | 64 | 2.51145102e-05 / 7.14808702e-05 |
| rarity_uniform_equal_seed0 | raw_swap_exact_row | 64 | 0.00278815464 / 0.00279918313 |
| rarity_uniform_equal_seed0 | raw_swap_stability | 128 | 0.00140663458 / 0.00279918313 |
| rarity_uniform_equal_seed0 | reset_L | 160 | 0.002791523 / 0.00281581283 |
| rarity_uniform_equal_seed0 | same_category_substitution | 128 | 2.92410841e-05 / 8.37743282e-05 |
| rarity_uniform_equal_seed0 | set_H | 160 | 0.00279245777 / 0.00281183422 |
| rarity_uniform_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00279259984 / 0.00280271471 |
| rarity_uniform_original_seed0 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_original_seed0 | A_swap_exact_row | 64 | 0.250536802 / 0.251687922 |
| rarity_uniform_original_seed0 | both_swap_exact_row | 64 | 0.00436772651 / 0.0062135011 |
| rarity_uniform_original_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_original_seed0 | neutral_N | 192 | 0.00501435017 / 0.0383397788 |
| rarity_uniform_original_seed0 | neutral_raw_swap_stability | 128 | 0.00112070044 / 0.0373269543 |
| rarity_uniform_original_seed0 | raw_swap_effect | 64 | 0.248218665 / 0.249134906 |
| rarity_uniform_original_seed0 | raw_swap_exact_row | 64 | 0.00436772651 / 0.0062135011 |
| rarity_uniform_original_seed0 | raw_swap_stability | 128 | 0.249377734 / 0.251687922 |
| rarity_uniform_original_seed0 | reset_L | 160 | 0.00290810904 / 0.00535829365 |
| rarity_uniform_original_seed0 | same_category_substitution | 128 | 0.00112070044 / 0.0373269543 |
| rarity_uniform_original_seed0 | set_H | 160 | 0.00602366868 / 0.00727634132 |
| rarity_uniform_original_seed0 | upper_state_exchange_same_N | 64 | 0.00473039935 / 0.0124557763 |
| dose_dose100_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| dose_dose100_equal_seed0 | A_swap_exact_row | 64 | 0.00276479986 / 0.00443442166 |
| dose_dose100_equal_seed0 | both_swap_exact_row | 64 | 0.00276479986 / 0.00443442166 |
| dose_dose100_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose100_equal_seed0 | neutral_N | 192 | 0.00283755874 / 0.00469014049 |
| dose_dose100_equal_seed0 | neutral_raw_swap_stability | 128 | 0.000199547736 / 0.000662252307 |
| dose_dose100_equal_seed0 | raw_swap_effect | 64 | 0.000712695997 / 0.00277104974 |
| dose_dose100_equal_seed0 | raw_swap_exact_row | 64 | 0.00276479986 / 0.00443442166 |
| dose_dose100_equal_seed0 | raw_swap_stability | 128 | 0.00173874793 / 0.00443442166 |
| dose_dose100_equal_seed0 | reset_L | 160 | 0.00271743517 / 0.00447155535 |
| dose_dose100_equal_seed0 | same_category_substitution | 128 | 0.000199547736 / 0.000662252307 |
| dose_dose100_equal_seed0 | set_H | 160 | 0.00300234314 / 0.00699132681 |
| dose_dose100_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00281528221 / 0.00456233323 |
| dose_dose100_original_seed0 | A_swap_effect | 64 | 0 / 0 |
| dose_dose100_original_seed0 | A_swap_exact_row | 64 | 0.245612091 / 0.260140389 |
| dose_dose100_original_seed0 | both_swap_exact_row | 64 | 0.0105071554 / 0.0406229347 |
| dose_dose100_original_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose100_original_seed0 | neutral_N | 192 | 0.0129871587 / 0.152221531 |
| dose_dose100_original_seed0 | neutral_raw_swap_stability | 128 | 0.011915173 / 0.140449628 |
| dose_dose100_original_seed0 | raw_swap_effect | 64 | 0.240655574 / 0.26478789 |
| dose_dose100_original_seed0 | raw_swap_exact_row | 64 | 0.0105071554 / 0.0406229347 |
| dose_dose100_original_seed0 | raw_swap_stability | 128 | 0.243133832 / 0.26478789 |
| dose_dose100_original_seed0 | reset_L | 160 | 0.0130966808 / 0.185110435 |
| dose_dose100_original_seed0 | same_category_substitution | 128 | 0.011915173 / 0.140449628 |
| dose_dose100_original_seed0 | set_H | 160 | 0.0151671644 / 0.0592278838 |
| dose_dose100_original_seed0 | upper_state_exchange_same_N | 64 | 0.0112186723 / 0.0572645664 |
| dose_dose10_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| dose_dose10_equal_seed0 | A_swap_exact_row | 64 | 0.00283722905 / 0.00308872759 |
| dose_dose10_equal_seed0 | both_swap_exact_row | 64 | 0.00283722905 / 0.00308872759 |
| dose_dose10_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose10_equal_seed0 | neutral_N | 192 | 0.00286957389 / 0.00391282141 |
| dose_dose10_equal_seed0 | neutral_raw_swap_stability | 128 | 0.000186626567 / 0.000666856766 |
| dose_dose10_equal_seed0 | raw_swap_effect | 64 | 0.000370807014 / 0.00201225281 |
| dose_dose10_equal_seed0 | raw_swap_exact_row | 64 | 0.00283722905 / 0.00308872759 |
| dose_dose10_equal_seed0 | raw_swap_stability | 128 | 0.00160401803 / 0.00308872759 |
| dose_dose10_equal_seed0 | reset_L | 160 | 0.00280209845 / 0.00374653935 |
| dose_dose10_equal_seed0 | same_category_substitution | 128 | 0.000186626567 / 0.000666856766 |
| dose_dose10_equal_seed0 | set_H | 160 | 0.00291335145 / 0.00368730724 |
| dose_dose10_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00285714609 / 0.0033236146 |
| dose_dose10_original_seed0 | A_swap_effect | 64 | 0 / 0 |
| dose_dose10_original_seed0 | A_swap_exact_row | 64 | 0.248622136 / 0.256840453 |
| dose_dose10_original_seed0 | both_swap_exact_row | 64 | 0.0103154344 / 0.0339458287 |
| dose_dose10_original_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose10_original_seed0 | neutral_N | 192 | 0.00921233887 / 0.0756864101 |
| dose_dose10_original_seed0 | neutral_raw_swap_stability | 128 | 0.0078653869 / 0.0737927705 |
| dose_dose10_original_seed0 | raw_swap_effect | 64 | 0.240489261 / 0.247829042 |
| dose_dose10_original_seed0 | raw_swap_exact_row | 64 | 0.0103154344 / 0.0339458287 |
| dose_dose10_original_seed0 | raw_swap_stability | 128 | 0.244555698 / 0.256840453 |
| dose_dose10_original_seed0 | reset_L | 160 | 0.00940865874 / 0.188656226 |
| dose_dose10_original_seed0 | same_category_substitution | 128 | 0.0078653869 / 0.0737927705 |
| dose_dose10_original_seed0 | set_H | 160 | 0.0112932699 / 0.0418146551 |
| dose_dose10_original_seed0 | upper_state_exchange_same_N | 64 | 0.0078803791 / 0.0226299018 |
| dose_dose1_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| dose_dose1_equal_seed0 | A_swap_exact_row | 64 | 0.00281319092 / 0.00324910879 |
| dose_dose1_equal_seed0 | both_swap_exact_row | 64 | 0.00281319092 / 0.00324910879 |
| dose_dose1_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose1_equal_seed0 | neutral_N | 192 | 0.00282827431 / 0.00345507264 |
| dose_dose1_equal_seed0 | neutral_raw_swap_stability | 128 | 0.000107097439 / 0.000362843275 |
| dose_dose1_equal_seed0 | raw_swap_effect | 64 | 0.000550569501 / 0.00246836245 |
| dose_dose1_equal_seed0 | raw_swap_exact_row | 64 | 0.00281319092 / 0.00324910879 |
| dose_dose1_equal_seed0 | raw_swap_stability | 128 | 0.00168188021 / 0.00324910879 |
| dose_dose1_equal_seed0 | reset_L | 160 | 0.00279543251 / 0.00363606215 |
| dose_dose1_equal_seed0 | same_category_substitution | 128 | 0.000107097439 / 0.000362843275 |
| dose_dose1_equal_seed0 | set_H | 160 | 0.00293639647 / 0.00402662158 |
| dose_dose1_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00282393512 / 0.00330200791 |
| dose_dose1_original_seed0 | A_swap_effect | 64 | 0 / 0 |
| dose_dose1_original_seed0 | A_swap_exact_row | 64 | 0.249823267 / 0.253119148 |
| dose_dose1_original_seed0 | both_swap_exact_row | 64 | 0.00754839077 / 0.0321055949 |
| dose_dose1_original_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose1_original_seed0 | neutral_N | 192 | 0.0070576395 / 0.0642769784 |
| dose_dose1_original_seed0 | neutral_raw_swap_stability | 128 | 0.00351819576 / 0.0630522743 |
| dose_dose1_original_seed0 | raw_swap_effect | 64 | 0.24439701 / 0.249037959 |
| dose_dose1_original_seed0 | raw_swap_exact_row | 64 | 0.00754839077 / 0.0321055949 |
| dose_dose1_original_seed0 | raw_swap_stability | 128 | 0.247110138 / 0.253119148 |
| dose_dose1_original_seed0 | reset_L | 160 | 0.00879162014 / 0.187914714 |
| dose_dose1_original_seed0 | same_category_substitution | 128 | 0.00351819576 / 0.0630522743 |
| dose_dose1_original_seed0 | set_H | 160 | 0.00916083027 / 0.0413860679 |
| dose_dose1_original_seed0 | upper_state_exchange_same_N | 64 | 0.00647706585 / 0.0235783905 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.818359375 | 0.052734375 [0.013671875, 0.09765625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([90], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.83203125 | 0.052734375 [0.0116699219, 0.09375] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([104], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.7890625 | 0.015625 [-0.029296875, 0.0605957031] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([102], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.857421875 | 0.056640625 [0.021484375, 0.0957519531] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([99], []) |
| rarity_uniform_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.83203125 | 0.03515625 [-0.001953125, 0.07421875] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([110], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.50390625 | 0.140625 [0.091796875, 0.189501953] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([249], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.58203125 | 0.2578125 [0.20703125, 0.3203125] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([257], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.26953125 | 0.033203125 [-0.017578125, 0.0820800781] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([271], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.541015625 | 0.2421875 [0.183544922, 0.300830078] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([306], []) |
| rarity_uniform_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.564453125 | 0.267578125 [0.212890625, 0.322265625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([418], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.91796875 | 0.009765625 [-0.0137207031, 0.037109375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.935546875 | 0.017578125 [-0.01171875, 0.04296875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.94140625 | 0.015625 [-0.00390625, 0.037109375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.953125 | 0.03125 [0.009765625, 0.052734375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.955078125 | 0.01953125 [-0.001953125, 0.041015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.6640625 | 0.103515625 [0.05859375, 0.15234375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.720703125 | 0.158203125 [0.111328125, 0.201220703] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.576171875 | -0.052734375 [-0.0996582031, -0.00385742188] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.751953125 | 0.126953125 [0.076171875, 0.173828125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.740234375 | 0.181640625 [0.134716797, 0.23046875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.794921875 | 0.001953125 [-0.037109375, 0.04296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([142], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.8359375 | 0.0390625 [-0.00390625, 0.0781738281] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([121], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.783203125 | -0.01953125 [-0.06640625, 0.0234375] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([119], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.85546875 | 0.021484375 [-0.01953125, 0.064453125] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([132], []) |
| rarity_uniform_equal_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.830078125 | 0.025390625 [-0.015625, 0.064453125] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([165], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.439453125 | 0.05859375 [0.0078125, 0.109375] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([528], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.41015625 | 0.0703125 [0.017578125, 0.125] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([337], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.1875 | -0.087890625 [-0.13671875, -0.0390625] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([572], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.41796875 | 0.12109375 [0.068359375, 0.177734375] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([322], []) |
| rarity_uniform_equal_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.42578125 | 0.1171875 [0.05859375, 0.169921875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([682], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.912109375 | 0.001953125 [-0.02734375, 0.03125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.93359375 | 0.015625 [-0.0078125, 0.0390625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.939453125 | 0.013671875 [-0.005859375, 0.033203125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.93359375 | 0 [-0.021484375, 0.021484375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.939453125 | 0.017578125 [-0.001953125, 0.0390625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.5625 | 0.001953125 [-0.044921875, 0.0488769531] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.5859375 | 0.02734375 [-0.02734375, 0.080078125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.4765625 | -0.125 [-0.171875, -0.07421875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.580078125 | -0.001953125 [-0.05078125, 0.05078125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.6328125 | 0.083984375 [0.033203125, 0.136767578] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 1 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([44], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.59375 | -0.185546875 [-0.232470703, -0.13671875] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([81], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.58203125 | -0.19140625 [-0.24609375, -0.140625] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([85], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.533203125 | -0.267578125 [-0.318359375, -0.216796875] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([94], []) |
| rarity_uniform_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.75390625 | -0.04296875 [-0.0859375, 0] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([86], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.96875 | 0.60546875 [0.560546875, 0.646484375] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([784], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.0859375 | -0.23828125 [-0.28125, -0.189453125] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([212], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.0625 | -0.173828125 [-0.21484375, -0.12890625] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([216], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.083984375 | -0.21484375 [-0.26171875, -0.171875] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([218], []) |
| rarity_uniform_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.11328125 | -0.18359375 [-0.23046875, -0.138671875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([207], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 1 | 0.091796875 [0.068359375, 0.117236328] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.91796875 | 0 [-0.025390625, 0.0234375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.9296875 | 0.00390625 [-0.009765625, 0.01953125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.9375 | 0.015625 [0, 0.033203125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.951171875 | 0.015625 [-0.001953125, 0.033203125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.984375 | 0.423828125 [0.380859375, 0.466796875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.4140625 | -0.1484375 [-0.197314453, -0.099609375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.388671875 | -0.240234375 [-0.29296875, -0.191357422] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.396484375 | -0.228515625 [-0.279345703, -0.1796875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.439453125 | -0.119140625 [-0.169921875, -0.06640625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 1 | 0.79296875 / 1 | 0.20703125 [0.173828125, 0.244140625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([39], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.642578125 | -0.154296875 [-0.201171875, -0.10546875] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([134], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.544921875 | -0.2578125 [-0.312548828, -0.205078125] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([122], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.611328125 | -0.22265625 [-0.269580078, -0.17578125] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([168], []) |
| rarity_uniform_original_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.7890625 | -0.015625 [-0.056640625, 0.0234375] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([133], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.982421875 | 0.6015625 [0.55859375, 0.642578125] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([428], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.052734375 | -0.287109375 [-0.328173828, -0.2421875] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([280], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.048828125 | -0.2265625 [-0.271484375, -0.18359375] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([266], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.064453125 | -0.232421875 [-0.275390625, -0.189453125] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([330], []) |
| rarity_uniform_original_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.103515625 | -0.205078125 [-0.250048828, -0.158203125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([288], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.998046875 | 0.087890625 [0.0625, 0.11328125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.90625 | -0.01171875 [-0.0390625, 0.013671875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.9296875 | 0.00390625 [-0.013671875, 0.021484375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.9296875 | -0.00390625 [-0.0234375, 0.015625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.9375 | 0.015625 [-0.0078125, 0.041015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.984375 | 0.423828125 [0.382763672, 0.46875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.365234375 | -0.193359375 [-0.23828125, -0.146435547] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.41015625 | -0.19140625 [-0.238330078, -0.14453125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.38671875 | -0.1953125 [-0.24609375, -0.148388672] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.42578125 | -0.123046875 [-0.173828125, -0.0703125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.990234375 | 0.224609375 [0.185546875, 0.26171875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([62], []) |
| dose_dose100_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.939453125 | 0.16015625 [0.123046875, 0.203125] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([79], []) |
| dose_dose100_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.955078125 | 0.181640625 [0.142578125, 0.21875] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([89], []) |
| dose_dose100_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.96875 | 0.16796875 [0.134765625, 0.203125] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([83], []) |
| dose_dose100_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.953125 | 0.15625 [0.12109375, 0.1953125] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([43], []) |
| dose_dose100_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.919921875 | 0.556640625 [0.5078125, 0.601611328] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([300], []) |
| dose_dose100_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.916015625 | 0.591796875 [0.552734375, 0.63671875] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([298], []) |
| dose_dose100_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.90625 | 0.669921875 [0.626953125, 0.712890625] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([313], []) |
| dose_dose100_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.93359375 | 0.634765625 [0.591748047, 0.679736328] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([394], []) |
| dose_dose100_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.921875 | 0.625 [0.578125, 0.66796875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([241], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.984375 | 0.076171875 [0.052734375, 0.1015625] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.953125 | 0.03515625 [0.009765625, 0.060546875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.9765625 | 0.05078125 [0.02734375, 0.07421875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.970703125 | 0.048828125 [0.0234375, 0.07421875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.966796875 | 0.03125 [0.009765625, 0.0546875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.9140625 | 0.353515625 [0.310546875, 0.396484375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.912109375 | 0.349609375 [0.308544922, 0.390625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.9140625 | 0.28515625 [0.244140625, 0.328125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.9296875 | 0.3046875 [0.263671875, 0.345703125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.91796875 | 0.359375 [0.31640625, 0.408203125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.94140625 | 0.1484375 [0.111328125, 0.1875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([77], []) |
| dose_dose100_equal_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.876953125 | 0.080078125 [0.041015625, 0.12109375] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([117], []) |
| dose_dose100_equal_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.923828125 | 0.12109375 [0.080078125, 0.16015625] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([150], []) |
| dose_dose100_equal_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.951171875 | 0.1171875 [0.08203125, 0.152392578] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([180], []) |
| dose_dose100_equal_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.9453125 | 0.140625 [0.1015625, 0.177734375] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([109], []) |
| dose_dose100_equal_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.76171875 | 0.380859375 [0.326171875, 0.4375] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([453], []) |
| dose_dose100_equal_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.77734375 | 0.4375 [0.388671875, 0.490234375] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([304], []) |
| dose_dose100_equal_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.736328125 | 0.4609375 [0.410107422, 0.511767578] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([248], []) |
| dose_dose100_equal_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.73828125 | 0.44140625 [0.3828125, 0.494140625] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([491], []) |
| dose_dose100_equal_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.814453125 | 0.505859375 [0.453125, 0.5546875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([223], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.984375 | 0.07421875 [0.05078125, 0.09765625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.947265625 | 0.029296875 [0.00390625, 0.056640625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.96484375 | 0.0390625 [0.013671875, 0.0625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.966796875 | 0.033203125 [0.00971679688, 0.056640625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.9765625 | 0.0546875 [0.033203125, 0.078125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.830078125 | 0.26953125 [0.22265625, 0.314501953] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.86328125 | 0.3046875 [0.2578125, 0.353515625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.830078125 | 0.228515625 [0.181640625, 0.273486328] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.84375 | 0.26171875 [0.21484375, 0.306640625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.89453125 | 0.345703125 [0.298828125, 0.39453125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.99609375 | 0.23046875 [0.19140625, 0.265625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([60], []) |
| dose_dose100_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.9609375 | 0.181640625 [0.146435547, 0.220703125] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([69], []) |
| dose_dose100_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.943359375 | 0.169921875 [0.1328125, 0.20703125] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([73], []) |
| dose_dose100_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.978515625 | 0.177734375 [0.14453125, 0.210986328] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([89], []) |
| dose_dose100_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.984375 | 0.1875 [0.154248047, 0.224658203] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([66], []) |
| dose_dose100_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.9453125 | 0.58203125 [0.533203125, 0.626953125] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([204], []) |
| dose_dose100_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.927734375 | 0.603515625 [0.564453125, 0.650390625] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([314], []) |
| dose_dose100_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.9140625 | 0.677734375 [0.6328125, 0.720703125] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([286], []) |
| dose_dose100_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.92578125 | 0.626953125 [0.58203125, 0.671875] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([254], []) |
| dose_dose100_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.943359375 | 0.646484375 [0.6015625, 0.689453125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([310], []) |
| dose_dose100_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.990234375 | 0.08203125 [0.05859375, 0.107421875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.966796875 | 0.048828125 [0.0253417969, 0.072265625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.96484375 | 0.0390625 [0.015625, 0.0625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.984375 | 0.0625 [0.037109375, 0.0859375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.98828125 | 0.052734375 [0.0312011719, 0.076171875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.94921875 | 0.388671875 [0.34375, 0.43359375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.916015625 | 0.353515625 [0.310546875, 0.39453125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.916015625 | 0.287109375 [0.249951172, 0.330078125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.927734375 | 0.302734375 [0.263623047, 0.345703125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.92578125 | 0.3671875 [0.32421875, 0.4140625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.99609375 | 0.203125 [0.169921875, 0.240234375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([94], []) |
| dose_dose100_original_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.9296875 | 0.1328125 [0.09375, 0.173828125] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([96], []) |
| dose_dose100_original_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.931640625 | 0.12890625 [0.087890625, 0.169921875] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([161], []) |
| dose_dose100_original_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.96484375 | 0.130859375 [0.09765625, 0.166015625] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([108], []) |
| dose_dose100_original_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.962890625 | 0.158203125 [0.1171875, 0.1953125] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([110], []) |
| dose_dose100_original_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.88671875 | 0.505859375 [0.458984375, 0.55078125] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([821], []) |
| dose_dose100_original_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.849609375 | 0.509765625 [0.462890625, 0.560546875] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([436], []) |
| dose_dose100_original_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.794921875 | 0.51953125 [0.46875, 0.568359375] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([561], []) |
| dose_dose100_original_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.833984375 | 0.537109375 [0.486328125, 0.583984375] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([391], []) |
| dose_dose100_original_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.810546875 | 0.501953125 [0.44921875, 0.55078125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([494], []) |
| dose_dose100_original_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.990234375 | 0.080078125 [0.0546875, 0.107421875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.955078125 | 0.037109375 [0.01171875, 0.064453125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.970703125 | 0.044921875 [0.021484375, 0.068359375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.974609375 | 0.041015625 [0.017578125, 0.06640625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.974609375 | 0.052734375 [0.029296875, 0.076171875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.921875 | 0.361328125 [0.318310547, 0.40625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.869140625 | 0.310546875 [0.265625, 0.359423828] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.841796875 | 0.240234375 [0.1953125, 0.287109375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.89453125 | 0.3125 [0.26953125, 0.35546875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.86328125 | 0.314453125 [0.26953125, 0.363330078] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.9921875 | 0.2265625 [0.1875, 0.261767578] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([55], []) |
| dose_dose10_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.947265625 | 0.16796875 [0.1328125, 0.203125] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([74], []) |
| dose_dose10_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.951171875 | 0.177734375 [0.138671875, 0.212890625] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([74], []) |
| dose_dose10_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.9765625 | 0.17578125 [0.14453125, 0.209033203] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([90], []) |
| dose_dose10_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.970703125 | 0.173828125 [0.13671875, 0.2109375] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([66], []) |
| dose_dose10_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.9375 | 0.57421875 [0.525390625, 0.6171875] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([211], []) |
| dose_dose10_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.90625 | 0.58203125 [0.541015625, 0.627001953] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([254], []) |
| dose_dose10_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.919921875 | 0.68359375 [0.640625, 0.728515625] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([295], []) |
| dose_dose10_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.919921875 | 0.62109375 [0.580078125, 0.666064453] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([293], []) |
| dose_dose10_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.921875 | 0.625 [0.580078125, 0.66796875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([285], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.994140625 | 0.0859375 [0.060546875, 0.11328125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.958984375 | 0.041015625 [0.015625, 0.06640625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.970703125 | 0.044921875 [0.021484375, 0.068359375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.98828125 | 0.06640625 [0.04296875, 0.087890625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.97265625 | 0.037109375 [0.015625, 0.056640625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.955078125 | 0.39453125 [0.353515625, 0.435595703] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.90234375 | 0.33984375 [0.294873047, 0.380908203] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.923828125 | 0.294921875 [0.257763672, 0.333984375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.9375 | 0.3125 [0.271484375, 0.357421875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.896484375 | 0.337890625 [0.29296875, 0.384814453] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.9140625 | 0.12109375 [0.083984375, 0.162109375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([88], []) |
| dose_dose10_equal_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.8203125 | 0.0234375 [-0.021484375, 0.06640625] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([86], []) |
| dose_dose10_equal_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.8828125 | 0.080078125 [0.0390625, 0.12109375] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([125], []) |
| dose_dose10_equal_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.943359375 | 0.109375 [0.072265625, 0.150390625] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([110], []) |
| dose_dose10_equal_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.904296875 | 0.099609375 [0.056640625, 0.134765625] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([128], []) |
| dose_dose10_equal_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.81640625 | 0.435546875 [0.38671875, 0.490234375] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([178], []) |
| dose_dose10_equal_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.666015625 | 0.326171875 [0.271484375, 0.382861328] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([132], []) |
| dose_dose10_equal_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.732421875 | 0.45703125 [0.400390625, 0.5078125] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([314], []) |
| dose_dose10_equal_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.7734375 | 0.4765625 [0.427734375, 0.525390625] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([479], []) |
| dose_dose10_equal_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.744140625 | 0.435546875 [0.380859375, 0.490234375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([381], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.970703125 | 0.060546875 [0.033203125, 0.087890625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.94921875 | 0.03125 [0.005859375, 0.056640625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.958984375 | 0.033203125 [0.009765625, 0.056640625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.98046875 | 0.046875 [0.0234375, 0.0703125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.96484375 | 0.04296875 [0.021484375, 0.06640625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.88671875 | 0.326171875 [0.279296875, 0.37109375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.791015625 | 0.232421875 [0.185546875, 0.277392578] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.837890625 | 0.236328125 [0.193359375, 0.28125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.8671875 | 0.28515625 [0.236328125, 0.330126953] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.826171875 | 0.27734375 [0.228515625, 0.322265625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.9921875 | 0.2265625 [0.189404297, 0.261767578] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([72], []) |
| dose_dose10_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.958984375 | 0.1796875 [0.140625, 0.21875] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([69], []) |
| dose_dose10_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.962890625 | 0.189453125 [0.150390625, 0.224609375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([72], []) |
| dose_dose10_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.978515625 | 0.177734375 [0.142578125, 0.212939453] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([85], []) |
| dose_dose10_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.962890625 | 0.166015625 [0.130859375, 0.203125] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([92], []) |
| dose_dose10_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.9375 | 0.57421875 [0.52734375, 0.619140625] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([361], []) |
| dose_dose10_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.904296875 | 0.580078125 [0.540966797, 0.625] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([271], []) |
| dose_dose10_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.908203125 | 0.671875 [0.626953125, 0.71484375] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([332], []) |
| dose_dose10_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.904296875 | 0.60546875 [0.560546875, 0.6484375] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([328], []) |
| dose_dose10_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.93359375 | 0.63671875 [0.591796875, 0.677783203] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([378], []) |
| dose_dose10_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.99609375 | 0.087890625 [0.064453125, 0.11328125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.978515625 | 0.060546875 [0.03515625, 0.0859375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.974609375 | 0.048828125 [0.025390625, 0.072265625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.97265625 | 0.05078125 [0.029296875, 0.076171875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.978515625 | 0.04296875 [0.0234375, 0.064453125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.94140625 | 0.380859375 [0.33984375, 0.42578125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.900390625 | 0.337890625 [0.294921875, 0.376953125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.93359375 | 0.3046875 [0.267529297, 0.345703125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.92578125 | 0.30078125 [0.26171875, 0.341796875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.923828125 | 0.365234375 [0.322265625, 0.410205078] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.990234375 | 0.197265625 [0.1640625, 0.232421875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([110], []) |
| dose_dose10_original_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.94140625 | 0.14453125 [0.103515625, 0.181640625] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([114], []) |
| dose_dose10_original_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.962890625 | 0.16015625 [0.122998047, 0.1953125] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([114], []) |
| dose_dose10_original_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.9609375 | 0.126953125 [0.095703125, 0.162158203] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([108], []) |
| dose_dose10_original_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.95703125 | 0.15234375 [0.11328125, 0.185546875] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([125], []) |
| dose_dose10_original_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.90625 | 0.525390625 [0.482421875, 0.570361328] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([632], []) |
| dose_dose10_original_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.814453125 | 0.474609375 [0.4296875, 0.52734375] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([342], []) |
| dose_dose10_original_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.8359375 | 0.560546875 [0.509716797, 0.609375] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([374], []) |
| dose_dose10_original_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.78125 | 0.484375 [0.435546875, 0.533203125] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([402], []) |
| dose_dose10_original_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.8359375 | 0.52734375 [0.4765625, 0.57421875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([300], []) |
| dose_dose10_original_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.990234375 | 0.080078125 [0.0546875, 0.107421875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.96484375 | 0.046875 [0.021484375, 0.072265625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.97265625 | 0.046875 [0.0234375, 0.0703125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.974609375 | 0.041015625 [0.01953125, 0.064453125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.966796875 | 0.044921875 [0.01953125, 0.072265625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.923828125 | 0.36328125 [0.322265625, 0.40625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.853515625 | 0.294921875 [0.25, 0.341796875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.900390625 | 0.298828125 [0.255810547, 0.341796875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.86328125 | 0.28125 [0.236279297, 0.32421875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.8984375 | 0.349609375 [0.304638672, 0.3984375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.982421875 | 0.216796875 [0.177685547, 0.25390625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([71], []) |
| dose_dose1_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.9140625 | 0.134765625 [0.09765625, 0.17578125] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([91], []) |
| dose_dose1_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.94921875 | 0.17578125 [0.138671875, 0.2109375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([84], []) |
| dose_dose1_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.9140625 | 0.11328125 [0.078125, 0.154296875] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([74], []) |
| dose_dose1_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.94921875 | 0.15234375 [0.115234375, 0.19140625] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([84], []) |
| dose_dose1_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.91796875 | 0.5546875 [0.507763672, 0.599609375] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([516], []) |
| dose_dose1_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.857421875 | 0.533203125 [0.48828125, 0.578125] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([320], []) |
| dose_dose1_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.888671875 | 0.65234375 [0.60546875, 0.697265625] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([266], []) |
| dose_dose1_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.888671875 | 0.58984375 [0.544873047, 0.63671875] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([343], []) |
| dose_dose1_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.890625 | 0.59375 [0.548779297, 0.638671875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([412], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.990234375 | 0.08203125 [0.056640625, 0.107470703] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.951171875 | 0.033203125 [0.0078125, 0.05859375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.96875 | 0.04296875 [0.01953125, 0.06640625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.958984375 | 0.037109375 [0.013671875, 0.0605957031] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.974609375 | 0.0390625 [0.01953125, 0.05859375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.912109375 | 0.3515625 [0.3046875, 0.396484375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.859375 | 0.296875 [0.255810547, 0.33984375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.87109375 | 0.2421875 [0.201171875, 0.283203125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.896484375 | 0.271484375 [0.230419922, 0.312548828] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.908203125 | 0.349609375 [0.3046875, 0.39453125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / linear / category3 / 1 | 0.79296875 / 0.927734375 | 0.134765625 [0.099609375, 0.17578125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([80], []) |
| dose_dose1_equal_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.865234375 | 0.068359375 [0.02734375, 0.109375] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([109], []) |
| dose_dose1_equal_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.921875 | 0.119140625 [0.078125, 0.158203125] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([139], []) |
| dose_dose1_equal_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.88671875 | 0.052734375 [0.013671875, 0.09375] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([106], []) |
| dose_dose1_equal_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.931640625 | 0.126953125 [0.08984375, 0.162158203] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([164], []) |
| dose_dose1_equal_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.79296875 | 0.412109375 [0.365234375, 0.46484375] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([377], []) |
| dose_dose1_equal_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.705078125 | 0.365234375 [0.310546875, 0.421875] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([203], []) |
| dose_dose1_equal_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.755859375 | 0.48046875 [0.427734375, 0.533203125] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([269], []) |
| dose_dose1_equal_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.724609375 | 0.427734375 [0.37109375, 0.48046875] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([230], []) |
| dose_dose1_equal_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.84375 | 0.53515625 [0.48828125, 0.582080078] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([468], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.974609375 | 0.064453125 [0.0390625, 0.08984375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.94140625 | 0.0234375 [-0.001953125, 0.05078125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.953125 | 0.02734375 [0.00390625, 0.052734375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.94921875 | 0.015625 [-0.0078125, 0.0391113281] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.9765625 | 0.0546875 [0.03125, 0.078125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.861328125 | 0.30078125 [0.255810547, 0.34765625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.822265625 | 0.263671875 [0.214794922, 0.3125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.814453125 | 0.212890625 [0.169921875, 0.257861328] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.849609375 | 0.267578125 [0.22265625, 0.314501953] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.87890625 | 0.330078125 [0.283203125, 0.376953125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 1 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([67], []) |
| dose_dose1_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.97265625 | 0.193359375 [0.15625, 0.23046875] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([94], []) |
| dose_dose1_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.90234375 | 0.12890625 [0.0859375, 0.168017578] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([93], []) |
| dose_dose1_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.958984375 | 0.158203125 [0.125, 0.193408203] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([69], []) |
| dose_dose1_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.9765625 | 0.1796875 [0.146484375, 0.216796875] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([80], []) |
| dose_dose1_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.93359375 | 0.5703125 [0.523388672, 0.61328125] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([611], []) |
| dose_dose1_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.90234375 | 0.578125 [0.537109375, 0.623046875] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([411], []) |
| dose_dose1_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.865234375 | 0.62890625 [0.5859375, 0.671875] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([376], []) |
| dose_dose1_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.861328125 | 0.5625 [0.515625, 0.611328125] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([327], []) |
| dose_dose1_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.90234375 | 0.60546875 [0.55859375, 0.650390625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([306], []) |
| dose_dose1_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.9921875 | 0.083984375 [0.060546875, 0.109375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.966796875 | 0.048828125 [0.0234375, 0.076171875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.95703125 | 0.03125 [0.005859375, 0.056640625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.9765625 | 0.0546875 [0.029296875, 0.078125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.970703125 | 0.03515625 [0.015625, 0.056640625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.9375 | 0.376953125 [0.3359375, 0.419921875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.888671875 | 0.326171875 [0.283203125, 0.3671875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.892578125 | 0.263671875 [0.2265625, 0.302734375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.88671875 | 0.26171875 [0.222607422, 0.302734375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.90625 | 0.34765625 [0.302734375, 0.396484375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / linear / category3 / 1 | 0.79296875 / 1 | 0.20703125 [0.173828125, 0.244140625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([126], []) / True ([125], []) |
| dose_dose1_original_seed0 | upper / linear / category3 / 2 | 0.796875 / 0.94921875 | 0.15234375 [0.11328125, 0.189501953] | 0.90625 / 0.82421875 / 1 | True ([164], []) / True ([135], []) |
| dose_dose1_original_seed0 | upper / linear / category3 / 3 | 0.802734375 / 0.890625 | 0.087890625 [0.0468261719, 0.12890625] | 0.9296875 / 0.87109375 / 1 | True ([146], []) / True ([108], []) |
| dose_dose1_original_seed0 | upper / linear / category3 / 4 | 0.833984375 / 0.962890625 | 0.12890625 [0.095703125, 0.166015625] | 0.93359375 / 0.875 / 1 | True ([148], []) / True ([137], []) |
| dose_dose1_original_seed0 | upper / linear / category3 / 5 | 0.8046875 / 0.96484375 | 0.16015625 [0.123046875, 0.197314453] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([126], []) |
| dose_dose1_original_seed0 | upper / linear / sum36 / 1 | 0.380859375 / 0.861328125 | 0.48046875 [0.431591797, 0.529296875] | 0.33984375 / 0.169921875 / 1 | True ([533], []) / True ([618], []) |
| dose_dose1_original_seed0 | upper / linear / sum36 / 2 | 0.33984375 / 0.8359375 | 0.49609375 [0.44921875, 0.548828125] | 0.35546875 / 0.16015625 / 1 | True ([568], []) / True ([635], []) |
| dose_dose1_original_seed0 | upper / linear / sum36 / 3 | 0.275390625 / 0.73828125 | 0.462890625 [0.410107422, 0.507861328] | 0.40625 / 0.216796875 / 1 | True ([544], []) / True ([266], []) |
| dose_dose1_original_seed0 | upper / linear / sum36 / 4 | 0.296875 / 0.7578125 | 0.4609375 [0.410107422, 0.51171875] | 0.375 / 0.19140625 / 0.998046875 | True ([538], []) / True ([350], []) |
| dose_dose1_original_seed0 | upper / linear / sum36 / 5 | 0.30859375 / 0.814453125 | 0.505859375 [0.453076172, 0.5546875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([541], []) / True ([352], []) |
| dose_dose1_original_seed0 | upper / mlp64 / category3 / 1 | 0.91015625 / 0.99609375 | 0.0859375 [0.060546875, 0.111328125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / category3 / 2 | 0.91796875 / 0.97265625 | 0.0546875 [0.02734375, 0.080078125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / category3 / 3 | 0.92578125 / 0.9453125 | 0.01953125 [-0.005859375, 0.044921875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / category3 / 4 | 0.93359375 / 0.9765625 | 0.04296875 [0.01953125, 0.06640625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / category3 / 5 | 0.921875 / 0.966796875 | 0.044921875 [0.025390625, 0.06640625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / sum36 / 1 | 0.560546875 / 0.912109375 | 0.3515625 [0.308544922, 0.400390625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / sum36 / 2 | 0.55859375 / 0.859375 | 0.30078125 [0.25390625, 0.345751953] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / sum36 / 3 | 0.6015625 / 0.828125 | 0.2265625 [0.181591797, 0.271533203] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / sum36 / 4 | 0.58203125 / 0.84765625 | 0.265625 [0.220703125, 0.310546875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed0 | upper / mlp64 / sum36 / 5 | 0.548828125 / 0.873046875 | 0.32421875 [0.277294922, 0.371142578] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed0 | 0 | 1.09447777 | 0 | 0.0236851002 | 0 |
| rarity_uniform_equal_seed0 | 1000 | 1.0863483 | 0 | 4.06273224e-05 | 0 |
| rarity_uniform_equal_seed0 | 2000 | 1.08389795 | 0 | 0.000349846015 | 0 |
| rarity_uniform_equal_seed0 | 5000 | 1.08151126 | 0 | 9.17710046e-06 | 0 |
| rarity_uniform_equal_seed0 | 10000 | 1.07647598 | 0 | 3.87934484e-05 | 0 |
| rarity_uniform_equal_seed0 | 15000 | 1.08152711 | 0 | 3.12007738e-06 | 0 |
| rarity_uniform_equal_seed0 | 20000 | 1.08533144 | 0 | 3.56903549e-05 | 0 |
| rarity_uniform_original_seed0 | 0 | 1.10110247 | 0 | 0.0873579579 | 0 |
| rarity_uniform_original_seed0 | 1000 | 1.03980613 | 0 | 0.00164242641 | 0 |
| rarity_uniform_original_seed0 | 2000 | 1.04436517 | 0 | 0.00111866426 | 0 |
| rarity_uniform_original_seed0 | 5000 | 1.03869855 | 0 | 0.000314945679 | 0 |
| rarity_uniform_original_seed0 | 10000 | 1.03412378 | 0 | 0.000258404587 | 0 |
| rarity_uniform_original_seed0 | 15000 | 1.03774488 | 0 | 0.000207039825 | 0 |
| rarity_uniform_original_seed0 | 20000 | 1.03391683 | 0 | 0.000215068465 | 0 |
| dose_dose100_equal_seed0 | 0 | 1.09447777 | 3.58652425 | 0.0236851002 | 0 |
| dose_dose100_equal_seed0 | 1000 | 1.08645725 | 0.53831923 | 0.000147662532 | 0.205565787 |
| dose_dose100_equal_seed0 | 2000 | 1.08379984 | 0.350342184 | 0.000368057208 | 0.376386331 |
| dose_dose100_equal_seed0 | 5000 | 1.08151698 | 0.194987595 | 2.31240007e-05 | 0.570820544 |
| dose_dose100_equal_seed0 | 10000 | 1.07640612 | 0.129988119 | 3.95739746e-05 | 0.687170043 |
| dose_dose100_equal_seed0 | 15000 | 1.0815109 | 0.105127454 | 8.07129047e-07 | 0.741886638 |
| dose_dose100_equal_seed0 | 20000 | 1.08527672 | 0.0973001048 | 4.13875029e-05 | 0.776058932 |
| dose_dose100_original_seed0 | 0 | 1.10110247 | 3.58725977 | 0.0873579579 | 0 |
| dose_dose100_original_seed0 | 1000 | 1.04271591 | 0.571905375 | 0.00889242377 | 0.195293636 |
| dose_dose100_original_seed0 | 2000 | 1.04364252 | 0.335714608 | 0.00395101733 | 0.381870268 |
| dose_dose100_original_seed0 | 5000 | 1.03894687 | 0.18775478 | 0.00158529589 | 0.594802537 |
| dose_dose100_original_seed0 | 10000 | 1.03687894 | 0.127035245 | 0.00137670557 | 0.717127072 |
| dose_dose100_original_seed0 | 15000 | 1.03912044 | 0.0978009626 | 0.00122378598 | 0.769347248 |
| dose_dose100_original_seed0 | 20000 | 1.03368056 | 0.0765249804 | 0.0010227144 | 0.818989155 |
| dose_dose10_equal_seed0 | 0 | 1.09447777 | 0.3596434 | 0.0236851002 | 0 |
| dose_dose10_equal_seed0 | 1000 | 1.08665276 | 0.0612112097 | 0.00013833345 | 0.12220176 |
| dose_dose10_equal_seed0 | 2000 | 1.08367193 | 0.0505975932 | 0.000430918283 | 0.2737876 |
| dose_dose10_equal_seed0 | 5000 | 1.08160937 | 0.0285861455 | 2.36512906e-05 | 0.465561694 |
| dose_dose10_equal_seed0 | 10000 | 1.07646203 | 0.0183308255 | 4.7544171e-05 | 0.615305914 |
| dose_dose10_equal_seed0 | 15000 | 1.08155525 | 0.00967765693 | 4.98966157e-06 | 0.683977901 |
| dose_dose10_equal_seed0 | 20000 | 1.0853231 | 0.0119688213 | 3.98721604e-05 | 0.72404338 |
| dose_dose10_original_seed0 | 0 | 1.10110247 | 0.338945329 | 0.0873579579 | 0 |
| dose_dose10_original_seed0 | 1000 | 1.04197967 | 0.0732576028 | 0.00458161692 | 0.110947411 |
| dose_dose10_original_seed0 | 2000 | 1.04305565 | 0.0467875451 | 0.00254469979 | 0.263392674 |
| dose_dose10_original_seed0 | 5000 | 1.03963256 | 0.0283791088 | 0.00148378345 | 0.494986699 |
| dose_dose10_original_seed0 | 10000 | 1.03472459 | 0.0186564289 | 0.000859588501 | 0.628442807 |
| dose_dose10_original_seed0 | 15000 | 1.03832543 | 0.0153119145 | 0.000797675737 | 0.689298138 |
| dose_dose10_original_seed0 | 20000 | 1.03549683 | 0.0105438102 | 0.000632161075 | 0.722447309 |
| dose_dose1_equal_seed0 | 0 | 1.09447777 | 0.0420023352 | 0.0236851002 | 0 |
| dose_dose1_equal_seed0 | 1000 | 1.08640766 | 0.00665401481 | 8.65649367e-05 | 0.0282791078 |
| dose_dose1_equal_seed0 | 2000 | 1.08372951 | 0.00531205814 | 0.00045124531 | 0.120237364 |
| dose_dose1_equal_seed0 | 5000 | 1.08192611 | 0.0023347286 | 4.44389598e-05 | 0.265479844 |
| dose_dose1_equal_seed0 | 10000 | 1.07648003 | 0.002527487 | 3.94994822e-05 | 0.398526703 |
| dose_dose1_equal_seed0 | 15000 | 1.08153749 | 0.00165393122 | 2.03901904e-06 | 0.458072437 |
| dose_dose1_equal_seed0 | 20000 | 1.0852797 | 0.00144179258 | 3.7348076e-05 | 0.523020258 |
| dose_dose1_original_seed0 | 0 | 1.10110247 | 0.0319826342 | 0.0873579579 | 0 |
| dose_dose1_original_seed0 | 1000 | 1.04002213 | 0.0104279593 | 0.00193347324 | 0.00466543892 |
| dose_dose1_original_seed0 | 2000 | 1.04450071 | 0.011691221 | 0.00137118807 | 0.0488643339 |
| dose_dose1_original_seed0 | 5000 | 1.03875363 | 0.00798678305 | 0.000785757617 | 0.212072846 |
| dose_dose1_original_seed0 | 10000 | 1.03409731 | 0.00198186538 | 0.000466409178 | 0.366891754 |
| dose_dose1_original_seed0 | 15000 | 1.03811204 | 0.00364489201 | 0.000526813821 | 0.448455085 |
| dose_dose1_original_seed0 | 20000 | 1.03419983 | 0.00211291597 | 0.000369042989 | 0.511356661 |

### Seed 1 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

The uniform rarity rows are the shared 0% dose controls, not additional runs.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| rarity_uniform_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 172/24435, 129/24435, 1764/24435, 4245/24435, 20/24435 | 0/24435 | not applicable |
| rarity_uniform_original_seed1 | B_INCOMPLETE | 5/24435; 10/24435; 7/24435; 12/24435 | 49/24435; 54/24435; 64/24435; 47/24435 | 1 / 2 of 101 | 50/24435, 60/24435, 657/24435, 286/24435, 458/24435 | 0/24435 | not applicable |
| dose_dose100_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 23991/24435, 23286/24435, 23282/24435, 23580/24435, 22974/24435 | 19562/24435 | not applicable |
| dose_dose100_original_seed1 | B_INCOMPLETE | 200/24435; 194/24435; 206/24435; 200/24435 | 8931/24435; 8850/24435; 8882/24435; 8912/24435 | 1 / 67 of 101 | 24002/24435, 23432/24435, 23776/24435, 23782/24435, 23350/24435 | 20695/24435 | not applicable |
| dose_dose10_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 23359/24435, 23195/24435, 22673/24435, 22885/24435, 22757/24435 | 17392/24435 | not applicable |
| dose_dose10_original_seed1 | B_INCOMPLETE | 214/24435; 216/24435; 218/24435; 240/24435 | 890/24435; 880/24435; 860/24435; 873/24435 | 2 / 15 of 101 | 23445/24435, 23087/24435, 22535/24435, 23025/24435, 23209/24435 | 17780/24435 | not applicable |
| dose_dose1_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 22528/24435, 22053/24435, 21367/24435, 22220/24435, 21874/24435 | 13052/24435 | not applicable |
| dose_dose1_original_seed1 | B_INCOMPLETE | 82/24435; 87/24435; 81/24435; 88/24435 | 348/24435; 356/24435; 341/24435; 370/24435 | 1 / 6 of 101 | 22779/24435, 21427/24435, 20928/24435, 21710/24435, 21328/24435 | 11609/24435 | not applicable |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed1 | 39580462 | 0 / 0 | {'12': 189645, '13': 1492783, '23': 130938, '24': 3436635} | {'10': 189951, '16': 1494372, '20': 131278, '27': 3438743} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| rarity_uniform_original_seed1 | 39586743 | 0 / 0 | {'12': 206428, '13': 1494046, '23': 131206, '24': 3149758} | {'10': 204701, '16': 1492564, '20': 130744, '27': 3151364} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| dose_dose100_equal_seed1 | 39580462 | 39580462 / 1 | {'12': 189645, '13': 1492783, '23': 130938, '24': 3436635} | {'10': 189951, '16': 1494372, '20': 131278, '27': 3438743} | not applicable |
| dose_dose100_original_seed1 | 39586743 | 39586743 / 1 | {'12': 206428, '13': 1494046, '23': 131206, '24': 3149758} | {'10': 204701, '16': 1492564, '20': 130744, '27': 3151364} | not applicable |
| dose_dose10_equal_seed1 | 39580462 | 3959470 / 0.100035972 | {'12': 189645, '13': 1492783, '23': 130938, '24': 3436635} | {'10': 189951, '16': 1494372, '20': 131278, '27': 3438743} | not applicable |
| dose_dose10_original_seed1 | 39586743 | 3960405 / 0.100043719 | {'12': 206428, '13': 1494046, '23': 131206, '24': 3149758} | {'10': 204701, '16': 1492564, '20': 130744, '27': 3151364} | not applicable |
| dose_dose1_equal_seed1 | 39580462 | 396546 / 0.010018731 | {'12': 189645, '13': 1492783, '23': 130938, '24': 3436635} | {'10': 189951, '16': 1494372, '20': 131278, '27': 3438743} | not applicable |
| dose_dose1_original_seed1 | 39586743 | 394380 / 0.00996242606 | {'12': 206428, '13': 1494046, '23': 131206, '24': 3149758} | {'10': 204701, '16': 1492564, '20': 130744, '27': 3151364} | not applicable |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rarity_uniform_equal_seed1 | 0.00482098013/0.00489571691 (n=32) | 0.00479944749/0.00486731529 (n=32) | 0.00491968263/0.00505003333 (n=64) | 0.00502422568/0.00519685447 (n=64) | 0.00512485066/0.00527951121 (n=64) | 0.00519888685/0.00537875295 (n=64) | 0.00528851757/0.00544086099 (n=64) | 0.00535332924/0.00563085079 (n=64) | 0.00542388042/0.0056540668 (n=64) | 0.00552316569/0.00574155152 (n=64) | 0.00491804071 / 0.00519685447 / True | 0.00531877174 / 0.00574155152 / True |
| rarity_uniform_original_seed1 | 0.00558635732/0.00613420457 (n=32) | 0.00484022009/0.00547485054 (n=32) | 0.00567690434/0.00781795382 (n=64) | 0.00556325691/0.0110847205 (n=64) | 0.00626961479/0.0533820391 (n=64) | 0.0051453074/0.0142772496 (n=64) | 0.00920776278/0.25216084 (n=64) | 0.00497917144/0.01282911 (n=64) | 0.00514214789/0.0139665753 (n=64) | 0.00489244959/0.0247732699 (n=64) | 0.00548448332 / 0.0110847205 / True | 0.00593940898 / 0.25216084 / False |
| dose_dose100_equal_seed1 | 0.00493160775/0.00554125011 (n=32) | 0.00491818879/0.00498892367 (n=32) | 0.00494282017/0.00529846549 (n=64) | 0.00495993206/0.00537379086 (n=64) | 0.00498008216/0.00553607941 (n=64) | 0.00501650246/0.0055462271 (n=64) | 0.00504720747/0.00545164943 (n=64) | 0.00506900973/0.00557763875 (n=64) | 0.00505180773/0.00550997257 (n=64) | 0.00508999499/0.00559130311 (n=64) | 0.00494255017 / 0.00554125011 / True | 0.00504243409 / 0.00559130311 / True |
| dose_dose100_original_seed1 | 0.00419042632/0.00873797387 (n=32) | 0.0132016595/0.0229870826 (n=32) | 0.00892594142/0.0432229936 (n=64) | 0.0112592537/0.0470235944 (n=64) | 0.0157958498/0.111456484 (n=64) | 0.01239141/0.0506912321 (n=64) | 0.0204859579/0.238473415 (n=64) | 0.020980748/0.248824149 (n=64) | 0.0173349992/0.105283409 (n=64) | 0.0263512012/0.220934063 (n=64) | 0.00962707936 / 0.0470235944 / False | 0.0188900277 / 0.248824149 / False |
| dose_dose10_equal_seed1 | 0.00491122203/0.005521819 (n=32) | 0.00494563719/0.00520148873 (n=32) | 0.00496706716/0.00541096926 (n=64) | 0.00497035123/0.00548163056 (n=64) | 0.00496209273/0.00541204214 (n=64) | 0.00502456934/0.00582645833 (n=64) | 0.00506525068/0.00592984259 (n=64) | 0.00509952777/0.00569631159 (n=64) | 0.00513812853/0.00582301617 (n=64) | 0.00512220291/0.00567483902 (n=64) | 0.00495528267 / 0.005521819 / True | 0.00506862866 / 0.00592984259 / True |
| dose_dose10_original_seed1 | 0.0070589555/0.0129037574 (n=32) | 0.0110955974/0.0331380069 (n=32) | 0.0105903192/0.0514267683 (n=64) | 0.0138726031/0.215891927 (n=64) | 0.0245071312/0.237846732 (n=64) | 0.0179993175/0.257359207 (n=64) | 0.0328295666/0.261540256 (n=64) | 0.029060537/0.260149315 (n=64) | 0.033303174/0.258814268 (n=64) | 0.0427678052/0.261983186 (n=64) | 0.0111800662 / 0.215891927 / False | 0.0300779219 / 0.261983186 / False |
| dose_dose1_equal_seed1 | 0.00471365871/0.00538170338 (n=32) | 0.0049643144/0.00580585003 (n=32) | 0.00488722045/0.00578732789 (n=64) | 0.00483526196/0.00558662415 (n=64) | 0.00498306844/0.00652179122 (n=64) | 0.0049232177/0.00603558123 (n=64) | 0.00507018389/0.00639851391 (n=64) | 0.00509468233/0.00581386685 (n=64) | 0.00513964286/0.00624600053 (n=64) | 0.00514193717/0.00641649961 (n=64) | 0.00485382299 / 0.00580585003 / True | 0.00505878873 / 0.00652179122 / True |
| dose_dose1_original_seed1 | 0.00692385389/0.00864633173 (n=32) | 0.00899836374/0.0769859701 (n=32) | 0.00675036164/0.0104228854 (n=64) | 0.00727534015/0.0758370012 (n=64) | 0.0143088693/0.258114323 (n=64) | 0.0123450755/0.0998782814 (n=64) | 0.0212087332/0.256128855 (n=64) | 0.0253678981/0.25686162 (n=64) | 0.0247654995/0.246385306 (n=64) | 0.0494053047/0.256306246 (n=64) | 0.00732893687 / 0.0769859701 / False | 0.0245668967 / 0.258114323 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed1 | 0.000106416154 / 0.000109995794 (n=20222) | not recorded / 8.24881718e-05 | none | 0.000114187598 / True | 0 / True |
| rarity_uniform_original_seed1 | 0.000167032181 / 0.000178754335 (n=24118) | 0.997861334 / 0.255261242 | law_TV, swaps | 0.0134377033 / True | 0 / True |
| dose_dose100_equal_seed1 | 0.000102221704 / 0.000103846858 (n=20222) | not recorded / 0.00012441026 | none | 0.0003464818 / True | 0 / True |
| dose_dose100_original_seed1 | 0.00093252741 / 0.000890607512 (n=24118) | 0.992685184 / 0.261532336 | law_TV, rerender, swaps | 0.0343753099 / False | 0 / True |
| dose_dose10_equal_seed1 | 0.000101301588 / 0.000101372595 (n=20222) | not recorded / 0.000246306416 | none | 0.000179320574 / True | 0 / True |
| dose_dose10_original_seed1 | 0.000831885304 / 0.000780290957 (n=24118) | 0.990077299 / 0.261308819 | law_TV, rerender, swaps | 0.0554573163 / False | 0 / True |
| dose_dose1_equal_seed1 | 0.000102751289 / 0.000100432403 (n=20222) | not recorded / 0.000356471166 | none | 0.000673010945 / True | 0 / True |
| dose_dose1_original_seed1 | 0.000475603946 / 0.000478797581 (n=24118) | 0.996779188 / 0.260490119 | law_TV, rerender, swaps | 0.134882957 / False | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| rarity_uniform_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_equal_seed1 | A_swap_exact_row | 64 | 0.0048162553 / 0.00499030948 |
| rarity_uniform_equal_seed1 | both_swap_exact_row | 64 | 0.0048162553 / 0.00499030948 |
| rarity_uniform_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_equal_seed1 | neutral_N | 192 | 0.00495139052 / 0.0052318871 |
| rarity_uniform_equal_seed1 | neutral_raw_swap_stability | 128 | 6.29846472e-05 / 0.000159934163 |
| rarity_uniform_equal_seed1 | raw_swap_effect | 64 | 6.38510101e-05 / 0.000208899379 |
| rarity_uniform_equal_seed1 | raw_swap_exact_row | 64 | 0.0048162553 / 0.00499030948 |
| rarity_uniform_equal_seed1 | raw_swap_stability | 128 | 0.00244005315 / 0.00499030948 |
| rarity_uniform_equal_seed1 | reset_L | 160 | 0.00494260173 / 0.00537262857 |
| rarity_uniform_equal_seed1 | same_category_substitution | 128 | 6.29846472e-05 / 0.000159934163 |
| rarity_uniform_equal_seed1 | set_H | 160 | 0.00492679868 / 0.005215168 |
| rarity_uniform_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00491883536 / 0.00511404872 |
| rarity_uniform_original_seed1 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_original_seed1 | A_swap_exact_row | 64 | 0.254448437 / 0.25613457 |
| rarity_uniform_original_seed1 | both_swap_exact_row | 64 | 0.00519835844 / 0.00650531054 |
| rarity_uniform_original_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_original_seed1 | neutral_N | 192 | 0.00644388186 / 0.0613576323 |
| rarity_uniform_original_seed1 | neutral_raw_swap_stability | 128 | 0.00223508442 / 0.054870218 |
| rarity_uniform_original_seed1 | raw_swap_effect | 64 | 0.255657386 / 0.257126391 |
| rarity_uniform_original_seed1 | raw_swap_exact_row | 64 | 0.00519835844 / 0.00650531054 |
| rarity_uniform_original_seed1 | raw_swap_stability | 128 | 0.255052911 / 0.257126391 |
| rarity_uniform_original_seed1 | reset_L | 160 | 0.00629907753 / 0.0271157622 |
| rarity_uniform_original_seed1 | same_category_substitution | 128 | 0.00223508442 / 0.054870218 |
| rarity_uniform_original_seed1 | set_H | 160 | 0.00555046895 / 0.0315754414 |
| rarity_uniform_original_seed1 | upper_state_exchange_same_N | 64 | 0.00609618751 / 0.0166018456 |
| dose_dose100_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| dose_dose100_equal_seed1 | A_swap_exact_row | 64 | 0.00493946718 / 0.00563067198 |
| dose_dose100_equal_seed1 | both_swap_exact_row | 64 | 0.00493946718 / 0.00563067198 |
| dose_dose100_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose100_equal_seed1 | neutral_N | 192 | 0.00496509299 / 0.00564391911 |
| dose_dose100_equal_seed1 | neutral_raw_swap_stability | 128 | 4.78577567e-05 / 0.000165328383 |
| dose_dose100_equal_seed1 | raw_swap_effect | 64 | 0.000155334361 / 0.000725954771 |
| dose_dose100_equal_seed1 | raw_swap_exact_row | 64 | 0.00493946718 / 0.00563067198 |
| dose_dose100_equal_seed1 | raw_swap_stability | 128 | 0.00254740077 / 0.00563067198 |
| dose_dose100_equal_seed1 | reset_L | 160 | 0.00498630004 / 0.0063572824 |
| dose_dose100_equal_seed1 | same_category_substitution | 128 | 4.78577567e-05 / 0.000165328383 |
| dose_dose100_equal_seed1 | set_H | 160 | 0.00498951338 / 0.0056656152 |
| dose_dose100_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00495869853 / 0.0056373179 |
| dose_dose100_original_seed1 | A_swap_effect | 64 | 0 / 0 |
| dose_dose100_original_seed1 | A_swap_exact_row | 64 | 0.254164424 / 0.27180887 |
| dose_dose100_original_seed1 | both_swap_exact_row | 64 | 0.0108267299 / 0.0627179295 |
| dose_dose100_original_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose100_original_seed1 | neutral_N | 192 | 0.0117050527 / 0.0465593785 |
| dose_dose100_original_seed1 | neutral_raw_swap_stability | 128 | 0.0102779468 / 0.0754275322 |
| dose_dose100_original_seed1 | raw_swap_effect | 64 | 0.256832967 / 0.279650569 |
| dose_dose100_original_seed1 | raw_swap_exact_row | 64 | 0.0108267299 / 0.0627179295 |
| dose_dose100_original_seed1 | raw_swap_stability | 128 | 0.255498695 / 0.279650569 |
| dose_dose100_original_seed1 | reset_L | 160 | 0.0145010002 / 0.252945706 |
| dose_dose100_original_seed1 | same_category_substitution | 128 | 0.0102779468 / 0.0754275322 |
| dose_dose100_original_seed1 | set_H | 160 | 0.0132989398 / 0.0802678466 |
| dose_dose100_original_seed1 | upper_state_exchange_same_N | 64 | 0.0111769546 / 0.0354219079 |
| dose_dose10_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| dose_dose10_equal_seed1 | A_swap_exact_row | 64 | 0.0049436891 / 0.00539763272 |
| dose_dose10_equal_seed1 | both_swap_exact_row | 64 | 0.0049436891 / 0.00539763272 |
| dose_dose10_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose10_equal_seed1 | neutral_N | 192 | 0.00499332673 / 0.00549891591 |
| dose_dose10_equal_seed1 | neutral_raw_swap_stability | 128 | 0.000112063019 / 0.000413566828 |
| dose_dose10_equal_seed1 | raw_swap_effect | 64 | 0.000201648567 / 0.000499919057 |
| dose_dose10_equal_seed1 | raw_swap_exact_row | 64 | 0.0049436891 / 0.00539763272 |
| dose_dose10_equal_seed1 | raw_swap_stability | 128 | 0.00257266883 / 0.00539763272 |
| dose_dose10_equal_seed1 | reset_L | 160 | 0.00498201083 / 0.00592823327 |
| dose_dose10_equal_seed1 | same_category_substitution | 128 | 0.000112063019 / 0.000413566828 |
| dose_dose10_equal_seed1 | set_H | 160 | 0.00501060449 / 0.00543600321 |
| dose_dose10_equal_seed1 | upper_state_exchange_same_N | 64 | 0.0049809888 / 0.00542987883 |
| dose_dose10_original_seed1 | A_swap_effect | 64 | 0 / 0 |
| dose_dose10_original_seed1 | A_swap_exact_row | 64 | 0.253095743 / 0.262329087 |
| dose_dose10_original_seed1 | both_swap_exact_row | 64 | 0.0105204827 / 0.081709221 |
| dose_dose10_original_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose10_original_seed1 | neutral_N | 192 | 0.0132433255 / 0.208845124 |
| dose_dose10_original_seed1 | neutral_raw_swap_stability | 128 | 0.01082908 / 0.188848823 |
| dose_dose10_original_seed1 | raw_swap_effect | 64 | 0.253939272 / 0.267244533 |
| dose_dose10_original_seed1 | raw_swap_exact_row | 64 | 0.0105204827 / 0.081709221 |
| dose_dose10_original_seed1 | raw_swap_stability | 128 | 0.253517507 / 0.267244533 |
| dose_dose10_original_seed1 | reset_L | 160 | 0.0158052234 / 0.255605459 |
| dose_dose10_original_seed1 | same_category_substitution | 128 | 0.01082908 / 0.188848823 |
| dose_dose10_original_seed1 | set_H | 160 | 0.012155903 / 0.0951114446 |
| dose_dose10_original_seed1 | upper_state_exchange_same_N | 64 | 0.011557329 / 0.0931234807 |
| dose_dose1_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| dose_dose1_equal_seed1 | A_swap_exact_row | 64 | 0.00478415983 / 0.00580891967 |
| dose_dose1_equal_seed1 | both_swap_exact_row | 64 | 0.00478415983 / 0.00580891967 |
| dose_dose1_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose1_equal_seed1 | neutral_N | 192 | 0.00485285038 / 0.00598300993 |
| dose_dose1_equal_seed1 | neutral_raw_swap_stability | 128 | 8.80205771e-05 / 0.000343769789 |
| dose_dose1_equal_seed1 | raw_swap_effect | 64 | 0.000375878997 / 0.00109151006 |
| dose_dose1_equal_seed1 | raw_swap_exact_row | 64 | 0.00478415983 / 0.00580891967 |
| dose_dose1_equal_seed1 | raw_swap_stability | 128 | 0.00258001941 / 0.00580891967 |
| dose_dose1_equal_seed1 | reset_L | 160 | 0.00469091292 / 0.00587402284 |
| dose_dose1_equal_seed1 | same_category_substitution | 128 | 8.80205771e-05 / 0.000343769789 |
| dose_dose1_equal_seed1 | set_H | 160 | 0.00499303788 / 0.00694724917 |
| dose_dose1_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00483582309 / 0.00589610636 |
| dose_dose1_original_seed1 | A_swap_effect | 64 | 0 / 0 |
| dose_dose1_original_seed1 | A_swap_exact_row | 64 | 0.254914266 / 0.259086035 |
| dose_dose1_original_seed1 | both_swap_exact_row | 64 | 0.00733698288 / 0.0199349225 |
| dose_dose1_original_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose1_original_seed1 | neutral_N | 192 | 0.00812624989 / 0.107394442 |
| dose_dose1_original_seed1 | neutral_raw_swap_stability | 128 | 0.00498542766 / 0.0876284987 |
| dose_dose1_original_seed1 | raw_swap_effect | 64 | 0.256317155 / 0.260555342 |
| dose_dose1_original_seed1 | raw_swap_exact_row | 64 | 0.00733698288 / 0.0199349225 |
| dose_dose1_original_seed1 | raw_swap_stability | 128 | 0.255615711 / 0.260555342 |
| dose_dose1_original_seed1 | reset_L | 160 | 0.00882560471 / 0.0747510642 |
| dose_dose1_original_seed1 | same_category_substitution | 128 | 0.00498542766 / 0.0876284987 |
| dose_dose1_original_seed1 | set_H | 160 | 0.0073806223 / 0.0344181806 |
| dose_dose1_original_seed1 | upper_state_exchange_same_N | 64 | 0.00734497677 / 0.0293737203 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.83203125 | 0.029296875 [-0.0078125, 0.064453125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([103], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.861328125 | 0.12890625 [0.0859375, 0.173828125] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([100], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.91796875 | 0.16796875 [0.130859375, 0.208984375] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([113], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.884765625 | 0.119140625 [0.076171875, 0.166015625] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([95], []) |
| rarity_uniform_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.83203125 | 0.06640625 [0.0331542969, 0.1015625] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([93], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.546875 | 0.23828125 [0.185546875, 0.294921875] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([351], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.458984375 | 0.1953125 [0.14453125, 0.24609375] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([345], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.658203125 | 0.357421875 [0.310498047, 0.408203125] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([533], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.576171875 | 0.31640625 [0.26171875, 0.369189453] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([338], []) |
| rarity_uniform_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.447265625 | 0.080078125 [0.01953125, 0.13671875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([406], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.923828125 | 0.015625 [-0.00786132812, 0.04296875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.953125 | 0.041015625 [0.021484375, 0.060546875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.9609375 | 0.052734375 [0.02734375, 0.076171875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.958984375 | 0.01953125 [0, 0.0390625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.9453125 | 0.01953125 [-0.00390625, 0.04296875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.75 | 0.142578125 [0.0976074219, 0.19140625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.751953125 | 0.150390625 [0.103515625, 0.201171875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.794921875 | 0.220703125 [0.17578125, 0.261767578] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.771484375 | 0.203125 [0.150390625, 0.25390625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.72265625 | 0.025390625 [-0.0254394531, 0.0703613281] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.828125 | 0.017578125 [-0.01953125, 0.05078125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([129], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.87890625 | 0.11328125 [0.07421875, 0.15234375] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([123], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.8984375 | 0.146484375 [0.109375, 0.185546875] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([138], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.861328125 | 0.115234375 [0.0703125, 0.1640625] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([118], []) |
| rarity_uniform_equal_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.8359375 | 0.044921875 [0.009765625, 0.0781738281] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([159], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.46484375 | 0.119140625 [0.0663574219, 0.171875] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([497], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.3671875 | 0.06640625 [0.01171875, 0.119189453] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([624], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.568359375 | 0.244140625 [0.19140625, 0.296875] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([780], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.4375 | 0.15234375 [0.0976074219, 0.208984375] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([448], []) |
| rarity_uniform_equal_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.353515625 | -0.048828125 [-0.103515625, 0.00390625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([583], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.923828125 | 0 [-0.02734375, 0.0234375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.91796875 | 0.015625 [-0.009765625, 0.041015625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.951171875 | 0.03125 [0.009765625, 0.052734375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.94921875 | 0.017578125 [0, 0.037109375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.93359375 | 0.009765625 [-0.01171875, 0.03125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.607421875 | 0.005859375 [-0.046875, 0.0566894531] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.55078125 | 0.00390625 [-0.0508300781, 0.056640625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.63671875 | 0.07421875 [0.0233886719, 0.12109375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.58203125 | 0.001953125 [-0.041015625, 0.05078125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.59375 | -0.09375 [-0.142578125, -0.046875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 1 | 0.197265625 [0.162109375, 0.232421875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([38], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.45703125 | -0.275390625 [-0.330078125, -0.21875] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([90], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.640625 | -0.109375 [-0.158203125, -0.05859375] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([91], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.671875 | -0.09375 [-0.14453125, -0.0448730469] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([84], []) |
| rarity_uniform_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.7109375 | -0.0546875 [-0.0996582031, -0.0116699219] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([99], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.982421875 | 0.673828125 [0.634765625, 0.714892578] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([507], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.0546875 | -0.208984375 [-0.25390625, -0.166015625] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([193], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.064453125 | -0.236328125 [-0.28125, -0.195263672] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([215], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.087890625 | -0.171875 [-0.2109375, -0.126953125] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([209], []) |
| rarity_uniform_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.09375 | -0.2734375 [-0.322265625, -0.226513672] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([203], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.068359375, 0.1171875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.90625 | -0.005859375 [-0.025390625, 0.01171875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.923828125 | 0.015625 [-0.00390625, 0.03515625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.939453125 | 0 [-0.013671875, 0.013671875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.93359375 | 0.0078125 [-0.01171875, 0.02734375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.994140625 | 0.38671875 [0.34765625, 0.427734375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.396484375 | -0.205078125 [-0.251953125, -0.158203125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.388671875 | -0.185546875 [-0.234375, -0.134716797] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.38671875 | -0.181640625 [-0.23046875, -0.130859375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.4609375 | -0.236328125 [-0.283203125, -0.187451172] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 1 | 0.810546875 / 1 | 0.189453125 [0.154248047, 0.224609375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([32], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.552734375 | -0.212890625 [-0.263671875, -0.1640625] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([113], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.6796875 | -0.072265625 [-0.121142578, -0.0234375] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([145], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.732421875 | -0.013671875 [-0.05859375, 0.037109375] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([154], []) |
| rarity_uniform_original_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.6328125 | -0.158203125 [-0.20703125, -0.111328125] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([157], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.982421875 | 0.63671875 [0.597607422, 0.677734375] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([453], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.04296875 | -0.2578125 [-0.30078125, -0.21484375] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([237], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.0546875 | -0.26953125 [-0.3125, -0.2265625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([299], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.09375 | -0.19140625 [-0.23828125, -0.14453125] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([365], []) |
| rarity_uniform_original_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.0625 | -0.33984375 [-0.38671875, -0.291015625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([224], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.998046875 | 0.07421875 [0.0526855469, 0.095703125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.896484375 | -0.005859375 [-0.03125, 0.01953125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.923828125 | 0.00390625 [-0.015625, 0.0234375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.9375 | 0.005859375 [-0.009765625, 0.0234375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.92578125 | 0.001953125 [-0.01953125, 0.0234375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.986328125 | 0.384765625 [0.345703125, 0.423876953] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.349609375 | -0.197265625 [-0.244140625, -0.154296875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.3984375 | -0.1640625 [-0.2109375, -0.119140625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.400390625 | -0.1796875 [-0.22265625, -0.136669922] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.41796875 | -0.26953125 [-0.31640625, -0.220703125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.98046875 | 0.177734375 [0.142578125, 0.212890625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([56], []) |
| dose_dose100_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.98046875 | 0.248046875 [0.212890625, 0.2890625] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([78], []) |
| dose_dose100_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.978515625 | 0.228515625 [0.193359375, 0.267578125] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([78], []) |
| dose_dose100_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.966796875 | 0.201171875 [0.162109375, 0.23828125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([70], []) |
| dose_dose100_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.91796875 | 0.15234375 [0.107421875, 0.193408203] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([50], []) |
| dose_dose100_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.962890625 | 0.654296875 [0.61328125, 0.69921875] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([158], []) |
| dose_dose100_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.912109375 | 0.6484375 [0.6015625, 0.689453125] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([268], []) |
| dose_dose100_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.912109375 | 0.611328125 [0.56640625, 0.654296875] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([287], []) |
| dose_dose100_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.91796875 | 0.658203125 [0.619091797, 0.701171875] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([298], []) |
| dose_dose100_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.91796875 | 0.55078125 [0.501904297, 0.59765625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([311], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.990234375 | 0.08203125 [0.060546875, 0.109375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.99609375 | 0.083984375 [0.05859375, 0.107470703] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.98046875 | 0.072265625 [0.046875, 0.095703125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.974609375 | 0.03515625 [0.01171875, 0.056640625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.97265625 | 0.046875 [0.025390625, 0.0703125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.974609375 | 0.3671875 [0.32421875, 0.41015625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.896484375 | 0.294921875 [0.251953125, 0.337890625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.923828125 | 0.349609375 [0.306591797, 0.390625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.939453125 | 0.37109375 [0.326171875, 0.41796875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.8984375 | 0.201171875 [0.16015625, 0.2421875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.88671875 | 0.076171875 [0.041015625, 0.109423828] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([82], []) |
| dose_dose100_equal_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.935546875 | 0.169921875 [0.130810547, 0.2109375] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([100], []) |
| dose_dose100_equal_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.9296875 | 0.177734375 [0.13671875, 0.21875] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([119], []) |
| dose_dose100_equal_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.955078125 | 0.208984375 [0.169873047, 0.25] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([141], []) |
| dose_dose100_equal_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.896484375 | 0.10546875 [0.0625, 0.148486328] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([156], []) |
| dose_dose100_equal_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.818359375 | 0.47265625 [0.42578125, 0.52734375] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([161], []) |
| dose_dose100_equal_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.802734375 | 0.501953125 [0.451171875, 0.548876953] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([256], []) |
| dose_dose100_equal_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.751953125 | 0.427734375 [0.375, 0.482421875] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([514], []) |
| dose_dose100_equal_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.810546875 | 0.525390625 [0.474609375, 0.576220703] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([436], []) |
| dose_dose100_equal_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.794921875 | 0.392578125 [0.33984375, 0.445361328] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([701], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.98046875 | 0.056640625 [0.03125, 0.080078125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.9765625 | 0.07421875 [0.048828125, 0.099609375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.97265625 | 0.052734375 [0.03125, 0.076171875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.970703125 | 0.0390625 [0.0194824219, 0.0625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.96484375 | 0.041015625 [0.013671875, 0.0703613281] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.89453125 | 0.29296875 [0.24609375, 0.341796875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.88671875 | 0.33984375 [0.29296875, 0.384765625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.857421875 | 0.294921875 [0.25, 0.341796875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.8984375 | 0.318359375 [0.275390625, 0.361328125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.86328125 | 0.17578125 [0.1328125, 0.216845703] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.994140625 | 0.19140625 [0.15625, 0.2265625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([50], []) |
| dose_dose100_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.97265625 | 0.240234375 [0.203125, 0.28125] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([73], []) |
| dose_dose100_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.96875 | 0.21875 [0.185498047, 0.2578125] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([62], []) |
| dose_dose100_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.984375 | 0.21875 [0.181640625, 0.255859375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([75], []) |
| dose_dose100_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.9609375 | 0.1953125 [0.154248047, 0.232421875] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([59], []) |
| dose_dose100_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.958984375 | 0.650390625 [0.609375, 0.693359375] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([275], []) |
| dose_dose100_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.91796875 | 0.654296875 [0.60546875, 0.697265625] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([265], []) |
| dose_dose100_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.931640625 | 0.630859375 [0.591796875, 0.671875] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([235], []) |
| dose_dose100_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.9375 | 0.677734375 [0.640576172, 0.71875] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([293], []) |
| dose_dose100_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.939453125 | 0.572265625 [0.521484375, 0.615234375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([247], []) |
| dose_dose100_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.98828125 | 0.080078125 [0.05859375, 0.107421875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.98046875 | 0.068359375 [0.0429199219, 0.091796875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.984375 | 0.076171875 [0.0526855469, 0.103515625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.982421875 | 0.04296875 [0.0214355469, 0.064453125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.966796875 | 0.041015625 [0.015625, 0.06640625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.96875 | 0.361328125 [0.322265625, 0.404345703] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.9140625 | 0.3125 [0.265625, 0.35546875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.943359375 | 0.369140625 [0.32421875, 0.412109375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.96484375 | 0.396484375 [0.3515625, 0.441455078] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.935546875 | 0.23828125 [0.197216797, 0.281298828] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.994140625 | 0.18359375 [0.146484375, 0.21875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([61], []) |
| dose_dose100_original_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.94921875 | 0.18359375 [0.1484375, 0.22265625] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([115], []) |
| dose_dose100_original_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.9453125 | 0.193359375 [0.154296875, 0.23046875] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([109], []) |
| dose_dose100_original_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.97265625 | 0.2265625 [0.189453125, 0.267578125] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([96], []) |
| dose_dose100_original_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.923828125 | 0.1328125 [0.0917480469, 0.173828125] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([88], []) |
| dose_dose100_original_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.947265625 | 0.6015625 [0.55859375, 0.64453125] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([315], []) |
| dose_dose100_original_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.794921875 | 0.494140625 [0.443359375, 0.544970703] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([584], []) |
| dose_dose100_original_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.76171875 | 0.4375 [0.38671875, 0.490234375] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([304], []) |
| dose_dose100_original_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.8125 | 0.52734375 [0.47265625, 0.582080078] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([294], []) |
| dose_dose100_original_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.8125 | 0.41015625 [0.357421875, 0.46484375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([321], []) |
| dose_dose100_original_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.994140625 | 0.0703125 [0.046875, 0.09375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.982421875 | 0.080078125 [0.0546875, 0.103515625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.97265625 | 0.052734375 [0.0292480469, 0.078125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.982421875 | 0.05078125 [0.029296875, 0.076171875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.97265625 | 0.048828125 [0.0234375, 0.076171875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.955078125 | 0.353515625 [0.3125, 0.396484375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.84765625 | 0.30078125 [0.255859375, 0.345703125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.85546875 | 0.29296875 [0.246044922, 0.341796875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.873046875 | 0.29296875 [0.24609375, 0.335986328] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.861328125 | 0.173828125 [0.126953125, 0.21875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.994140625 | 0.19140625 [0.15625, 0.2265625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([63], []) |
| dose_dose10_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.974609375 | 0.2421875 [0.20703125, 0.283203125] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([77], []) |
| dose_dose10_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.96875 | 0.21875 [0.181640625, 0.2578125] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([74], []) |
| dose_dose10_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.984375 | 0.21875 [0.181640625, 0.2578125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([72], []) |
| dose_dose10_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.96875 | 0.203125 [0.1640625, 0.23828125] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([80], []) |
| dose_dose10_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.947265625 | 0.638671875 [0.59765625, 0.68359375] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([276], []) |
| dose_dose10_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.904296875 | 0.640625 [0.593701172, 0.681689453] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([283], []) |
| dose_dose10_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.90625 | 0.60546875 [0.560546875, 0.6484375] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([380], []) |
| dose_dose10_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.904296875 | 0.64453125 [0.60546875, 0.6875] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([371], []) |
| dose_dose10_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.919921875 | 0.552734375 [0.505859375, 0.59765625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([332], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.994140625 | 0.0859375 [0.064453125, 0.111376953] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.974609375 | 0.0625 [0.0390136719, 0.0859375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.96875 | 0.060546875 [0.037109375, 0.0859375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.990234375 | 0.05078125 [0.029296875, 0.0703125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.9765625 | 0.05078125 [0.029296875, 0.0723144531] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.927734375 | 0.3203125 [0.279296875, 0.36328125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.919921875 | 0.318359375 [0.275341797, 0.36328125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.91015625 | 0.3359375 [0.29296875, 0.375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.91796875 | 0.349609375 [0.302734375, 0.396484375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.927734375 | 0.23046875 [0.1875, 0.271484375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.93359375 | 0.123046875 [0.0859375, 0.158251953] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([78], []) |
| dose_dose10_equal_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.947265625 | 0.181640625 [0.142578125, 0.220703125] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([146], []) |
| dose_dose10_equal_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.962890625 | 0.2109375 [0.169921875, 0.25] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([98], []) |
| dose_dose10_equal_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.9609375 | 0.21484375 [0.177734375, 0.255859375] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([131], []) |
| dose_dose10_equal_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.896484375 | 0.10546875 [0.06640625, 0.144580078] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([86], []) |
| dose_dose10_equal_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.81640625 | 0.470703125 [0.419921875, 0.5234375] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([211], []) |
| dose_dose10_equal_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.765625 | 0.46484375 [0.416015625, 0.517578125] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([383], []) |
| dose_dose10_equal_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.76171875 | 0.4375 [0.388671875, 0.490234375] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([595], []) |
| dose_dose10_equal_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.71875 | 0.43359375 [0.380859375, 0.482470703] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([557], []) |
| dose_dose10_equal_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.828125 | 0.42578125 [0.373046875, 0.478515625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([136], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.978515625 | 0.0546875 [0.03125, 0.076171875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.96875 | 0.06640625 [0.0390625, 0.09375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.978515625 | 0.05859375 [0.0351074219, 0.083984375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.982421875 | 0.05078125 [0.029296875, 0.076171875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.97265625 | 0.048828125 [0.0253417969, 0.072265625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.85546875 | 0.25390625 [0.206982422, 0.30078125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.87109375 | 0.32421875 [0.28125, 0.369140625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.8515625 | 0.2890625 [0.2421875, 0.3359375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.83203125 | 0.251953125 [0.205029297, 0.294921875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.8984375 | 0.2109375 [0.169921875, 0.252001953] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.994140625 | 0.19140625 [0.156201172, 0.2265625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([65], []) |
| dose_dose10_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.984375 | 0.251953125 [0.21484375, 0.293017578] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([86], []) |
| dose_dose10_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.97265625 | 0.22265625 [0.1875, 0.263671875] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([99], []) |
| dose_dose10_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.97265625 | 0.20703125 [0.16796875, 0.24609375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([70], []) |
| dose_dose10_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.9765625 | 0.2109375 [0.169921875, 0.24609375] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([70], []) |
| dose_dose10_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.951171875 | 0.642578125 [0.59765625, 0.6875] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([282], []) |
| dose_dose10_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.916015625 | 0.65234375 [0.603466797, 0.693359375] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([289], []) |
| dose_dose10_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.88671875 | 0.5859375 [0.541015625, 0.630859375] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([304], []) |
| dose_dose10_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.927734375 | 0.66796875 [0.628857422, 0.708984375] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([280], []) |
| dose_dose10_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.94140625 | 0.57421875 [0.525390625, 0.615234375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([279], []) |
| dose_dose10_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.994140625 | 0.0859375 [0.064453125, 0.111376953] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.984375 | 0.072265625 [0.048828125, 0.095703125] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.982421875 | 0.07421875 [0.05078125, 0.09765625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.986328125 | 0.046875 [0.02734375, 0.0664550781] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.986328125 | 0.060546875 [0.0390625, 0.0820800781] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.93359375 | 0.326171875 [0.28515625, 0.3671875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.90625 | 0.3046875 [0.259765625, 0.345703125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.88671875 | 0.3125 [0.263671875, 0.35546875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.93359375 | 0.365234375 [0.322265625, 0.410205078] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.94140625 | 0.244140625 [0.203125, 0.283203125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.990234375 | 0.1796875 [0.14453125, 0.212939453] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([72], []) |
| dose_dose10_original_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.951171875 | 0.185546875 [0.146484375, 0.22265625] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([89], []) |
| dose_dose10_original_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.890625 | 0.138671875 [0.09375, 0.181640625] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([107], []) |
| dose_dose10_original_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.92578125 | 0.1796875 [0.142578125, 0.22265625] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([115], []) |
| dose_dose10_original_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.955078125 | 0.1640625 [0.124951172, 0.201171875] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([120], []) |
| dose_dose10_original_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.892578125 | 0.546875 [0.5, 0.59765625] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([847], []) |
| dose_dose10_original_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.767578125 | 0.466796875 [0.414013672, 0.517578125] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([411], []) |
| dose_dose10_original_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.701171875 | 0.376953125 [0.330078125, 0.423828125] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([305], []) |
| dose_dose10_original_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.779296875 | 0.494140625 [0.439453125, 0.544921875] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([281], []) |
| dose_dose10_original_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.818359375 | 0.416015625 [0.369091797, 0.466796875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([275], []) |
| dose_dose10_original_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.990234375 | 0.06640625 [0.04296875, 0.087890625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.97265625 | 0.0703125 [0.044921875, 0.095703125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.962890625 | 0.04296875 [0.017578125, 0.068359375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.962890625 | 0.03125 [0.009765625, 0.0546875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.982421875 | 0.05859375 [0.0351074219, 0.083984375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.892578125 | 0.291015625 [0.251953125, 0.3359375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.826171875 | 0.279296875 [0.23046875, 0.326171875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.796875 | 0.234375 [0.189453125, 0.281298828] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.859375 | 0.279296875 [0.236328125, 0.322265625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.876953125 | 0.189453125 [0.144482422, 0.236328125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.978515625 | 0.17578125 [0.142578125, 0.2109375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([69], []) |
| dose_dose1_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.958984375 | 0.2265625 [0.1875, 0.267626953] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([80], []) |
| dose_dose1_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.8984375 | 0.1484375 [0.111328125, 0.19140625] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([80], []) |
| dose_dose1_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.92578125 | 0.16015625 [0.119140625, 0.19921875] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([66], []) |
| dose_dose1_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.892578125 | 0.126953125 [0.0859375, 0.171875] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([60], []) |
| dose_dose1_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.92578125 | 0.6171875 [0.57421875, 0.662109375] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([311], []) |
| dose_dose1_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.8984375 | 0.634765625 [0.5859375, 0.677734375] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([308], []) |
| dose_dose1_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.85546875 | 0.5546875 [0.5078125, 0.599609375] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([295], []) |
| dose_dose1_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.8984375 | 0.638671875 [0.599560547, 0.681640625] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([327], []) |
| dose_dose1_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.880859375 | 0.513671875 [0.4609375, 0.560546875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([334], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.978515625 | 0.0703125 [0.044921875, 0.09765625] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.9609375 | 0.048828125 [0.021484375, 0.0742675781] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.947265625 | 0.0390625 [0.015625, 0.0625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.97265625 | 0.033203125 [0.01171875, 0.0546875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.953125 | 0.02734375 [0.001953125, 0.05078125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.919921875 | 0.3125 [0.26953125, 0.355517578] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.880859375 | 0.279296875 [0.232421875, 0.322314453] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.85546875 | 0.28125 [0.240185547, 0.32421875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.904296875 | 0.3359375 [0.29296875, 0.3828125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.912109375 | 0.21484375 [0.173828125, 0.2578125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.896484375 | 0.0859375 [0.046875, 0.123046875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([69], []) |
| dose_dose1_equal_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.923828125 | 0.158203125 [0.1171875, 0.199267578] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([149], []) |
| dose_dose1_equal_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.84765625 | 0.095703125 [0.05078125, 0.138671875] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([107], []) |
| dose_dose1_equal_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.89453125 | 0.1484375 [0.109375, 0.19140625] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([122], []) |
| dose_dose1_equal_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.87109375 | 0.080078125 [0.0390625, 0.12109375] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([91], []) |
| dose_dose1_equal_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.802734375 | 0.45703125 [0.404296875, 0.51171875] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([218], []) |
| dose_dose1_equal_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.779296875 | 0.478515625 [0.427734375, 0.529296875] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([373], []) |
| dose_dose1_equal_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.6953125 | 0.37109375 [0.3203125, 0.423828125] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([175], []) |
| dose_dose1_equal_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.703125 | 0.41796875 [0.3671875, 0.46875] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([251], []) |
| dose_dose1_equal_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.7109375 | 0.30859375 [0.248046875, 0.37109375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([304], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.970703125 | 0.046875 [0.0234375, 0.0703125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.966796875 | 0.064453125 [0.03515625, 0.09375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.935546875 | 0.015625 [-0.01171875, 0.041015625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.96484375 | 0.033203125 [0.013671875, 0.056640625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.94140625 | 0.017578125 [-0.0078125, 0.044921875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.837890625 | 0.236328125 [0.191357422, 0.283203125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.8359375 | 0.2890625 [0.244140625, 0.33203125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.779296875 | 0.216796875 [0.171826172, 0.263671875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.841796875 | 0.26171875 [0.21484375, 0.30859375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.8125 | 0.125 [0.078125, 0.171923828] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.994140625 | 0.19140625 [0.15625, 0.226611328] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([49], []) |
| dose_dose1_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.904296875 | 0.171875 [0.130859375, 0.218798828] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([87], []) |
| dose_dose1_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.890625 | 0.140625 [0.1015625, 0.18359375] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([85], []) |
| dose_dose1_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.919921875 | 0.154296875 [0.115234375, 0.1953125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([70], []) |
| dose_dose1_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.9609375 | 0.1953125 [0.15625, 0.232421875] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([69], []) |
| dose_dose1_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.953125 | 0.64453125 [0.6015625, 0.689501953] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([355], []) |
| dose_dose1_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.857421875 | 0.59375 [0.546875, 0.638671875] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([274], []) |
| dose_dose1_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.8359375 | 0.53515625 [0.488232422, 0.58203125] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([277], []) |
| dose_dose1_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.88671875 | 0.626953125 [0.58203125, 0.669970703] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([341], []) |
| dose_dose1_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.8828125 | 0.515625 [0.46484375, 0.5625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([288], []) |
| dose_dose1_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.9921875 | 0.083984375 [0.0624511719, 0.109423828] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.955078125 | 0.04296875 [0.0194824219, 0.06640625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.94921875 | 0.041015625 [0.017578125, 0.0625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.953125 | 0.013671875 [-0.005859375, 0.03515625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.970703125 | 0.044921875 [0.021484375, 0.0703125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.953125 | 0.345703125 [0.3046875, 0.388671875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.880859375 | 0.279296875 [0.236328125, 0.32421875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.87109375 | 0.296875 [0.25390625, 0.337890625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.884765625 | 0.31640625 [0.271484375, 0.361328125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.888671875 | 0.19140625 [0.148388672, 0.23046875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / linear / category3 / 1 | 0.810546875 / 0.98828125 | 0.177734375 [0.140625, 0.212890625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([143], []) / True ([51], []) |
| dose_dose1_original_seed1 | upper / linear / category3 / 2 | 0.765625 / 0.90234375 | 0.13671875 [0.09765625, 0.177734375] | 0.90625 / 0.82421875 / 1 | True ([145], []) / True ([131], []) |
| dose_dose1_original_seed1 | upper / linear / category3 / 3 | 0.751953125 / 0.88671875 | 0.134765625 [0.09765625, 0.175830078] | 0.9296875 / 0.87109375 / 1 | True ([150], []) / True ([126], []) |
| dose_dose1_original_seed1 | upper / linear / category3 / 4 | 0.74609375 / 0.923828125 | 0.177734375 [0.138623047, 0.22265625] | 0.93359375 / 0.875 / 1 | True ([142], []) / True ([153], []) |
| dose_dose1_original_seed1 | upper / linear / category3 / 5 | 0.791015625 / 0.95703125 | 0.166015625 [0.12890625, 0.201220703] | 0.927734375 / 0.86328125 / 1 | True ([178], []) / True ([105], []) |
| dose_dose1_original_seed1 | upper / linear / sum36 / 1 | 0.345703125 / 0.900390625 | 0.5546875 [0.513671875, 0.59765625] | 0.33984375 / 0.169921875 / 1 | True ([558], []) / True ([802], []) |
| dose_dose1_original_seed1 | upper / linear / sum36 / 2 | 0.30078125 / 0.740234375 | 0.439453125 [0.386669922, 0.494140625] | 0.35546875 / 0.16015625 / 1 | True ([458], []) / True ([441], []) |
| dose_dose1_original_seed1 | upper / linear / sum36 / 3 | 0.32421875 / 0.693359375 | 0.369140625 [0.318359375, 0.421875] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([276], []) |
| dose_dose1_original_seed1 | upper / linear / sum36 / 4 | 0.28515625 / 0.810546875 | 0.525390625 [0.474609375, 0.578125] | 0.375 / 0.19140625 / 0.998046875 | True ([531], []) / True ([526], []) |
| dose_dose1_original_seed1 | upper / linear / sum36 / 5 | 0.40234375 / 0.80859375 | 0.40625 [0.349609375, 0.4609375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([600], []) / True ([336], []) |
| dose_dose1_original_seed1 | upper / mlp64 / category3 / 1 | 0.923828125 / 0.986328125 | 0.0625 [0.0390625, 0.0840332031] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / category3 / 2 | 0.90234375 / 0.947265625 | 0.044921875 [0.0155761719, 0.0742675781] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / category3 / 3 | 0.919921875 / 0.943359375 | 0.0234375 [0, 0.0469238281] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / category3 / 4 | 0.931640625 / 0.958984375 | 0.02734375 [0.005859375, 0.052734375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / category3 / 5 | 0.923828125 / 0.9765625 | 0.052734375 [0.029296875, 0.080078125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / sum36 / 1 | 0.6015625 / 0.916015625 | 0.314453125 [0.271484375, 0.357421875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / sum36 / 2 | 0.546875 / 0.82421875 | 0.27734375 [0.232373047, 0.322314453] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / sum36 / 3 | 0.5625 / 0.794921875 | 0.232421875 [0.1875, 0.275439453] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / sum36 / 4 | 0.580078125 / 0.869140625 | 0.2890625 [0.248046875, 0.3359375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed1 | upper / mlp64 / sum36 / 5 | 0.6875 / 0.849609375 | 0.162109375 [0.119091797, 0.205078125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed1 | 0 | 1.09032154 | 0 | 0.0125658394 | 0 |
| rarity_uniform_equal_seed1 | 1000 | 1.0831995 | 0 | 4.24726329e-05 | 0 |
| rarity_uniform_equal_seed1 | 2000 | 1.08072841 | 0 | 3.92188169e-05 | 0 |
| rarity_uniform_equal_seed1 | 5000 | 1.08291638 | 0 | 9.29171385e-05 | 0 |
| rarity_uniform_equal_seed1 | 10000 | 1.09012055 | 0 | 1.28598429e-05 | 0 |
| rarity_uniform_equal_seed1 | 15000 | 1.0794034 | 0 | 2.10849057e-05 | 0 |
| rarity_uniform_equal_seed1 | 20000 | 1.08105695 | 0 | 0.000106416154 | 0 |
| rarity_uniform_original_seed1 | 0 | 1.09025669 | 0 | 0.0671472389 | 0 |
| rarity_uniform_original_seed1 | 1000 | 1.03739917 | 0 | 0.001836219 | 0 |
| rarity_uniform_original_seed1 | 2000 | 1.05037534 | 0 | 0.00170006547 | 0 |
| rarity_uniform_original_seed1 | 5000 | 1.04044962 | 0 | 0.00063713864 | 0 |
| rarity_uniform_original_seed1 | 10000 | 1.03420663 | 0 | 0.000397725397 | 0 |
| rarity_uniform_original_seed1 | 15000 | 1.04124963 | 0 | 0.000184900387 | 0 |
| rarity_uniform_original_seed1 | 20000 | 1.03548837 | 0 | 0.000167032181 | 0 |
| dose_dose100_equal_seed1 | 0 | 1.09032154 | 3.60113955 | 0.0125658394 | 0 |
| dose_dose100_equal_seed1 | 1000 | 1.08328724 | 0.614033103 | 0.000146007849 | 0.146715777 |
| dose_dose100_equal_seed1 | 2000 | 1.08116829 | 0.359600544 | 7.98460213e-05 | 0.335052179 |
| dose_dose100_equal_seed1 | 5000 | 1.08290565 | 0.209213644 | 0.000112137381 | 0.561735216 |
| dose_dose100_equal_seed1 | 10000 | 1.09021091 | 0.111915775 | 2.35309228e-05 | 0.711274811 |
| dose_dose100_equal_seed1 | 15000 | 1.07933986 | 0.0904552117 | 3.04535695e-05 | 0.775445058 |
| dose_dose100_equal_seed1 | 20000 | 1.08103943 | 0.0821067467 | 0.000102221704 | 0.800572949 |
| dose_dose100_original_seed1 | 0 | 1.09025669 | 3.59748459 | 0.0671472389 | 0 |
| dose_dose100_original_seed1 | 1000 | 1.04060471 | 0.546649337 | 0.00734088522 | 0.198567628 |
| dose_dose100_original_seed1 | 2000 | 1.05168653 | 0.352030277 | 0.00510579206 | 0.361653366 |
| dose_dose100_original_seed1 | 5000 | 1.04147375 | 0.206199259 | 0.00214305417 | 0.586208308 |
| dose_dose100_original_seed1 | 10000 | 1.03592575 | 0.110288374 | 0.00167970628 | 0.727071823 |
| dose_dose100_original_seed1 | 15000 | 1.04270899 | 0.0757339001 | 0.000919462665 | 0.808635154 |
| dose_dose100_original_seed1 | 20000 | 1.0355581 | 0.059800934 | 0.00093252741 | 0.846940864 |
| dose_dose10_equal_seed1 | 0 | 1.09032154 | 0.348955959 | 0.0125658394 | 0 |
| dose_dose10_equal_seed1 | 1000 | 1.08332551 | 0.0666891783 | 0.000127612213 | 0.105954573 |
| dose_dose10_equal_seed1 | 2000 | 1.08089828 | 0.0478503667 | 7.83554344e-05 | 0.227051361 |
| dose_dose10_equal_seed1 | 5000 | 1.08288956 | 0.0305310786 | 0.000121727814 | 0.425823614 |
| dose_dose10_equal_seed1 | 10000 | 1.09027052 | 0.0164185092 | 3.26741645e-05 | 0.58755883 |
| dose_dose10_equal_seed1 | 15000 | 1.0793308 | 0.014170018 | 3.46128558e-05 | 0.666134643 |
| dose_dose10_equal_seed1 | 20000 | 1.08102417 | 0.0122416886 | 0.000101301588 | 0.71176591 |
| dose_dose10_original_seed1 | 0 | 1.09025669 | 0.367303312 | 0.0671472389 | 0 |
| dose_dose10_original_seed1 | 1000 | 1.03955829 | 0.0863547921 | 0.00482261392 | 0.0874974422 |
| dose_dose10_original_seed1 | 2000 | 1.05197406 | 0.0492750145 | 0.00369120408 | 0.249887457 |
| dose_dose10_original_seed1 | 5000 | 1.04159749 | 0.0315300412 | 0.00133740887 | 0.505586249 |
| dose_dose10_original_seed1 | 10000 | 1.03549743 | 0.0152642047 | 0.00117279548 | 0.63380397 |
| dose_dose10_original_seed1 | 15000 | 1.04178393 | 0.0114184674 | 0.000811098443 | 0.695723348 |
| dose_dose10_original_seed1 | 20000 | 1.03561258 | 0.01368808 | 0.000831885304 | 0.727644772 |
| dose_dose1_equal_seed1 | 0 | 1.09032154 | 0.0385664776 | 0.0125658394 | 0 |
| dose_dose1_equal_seed1 | 1000 | 1.0833832 | 0.00883432664 | 7.58035984e-05 | 0.0201350522 |
| dose_dose1_equal_seed1 | 2000 | 1.08076644 | 0.00656745862 | 5.81619889e-05 | 0.104399427 |
| dose_dose1_equal_seed1 | 5000 | 1.0827738 | 0.00617865054 | 0.000119103697 | 0.294209126 |
| dose_dose1_equal_seed1 | 10000 | 1.09021473 | 0.00303067453 | 1.98533871e-05 | 0.406629834 |
| dose_dose1_equal_seed1 | 15000 | 1.07915699 | 0.00321712065 | 6.31510359e-05 | 0.470595457 |
| dose_dose1_equal_seed1 | 20000 | 1.08101606 | 0.00218794262 | 0.000102751289 | 0.534151831 |
| dose_dose1_original_seed1 | 0 | 1.09025669 | 0.0275109913 | 0.0671472389 | 0 |
| dose_dose1_original_seed1 | 1000 | 1.03812861 | 0.017320158 | 0.00238464301 | 0.00126867199 |
| dose_dose1_original_seed1 | 2000 | 1.05042005 | 0.00918735564 | 0.00242182642 | 0.0240229179 |
| dose_dose1_original_seed1 | 5000 | 1.0413028 | 0.00568231149 | 0.00101303661 | 0.186494782 |
| dose_dose1_original_seed1 | 10000 | 1.0345639 | 0.00371419941 | 0.000694892468 | 0.317127072 |
| dose_dose1_original_seed1 | 15000 | 1.04152477 | 0.00262559624 | 0.000485987428 | 0.403396767 |
| dose_dose1_original_seed1 | 20000 | 1.03565156 | 0.0042504943 | 0.000475603946 | 0.475097197 |

### Seed 2 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

The uniform rarity rows are the shared 0% dose controls, not additional runs.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| rarity_uniform_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 48/24435, 684/24435, 290/24435, 172/24435, 21/24435 | 0/24435 | not applicable |
| rarity_uniform_original_seed2 | B_INCOMPLETE | 9/24435; 7/24435; 7/24435; 13/24435 | 41/24435; 34/24435; 41/24435; 40/24435 | 1 / 3 of 101 | 50/24435, 65/24435, 944/24435, 615/24435, 39/24435 | 0/24435 | not applicable |
| dose_dose100_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 24111/24435, 23424/24435, 23394/24435, 23392/24435, 23613/24435 | 20295/24435 | not applicable |
| dose_dose100_original_seed2 | B_INCOMPLETE | 406/24435; 414/24435; 398/24435; 400/24435 | 3619/24435; 3635/24435; 3622/24435; 3631/24435 | 3 / 22 of 101 | 24012/24435, 23472/24435, 23330/24435, 24021/24435, 23367/24435 | 20543/24435 | not applicable |
| dose_dose10_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 23126/24435, 22539/24435, 23048/24435, 22583/24435, 22957/24435 | 16874/24435 | not applicable |
| dose_dose10_original_seed2 | B_INCOMPLETE | 106/24435; 101/24435; 94/24435; 103/24435 | 556/24435; 566/24435; 523/24435; 586/24435 | 1 / 13 of 101 | 23508/24435, 22795/24435, 22849/24435, 22998/24435, 22575/24435 | 17225/24435 | not applicable |
| dose_dose1_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 22596/24435, 21862/24435, 21934/24435, 21484/24435, 21733/24435 | 12551/24435 | not applicable |
| dose_dose1_original_seed2 | B_INCOMPLETE | 85/24435; 93/24435; 83/24435; 96/24435 | 325/24435; 324/24435; 302/24435; 334/24435 | 3 / 8 of 101 | 23020/24435, 21636/24435, 21000/24435, 22178/24435, 21584/24435 | 12647/24435 | not applicable |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed2 | 39580797 | 0 / 0 | {'12': 190469, '13': 1490269, '23': 131016, '24': 3435815} | {'10': 190308, '16': 1493126, '20': 130735, '27': 3436322} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| rarity_uniform_original_seed2 | 39584144 | 0 / 0 | {'12': 206552, '13': 1492472, '23': 131003, '24': 3149917} | {'10': 205025, '16': 1494234, '20': 131093, '27': 3148948} | {'cutoff_sum_counts': {'12': 1.0, '13': 1.0, '23': 1.0, '24': 1.0}, 'decoy_sum_counts': {'10': 1.0, '16': 1.0, '20': 1.0, '27': 1.0}} |
| dose_dose100_equal_seed2 | 39580797 | 39580797 / 1 | {'12': 190469, '13': 1490269, '23': 131016, '24': 3435815} | {'10': 190308, '16': 1493126, '20': 130735, '27': 3436322} | not applicable |
| dose_dose100_original_seed2 | 39584144 | 39584144 / 1 | {'12': 206552, '13': 1492472, '23': 131003, '24': 3149917} | {'10': 205025, '16': 1494234, '20': 131093, '27': 3148948} | not applicable |
| dose_dose10_equal_seed2 | 39580797 | 3957851 / 0.0999942219 | {'12': 190469, '13': 1490269, '23': 131016, '24': 3435815} | {'10': 190308, '16': 1493126, '20': 130735, '27': 3436322} | not applicable |
| dose_dose10_original_seed2 | 39584144 | 3956567 / 0.0999533298 | {'12': 206552, '13': 1492472, '23': 131003, '24': 3149917} | {'10': 205025, '16': 1494234, '20': 131093, '27': 3148948} | not applicable |
| dose_dose1_equal_seed2 | 39580797 | 395827 / 0.0100004808 | {'12': 190469, '13': 1490269, '23': 131016, '24': 3435815} | {'10': 190308, '16': 1493126, '20': 130735, '27': 3436322} | not applicable |
| dose_dose1_original_seed2 | 39584144 | 395361 / 0.00998786282 | {'12': 206552, '13': 1492472, '23': 131003, '24': 3149917} | {'10': 205025, '16': 1494234, '20': 131093, '27': 3148948} | not applicable |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rarity_uniform_equal_seed2 | 0.00325377379/0.00333186984 (n=32) | 0.00320759043/0.00334812701 (n=32) | 0.00323788309/0.0033608675 (n=64) | 0.00323368493/0.00333601236 (n=64) | 0.00323852082/0.00333894789 (n=64) | 0.00324331364/0.00337997079 (n=64) | 0.00324333156/0.0033659488 (n=64) | 0.00323970825/0.0033544153 (n=64) | 0.00323828473/0.00340111554 (n=64) | 0.00324460375/0.00336408615 (n=64) | 0.00323408338 / 0.0033608675 / True | 0.00324129379 / 0.00340111554 / True |
| rarity_uniform_original_seed2 | 0.00429638568/0.00554978102 (n=32) | 0.00665977993/0.0148282051 (n=32) | 0.00546126894/0.0227398053 (n=64) | 0.00520684046/0.0143512636 (n=64) | 0.00532702729/0.0179997236 (n=64) | 0.00593012967/0.0430342108 (n=64) | 0.00985496596/0.249877714 (n=64) | 0.00706158788/0.0204183608 (n=64) | 0.0096109506/0.0298115611 (n=64) | 0.0106212745/0.0241098702 (n=64) | 0.00538206407 / 0.0227398053 / False | 0.00806765598 / 0.249877714 / False |
| dose_dose100_equal_seed2 | 0.00315117557/0.00377300382 (n=32) | 0.00305734621/0.00310112536 (n=32) | 0.0031459725/0.00459522009 (n=64) | 0.00316612516/0.00399878621 (n=64) | 0.00316145481/0.00392001867 (n=64) | 0.00311950338/0.00340630114 (n=64) | 0.0031483334/0.00388139486 (n=64) | 0.00313785393/0.00378403068 (n=64) | 0.00318221329/0.00463156402 (n=64) | 0.00319486647/0.0038561672 (n=64) | 0.00313878618 / 0.00459522009 / True | 0.00315737088 / 0.00463156402 / True |
| dose_dose100_original_seed2 | 0.00875986647/0.015884839 (n=32) | 0.0128822471/0.0701739937 (n=32) | 0.0125281384/0.0699726492 (n=64) | 0.0221956351/0.185219705 (n=64) | 0.0313336746/0.270040423 (n=64) | 0.0389748439/0.222209424 (n=64) | 0.0538412975/0.256968841 (n=64) | 0.0503711062/0.234648183 (n=64) | 0.0580658633/0.242695294 (n=64) | 0.0490049763/0.240844272 (n=64) | 0.0151816101 / 0.185219705 / False | 0.0469319603 / 0.270040423 / False |
| dose_dose10_equal_seed2 | 0.00333556719/0.00387473404 (n=32) | 0.00298088975/0.00320713222 (n=32) | 0.00314506912/0.00463655591 (n=64) | 0.00327872462/0.00542783737 (n=64) | 0.00319521781/0.00508795679 (n=64) | 0.00332092261/0.00507034361 (n=64) | 0.00327075575/0.00515329838 (n=64) | 0.00320994435/0.00521600246 (n=64) | 0.00337173278/0.00491760671 (n=64) | 0.00341801974/0.00583915412 (n=64) | 0.0031940074 / 0.00542783737 / True | 0.00329776551 / 0.00583915412 / True |
| dose_dose10_original_seed2 | 0.00659994059/0.0105090216 (n=32) | 0.00956640346/0.0294613913 (n=32) | 0.00856448291/0.0421923995 (n=64) | 0.0126174657/0.195244715 (n=64) | 0.0121721231/0.0827627182 (n=64) | 0.0176236467/0.179438218 (n=64) | 0.0242458931/0.222125314 (n=64) | 0.0272949865/0.24326098 (n=64) | 0.0274312041/0.261466801 (n=64) | 0.0323662993/0.266543053 (n=64) | 0.00975504021 / 0.195244715 / False | 0.0235223588 / 0.266543053 / False |
| dose_dose1_equal_seed2 | 0.00317846844/0.00419843197 (n=32) | 0.00288492255/0.0030823648 (n=32) | 0.0031516084/0.00579899549 (n=64) | 0.00309053925/0.00392851233 (n=64) | 0.00317731919/0.00577439368 (n=64) | 0.00325222197/0.00616873801 (n=64) | 0.00330368197/0.00504679978 (n=64) | 0.00328178261/0.00531935692 (n=64) | 0.00342557067/0.00595413148 (n=64) | 0.00326110958/0.00488886237 (n=64) | 0.00309128105 / 0.00579899549 / True | 0.00328361433 / 0.00616873801 / True |
| dose_dose1_original_seed2 | 0.00564929633/0.00743109733 (n=32) | 0.00609275466/0.00715836883 (n=32) | 0.00798033294/0.0426222607 (n=64) | 0.0108715785/0.11074914 (n=64) | 0.0243698338/0.258419149 (n=64) | 0.0132921344/0.239032902 (n=64) | 0.0241229717/0.25662899 (n=64) | 0.0197981248/0.256731384 (n=64) | 0.0246737327/0.256047934 (n=64) | 0.0173000122/0.255491547 (n=64) | 0.00824097897 / 0.11074914 / False | 0.0205928016 / 0.258419149 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed2 | 3.89530277e-05 / 3.919014e-05 (n=20211) | not recorded / 7.4217096e-05 | none | 0.000219479203 / True | 0 / True |
| rarity_uniform_original_seed2 | 0.000174531007 / 0.000189056231 (n=24131) | 0.997650538 / 0.252513766 | law_TV, swaps | 0.00793328136 / True | 0 / True |
| dose_dose100_equal_seed2 | 4.09715277e-05 / 4.270538e-05 (n=20211) | not recorded / 0.000251754653 | none | 0.00042578578 / True | 0 / True |
| dose_dose100_original_seed2 | 0.00123433675 / 0.00109884378 (n=24131) | 0.982970686 / 0.244995192 | law_TV, rerender, swaps | 0.0921629518 / False | 0 / True |
| dose_dose10_equal_seed2 | 4.31136918e-05 / 4.83314424e-05 (n=20211) | not recorded / 0.000477300491 | none | 0.000646829605 / True | 0 / True |
| dose_dose10_original_seed2 | 0.000686644649 / 0.000784644279 (n=24131) | 0.992669253 / 0.251700461 | law_TV, rerender, swaps | 0.0200648382 / False | 0 / True |
| dose_dose1_equal_seed2 | 4.27734074e-05 / 4.79152658e-05 (n=20211) | not recorded / 0.000637603458 | none | 0.000586628914 / True | 0 / True |
| dose_dose1_original_seed2 | 0.000618522311 / 0.000820319956 (n=24131) | 0.994721478 / 0.256639302 | law_TV, swaps | 0.0118753985 / True | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| rarity_uniform_equal_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_equal_seed2 | A_swap_exact_row | 64 | 0.00321744406 / 0.00333410501 |
| rarity_uniform_equal_seed2 | both_swap_exact_row | 64 | 0.00321744406 / 0.00333410501 |
| rarity_uniform_equal_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_equal_seed2 | neutral_N | 192 | 0.00322136446 / 0.00339455903 |
| rarity_uniform_equal_seed2 | neutral_raw_swap_stability | 128 | 9.16725257e-05 / 0.000249415636 |
| rarity_uniform_equal_seed2 | raw_swap_effect | 64 | 0.000109301414 / 0.000231802464 |
| rarity_uniform_equal_seed2 | raw_swap_exact_row | 64 | 0.00321744406 / 0.00333410501 |
| rarity_uniform_equal_seed2 | raw_swap_stability | 128 | 0.00166337274 / 0.00333410501 |
| rarity_uniform_equal_seed2 | reset_L | 160 | 0.00324777476 / 0.00339499116 |
| rarity_uniform_equal_seed2 | same_category_substitution | 128 | 9.16725257e-05 / 0.000249415636 |
| rarity_uniform_equal_seed2 | set_H | 160 | 0.00318467971 / 0.00326183438 |
| rarity_uniform_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00322115142 / 0.00333410501 |
| rarity_uniform_original_seed2 | A_swap_effect | 64 | 0 / 0 |
| rarity_uniform_original_seed2 | A_swap_exact_row | 64 | 0.253982547 / 0.257066146 |
| rarity_uniform_original_seed2 | both_swap_exact_row | 64 | 0.0054668379 / 0.0080999732 |
| rarity_uniform_original_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| rarity_uniform_original_seed2 | neutral_N | 192 | 0.00526839599 / 0.013760522 |
| rarity_uniform_original_seed2 | neutral_raw_swap_stability | 128 | 0.00249371753 / 0.0228154361 |
| rarity_uniform_original_seed2 | raw_swap_effect | 64 | 0.254539587 / 0.258692071 |
| rarity_uniform_original_seed2 | raw_swap_exact_row | 64 | 0.0054668379 / 0.0080999732 |
| rarity_uniform_original_seed2 | raw_swap_stability | 128 | 0.254261067 / 0.258692071 |
| rarity_uniform_original_seed2 | reset_L | 160 | 0.00445461641 / 0.0101616457 |
| rarity_uniform_original_seed2 | same_category_substitution | 128 | 0.00249371753 / 0.0228154361 |
| rarity_uniform_original_seed2 | set_H | 160 | 0.006547292 / 0.0115155876 |
| rarity_uniform_original_seed2 | upper_state_exchange_same_N | 64 | 0.00524523901 / 0.00873918086 |
| dose_dose100_equal_seed2 | A_swap_effect | 64 | 0 / 0 |
| dose_dose100_equal_seed2 | A_swap_exact_row | 64 | 0.00312420726 / 0.00542233884 |
| dose_dose100_equal_seed2 | both_swap_exact_row | 64 | 0.00312420726 / 0.00542233884 |
| dose_dose100_equal_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose100_equal_seed2 | neutral_N | 192 | 0.00314119807 / 0.00534403324 |
| dose_dose100_equal_seed2 | neutral_raw_swap_stability | 128 | 0.000105370535 / 0.000516831875 |
| dose_dose100_equal_seed2 | raw_swap_effect | 64 | 0.000218618661 / 0.00232331455 |
| dose_dose100_equal_seed2 | raw_swap_exact_row | 64 | 0.00312420726 / 0.00542233884 |
| dose_dose100_equal_seed2 | raw_swap_stability | 128 | 0.00167141296 / 0.00542233884 |
| dose_dose100_equal_seed2 | reset_L | 160 | 0.00323825749 / 0.00754158199 |
| dose_dose100_equal_seed2 | same_category_substitution | 128 | 0.000105370535 / 0.000516831875 |
| dose_dose100_equal_seed2 | set_H | 160 | 0.00310898302 / 0.00544667244 |
| dose_dose100_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00313699944 / 0.00534403324 |
| dose_dose100_original_seed2 | A_swap_effect | 64 | 0 / 0 |
| dose_dose100_original_seed2 | A_swap_exact_row | 64 | 0.252391644 / 0.26596339 |
| dose_dose100_original_seed2 | both_swap_exact_row | 64 | 0.0113251542 / 0.0375970528 |
| dose_dose100_original_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose100_original_seed2 | neutral_N | 192 | 0.016573079 / 0.231835976 |
| dose_dose100_original_seed2 | neutral_raw_swap_stability | 128 | 0.0150018195 / 0.143672474 |
| dose_dose100_original_seed2 | raw_swap_effect | 64 | 0.251057732 / 0.268141456 |
| dose_dose100_original_seed2 | raw_swap_exact_row | 64 | 0.0113251542 / 0.0375970528 |
| dose_dose100_original_seed2 | raw_swap_stability | 128 | 0.251724688 / 0.268141456 |
| dose_dose100_original_seed2 | reset_L | 160 | 0.0168372726 / 0.260040827 |
| dose_dose100_original_seed2 | same_category_substitution | 128 | 0.0150018195 / 0.143672474 |
| dose_dose100_original_seed2 | set_H | 160 | 0.0105806909 / 0.0467537194 |
| dose_dose100_original_seed2 | upper_state_exchange_same_N | 64 | 0.0135832696 / 0.135632873 |
| dose_dose10_equal_seed2 | A_swap_effect | 64 | 0 / 0 |
| dose_dose10_equal_seed2 | A_swap_exact_row | 64 | 0.00313176983 / 0.00423710048 |
| dose_dose10_equal_seed2 | both_swap_exact_row | 64 | 0.00313176983 / 0.00423710048 |
| dose_dose10_equal_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose10_equal_seed2 | neutral_N | 192 | 0.00311300376 / 0.00416536629 |
| dose_dose10_equal_seed2 | neutral_raw_swap_stability | 128 | 0.00021228136 / 0.000585123897 |
| dose_dose10_equal_seed2 | raw_swap_effect | 64 | 0.000456057023 / 0.00191392004 |
| dose_dose10_equal_seed2 | raw_swap_exact_row | 64 | 0.00313176983 / 0.00423710048 |
| dose_dose10_equal_seed2 | raw_swap_stability | 128 | 0.00179391343 / 0.00423710048 |
| dose_dose10_equal_seed2 | reset_L | 160 | 0.0033244594 / 0.00535085797 |
| dose_dose10_equal_seed2 | same_category_substitution | 128 | 0.00021228136 / 0.000585123897 |
| dose_dose10_equal_seed2 | set_H | 160 | 0.00297176074 / 0.00425483286 |
| dose_dose10_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00311540347 / 0.00386975706 |
| dose_dose10_original_seed2 | A_swap_effect | 64 | 0 / 0 |
| dose_dose10_original_seed2 | A_swap_exact_row | 64 | 0.254512114 / 0.266605735 |
| dose_dose10_original_seed2 | both_swap_exact_row | 64 | 0.0081629795 / 0.0255256146 |
| dose_dose10_original_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose10_original_seed2 | neutral_N | 192 | 0.00823231635 / 0.0971585065 |
| dose_dose10_original_seed2 | neutral_raw_swap_stability | 128 | 0.0073686862 / 0.0684828833 |
| dose_dose10_original_seed2 | raw_swap_effect | 64 | 0.255511248 / 0.267660759 |
| dose_dose10_original_seed2 | raw_swap_exact_row | 64 | 0.0081629795 / 0.0255256146 |
| dose_dose10_original_seed2 | raw_swap_stability | 128 | 0.255011681 / 0.267660759 |
| dose_dose10_original_seed2 | reset_L | 160 | 0.0101465531 / 0.183938235 |
| dose_dose10_original_seed2 | same_category_substitution | 128 | 0.0073686862 / 0.0684828833 |
| dose_dose10_original_seed2 | set_H | 160 | 0.00853124531 / 0.0447341576 |
| dose_dose10_original_seed2 | upper_state_exchange_same_N | 64 | 0.00765910593 / 0.0414277166 |
| dose_dose1_equal_seed2 | A_swap_effect | 64 | 0 / 0 |
| dose_dose1_equal_seed2 | A_swap_exact_row | 64 | 0.00309849693 / 0.0061828196 |
| dose_dose1_equal_seed2 | both_swap_exact_row | 64 | 0.00309849693 / 0.0061828196 |
| dose_dose1_equal_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose1_equal_seed2 | neutral_N | 192 | 0.00311305188 / 0.00599123538 |
| dose_dose1_equal_seed2 | neutral_raw_swap_stability | 128 | 0.000198329217 / 0.000720754266 |
| dose_dose1_equal_seed2 | raw_swap_effect | 64 | 0.000603612047 / 0.00308401883 |
| dose_dose1_equal_seed2 | raw_swap_exact_row | 64 | 0.00309849693 / 0.0061828196 |
| dose_dose1_equal_seed2 | raw_swap_stability | 128 | 0.00185105449 / 0.0061828196 |
| dose_dose1_equal_seed2 | reset_L | 160 | 0.00341496356 / 0.00922568142 |
| dose_dose1_equal_seed2 | same_category_substitution | 128 | 0.000198329217 / 0.000720754266 |
| dose_dose1_equal_seed2 | set_H | 160 | 0.00295503242 / 0.00626860559 |
| dose_dose1_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00310847769 / 0.00599123538 |
| dose_dose1_original_seed2 | A_swap_effect | 64 | 0 / 0 |
| dose_dose1_original_seed2 | A_swap_exact_row | 64 | 0.255017646 / 0.257597797 |
| dose_dose1_original_seed2 | both_swap_exact_row | 64 | 0.0058716886 / 0.00759779662 |
| dose_dose1_original_seed2 | neutral_A_swap_stability | 128 | 0 / 0 |
| dose_dose1_original_seed2 | neutral_N | 192 | 0.00869322196 / 0.0648373663 |
| dose_dose1_original_seed2 | neutral_raw_swap_stability | 128 | 0.00380040525 / 0.0756926015 |
| dose_dose1_original_seed2 | raw_swap_effect | 64 | 0.255434085 / 0.257663824 |
| dose_dose1_original_seed2 | raw_swap_exact_row | 64 | 0.0058716886 / 0.00759779662 |
| dose_dose1_original_seed2 | raw_swap_stability | 128 | 0.255225866 / 0.257663824 |
| dose_dose1_original_seed2 | reset_L | 160 | 0.0109577597 / 0.245765068 |
| dose_dose1_original_seed2 | same_category_substitution | 128 | 0.00380040525 / 0.0756926015 |
| dose_dose1_original_seed2 | set_H | 160 | 0.00634870501 / 0.00815066695 |
| dose_dose1_original_seed2 | upper_state_exchange_same_N | 64 | 0.00780011038 / 0.0134374127 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.67578125 | -0.068359375 [-0.115234375, -0.015625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([96], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.884765625 | 0.126953125 [0.0859375, 0.166015625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([79], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.87109375 | 0.123046875 [0.080078125, 0.1640625] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([113], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.890625 | 0.07421875 [0.037109375, 0.115234375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([79], []) |
| rarity_uniform_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.798828125 | 0.078125 [0.0351074219, 0.123046875] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([73], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.365234375 | 0.111328125 [0.056640625, 0.1640625] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([321], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.5078125 | 0.185546875 [0.134765625, 0.238330078] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([365], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.556640625 | 0.263671875 [0.212890625, 0.3125] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([625], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.5546875 | 0.1953125 [0.142529297, 0.248046875] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([340], []) |
| rarity_uniform_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.462890625 | 0.193359375 [0.138671875, 0.25] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([356], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.9140625 | -0.009765625 [-0.0332519531, 0.01171875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.947265625 | 0.0234375 [-0.001953125, 0.0488769531] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.955078125 | 0.025390625 [0.005859375, 0.044921875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.953125 | 0.01953125 [0, 0.0390625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9296875 | 0.017578125 [-0.005859375, 0.044921875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.708984375 | 0.15234375 [0.103515625, 0.201171875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.66796875 | 0.064453125 [0.015625, 0.115234375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.79296875 | 0.2265625 [0.177734375, 0.2734375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.814453125 | 0.193359375 [0.148388672, 0.240234375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.669921875 | 0.025390625 [-0.0312988281, 0.076171875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.7109375 | -0.0625 [-0.109423828, -0.01171875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([111], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.8828125 | 0.08203125 [0.044921875, 0.119140625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([113], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.87109375 | 0.099609375 [0.060546875, 0.140625] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([146], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.87109375 | 0.02734375 [-0.01171875, 0.0625] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([152], []) |
| rarity_uniform_equal_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.81640625 | 0.07421875 [0.03515625, 0.115234375] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([114], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.33203125 | 0.064453125 [0.009765625, 0.1171875] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([567], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.478515625 | 0.125 [0.072265625, 0.17578125] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([643], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.513671875 | 0.205078125 [0.154296875, 0.257861328] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([821], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.5078125 | 0.126953125 [0.0703125, 0.181640625] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([788], []) |
| rarity_uniform_equal_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.4140625 | 0.126953125 [0.0663574219, 0.18359375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([660], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.91015625 | 0.001953125 [-0.021484375, 0.025390625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.9375 | 0.021484375 [-0.00390625, 0.0469238281] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.9296875 | 0.013671875 [-0.01171875, 0.037109375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.947265625 | 0.005859375 [-0.017578125, 0.02734375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.939453125 | 0.037109375 [0.01171875, 0.0625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.630859375 | 0.1171875 [0.068359375, 0.164111328] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.5859375 | -0.013671875 [-0.0684082031, 0.0390625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.71875 | 0.142578125 [0.095703125, 0.19140625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.748046875 | 0.107421875 [0.05859375, 0.15625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.623046875 | -0.01171875 [-0.0625, 0.041015625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 1 | 0.255859375 [0.21875, 0.29296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([97], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.548828125 | -0.208984375 [-0.263671875, -0.150390625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([92], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.619140625 | -0.12890625 [-0.18359375, -0.07421875] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([96], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.72265625 | -0.09375 [-0.14453125, -0.04296875] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([91], []) |
| rarity_uniform_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.580078125 | -0.140625 [-0.193359375, -0.08984375] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([76], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.966796875 | 0.712890625 [0.677685547, 0.75] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([556], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.0703125 | -0.251953125 [-0.29296875, -0.208935547] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([206], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.072265625 | -0.220703125 [-0.26171875, -0.17578125] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([226], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.111328125 | -0.248046875 [-0.294921875, -0.19921875] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([244], []) |
| rarity_uniform_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.09765625 | -0.171875 [-0.216796875, -0.130859375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([210], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 1 | 0.076171875 [0.052734375, 0.099609375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.90234375 | -0.021484375 [-0.04296875, 0] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.931640625 | 0.001953125 [-0.015625, 0.021484375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.931640625 | -0.001953125 [-0.017578125, 0.013671875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.923828125 | 0.01171875 [-0.0078125, 0.03515625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.9765625 | 0.419921875 [0.382763672, 0.462890625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.431640625 | -0.171875 [-0.220703125, -0.12109375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.384765625 | -0.181640625 [-0.228515625, -0.136669922] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.482421875 | -0.138671875 [-0.19140625, -0.083984375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.4296875 | -0.21484375 [-0.269580078, -0.162109375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 1 | 0.7734375 / 1 | 0.2265625 [0.189453125, 0.263671875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([56], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.5234375 | -0.27734375 [-0.328173828, -0.22265625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([120], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.69140625 | -0.080078125 [-0.126953125, -0.025390625] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([123], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.705078125 | -0.138671875 [-0.1875, -0.08984375] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([132], []) |
| rarity_uniform_original_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.611328125 | -0.130859375 [-0.1796875, -0.08203125] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([129], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.97265625 | 0.705078125 [0.666015625, 0.748046875] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([484], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.056640625 | -0.296875 [-0.33984375, -0.251953125] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([336], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.087890625 | -0.220703125 [-0.265625, -0.177734375] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([367], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.0859375 | -0.294921875 [-0.33984375, -0.248046875] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([302], []) |
| rarity_uniform_original_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.0546875 | -0.232421875 [-0.28125, -0.1875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([306], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 1 | 0.091796875 [0.06640625, 0.117236328] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.900390625 | -0.015625 [-0.0390625, 0.005859375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.927734375 | 0.01171875 [-0.0078125, 0.029296875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.931640625 | -0.009765625 [-0.029296875, 0.0078125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.92578125 | 0.0234375 [-0.001953125, 0.046875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.974609375 | 0.4609375 [0.416015625, 0.505859375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.37890625 | -0.220703125 [-0.273486328, -0.165966797] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.37890625 | -0.197265625 [-0.242236328, -0.148388672] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.43359375 | -0.20703125 [-0.255908203, -0.15625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| rarity_uniform_original_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.384765625 | -0.25 [-0.29296875, -0.19921875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.984375 | 0.240234375 [0.203125, 0.279296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([57], []) |
| dose_dose100_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.916015625 | 0.158203125 [0.115234375, 0.19921875] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([79], []) |
| dose_dose100_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.951171875 | 0.203125 [0.162109375, 0.240234375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([81], []) |
| dose_dose100_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.974609375 | 0.158203125 [0.125, 0.1953125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([75], []) |
| dose_dose100_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.9765625 | 0.255859375 [0.216796875, 0.294921875] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([66], []) |
| dose_dose100_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.97265625 | 0.71875 [0.6796875, 0.7578125] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([161], []) |
| dose_dose100_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.92578125 | 0.603515625 [0.5625, 0.646484375] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([316], []) |
| dose_dose100_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.890625 | 0.59765625 [0.55078125, 0.642578125] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([302], []) |
| dose_dose100_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.931640625 | 0.572265625 [0.529296875, 0.615234375] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([334], []) |
| dose_dose100_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.94140625 | 0.671875 [0.62890625, 0.71484375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([259], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.984375 | 0.060546875 [0.037109375, 0.083984375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.966796875 | 0.04296875 [0.01953125, 0.06640625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.9609375 | 0.03125 [0.0078125, 0.0546875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.986328125 | 0.052734375 [0.0312011719, 0.076171875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9921875 | 0.080078125 [0.056640625, 0.107421875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.974609375 | 0.41796875 [0.376953125, 0.462890625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.923828125 | 0.3203125 [0.279296875, 0.361328125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.908203125 | 0.341796875 [0.30078125, 0.3828125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.92578125 | 0.3046875 [0.259765625, 0.34765625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.93359375 | 0.2890625 [0.244140625, 0.333984375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.85546875 | 0.08203125 [0.041015625, 0.125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([88], []) |
| dose_dose100_equal_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.91015625 | 0.109375 [0.0703125, 0.1484375] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([117], []) |
| dose_dose100_equal_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.765625 | -0.005859375 [-0.05078125, 0.044921875] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([90], []) |
| dose_dose100_equal_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.951171875 | 0.107421875 [0.07421875, 0.142578125] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([169], []) |
| dose_dose100_equal_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.916015625 | 0.173828125 [0.130859375, 0.21875] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([94], []) |
| dose_dose100_equal_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.845703125 | 0.578125 [0.53125, 0.626953125] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([119], []) |
| dose_dose100_equal_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.810546875 | 0.45703125 [0.40625, 0.5078125] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([658], []) |
| dose_dose100_equal_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.728515625 | 0.419921875 [0.367138672, 0.47265625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([173], []) |
| dose_dose100_equal_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.77734375 | 0.396484375 [0.34375, 0.451171875] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([658], []) |
| dose_dose100_equal_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.7734375 | 0.486328125 [0.43359375, 0.54296875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([215], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.947265625 | 0.0390625 [0.013671875, 0.064453125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.95703125 | 0.041015625 [0.013671875, 0.0664550781] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.939453125 | 0.0234375 [0, 0.046875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.978515625 | 0.037109375 [0.017578125, 0.060546875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.984375 | 0.08203125 [0.056640625, 0.109375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.900390625 | 0.38671875 [0.33984375, 0.431640625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.84765625 | 0.248046875 [0.197265625, 0.291015625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.857421875 | 0.28125 [0.236279297, 0.328125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.875 | 0.234375 [0.19140625, 0.275390625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.859375 | 0.224609375 [0.181640625, 0.265625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.98828125 | 0.244140625 [0.20703125, 0.28515625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([52], []) |
| dose_dose100_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.966796875 | 0.208984375 [0.171826172, 0.248046875] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([79], []) |
| dose_dose100_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.978515625 | 0.23046875 [0.19140625, 0.267578125] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([87], []) |
| dose_dose100_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.990234375 | 0.173828125 [0.142578125, 0.207080078] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([72], []) |
| dose_dose100_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.9609375 | 0.240234375 [0.199169922, 0.279345703] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([78], []) |
| dose_dose100_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.9765625 | 0.72265625 [0.685546875, 0.76171875] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([192], []) |
| dose_dose100_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.9140625 | 0.591796875 [0.550732422, 0.63671875] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([304], []) |
| dose_dose100_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.921875 | 0.62890625 [0.5859375, 0.671875] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([336], []) |
| dose_dose100_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.955078125 | 0.595703125 [0.552734375, 0.638671875] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([254], []) |
| dose_dose100_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.923828125 | 0.654296875 [0.611328125, 0.69921875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([203], []) |
| dose_dose100_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.98046875 | 0.056640625 [0.033203125, 0.080078125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.978515625 | 0.0546875 [0.02734375, 0.0781738281] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.984375 | 0.0546875 [0.03515625, 0.076171875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.990234375 | 0.056640625 [0.037109375, 0.078125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.986328125 | 0.07421875 [0.05078125, 0.099609375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.970703125 | 0.4140625 [0.375, 0.457080078] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.91015625 | 0.306640625 [0.267578125, 0.349609375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.91796875 | 0.3515625 [0.310498047, 0.392626953] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.95703125 | 0.3359375 [0.29296875, 0.380859375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.94140625 | 0.296875 [0.251904297, 0.337939453] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.98828125 | 0.21484375 [0.1796875, 0.250048828] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([78], []) |
| dose_dose100_original_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.931640625 | 0.130859375 [0.09375, 0.16796875] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([112], []) |
| dose_dose100_original_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.95703125 | 0.185546875 [0.150341797, 0.228564453] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([122], []) |
| dose_dose100_original_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.970703125 | 0.126953125 [0.09375, 0.16015625] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([89], []) |
| dose_dose100_original_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.91796875 | 0.17578125 [0.1328125, 0.216796875] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([97], []) |
| dose_dose100_original_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.93359375 | 0.666015625 [0.619140625, 0.712890625] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([335], []) |
| dose_dose100_original_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.751953125 | 0.3984375 [0.34375, 0.453125] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([380], []) |
| dose_dose100_original_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.8359375 | 0.52734375 [0.480419922, 0.572265625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([588], []) |
| dose_dose100_original_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.826171875 | 0.4453125 [0.39453125, 0.494140625] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([233], []) |
| dose_dose100_original_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.83203125 | 0.544921875 [0.4921875, 0.593798828] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([157], []) |
| dose_dose100_original_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.98046875 | 0.072265625 [0.046875, 0.099609375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.96875 | 0.052734375 [0.0272949219, 0.080078125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.970703125 | 0.0546875 [0.03125, 0.0781738281] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.982421875 | 0.041015625 [0.021484375, 0.0605957031] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.974609375 | 0.072265625 [0.046875, 0.099609375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.9453125 | 0.431640625 [0.384765625, 0.478515625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.8203125 | 0.220703125 [0.173779297, 0.265625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.890625 | 0.314453125 [0.271484375, 0.359375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.91015625 | 0.26953125 [0.228515625, 0.3125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose100_original_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.8984375 | 0.263671875 [0.22265625, 0.306640625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.982421875 | 0.23828125 [0.201171875, 0.279296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([59], []) |
| dose_dose10_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.947265625 | 0.189453125 [0.152294922, 0.2265625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([69], []) |
| dose_dose10_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.9453125 | 0.197265625 [0.16015625, 0.234375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([74], []) |
| dose_dose10_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.95703125 | 0.140625 [0.103515625, 0.177734375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([86], []) |
| dose_dose10_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.96875 | 0.248046875 [0.208935547, 0.28515625] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([77], []) |
| dose_dose10_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.939453125 | 0.685546875 [0.642529297, 0.724609375] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([180], []) |
| dose_dose10_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.8828125 | 0.560546875 [0.517578125, 0.609375] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([360], []) |
| dose_dose10_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.904296875 | 0.611328125 [0.5703125, 0.65234375] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([314], []) |
| dose_dose10_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.91015625 | 0.55078125 [0.505859375, 0.595751953] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([332], []) |
| dose_dose10_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.908203125 | 0.638671875 [0.595703125, 0.685546875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([304], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.9765625 | 0.052734375 [0.029296875, 0.07421875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.966796875 | 0.04296875 [0.017578125, 0.068359375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.955078125 | 0.025390625 [0.001953125, 0.048828125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.978515625 | 0.044921875 [0.0234375, 0.068359375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.986328125 | 0.07421875 [0.05078125, 0.1015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.921875 | 0.365234375 [0.32421875, 0.408203125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.900390625 | 0.296875 [0.253857422, 0.337890625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.916015625 | 0.349609375 [0.30859375, 0.39453125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.91796875 | 0.296875 [0.255810547, 0.337890625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.92578125 | 0.28125 [0.236279297, 0.322265625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.849609375 | 0.076171875 [0.029296875, 0.12109375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([104], []) |
| dose_dose10_equal_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.927734375 | 0.126953125 [0.08984375, 0.1640625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([97], []) |
| dose_dose10_equal_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.921875 | 0.150390625 [0.11328125, 0.193408203] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([120], []) |
| dose_dose10_equal_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.939453125 | 0.095703125 [0.05859375, 0.1328125] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([142], []) |
| dose_dose10_equal_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.921875 | 0.1796875 [0.138671875, 0.220703125] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([95], []) |
| dose_dose10_equal_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.814453125 | 0.546875 [0.499951172, 0.59765625] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([183], []) |
| dose_dose10_equal_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.77734375 | 0.423828125 [0.375, 0.48046875] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([493], []) |
| dose_dose10_equal_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.7890625 | 0.48046875 [0.4296875, 0.53125] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([272], []) |
| dose_dose10_equal_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.744140625 | 0.36328125 [0.3125, 0.4140625] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([452], []) |
| dose_dose10_equal_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.765625 | 0.478515625 [0.419921875, 0.533251953] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([180], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.94921875 | 0.041015625 [0.0136230469, 0.068359375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.947265625 | 0.03125 [0.00390625, 0.0586425781] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.951171875 | 0.03515625 [0.0078125, 0.060546875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.96875 | 0.02734375 [0.005859375, 0.0488769531] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.9765625 | 0.07421875 [0.048828125, 0.10546875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.892578125 | 0.37890625 [0.333984375, 0.42578125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.822265625 | 0.22265625 [0.173828125, 0.271484375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.86328125 | 0.287109375 [0.2421875, 0.333984375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.849609375 | 0.208984375 [0.166015625, 0.251953125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.884765625 | 0.25 [0.205078125, 0.294921875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.99609375 | 0.251953125 [0.216796875, 0.2890625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([60], []) |
| dose_dose10_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.9609375 | 0.203125 [0.1640625, 0.2421875] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([71], []) |
| dose_dose10_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.974609375 | 0.2265625 [0.189453125, 0.263671875] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([83], []) |
| dose_dose10_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.9765625 | 0.16015625 [0.126953125, 0.195361328] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([77], []) |
| dose_dose10_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.974609375 | 0.25390625 [0.21484375, 0.291064453] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([71], []) |
| dose_dose10_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.95703125 | 0.703125 [0.6640625, 0.7421875] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([375], []) |
| dose_dose10_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.9140625 | 0.591796875 [0.55078125, 0.636767578] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([280], []) |
| dose_dose10_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.912109375 | 0.619140625 [0.576171875, 0.660205078] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([359], []) |
| dose_dose10_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.916015625 | 0.556640625 [0.513671875, 0.6015625] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([443], []) |
| dose_dose10_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.921875 | 0.65234375 [0.609375, 0.697265625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([396], []) |
| dose_dose10_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.990234375 | 0.06640625 [0.041015625, 0.091796875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.978515625 | 0.0546875 [0.0292480469, 0.080078125] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.984375 | 0.0546875 [0.033203125, 0.078125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.982421875 | 0.048828125 [0.02734375, 0.072265625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9921875 | 0.080078125 [0.056640625, 0.10546875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.9609375 | 0.404296875 [0.365234375, 0.447265625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.921875 | 0.318359375 [0.279296875, 0.361376953] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.919921875 | 0.353515625 [0.314453125, 0.3984375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.93359375 | 0.3125 [0.26953125, 0.353564453] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.923828125 | 0.279296875 [0.234375, 0.32421875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.990234375 | 0.216796875 [0.177734375, 0.251953125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([57], []) |
| dose_dose10_original_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.93359375 | 0.1328125 [0.09375, 0.171875] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([107], []) |
| dose_dose10_original_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.95703125 | 0.185546875 [0.1484375, 0.2265625] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([94], []) |
| dose_dose10_original_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.962890625 | 0.119140625 [0.0859375, 0.154296875] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([135], []) |
| dose_dose10_original_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.9375 | 0.1953125 [0.154296875, 0.23828125] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([101], []) |
| dose_dose10_original_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.904296875 | 0.63671875 [0.58984375, 0.683642578] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([1210], []) |
| dose_dose10_original_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.810546875 | 0.45703125 [0.40625, 0.507861328] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([279], []) |
| dose_dose10_original_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.7734375 | 0.46484375 [0.4140625, 0.515625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([522], []) |
| dose_dose10_original_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.82421875 | 0.443359375 [0.390625, 0.494140625] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([506], []) |
| dose_dose10_original_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.73046875 | 0.443359375 [0.38671875, 0.498046875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([296], []) |
| dose_dose10_original_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.990234375 | 0.08203125 [0.0546875, 0.107421875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.978515625 | 0.0625 [0.037109375, 0.087890625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.982421875 | 0.06640625 [0.04296875, 0.091796875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.98046875 | 0.0390625 [0.017578125, 0.0625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.9765625 | 0.07421875 [0.048828125, 0.10546875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.91796875 | 0.404296875 [0.361328125, 0.44921875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.87890625 | 0.279296875 [0.234326172, 0.322265625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.8515625 | 0.275390625 [0.23046875, 0.3203125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.8828125 | 0.2421875 [0.199169922, 0.283203125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose10_original_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.828125 | 0.193359375 [0.1484375, 0.236328125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.984375 | 0.240234375 [0.203125, 0.277392578] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([74], []) |
| dose_dose1_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.921875 | 0.1640625 [0.125, 0.203125] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([71], []) |
| dose_dose1_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.9453125 | 0.197265625 [0.158203125, 0.234423828] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([85], []) |
| dose_dose1_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.9296875 | 0.11328125 [0.080078125, 0.15234375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([47], []) |
| dose_dose1_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.9375 | 0.216796875 [0.175732422, 0.2578125] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([71], []) |
| dose_dose1_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.923828125 | 0.669921875 [0.62890625, 0.7109375] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([282], []) |
| dose_dose1_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.89453125 | 0.572265625 [0.529248047, 0.6171875] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([311], []) |
| dose_dose1_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.876953125 | 0.583984375 [0.542919922, 0.62890625] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([374], []) |
| dose_dose1_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.876953125 | 0.517578125 [0.474609375, 0.564453125] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([276], []) |
| dose_dose1_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.896484375 | 0.626953125 [0.583984375, 0.67578125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([298], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.984375 | 0.060546875 [0.037109375, 0.0840332031] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.947265625 | 0.0234375 [-0.001953125, 0.046875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.970703125 | 0.041015625 [0.017578125, 0.064453125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.978515625 | 0.044921875 [0.025390625, 0.0645019531] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.96875 | 0.056640625 [0.0292480469, 0.083984375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.9453125 | 0.388671875 [0.347607422, 0.431640625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.87890625 | 0.275390625 [0.232421875, 0.31640625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.884765625 | 0.318359375 [0.279296875, 0.361328125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.900390625 | 0.279296875 [0.236328125, 0.322265625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.91015625 | 0.265625 [0.21875, 0.30859375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.916015625 | 0.142578125 [0.099609375, 0.18359375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([91], []) |
| dose_dose1_equal_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.904296875 | 0.103515625 [0.06640625, 0.140625] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([133], []) |
| dose_dose1_equal_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.890625 | 0.119140625 [0.078125, 0.16015625] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([101], []) |
| dose_dose1_equal_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.904296875 | 0.060546875 [0.0234375, 0.09765625] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([133], []) |
| dose_dose1_equal_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.8046875 | 0.0625 [0.015625, 0.111328125] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([94], []) |
| dose_dose1_equal_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.841796875 | 0.57421875 [0.525390625, 0.623046875] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([288], []) |
| dose_dose1_equal_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.8125 | 0.458984375 [0.40625, 0.51171875] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([502], []) |
| dose_dose1_equal_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.666015625 | 0.357421875 [0.30078125, 0.40625] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([205], []) |
| dose_dose1_equal_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.7421875 | 0.361328125 [0.306640625, 0.416015625] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([343], []) |
| dose_dose1_equal_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.712890625 | 0.42578125 [0.3671875, 0.484375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([144], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.966796875 | 0.05859375 [0.03515625, 0.083984375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.939453125 | 0.0234375 [-0.005859375, 0.0508300781] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.962890625 | 0.046875 [0.021484375, 0.0723144531] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.953125 | 0.01171875 [-0.009765625, 0.037109375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.9609375 | 0.05859375 [0.03125, 0.08984375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.896484375 | 0.3828125 [0.335888672, 0.4296875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.875 | 0.275390625 [0.23046875, 0.31640625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.837890625 | 0.26171875 [0.216796875, 0.30859375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.830078125 | 0.189453125 [0.142578125, 0.232470703] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.833984375 | 0.19921875 [0.152294922, 0.244140625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.998046875 | 0.25390625 [0.21875, 0.29296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([49], []) |
| dose_dose1_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.9765625 | 0.21875 [0.181591797, 0.255859375] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([68], []) |
| dose_dose1_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.900390625 | 0.15234375 [0.111328125, 0.1953125] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([84], []) |
| dose_dose1_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.9375 | 0.12109375 [0.083984375, 0.158251953] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([64], []) |
| dose_dose1_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.94921875 | 0.228515625 [0.189453125, 0.26953125] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([66], []) |
| dose_dose1_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.955078125 | 0.701171875 [0.662109375, 0.7421875] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([532], []) |
| dose_dose1_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.873046875 | 0.55078125 [0.505810547, 0.599658203] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([231], []) |
| dose_dose1_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.857421875 | 0.564453125 [0.51953125, 0.607421875] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([390], []) |
| dose_dose1_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.90234375 | 0.54296875 [0.501904297, 0.589892578] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([341], []) |
| dose_dose1_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.873046875 | 0.603515625 [0.55859375, 0.65234375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([275], []) |
| dose_dose1_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.998046875 | 0.07421875 [0.05078125, 0.099609375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.98828125 | 0.064453125 [0.04296875, 0.087890625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.951171875 | 0.021484375 [-0.005859375, 0.048828125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.953125 | 0.01953125 [-0.00200195312, 0.041015625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.9765625 | 0.064453125 [0.037109375, 0.091796875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.955078125 | 0.3984375 [0.357421875, 0.441455078] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.8828125 | 0.279296875 [0.232421875, 0.32421875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.869140625 | 0.302734375 [0.261669922, 0.347705078] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.91015625 | 0.2890625 [0.24609375, 0.330126953] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.908203125 | 0.263671875 [0.21875, 0.30859375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / linear / category3 / 1 | 0.7734375 / 0.99609375 | 0.22265625 [0.187451172, 0.2578125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([133], []) / True ([74], []) |
| dose_dose1_original_seed2 | upper / linear / category3 / 2 | 0.80078125 / 0.953125 | 0.15234375 [0.115234375, 0.1875] | 0.90625 / 0.82421875 / 1 | True ([126], []) / True ([106], []) |
| dose_dose1_original_seed2 | upper / linear / category3 / 3 | 0.771484375 / 0.88671875 | 0.115234375 [0.078125, 0.158203125] | 0.9296875 / 0.87109375 / 1 | True ([126], []) / True ([134], []) |
| dose_dose1_original_seed2 | upper / linear / category3 / 4 | 0.84375 / 0.93359375 | 0.08984375 [0.052734375, 0.126953125] | 0.93359375 / 0.875 / 1 | True ([143], []) / True ([135], []) |
| dose_dose1_original_seed2 | upper / linear / category3 / 5 | 0.7421875 / 0.947265625 | 0.205078125 [0.166015625, 0.24609375] | 0.927734375 / 0.86328125 / 1 | True ([121], []) / True ([125], []) |
| dose_dose1_original_seed2 | upper / linear / sum36 / 1 | 0.267578125 / 0.90625 | 0.638671875 [0.597607422, 0.68359375] | 0.33984375 / 0.169921875 / 1 | True ([461], []) / True ([852], []) |
| dose_dose1_original_seed2 | upper / linear / sum36 / 2 | 0.353515625 / 0.740234375 | 0.38671875 [0.333984375, 0.4375] | 0.35546875 / 0.16015625 / 1 | True ([549], []) / True ([463], []) |
| dose_dose1_original_seed2 | upper / linear / sum36 / 3 | 0.30859375 / 0.69921875 | 0.390625 [0.33984375, 0.4375] | 0.40625 / 0.216796875 / 1 | True ([456], []) / True ([701], []) |
| dose_dose1_original_seed2 | upper / linear / sum36 / 4 | 0.380859375 / 0.82421875 | 0.443359375 [0.396484375, 0.4921875] | 0.375 / 0.19140625 / 0.998046875 | True ([569], []) / True ([340], []) |
| dose_dose1_original_seed2 | upper / linear / sum36 / 5 | 0.287109375 / 0.765625 | 0.478515625 [0.427685547, 0.529296875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([576], []) / True ([475], []) |
| dose_dose1_original_seed2 | upper / mlp64 / category3 / 1 | 0.908203125 / 0.98828125 | 0.080078125 [0.052734375, 0.107421875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / category3 / 2 | 0.916015625 / 0.978515625 | 0.0625 [0.041015625, 0.087890625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / category3 / 3 | 0.916015625 / 0.953125 | 0.037109375 [0.0155761719, 0.0625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / category3 / 4 | 0.94140625 / 0.95703125 | 0.015625 [-0.00390625, 0.037109375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / category3 / 5 | 0.90234375 / 0.97265625 | 0.0703125 [0.044921875, 0.09765625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / sum36 / 1 | 0.513671875 / 0.931640625 | 0.41796875 [0.373046875, 0.462890625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / sum36 / 2 | 0.599609375 / 0.84375 | 0.244140625 [0.199169922, 0.287158203] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / sum36 / 3 | 0.576171875 / 0.80078125 | 0.224609375 [0.181591797, 0.271484375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / sum36 / 4 | 0.640625 / 0.876953125 | 0.236328125 [0.195263672, 0.279296875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| dose_dose1_original_seed2 | upper / mlp64 / sum36 / 5 | 0.634765625 / 0.853515625 | 0.21875 [0.17578125, 0.261767578] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| rarity_uniform_equal_seed2 | 0 | 1.0997026 | 0 | 0.0265623486 | 0 |
| rarity_uniform_equal_seed2 | 1000 | 1.08439505 | 0 | 2.08760651e-05 | 0 |
| rarity_uniform_equal_seed2 | 2000 | 1.08031869 | 0 | 6.71052083e-05 | 0 |
| rarity_uniform_equal_seed2 | 5000 | 1.07717252 | 0 | 2.42738406e-05 | 0 |
| rarity_uniform_equal_seed2 | 10000 | 1.08139765 | 0 | 3.51278999e-05 | 0 |
| rarity_uniform_equal_seed2 | 15000 | 1.08397639 | 0 | 0.000111015225 | 0 |
| rarity_uniform_equal_seed2 | 20000 | 1.07795656 | 0 | 3.89530277e-05 | 0 |
| rarity_uniform_original_seed2 | 0 | 1.09055185 | 0 | 0.0838733646 | 0 |
| rarity_uniform_original_seed2 | 1000 | 1.02808809 | 0 | 0.0020011176 | 0 |
| rarity_uniform_original_seed2 | 2000 | 1.05817652 | 0 | 0.00139650043 | 0 |
| rarity_uniform_original_seed2 | 5000 | 1.04873502 | 0 | 0.000674115571 | 0 |
| rarity_uniform_original_seed2 | 10000 | 1.0559504 | 0 | 0.000426274364 | 0 |
| rarity_uniform_original_seed2 | 15000 | 1.03420711 | 0 | 0.000262472113 | 0 |
| rarity_uniform_original_seed2 | 20000 | 1.0387516 | 0 | 0.000174531007 | 0 |
| dose_dose100_equal_seed2 | 0 | 1.0997026 | 3.62805605 | 0.0265623486 | 0 |
| dose_dose100_equal_seed2 | 1000 | 1.08432746 | 0.539304316 | 0.000107493626 | 0.174299161 |
| dose_dose100_equal_seed2 | 2000 | 1.08002973 | 0.348029882 | 9.24496806e-05 | 0.352649887 |
| dose_dose100_equal_seed2 | 5000 | 1.07698882 | 0.200004444 | 1.86944979e-05 | 0.568160426 |
| dose_dose100_equal_seed2 | 10000 | 1.08135509 | 0.113023318 | 3.79714437e-05 | 0.716676898 |
| dose_dose100_equal_seed2 | 15000 | 1.08400416 | 0.0851652846 | 0.000107516085 | 0.786290158 |
| dose_dose100_equal_seed2 | 20000 | 1.0779649 | 0.0730765089 | 4.09715277e-05 | 0.830570902 |
| dose_dose100_original_seed2 | 0 | 1.09055185 | 3.62528443 | 0.0838733646 | 0 |
| dose_dose100_original_seed2 | 1000 | 1.03058887 | 0.562485278 | 0.00776356281 | 0.179251074 |
| dose_dose100_original_seed2 | 2000 | 1.05904722 | 0.381356984 | 0.00425757987 | 0.330223041 |
| dose_dose100_original_seed2 | 5000 | 1.04878712 | 0.191128433 | 0.00227895132 | 0.595048087 |
| dose_dose100_original_seed2 | 10000 | 1.05556011 | 0.1083434 | 0.00154024111 | 0.747288725 |
| dose_dose100_original_seed2 | 15000 | 1.03482211 | 0.0784740299 | 0.00125417509 | 0.811786372 |
| dose_dose100_original_seed2 | 20000 | 1.04096019 | 0.0746310949 | 0.00123433675 | 0.840720278 |
| dose_dose10_equal_seed2 | 0 | 1.0997026 | 0.367085129 | 0.0265623486 | 0 |
| dose_dose10_equal_seed2 | 1000 | 1.08453226 | 0.0609319992 | 8.1052588e-05 | 0.0962144465 |
| dose_dose10_equal_seed2 | 2000 | 1.08006418 | 0.0422832556 | 0.000117850111 | 0.254307346 |
| dose_dose10_equal_seed2 | 5000 | 1.07705271 | 0.0299681574 | 2.75266028e-05 | 0.450869654 |
| dose_dose10_equal_seed2 | 10000 | 1.08144057 | 0.0184486136 | 3.54370229e-05 | 0.578555351 |
| dose_dose10_equal_seed2 | 15000 | 1.08398235 | 0.0150735285 | 0.000106390442 | 0.647022713 |
| dose_dose10_equal_seed2 | 20000 | 1.07798696 | 0.0126594435 | 4.31136918e-05 | 0.69056681 |
| dose_dose10_original_seed2 | 0 | 1.09055185 | 0.354395002 | 0.0838733646 | 0 |
| dose_dose10_original_seed2 | 1000 | 1.02738953 | 0.0593105219 | 0.0044680684 | 0.105504399 |
| dose_dose10_original_seed2 | 2000 | 1.05712616 | 0.0496199727 | 0.00311160809 | 0.220094127 |
| dose_dose10_original_seed2 | 5000 | 1.04770994 | 0.0289200209 | 0.00131305677 | 0.433190096 |
| dose_dose10_original_seed2 | 10000 | 1.05576253 | 0.0197845325 | 0.000986103281 | 0.57888275 |
| dose_dose10_original_seed2 | 15000 | 1.03399181 | 0.0146417934 | 0.000743956427 | 0.650460405 |
| dose_dose10_original_seed2 | 20000 | 1.03936625 | 0.0137653267 | 0.000686644649 | 0.704931451 |
| dose_dose1_equal_seed2 | 0 | 1.0997026 | 0.0340721533 | 0.0265623486 | 0 |
| dose_dose1_equal_seed2 | 1000 | 1.08452165 | 0.0114821233 | 0.000102870262 | 0.0259873133 |
| dose_dose1_equal_seed2 | 2000 | 1.08009577 | 0.0067971563 | 0.000127322949 | 0.123347657 |
| dose_dose1_equal_seed2 | 5000 | 1.07712555 | 0.00433246 | 2.8022472e-05 | 0.285041948 |
| dose_dose1_equal_seed2 | 10000 | 1.0814265 | 0.00389232533 | 3.23481968e-05 | 0.394679763 |
| dose_dose1_equal_seed2 | 15000 | 1.08397889 | 0.00439642603 | 0.000105601063 | 0.467403315 |
| dose_dose1_equal_seed2 | 20000 | 1.07798135 | 0.00266007567 | 4.27734074e-05 | 0.513648455 |
| dose_dose1_original_seed2 | 0 | 1.09055185 | 0.0272673629 | 0.0838733646 | 0 |
| dose_dose1_original_seed2 | 1000 | 1.02808416 | 0.00670790253 | 0.00227825781 | 0.00536116227 |
| dose_dose1_original_seed2 | 2000 | 1.05750489 | 0.00809145533 | 0.00165685863 | 0.0558624923 |
| dose_dose1_original_seed2 | 5000 | 1.04700017 | 0.00421456201 | 0.00086617859 | 0.209821977 |
| dose_dose1_original_seed2 | 10000 | 1.05541205 | 0.00239101145 | 0.000471592731 | 0.389154901 |
| dose_dose1_original_seed2 | 15000 | 1.03476763 | 0.00106922898 | 0.000314430991 | 0.459504809 |
| dose_dose1_original_seed2 | 20000 | 1.03872454 | 0.0021014621 | 0.000618522311 | 0.517577246 |

## erosion

### Seed 0 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 24435/24435, 24434/24435, 24433/24435, 24435/24435, 24434/24435 | 24431/24435 | 1505/1555 |
| erosion_a_plus_b_original_seed0 | B_INCOMPLETE | 0/24435; 0/24435; 0/24435; 0/24435 | 0/24435; 0/24435; 0/24435; 0/24435 | 0 / 0 of 101 | 24435/24435, 24435/24435, 24435/24435, 24435/24435, 24434/24435 | 24434/24435 | 1552/1555 |
| erosion_b_only_equal_seed0 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 9306/24435, 9306/24435, 9306/24435, 9306/24435, 9306/24435 | 0/24435 | 1/1555 |
| erosion_b_only_original_seed0 | B_INCOMPLETE | 32/24435; 34/24435; 29/24435; 37/24435 | 450/24435; 464/24435; 449/24435; 459/24435 | 1 / 3 of 101 | 11176/24435, 11170/24435, 11172/24435, 11186/24435, 11182/24435 | 10/24435 | 3/1555 |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | 39581042 | 39581042 / 1 | {'12': 190111, '13': 1493635, '23': 131282, '24': 3438039} | {'10': 189640, '16': 1494343, '20': 130786, '27': 3437884} | not applicable |
| erosion_a_plus_b_original_seed0 | 39584565 | 39584565 / 1 | {'12': 205614, '13': 1493253, '23': 131346, '24': 3148592} | {'10': 206076, '16': 1493767, '20': 131073, '27': 3148191} | not applicable |
| erosion_b_only_equal_seed0 | 39581042 | 0 / 0 | {'12': 190111, '13': 1493635, '23': 131282, '24': 3438039} | {'10': 189640, '16': 1494343, '20': 130786, '27': 3437884} | not applicable |
| erosion_b_only_original_seed0 | 39584565 | 0 / 0 | {'12': 205614, '13': 1493253, '23': 131346, '24': 3148592} | {'10': 206076, '16': 1493767, '20': 131073, '27': 3148191} | not applicable |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | 0.00278706616/0.00278766453 (n=32) | 0.00278756488/0.00278763473 (n=32) | 0.00278713158/0.00278761983 (n=64) | 0.00278693717/0.00278754532 (n=64) | 0.00278669992/0.00278748572 (n=64) | 0.0027863821/0.00278738141 (n=64) | 0.00278629363/0.00278717279 (n=64) | 0.00278591365/0.00278733671 (n=64) | 0.00278595975/0.00278690457 (n=64) | 0.00278541236/0.00278669596 (n=64) | 0.00278712809 / 0.00278766453 / True | 0.00278611023 / 0.00278748572 / True |
| erosion_a_plus_b_original_seed0 | 0.00116962148/0.00132296979 (n=32) | 0.00601489609/0.00792622566 (n=32) | 0.00329594559/0.0090803653 (n=64) | 0.00357877277/0.0108847618 (n=64) | 0.00407122902/0.0152886659 (n=64) | 0.00503408117/0.0184420794 (n=64) | 0.00770806766/0.0537997037 (n=64) | 0.0111021684/0.222364947 (n=64) | 0.00997878704/0.0723121762 (n=64) | 0.0192925686/0.252121478 (n=64) | 0.00348899238 / 0.0108847618 / True | 0.0095311503 / 0.252121478 / False |
| erosion_b_only_equal_seed0 | 0.00278626429/0.00278629363 (n=32) | 0.00278627733/0.00278630853 (n=32) | 0.00278627756/0.00278633833 (n=64) | 0.00278629619/0.00278636813 (n=64) | 0.0027863048/0.00278641284 (n=64) | 0.00278632017/0.00278639793 (n=64) | 0.00278632343/0.00278644264 (n=64) | 0.00278633949/0.00278650224 (n=64) | 0.00278636348/0.00278645754 (n=64) | 0.00278636464/0.00278650224 (n=64) | 0.00278628152 / 0.00278636813 / True | 0.002786336 / 0.00278650224 / True |
| erosion_b_only_original_seed0 | 0.000897687627/0.00110180676 (n=32) | 0.00471171364/0.00544990599 (n=32) | 0.00414157088/0.0100360513 (n=64) | 0.00477317814/0.0108106285 (n=64) | 0.00711835455/0.14469105 (n=64) | 0.00570304936/0.0289816707 (n=64) | 0.00910775061/0.249425426 (n=64) | 0.00484777126/0.0115803033 (n=64) | 0.00472038682/0.00804032385 (n=64) | 0.00488333835/0.01044707 (n=64) | 0.00390648322 / 0.0108106285 / True | 0.00606344182 / 0.249425426 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | 3.57354789e-05 / 3.57237666e-05 (n=20282) | not recorded / 6.32833689e-07 | none | 1.93715096e-07 / True | 0 / True |
| erosion_a_plus_b_original_seed0 | 5.04228755e-05 / 3.82890257e-05 (n=24185) | 0.999217173 / 0.248288944 | law_TV | 0.000676825643 / True | 0 / True |
| erosion_b_only_equal_seed0 | 3.57143513e-05 / 3.57090702e-05 (n=20282) | not recorded / 4.33064997e-08 | none | 8.94069672e-08 / True | 0 / True |
| erosion_b_only_original_seed0 | 0.000152459468 / 0.000134662027 (n=24185) | 0.998842746 / 0.249066621 | law_TV, swaps | 0.0170080587 / True | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | A_swap_effect | 64 | 4.41912562e-07 / 2.71201134e-06 |
| erosion_a_plus_b_equal_seed0 | A_swap_exact_row | 64 | 0.0027873537 / 0.00278763473 |
| erosion_a_plus_b_equal_seed0 | both_swap_exact_row | 64 | 0.00278730853 / 0.00278766453 |
| erosion_a_plus_b_equal_seed0 | neutral_A_swap_stability | 128 | 1.94297172e-07 / 1.04308128e-06 |
| erosion_a_plus_b_equal_seed0 | neutral_N | 192 | 0.00278701594 / 0.00278760493 |
| erosion_a_plus_b_equal_seed0 | neutral_raw_swap_stability | 128 | 2.65426934e-08 / 1.49011612e-07 |
| erosion_a_plus_b_equal_seed0 | raw_swap_effect | 64 | 7.03148544e-08 / 1.31130219e-06 |
| erosion_a_plus_b_equal_seed0 | raw_swap_exact_row | 64 | 0.0027873537 / 0.00278763473 |
| erosion_a_plus_b_equal_seed0 | raw_swap_stability | 128 | 0.00139371201 / 0.00278763473 |
| erosion_a_plus_b_equal_seed0 | reset_L | 160 | 0.0027866846 / 0.00278763473 |
| erosion_a_plus_b_equal_seed0 | same_category_substitution | 128 | 1.93133019e-07 / 1.04308128e-06 |
| erosion_a_plus_b_equal_seed0 | set_H | 160 | 0.00278717326 / 0.00278766453 |
| erosion_a_plus_b_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00278709061 / 0.00278760493 |
| erosion_a_plus_b_original_seed0 | A_swap_effect | 64 | 0.128331607 / 0.243355975 |
| erosion_a_plus_b_original_seed0 | A_swap_exact_row | 64 | 0.127535596 / 0.245143875 |
| erosion_a_plus_b_original_seed0 | both_swap_exact_row | 64 | 0.00334368646 / 0.00676579773 |
| erosion_a_plus_b_original_seed0 | neutral_A_swap_stability | 128 | 0.000730814354 / 0.0112021565 |
| erosion_a_plus_b_original_seed0 | neutral_N | 192 | 0.00331920952 / 0.0122857988 |
| erosion_a_plus_b_original_seed0 | neutral_raw_swap_stability | 128 | 0.00138583669 / 0.0310759693 |
| erosion_a_plus_b_original_seed0 | raw_swap_effect | 64 | 0.124809826 / 0.243116654 |
| erosion_a_plus_b_original_seed0 | raw_swap_exact_row | 64 | 0.130993182 / 0.247346327 |
| erosion_a_plus_b_original_seed0 | raw_swap_stability | 128 | 0.126172711 / 0.245143875 |
| erosion_a_plus_b_original_seed0 | reset_L | 160 | 0.00127283088 / 0.00233361125 |
| erosion_a_plus_b_original_seed0 | same_category_substitution | 128 | 0.000612186501 / 0.00860536098 |
| erosion_a_plus_b_original_seed0 | set_H | 160 | 0.00539358025 / 0.00680731237 |
| erosion_a_plus_b_original_seed0 | upper_state_exchange_same_N | 64 | 0.00311082008 / 0.00648146868 |
| erosion_b_only_equal_seed0 | A_swap_effect | 64 | 0 / 0 |
| erosion_b_only_equal_seed0 | A_swap_exact_row | 64 | 0.00278626615 / 0.00278629363 |
| erosion_b_only_equal_seed0 | both_swap_exact_row | 64 | 0.00278626615 / 0.00278629363 |
| erosion_b_only_equal_seed0 | neutral_A_swap_stability | 128 | 0 / 0 |
| erosion_b_only_equal_seed0 | neutral_N | 192 | 0.00278628214 / 0.00278636813 |
| erosion_b_only_equal_seed0 | neutral_raw_swap_stability | 128 | 2.50292942e-08 / 7.4505806e-08 |
| erosion_b_only_equal_seed0 | raw_swap_effect | 64 | 3.16649675e-08 / 8.94069672e-08 |
| erosion_b_only_equal_seed0 | raw_swap_exact_row | 64 | 0.00278626615 / 0.00278629363 |
| erosion_b_only_equal_seed0 | raw_swap_stability | 128 | 0.00139314891 / 0.00278629363 |
| erosion_b_only_equal_seed0 | reset_L | 160 | 0.0027862669 / 0.00278636813 |
| erosion_b_only_equal_seed0 | same_category_substitution | 128 | 2.50292942e-08 / 7.4505806e-08 |
| erosion_b_only_equal_seed0 | set_H | 160 | 0.00278629092 / 0.00278636813 |
| erosion_b_only_equal_seed0 | upper_state_exchange_same_N | 64 | 0.00278627826 / 0.00278632343 |
| erosion_b_only_original_seed0 | A_swap_effect | 64 | 0.000516215106 / 0.00480796397 |
| erosion_b_only_original_seed0 | A_swap_exact_row | 64 | 0.249627559 / 0.251433216 |
| erosion_b_only_original_seed0 | both_swap_exact_row | 64 | 0.00273273746 / 0.0050881952 |
| erosion_b_only_original_seed0 | neutral_A_swap_stability | 128 | 0.00080912374 / 0.0191208273 |
| erosion_b_only_original_seed0 | neutral_N | 192 | 0.00440403904 / 0.0312040001 |
| erosion_b_only_original_seed0 | neutral_raw_swap_stability | 128 | 0.00240048522 / 0.0531919301 |
| erosion_b_only_original_seed0 | raw_swap_effect | 64 | 0.248826318 / 0.249552995 |
| erosion_b_only_original_seed0 | raw_swap_exact_row | 64 | 0.00313732121 / 0.00946933031 |
| erosion_b_only_original_seed0 | raw_swap_stability | 128 | 0.249226939 / 0.251433216 |
| erosion_b_only_original_seed0 | reset_L | 160 | 0.00348996455 / 0.0574328899 |
| erosion_b_only_original_seed0 | same_category_substitution | 128 | 0.00176649244 / 0.0261207372 |
| erosion_b_only_original_seed0 | set_H | 160 | 0.00449406654 / 0.00517913699 |
| erosion_b_only_original_seed0 | upper_state_exchange_same_N | 64 | 0.00420623668 / 0.0188694447 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.8125 | 0.046875 [0.00190429688, 0.08984375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([89], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.78515625 | 0.005859375 [-0.037109375, 0.0508300781] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([75], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.681640625 | -0.091796875 [-0.136767578, -0.046875] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([63], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.80859375 | 0.0078125 [-0.0352050781, 0.0508300781] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([73], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.705078125 | -0.091796875 [-0.134765625, -0.05078125] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([60], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.453125 | 0.08984375 [0.037109375, 0.142578125] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([325], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.408203125 | 0.083984375 [0.03125, 0.138720703] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([249], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.2734375 | 0.037109375 [-0.009765625, 0.0859375] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([321], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.326171875 | 0.02734375 [-0.0234375, 0.078125] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([418], []) |
| erosion_a_plus_b_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.25390625 | -0.04296875 [-0.09375, 0.00390625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([365], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.921875 | 0.013671875 [-0.01171875, 0.041015625] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.900390625 | -0.017578125 [-0.04296875, 0.00590820312] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.92578125 | 0 [-0.01953125, 0.01953125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.931640625 | 0.009765625 [-0.01171875, 0.03125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.919921875 | -0.015625 [-0.037109375, 0.005859375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.6015625 | 0.041015625 [-0.005859375, 0.08984375] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.576171875 | 0.013671875 [-0.037109375, 0.064453125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.54296875 | -0.0859375 [-0.1328125, -0.037109375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.623046875 | -0.001953125 [-0.05078125, 0.0469238281] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.5234375 | -0.03515625 [-0.0859375, 0.01953125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / category3 / 1 | 0.8515625 / 0.671875 | -0.1796875 [-0.22265625, -0.130859375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([128], []) / True ([111], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / category3 / 2 | 0.845703125 / 0.609375 | -0.236328125 [-0.28515625, -0.185546875] | 0.90625 / 0.82421875 / 1 | True ([121], []) / True ([131], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / category3 / 3 | 0.91015625 / 0.5625 | -0.34765625 [-0.3984375, -0.3046875] | 0.9296875 / 0.87109375 / 1 | True ([124], []) / True ([118], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / category3 / 4 | 0.9453125 / 0.669921875 | -0.275390625 [-0.322265625, -0.232421875] | 0.93359375 / 0.875 / 1 | True ([106], []) / True ([153], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / category3 / 5 | 0.8828125 / 0.712890625 | -0.169921875 [-0.216796875, -0.128857422] | 0.927734375 / 0.86328125 / 1 | True ([109], []) / True ([125], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / sum36 / 1 | 0.88671875 / 0.408203125 | -0.478515625 [-0.529296875, -0.431591797] | 0.33984375 / 0.169921875 / 1 | True ([151], []) / True ([269], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / sum36 / 2 | 0.904296875 / 0.2890625 | -0.615234375 [-0.666015625, -0.574169922] | 0.35546875 / 0.16015625 / 1 | True ([139], []) / True ([214], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / sum36 / 3 | 0.86328125 / 0.30859375 | -0.5546875 [-0.603515625, -0.50390625] | 0.40625 / 0.216796875 / 1 | True ([158], []) / True ([211], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / sum36 / 4 | 0.86328125 / 0.310546875 | -0.552734375 [-0.603515625, -0.505859375] | 0.375 / 0.19140625 / 0.998046875 | True ([164], []) / True ([229], []) |
| erosion_a_plus_b_equal_seed0 | upper / linear / sum36 / 5 | 0.884765625 / 0.26953125 | -0.615234375 [-0.66015625, -0.564453125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([135], []) / True ([206], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / category3 / 1 | 0.951171875 / 0.921875 | -0.029296875 [-0.048828125, -0.009765625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / category3 / 2 | 0.955078125 / 0.919921875 | -0.03515625 [-0.056640625, -0.01171875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / category3 / 3 | 0.96875 / 0.9296875 | -0.0390625 [-0.05859375, -0.021484375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / category3 / 4 | 0.962890625 / 0.935546875 | -0.02734375 [-0.046875, -0.009765625] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / category3 / 5 | 0.953125 / 0.9296875 | -0.0234375 [-0.044921875, -0.001953125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.892578125 / 0.560546875 | -0.33203125 [-0.375048828, -0.283203125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.853515625 / 0.578125 | -0.275390625 [-0.32421875, -0.23046875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.8828125 / 0.51171875 | -0.37109375 [-0.421875, -0.330078125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.8828125 / 0.546875 | -0.3359375 [-0.384765625, -0.287060547] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.884765625 / 0.5703125 | -0.314453125 [-0.357421875, -0.26953125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.962890625 | 0.197265625 [0.15625, 0.236328125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([118], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.791015625 | 0.01171875 [-0.03125, 0.05859375] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([91], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.69140625 | -0.08203125 [-0.130859375, -0.033203125] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([63], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.845703125 | 0.044921875 [0.009765625, 0.083984375] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([112], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.87109375 | 0.07421875 [0.0390136719, 0.107421875] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([98], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.83203125 | 0.46875 [0.41796875, 0.513671875] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([1375], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.33203125 | 0.0078125 [-0.037109375, 0.0547363281] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([168], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.1328125 | -0.103515625 [-0.146484375, -0.056640625] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([210], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.466796875 | 0.16796875 [0.113232422, 0.224609375] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([367], []) |
| erosion_a_plus_b_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.412109375 | 0.115234375 [0.05859375, 0.169921875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([345], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.984375 | 0.076171875 [0.052734375, 0.101611328] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.931640625 | 0.013671875 [-0.009765625, 0.03515625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.927734375 | 0.001953125 [-0.017578125, 0.021484375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.95703125 | 0.03515625 [0.009765625, 0.05859375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.9453125 | 0.009765625 [-0.01171875, 0.03125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.90625 | 0.345703125 [0.302685547, 0.39453125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.583984375 | 0.021484375 [-0.0293457031, 0.0703125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.5 | -0.12890625 [-0.1796875, -0.08203125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.734375 | 0.109375 [0.05859375, 0.160205078] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.681640625 | 0.123046875 [0.07421875, 0.175830078] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / category3 / 1 | 0.8515625 / 1 | 0.1484375 [0.12109375, 0.181640625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([128], []) / True ([27], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / category3 / 2 | 0.845703125 / 0.732421875 | -0.11328125 [-0.15625, -0.0625] | 0.90625 / 0.82421875 / 1 | True ([121], []) / True ([126], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / category3 / 3 | 0.91015625 / 0.7421875 | -0.16796875 [-0.21484375, -0.123046875] | 0.9296875 / 0.87109375 / 1 | True ([124], []) / True ([139], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / category3 / 4 | 0.9453125 / 0.572265625 | -0.373046875 [-0.419921875, -0.32421875] | 0.93359375 / 0.875 / 1 | True ([106], []) / True ([135], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / category3 / 5 | 0.8828125 / 0.826171875 | -0.056640625 [-0.09765625, -0.01953125] | 0.927734375 / 0.86328125 / 1 | True ([109], []) / True ([119], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / sum36 / 1 | 0.88671875 / 0.78125 | -0.10546875 [-0.1484375, -0.0625] | 0.33984375 / 0.169921875 / 1 | True ([151], []) / True ([457], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / sum36 / 2 | 0.904296875 / 0.349609375 | -0.5546875 [-0.60546875, -0.505859375] | 0.35546875 / 0.16015625 / 1 | True ([139], []) / True ([239], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / sum36 / 3 | 0.86328125 / 0.328125 | -0.53515625 [-0.580078125, -0.486328125] | 0.40625 / 0.216796875 / 1 | True ([158], []) / True ([201], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / sum36 / 4 | 0.86328125 / 0.30078125 | -0.5625 [-0.611328125, -0.515576172] | 0.375 / 0.19140625 / 0.998046875 | True ([164], []) / True ([191], []) |
| erosion_a_plus_b_original_seed0 | upper / linear / sum36 / 5 | 0.884765625 / 0.32421875 | -0.560546875 [-0.605517578, -0.515576172] | 0.404296875 / 0.189453125 / 0.998046875 | True ([135], []) / True ([208], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / category3 / 1 | 0.951171875 / 1 | 0.048828125 [0.03125, 0.068359375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / category3 / 2 | 0.955078125 / 0.91796875 | -0.037109375 [-0.05859375, -0.013671875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / category3 / 3 | 0.96875 / 0.9375 | -0.03125 [-0.05078125, -0.013671875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / category3 / 4 | 0.962890625 / 0.9296875 | -0.033203125 [-0.052734375, -0.013671875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / category3 / 5 | 0.953125 / 0.9375 | -0.015625 [-0.037109375, 0.0078125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / sum36 / 1 | 0.892578125 / 0.814453125 | -0.078125 [-0.115234375, -0.037109375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / sum36 / 2 | 0.853515625 / 0.61328125 | -0.240234375 [-0.287109375, -0.193359375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / sum36 / 3 | 0.8828125 / 0.61328125 | -0.26953125 [-0.318359375, -0.224609375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / sum36 / 4 | 0.8828125 / 0.576171875 | -0.306640625 [-0.353515625, -0.2578125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed0 | upper / mlp64 / sum36 / 5 | 0.884765625 / 0.595703125 | -0.2890625 [-0.3359375, -0.244091797] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.810546875 | 0.044921875 [0, 0.087890625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([99], []) |
| erosion_b_only_equal_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.7578125 | -0.021484375 [-0.0664550781, 0.025390625] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([81], []) |
| erosion_b_only_equal_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.841796875 | 0.068359375 [0.029296875, 0.109375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([91], []) |
| erosion_b_only_equal_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.859375 | 0.05859375 [0.021484375, 0.095703125] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([95], []) |
| erosion_b_only_equal_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.859375 | 0.0625 [0.02734375, 0.099609375] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([72], []) |
| erosion_b_only_equal_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.455078125 | 0.091796875 [0.0390136719, 0.142578125] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([310], []) |
| erosion_b_only_equal_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.44140625 | 0.1171875 [0.064453125, 0.169921875] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([355], []) |
| erosion_b_only_equal_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.4375 | 0.201171875 [0.1484375, 0.251953125] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([346], []) |
| erosion_b_only_equal_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.490234375 | 0.19140625 [0.140625, 0.238330078] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([391], []) |
| erosion_b_only_equal_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.4921875 | 0.1953125 [0.13671875, 0.24609375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([304], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.93359375 | 0.025390625 [0.001953125, 0.052734375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.90625 | -0.01171875 [-0.03515625, 0.009765625] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.951171875 | 0.025390625 [0.009765625, 0.0410644531] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.94921875 | 0.02734375 [0.005859375, 0.046875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.94921875 | 0.013671875 [-0.009765625, 0.03515625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.63671875 | 0.076171875 [0.029296875, 0.123046875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.68359375 | 0.12109375 [0.07421875, 0.171875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.69140625 | 0.0625 [0.0214355469, 0.1015625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.70703125 | 0.08203125 [0.0331542969, 0.130859375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.732421875 | 0.173828125 [0.12109375, 0.224658203] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / linear / category3 / 1 | 0.8515625 / 0.826171875 | -0.025390625 [-0.0684082031, 0.017578125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([128], []) / True ([130], []) |
| erosion_b_only_equal_seed0 | upper / linear / category3 / 2 | 0.845703125 / 0.775390625 | -0.0703125 [-0.115234375, -0.029296875] | 0.90625 / 0.82421875 / 1 | True ([121], []) / True ([156], []) |
| erosion_b_only_equal_seed0 | upper / linear / category3 / 3 | 0.91015625 / 0.830078125 | -0.080078125 [-0.119140625, -0.044921875] | 0.9296875 / 0.87109375 / 1 | True ([124], []) / True ([122], []) |
| erosion_b_only_equal_seed0 | upper / linear / category3 / 4 | 0.9453125 / 0.857421875 | -0.087890625 [-0.123046875, -0.0546875] | 0.93359375 / 0.875 / 1 | True ([106], []) / True ([182], []) |
| erosion_b_only_equal_seed0 | upper / linear / category3 / 5 | 0.8828125 / 0.859375 | -0.0234375 [-0.060546875, 0.01171875] | 0.927734375 / 0.86328125 / 1 | True ([109], []) / True ([149], []) |
| erosion_b_only_equal_seed0 | upper / linear / sum36 / 1 | 0.88671875 / 0.466796875 | -0.419921875 [-0.46875, -0.375] | 0.33984375 / 0.169921875 / 1 | True ([151], []) / True ([562], []) |
| erosion_b_only_equal_seed0 | upper / linear / sum36 / 2 | 0.904296875 / 0.44921875 | -0.455078125 [-0.50390625, -0.41015625] | 0.35546875 / 0.16015625 / 1 | True ([139], []) / True ([532], []) |
| erosion_b_only_equal_seed0 | upper / linear / sum36 / 3 | 0.86328125 / 0.41796875 | -0.4453125 [-0.494189453, -0.396435547] | 0.40625 / 0.216796875 / 1 | True ([158], []) / True ([434], []) |
| erosion_b_only_equal_seed0 | upper / linear / sum36 / 4 | 0.86328125 / 0.490234375 | -0.373046875 [-0.425830078, -0.3203125] | 0.375 / 0.19140625 / 0.998046875 | True ([164], []) / True ([636], []) |
| erosion_b_only_equal_seed0 | upper / linear / sum36 / 5 | 0.884765625 / 0.478515625 | -0.40625 [-0.455078125, -0.35546875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([135], []) / True ([651], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / category3 / 1 | 0.951171875 / 0.93359375 | -0.017578125 [-0.03515625, 0.001953125] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / category3 / 2 | 0.955078125 / 0.89453125 | -0.060546875 [-0.087890625, -0.03515625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / category3 / 3 | 0.96875 / 0.943359375 | -0.025390625 [-0.0430175781, -0.0078125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / category3 / 4 | 0.962890625 / 0.94140625 | -0.021484375 [-0.041015625, -0.00385742188] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / category3 / 5 | 0.953125 / 0.947265625 | -0.005859375 [-0.02734375, 0.015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / sum36 / 1 | 0.892578125 / 0.578125 | -0.314453125 [-0.361328125, -0.26953125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / sum36 / 2 | 0.853515625 / 0.64453125 | -0.208984375 [-0.25390625, -0.165966797] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / sum36 / 3 | 0.8828125 / 0.619140625 | -0.263671875 [-0.30859375, -0.220703125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / sum36 / 4 | 0.8828125 / 0.6796875 | -0.203125 [-0.244140625, -0.16015625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed0 | upper / mlp64 / sum36 / 5 | 0.884765625 / 0.708984375 | -0.17578125 [-0.214892578, -0.13671875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / linear / category3 / 1 | 0.765625 / 0.998046875 | 0.232421875 [0.193359375, 0.267626953] | 0.919921875 / 0.8515625 / 0.998046875 | True ([87], []) / True ([117], []) |
| erosion_b_only_original_seed0 | raw / linear / category3 / 2 | 0.779296875 / 0.583984375 | -0.1953125 [-0.25, -0.142529297] | 0.90625 / 0.82421875 / 1 | True ([84], []) / True ([91], []) |
| erosion_b_only_original_seed0 | raw / linear / category3 / 3 | 0.7734375 / 0.51953125 | -0.25390625 [-0.30859375, -0.19921875] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([91], []) |
| erosion_b_only_original_seed0 | raw / linear / category3 / 4 | 0.80078125 / 0.560546875 | -0.240234375 [-0.2890625, -0.189453125] | 0.93359375 / 0.875 / 1 | True ([52], []) / True ([85], []) |
| erosion_b_only_original_seed0 | raw / linear / category3 / 5 | 0.796875 / 0.658203125 | -0.138671875 [-0.1875, -0.08984375] | 0.927734375 / 0.86328125 / 1 | True ([85], []) / True ([98], []) |
| erosion_b_only_original_seed0 | raw / linear / sum36 / 1 | 0.36328125 / 0.978515625 | 0.615234375 [0.5703125, 0.65625] | 0.33984375 / 0.169921875 / 1 | True ([331], []) / True ([600], []) |
| erosion_b_only_original_seed0 | raw / linear / sum36 / 2 | 0.32421875 / 0.087890625 | -0.236328125 [-0.277392578, -0.189404297] | 0.35546875 / 0.16015625 / 1 | True ([346], []) / True ([235], []) |
| erosion_b_only_original_seed0 | raw / linear / sum36 / 3 | 0.236328125 / 0.064453125 | -0.171875 [-0.212890625, -0.130810547] | 0.40625 / 0.216796875 / 1 | True ([345], []) / True ([290], []) |
| erosion_b_only_original_seed0 | raw / linear / sum36 / 4 | 0.298828125 / 0.076171875 | -0.22265625 [-0.263671875, -0.1796875] | 0.375 / 0.19140625 / 0.998046875 | True ([359], []) / True ([259], []) |
| erosion_b_only_original_seed0 | raw / linear / sum36 / 5 | 0.296875 / 0.09375 | -0.203125 [-0.248046875, -0.158203125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([458], []) / True ([218], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.06640625, 0.115234375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / category3 / 2 | 0.91796875 / 0.908203125 | -0.009765625 [-0.0332519531, 0.013671875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / category3 / 3 | 0.92578125 / 0.931640625 | 0.005859375 [-0.0078125, 0.0195800781] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / category3 / 4 | 0.921875 / 0.93359375 | 0.01171875 [-0.00390625, 0.029296875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / category3 / 5 | 0.935546875 / 0.92578125 | -0.009765625 [-0.029296875, 0.01171875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / sum36 / 1 | 0.560546875 / 0.986328125 | 0.42578125 [0.384716797, 0.46875] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / sum36 / 2 | 0.5625 / 0.376953125 | -0.185546875 [-0.232421875, -0.140576172] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / sum36 / 3 | 0.62890625 / 0.384765625 | -0.244140625 [-0.291015625, -0.19921875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / sum36 / 4 | 0.625 / 0.337890625 | -0.287109375 [-0.33984375, -0.236328125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | raw / mlp64 / sum36 / 5 | 0.55859375 / 0.431640625 | -0.126953125 [-0.171923828, -0.072265625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / linear / category3 / 1 | 0.8515625 / 1 | 0.1484375 [0.12109375, 0.181640625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([128], []) / True ([126], []) |
| erosion_b_only_original_seed0 | upper / linear / category3 / 2 | 0.845703125 / 0.888671875 | 0.04296875 [0.005859375, 0.080078125] | 0.90625 / 0.82421875 / 1 | True ([121], []) / True ([113], []) |
| erosion_b_only_original_seed0 | upper / linear / category3 / 3 | 0.91015625 / 0.87890625 | -0.03125 [-0.068359375, 0.005859375] | 0.9296875 / 0.87109375 / 1 | True ([124], []) / True ([196], []) |
| erosion_b_only_original_seed0 | upper / linear / category3 / 4 | 0.9453125 / 0.904296875 | -0.041015625 [-0.0703125, -0.009765625] | 0.93359375 / 0.875 / 1 | True ([106], []) / True ([160], []) |
| erosion_b_only_original_seed0 | upper / linear / category3 / 5 | 0.8828125 / 0.876953125 | -0.005859375 [-0.046875, 0.03125] | 0.927734375 / 0.86328125 / 1 | True ([109], []) / True ([138], []) |
| erosion_b_only_original_seed0 | upper / linear / sum36 / 1 | 0.88671875 / 0.9375 | 0.05078125 [0.01953125, 0.083984375] | 0.33984375 / 0.169921875 / 1 | True ([151], []) / True ([299], []) |
| erosion_b_only_original_seed0 | upper / linear / sum36 / 2 | 0.904296875 / 0.3125 | -0.591796875 [-0.63671875, -0.546875] | 0.35546875 / 0.16015625 / 1 | True ([139], []) / True ([378], []) |
| erosion_b_only_original_seed0 | upper / linear / sum36 / 3 | 0.86328125 / 0.36328125 | -0.5 [-0.552734375, -0.443359375] | 0.40625 / 0.216796875 / 1 | True ([158], []) / True ([1707], []) |
| erosion_b_only_original_seed0 | upper / linear / sum36 / 4 | 0.86328125 / 0.404296875 | -0.458984375 [-0.509765625, -0.40625] | 0.375 / 0.19140625 / 0.998046875 | True ([164], []) / True ([344], []) |
| erosion_b_only_original_seed0 | upper / linear / sum36 / 5 | 0.884765625 / 0.279296875 | -0.60546875 [-0.654296875, -0.556640625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([135], []) / True ([246], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / category3 / 1 | 0.951171875 / 1 | 0.048828125 [0.03125, 0.068359375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / category3 / 2 | 0.955078125 / 0.904296875 | -0.05078125 [-0.076171875, -0.025390625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / category3 / 3 | 0.96875 / 0.923828125 | -0.044921875 [-0.068359375, -0.0234375] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / category3 / 4 | 0.962890625 / 0.931640625 | -0.03125 [-0.05078125, -0.01171875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / category3 / 5 | 0.953125 / 0.927734375 | -0.025390625 [-0.046875, -0.001953125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / sum36 / 1 | 0.892578125 / 0.96875 | 0.076171875 [0.05078125, 0.103515625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / sum36 / 2 | 0.853515625 / 0.42578125 | -0.427734375 [-0.47265625, -0.3828125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / sum36 / 3 | 0.8828125 / 0.474609375 | -0.408203125 [-0.453125, -0.365234375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / sum36 / 4 | 0.8828125 / 0.462890625 | -0.419921875 [-0.46484375, -0.37109375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed0 | upper / mlp64 / sum36 / 5 | 0.884765625 / 0.455078125 | -0.4296875 [-0.472705078, -0.38671875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | 0 | 1.09241438 | 0.0468969084 | 0.0199186955 | 1 |
| erosion_a_plus_b_equal_seed0 | 1000 | 1.08638668 | 0.000969681889 | 4.65552588e-05 | 1 |
| erosion_a_plus_b_equal_seed0 | 2000 | 1.08388889 | 0.000320732361 | 0.000414020514 | 1 |
| erosion_a_plus_b_equal_seed0 | 5000 | 1.0816654 | 4.44496363e-05 | 1.65409739e-05 | 1 |
| erosion_a_plus_b_equal_seed0 | 10000 | 1.07645953 | 2.80567792e-06 | 4.70316991e-05 | 1 |
| erosion_a_plus_b_equal_seed0 | 15000 | 1.08152926 | 2.12260815e-07 | 7.51624281e-08 | 1 |
| erosion_a_plus_b_equal_seed0 | 20000 | 1.08533263 | 0.00115581206 | 3.57354789e-05 | 0.9998363 |
| erosion_a_plus_b_original_seed0 | 0 | 1.09882939 | 0.0476898439 | 0.0837887374 | 1 |
| erosion_a_plus_b_original_seed0 | 1000 | 1.03907132 | 0.000954906805 | 0.000318464644 | 1 |
| erosion_a_plus_b_original_seed0 | 2000 | 1.04276514 | 0.000314865552 | 0.000127272445 | 1 |
| erosion_a_plus_b_original_seed0 | 5000 | 1.03880095 | 4.02362784e-05 | 0.000195004461 | 1 |
| erosion_a_plus_b_original_seed0 | 10000 | 1.03390467 | 2.46024547e-06 | 0.000108525348 | 1 |
| erosion_a_plus_b_original_seed0 | 15000 | 1.03743672 | 1.65172636e-07 | 6.72599806e-05 | 1 |
| erosion_a_plus_b_original_seed0 | 20000 | 1.03338313 | 0.000154460024 | 5.04228755e-05 | 0.999959075 |
| erosion_b_only_equal_seed0 | 0 | 1.09241438 | 0 | 0.0199186955 | 1 |
| erosion_b_only_equal_seed0 | 1000 | 1.0864408 | 0 | 4.66182168e-05 | 0.000613873542 |
| erosion_b_only_equal_seed0 | 2000 | 1.08379841 | 0 | 0.000534641998 | 0.000613873542 |
| erosion_b_only_equal_seed0 | 5000 | 1.08158541 | 0 | 5.75505524e-06 | 0.000613873542 |
| erosion_b_only_equal_seed0 | 10000 | 1.07647145 | 0 | 3.7403823e-05 | 0 |
| erosion_b_only_equal_seed0 | 15000 | 1.08152938 | 0 | 7.37271715e-08 | 0 |
| erosion_b_only_equal_seed0 | 20000 | 1.08533275 | 0 | 3.57143513e-05 | 0 |
| erosion_b_only_original_seed0 | 0 | 1.09882939 | 0 | 0.0837887374 | 1 |
| erosion_b_only_original_seed0 | 1000 | 1.04006469 | 0 | 0.00151952956 | 0.000122774708 |
| erosion_b_only_original_seed0 | 2000 | 1.0441159 | 0 | 0.000694773309 | 0.000532023736 |
| erosion_b_only_original_seed0 | 5000 | 1.03915536 | 0 | 0.000367594005 | 8.18498056e-05 |
| erosion_b_only_original_seed0 | 10000 | 1.03402126 | 0 | 0.000364454888 | 8.18498056e-05 |
| erosion_b_only_original_seed0 | 15000 | 1.03823221 | 0 | 0.000253825913 | 8.18498056e-05 |
| erosion_b_only_original_seed0 | 20000 | 1.03351021 | 0 | 0.000152459468 | 0.000409249028 |

| Run | Early update | A slot counts | A vector | Loss parts |
|---|---|---|---|---|
| erosion_a_plus_b_equal_seed0 | 1 | 101/128, 101/128, 104/128, 105/128, 98/128 | 26/128 | {'A': 0.046896908432245255, 'A_selected_rounds': 1961, 'B': 1.092414379119873, 'active_rounds': 1961} |
| erosion_a_plus_b_equal_seed0 | 5 | 103/128, 106/128, 108/128, 103/128, 101/128 | 34/128 | {'A': 0.3073795735836029, 'A_selected_rounds': 1988, 'B': 1.078127384185791, 'active_rounds': 1988} |
| erosion_a_plus_b_equal_seed0 | 10 | 119/128, 118/128, 118/128, 120/128, 110/128 | 73/128 | {'A': 0.4089803397655487, 'A_selected_rounds': 1998, 'B': 1.0736981630325317, 'active_rounds': 1998} |
| erosion_a_plus_b_equal_seed0 | 50 | 128/128, 127/128, 128/128, 127/128, 127/128 | 125/128 | {'A': 0.016101067885756493, 'A_selected_rounds': 1978, 'B': 1.0825397968292236, 'active_rounds': 1978} |
| erosion_a_plus_b_equal_seed0 | 100 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.008290553465485573, 'A_selected_rounds': 1975, 'B': 1.0839370489120483, 'active_rounds': 1975} |
| erosion_a_plus_b_original_seed0 | 1 | 100/128, 101/128, 105/128, 104/128, 98/128 | 26/128 | {'A': 0.04768984392285347, 'A_selected_rounds': 1992, 'B': 1.0988293886184692, 'active_rounds': 1992} |
| erosion_a_plus_b_original_seed0 | 5 | 118/128, 116/128, 114/128, 116/128, 112/128 | 66/128 | {'A': 0.29754412174224854, 'A_selected_rounds': 1963, 'B': 1.0809369087219238, 'active_rounds': 1963} |
| erosion_a_plus_b_original_seed0 | 10 | 116/128, 118/128, 115/128, 117/128, 112/128 | 66/128 | {'A': 0.3416179120540619, 'A_selected_rounds': 1993, 'B': 1.0704494714736938, 'active_rounds': 1993} |
| erosion_a_plus_b_original_seed0 | 50 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.014954648911952972, 'A_selected_rounds': 1983, 'B': 1.0653444528579712, 'active_rounds': 1983} |
| erosion_a_plus_b_original_seed0 | 100 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.008757418021559715, 'A_selected_rounds': 1987, 'B': 1.0497618913650513, 'active_rounds': 1987} |
| erosion_b_only_equal_seed0 | 1 | 80/128, 81/128, 80/128, 77/128, 72/128 | 3/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.092414379119873, 'active_rounds': 1961} |
| erosion_b_only_equal_seed0 | 5 | 59/128, 64/128, 63/128, 64/128, 58/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0780830383300781, 'active_rounds': 1988} |
| erosion_b_only_equal_seed0 | 10 | 61/128, 64/128, 63/128, 64/128, 57/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0739827156066895, 'active_rounds': 1998} |
| erosion_b_only_equal_seed0 | 50 | 60/128, 62/128, 62/128, 61/128, 55/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0822935104370117, 'active_rounds': 1978} |
| erosion_b_only_equal_seed0 | 100 | 50/128, 52/128, 55/128, 49/128, 46/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.084081768989563, 'active_rounds': 1975} |
| erosion_b_only_original_seed0 | 1 | 94/128, 96/128, 95/128, 97/128, 85/128 | 13/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0988293886184692, 'active_rounds': 1992} |
| erosion_b_only_original_seed0 | 5 | 71/128, 76/128, 72/128, 75/128, 62/128 | 2/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0800786018371582, 'active_rounds': 1963} |
| erosion_b_only_original_seed0 | 10 | 70/128, 75/128, 72/128, 75/128, 63/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0675603151321411, 'active_rounds': 1993} |
| erosion_b_only_original_seed0 | 50 | 50/128, 54/128, 57/128, 52/128, 47/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0673670768737793, 'active_rounds': 1983} |
| erosion_b_only_original_seed0 | 100 | 49/128, 53/128, 55/128, 50/128, 46/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0503771305084229, 'active_rounds': 1987} |

### Seed 1 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 24435/24435, 24435/24435, 24435/24435, 24435/24435, 24435/24435 | 24435/24435 | 1555/1555 |
| erosion_a_plus_b_original_seed1 | B_PASS | 0/24435; 0/24435; 0/24435; 0/24435 | 11/24435; 11/24435; 11/24435; 12/24435 | 0 / 0 of 101 | 24435/24435, 24435/24435, 24435/24435, 24435/24435, 24435/24435 | 24435/24435 | 1554/1555 |
| erosion_b_only_equal_seed1 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 1976/24435, 1976/24435, 1976/24435, 1976/24435, 1976/24435 | 0/24435 | 5/1555 |
| erosion_b_only_original_seed1 | B_INCOMPLETE | 22/24435; 20/24435; 18/24435; 29/24435 | 292/24435; 278/24435; 291/24435; 297/24435 | 1 / 9 of 101 | 11283/24435, 11283/24435, 11283/24435, 11283/24435, 11283/24435 | 30/24435 | 12/1555 |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | 39580462 | 39580462 / 1 | {'12': 189645, '13': 1492783, '23': 130938, '24': 3436635} | {'10': 189951, '16': 1494372, '20': 131278, '27': 3438743} | not applicable |
| erosion_a_plus_b_original_seed1 | 39586743 | 39586743 / 1 | {'12': 206428, '13': 1494046, '23': 131206, '24': 3149758} | {'10': 204701, '16': 1492564, '20': 130744, '27': 3151364} | not applicable |
| erosion_b_only_equal_seed1 | 39580462 | 0 / 0 | {'12': 189645, '13': 1492783, '23': 130938, '24': 3436635} | {'10': 189951, '16': 1494372, '20': 131278, '27': 3438743} | not applicable |
| erosion_b_only_original_seed1 | 39586743 | 0 / 0 | {'12': 206428, '13': 1494046, '23': 131206, '24': 3149758} | {'10': 204701, '16': 1492564, '20': 130744, '27': 3151364} | not applicable |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | 0.00500145042/0.00500194728 (n=32) | 0.00500112399/0.00500123203 (n=32) | 0.00500168698/0.00500245392 (n=64) | 0.00500218151/0.00500282645 (n=64) | 0.00500248536/0.00500366092 (n=64) | 0.00500291842/0.00500385463 (n=64) | 0.0050033622/0.00500461459 (n=64) | 0.00500375428/0.00500525534 (n=64) | 0.00500414777/0.00500504673 (n=64) | 0.00500459271/0.00500582159 (n=64) | 0.00500171857 / 0.00500282645 / True | 0.00500354345 / 0.00500582159 / True |
| erosion_a_plus_b_original_seed1 | 0.00678853458/0.00883157551 (n=32) | 0.00438015419/0.00451572984 (n=32) | 0.00565482676/0.0110094249 (n=64) | 0.00562604691/0.0162439868 (n=64) | 0.00542986474/0.00956751406 (n=64) | 0.00530185574/0.0092028603 (n=64) | 0.0052279745/0.0146133453 (n=64) | 0.00519583456/0.0143289268 (n=64) | 0.00491961127/0.00787325948 (n=64) | 0.00521426508/0.0169001594 (n=64) | 0.00562173935 / 0.0162439868 / True | 0.00521490098 / 0.0169001594 / True |
| erosion_b_only_equal_seed1 | 0.00500193425/0.00500196218 (n=32) | 0.0050019077/0.00500194728 (n=32) | 0.00500201108/0.0050020963 (n=64) | 0.00500210398/0.0050021559 (n=64) | 0.00500217057/0.00500224531 (n=64) | 0.00500226649/0.00500236452 (n=64) | 0.00500234333/0.00500243902 (n=64) | 0.00500242156/0.00500251353 (n=64) | 0.00500252098/0.00500261784 (n=64) | 0.00500259758/0.00500267744 (n=64) | 0.00500201201 / 0.0050021559 / True | 0.00500238675 / 0.00500267744 / True |
| erosion_b_only_original_seed1 | 0.00407378911/0.00489100069 (n=32) | 0.0087451397/0.055624187 (n=32) | 0.00684915623/0.0370277613 (n=64) | 0.00658974191/0.00881398469 (n=64) | 0.00657113071/0.0104407221 (n=64) | 0.00676685909/0.0223876238 (n=64) | 0.0105765819/0.25778915 (n=64) | 0.0073191257/0.0534001589 (n=64) | 0.00654241629/0.00810141861 (n=64) | 0.006709398/0.0184606165 (n=64) | 0.00661612085 / 0.055624187 / False | 0.00741425195 / 0.25778915 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | 9.67796353e-05 / 9.67967736e-05 (n=20222) | not recorded / 7.00354576e-07 | none | 2.23517418e-07 / True | 0 / True |
| erosion_a_plus_b_original_seed1 | 0.000128298693 / 0.000143638436 (n=24118) | 0.997799983 / 0.256649375 | none | 0.00145102292 / True | 0 / True |
| erosion_b_only_equal_seed1 | 9.67525692e-05 / 9.67609655e-05 (n=20222) | not recorded / 5.21540642e-08 | none | 7.4505806e-08 / True | 0 / True |
| erosion_b_only_original_seed1 | 0.000269689295 / 0.000207618281 (n=24118) | 0.995916443 / 0.258668661 | law_TV, rerender, swaps | 0.0469356924 / False | 0 / True |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | A_swap_effect | 64 | 4.88711521e-07 / 1.71363354e-06 |
| erosion_a_plus_b_equal_seed1 | A_swap_exact_row | 64 | 0.00500125228 / 0.00500178337 |
| erosion_a_plus_b_equal_seed1 | both_swap_exact_row | 64 | 0.00500125485 / 0.00500181317 |
| erosion_a_plus_b_equal_seed1 | neutral_A_swap_stability | 128 | 2.56346539e-07 / 9.83476639e-07 |
| erosion_a_plus_b_equal_seed1 | neutral_N | 192 | 0.00500177227 / 0.00500310957 |
| erosion_a_plus_b_equal_seed1 | neutral_raw_swap_stability | 128 | 3.53902578e-08 / 1.1920929e-07 |
| erosion_a_plus_b_equal_seed1 | raw_swap_effect | 64 | 3.46917659e-08 / 1.34110451e-07 |
| erosion_a_plus_b_equal_seed1 | raw_swap_exact_row | 64 | 0.00500125228 / 0.00500178337 |
| erosion_a_plus_b_equal_seed1 | raw_swap_stability | 128 | 0.00250064349 / 0.00500178337 |
| erosion_a_plus_b_equal_seed1 | reset_L | 160 | 0.00500182947 / 0.00500307977 |
| erosion_a_plus_b_equal_seed1 | same_category_substitution | 128 | 2.56230123e-07 / 1.05798244e-06 |
| erosion_a_plus_b_equal_seed1 | set_H | 160 | 0.00500160223 / 0.00500249863 |
| erosion_a_plus_b_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00500164321 / 0.00500224531 |
| erosion_a_plus_b_original_seed1 | A_swap_effect | 64 | 0.0935574152 / 0.248264417 |
| erosion_a_plus_b_original_seed1 | A_swap_exact_row | 64 | 0.167114417 / 0.257203743 |
| erosion_a_plus_b_original_seed1 | both_swap_exact_row | 64 | 0.0059248592 / 0.0195659846 |
| erosion_a_plus_b_original_seed1 | neutral_A_swap_stability | 128 | 0.000453130517 / 0.00489111245 |
| erosion_a_plus_b_original_seed1 | neutral_N | 192 | 0.00579995029 / 0.0195389166 |
| erosion_a_plus_b_original_seed1 | neutral_raw_swap_stability | 128 | 0.000559239474 / 0.0049771592 |
| erosion_a_plus_b_original_seed1 | raw_swap_effect | 64 | 0.168758392 / 0.256189764 |
| erosion_a_plus_b_original_seed1 | raw_swap_exact_row | 64 | 0.0924153256 / 0.249885157 |
| erosion_a_plus_b_original_seed1 | raw_swap_stability | 128 | 0.167936404 / 0.257203743 |
| erosion_a_plus_b_original_seed1 | reset_L | 160 | 0.00689084851 / 0.0195659846 |
| erosion_a_plus_b_original_seed1 | same_category_substitution | 128 | 0.000289833872 / 0.00145372748 |
| erosion_a_plus_b_original_seed1 | set_H | 160 | 0.00441782749 / 0.0051522404 |
| erosion_a_plus_b_original_seed1 | upper_state_exchange_same_N | 64 | 0.00584132446 / 0.0195389166 |
| erosion_b_only_equal_seed1 | A_swap_effect | 64 | 0 / 0 |
| erosion_b_only_equal_seed1 | A_swap_exact_row | 64 | 0.00500191865 / 0.00500196218 |
| erosion_b_only_equal_seed1 | both_swap_exact_row | 64 | 0.00500191865 / 0.00500196218 |
| erosion_b_only_equal_seed1 | neutral_A_swap_stability | 128 | 0 / 0 |
| erosion_b_only_equal_seed1 | neutral_N | 192 | 0.00500203824 / 0.0050021708 |
| erosion_b_only_equal_seed1 | neutral_raw_swap_stability | 128 | 2.79396772e-08 / 7.4505806e-08 |
| erosion_b_only_equal_seed1 | raw_swap_effect | 64 | 3.49245965e-08 / 7.4505806e-08 |
| erosion_b_only_equal_seed1 | raw_swap_exact_row | 64 | 0.00500191865 / 0.00500196218 |
| erosion_b_only_equal_seed1 | raw_swap_stability | 128 | 0.00250097679 / 0.00500196218 |
| erosion_b_only_equal_seed1 | reset_L | 160 | 0.0050020284 / 0.0050021857 |
| erosion_b_only_equal_seed1 | same_category_substitution | 128 | 2.79396772e-08 / 7.4505806e-08 |
| erosion_b_only_equal_seed1 | set_H | 160 | 0.00500201797 / 0.0050021559 |
| erosion_b_only_equal_seed1 | upper_state_exchange_same_N | 64 | 0.00500200689 / 0.00500208139 |
| erosion_b_only_original_seed1 | A_swap_effect | 64 | 0.0309792781 / 0.219551362 |
| erosion_b_only_original_seed1 | A_swap_exact_row | 64 | 0.228550439 / 0.257764325 |
| erosion_b_only_original_seed1 | both_swap_exact_row | 64 | 0.00570641703 / 0.00772386044 |
| erosion_b_only_original_seed1 | neutral_A_swap_stability | 128 | 0.00406372803 / 0.123645455 |
| erosion_b_only_original_seed1 | neutral_N | 192 | 0.00895274442 / 0.221839443 |
| erosion_b_only_original_seed1 | neutral_raw_swap_stability | 128 | 0.00520700286 / 0.223208971 |
| erosion_b_only_original_seed1 | raw_swap_effect | 64 | 0.233109189 / 0.261912368 |
| erosion_b_only_original_seed1 | raw_swap_exact_row | 64 | 0.0334247404 / 0.220151693 |
| erosion_b_only_original_seed1 | raw_swap_stability | 128 | 0.230829814 / 0.261912368 |
| erosion_b_only_original_seed1 | reset_L | 160 | 0.00725955707 / 0.101797119 |
| erosion_b_only_original_seed1 | same_category_substitution | 128 | 0.00541254372 / 0.21893701 |
| erosion_b_only_original_seed1 | set_H | 160 | 0.00745527465 / 0.00779983401 |
| erosion_b_only_original_seed1 | upper_state_exchange_same_N | 64 | 0.00748251902 / 0.0521777421 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.736328125 | -0.06640625 [-0.107421875, -0.025390625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([66], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.7421875 | 0.009765625 [-0.0332519531, 0.056640625] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([52], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.748046875 | -0.001953125 [-0.04296875, 0.041015625] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([68], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.80078125 | 0.03515625 [-0.0078125, 0.072265625] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([66], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.7734375 | 0.0078125 [-0.025390625, 0.041015625] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([52], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.228515625 | -0.080078125 [-0.126953125, -0.03515625] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([252], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.34765625 | 0.083984375 [0.033203125, 0.13671875] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([268], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.255859375 | -0.044921875 [-0.095703125, 0.00590820312] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([244], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.3515625 | 0.091796875 [0.044921875, 0.142578125] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([424], []) |
| erosion_a_plus_b_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.314453125 | -0.052734375 [-0.109375, 0] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([344], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.91015625 | 0.001953125 [-0.025390625, 0.03125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.921875 | 0.009765625 [-0.01171875, 0.033203125] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.927734375 | 0.01953125 [-0.001953125, 0.0390625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.94140625 | 0.001953125 [-0.017578125, 0.0234375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.91796875 | -0.0078125 [-0.029296875, 0.015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.53515625 | -0.072265625 [-0.123046875, -0.025390625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.630859375 | 0.029296875 [-0.021484375, 0.080078125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.490234375 | -0.083984375 [-0.138671875, -0.03515625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.603515625 | 0.03515625 [-0.0117675781, 0.083984375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.615234375 | -0.08203125 [-0.13671875, -0.033203125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / category3 / 1 | 0.884765625 / 0.783203125 | -0.1015625 [-0.142626953, -0.05859375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([108], []) / True ([176], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / category3 / 2 | 0.873046875 / 0.7890625 | -0.083984375 [-0.123046875, -0.0390625] | 0.90625 / 0.82421875 / 1 | True ([101], []) / True ([171], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / category3 / 3 | 0.8203125 / 0.86328125 | 0.04296875 [0, 0.0859375] | 0.9296875 / 0.87109375 / 1 | True ([104], []) / True ([107], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / category3 / 4 | 0.880859375 / 0.853515625 | -0.02734375 [-0.064453125, 0.009765625] | 0.93359375 / 0.875 / 1 | True ([110], []) / True ([125], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / category3 / 5 | 0.90234375 / 0.80078125 | -0.1015625 [-0.14453125, -0.056640625] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([125], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / sum36 / 1 | 0.859375 / 0.875 | 0.015625 [-0.021484375, 0.0546875] | 0.33984375 / 0.169921875 / 1 | True ([178], []) / True ([335], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / sum36 / 2 | 0.85546875 / 0.70703125 | -0.1484375 [-0.199267578, -0.09765625] | 0.35546875 / 0.16015625 / 1 | True ([166], []) / True ([279], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / sum36 / 3 | 0.8828125 / 0.6953125 | -0.1875 [-0.236328125, -0.13671875] | 0.40625 / 0.216796875 / 1 | True ([165], []) / True ([274], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / sum36 / 4 | 0.892578125 / 0.794921875 | -0.09765625 [-0.138720703, -0.0546875] | 0.375 / 0.19140625 / 0.998046875 | True ([148], []) / True ([269], []) |
| erosion_a_plus_b_equal_seed1 | upper / linear / sum36 / 5 | 0.904296875 / 0.78515625 | -0.119140625 [-0.166015625, -0.076171875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([177], []) / True ([266], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / category3 / 1 | 0.955078125 / 0.951171875 | -0.00390625 [-0.0234375, 0.015625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / category3 / 2 | 0.9375 / 0.9296875 | -0.0078125 [-0.0312988281, 0.0137207031] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / category3 / 3 | 0.9375 / 0.962890625 | 0.025390625 [0.001953125, 0.046875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / category3 / 4 | 0.95703125 / 0.966796875 | 0.009765625 [-0.009765625, 0.029296875] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / category3 / 5 | 0.9609375 / 0.955078125 | -0.005859375 [-0.029296875, 0.017578125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.876953125 / 0.90234375 | 0.025390625 [-0.009765625, 0.0605957031] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.849609375 / 0.798828125 | -0.05078125 [-0.091796875, -0.009765625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.865234375 / 0.775390625 | -0.08984375 [-0.130859375, -0.048828125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.8984375 / 0.859375 | -0.0390625 [-0.076171875, 0] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.904296875 / 0.84765625 | -0.056640625 [-0.0918457031, -0.0194824219] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.986328125 | 0.18359375 [0.1484375, 0.216845703] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([108], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.73828125 | 0.005859375 [-0.037109375, 0.0546875] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([93], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.744140625 | -0.005859375 [-0.0508300781, 0.04296875] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([99], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.798828125 | 0.033203125 [-0.00786132812, 0.080078125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([81], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.78125 | 0.015625 [-0.029296875, 0.05859375] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([89], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.7421875 | 0.43359375 [0.3828125, 0.486328125] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([1242], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.326171875 | 0.0625 [0.0078125, 0.115234375] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([190], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.21875 | -0.08203125 [-0.132861328, -0.0331542969] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([273], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.330078125 | 0.0703125 [0.01953125, 0.123046875] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([272], []) |
| erosion_a_plus_b_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.212890625 | -0.154296875 [-0.208984375, -0.099609375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([242], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.99609375 | 0.087890625 [0.064453125, 0.115234375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.90625 | -0.005859375 [-0.029296875, 0.013671875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.943359375 | 0.03515625 [0.01171875, 0.056640625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.947265625 | 0.0078125 [-0.013671875, 0.025390625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.94140625 | 0.015625 [-0.00395507812, 0.037109375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.81640625 | 0.208984375 [0.162060547, 0.2578125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.546875 | -0.0546875 [-0.107421875, 0] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.517578125 | -0.056640625 [-0.111376953, -0.005859375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.5625 | -0.005859375 [-0.05859375, 0.052734375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.564453125 | -0.1328125 [-0.1875, -0.080078125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / category3 / 1 | 0.884765625 / 1 | 0.115234375 [0.087890625, 0.142578125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([108], []) / True ([42], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / category3 / 2 | 0.873046875 / 0.720703125 | -0.15234375 [-0.197265625, -0.107421875] | 0.90625 / 0.82421875 / 1 | True ([101], []) / True ([111], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / category3 / 3 | 0.8203125 / 0.640625 | -0.1796875 [-0.232421875, -0.130810547] | 0.9296875 / 0.87109375 / 1 | True ([104], []) / True ([112], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / category3 / 4 | 0.880859375 / 0.62109375 | -0.259765625 [-0.306640625, -0.21484375] | 0.93359375 / 0.875 / 1 | True ([110], []) / True ([131], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / category3 / 5 | 0.90234375 / 0.740234375 | -0.162109375 [-0.205078125, -0.119140625] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([106], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / sum36 / 1 | 0.859375 / 0.802734375 | -0.056640625 [-0.103564453, -0.009765625] | 0.33984375 / 0.169921875 / 1 | True ([178], []) / True ([640], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / sum36 / 2 | 0.85546875 / 0.39453125 | -0.4609375 [-0.509765625, -0.41015625] | 0.35546875 / 0.16015625 / 1 | True ([166], []) / True ([311], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / sum36 / 3 | 0.8828125 / 0.375 | -0.5078125 [-0.560546875, -0.460888672] | 0.40625 / 0.216796875 / 1 | True ([165], []) / True ([302], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / sum36 / 4 | 0.892578125 / 0.296875 | -0.595703125 [-0.642578125, -0.548828125] | 0.375 / 0.19140625 / 0.998046875 | True ([148], []) / True ([299], []) |
| erosion_a_plus_b_original_seed1 | upper / linear / sum36 / 5 | 0.904296875 / 0.3984375 | -0.505859375 [-0.556640625, -0.45703125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([177], []) / True ([326], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / category3 / 1 | 0.955078125 / 1 | 0.044921875 [0.02734375, 0.060546875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / category3 / 2 | 0.9375 / 0.908203125 | -0.029296875 [-0.05078125, -0.0078125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / category3 / 3 | 0.9375 / 0.9296875 | -0.0078125 [-0.03125, 0.013671875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / category3 / 4 | 0.95703125 / 0.9375 | -0.01953125 [-0.0352050781, -0.001953125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / category3 / 5 | 0.9609375 / 0.92578125 | -0.03515625 [-0.05859375, -0.01171875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / sum36 / 1 | 0.876953125 / 0.837890625 | -0.0390625 [-0.0781738281, -0.001953125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / sum36 / 2 | 0.849609375 / 0.57421875 | -0.275390625 [-0.322265625, -0.228515625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / sum36 / 3 | 0.865234375 / 0.6328125 | -0.232421875 [-0.275390625, -0.1875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / sum36 / 4 | 0.8984375 / 0.5703125 | -0.328125 [-0.377001953, -0.283203125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed1 | upper / mlp64 / sum36 / 5 | 0.904296875 / 0.642578125 | -0.26171875 [-0.306640625, -0.216796875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.7890625 | -0.013671875 [-0.05859375, 0.03125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([94], []) |
| erosion_b_only_equal_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.81640625 | 0.083984375 [0.0390625, 0.12890625] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([79], []) |
| erosion_b_only_equal_seed1 | raw / linear / category3 / 3 | 0.75 / 0.810546875 | 0.060546875 [0.021484375, 0.1015625] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([77], []) |
| erosion_b_only_equal_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.8984375 | 0.1328125 [0.09765625, 0.171875] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([90], []) |
| erosion_b_only_equal_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.794921875 | 0.029296875 [-0.00590820312, 0.06640625] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([62], []) |
| erosion_b_only_equal_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.361328125 | 0.052734375 [0.00390625, 0.103515625] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([298], []) |
| erosion_b_only_equal_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.439453125 | 0.17578125 [0.126953125, 0.224609375] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([352], []) |
| erosion_b_only_equal_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.5 | 0.19921875 [0.1484375, 0.25] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([305], []) |
| erosion_b_only_equal_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.587890625 | 0.328125 [0.275390625, 0.37890625] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([575], []) |
| erosion_b_only_equal_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.365234375 | -0.001953125 [-0.056640625, 0.0527832031] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([276], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.916015625 | 0.0078125 [-0.017578125, 0.037109375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.93359375 | 0.021484375 [-0.001953125, 0.04296875] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.94140625 | 0.033203125 [0.0078125, 0.05859375] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.955078125 | 0.015625 [-0.005859375, 0.03515625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.9296875 | 0.00390625 [-0.01953125, 0.025390625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.625 | 0.017578125 [-0.0293457031, 0.0684082031] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.66796875 | 0.06640625 [0.017578125, 0.115234375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.6875 | 0.11328125 [0.068359375, 0.16015625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.732421875 | 0.1640625 [0.11328125, 0.212890625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.708984375 | 0.01171875 [-0.03515625, 0.05859375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / linear / category3 / 1 | 0.884765625 / 0.796875 | -0.087890625 [-0.125048828, -0.046875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([108], []) / True ([124], []) |
| erosion_b_only_equal_seed1 | upper / linear / category3 / 2 | 0.873046875 / 0.822265625 | -0.05078125 [-0.0879394531, -0.013671875] | 0.90625 / 0.82421875 / 1 | True ([101], []) / True ([132], []) |
| erosion_b_only_equal_seed1 | upper / linear / category3 / 3 | 0.8203125 / 0.8359375 | 0.015625 [-0.0176269531, 0.052734375] | 0.9296875 / 0.87109375 / 1 | True ([104], []) / True ([123], []) |
| erosion_b_only_equal_seed1 | upper / linear / category3 / 4 | 0.880859375 / 0.896484375 | 0.015625 [-0.01953125, 0.05078125] | 0.93359375 / 0.875 / 1 | True ([110], []) / True ([137], []) |
| erosion_b_only_equal_seed1 | upper / linear / category3 / 5 | 0.90234375 / 0.8046875 | -0.09765625 [-0.134765625, -0.060546875] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([111], []) |
| erosion_b_only_equal_seed1 | upper / linear / sum36 / 1 | 0.859375 / 0.36328125 | -0.49609375 [-0.541015625, -0.44921875] | 0.33984375 / 0.169921875 / 1 | True ([178], []) / True ([506], []) |
| erosion_b_only_equal_seed1 | upper / linear / sum36 / 2 | 0.85546875 / 0.44140625 | -0.4140625 [-0.46484375, -0.36328125] | 0.35546875 / 0.16015625 / 1 | True ([166], []) / True ([501], []) |
| erosion_b_only_equal_seed1 | upper / linear / sum36 / 3 | 0.8828125 / 0.494140625 | -0.388671875 [-0.4375, -0.337890625] | 0.40625 / 0.216796875 / 1 | True ([165], []) / True ([519], []) |
| erosion_b_only_equal_seed1 | upper / linear / sum36 / 4 | 0.892578125 / 0.552734375 | -0.33984375 [-0.384765625, -0.291015625] | 0.375 / 0.19140625 / 0.998046875 | True ([148], []) / True ([736], []) |
| erosion_b_only_equal_seed1 | upper / linear / sum36 / 5 | 0.904296875 / 0.375 | -0.529296875 [-0.57421875, -0.482421875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([177], []) / True ([423], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / category3 / 1 | 0.955078125 / 0.916015625 | -0.0390625 [-0.064453125, -0.015625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / category3 / 2 | 0.9375 / 0.91796875 | -0.01953125 [-0.044921875, 0.00390625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / category3 / 3 | 0.9375 / 0.927734375 | -0.009765625 [-0.033203125, 0.0156738281] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / category3 / 4 | 0.95703125 / 0.95703125 | 0 [-0.017578125, 0.017578125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / category3 / 5 | 0.9609375 / 0.92578125 | -0.03515625 [-0.060546875, -0.01171875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / sum36 / 1 | 0.876953125 / 0.6015625 | -0.275390625 [-0.322314453, -0.23046875] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / sum36 / 2 | 0.849609375 / 0.64453125 | -0.205078125 [-0.248046875, -0.158203125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / sum36 / 3 | 0.865234375 / 0.62890625 | -0.236328125 [-0.279296875, -0.193359375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / sum36 / 4 | 0.8984375 / 0.6875 | -0.2109375 [-0.25, -0.173828125] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed1 | upper / mlp64 / sum36 / 5 | 0.904296875 / 0.671875 | -0.232421875 [-0.27734375, -0.19140625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / linear / category3 / 1 | 0.802734375 / 0.99609375 | 0.193359375 [0.158203125, 0.228515625] | 0.919921875 / 0.8515625 / 0.998046875 | True ([74], []) / True ([116], []) |
| erosion_b_only_original_seed1 | raw / linear / category3 / 2 | 0.732421875 / 0.451171875 | -0.28125 [-0.332080078, -0.228515625] | 0.90625 / 0.82421875 / 1 | True ([59], []) / True ([92], []) |
| erosion_b_only_original_seed1 | raw / linear / category3 / 3 | 0.75 / 0.55078125 | -0.19921875 [-0.251953125, -0.14453125] | 0.9296875 / 0.87109375 / 1 | True ([62], []) / True ([103], []) |
| erosion_b_only_original_seed1 | raw / linear / category3 / 4 | 0.765625 / 0.505859375 | -0.259765625 [-0.3125, -0.205078125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([91], []) |
| erosion_b_only_original_seed1 | raw / linear / category3 / 5 | 0.765625 / 0.443359375 | -0.322265625 [-0.375048828, -0.267578125] | 0.927734375 / 0.86328125 / 1 | True ([70], []) / True ([83], []) |
| erosion_b_only_original_seed1 | raw / linear / sum36 / 1 | 0.30859375 / 0.962890625 | 0.654296875 [0.61328125, 0.69921875] | 0.33984375 / 0.169921875 / 1 | True ([392], []) / True ([589], []) |
| erosion_b_only_original_seed1 | raw / linear / sum36 / 2 | 0.263671875 / 0.05078125 | -0.212890625 [-0.25390625, -0.175732422] | 0.35546875 / 0.16015625 / 1 | True ([303], []) / True ([229], []) |
| erosion_b_only_original_seed1 | raw / linear / sum36 / 3 | 0.30078125 / 0.037109375 | -0.263671875 [-0.304736328, -0.22265625] | 0.40625 / 0.216796875 / 1 | True ([324], []) / True ([228], []) |
| erosion_b_only_original_seed1 | raw / linear / sum36 / 4 | 0.259765625 / 0.076171875 | -0.18359375 [-0.224609375, -0.140625] | 0.375 / 0.19140625 / 0.998046875 | True ([342], []) / True ([246], []) |
| erosion_b_only_original_seed1 | raw / linear / sum36 / 5 | 0.3671875 / 0.0390625 | -0.328125 [-0.373046875, -0.283203125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([453], []) / True ([245], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / category3 / 1 | 0.908203125 / 0.998046875 | 0.08984375 [0.068359375, 0.1171875] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / category3 / 2 | 0.912109375 / 0.900390625 | -0.01171875 [-0.033203125, 0.0078125] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / category3 / 3 | 0.908203125 / 0.9296875 | 0.021484375 [0.001953125, 0.0391113281] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / category3 / 4 | 0.939453125 / 0.931640625 | -0.0078125 [-0.021484375, 0.005859375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / category3 / 5 | 0.92578125 / 0.927734375 | 0.001953125 [-0.0156738281, 0.0195800781] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / sum36 / 1 | 0.607421875 / 0.978515625 | 0.37109375 [0.330078125, 0.4140625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / sum36 / 2 | 0.6015625 / 0.365234375 | -0.236328125 [-0.28125, -0.185546875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / sum36 / 3 | 0.57421875 / 0.396484375 | -0.177734375 [-0.224609375, -0.130859375] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / sum36 / 4 | 0.568359375 / 0.3671875 | -0.201171875 [-0.248046875, -0.152294922] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | raw / mlp64 / sum36 / 5 | 0.697265625 / 0.400390625 | -0.296875 [-0.345703125, -0.24609375] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / linear / category3 / 1 | 0.884765625 / 1 | 0.115234375 [0.087890625, 0.142578125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([108], []) / True ([78], []) |
| erosion_b_only_original_seed1 | upper / linear / category3 / 2 | 0.873046875 / 0.72265625 | -0.150390625 [-0.1953125, -0.107373047] | 0.90625 / 0.82421875 / 1 | True ([101], []) / True ([169], []) |
| erosion_b_only_original_seed1 | upper / linear / category3 / 3 | 0.8203125 / 0.705078125 | -0.115234375 [-0.154296875, -0.07421875] | 0.9296875 / 0.87109375 / 1 | True ([104], []) / True ([121], []) |
| erosion_b_only_original_seed1 | upper / linear / category3 / 4 | 0.880859375 / 0.693359375 | -0.1875 [-0.230517578, -0.146484375] | 0.93359375 / 0.875 / 1 | True ([110], []) / True ([138], []) |
| erosion_b_only_original_seed1 | upper / linear / category3 / 5 | 0.90234375 / 0.75 | -0.15234375 [-0.1953125, -0.109375] | 0.927734375 / 0.86328125 / 1 | True ([133], []) / True ([130], []) |
| erosion_b_only_original_seed1 | upper / linear / sum36 / 1 | 0.859375 / 0.759765625 | -0.099609375 [-0.146484375, -0.052734375] | 0.33984375 / 0.169921875 / 1 | True ([178], []) / True ([594], []) |
| erosion_b_only_original_seed1 | upper / linear / sum36 / 2 | 0.85546875 / 0.314453125 | -0.541015625 [-0.5859375, -0.494140625] | 0.35546875 / 0.16015625 / 1 | True ([166], []) / True ([2183], []) |
| erosion_b_only_original_seed1 | upper / linear / sum36 / 3 | 0.8828125 / 0.236328125 | -0.646484375 [-0.693359375, -0.6015625] | 0.40625 / 0.216796875 / 1 | True ([165], []) / True ([524], []) |
| erosion_b_only_original_seed1 | upper / linear / sum36 / 4 | 0.892578125 / 0.236328125 | -0.65625 [-0.701171875, -0.61328125] | 0.375 / 0.19140625 / 0.998046875 | True ([148], []) / True ([566], []) |
| erosion_b_only_original_seed1 | upper / linear / sum36 / 5 | 0.904296875 / 0.380859375 | -0.5234375 [-0.576171875, -0.47265625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([177], []) / True ([3033], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / category3 / 1 | 0.955078125 / 1 | 0.044921875 [0.02734375, 0.060546875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / category3 / 2 | 0.9375 / 0.904296875 | -0.033203125 [-0.0546875, -0.013671875] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / category3 / 3 | 0.9375 / 0.923828125 | -0.013671875 [-0.037109375, 0.0078125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / category3 / 4 | 0.95703125 / 0.931640625 | -0.025390625 [-0.0410644531, -0.0078125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / category3 / 5 | 0.9609375 / 0.927734375 | -0.033203125 [-0.056640625, -0.01171875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / sum36 / 1 | 0.876953125 / 0.869140625 | -0.0078125 [-0.046875, 0.033203125] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / sum36 / 2 | 0.849609375 / 0.44140625 | -0.408203125 [-0.451171875, -0.36328125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / sum36 / 3 | 0.865234375 / 0.431640625 | -0.43359375 [-0.478515625, -0.388671875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / sum36 / 4 | 0.8984375 / 0.400390625 | -0.498046875 [-0.541064453, -0.453076172] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed1 | upper / mlp64 / sum36 / 5 | 0.904296875 / 0.47265625 | -0.431640625 [-0.474609375, -0.384765625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | 0 | 1.08878052 | 0.0454996303 | 0.0098918757 | 1 |
| erosion_a_plus_b_equal_seed1 | 1000 | 1.08317661 | 0.000950363872 | 4.53343785e-05 | 1 |
| erosion_a_plus_b_equal_seed1 | 2000 | 1.08077407 | 0.000316859398 | 2.92349108e-05 | 1 |
| erosion_a_plus_b_equal_seed1 | 5000 | 1.08276021 | 4.30447544e-05 | 5.63729414e-05 | 1 |
| erosion_a_plus_b_equal_seed1 | 10000 | 1.09019303 | 2.88917386e-06 | 1.94612197e-05 | 1 |
| erosion_a_plus_b_equal_seed1 | 15000 | 1.07939637 | 2.05522412e-07 | 1.82690001e-05 | 1 |
| erosion_a_plus_b_equal_seed1 | 20000 | 1.08101809 | 0.000228374745 | 9.67796353e-05 | 1 |
| erosion_a_plus_b_original_seed1 | 0 | 1.08844316 | 0.0484564975 | 0.0646416539 | 1 |
| erosion_a_plus_b_original_seed1 | 1000 | 1.03592312 | 0.000840271008 | 0.0006221563 | 1 |
| erosion_a_plus_b_original_seed1 | 2000 | 1.04982328 | 0.00028195497 | 0.000932823453 | 1 |
| erosion_a_plus_b_original_seed1 | 5000 | 1.04033816 | 3.80112106e-05 | 0.000210376721 | 1 |
| erosion_a_plus_b_original_seed1 | 10000 | 1.03421068 | 2.48130482e-06 | 0.000140012174 | 1 |
| erosion_a_plus_b_original_seed1 | 15000 | 1.04179776 | 0.0496908836 | 0.00095494509 | 0.937016575 |
| erosion_a_plus_b_original_seed1 | 20000 | 1.03582311 | 0.000141367127 | 0.000128298693 | 1 |
| erosion_b_only_equal_seed1 | 0 | 1.08878052 | 0 | 0.0098918757 | 1 |
| erosion_b_only_equal_seed1 | 1000 | 1.08309555 | 0 | 3.33827558e-05 | 0 |
| erosion_b_only_equal_seed1 | 2000 | 1.08056056 | 0 | 4.73496463e-05 | 0 |
| erosion_b_only_equal_seed1 | 5000 | 1.08257151 | 0 | 2.5644429e-05 | 0 |
| erosion_b_only_equal_seed1 | 10000 | 1.09017062 | 0 | 1.3103305e-05 | 0 |
| erosion_b_only_equal_seed1 | 15000 | 1.07939637 | 0 | 1.82057405e-05 | 0 |
| erosion_b_only_equal_seed1 | 20000 | 1.08101785 | 0 | 9.67525692e-05 | 0 |
| erosion_b_only_original_seed1 | 0 | 1.08844316 | 0 | 0.0646416539 | 1 |
| erosion_b_only_original_seed1 | 1000 | 1.03773177 | 0 | 0.00172923069 | 0.00278289339 |
| erosion_b_only_original_seed1 | 2000 | 1.0498116 | 0 | 0.00189363755 | 0.00278289339 |
| erosion_b_only_original_seed1 | 5000 | 1.04093146 | 0 | 0.000690779819 | 0.00278289339 |
| erosion_b_only_original_seed1 | 10000 | 1.03458512 | 0 | 0.000350466788 | 0.00278289339 |
| erosion_b_only_original_seed1 | 15000 | 1.04116464 | 0 | 0.00016964139 | 0.00278289339 |
| erosion_b_only_original_seed1 | 20000 | 1.03529739 | 0 | 0.000269689295 | 0.00122774708 |

| Run | Early update | A slot counts | A vector | Loss parts |
|---|---|---|---|---|
| erosion_a_plus_b_equal_seed1 | 1 | 101/128, 100/128, 104/128, 105/128, 98/128 | 26/128 | {'A': 0.04549963027238846, 'A_selected_rounds': 1969, 'B': 1.0887805223464966, 'active_rounds': 1969} |
| erosion_a_plus_b_equal_seed1 | 5 | 106/128, 106/128, 108/128, 108/128, 103/128 | 46/128 | {'A': 0.2660517990589142, 'A_selected_rounds': 1955, 'B': 1.0903804302215576, 'active_rounds': 1955} |
| erosion_a_plus_b_equal_seed1 | 10 | 121/128, 118/128, 117/128, 120/128, 114/128 | 79/128 | {'A': 0.3996342420578003, 'A_selected_rounds': 2002, 'B': 1.0785578489303589, 'active_rounds': 2002} |
| erosion_a_plus_b_equal_seed1 | 50 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.01613791286945343, 'A_selected_rounds': 1972, 'B': 1.0892235040664673, 'active_rounds': 1972} |
| erosion_a_plus_b_equal_seed1 | 100 | 128/128, 128/128, 128/128, 128/128, 128/128 | 128/128 | {'A': 0.007928813807666302, 'A_selected_rounds': 1999, 'B': 1.081703782081604, 'active_rounds': 1999} |
| erosion_a_plus_b_original_seed1 | 1 | 101/128, 100/128, 103/128, 105/128, 97/128 | 23/128 | {'A': 0.048456497490406036, 'A_selected_rounds': 1969, 'B': 1.0884431600570679, 'active_rounds': 1969} |
| erosion_a_plus_b_original_seed1 | 5 | 119/128, 119/128, 118/128, 119/128, 115/128 | 80/128 | {'A': 0.2558508813381195, 'A_selected_rounds': 2013, 'B': 1.0729501247406006, 'active_rounds': 2013} |
| erosion_a_plus_b_original_seed1 | 10 | 122/128, 121/128, 118/128, 120/128, 115/128 | 84/128 | {'A': 0.32718658447265625, 'A_selected_rounds': 1984, 'B': 1.0538904666900635, 'active_rounds': 1984} |
| erosion_a_plus_b_original_seed1 | 50 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.01416817307472229, 'A_selected_rounds': 1977, 'B': 1.0502285957336426, 'active_rounds': 1977} |
| erosion_a_plus_b_original_seed1 | 100 | 128/128, 128/128, 128/128, 128/128, 128/128 | 128/128 | {'A': 0.008442032150924206, 'A_selected_rounds': 1978, 'B': 1.042803168296814, 'active_rounds': 1978} |
| erosion_b_only_equal_seed1 | 1 | 81/128, 84/128, 83/128, 80/128, 73/128 | 5/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0887805223464966, 'active_rounds': 1969} |
| erosion_b_only_equal_seed1 | 5 | 60/128, 62/128, 65/128, 58/128, 58/128 | 2/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0907388925552368, 'active_rounds': 1955} |
| erosion_b_only_equal_seed1 | 10 | 50/128, 52/128, 55/128, 49/128, 46/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0786969661712646, 'active_rounds': 2002} |
| erosion_b_only_equal_seed1 | 50 | 49/128, 52/128, 55/128, 49/128, 46/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0892353057861328, 'active_rounds': 1972} |
| erosion_b_only_equal_seed1 | 100 | 49/128, 52/128, 55/128, 49/128, 46/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.08128023147583, 'active_rounds': 1999} |
| erosion_b_only_original_seed1 | 1 | 80/128, 80/128, 80/128, 76/128, 72/128 | 2/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0884431600570679, 'active_rounds': 1969} |
| erosion_b_only_original_seed1 | 5 | 50/128, 52/128, 55/128, 49/128, 46/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0720329284667969, 'active_rounds': 2013} |
| erosion_b_only_original_seed1 | 10 | 50/128, 52/128, 55/128, 50/128, 46/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.054946780204773, 'active_rounds': 1984} |
| erosion_b_only_original_seed1 | 50 | 50/128, 53/128, 57/128, 51/128, 47/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0531491041183472, 'active_rounds': 1977} |
| erosion_b_only_original_seed1 | 100 | 61/128, 61/128, 65/128, 57/128, 53/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.044373631477356, 'active_rounds': 1978} |

### Seed 2 — original and equal laws

Census category errors are B-signature errors; undefined under equal law. TV failures are still measured under equal law.

| Run | Endpoint | Census signature errors r0/r1/r2/r3 | TV failures r0/r1/r2/r3 | Saved r9 signature / TV failures | A slot counts 1–5 | A vector | Local histories |
|---|---|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | B_PASS | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 24435/24435, 24435/24435, 24435/24435, 24435/24435, 24435/24435 | 24435/24435 | 1554/1555 |
| erosion_a_plus_b_original_seed2 | B_INCOMPLETE | 0/24435; 0/24435; 0/24435; 0/24435 | 4/24435; 4/24435; 5/24435; 5/24435 | 0 / 0 of 101 | 24431/24435, 24431/24435, 24433/24435, 24432/24435, 24432/24435 | 24419/24435 | 1447/1555 |
| erosion_b_only_equal_seed2 | B_INCOMPLETE | undefined; undefined; undefined; undefined | 0/24435; 0/24435; 0/24435; 0/24435 | None / 0 of 101 | 1947/24435, 1950/24435, 1950/24435, 1946/24435, 1951/24435 | 0/24435 | 61/1555 |
| erosion_b_only_original_seed2 | B_INCOMPLETE | 5/24435; 6/24435; 4/24435; 8/24435 | 31/24435; 36/24435; 31/24435; 45/24435 | 1 / 4 of 101 | 9405/24435, 9413/24435, 9410/24435, 9398/24435, 9401/24435 | 10/24435 | 6/1555 |

| Run | Active rounds | A-supervised rounds / observed dose | Cutoff 12/13/23/24 counts | Decoy 10/16/20/27 counts | Cutoff/decoy enrichment vs paired uniform |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | 39580797 | 39580797 / 1 | {'12': 190469, '13': 1490269, '23': 131016, '24': 3435815} | {'10': 190308, '16': 1493126, '20': 130735, '27': 3436322} | not applicable |
| erosion_a_plus_b_original_seed2 | 39584144 | 39584144 / 1 | {'12': 206552, '13': 1492472, '23': 131003, '24': 3149917} | {'10': 205025, '16': 1494234, '20': 131093, '27': 3148948} | not applicable |
| erosion_b_only_equal_seed2 | 39580797 | 0 / 0 | {'12': 190469, '13': 1490269, '23': 131016, '24': 3435815} | {'10': 190308, '16': 1493126, '20': 130735, '27': 3436322} | not applicable |
| erosion_b_only_original_seed2 | 39584144 | 0 / 0 | {'12': 206552, '13': 1492472, '23': 131003, '24': 3149917} | {'10': 205025, '16': 1494234, '20': 131093, '27': 3148948} | not applicable |

Law cells below are mean/max TV with the number of scored predictions. Short = L/H and N1–N2; extrapolation = N3–N8.

| Run | L_single_round | H_single_round | N_run_1 | N_run_2 | N_run_3 | N_run_4 | N_run_5 | N_run_6 | N_run_7 | N_run_8 | Short mean / max / pass | Extrapolation mean / max / pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | 0.00324745756/0.00324773788 (n=32) | 0.00324741332/0.00324742496 (n=32) | 0.00324747059/0.00324812531 (n=64) | 0.0032474699/0.00324764848 (n=64) | 0.00324748806/0.00324760377 (n=64) | 0.00324750808/0.00324770808 (n=64) | 0.00324753323/0.00324773788 (n=64) | 0.00324754743/0.0032479912 (n=64) | 0.00324755954/0.00324776769 (n=64) | 0.00324757886/0.00324775279 (n=64) | 0.00324745864 / 0.00324812531 / True | 0.00324753587 / 0.0032479912 / True |
| erosion_a_plus_b_original_seed2 | 0.00762095093/0.0179508179 (n=32) | 0.00633172109/0.00646913052 (n=32) | 0.00734690879/0.0239504948 (n=64) | 0.00714587548/0.0207416266 (n=64) | 0.00645224983/0.0216404051 (n=64) | 0.00602063606/0.0232624859 (n=64) | 0.00591029716/0.012126416 (n=64) | 0.00619162177/0.0137146786 (n=64) | 0.00607901462/0.0144119784 (n=64) | 0.00671986898/0.018163234 (n=64) | 0.00715637343 / 0.0239504948 / False | 0.00622894807 / 0.0232624859 / False |
| erosion_b_only_equal_seed2 | 0.00324751716/0.00324754417 (n=32) | 0.00324751437/0.00324751437 (n=32) | 0.00324751181/0.00324757397 (n=64) | 0.00324752554/0.00324755907 (n=64) | 0.00324752554/0.00324755907 (n=64) | 0.00324752997/0.00324757397 (n=64) | 0.0032475323/0.00324758887 (n=64) | 0.00324753835/0.00324760377 (n=64) | 0.00324754394/0.00324758887 (n=64) | 0.00324755348/0.00324760377 (n=64) | 0.0032475177 / 0.00324757397 / True | 0.00324753726 / 0.00324760377 / True |
| erosion_b_only_original_seed2 | 0.00596029125/0.00618077815 (n=32) | 0.00554593932/0.00762147456 (n=32) | 0.00602044561/0.00800742954 (n=64) | 0.00655493839/0.0130419135 (n=64) | 0.00830073119/0.0898597538 (n=64) | 0.00748542685/0.0575128943 (n=64) | 0.010597077/0.236818455 (n=64) | 0.00727006316/0.0123983696 (n=64) | 0.00798246206/0.0229597241 (n=64) | 0.00810225226/0.0128023177 (n=64) | 0.00610949976 / 0.0130419135 / True | 0.00828966875 / 0.236818455 / False |

| Run | Natural / unseen KL bits (unseen n) | Witness recovery / prediction TV | Failed registered bars | Rerender prediction TV / pass | A rerender differences / pass |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | 3.93495216e-05 / 3.9346554e-05 (n=20211) | not recorded / 8.28877091e-08 | none | 4.47034836e-08 / True | 0 / True |
| erosion_a_plus_b_original_seed2 | 0.000128812171 / 0.000107648564 (n=24131) | 0.996222447 / 0.256246448 | law_TV, rerender, swaps | 0.00110461563 / True | 1 / False |
| erosion_b_only_equal_seed2 | 3.93075072e-05 / 3.93094409e-05 (n=20211) | not recorded / 4.23751771e-08 | rerender | 1.1920929e-07 / True | 35 / False |
| erosion_b_only_original_seed2 | 0.000153686815 / 0.00014822106 (n=24131) | 0.997861176 / 0.253940672 | law_TV, rerender, swaps | 0.0186237916 / True | 16 / False |

| Run | Swap case | Count | Mean / max TV |
|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | A_swap_effect | 64 | 5.47152013e-08 / 3.12924385e-07 |
| erosion_a_plus_b_equal_seed2 | A_swap_exact_row | 64 | 0.00324743381 / 0.00324769318 |
| erosion_a_plus_b_equal_seed2 | both_swap_exact_row | 64 | 0.00324743544 / 0.00324772298 |
| erosion_a_plus_b_equal_seed2 | neutral_A_swap_stability | 128 | 2.96859071e-08 / 8.94069672e-08 |
| erosion_a_plus_b_equal_seed2 | neutral_N | 192 | 0.00324745934 / 0.00324775279 |
| erosion_a_plus_b_equal_seed2 | neutral_raw_swap_stability | 128 | 4.07453626e-09 / 5.96046448e-08 |
| erosion_a_plus_b_equal_seed2 | raw_swap_effect | 64 | 6.28642738e-09 / 7.4505806e-08 |
| erosion_a_plus_b_equal_seed2 | raw_swap_exact_row | 64 | 0.00324743381 / 0.00324769318 |
| erosion_a_plus_b_equal_seed2 | raw_swap_stability | 128 | 0.00162372005 / 0.00324769318 |
| erosion_a_plus_b_equal_seed2 | reset_L | 160 | 0.00324748745 / 0.00324800611 |
| erosion_a_plus_b_equal_seed2 | same_category_substitution | 128 | 3.0384399e-08 / 7.4505806e-08 |
| erosion_a_plus_b_equal_seed2 | set_H | 160 | 0.00324744489 / 0.00324773788 |
| erosion_a_plus_b_equal_seed2 | upper_state_exchange_same_N | 64 | 0.0032474522 / 0.00324772298 |
| erosion_a_plus_b_original_seed2 | A_swap_effect | 64 | 0.0468646985 / 0.235289879 |
| erosion_a_plus_b_original_seed2 | A_swap_exact_row | 64 | 0.209782665 / 0.254177935 |
| erosion_a_plus_b_original_seed2 | both_swap_exact_row | 64 | 0.00676285941 / 0.0232143104 |
| erosion_a_plus_b_original_seed2 | neutral_A_swap_stability | 128 | 0.000953140319 / 0.0171196461 |
| erosion_a_plus_b_original_seed2 | neutral_N | 192 | 0.0068837322 / 0.0308299959 |
| erosion_a_plus_b_original_seed2 | neutral_raw_swap_stability | 128 | 0.000702506455 / 0.0149610117 |
| erosion_a_plus_b_original_seed2 | raw_swap_effect | 64 | 0.212717369 / 0.255110919 |
| erosion_a_plus_b_original_seed2 | raw_swap_exact_row | 64 | 0.0449714396 / 0.23104021 |
| erosion_a_plus_b_original_seed2 | raw_swap_stability | 128 | 0.211250017 / 0.255110919 |
| erosion_a_plus_b_original_seed2 | reset_L | 160 | 0.00545381531 / 0.0232143104 |
| erosion_a_plus_b_original_seed2 | same_category_substitution | 128 | 0.000934278942 / 0.018129468 |
| erosion_a_plus_b_original_seed2 | set_H | 160 | 0.00646154233 / 0.00666613132 |
| erosion_a_plus_b_original_seed2 | upper_state_exchange_same_N | 64 | 0.00681131578 / 0.023241736 |
| erosion_b_only_equal_seed2 | A_swap_effect | 64 | 1.0477379e-08 / 5.96046448e-08 |
| erosion_b_only_equal_seed2 | A_swap_exact_row | 64 | 0.0032475146 / 0.00324755907 |
| erosion_b_only_equal_seed2 | both_swap_exact_row | 64 | 0.00324751483 / 0.00324755907 |
| erosion_b_only_equal_seed2 | neutral_A_swap_stability | 128 | 1.26892701e-08 / 7.4505806e-08 |
| erosion_b_only_equal_seed2 | neutral_N | 192 | 0.00324751996 / 0.00324757397 |
| erosion_b_only_equal_seed2 | neutral_raw_swap_stability | 128 | 3.37604433e-09 / 4.47034836e-08 |
| erosion_b_only_equal_seed2 | raw_swap_effect | 64 | 2.56113708e-09 / 2.98023224e-08 |
| erosion_b_only_equal_seed2 | raw_swap_exact_row | 64 | 0.0032475146 / 0.00324755907 |
| erosion_b_only_equal_seed2 | raw_swap_stability | 128 | 0.00162375858 / 0.00324755907 |
| erosion_b_only_equal_seed2 | reset_L | 160 | 0.00324752033 / 0.00324760377 |
| erosion_b_only_equal_seed2 | same_category_substitution | 128 | 1.31549314e-08 / 7.4505806e-08 |
| erosion_b_only_equal_seed2 | set_H | 160 | 0.00324751856 / 0.00324757397 |
| erosion_b_only_equal_seed2 | upper_state_exchange_same_N | 64 | 0.00324751833 / 0.00324757397 |
| erosion_b_only_original_seed2 | A_swap_effect | 64 | 7.28782034e-05 / 0.000257506967 |
| erosion_b_only_original_seed2 | A_swap_exact_row | 64 | 0.254053725 / 0.256447703 |
| erosion_b_only_original_seed2 | both_swap_exact_row | 64 | 0.0057833246 / 0.00644770265 |
| erosion_b_only_original_seed2 | neutral_A_swap_stability | 128 | 0.000194278953 / 0.0118736923 |
| erosion_b_only_original_seed2 | neutral_N | 192 | 0.00759165338 / 0.199914128 |
| erosion_b_only_original_seed2 | neutral_raw_swap_stability | 128 | 0.00288979994 / 0.175042398 |
| erosion_b_only_original_seed2 | raw_swap_effect | 64 | 0.254335183 / 0.255019531 |
| erosion_b_only_original_seed2 | raw_swap_exact_row | 64 | 0.00577735796 / 0.00644770265 |
| erosion_b_only_original_seed2 | raw_swap_stability | 128 | 0.254194454 / 0.256447703 |
| erosion_b_only_original_seed2 | reset_L | 160 | 0.00529640508 / 0.00852996111 |
| erosion_b_only_original_seed2 | same_category_substitution | 128 | 0.00289782218 / 0.174787603 |
| erosion_b_only_original_seed2 | set_H | 160 | 0.00560976365 / 0.00629063696 |
| erosion_b_only_original_seed2 | upper_state_exchange_same_N | 64 | 0.00667806447 / 0.0448610634 |

Probe tables use frozen saved predictions. Oracle is the calibrated exact-A control, not a theoretical floor. MLP fits have a fixed budget and make no convergence claim. Paired intervals retain the original seed and method.

| Run | Carrier / reader / target / slot | Update 0 / endpoint | Gain [paired CI95] | Majority / shuffled / oracle | Convergence 0 / endpoint (iterations, warnings) |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.6796875 | -0.064453125 [-0.109375, -0.017578125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([71], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.822265625 | 0.064453125 [0.0214355469, 0.10546875] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([66], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.833984375 | 0.0859375 [0.05078125, 0.12109375] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([79], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.78515625 | -0.03125 [-0.0703613281, 0.0078125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([55], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.748046875 | 0.02734375 [-0.01171875, 0.068359375] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([55], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.3125 | 0.05859375 [0.0155761719, 0.107421875] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([246], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.40234375 | 0.080078125 [0.029296875, 0.12890625] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([314], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.33984375 | 0.046875 [0.005859375, 0.091796875] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([290], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.322265625 | -0.037109375 [-0.087890625, 0.0137207031] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([271], []) |
| erosion_a_plus_b_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.30859375 | 0.0390625 [-0.0078125, 0.083984375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([327], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.912109375 | -0.01171875 [-0.033203125, 0.009765625] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.947265625 | 0.0234375 [0.001953125, 0.0449707031] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.943359375 | 0.013671875 [-0.005859375, 0.03515625] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.9296875 | -0.00390625 [-0.0234375, 0.013671875] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.92578125 | 0.013671875 [-0.013671875, 0.041015625] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.58203125 | 0.025390625 [-0.021484375, 0.0703125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.642578125 | 0.0390625 [-0.00390625, 0.0801269531] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.6171875 | 0.05078125 [0.005859375, 0.1015625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.611328125 | -0.009765625 [-0.0546875, 0.037109375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.646484375 | 0.001953125 [-0.044921875, 0.046875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / category3 / 1 | 0.9296875 / 0.791015625 | -0.138671875 [-0.177734375, -0.0995605469] | 0.919921875 / 0.8515625 / 0.998046875 | True ([109], []) / True ([113], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / category3 / 2 | 0.8515625 / 0.849609375 | -0.001953125 [-0.041015625, 0.0371582031] | 0.90625 / 0.82421875 / 1 | True ([133], []) / True ([107], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / category3 / 3 | 0.80859375 / 0.830078125 | 0.021484375 [-0.02734375, 0.06640625] | 0.9296875 / 0.87109375 / 1 | True ([112], []) / True ([127], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / category3 / 4 | 0.904296875 / 0.72265625 | -0.181640625 [-0.224609375, -0.138671875] | 0.93359375 / 0.875 / 1 | True ([119], []) / True ([120], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / category3 / 5 | 0.84375 / 0.857421875 | 0.013671875 [-0.029296875, 0.0586425781] | 0.927734375 / 0.86328125 / 1 | True ([103], []) / True ([117], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / sum36 / 1 | 0.873046875 / 0.666015625 | -0.20703125 [-0.255859375, -0.158203125] | 0.33984375 / 0.169921875 / 1 | True ([117], []) / True ([192], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / sum36 / 2 | 0.888671875 / 0.734375 | -0.154296875 [-0.203125, -0.109375] | 0.35546875 / 0.16015625 / 1 | True ([182], []) / True ([146], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / sum36 / 3 | 0.880859375 / 0.73046875 | -0.150390625 [-0.193359375, -0.103515625] | 0.40625 / 0.216796875 / 1 | True ([133], []) / True ([117], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / sum36 / 4 | 0.919921875 / 0.6640625 | -0.255859375 [-0.30078125, -0.20703125] | 0.375 / 0.19140625 / 0.998046875 | True ([177], []) / True ([143], []) |
| erosion_a_plus_b_equal_seed2 | upper / linear / sum36 / 5 | 0.904296875 / 0.751953125 | -0.15234375 [-0.1953125, -0.109375] | 0.404296875 / 0.189453125 / 0.998046875 | True ([162], []) / True ([162], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / category3 / 1 | 0.96484375 / 0.953125 | -0.01171875 [-0.03125, 0.009765625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / category3 / 2 | 0.95703125 / 0.9453125 | -0.01171875 [-0.033203125, 0.009765625] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / category3 / 3 | 0.943359375 / 0.94140625 | -0.001953125 [-0.021484375, 0.01953125] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / category3 / 4 | 0.953125 / 0.962890625 | 0.009765625 [-0.009765625, 0.02734375] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / category3 / 5 | 0.955078125 / 0.962890625 | 0.0078125 [-0.015625, 0.03125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.859375 / 0.775390625 | -0.083984375 [-0.126953125, -0.0429199219] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.865234375 / 0.8515625 | -0.013671875 [-0.052734375, 0.0234375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.876953125 / 0.84765625 | -0.029296875 [-0.068359375, 0.0117675781] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.88671875 / 0.77734375 | -0.109375 [-0.152392578, -0.06640625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.89453125 / 0.890625 | -0.00390625 [-0.041015625, 0.033203125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.9765625 | 0.232421875 [0.1953125, 0.271484375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([133], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.76953125 | 0.01171875 [-0.0390625, 0.060546875] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([79], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.775390625 | 0.02734375 [-0.021484375, 0.072265625] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([97], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.609375 | -0.20703125 [-0.25, -0.158203125] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([76], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.6484375 | -0.072265625 [-0.12890625, -0.0234375] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([66], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.802734375 | 0.548828125 [0.498046875, 0.599609375] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([1436], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.220703125 | -0.1015625 [-0.152392578, -0.048828125] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([208], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.208984375 | -0.083984375 [-0.134765625, -0.033203125] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([157], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.140625 | -0.21875 [-0.267578125, -0.166015625] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([194], []) |
| erosion_a_plus_b_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.21875 | -0.05078125 [-0.0996582031, -0.001953125] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([231], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.982421875 | 0.05859375 [0.0390136719, 0.080078125] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.919921875 | -0.00390625 [-0.03125, 0.021484375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.93359375 | 0.00390625 [-0.01953125, 0.029296875] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.939453125 | 0.005859375 [-0.009765625, 0.0234375] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.931640625 | 0.01953125 [-0.001953125, 0.04296875] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.8671875 | 0.310546875 [0.265625, 0.357470703] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.537109375 | -0.06640625 [-0.123046875, -0.01171875] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.4921875 | -0.07421875 [-0.125, -0.017578125] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.52734375 | -0.09375 [-0.15234375, -0.0390625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.560546875 | -0.083984375 [-0.140625, -0.0312011719] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / category3 / 1 | 0.9296875 / 1 | 0.0703125 [0.048828125, 0.091796875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([109], []) / True ([40], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / category3 / 2 | 0.8515625 / 0.7265625 | -0.125 [-0.17578125, -0.0741699219] | 0.90625 / 0.82421875 / 1 | True ([133], []) / True ([130], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / category3 / 3 | 0.80859375 / 0.78515625 | -0.0234375 [-0.076171875, 0.0273925781] | 0.9296875 / 0.87109375 / 1 | True ([112], []) / True ([128], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / category3 / 4 | 0.904296875 / 0.69921875 | -0.205078125 [-0.25390625, -0.162109375] | 0.93359375 / 0.875 / 1 | True ([119], []) / True ([133], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / category3 / 5 | 0.84375 / 0.748046875 | -0.095703125 [-0.140625, -0.048828125] | 0.927734375 / 0.86328125 / 1 | True ([103], []) / True ([116], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / sum36 / 1 | 0.873046875 / 0.6640625 | -0.208984375 [-0.259765625, -0.158203125] | 0.33984375 / 0.169921875 / 1 | True ([117], []) / True ([1054], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / sum36 / 2 | 0.888671875 / 0.416015625 | -0.47265625 [-0.525390625, -0.421875] | 0.35546875 / 0.16015625 / 1 | True ([182], []) / True ([237], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / sum36 / 3 | 0.880859375 / 0.326171875 | -0.5546875 [-0.603515625, -0.505859375] | 0.40625 / 0.216796875 / 1 | True ([133], []) / True ([232], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / sum36 / 4 | 0.919921875 / 0.419921875 | -0.5 [-0.546875, -0.451123047] | 0.375 / 0.19140625 / 0.998046875 | True ([177], []) / True ([233], []) |
| erosion_a_plus_b_original_seed2 | upper / linear / sum36 / 5 | 0.904296875 / 0.376953125 | -0.52734375 [-0.576171875, -0.4765625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([162], []) / True ([236], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / category3 / 1 | 0.96484375 / 1 | 0.03515625 [0.01953125, 0.052734375] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / category3 / 2 | 0.95703125 / 0.923828125 | -0.033203125 [-0.060546875, -0.0078125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / category3 / 3 | 0.943359375 / 0.93359375 | -0.009765625 [-0.0273925781, 0.009765625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / category3 / 4 | 0.953125 / 0.951171875 | -0.001953125 [-0.021484375, 0.017578125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / category3 / 5 | 0.955078125 / 0.92578125 | -0.029296875 [-0.052734375, -0.005859375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / sum36 / 1 | 0.859375 / 0.779296875 | -0.080078125 [-0.125, -0.03515625] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / sum36 / 2 | 0.865234375 / 0.6796875 | -0.185546875 [-0.23046875, -0.138623047] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / sum36 / 3 | 0.876953125 / 0.60546875 | -0.271484375 [-0.3125, -0.2265625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / sum36 / 4 | 0.88671875 / 0.740234375 | -0.146484375 [-0.1953125, -0.1015625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_a_plus_b_original_seed2 | upper / mlp64 / sum36 / 5 | 0.89453125 / 0.611328125 | -0.283203125 [-0.330078125, -0.232421875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / linear / category3 / 1 | 0.744140625 / 0.67578125 | -0.068359375 [-0.115283203, -0.017578125] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([90], []) |
| erosion_b_only_equal_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.8359375 | 0.078125 [0.037109375, 0.119140625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([85], []) |
| erosion_b_only_equal_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.8515625 | 0.103515625 [0.064453125, 0.138720703] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([79], []) |
| erosion_b_only_equal_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.748046875 | -0.068359375 [-0.109375, -0.02734375] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([53], []) |
| erosion_b_only_equal_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.767578125 | 0.046875 [0.00390625, 0.08984375] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([53], []) |
| erosion_b_only_equal_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.365234375 | 0.111328125 [0.06640625, 0.158300781] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([320], []) |
| erosion_b_only_equal_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.509765625 | 0.1875 [0.138671875, 0.238330078] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([398], []) |
| erosion_b_only_equal_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.396484375 | 0.103515625 [0.052734375, 0.154296875] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([367], []) |
| erosion_b_only_equal_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.3984375 | 0.0390625 [-0.009765625, 0.0898925781] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([482], []) |
| erosion_b_only_equal_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.373046875 | 0.103515625 [0.052734375, 0.152392578] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([255], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.92578125 | 0.001953125 [-0.021484375, 0.0234375] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.9296875 | 0.005859375 [-0.015625, 0.02734375] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.94140625 | 0.01171875 [-0.0078125, 0.03125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.93359375 | 0 [-0.017578125, 0.01953125] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.935546875 | 0.0234375 [0, 0.048828125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.587890625 | 0.03125 [-0.021484375, 0.078125] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.701171875 | 0.09765625 [0.052734375, 0.14453125] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.673828125 | 0.107421875 [0.0644042969, 0.154296875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.73828125 | 0.1171875 [0.0703125, 0.162109375] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.66796875 | 0.0234375 [-0.025390625, 0.0703125] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / linear / category3 / 1 | 0.9296875 / 0.677734375 | -0.251953125 [-0.296875, -0.208935547] | 0.919921875 / 0.8515625 / 0.998046875 | True ([109], []) / True ([111], []) |
| erosion_b_only_equal_seed2 | upper / linear / category3 / 2 | 0.8515625 / 0.802734375 | -0.048828125 [-0.091796875, -0.00776367188] | 0.90625 / 0.82421875 / 1 | True ([133], []) / True ([111], []) |
| erosion_b_only_equal_seed2 | upper / linear / category3 / 3 | 0.80859375 / 0.82421875 | 0.015625 [-0.03125, 0.060546875] | 0.9296875 / 0.87109375 / 1 | True ([112], []) / True ([118], []) |
| erosion_b_only_equal_seed2 | upper / linear / category3 / 4 | 0.904296875 / 0.73828125 | -0.166015625 [-0.20703125, -0.123046875] | 0.93359375 / 0.875 / 1 | True ([119], []) / True ([121], []) |
| erosion_b_only_equal_seed2 | upper / linear / category3 / 5 | 0.84375 / 0.775390625 | -0.068359375 [-0.109375, -0.025390625] | 0.927734375 / 0.86328125 / 1 | True ([103], []) / True ([130], []) |
| erosion_b_only_equal_seed2 | upper / linear / sum36 / 1 | 0.873046875 / 0.34375 | -0.529296875 [-0.580078125, -0.4765625] | 0.33984375 / 0.169921875 / 1 | True ([117], []) / True ([273], []) |
| erosion_b_only_equal_seed2 | upper / linear / sum36 / 2 | 0.888671875 / 0.451171875 | -0.4375 [-0.482421875, -0.388623047] | 0.35546875 / 0.16015625 / 1 | True ([182], []) / True ([262], []) |
| erosion_b_only_equal_seed2 | upper / linear / sum36 / 3 | 0.880859375 / 0.318359375 | -0.5625 [-0.611328125, -0.515625] | 0.40625 / 0.216796875 / 1 | True ([133], []) / True ([195], []) |
| erosion_b_only_equal_seed2 | upper / linear / sum36 / 4 | 0.919921875 / 0.37890625 | -0.541015625 [-0.58984375, -0.494140625] | 0.375 / 0.19140625 / 0.998046875 | True ([177], []) / True ([238], []) |
| erosion_b_only_equal_seed2 | upper / linear / sum36 / 5 | 0.904296875 / 0.31640625 | -0.587890625 [-0.6328125, -0.54296875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([162], []) / True ([240], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / category3 / 1 | 0.96484375 / 0.916015625 | -0.048828125 [-0.072265625, -0.025390625] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / category3 / 2 | 0.95703125 / 0.935546875 | -0.021484375 [-0.044921875, -0.001953125] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / category3 / 3 | 0.943359375 / 0.92578125 | -0.017578125 [-0.0390625, 0.00390625] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / category3 / 4 | 0.953125 / 0.943359375 | -0.009765625 [-0.02734375, 0.0078125] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / category3 / 5 | 0.955078125 / 0.94921875 | -0.005859375 [-0.029296875, 0.017578125] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / sum36 / 1 | 0.859375 / 0.572265625 | -0.287109375 [-0.334033203, -0.240185547] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / sum36 / 2 | 0.865234375 / 0.61328125 | -0.251953125 [-0.298828125, -0.212890625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / sum36 / 3 | 0.876953125 / 0.61328125 | -0.263671875 [-0.308642578, -0.216796875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / sum36 / 4 | 0.88671875 / 0.646484375 | -0.240234375 [-0.283203125, -0.197265625] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_equal_seed2 | upper / mlp64 / sum36 / 5 | 0.89453125 / 0.654296875 | -0.240234375 [-0.28515625, -0.197265625] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / linear / category3 / 1 | 0.744140625 / 1 | 0.255859375 [0.21875, 0.29296875] | 0.919921875 / 0.8515625 / 0.998046875 | True ([58], []) / True ([84], []) |
| erosion_b_only_original_seed2 | raw / linear / category3 / 2 | 0.7578125 / 0.5703125 | -0.1875 [-0.240234375, -0.134765625] | 0.90625 / 0.82421875 / 1 | True ([44], []) / True ([94], []) |
| erosion_b_only_original_seed2 | raw / linear / category3 / 3 | 0.748046875 / 0.517578125 | -0.23046875 [-0.293017578, -0.177685547] | 0.9296875 / 0.87109375 / 1 | True ([56], []) / True ([101], []) |
| erosion_b_only_original_seed2 | raw / linear / category3 / 4 | 0.81640625 / 0.51171875 | -0.3046875 [-0.355517578, -0.25] | 0.93359375 / 0.875 / 1 | True ([48], []) / True ([99], []) |
| erosion_b_only_original_seed2 | raw / linear / category3 / 5 | 0.720703125 / 0.404296875 | -0.31640625 [-0.369140625, -0.265625] | 0.927734375 / 0.86328125 / 1 | True ([40], []) / True ([72], []) |
| erosion_b_only_original_seed2 | raw / linear / sum36 / 1 | 0.25390625 / 0.98046875 | 0.7265625 [0.691357422, 0.765625] | 0.33984375 / 0.169921875 / 1 | True ([250], []) / True ([454], []) |
| erosion_b_only_original_seed2 | raw / linear / sum36 / 2 | 0.322265625 / 0.0859375 | -0.236328125 [-0.279296875, -0.19140625] | 0.35546875 / 0.16015625 / 1 | True ([391], []) / True ([212], []) |
| erosion_b_only_original_seed2 | raw / linear / sum36 / 3 | 0.29296875 / 0.052734375 | -0.240234375 [-0.283203125, -0.19921875] | 0.40625 / 0.216796875 / 1 | True ([315], []) / True ([228], []) |
| erosion_b_only_original_seed2 | raw / linear / sum36 / 4 | 0.359375 / 0.04296875 | -0.31640625 [-0.36328125, -0.267578125] | 0.375 / 0.19140625 / 0.998046875 | True ([337], []) / True ([202], []) |
| erosion_b_only_original_seed2 | raw / linear / sum36 / 5 | 0.26953125 / 0.048828125 | -0.220703125 [-0.263671875, -0.1796875] | 0.404296875 / 0.189453125 / 0.998046875 | True ([319], []) / True ([205], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / category3 / 1 | 0.923828125 / 0.998046875 | 0.07421875 [0.05078125, 0.09765625] | 0.919921875 / 0.8515625 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / category3 / 2 | 0.923828125 / 0.904296875 | -0.01953125 [-0.041015625, 0.001953125] | 0.90625 / 0.82421875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / category3 / 3 | 0.9296875 / 0.931640625 | 0.001953125 [-0.015625, 0.01953125] | 0.9296875 / 0.87109375 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / category3 / 4 | 0.93359375 / 0.93359375 | 0 [-0.015625, 0.015625] | 0.93359375 / 0.875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / category3 / 5 | 0.912109375 / 0.92578125 | 0.013671875 [-0.0078125, 0.037109375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / sum36 / 1 | 0.556640625 / 0.986328125 | 0.4296875 [0.390625, 0.47265625] | 0.33984375 / 0.169921875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / sum36 / 2 | 0.603515625 / 0.447265625 | -0.15625 [-0.20703125, -0.103515625] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / sum36 / 3 | 0.56640625 / 0.439453125 | -0.126953125 [-0.171875, -0.07421875] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / sum36 / 4 | 0.62109375 / 0.3828125 | -0.23828125 [-0.2890625, -0.1875] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | raw / mlp64 / sum36 / 5 | 0.64453125 / 0.421875 | -0.22265625 [-0.275390625, -0.16796875] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / linear / category3 / 1 | 0.9296875 / 0.998046875 | 0.068359375 [0.0468261719, 0.08984375] | 0.919921875 / 0.8515625 / 0.998046875 | True ([109], []) / True ([138], []) |
| erosion_b_only_original_seed2 | upper / linear / category3 / 2 | 0.8515625 / 0.697265625 | -0.154296875 [-0.19921875, -0.10546875] | 0.90625 / 0.82421875 / 1 | True ([133], []) / True ([110], []) |
| erosion_b_only_original_seed2 | upper / linear / category3 / 3 | 0.80859375 / 0.703125 | -0.10546875 [-0.16015625, -0.052734375] | 0.9296875 / 0.87109375 / 1 | True ([112], []) / True ([149], []) |
| erosion_b_only_original_seed2 | upper / linear / category3 / 4 | 0.904296875 / 0.64453125 | -0.259765625 [-0.308642578, -0.2109375] | 0.93359375 / 0.875 / 1 | True ([119], []) / True ([142], []) |
| erosion_b_only_original_seed2 | upper / linear / category3 / 5 | 0.84375 / 0.662109375 | -0.181640625 [-0.232421875, -0.130859375] | 0.927734375 / 0.86328125 / 1 | True ([103], []) / True ([124], []) |
| erosion_b_only_original_seed2 | upper / linear / sum36 / 1 | 0.873046875 / 0.962890625 | 0.08984375 [0.05859375, 0.123046875] | 0.33984375 / 0.169921875 / 1 | True ([117], []) / True ([393], []) |
| erosion_b_only_original_seed2 | upper / linear / sum36 / 2 | 0.888671875 / 0.1953125 | -0.693359375 [-0.736328125, -0.65234375] | 0.35546875 / 0.16015625 / 1 | True ([182], []) / True ([341], []) |
| erosion_b_only_original_seed2 | upper / linear / sum36 / 3 | 0.880859375 / 0.13671875 | -0.744140625 [-0.78515625, -0.70703125] | 0.40625 / 0.216796875 / 1 | True ([133], []) / True ([352], []) |
| erosion_b_only_original_seed2 | upper / linear / sum36 / 4 | 0.919921875 / 0.11328125 | -0.806640625 [-0.841796875, -0.767578125] | 0.375 / 0.19140625 / 0.998046875 | True ([177], []) / True ([346], []) |
| erosion_b_only_original_seed2 | upper / linear / sum36 / 5 | 0.904296875 / 0.166015625 | -0.73828125 [-0.775439453, -0.697265625] | 0.404296875 / 0.189453125 / 0.998046875 | True ([162], []) / True ([302], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / category3 / 1 | 0.96484375 / 0.994140625 | 0.029296875 [0.013671875, 0.046875] | 0.919921875 / 0.8515625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / category3 / 2 | 0.95703125 / 0.908203125 | -0.048828125 [-0.076171875, -0.0234375] | 0.90625 / 0.82421875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / category3 / 3 | 0.943359375 / 0.935546875 | -0.0078125 [-0.02734375, 0.01171875] | 0.9296875 / 0.87109375 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / category3 / 4 | 0.953125 / 0.93359375 | -0.01953125 [-0.0391113281, 0] | 0.93359375 / 0.875 / 0.998046875 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / category3 / 5 | 0.955078125 / 0.927734375 | -0.02734375 [-0.052734375, -0.005859375] | 0.927734375 / 0.86328125 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / sum36 / 1 | 0.859375 / 0.974609375 | 0.115234375 [0.0859375, 0.1484375] | 0.33984375 / 0.169921875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / sum36 / 2 | 0.865234375 / 0.474609375 | -0.390625 [-0.43359375, -0.34375] | 0.35546875 / 0.16015625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / sum36 / 3 | 0.876953125 / 0.4921875 | -0.384765625 [-0.435546875, -0.337890625] | 0.40625 / 0.216796875 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / sum36 / 4 | 0.88671875 / 0.4453125 | -0.44140625 [-0.48828125, -0.398388672] | 0.375 / 0.19140625 / 1 | None ([100], []) / None ([100], []) |
| erosion_b_only_original_seed2 | upper / mlp64 / sum36 / 5 | 0.89453125 / 0.513671875 | -0.380859375 [-0.42578125, -0.331982422] | 0.404296875 / 0.189453125 / 1 | None ([100], []) / None ([100], []) |

| Run | Update | B loss | A loss | Natural KL | A vector accuracy |
|---|---|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | 0 | 1.09945548 | 0.0485652462 | 0.0274039869 | 1 |
| erosion_a_plus_b_equal_seed2 | 1000 | 1.08450854 | 0.000951774186 | 3.68068302e-05 | 1 |
| erosion_a_plus_b_equal_seed2 | 2000 | 1.08029211 | 0.000316420861 | 0.000114426161 | 1 |
| erosion_a_plus_b_equal_seed2 | 5000 | 1.07712114 | 4.33258174e-05 | 8.31592281e-06 | 1 |
| erosion_a_plus_b_equal_seed2 | 10000 | 1.08138394 | 2.63489346e-06 | 3.00829715e-05 | 1 |
| erosion_a_plus_b_equal_seed2 | 15000 | 1.08400154 | 1.9144872e-07 | 9.79406294e-05 | 1 |
| erosion_a_plus_b_equal_seed2 | 20000 | 1.07795584 | 0.000620834006 | 3.93495216e-05 | 1 |
| erosion_a_plus_b_original_seed2 | 0 | 1.09178734 | 0.0484271795 | 0.0846561843 | 1 |
| erosion_a_plus_b_original_seed2 | 1000 | 1.02694881 | 0.00094444881 | 0.00120808893 | 1 |
| erosion_a_plus_b_original_seed2 | 2000 | 1.05770183 | 0.000293396413 | 0.000625202812 | 1 |
| erosion_a_plus_b_original_seed2 | 5000 | 1.04872227 | 4.30199871e-05 | 0.000190665511 | 1 |
| erosion_a_plus_b_original_seed2 | 10000 | 1.05511749 | 2.80995278e-06 | 0.000130395626 | 1 |
| erosion_a_plus_b_original_seed2 | 15000 | 1.03426301 | 1.85844314e-07 | 0.000185566647 | 1 |
| erosion_a_plus_b_original_seed2 | 20000 | 1.03883183 | 0.00476287585 | 0.000128812171 | 0.999345202 |
| erosion_b_only_equal_seed2 | 0 | 1.09945548 | 0 | 0.0274039869 | 1 |
| erosion_b_only_equal_seed2 | 1000 | 1.08440173 | 0 | 2.55456233e-05 | 0 |
| erosion_b_only_equal_seed2 | 2000 | 1.08030605 | 0 | 6.89687679e-05 | 0 |
| erosion_b_only_equal_seed2 | 5000 | 1.07720363 | 0 | 2.88153175e-05 | 0 |
| erosion_b_only_equal_seed2 | 10000 | 1.08138478 | 0 | 3.06474893e-05 | 0 |
| erosion_b_only_equal_seed2 | 15000 | 1.08400118 | 0 | 9.78615613e-05 | 0 |
| erosion_b_only_equal_seed2 | 20000 | 1.07795596 | 0 | 3.93075072e-05 | 0 |
| erosion_b_only_original_seed2 | 0 | 1.09178734 | 0 | 0.0846561843 | 1 |
| erosion_b_only_original_seed2 | 1000 | 1.02777469 | 0 | 0.00234613664 | 0.000368324125 |
| erosion_b_only_original_seed2 | 2000 | 1.05734086 | 0 | 0.00144240571 | 0.000695723348 |
| erosion_b_only_original_seed2 | 5000 | 1.04875994 | 0 | 0.000464389959 | 0.000695723348 |
| erosion_b_only_original_seed2 | 10000 | 1.05588555 | 0 | 0.000292167242 | 0 |
| erosion_b_only_original_seed2 | 15000 | 1.03420866 | 0 | 0.000236104071 | 0.000409249028 |
| erosion_b_only_original_seed2 | 20000 | 1.03860044 | 0 | 0.000153686815 | 0.000409249028 |

| Run | Early update | A slot counts | A vector | Loss parts |
|---|---|---|---|---|
| erosion_a_plus_b_equal_seed2 | 1 | 100/128, 101/128, 105/128, 103/128, 98/128 | 25/128 | {'A': 0.04856524616479874, 'A_selected_rounds': 1996, 'B': 1.09945547580719, 'active_rounds': 1996} |
| erosion_a_plus_b_equal_seed2 | 5 | 108/128, 107/128, 107/128, 106/128, 103/128 | 45/128 | {'A': 0.21990883350372314, 'A_selected_rounds': 1979, 'B': 1.086190104484558, 'active_rounds': 1979} |
| erosion_a_plus_b_equal_seed2 | 10 | 120/128, 119/128, 119/128, 118/128, 115/128 | 79/128 | {'A': 0.4156608283519745, 'A_selected_rounds': 1958, 'B': 1.0855878591537476, 'active_rounds': 1958} |
| erosion_a_plus_b_equal_seed2 | 50 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.016235332936048508, 'A_selected_rounds': 1977, 'B': 1.0878667831420898, 'active_rounds': 1977} |
| erosion_a_plus_b_equal_seed2 | 100 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.008743124082684517, 'A_selected_rounds': 1983, 'B': 1.0835916996002197, 'active_rounds': 1983} |
| erosion_a_plus_b_original_seed2 | 1 | 101/128, 101/128, 105/128, 106/128, 98/128 | 28/128 | {'A': 0.04842717945575714, 'A_selected_rounds': 1998, 'B': 1.091787338256836, 'active_rounds': 1998} |
| erosion_a_plus_b_original_seed2 | 5 | 97/128, 98/128, 100/128, 99/128, 91/128 | 22/128 | {'A': 0.24725255370140076, 'A_selected_rounds': 1982, 'B': 1.072322130203247, 'active_rounds': 1982} |
| erosion_a_plus_b_original_seed2 | 10 | 119/128, 118/128, 117/128, 119/128, 113/128 | 76/128 | {'A': 0.3697628676891327, 'A_selected_rounds': 1993, 'B': 1.0677369832992554, 'active_rounds': 1993} |
| erosion_a_plus_b_original_seed2 | 50 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.014371786266565323, 'A_selected_rounds': 1965, 'B': 1.0558929443359375, 'active_rounds': 1965} |
| erosion_a_plus_b_original_seed2 | 100 | 128/128, 127/128, 128/128, 127/128, 128/128 | 126/128 | {'A': 0.008100869134068489, 'A_selected_rounds': 1970, 'B': 1.0481475591659546, 'active_rounds': 1970} |
| erosion_b_only_equal_seed2 | 1 | 98/128, 93/128, 94/128, 93/128, 83/128 | 17/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.09945547580719, 'active_rounds': 1996} |
| erosion_b_only_equal_seed2 | 5 | 12/128, 9/128, 7/128, 14/128, 10/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.085984230041504, 'active_rounds': 1979} |
| erosion_b_only_equal_seed2 | 10 | 11/128, 7/128, 6/128, 12/128, 9/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0845493078231812, 'active_rounds': 1958} |
| erosion_b_only_equal_seed2 | 50 | 11/128, 7/128, 6/128, 11/128, 9/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.08893620967865, 'active_rounds': 1977} |
| erosion_b_only_equal_seed2 | 100 | 11/128, 7/128, 6/128, 11/128, 9/128 | 0/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0834524631500244, 'active_rounds': 1983} |
| erosion_b_only_original_seed2 | 1 | 87/128, 88/128, 84/128, 82/128, 77/128 | 11/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.091787338256836, 'active_rounds': 1998} |
| erosion_b_only_original_seed2 | 5 | 61/128, 63/128, 62/128, 64/128, 56/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.072237253189087, 'active_rounds': 1982} |
| erosion_b_only_original_seed2 | 10 | 62/128, 63/128, 62/128, 63/128, 56/128 | 2/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0659674406051636, 'active_rounds': 1993} |
| erosion_b_only_original_seed2 | 50 | 50/128, 54/128, 57/128, 49/128, 51/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0604256391525269, 'active_rounds': 1965} |
| erosion_b_only_original_seed2 | 100 | 50/128, 54/128, 56/128, 49/128, 47/128 | 1/128 | {'A': 0.0, 'A_selected_rounds': 0, 'B': 1.0504672527313232, 'active_rounds': 1970} |

## Dose category decomposition

A-head category errors and B predictive-signature errors are distinct measurements. Original-law counts come from a post-hoc, one-thread float32 CPU replay of the saved 20k checkpoints on all 24,435 boards in registered rendering 0. No parameter updates or fits occur; seed 0 is checked against analysis's independent replay. Equal-law B signatures are undefined.

| Run | A-head slot-1 category errors | B-signature errors | B errors with correct A category | Source |
|---|---|---|---|---|
| dose_dose100_equal_seed0 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose100_equal_seed1 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose100_equal_seed2 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose100_original_seed0 | 155 | 298 | 200 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose100_original_seed1 | 110 | 200 | 166 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose100_original_seed2 | 108 | 406 | 339 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose10_equal_seed0 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose10_equal_seed1 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose10_equal_seed2 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose10_original_seed0 | 168 | 160 | 92 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose10_original_seed1 | 258 | 214 | 129 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose10_original_seed2 | 196 | 106 | 51 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose1_equal_seed0 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose1_equal_seed1 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose1_equal_seed2 | None | None | None | UNDEFINED_EQUAL_LAW_SIGNATURE |
| dose_dose1_original_seed0 | 552 | 81 | 24 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose1_original_seed1 | 392 | 82 | 23 | POST_HOC_CPU_CHECKPOINT_REPLAY |
| dose_dose1_original_seed2 | 593 | 85 | 11 | POST_HOC_CPU_CHECKPOINT_REPLAY |

## Original-law B-only erosion output alphabets

Values are in twelfths. These are not one constant answer.

| Seed | Alphabet | Source |
|---|---|---|
| 0 | [0, 4, 36] | independent original-law checkpoint replay |
| 1 | [0, 8] | independent original-law checkpoint replay |
| 2 | [0, 4, 15] | independent original-law checkpoint replay |

## Missing runs

None
