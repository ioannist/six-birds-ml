# Public scientific registration

This is a public projection. Complete numerical settings, source identities and registered criteria are recorded in `registration.json`.

## r8: route access during B-only training

**Question.** With the same records game and only next-category supervision, does access to an exact learned A interface change how quickly and reliably a network learns B? When the raw route has no access to A answers, does B training make the five per-slot sums more readable inside it?

### Three claims

1. **Interface:** \(B_t=(a_t,e_t)\) strictly extends the *current completed sum board* as a predictive interface: the same current board can require different next-round laws after different histories. This claim concerns that interface, not the unrestricted continuous carrier.
2. **Lower objects:** the mode \(e_t\) is constructed from the history of completed A sum boards. It needs the slot-1 category; the other four sums are not rewarded by B prediction.
3. **Pathway:** r8 tests whether supplying learned A answers changes B learning, and whether B-only training makes A readable in a raw route. Raw records determine A, so route access and probe readability alone cannot prove that a dual-route model *uses* A on consistent inputs.

### Arms and training

Use one `ChoiceNetwork` architecture and paired initial weights per seed. Load the **same previously verified, exact A memory core** into every arm and freeze it. Mask its output from the upper recurrence in raw-only; mask the raw vector in A-only; expose both in dual. Masked channels are constant zero throughout that arm’s training and evaluation. The raw encoder resets each round; the upper recurrence alone persists.

| Arm | Upper input | r8 training loss |
|---|---|---|
| A-only | Five hard answers from frozen learned A | Next-category cross-entropy only |
| Raw-only | Per-round raw encoder vector | Next-category cross-entropy only |
| Dual | Both routes | Next-category cross-entropy only |

**No arm receives an A-answer loss in r8.** The A source acquired its sums before r8; its checkpoint and exactness audit must be named in the registration. Thus A-only tests *use of supplied A*, while **raw-only** tests spontaneous A readability under B-only training.

Use the shared online sampler and record projection, 12-round test, seeds 0–2, batch 256, AdamW learning rate 0.003 and weight decay 0.01, 20,000-update endpoint, original and equal laws, and saved Gate A routing. Pair training streams and test panels across the three arms. Do not select checkpoints by test performance.

### Measurements and calibration

- **B learning:** audit at updates **0, 1k, 2k, 5k, 10k, 15k, 20k**. Report natural and unseen excess KL, witness recovery, maximum L/H and \(N^1\)–\(N^8\) law TV, rerendering, and upper-state swaps. The B bars are: KL ≤0.01 bits, witness recovery ≥80%, and law/intervention TV ≤0.02. Report the *first audited crossing* of all bars and whether the 20k endpoint passes. The measured positive is the exact predictive oracle run on the same panels; the null is the exact current-board-only predictor, alongside update-0 model scores. The equal-law positive is its constant exact row; its floor has zero predictive witness deficit.
- **Route use:** at each audited checkpoint, apply the fixed legal-donor interventions to all arms and score damage relative to that checkpoint’s unaltered predictions. An inactive route must have **zero effect** in its single-route arm. Run exact forced-A and forced-raw mode-law oracles, plus a constant-row null, through the intervention scorer before interpreting any damage bar. For dual, route conflict cannot alone identify preference on consistent inputs, because sums are determined by the records.
- **Spontaneous A readability:** on the **raw-only** model, freeze weights and train predeclared linear and two-layer width-64 probes separately from (a) its per-round raw encoder state and (b) its upper state after that round, starting from a zero upper state. Predict **each of the five exact sums**, reporting held-out per-slot accuracy and cross-entropy. Probe labels train only the probes, never the r8 network. Split by board identity, include unseen legal renderings, and keep all sum values represented in probe training. Run the identical probes and split on the **update-0 untrained carrier first**, on every r8 checkpoint, and on same-width oracle carriers containing the five exact sums. Also report per-slot majority and shuffled-label floors. Require the oracle probes to decode at ≥99% per slot; otherwise the probe family has failed calibration. Claim a training-related gain only where held-out performance improves over the paired untrained carrier with a positive confidence interval. If the untrained carrier is already at the oracle ceiling, mark that slot **unresolvable by this probe**, however well the trained carrier scores.

At the first-hour read, check frozen-A exactness, inactive-route zero effects, oracle/null separation, update-0 probe baselines, online-stream pairing, and falling B training loss. **Futility at 5k:** stop and report an arm as *no detectable B learning* if neither its training loss nor natural-test excess KL has closed at least 10% of its measured update-0-to-oracle gap. Calibration failure stops interpretation of the affected measurement, not the other arms. Keep the fixed 20k endpoint for arms that continue.

### Predeclared reading

| Result | Conclusion |
|---|---|
| A-only learns B faster or passes when raw-only does not | Access to completed A objects helps realize the predictive extension; it does not show spontaneous A formation. |
| Raw-only passes B; only slot-1 A improves beyond its untrained carrier | B-only training organized the rewarded slot-1 information; it did not establish a full five-slot A layer. |
| Raw-only passes B; all five sums improve beyond their untrained carriers | Evidence that B-only training also made full A readable in those states. Probe readability alone does not establish causal use of that A representation. |
| Raw-only passes B; no sum improves beyond the untrained carrier | B was learned without measured new A readability; report any high baseline decodability explicitly. |
| Dual outperforms both single routes | Access to both routes helps under this architecture. Use its intervention results to describe reliance, with the deterministic overlap caveat. |
| Equal-law shows a witness split or route-dependent predictive gain | Control failure; with zero mode deficit, no strict predictive-extension claim from that run. |

There are 18 runs: three routes × two laws × three seeds. Fixed inputs are in `evidence/panels/`. Registered settings and source identities are in `registration.json`.
