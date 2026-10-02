# r9: saved-network raw-route diagnosis

This is an inference-only study of the original-law r8 20,000-update checkpoints. `results.json` binds each checkpoint by SHA-256 and verifies the replayed prefix and swap maxima against its saved r8 audit. The board census contains all 24,435 legal boards, with one deterministic legal record rendering per board; the failed-panel analyses instead use the **exact saved renderings**. A board's operational category is determined by its one-round effect after both an established L state and an established H state: `(p0,p0)` means L, `(p0,p1)` means N, and `(p1,p1)` means H. This is a measurement of the upper network's effect, not a separate trained category reader.

| Seed | Raw-only category confusion, L/N/H rows and columns | Misread boards | Boards above TV 0.02 | A-only / dual misreads |
|---:|---|---:|---:|---:|
| 0 | `[[22488,3,0],[3,1830,2],[0,0,109]]` | 8 | 69 | 0 / 0 |
| 1 | `[[22488,3,0],[0,1834,1],[0,0,109]]` | 4 | 25 | 0 / 0 |
| 2 | `[[22488,3,0],[0,1835,0],[0,0,109]]` | 3 | 66 | 0 / 0 |

The sum-resolved counts in `results.json` show the boundary concentration. For distance at most one twelfth from either cutoff (930 boards), raw-only seeds 0/1/2 have 5/4/3 categorical misreads and 34/20/61 TV-limit failures. At distance at least four twelfths (20,573 boards), they have no categorical misreads and only 5/0/1 TV-limit failures. All 109 H boards classify as H in this one-rendering census, although seed 0's saved H-at-24 swap has TV 0.029: a correct category signature need not meet the stricter probability bar.

| Saved-panel failure | Raw-only TV, seeds 0/1/2 | Same rows: A-only TV | Same rows: dual TV | Direct observation |
|---|---:|---:|---:|---|
| Worst `L_N5` row 348 | 0.250 / 0.255 / 0.256 | 0.006 / 0.004 / 0.006 | 0.006 / 0.004 / 0.005 | The first N board is ID 24301, sum 23/12: its **saved rendering** acts as H in all raw-only seeds, and the error appears immediately after it. |
| Worst `L_N8`, seed 0 | 0.250 | 0.007 | 0.006 | Initially accurate through five N rounds; the sixth N (sum 21/12) raises TV to 0.093, and subsequent N rounds raise it to 0.250. Its isolated category signature remains N: a state-dependent neutral response. |
| Worst `H_N8`, seed 2 | 0.230 | 0.003 | 0.002 | The fourth N has sum 13/12 and raises TV from 0.006 to 0.092; later neutral rounds raise it further. Its isolated signature remains N. |

The same-scenario swap comparisons also localize the failure. Seed 0's `neutral_N` uses board 22546 (sum 13/12) and has TV **0.141 / 0.010 / 0.010** for raw-only / A-only / dual; its same-category N-to-N substitution differs by **0.117 / 0.0003 / 0.0005**. Seed 2's corresponding board 22616 (sum 13/12) has `neutral_N` TV **0.237 / 0.005 / 0.006** and substitution TV **0.110 / <0.0001 / 0.0002**. Seed 1's substitution is smaller but still fails, at TV **0.022**. The saved `upper_state_exchange_same_N` failures use those same near-boundary N boards; seed 0 also has a set-H probability error at sum 24/12 (TV **0.029**). Every failed saved prefix and swap case is itemized in `results.json` with its first threshold exceedance or scenario, an operational evidence class, board identities, sums, render-specific one-step effects, and comparison values for all routes.

To isolate recurrence from near-cutoff inputs, 32 fixed seeded sequences use only clear-N boards with slot-1 sums 16–20/12. At length eight after L, maximum TV is **0.115 / 0.017 / 0.013** for raw-only seeds 0/1/2, versus at most **0.008** for A-only and approximately **0.006** for dual on the same sequences. Seed 0 therefore also has measurable neutral-run drift; seeds 1 and 2 do not show an overall clear-N drift at the registered 0.02 limit.

## Training-signal frequency and scope

The exact board census is L/N/H = 22,491/1,835/109. The natural sampler selects N with probability 1/4 at an active round, then selects uniformly among 1,835 N boards: a particular N board has probability **1/7,340 = 0.0136% per active round**. A particular H board has probability **0.25/109 to 0.5/109** per active round, depending on the current mode; the much larger L population gives each L board probability **0.25/22,491 to 0.5/22,491**. The implicated ID 24301 occurs **5 times in 60,000 active natural-test rounds**, while the constructed `L_N5` panel deliberately includes it as the first N in its worst row; board 22546 occurs 5 times naturally and 3 times in the constructed prefix panel. An unconstrained five-N run would occur with probability `(1/4)^5 = 1/1,024`, but the actual online training stream stops *before* its third consecutive N input, so N³–N⁸ continuations have **zero training examples**; the constructed panel assigns 32 rows to each starting mode and run length. These are exact sampler/panel frequencies, not an estimate from retraining.

## Conclusion

The principal raw-only failure is a sparse, rendering- and context-sensitive approximation to the slot-1 category transition: a sum-23/12 neutral board can act as H, while near-boundary neutral boards that retain the correct isolated category can still shift the prediction enough to fail the probability and substitution bars. Repeated clear-neutral inputs expose additional drift in seed 0, but not in seeds 1 and 2, so neutral-run length alone does not explain the three-seed failure. A-only and dual largely suppress these errors on the *same* saved histories; this comparison identifies an access advantage for completed A answers under these networks, not a claim that raw records lack the required information. The board census uses one legal rendering per board, while every causal attribution to an r8 failure uses that failure's saved rendering.
