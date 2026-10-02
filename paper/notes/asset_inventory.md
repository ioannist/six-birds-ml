# Phase 2.4 asset inventory — draft, unreleased

All inputs are the claims ledger, ledger-built data, or manifest-listed,
hash-verified records. Each asset has a `.values.json` receipt naming the
specific source fields and ledger entries. The complete file lists and hashes
are in `figure_assets.json` and `table_assets.json`.

## Main assets

| File | Verified source | Content |
|---|---|---|
| `figures/fig1.pdf` | Ledger `task`, `theory_nonfactorization` | Task only: records, sums, slot-1 category, mode, probability law; same-board witness. |
| `figures/fig2.pdf` | r8/r12/r13 registrations | Shared recurrent architecture and route/loss matrix; probe and swap icons. |
| `figures/fig3.pdf` | Ledger r8/r10 probes, r8 KL/TV; r10 law cases; r12 census; corresponding calibration | Per-seed recovery versus reliability; census categorical misreads by sum. Historical task comparison is explicit. |
| `figures/fig4.pdf` | Ledger r13 noise/access/encoding; saved matched initial audits | Matched changes in target noise, access and encoding, including adverse seeds. |
| `figures/fig5.pdf` | r11 early readouts; hash-verified r13 per-update records and movement ranges | Per-seed exactness versus update and common observed movement; blocked decay control separate. |
| `tables/table1.tex` | Verified r8/r10/r11/r12/r13 endpoint records and probe results | Five-achievement summary, with supported/not supported/not established and support. |
| `tables/table2.tex` | Verified endpoint summaries, corresponding law cases and r8 comparator | Access and supplied-sums reliability, per seed; study-specific support and historical comparisons. |

Draft figure captions are in `figures/captions.tex`; each table includes its
caption. Counts remain integers; table continuous values use five significant
digits, with unrounded source values retained in receipts.

## FIX-FIRST publication layout

There are 16 vector figures and 36 table assets. The main manuscript uses the
two compact main tables and six compact analytical appendix tables
(`tables/compact_{A,B,C,D,E,F}.tex`). The condition matrix is Supplement Table
S1, the complete main comparison S2, history S3, study settings/endpoints
S4–S15, census/support/laws/exposure S16–S19, calibration/interchange S20–S21,
reader summaries S22–S24, geometry S25–S26, erosion summaries S27 and compute S28.
`supplement/table_inputs.tex` fixes those numbers through the table build script.
All nine study/group learning figures are included in the separate supplement;
two representative curves also appear in the analytical manuscript appendix.
Every supplement table names its complete detailed JSON file under
`paper/data/release/`. Those losslessly compressed files retain exact rows,
with a schema README and byte hashes in `release/index.json`. Printed ranges
are descriptive; they do not replace per-cell counts or paired intervals.
The package check enforces a supplement of at most 60 pages without heading-only
pages. Publication-length checks must be repeated after prose drafting; the
scaffold's page count is not a completed-manuscript length claim.

Geometry shows only the two recorded prediction-loss conditions, sampled and
probability targets. Empty requested series refuse building. Scoped table marks
are derived from counts, floors and convergence; computation refers to the
audited output. r11 law maxima and the r9 non-assessment label are retained.
The original task's 0.02 law bar and r10's original 0.05 / equal 0.02 bars have
different support, explicitly stated in the figure and table captions.

The clean package check covers both PDFs and their transitive dependencies.
External table previews accompany the figure previews; no PNG is included in
the manuscript source or public vector assets.

## Appendix assets

- `figures/appendix_C_methods.pdf`: probe and swap procedures; r10 calibration authority.
- `figures/appendix_D_r8.pdf`, `appendix_D_r10.pdf`, `appendix_D_r12.pdf`:
  recorded per-seed curves, original and equal laws separately.
- `figures/appendix_D_r11_{rarity,dose,erosion}.pdf` and
  `appendix_D_r13_{noise,access,encoding}.pdf`: all recorded condition/seed curves.
- `figures/appendix_E_geometry.pdf`: fixed supplementary cutoff discrimination
  at 0/5k/20k, with negative controls and exact ceilings.
- `tables/prepared_r{8,9,10,11,12,13}.tex`: registered sampling/training/criteria;
  r9 is explicitly read-only, without a training endpoint.
- `tables/appendix_B_r{8,9,10,11,12,13}.tex`: complete condition/seed matrices,
  including equal-law controls; source is the verified full control tables.
- `tables/appendix_B_{census,support,laws}.tex`: four-rendering census,
  sums/supplier/local-history/saved-r9 counts, and case-wise law errors.
- `tables/appendix_B_r10_coverage.tex`: current versus remembered value exposures.
- `tables/appendix_C_{calibration,interchange}.tex`: named scalar calibration
  summaries and fixed-pair interchange support/selectivity. Full arrays remain
  in the hash-bound archive rather than being expanded into TeX.
- `tables/appendix_D_erosion.tex`: exact starts, update 1, minima and endpoints;
  every saved update and movement count remains in its released detailed file.
- `tables/appendix_E_probes.tex`, `appendix_E_r11_probes.tex`,
  `appendix_E_r12_probes.tex`: both carriers/readers, slot-wise counts, floors,
  paired gain intervals and fit status.
- `tables/appendix_E_{original_geometry,geometry}.tex`: original support gaps
  and separate supplementary outcomes, distances and rendering variation.
- `tables/appendix_A_history.tex`, `appendix_F_compute.tex`: manifest history
  and recorded compute measurements, respectively.

## Rebuild and limitations

`build_figures.py` builds 16 vector PDFs and external 150-dpi inspection PNGs;
`build_tables.py` builds 36 TeX tables and 28 detailed JSON files. Both `--verify-rebuild` checks pass with
byte-identical assets and receipts on the recorded tool versions. The isolated
public package rebuild reproduces every PDF/table and its numeric rows without
access to the original checkout. Cross-version byte identity is not promised.

Every figure is 6.5 inches wide with Latin Modern Roman / Computer Modern math
text of at least 7 pt;
plain exponent notation avoids smaller log-axis superscripts. Tables use 8 pt
text and width-bounded columns, without shrinking the typeset font.

Recorded gaps remain explicit. In particular, the main endpoint table retains
the original endpoint-summary fields; r8's later census is in the r9 appendix
table. The r10 task has no corresponding first-slot-category misread measure.
MLP fits have fixed budgets, not assessed solver convergence. The original
geometry support gaps are not repaired by the separate supplementary panel.
Nothing here supplies a new training run, a new network evaluation or a stronger
inference than the registered studies and approved interpretation.

## Layout and audit conventions

Panel letters identify every multi-panel asset. Shared legends occupy reserved
space outside axes and titles, checked by the build. Inequality glyphs use math
typesetting; ranges use en dashes. Version and loss names follow the glossary.
The main task diagram now includes the preceding mode and probability bars;
the architecture attaches the sums output and loss. Recovery/average-error and
specific-failure columns are separate. Condition-coloured axis labels act as
direct colour keys in the mechanism figure.

The r11 erosion records distinguish the exact update-0 full-board audit from the
sampled early readouts at updates **1, 5, 10, 50 and 100**. All six original-law
starts have board-vector accuracy **1.0**. The plotted update-0 marker is bound to
that saved audit, not supplied by the oracle line; an inexact start would refuse
the build. Symlog update axes separate 0 from 1. No scientific value has changed.
