# Notation and terminology (glossary)

Each concept has exactly one name. The paper, captions, tables, ledger use only these terms. A term not listed here is introduced in the text once and added here.

## Task
- **Record:** one (slot, mass) item. The six masses are 1/6, 1/4, 1/3, 1/2, 2/3 and 3/4. A **board** is the sequence of 4 records placed in 5 **slots**.
- **Completed sum board:** the vector of five per-slot totals. Many record sequences realize the same completed sum board. The census enumerates all **24,435** completed sum boards.
- **Rendering:** one realization of a completed sum board as records: the decomposition into legal masses and the record order, plus the names and template where the study actually executed them. The same completed sum board has many renderings.
- **Sums:** the five per-slot totals of a board, in integer twelfths. The attainable values are **0 and 2–36** (36 values). Computing the sums is **task A**.
- **Slot-1 category:** L when slot 1's sum is ≤ 12/12, H when it is ≥ 24/12, and N otherwise.
- **Mode:** the task's binary on/off variable. An H board switches it on, an L board switches it off, and an N board leaves it unchanged. "Mode" always means the task variable. The network's activations are **internal states**, never "mode".
- **Prediction:** the network's probability vector over the next board's category. Predicting it correctly is **task B**.
- **Law:** the true next-category distribution: (½, ¼, ¼) when the mode is off and (¼, ¼, ½) when it is on.
- **Equal-law control:** the same task with (⅜, ¼, ⅜) in both modes, so the mode is irrelevant. Categorical misread signatures are undefined under the equal law.
- **Task layer:** a specified computation in the task's construction; distinct from an architectural layer or an established internal representation.
- **Layer A (lower computation):** records → the five current-round sums. An **A object** is a completed sum board.
- **Layer B (upper computation):** the stateful computation over A objects that updates the mode from the slot-1 category and produces the next-category law. r10 retains A and uses a different upper rule.
- **Strict extension (of the task):** B does not factor through the **current** A description (non-factorization only), witnessed by histories with equal current A values and different B laws. No retention requirement: B need not contain A, and A need not be recoverable from B. A property of the **task**, never of the network; defined once in §3.2 with citations.
- **Designed decomposition:** the task's specified A/B relationship.
- **Learning hypothesis:** final-output training induces the lower computation and builds the upper computation on it. The programme's working hypothesis, motivated by Six Birds (Foundations I §1.1, arXiv:2602.00134); the studies measure evidence bearing on it, not a certificate of internal layering.
- **The all-slots task (r10):** a different task. For each slot the task remembers the **last nonzero sum**, which is kept through rounds where that slot's sum is zero. The law depends on the remembered value of a publicly queried slot (36 laws). Its equal-law control is uniform (⅓, ⅓, ⅓). The name is always "the all-slots task".

- **Jagged competence:** high average competence alongside specific failures (low natural KL next to constructed-history and census failures). It is the phenomenon the paper explains in this task; it is never its own explanation.

## Versions
Each name states the input, an arrow, and what the loss is computed on.
- **records → prediction:** input is the records; the loss is on the prediction only.
- **records+sums → prediction:** input is the records plus exact sums from a frozen sums network (one-hot unless stated); the loss is on the prediction only.
- **records → prediction+sums:** input is the records; the loss is on the prediction plus an extra **sums output**, read from the shared state.
- **Connected (frozen / live):** a records → prediction+sums network whose sums output is also fed to the prediction. *Frozen* uses a fixed copy; *live* uses the training sums output.
- **Numerical encoding:** exact sums given as (s/36, 1 − s/36), padded to the one-hot width.
- **Probability targets:** the loss uses the exact next-category law instead of one sampled category.
- **Erosion continuation:** training that starts from an exact sums network. **B-only** updates on the prediction loss only; **A+B** also keeps the sums loss.

## Asset version/variant labels

These are the allowed complete condition labels in figures and tables. A study
prefix, seed and law may qualify them. Coverage and loss variants do not define
new architectures. The sums-route-only controls mask records at the prediction
interface. Optimizer names below qualify the erosion experiment only.

- **records → prediction**
- **records+sums → prediction**
- **records → prediction+sums**
- **Connected (frozen)**
- **Connected (live)**
- **records+sums → prediction (sums route only)**
- **records → prediction (uniform sampling)**
- **records → prediction (cutoff coverage)**
- **records → prediction (decoy coverage)**
- **records+sums → prediction (exact supplied)**
- **records+sums → prediction (one-hot encoding)**
- **records+sums → prediction (Numerical encoding)**
- **records → prediction (sampled targets)**
- **records → prediction (Probability targets)**
- **records → prediction+sums (sampled targets)**
- **records → prediction+sums (Probability targets)**
- **records → prediction (Erosion continuation)**
- **records → prediction+sums (Erosion continuation)**
- **records → prediction+sums (sums dose 1%)**
- **records → prediction+sums (sums dose 10%)**
- **records → prediction+sums (sums dose 100%)**
- **AdamW**
- **reduced-lr AdamW**
- **SGD**
- **blocked prediction gradient**

## Measurements
- **Natural KL:** KL(law ‖ prediction) in bits on naturally sampled episodes, as in the scoring code (r8 `oldgame_multiround_route_access.py`; r10 `oldgame_multiround_allslots.py`). **Unseen KL** is the same quantity on each study's tracked unseen board combinations; the support differs by study.
- **Scope of the next three definitions:** they apply to the original task (r8, r9, r11, r12, r13). The all-slots task (r10) uses its own panels and bars, defined in Appendix B.
- **Law panels:** constructed histories (L/H anchors followed by N¹–N⁸), scored by **law TV**, the total-variation distance between prediction and law. The **short panel** is L/H and N¹–N²; the **long panel** is N³–N⁸. The bar is 0.02.
- **Census:** all 24,435 completed sum boards, in 4 fixed renderings, plus the saved r9 renderings.
  - **Categorical misread:** a board whose two-context prediction signature (its predictions after the established off history and after the on history) is closest to the template of the wrong slot-1 category. Templates are the L, N and H signatures under the two anchors.
  - **TV-error count:** a board whose maximum prediction TV over those two contexts exceeds 0.02. It is a different measure from a misread; the two are never merged.
  - **Cutoff band:** slot-1 sums 11–13 and 23–25 (930 completed sum boards); the rest are the **other boards** (23,505).
- **Pass (B pass):** the run meets every prediction criterion registered for its study, at that study's fixed endpoint. It is not exhaustive correctness.
- **Probe:** a separate classifier fitted after training on frozen internal states. It predicts a sum or category from them. **Recoverable** means a probe recovers the quantity above its floors. Recoverable is never used to mean "used".
- **Floors and ceilings:**
  - the untrained network;
  - the majority class;
  - shuffled labels;
  - the board-only predictor (uses the current board alone);
  - the exact oracle (the ceiling).
- **Swap test:** an aligned block of internal state for one slot is copied from a donor board.
  - **Donor-follow** is the fraction of swaps in which the prediction follows the donor.
  - **Selectivity** holds when no other slot's decoded sum changes.
  - The controls are the trained positive, the no-op swap and the shuffled alignment.
- **Used:** a quantity is used by the prediction only when a calibrated, selective swap test or a matched connection or encoding comparison supports it.
- **Local exactness:** the fraction of the **1,555 local histories** (the per-slot sum computation) for which the sums output is exactly correct.
- **Board-vector exactness:** the fraction of the 24,435 completed sum boards whose full five-sum vector is correct. In r11, the early readouts used a sampled panel of boards.
- **Cumulative movement:** the sum over updates of the Euclidean norm of each parameter step of the sums network.

## Studies
- **r8–r13:** registered studies. Their follow-ups, corrected audits and supplementary analyses are labeled in Appendix A. **Matched** means identical code, data stream, initialization, update count and panels, differing only in the stated factor; every other comparison is **historical**.
- **Seeds:** 0, 1 and 2 in every condition. Per-seed values are written in seed order, e.g. "58 / 328 / 87".

## The five achievements (in realizing the designed decomposition; neither sequential stages nor the definition of strictness)
1. **Recoverability:** a probe can read the quantity.
2. **Computation:** an output computes it exactly.
3. **Access:** the prediction receives it.
4. **Preservation:** it survives further training.
5. **Reliable prediction:** every registered prediction criterion is met.
