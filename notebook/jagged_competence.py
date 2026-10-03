# %% [markdown]
# # Where Does Jagged Competence Come From? — run it yourself
#
# Choose **Runtime → Run all** in Colab, or **Run All** in local Jupyter.
# Quick mode verifies the released results and trains a small fresh network;
# full mode changes the live training budget to 20,000 updates, not the evidence.
# We keep **paper results**, **fresh measurements** and **short training** separate.
# Expand a named code cell to inspect its implementation. No paid service is needed.
#
# The source snapshot is pinned. Local execution uses this checkout and checks its
# evidence hashes. CPU and GPU training streams need not be bitwise identical.

# %%
# @title Setup: choose the live training budget { display-mode: "form" }
MODE = "quick"  # @param ["quick", "full"]
from runtime import Session  # INLINE_RUNTIME
session = Session(MODE)
session.setup()

# %% [markdown]
# ## 1. The task has two layers
#
# Four records put masses into five slots. **A** adds the masses in this round.
# **B** remembers whether the last non-neutral first-slot sum turned the mode
# off or on. A neutral board leaves that mode unchanged. We will construct two
# legal histories with identical final sums but different next-category laws.
# Masses and sums below are in twelfths. The board census is exhaustive.

# %%
# @title Draw a board and check the two-history witness
session.task()

# %% [markdown]
# ## 2. Check the paper's numerical evidence
#
# This executes the paper's ledger checker: it recomputes the registered numbers
# from hash-bound released artifacts, rather than trusting a notebook constant.
# Then it rebuilds Figures 1–5 and Table 1 with the paper's own asset functions.
# Each displayed value has a ledger or manifest reference. This checks the
# released evidence; it does not rerun hundreds of full training experiments.

# %%
# @title Recompute the ledger and display rebuilt paper figures and Table 1
session.paper_assets()

# %% [markdown]
# ## 3. Trained networks: recoverable is not always reliable
#
# We reload **records → prediction** checkpoints at updates 0 and 20,000 for
# seeds 0–2. For each slot we refit the registered linear sum probe, with
# training-only standardization and a disjoint 512-board evaluation set.
# Readability is not evidence that prediction uses those decoded sums.
# Class-balanced fitting can score below the majority baseline. Lower measured
# readability does not establish that information was removed from the state.
# Low natural KL and constructed-history law failures are shown side by side.

# %%
# @title Refit released raw-carrier probes and replay the prediction panels
session.released_networks()

# %% [markdown]
# The next census uses the distributed **r12 records → prediction+sums** network,
# seed 0, on all 24,435 boards and all four fixed renderings. Categorical misreads
# and probability-TV failures are different counts. We also show the paper's
# r12 uniform records → prediction census as a **separate saved result**; that
# condition's checkpoint is not included in this distribution. These are not
# matched comparisons with r8.

# %%
# @title Replay the available r12 network's full board census
session.census()

# %% [markdown]
# ## 4. Train a fresh network yourself
#
# This is new training, not a replay of a selected paper checkpoint. Only the
# next-category prediction loss trains the records encoder and recurrent upper
# state: no sums labels enter its optimizer. We use the device-resident sampler
# from r11 and the same raw-route architecture, AdamW rate and weight decay.
# Quick mode uses a smaller CPU budget than GPU. A short run can show weaker,
# noisier effects, or no readability gain at all; it does not establish closure.
# The plots update during training. Full mode uses 20,000 updates.
# Live KL uses 512 fixed independent test episodes (128 in the test-only budget),
# not the full 5,000-episode replay above; the fresh census is explicitly reduced.

# %%
# @title Train, plot the learning curve, then probe and audit the fresh model
session.train_live()

# %% [markdown]
# ## 5. Erosion after one update
#
# The frozen continuous sums parent is exact on **all 1,555 local histories**.
# From identical copies, apply one prediction-loss update under AdamW,
# reduced-rate AdamW, displacement-matched SGD, and a blocked-gradient control
# that still applies weight decay. The max task is not involved here.
# We show fresh counts next to the paper's seed-0 counts. The paper used CUDA
# draws; a fresh CPU minibatch is different, so matching those counts is not a
# pass requirement. The exact parent and blocked control must remain exact.

# %%
# @title Audit exact sums, perform one update, and compare with the paper
session.erosion()

# %% [markdown]
# ## 6. Access and encoding: released r13 results
#
# The connection experiment separates a disconnected sums head from frozen,
# live and exact supplied sums. The encoding experiment compares one-hot and
# numerical sums at the same width. All seed values and failed endpoint labels
# remain visible: a connection or a different encoding is not a closure guarantee.
# The connection plots show categorical-misread counts beside long-panel law TV;
# these are separate measures, with all three seeds displayed.
# These are hash-verified released results, not new network fits.

# %%
# @title Plot the connection and encoding experiments with their ledger values
session.mechanisms()

# %% [markdown]
# ## 7. What did we learn?
#
# - **Averages can hide concentrated failures:** section 3 juxtaposes natural KL,
#   long neutral histories and the board census.
# - **Readability is not computation or use:** the raw-state probes in section 3
#   ask what a separate reader can recover, not what prediction actually reads.
# - **Further training can lose exact sums:** section 5 tests a fresh single update
#   and keeps its minibatch and precision separate from the paper's counts.
# - **Access and encoding matter, but are not sufficient:** section 6 retains
#   failing seeds and criteria alongside improvements.
# - **History coverage is a contributing condition, not a complete explanation:**
#   the rebuilt figures and the separate r12 census include unresolved cases.
# - **A short live run is an experiment, not confirmation:** section 4 reports
#   whatever its declared budget achieves. No checkpoint is selected by outcome.
#
# ## Run the full studies
#
# The next cell prints actual CLI commands for r8–r13, the registered endpoints,
# and available recorded timings. These are **not executed by Run All**.
# Use a fresh output/bulk directory and one visible accelerator where required.
# Verification must precede GPU continuations. CPU-era r8 remains CPU-only;
# its full runs can be much slower than the live device implementation here.
# Complete experiments include controls and seeds, not just the examples below.

# %%
# @title Show full-study commands and compute qualifications (does not train)
session.study_commands()

# %% [markdown]
# ## 8. This session's results
#
# The compact table distinguishes checks of the released paper from fresh live
# measurements. The JSON receipt records source identities, parameters, timings,
# convergence and all comparisons. Download it if you want to compare executions.

# %%
# @title Print and save the final results table
session.finish()
