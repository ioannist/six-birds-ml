# Reproduction

The distributed numerical evidence rebuilds the claim–evidence ledger without
an accelerator. Sources are pinned explicitly; an ordinary check cannot change
a pin or a stated value. The standalone package test rebuilds the same values
using only the public package and its manifest.

```sh
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python paper/scripts/build_ledger.py --check --verify-all
python paper/scripts/build_figures.py
python paper/scripts/build_tables.py
python paper/scripts/check_package.py
python paper/scripts/build_arxiv.py --public-source
python paper/scripts/build_arxiv.py --public-source --check
PYTHONPATH=src:. python -m pytest tests/test_paper_writeup.py tests/test_paper_assets.py tests/test_oldgame_multiround*.py
```

After an intentional edit: edit → explicit pin → assets → local PDF build →
arXiv package → tests. Pin with `python paper/scripts/build_ledger.py --pin`.
Asset receipts bind the resulting ledger hash; pinning after an asset build
makes its receipts stale. Sources and measurements are checked independently.

Build both PDFs with `cd paper && latexmk -pdf main.tex` and
`latexmk -pdf -jobname=supplement supplement/supplement.tex`. Local builds do not
replace the submitted PDFs in `submission/artifacts/`. The optional
`refresh_writeup.py --release-tool PATH` accepts an externally installed
`paper_build_release.py`; the toolkit is not a source or TeX dependency and the
script invokes its local build operation only.
For the public source distribution, `build_arxiv.py --public-source` writes only
under `paper/build/`: its reference PDF is compiled from portable sources. This
does not assert text equality with the immutable submitted PDFs, which retain
historical hardware wording.

## Data and devices

`SBML_DATA` names the bulk artifact directory; its default is this checkout's
`evidence/bulk/`. Evidence paths use `repo/` and `bulk/` archive-relative
references. CUDA selection uses `CUDA_VISIBLE_DEVICES`, independently of the
scientific seed and sample streams. CPU linear-probe fitting uses one thread;
evaluation remains float32 as registered.

Fixed independent board/rendering panels: `evidence/panels/`. Frozen name
resolver and complete held-out audit: `evidence/gate_A/`. The single parent sums
checkpoint has the repo-relative location specified by the studies. Concise
public scientific specifications replace correspondence. Numerical values and
checkpoint tensors are preserved.

Analysis and historical CUDA requirements are pinned separately. CPU torch
suffices for evidence tests, without claiming bitwise GPU continuation. Actual
historical commands/hardware are explicitly unknown where not recorded.
Exact counts, sampled supports, constructed histories and supplementary panels
remain separate. Probe intervals describe board resampling, not training-seed
variation. Calibration is not a trained-network achievement.
