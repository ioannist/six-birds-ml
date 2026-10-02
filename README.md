# Where Does Jagged Competence Come From?

Repository for the paper

> Ioannis Tsiokos. *Where Does Jagged Competence Come From?* Preprint, 2026.
> Zenodo DOI: [10.5281/zenodo.23094485](https://doi.org/10.5281/zenodo.23094485)

The paper and its supplement are in `paper/`.

Capable systems often show *jagged competence*: low average error alongside
failures on particular inputs. The paper studies where this comes from in a
task built from two known layers: a lower layer A that computes five per-slot
sums from records, and an upper layer B that predicts the next board's
category from the slot-1 sum and a mode carried over from earlier boards, so
that B is a strict extension of A. Small recurrent networks are trained on B,
and their acquisition of A is measured against exact ground truth. The central
finding is that learning B gives the network only a jagged version of A, and
that uneven acquisition, access and preservation of A explain part of B's
jagged competence.

The code, study outputs and the scripts that rebuild every number, figure and
table in the paper are being prepared for release here and will follow shortly.

## Licence

Code: MIT (`LICENSE`). Manuscript, figures and data: CC BY 4.0 (`LICENSE-CC-BY-4.0`).
