# Executable reader experiment

**[Open in Google Colab](https://colab.research.google.com/github/ioannist/six-birds-ml/blob/main/notebook/jagged_competence.ipynb).**

Choose **Runtime → Run all**. If the link is unavailable,
[download the notebook](https://raw.githubusercontent.com/ioannist/six-birds-ml/main/notebook/jagged_competence.ipynb),
upload it to Colab, and use Run all. Expand any named code cell to see its code.
The notebook contains its runtime: downloading just the `.ipynb` is sufficient.
Outside a checkout it downloads the scientific source at commit
`3c35f5800d758db1fe9594b46648b16756c639f5`, not a moving training implementation.
Inside a checkout it uses the local, hash-verified scientific evidence.
The session receipt distinguishes the hosted source pin from the actual executing
checkout's commit and modified/unmodified status; unpacked source directories are
identified as such rather than assigned the hosted commit.

## What runs

| Section | Computation | Budget / scope |
|---|---|---|
| Setup | Fixed seeds, device selection, minimal dependencies | First hosted run also downloads the source and evidence |
| Two-layer task | Exhaustive 24,435-board census; legal same-board witness | Seconds |
| Paper evidence | Full numerical ledger check; rebuild Figures 1–5 and Table 1 | About one minute on the tested CPU |
| Released networks | Six r8 checkpoints, 30 fresh linear probe fits, full natural/prefix replay | About half a minute on the tested CPU |
| Board census | r12 sums-target network, 24,435 boards × four renderings | Seconds; the uniform-condition figure remains a separately identified saved result |
| Live training | Fresh records → prediction model, no sums loss | Quick: 400 CPU updates / 1,000 CUDA updates. Full: 20,000 updates, batch 256 |
| One-update erosion | Exact parent plus four freshly matched updates; compare saved paper counts | Seconds; fresh CPU and historical CUDA minibatches are not identical |
| Access/encoding | Released per-seed r13 results, including failed criteria | Seconds |
| Summary | Counts, comparison status, versions and section timings | Downloadable JSON receipt |

Quick mode reserves roughly 10–15 minutes on a hosted accelerator, including
download/install time; a Colab T4 timing has not yet been measured. CPU execution
timing was **105.7 seconds on one CPU thread**, excluding download/installation,
with 400 live updates (137.7 updates/s excluding fitting/audits). Sections took:
setup 1.2 s, task 1.1 s, ledger/assets 64.2 s, released probes/predictions 22.7 s,
census 5.0 s, fresh training plus audits 9.6 s, erosion 1.0 s and mechanisms
0.1 s. The test-only 25-update run took 103.2 s: released evidence dominates.
This is not a T4 benchmark or a full-study runtime estimate.
The numerical evidence checks and
released-network fits are identical in quick and full modes. Only fresh training
changes. A short live run may show weaker or noisier effects than the paper; it
is not a substitute for the registered studies or their fixed endpoints.

Local sum-probe fits retain the registered settings: training-only
standardization, class-balanced logistic regression, C=10, tolerance 1e−5,
5,000 iterations; convergence, predictions and 512-board denominators are saved.
Readability is not a demonstration of use. Categorical misreads and TV failures
are separate counts. Class-balanced fitting may score below the majority floor;
lower measured readability does not establish information removal. Fresh erosion
rows describe a different first batch, not a failed replay of a saved paper row.
Every repeated paper number is compared with its ledger
reference; fresh numerical differences are displayed, not silently replaced.

## Local setup

Use Python 3.12 or newer. Install torch for your hardware first (the validated
version is 2.10.0), then the small notebook requirements. Colab already provides
torch; the notebook does not replace its accelerator installation. Local figure
rebuilding needs Latin Modern: install `fonts-lmodern` on Linux, use an existing
TeX installation, or set `SBML_LATIN_MODERN` to `lmroman10-regular.otf`.

```sh
python -m pip install torch==2.10.0
python -m pip install -r notebook/requirements.txt
python -m pip install jupyterlab pytest
python notebook/build.py --check
python -m jupyterlab notebook/jagged_competence.ipynb
```

Choose **Run All**. `SBML_DEVICE=auto` (default), `cpu` or `cuda` controls live
training. `CUDA_VISIBLE_DEVICES` selects your visible accelerator, with no fixed
physical ordinal. Numerical threads are limited to one. `SBML_DATA` optionally
points to an external bulk-evidence directory with the same layout as
`evidence/bulk/`; released checkpoints are still hash-checked. `SBML_REPO`
selects an existing checkout. `SBML_NOTEBOOK_OUTPUT` selects a writable session
directory for receipts, previews and the fresh checkpoint (otherwise temporary).
The manuscript and submitted PDFs are not rebuilt or modified.

## Build and test

`jagged_competence.py` is the percent-format cell source; `runtime.py` contains
the calculations. The standard-library builder embeds the runtime in the first
code cell, with stable cell IDs and no outputs or execution counts.

```sh
python notebook/build.py
python notebook/build.py --check
PYTHONPATH=src:. python -m pytest tests/test_executable_notebook.py -q
# Optional headless calculation run, without a Jupyter server:
SBML_DEVICE=cpu PYTHONPATH=src:. python notebook/jagged_competence.py
```

The nbclient test runs every cell in quick mode, shortening only fresh training
to 25 updates. It checks all task, asset and required ledger comparisons, all 30
released fits, and the four erosion conditions. An additional headless IPython
test exercises every cell where kernel sockets are unavailable; it does not
claim to replace a host/Colab kernel test. `SBML_NOTEBOOK_FAST=1` is solely a test
budget, not the default reader experience.

## Full studies (not launched by Run All)

These are much longer than the reader demonstration. Select an accelerator and
limit each process to one numerical thread. Preserve the released evidence:
the commands write new output trees. Run each registered GPU verification before
training; `--device cpu` is also supported except by the CPU-era r8 entry point,
which is CPU-only. These commands include both original- and equal-law controls.

```sh
export PYTHONPATH=src:.
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p build/full-studies build/full-bulk

# r8: all 18 route/law/seed combinations, 20k updates each (CPU).
for route in a_only raw_only dual; do
  for law in original equal; do
    for seed in 0 1 2; do
      python -m scripts.oldgame_multiround_route_access run --route "$route" --law "$law" --seed "$seed" --output-root build/full-studies/r8
    done
  done
done

# r9: read-only mechanism diagnosis of the released r8 checkpoints.
python -c "from pathlib import Path; from scripts import oldgame_multiround_raw_diagnosis as d; d.OUTPUT=Path('build/full-studies/r9'); d.main()"

# r10: all three arms, both laws and seeds; raw arms width 3, forced width 1.
python -m scripts.oldgame_multiround_allslots verify-gpu --device cuda --verification-output build/full-studies/r10_verify.json
for arm in free free_a a_forced; do
  width=3; [ "$arm" = a_forced ] && width=1
  python -m scripts.oldgame_multiround_allslots run --device cuda --runs "$arm" --chunk-runs "$width" --output-root build/full-studies/r10 --bulk-root build/full-bulk/r10
done

# r11: rarity, dose and exact-start erosion groups.
python -m scripts.oldgame_multiround_jagged verify-gpu --device cuda --output-root build/full-studies/r11_verify
for group in rarity dose erosion; do
  width=3; [ "$group" = erosion ] && width=1
  python -m scripts.oldgame_multiround_jagged run --device cuda --runs "$group" --chunk-runs "$width" --output-root build/full-studies/r11
done

# r12: natural/coverage mixtures, with raw, sums-target and supplied-sums arms.
python -m scripts.oldgame_multiround_coverage --stage verify-gpu --device cuda --verification-output build/full-studies/r12_verify.json
for group in rarity a_target a_supplied; do
  width=3; [ "$group" = a_supplied ] && width=1
  python -m scripts.oldgame_multiround_coverage --stage run --device cuda --runs "$group" --chunk-runs "$width" --output-root build/full-studies/r12 --bulk-root build/full-bulk/r12
done

# r13: all four mechanism experiments, including 200-update erosion.
python -m scripts.oldgame_multiround_mechanism --stage verify-gpu --device cuda --bulk-root build/full-bulk/r13
for shard in 0 1 2; do
  python -m scripts.oldgame_multiround_mechanism --stage run --device cuda --experiment all --process "$shard" --output-root build/full-studies/r13 --bulk-root build/full-bulk/r13
done
```

GPU groups are sequential above: Run All never starts a fleet. Fixed-horizon
r8–r13 runs use 20,000 updates except the 200-update erosion experiment; their
audits and futility rules remain those of each registration. Historical r8 runs
take about half an hour each on their recorded CPU, not a measured Colab GPU
estimate. The notebook displays hash-bound compute records and its own live
updates/s. GPU audit and probe costs can dominate training; use a 1k smoke on
your hardware before budgeting the complete studies. No full-fleet T4 runtime
has been measured. Consult each `HOST_COMMANDS.md` and registration for detailed
restore, grouping and reporting options.
