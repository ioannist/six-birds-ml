# Bibliography verification (2026-10-01)

Author lists were checked against the primary arXiv abstract pages for the
following identifiers (the links in `references.bib` locate each page):
2006.12433, 2006.07710, 2011.09468, 2006.00995, 1909.03368,
2303.02536, 2210.13382, 2406.03689, 2207.02098, 2301.05217,
2209.10652, 2102.12452, 2005.00719, 2106.02997, 2202.05262,
2004.07780, 1503.02531, 2001.06782 and 1612.00796.
The corpus titles remain verbatim from the recorded paperclip metadata.

Part 2.1 was checked against the [ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/f3064f7a0ca2328ecb41a3aef6177d68-Abstract-Conference.html):
Tian Ye, Zicheng Xu, Yuanzhi Li, Zeyuan Allen-Zhu, in that order.
Other corrections: the Delétang paper includes Li Kevin Wenliang, Chris Cundy
and Joel Veness; Geiger's alignment paper lists Noah D. Goodman. The full
Elhage and Kirkpatrick author lists replace `others`.

## Primary scoped Six Birds reference

Ioannis Tsiokos (2026), *Strict Theory Extension on a Lawful Continuous Cantor
Shell*, DOI [10.5281/zenodo.19189353](https://doi.org/10.5281/zenodo.19189353).
The identifier is recorded in sibling `six-birds-cantor/README.md`; its SHA-256
is `09d82f2ea3f039e7c617ed2bff811f9848488ca877eebaeac63145fbbfe41271`.
The statement location is Section 3.5, **Definability as factorization**,
and Section 6, Theorem 3 (**Strict theory extension on the audited shell**).
Source hashes:

- `paper/sections/03_canonical_object.tex`: `957c639ead56b073cebc6911669cb350b211a2efb68dba5b04863487e4e41c83`.
- `paper/sections/06_strict_extension.tex`: `8790142527a82c8384706d119f15c6cdffab3a931ac132273419746c3e0e58ee`.
- Local `THEORY_INDEX.md`, Section 3.1: `aac02294276e45899064a558672f39f86336402a21f54bc732d4fba96cecebbd`.

The paper uses non-factorization only for **Strictness (of the task)**: the same
neutral completed sum board after off/on histories requires different laws.
No Cantor theorem hypotheses are asserted for the network; no internal strict
layer is inferred. The sibling source statement, not a network certificate,
supplies the definition convention.

## Checks not completed

The SSRN page for Dell'Acqua et al. (4573321) and the publisher page for
McCloskey–Cohen (10.1016/S0079-7421(08)60536-8) returned HTTP 403. Their existing
author records are retained, explicitly not independently verified here.
The Zenodo DOI endpoint was inaccessible to the browser; its identifier and
statement were verified locally in the author's sibling source and theory index,
not by a fresh remote PID query. No DOI for this unreleased manuscript was added.
