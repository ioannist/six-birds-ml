# Scientific interpretation of r8–r13

Public scientific synthesis; paragraph numbering is retained for the explicit claim mappings.

**The studies separate five achievements that are often treated as one: making a lower result recoverable, computing it, giving prediction access to it, preserving it under further training, and producing reliable predictions; progress on one did not guarantee the others.**

A **lens** means the distinctions an observation retains. In the original game, the five sums are a lens on one board. Prediction needs history: the same neutral board can follow an off or on history and require different probabilities. Prediction is therefore a strict extension relative to the current board’s sums. This describes the task, not a demonstrated layer inside the network. Its exact update needs only slot 1’s cutoff category and the previous hidden state, rather than all five exact sums.

Training shapes which information becomes recoverable. When prediction depends only on slot 1, recovery of its sum improves while recovery of other sums declines. In r10’s different all-slots task, recovery improves for all five sums. These findings support task-dependent organization of information, without establishing exact sums computation everywhere.

Target noise contributes, but is insufficient. In r13, exact-probability targets improve average prediction error in every seed and both versions. They nearly remove **records → prediction** misreads in two seeds but worsen them in the third. The disadvantage of **records → prediction+sums** remains. Cutoff enrichment gives inconsistent repair, so rarity alone does not explain the results; missing history practice also matters, as the r11–r12 comparison shows.

Computing or recovering sums does not guarantee their predictive use. Adding sums loss improves the sums output but can worsen prediction. Connecting that output reduces misreads and average error, yet other prediction failures remain. Shared-loss interference remains a possible mechanism rather than an established cause.

Encoding matters. With the same exact sums and matched downstream architecture, one-hot answers outperform the tested numerical encoding: **0/0/2 versus 317/121/10 misreads**. This establishes encoding sensitivity under the tested budget, not a precision ceiling for continuous representations. Separate probes successfully distinguish both cutoff pairs in every probability-target seed, while prediction still fails some tests.

Prediction updates can erode an exact sums computation. Every tested active optimizer loses perfect exactness at update 1, with substantially different severity. Blocking prediction gradients preserves all 1,555 histories through 200 updates despite retained weight decay. Erosion therefore does not require AdamW; optimizer, step size, displacement and answer margins still matter.

Correct sums do not guarantee downstream reliability. Supplied conditions pass the registered prediction tests in some runs and fail in others. Residual failures need separate diagnosis: they can involve the history update, probability readout, rendering response or swaps. Better board responses and better history behavior are distinct achievements.

Two measurement cautions are central. **Average error can hide specific failures:** r8’s **records → prediction** networks have ordinary KL errors of approximately **0.00007–0.00030 bits**, yet none passes every registered prediction test. **Probes can recover information without establishing that prediction uses it:** r10’s high sum recovery coexists with failed selective swaps. Neither averages nor probes are misleading when interpreted within their scope; the mistake is treating them as evidence of complete reliability.

“Jagged intelligence” is useful here as a description of high average competence alongside concentrated, sometimes surprising failures. It is not itself an explanation. Constructed tests reveal incomplete reliability without estimating how frequently those failures occur in ordinary use.

Within this game and budget, supplying exact sums as discrete input was the most reliable route tested. In r12’s matched comparison, **records+sums → prediction** achieves **2/3 passes and 0–1 misreads**, versus **0/3 passes and 473–815 misreads** for **records → prediction+sums**. r13 supports the same access advantage. Connecting learned sums improves prediction, but none of those connected runs passes every registered test.

Beyond this game, the findings motivate tests: whether cleaner targets improve particular distinctions, whether structured intermediate inputs improve reliability, whether auxiliary outputs are used, and whether downstream training preserves earlier computations. They do not establish universal prescriptions for distillation, tools or protected pathways.

The evidence comes from one game family, small recurrent networks, three seeds and fixed training budgets. Passing the registered tests does not establish correctness everywhere. The studies demonstrate separations among the five achievements; they do not yet provide a general explanation of jagged intelligence.
