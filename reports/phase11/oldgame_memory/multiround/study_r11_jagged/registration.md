# Public scientific registration

This is a public projection. Complete numerical settings, source identities and registered criteria are recorded in `registration.json`.

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
