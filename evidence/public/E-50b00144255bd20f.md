# Public scientific registration

This is a public projection. Complete numerical settings, source identities and registered criteria are recorded in `registration_build_v1.json`.

## r10 registered design: can a free network form and use A?


### Three claims to register

1. **Interface.** The lower interface is the current five-sum board \(a_t\). The higher predictive interface is \(B_t=(a_t,e_t)\). It is *strict* in the scoped non-factorization sense: histories can end at the same \(a_t\) but have different \(e_t\) and different next-board laws. This is the fiber witness of Foundations III, Theorem 12 (cited in the manuscript bibliography); strictness alone does not certify neural realization or closure.
2. **Lower objects.** Every component of \(e_t\) is updated from the history of completed A sum boards, never from a supplied mode label.
3. **Pathway.** The empirical claim is that the free B-only network makes all five sums readable **and** that replacing an identified slot-\(k\) component of its internal state changes B according to that slot’s donor value. Readability, causal use, and exact B prediction are separate gates.

### Smallest B change that rewards exact sums in every slot

A count of five L/N/H categories would cover all slots but would **not** reward distinctions between exact sums within a category. Use the same four-record, five-slot game and a public query \(J_t\in\{1,\ldots,5\}\), sampled uniformly. Let \(V\) be the 36 legal sum values and \(i(v)\in\{0,\ldots,35\}\) their fixed order. Set
\[
e_{0,k}=0,\qquad
e_{t,k}=\begin{cases}a_{t,k},&a_{t,k}>0,\\e_{t-1,k},&a_{t,k}=0.\end{cases}
\]
After round \(t\), predict the next board category \(Q_{t+1}=(\sum_k a_{t+1,k})\bmod3\), with law
\[
P_v=\bigl(.10+.07\lfloor i(v)/6\rfloor,\;
          .10+.07(i(v)\bmod6),\;
          .80-.07[\lfloor i(v)/6\rfloor+(i(v)\bmod6)]\bigr),
\quad v=e_{t,J_t}.
\]
These are 36 distinct, positive three-category rows; the minimum pairwise TV is 0.07. Draw the next **legal** board conditional on its \(Q\). The equal-law control uses \(P_v=(1/3,1/3,1/3)\) for every \(v\). The model receives records and \(J_t\), and its B target is only \(Q_{t+1}\); it never receives \(e_t\), \(Q_t\), or a future board as input.

This changes the r8 category law and adds the public query. Keep r8’s online episodes, batch 256, AdamW \(3\times10^{-3}\), weight decay .01, seeds 0–2, and original/equal arms. Use eight active training rounds and twelve test rounds. The old “stop before N³” rule does not apply to this vector mode; test eight-round holds explicitly.

**Coverage is a gate, not an assumption.** The legal boards split by \(Q\) into **8,115 / 8,140 / 8,180**. Within each \(Q\), draw half the boards uniformly and half by first choosing uniformly a supported \((k,v)\) pair, then a legal board with that slot value and \(Q\). There are 150 supported pairs per \(Q\). Since every \(P_v(Q)\ge .10\), each legal slot-value pair has probability at least **1/3,000 per active round**, and at least **1/15,000** of being both present and publicly queried. Register the exact \(5\times36\) conditional-frequency table computed from this finite sampler; record observed training and test counts as well. If an evaluation cell lacks its declared minimum observations, report it as uncovered. This mixture changes board selection, not the records game.

### Arms and signals

| Arm | B input | Training targets |
|---|---|---|
| **Free** | Raw per-round records and public \(J_t\); recurrent state across rounds | Next \(Q\) only |
| **Free + A** | Identical network and initialization | Next \(Q\), plus five current exact sums with coefficient 1 |
| **Frozen-A dual, A-forced** | Hard answers from the verified frozen A core; raw encoder exists but its route to the B head is clamped | Next \(Q\) only |

The last arm is the **known-use positive control** for interchange. The untrained free network and an alignment fitted to shuffled A labels are null controls. All trained arms share each seed’s board/query stream and initial common parameters. No probe or mode labels update the free B-only network.

### Measurements and causal test

Audit at **0, 1k, 2k, 5k, 10k, 15k, and 20k**; retain the fixed 20k endpoint and report first audited crossing. Before training, walk the exact state-machine oracle through natural, held-out board, held-out rendering, same-current-board witness, and eight-round hold panels. Measure its zero expected KL and exact transition law. Run an untrained network and a mode-blind predictor on the same panels as floors. Register a B pass as natural and covered-value KL at most **10% of the measured mode-blind gap**, maximum constructed-law TV at most **0.05**, and passing same-board/different-history witnesses. Abort interpretation if the oracle and floor fail to separate.

First measure base-carrier decodability at update 0. At every audit, freeze the network and fit the same predeclared linear and small-MLP probes for each **exact 36-way sum** and its L/N/H category, at the per-round raw state and the post-round upper state. Probe labels train only probes. Use disjoint board identities where possible and held-out renderings throughout; report values **28–36 separately**, because some have only one legal board per slot and cannot support a board-disjoint train/test claim. Calibrate every probe family on an exact-A oracle carrier and compare paired held-out gains with the untrained carrier, majority floor, and shuffled labels, with confidence intervals. A full-A readability claim requires a gain for **each slot**, its calibrated positive, and explicit coverage of the rare-value scope.

For **use**, fit an orthogonal alignment of the frozen 16-dimensional per-round raw state into five three-dimensional slot blocks plus one residual dimension. Fit it and its A decoders using **training boards only**; fix rank and fitting budget before test. The engineered, randomly rotated exact-A carrier must pass both decoding and patching calibration. For each held-out slot \(k\), pair legal base and donor boards whose other four sums are identical and whose nonzero \(k\)-sums give oracle rows at least 0.07 TV apart. Start from the **same prior upper state**, keep the public query at \(J_t=k\), replace only aligned block \(k\) with the donor block, and score the fraction of predictions closer to the donor’s exact \(P_v\) than the base’s, alongside absolute TV to both rows. Require the unpatched base and donor predictions to be accurate; report eligible-pair counts for every slot. Check that probes of the other four slots do not change after patching. The frozen-A positive patches its executed slot-\(k\) answer; the untrained and shuffled-alignment nulls undergo the identical pairing. Pre-register donor-follow ≥0.80 for each covered slot **only if** the measured positive reaches ≥0.95 and both nulls remain ≤0.20; otherwise that slot’s intervention is uncalibrated. A failed alignment is **unresolved**, not evidence that A is absent.

The first-hour read checks the oracle/floor separation, exact frequency table and observed coverage, paired streams, frozen-A positive, update-0 probes, and initial B-loss/KL movement. At 5k, stop an arm for futility if **neither** training loss nor natural KL has closed 10% of its measured update-0-to-oracle gap. Preserve its negative result.

### Outcome-to-conclusion rules

| Endpoint pattern | Three-claims reading |
|---|---|
| Free B passes; five exact sums gain readability; five calibrated slot patches follow donors with no other-slot leakage | The strict predictive **interface** is realized; its **lower objects** are A-board histories; the free network shows **operational A-mediated use** on covered legal support. |
| Free B passes and A is readable, but patches fail or are uncalibrated | Interface and task pass; the **pathway remains unresolved**. |
| Free B passes with only categories, or fewer than five exact sums, readable | The network uses a sufficient **quotient of A**; no full exact-A claim. |
| Free B fails while Free + A or A-forced passes | Access to A helps this architecture; spontaneous formation/use is **not established** at this endpoint. |

The deterministic relation from raw records to A remains explicit: even successful interchange establishes a causal **identified subspace under this alignment and intervention**, not a unique internal theory.

### Build and compute


There are 18 trained runs: three arms × two laws × three seeds. Recorded timings are in the run summaries.


**Scope of the answer.** r10 can test whether a network trained only to predict B develops a readable, causally used representation of the five sums on the **legal board support**. It cannot establish a unique internal decomposition: a distributed computation can implement the same law without five separately identifiable variables. The verdict must say “A-mediated under the registered alignment” or “unresolved,” never infer an abstract A layer from a probe alone.

