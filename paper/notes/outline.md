# Outline — Where Does Jagged Competence Come From?

Every scientific claim below maps explicitly to the hash-verified evidence ledger. Interpretation paragraphs are in `paper/notes/interpretation.md` (JI §§1–13). Terms follow `notation_and_terminology.md`.

## Title
*Where Does Jagged Competence Come From?*

The abstract states the scope: this task and these networks.

## Angle
The paper explains where jagged competence comes from in the tested setting. Jaggedness, high average competence alongside specific failures, is the phenomenon. The explanation is that the five achievements (recoverability, computation, access, preservation, reliable prediction) are separate, so success on one leaves the others open; the failures we measured are tied to specific missing achievements (access, preservation) and to contributing conditions with measured effects (target noise, encoding, history coverage, the last from a historical comparison); some failures remain unexplained (19 r12 cases), and the paper says so. The title, abstract, the introduction's question and contributions, the opening claim of each results subsection, and the discussion carry this angle. "Jagged" is never its own explanation, and transfer beyond this setting is posed as a test to run.

## Thesis (JI §1)
The studies separate five achievements that are often treated as one:
1. making a lower result recoverable;
2. computing it;
3. giving the prediction access to it;
4. preserving it under further training;
5. producing reliable predictions.

Progress on one did not guarantee the others.

## Abstract plan (about 200 words, written last)
1. **Setting:** a records game with full ground truth, in which the next-category law depends on a hidden on/off mode that past slot-1 sums switch. The prediction cannot be computed from the current board's sums. This is a property of the task.
2. **Question:** where does jagged competence come from? A recurrent network trained to predict has low average error yet fails on specific boards and histories; which parts of the job did it fail to achieve, and what contributed to each failure?
3. **Method:** three versions (**records → prediction**, **records+sums → prediction**, **records → prediction+sums**); exhaustive census of boards, constructed-history panels, probes with control floors, swap tests, and four mechanism experiments; 3 seeds per condition.
4. **Findings, scoped:**
   - training shapes what is recoverable;
   - target noise contributes;
   - recovered or computed sums need not be used;
   - encoding matters;
   - prediction updates erode an exact sums computation;
   - exact sums do not guarantee reliability.
5. **Answer, scoped:** in this task, jagged competence comes from the separation of five achievements: success on one leaves the others open. The measured failures are tied to missing access and preservation and to contributing conditions with measured effects (target noise, encoding, history coverage); some cases remain unexplained. Low average error and high probe accuracy each hide these failures. Whether the same sources operate in other systems is posed as a test.

## Section plan

### 1 Introduction
- Motivation: jagged competence, high average competence alongside specific failures, is widely observed but its sources are hard to isolate in large systems. The question: where does it come from? A controlled task with full ground truth lets us locate the sources (JI §10).
- The measurement gap: averages and probes each look healthy while constructed tests fail (JI §9).
- The study: a controlled task, three versions, a census plus constructed tests, and mechanism experiments.
- **Contributions (3–4):**
  - (a) a controlled task with an exhaustive census, constructed-history panels, and calibrated probe and swap tests;
  - (b) an account of where jagged competence comes from in this task: the five achievements come apart, and the measured failures are tied to missing achievements and to contributing conditions with measured effects (JI §1);
  - (c) four matched mechanism experiments (noise, access, encoding, erosion) with their measured effects and limits (JI §§4–8);
  - (d) a released ledger and code that rebuild every number.

### 2 Related work (short; themes in the map below)

### 3 Task and setup
- 3.1 **The game.** Board, records, slots, sums; the hidden on/off mode; L/N/H categories; the next-category laws (½,¼,¼) and (¼,¼,½); the equal-law control. **Fig. 1.**
- 3.2 **Strictness as a task property** (JI §2). The same neutral board after an off or an on history needs different probabilities. The exact update needs only slot 1's cutoff category and the previous mode. Six Birds terms are defined once here, scoped to the task.
- 3.3 **Versions and training.** The three versions; the AdamW settings; online episodes; history coverage (r12); seeds 0–2; updates. **Fig. 2** (architecture).
- 3.4 **Study history.** r8–r13 as registered studies with follow-ups and corrected audits, pointing to App. A. The campaign was not one confirmatory study.

### 4 Measurements
- **Prediction criteria:** natural and unseen KL, witness recovery, constructed-history law panels (short vs long), swaps, rendering. Each comes with its exact-oracle ceiling and board-only/untrained floor.
- **Census:** 24,435 boards × 4 renderings. Categorical misreads are kept distinct from TV-error counts.
- **Probes:** linear and MLP; update 0 → endpoint; untrained, majority and shuffled floors; paired CIs.
- **Swap test:** the alignment; positive, no-op and shuffled controls; selectivity; support counts.
- **Calibration:** every bar is checked with the deciding functions.

### 5 Results (claim → evidence → bounded interpretation → scope)
Each subsection's opening claim names the source, separation or unresolved failure it examines: 5.1 recoverability; 5.2 the phenomenon itself (low average error, specific failures); 5.3 target noise; 5.4 access; 5.5 encoding (the form of access); 5.6 preservation; 5.7 what remains when the sums are exact (reliable prediction).
- **5.1 Training shapes what becomes recoverable** (JI §3).
  - **r8, records → prediction**, raw carrier, at the 20k endpoint vs update 0, on sampled probe-held-out boards:
    - slot-1 exact sum: linear probe ≈0.3 → 0.97–0.98;
    - slots 2–5: linear ≈0.3 → 0.05–0.10, and MLP ≈0.6 → ≈0.38 (mean over slots 2–5 and 3 seeds).
    - Caveat: the linear probe is class-balanced, so accuracy below the majority floor partly reflects that weighting.
    - Declining probe accuracy means reduced measured readability, not removal of information.
  - **r10, the all-slots task**, raw carrier, linear exact-sum probes, 20k vs update 0, sampled support: recovery rises for all five sums (0.20–0.37 → 0.88–0.95), with paired CIs excluding zero. Rare sum values lie outside the registered readability scope.
  - **Scope:** this is task-dependent organization of recoverable information. It is not exact computation everywhere. r8 vs r10 is a historical comparison across different tasks.
  - **Evidence:** Fig. 3 (left); Appendix E.
- **5.2 Average error hides specific failures** (JI §9).
  - **r8, records → prediction:** natural KL ≈0.0001–0.0003 bits, yet 0/3 runs pass, with law TV ≈0.25 on constructed histories.
  - **Census:** misreads concentrate in the cutoff band (the per-study counts are given in the census table).
  - **r12 vs r11:** the r12 history-coverage study has smaller long-panel errors than r11. This is a historical comparison: the curriculum and the loss weighting also changed.
    - r12 runs are 9 in total (three sampling arms × three seeds), and none passes.
    - Long-panel maxima reach 0.172; short-panel maxima range 0.020–0.066.
    - Prefix diagnoses: 20 board-associated (all coincident), 3 recurrence-associated, 19 unresolved and 120 non-deviating. Misreads do not explain every failure.
  - **Cutoff enrichment:** inconsistent repair.
  - **Evidence:** Fig. 3 (right); Appendix B.
- **5.3 Target noise contributes but is insufficient** (JI §4).
  - With exact-probability targets, records → prediction misreads go 58/328/87 → 2/1/149: two seeds near zero, one worse.
  - records → prediction+sums goes 473/648/815 → 473/400/523.
  - No run passes. Matched comparison (r13).
  - Evidence: **Fig. 4a**.
- **5.4 Computing or recovering sums does not guarantee their use** (JI §§5, 9).
  - **r12, matched comparison:**
    - records+sums → prediction passes 2/3, with 0–1 misreads;
    - records → prediction+sums passes 0/3, with 473–815 misreads;
    - prediction errors on boards where the sums output's **slot-1 category** is correct (not necessarily all five sums): 326/617/770.
  - **r13 access:** connecting the learned sums output to the prediction cuts misreads 1.3–11× (frozen) and 2.8–17× (live), and lowers natural KL, relative to disconnected.
    - This is attributed to the prediction's access to the sums under the tested architecture. It does not establish a selective internal sums representation.
    - **No connected learned-sums run passes every B criterion.** Long-history failures can remain (live seed 1: 0.251).
  - **r10:** probes recover the sums, and the interchange calibration succeeded. Even so, the tested alignment did not support selective replacement (188–436 other-slot changes per 1,024 swaps). Successful calibration and failed selectivity are reported separately.
  - Interference is not established.
  - **Evidence:** Fig. 4b; Table 2.
- **5.5 Encoding matters** (JI §6).
  - With the same exact sums: one-hot gives 0/0/2 misreads, numerical gives 317/121/10.
  - Supplementary cutoff geometry: probes discriminate 12/13 and 23/24 in every probability-target seed while the prediction still fails.
  - No precision ceiling is inferred.
  - Evidence: **Fig. 4c**.
- **5.6 Prediction updates can erode an exact sums computation** (JI §7).
  - **r11 (sampled early-board readouts):** in B-only continuation from an exact sums network, exactness is lost immediately and then degrades severely. Continued A loss largely protects it, though not everywhere: board vectors 24,434 / 24,435 / 24,419 out of 24,435.
  - **r13 (exhaustive 1,555 local histories):** exactness is lost at update 1 under AdamW, reduced-lr AdamW and SGD, with very different severity. Blocking the prediction gradient keeps 1,555/1,555 through 200 updates, with weight decay retained.
  - The active optimizers are compared only within the movement ranges each actually covered. The blocked condition is a separate decay control.
  - Erosion is not unique to Adam. Direction, displacement and answer margins are not isolated from one another.
  - **Evidence:** Fig. 5.
- **5.7 Correct sums do not guarantee reliable prediction** (JI §§8, 11).
  - **Registered pass** is defined per study at its fixed endpoint (criteria in Appendix B):
    - r8: dual 3/3, A-only 2/3;
    - r12: 2/3;
    - r13 one-hot exact: 1/3;
    - r10 (a different task and criterion set): even supplied A fails at 20k.
  - These are historical comparisons across architectures and tasks.
  - A registered pass is not exhaustive correctness: the passing r13 seed still has 2 census misreads.
  - Residual failures need separate diagnosis.
  - **Evidence:** Table 2.

### 6 Discussion
- The five achievements as a reading frame (JI §1). The order of presentation is not a developmental sequence.
- **Measurement cautions** (JI §9), not claims of transfer:
  - low average error can hide failures on constructed tests;
  - probes can recover information without showing that the prediction uses it.
- **Untested transfer questions**, phrased as tests:
  - Do these separations appear in other architectures, tasks and budgets?
  - Do exact magnitudes and the dependence of erosion severity on the optimizer carry over?
- Questions beyond this game, phrased as tests to run (JI §12): cleaner targets, structured intermediate inputs, whether auxiliary outputs are used, whether downstream training preserves earlier computations.
- Where jagged competence comes from, in summary: the separate achievements, the missing achievements and contributing conditions behind the measured failures, and the cases that remain unexplained; what this account explains in this task and what it leaves open (JI §10). "Jagged" names the phenomenon, never its cause.

### 7 Limitations
Each item is a "we cannot claim X because Y" statement:
- one game family;
- small recurrent networks;
- 3 seeds;
- fixed budgets;
- constructed tests do not estimate frequencies in ordinary use;
- historical comparisons;
- the swap test fails under one alignment, which excludes no other representation;
- passing the registered tests ≠ correctness everywhere (the r13 passing seed has 2 census misreads);
- the paperclip-era exemplar versions are not identifiable. This affects only style, not science, and is listed in the appendix only.

### 8 Conclusion (one paragraph)

## Main figures (5) and main tables (2)

| # | Content | Panels | Data |
|---|---|---|---|
| Fig. 1 | Task and ground truth | board → sums → on/off mode → next-category law; strictness witness (same board, two histories) | task definition |
| Fig. 2 | Shared architecture with a route/loss matrix | one recurrent architecture; a matrix of which input routes and losses each version uses (three versions plus r13 connected frozen/live, numerical encoding, probability targets); probe and swap-test icons only (procedures in App. C) | architecture |
| Fig. 3 | Recoverability vs reliability | (a) per-slot probe recovery, update 0 → 20k (r8, r10; carrier and probe family labeled); (b) natural KL vs constructed-law TV per run; (c) misreads by slot-1 sum (census) | r8, r10, r12 |
| Fig. 4 | Mechanisms | (a) noise: sampled vs probability targets, per seed; (b) access: disconnected / frozen / live / exact; (c) encoding: one-hot vs numerical | r12, r13 |
| Fig. 5 | Erosion | per-seed small multiples: exactness vs update, and vs cumulative movement within each optimizer's observed range; blocked shown as a separate decay control | r11, r13 |

| Table | Content |
|---|---|
| Tab. 1 | **Five-achievement summary:** for each version and condition, each achievement is marked supported, not supported or **not established**, with the evidence and support size, so the unequal support is visible |
| Tab. 2 | Access and supplied-condition reliability: study-specific criteria, pass counts, misreads, long-panel maxima; historical comparisons labeled |

**Prepared tables:**
- a **sampling/training/criteria table** per study (episodes, truncation, history coverage, losses, the r10 task, criteria and bars), for §3 or Appendix B;
- the **full study × version matrix** in Appendix B.

## Appendix allocation
- **A:** study history (registrations, follow-ups, corrected audits, supplementary analyses, scientific qualifications).
- **B:** full per-study tables r8–r13, including the equal-law controls.
- **C:** calibration (deciding functions, positives and negatives, swap-test support) and detailed swap-test alignment procedures.
- **D:** per-seed learning curves; erosion early readouts.
- **E:** probes in full (both carriers, both readout families, CIs, convergence) and geometry support, including the supplementary cutoff panel: fitting/evaluation pairs 135/150 (12/13) and 12/13 (23/24), discrimination outcomes and calibration.
- **F:** compute, hardware and reproduction (commands, artifacts, hashes).

## Related-work map
Each theme ends with agree / extend / differ.
1. **Feature learning and simplicity bias** (Hermann & Lampinen; Shah et al.; Pezeshki et al.). *Extend:* the task-dependent recoverability we observe matches suppression of unused features; we add the use and preservation measures.
2. **Probing vs use** (Hewitt & Liang; Elazar et al.; Belinkov; Ravichander et al.). *Agree:* recoverable ≠ used. *Extend:* we pair probes with calibrated swap tests and matched connection experiments in a task with full ground truth.
3. **Causal interventions** (Geiger et al., both papers; Meng et al., secondary). *Differ:* our swap test fails selectivity under one alignment, and we report that as a limit, not as absence.
4. **Synthetic-task world models** (Li et al.; Vafa et al.; Delétang et al.; Allen-Zhu & Li; Nanda et al.; Elhage et al.). *Agree:* averages hide constructed failures (Vafa et al.). *Extend:* an exhaustive census plus history panels.
5. **Auxiliary targets, soft targets and interference** (Hinton et al.; Yu et al.; Kirkpatrick et al.; McCloskey & Cohen). *Differ:* an auxiliary output that is not connected can coexist with worse prediction. Erosion under prediction updates resembles interference, but is not established as such.
6. **The jagged-frontier framing** (Dell'Acqua et al.). *Extend:* they observe jagged competence in the field; we locate its sources in a controlled task with full ground truth.

## Prohibited claims
- Strictness as an internal layer.
- Extension to LLMs, tools or distillation.
- Interference as established.
- A precision ceiling.
- Constructed failures as frequencies in ordinary use.
- The five achievements as a compulsory sequence.
