# Where Does Jagged Competence Come From?

Ioannis Tsiokos, 2026. [Paper and evidence](https://doi.org/10.5281/zenodo.23094485).

## Run it yourself

**[Open the executable notebook in Google Colab](https://colab.research.google.com/github/ioannist/six-birds-ml/blob/main/notebook/jagged_competence.ipynb).**

See the two-layer task, check the paper's numbers, replay trained networks and
train a small fresh network: quick mode took 106 seconds on one CPU thread after
setup; allow 10–15 minutes for a first hosted run, including download/install.
See [the notebook guide](notebook/README.md) for budgets and qualifications.
If the link fails, [download the notebook](https://raw.githubusercontent.com/ioannist/six-birds-ml/main/notebook/jagged_competence.ipynb),
upload it at [Google Colab](https://colab.research.google.com/), and choose
**Runtime → Run all**. Local Jupyter: open the downloaded notebook in this
checkout and choose **Run All**. [Setup and section guide](notebook/README.md).

The task separates current-board sums from a prediction law that also depends on
earlier boards. Measurements distinguish recoverability, audited computation,
access, preservation and reliable prediction. The source distribution contains
the paper and its r8–r13 experiments.

| Directory | Contents |
|---|---|
| `paper/` | Manuscript, supplement, figures, tables, ledger and build scripts |
| `notebook/` | Executable reader experiment, reviewable source and deterministic builder |
| `src/recombination_promotion/` | Scientific task, models and measurements |
| `scripts/` | r8–r13 entry points and shared sampling/scoring functions |
| `reports/phase11/oldgame_memory/multiround/` | Six study specifications, recorded results and calibrations |
| `evidence/` | Fixed input panels, numerical evidence and frozen dependencies |
| `tests/` | Paper and r8–r13 regression tests |

## Reproduction

Install `paper/requirements-analysis.txt`; training also needs torch (see
`paper/requirements.txt`). PDF builds require TeX Live, `latexmk`, `pdflatex`,
`pdfinfo` and `pdftotext`.

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

`paper/notes/reproduction.md` describes the input and build order. The submitted
release PDFs are retained unchanged. Portable evidence projections identify their
source hashes; correspondence is not distributed as evidence.
The arXiv check builds an archive under `paper/build/` and compares it with a
clean portable-source PDF, separately from the immutable submitted PDFs.

Study commands accept `--device cpu` or `--device cuda` where applicable. Select
accelerators through `CUDA_VISIBLE_DEVICES`; no physical device ordinal is fixed
by the source. Set `SBML_DATA` to an external bulk artifact directory, or use a
study's `--bulk-root` option. The default is `evidence/bulk/` in this checkout.
Study output and restoration semantics are specified by each CLI (`--help`).

Original code is MIT licensed (`LICENSE`). The manuscript, figures and released
original data are CC BY 4.0 (`LICENSE-CC-BY-4.0`). Third-party packages retain
their own licences.
