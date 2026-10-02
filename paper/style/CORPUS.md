# Style corpus (phase 1)

Retrieved through the paperclip arXiv source on 2026-10-01 and collected in the paperclip repo `sixbirds-jagged-exemplars`. The repo was committed with all 12 papers; the saved listing is in `paperclip_repo_status.txt`. All 12 papers are available in full text in paperclip. The extraction notes are in `exemplars/arx_<id>.md`.

**Exact titles and source pins.** The exact source titles, as given in paperclip metadata, are recorded verbatim in `source_pins_verbatim.md`. The titles in the table below are display titles; where a display title differs from the source title it is marked as paraphrased. The arXiv version read **cannot be identified**, because paperclip metadata has no version field. Each extraction is therefore pinned by retrieval date and by the SHA-256 of the full text in `source_pins_verbatim.md`. Venue data are as published in the proceedings.

## Primary empirical style models (12)

| # | arXiv ID | Title | Published version | Why it is in the corpus |
|---|---|---|---|---|
| 1 | 2006.12433 | What shapes feature representations? Exploring datasets, architectures, and training (Hermann & Lampinen) | NeurIPS 2020 | Controlled synthetic features; what training makes decodable vs suppressed (our r8/r10 recoverability result) |
| 2 | 2006.07710 | The Pitfalls of Simplicity Bias in Neural Networks (Shah et al.) | NeurIPS 2020 | Synthetic datasets that isolate a learning bias; average accuracy hiding reliance on shortcuts |
| 3 | 2011.09468 | Gradient Starvation: A Learning Proclivity in Neural Networks (Pezeshki et al.) | NeurIPS 2021 | Mechanism-level account of what the gradient builds; theory paired with controlled experiments |
| 4 | 2006.00995 | Amnesic Probing: Behavioral Explanation with Amnesic Counterfactuals (Elazar et al.) | TACL 2021 | Separates decodable information from used information (our probe vs swap test) |
| 5 | 1909.03368 | Designing and Interpreting Probes with Control Tasks (Hewitt & Liang) | EMNLP 2019 | Calibrated probe interpretation (selectivity, control tasks), as in our shuffled and untrained floors |
| 6 | 2303.02536 | Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations (Geiger et al.) | CLeaR 2024 | Interchange interventions on learned alignments (our swap test); chosen as the Geiger representative |
| 7 | 2210.13382 | Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task (Li et al.) | ICLR 2023 | Synthetic task with full ground truth; probes plus interventions |
| 8 | 2406.03689 | Evaluating the World Model Implicit in a [sequence] Model (Vafa et al.; title paraphrased) | NeurIPS 2024 | High average performance coexisting with failures on constructed tests |
| 9 | 2207.02098 | Neural Networks and the Chomsky Hierarchy (Delétang et al.) | ICLR 2023 | Controlled recurrent tasks; structured out-of-distribution length tests; seed reporting |
| 10 | 2407.20311 | Physics of Language Models: Part 2.1, Grade-School Math and the Hidden Reasoning Process (Allen-Zhu & Li) | ICLR 2025 | Synthetic data with ground truth; probes of hidden intermediate computation. Chosen as the Physics-of-LMs part closest to our probe/use question |
| 11 | 2301.05217 | Progress measures for grokking via mechanistic interpretability (Nanda et al.) | ICLR 2023 | Training-dynamics curves; cautious mechanistic claims combining probes and ablations |
| 12 | 2209.10652 | Toy Models of Superposition (Elhage et al.) | Anthropic / arXiv 2022 | Toy-model method; mixed representations (our r10 swap-test spillover) |

Published versions follow the venue proceedings: NeurIPS 2024 for Vafa et al. and ICLR 2025 for Allen-Zhu & Li are confirmed in their proceedings. Read-version pins are in `source_pins_verbatim.md`.

## Selection decisions

- **Geiger et al.:** the plan left the exact paper open. Chosen 2303.02536 (distributed alignment search) over 2106.02997 (causal abstractions of neural networks), because it learns an alignment and then performs interchange interventions, which is the closest to our swap test. 2106.02997 is cited as a measurement reference.
- **Allen-Zhu & Li:** Part 2.1 (2407.20311) over Part 1 (2305.13673). Part 2.1 probes hidden intermediate computation, which matches our recoverability-vs-use distinction.
- **Substitutions or omissions:** none. Every planned paper was available.

## Measurement references (cited, not style models)

Belinkov 2022 (probing survey); Ravichander et al. 2021; Geiger et al. 2021 (2106.02997); Meng et al. 2022, secondary.

## Framing and mechanism context (cited only)

Dell'Acqua et al. 2023 (jagged frontier); Geirhos et al. 2020 (shortcut survey); Hinton et al. 2015 (soft targets); Yu et al. 2020 (gradient conflict); Kirkpatrick et al. 2017 and McCloskey & Cohen 1989 (continual-learning interference).
