# Methods facts — r8–r13

Writer's reference, 2026-10-01. Facts describe executed instruments, not proposed capabilities. Study comparisons are **historical** unless the stated within-study factor is matched. Names follow `paper/notes/notation_and_terminology.md` (§Task, §Versions, §Measurements). No new training or inference was run for this sheet.

## Source key

All paths are repository-relative. `source:line` identifies the first relevant line, not an entire file as evidence. Registration references identify JSON fields or the named section of the companion Markdown.

| Key | Source |
|---|---|
| R8 / R10 / R11 / R12 / R13 | `reports/phase11/oldgame_memory/multiround/study_r8_route_access/registration.json`; `study_r10_allslots/registration.json`; `study_r11_jagged/registration.json`; `study_r12_coverage/registration.json`; `study_r13_mechanism/registration.json`, respectively, under that same directory |
| M | `src/recombination_promotion/oldgame_ext/multiround.py` |
| C | `scripts/multiround_panels.py` |
| O | `scripts/multiround_streams.py` |
| R | `scripts/oldgame_multiround_route_access.py` |
| J / JS | `src/recombination_promotion/oldgame_ext/multiround_jagged.py` / `scripts/oldgame_multiround_jagged.py` |
| V / VS | `src/recombination_promotion/oldgame_ext/multiround_coverage.py` / `scripts/oldgame_multiround_coverage.py` |
| X / XS | `src/recombination_promotion/oldgame_ext/multiround_mechanism.py` / `scripts/oldgame_multiround_mechanism.py` |
| T / TS | `src/recombination_promotion/oldgame_ext/multiround_allslots.py` / `scripts/oldgame_multiround_allslots.py` |
| P | `src/recombination_promotion/oldgame_ext/jagged_probes.py` |
| MC | `src/recombination_promotion/oldgame_ext/memory.py` |
| G | `src/recombination_promotion/oldgame_ext/game.py` |
| D9 | `scripts/oldgame_multiround_raw_diagnosis.py` |
| Ledger | `paper/notes/claims_ledger.json`, entry ID as given |

## 1. Original task: r8, r9, r11, r12, r13

| Fact | Source |
|---|---|
| Four records, five slots; masses 1/6, 1/4, 1/3, 1/2, 2/3, 3/4, encoded as integer twelfths 2, 3, 4, 6, 8, 9. A completed sum board has five totals, each in {0, 2, …, 36}. | Ledger `TASK-records`, `TASK-slots`, `TASK-masses`, `TASK-sums`; M:57 |
| Enumerating 30⁴ = 810,000 ordered placements gives 24,435 distinct completed sum boards. Slot-1 category counts: L 22,491; N 1,835; H 109. | M:57; Ledger `TASK-boards`, `TASK-category_counts` |
| Slot 1 means coordinate `board[0]`. L: sum ≤12; N: 13–23; H: sum ≥24. Initial mode is off. L resets off, H sets on, N preserves the preceding mode. | M:40, M:82, M:169 |
| Next-category probabilities in L/N/H order: off (1/2, 1/4, 1/4); on (1/4, 1/4, 1/2). Equal-law control: (3/8, 1/4, 3/8) in both modes. The sampled next category determines the next board's category. | M:28, M:169; Ledger `TASK-p0`, `TASK-p1`, `TASK-equal_law` |
| Conditional on category, the natural sampler selects a completed sum board uniformly, then a legal mass placement for that board. Rendering varies the six permutations of records 1–3; record 4 stays fixed. Full prompt rendering also varies query order, three Stage-1 templates and nonce bindings. | M:51, M:127, M:169; C:123 |
| Training prediction inputs are ordered four-record `(slot, mass-index)` tensors, not names, binding statements or prompt tokens. The routed evaluation separately resolves slots from Stage-1 prompts using the saved Gate A resolver. | C:123, C:145; J:150; R8 source identities |
| Frozen exact sums source: `reports/phase11/oldgame_memory/continuous/continuous_seed0_r7/trajectories/parent_A_step_002000.pt`, SHA-256 `0d14e7a2b63459d9e6c392d57d55cca02059ca0131f6225f18fafa2a3d38b5b9`. Verified on all 1,555 local histories; five independent per-slot histories reset each round. | M:226; R8 sources; C:35 |
| r8 natural training: fresh batch of 256 episodes, maximum eight rounds; exclude the third consecutive N **input and loss**. Retain the prediction target drawn at the preceding round. | O:204; M:189; R8 settings |
| r11 natural training has the same maximum eight rounds and truncation. Rarity conditions change only within-category board selection: uniform, 25% enrichment at sums L:{12}, N:{13,23}, H:{24}, or matched decoys L:{10}, N:{16,20}, H:{27}. Category draws and targets remain paired. | J:19, J:122, J:150; R11 design |
| r12 history coverage: each batch has 128 untruncated nine-round natural episodes and 128 coverage prefixes; eight examples per L/H anchor × k∈{1,…,8}. Each coverage prefix is anchor followed by Nᵏ; only its final position receives prediction loss. Natural positions receive prediction loss throughout. r13 non-erosion experiments reuse this protocol. | V:47, V:73, V:134; R13 companion Markdown §Common design |
| Natural test: 5,000 independent episodes ×12 rounds =60,000 scored positions, no training truncation. Original-law test seed 2026100101; equal-law test seed 2026100102; prefix seed 2026100103. The routed evaluation uses the saved resolver, without retraining. | C:30, C:258 |
| Unseen KL uses test positions whose ordered preceding two-board pair never occurred at an active training position. There are 50,000 candidate positions (rounds 3–12); mark during training, take remaining positions at the endpoint, no redraw. This is unseen **past combinations**, not an independent split of completed sum boards. | O:159; JS:637; VS:555 |
| Endpoint unseen support is run-specific. Recorded ranges: r8 20,146–24,111; r11 20,211–25,702; r12 20,975–25,704; r13 non-erosion 20,975–24,245 positions. Use each run's `unseen_count`, not these ranges as denominators. | r8 `*/audit_step_020000.json:audit.unseen_count`; respective `aggregate.json`: r11 experiment/run rows; r12 `runs`; r13 `experiments`; R:183 |
| r9 performs no training: all three r8 original-law versions × seeds 0–2, saved 20k checkpoints; complete board enumeration and long-neutral inference diagnosis. | D9:79; `study_r9_raw_diagnosis/results.json` |

## 2. All-slots task: r10 only

| Fact | Source |
|---|---|
| Same records, masses and 24,435 completed sum boards. Remembered value in each slot is its last nonzero sum; initially all five remembered values are zero. Public query J is uniform over five slots. It asks for the law indexed by that slot's remembered value, not its current sum. | T:23, T:48, T:130 |
| Q is total board sum modulo 3. The network sees records and public J, never Q or the remembered-value vector. For value index i=6a+b in the sorted 36-value vocabulary, law row is (0.10+0.07a, 0.10+0.07b, 0.80−0.07(a+b)). All 36 rows differ; minimum pairwise TV=0.07. Equal law is (1/3,1/3,1/3). | T:23, T:44, T:210; R10 exact rows |
| Initial Q is uniform over three categories. After predicting the next Q, select the next board conditional on that Q. Coverage mixture: 50% uniform board within Q; 50% uniform supported (slot, current nonzero value) pair within Q, then a board conditional on the pair. The registration records the exact 5×36 conditional-frequency table. | T:73, T:130, T:334; R10 conditional frequencies |
| Board-identity split: 19,548 training and 4,887 held-out boards, seed 2026101004. Training episodes eight rounds, batch 256, no N truncation. Natural test 5,000×12; held-out-board panel 1,000×12. Query/memory-dependent construction replaces original-task L/H,Nᵏ panels. | TS:99, TS:322; T:334; R10 settings/panels |
| Stream generators: 2026101001 + training seed +100×equal-law indicator, with offsets 0,100000,200000 for category/query, board and rendering streams. Test seed 2026101002; probe seed 2026101003. Current-value and remembered-query-value exposure counts are stored separately. | T:334; R10 seeds; T:388 |
| Constructed panels: 180 law-row presentations (five queries ×36 values); ten two-round witness histories; ten nine-round histories holding the queried slot empty through eight later rounds. | TS:322 |

## 3. Network modules and interfaces

| Module / interface | Exact dimensions and operation | Source |
|---|---|---|
| Sums network (`MemoryCore`) | Learned start 64; mass embedding 6×64; update MLP 128→64→64, GELU then Tanh; query-kind embedding 3×64; answer MLP 128→64→36, GELU. Five cells share this network; only the record's slot updates. Per-round reset. | MC:74; C:35 |
| Raw encoder | Symbol=6×slot+mass-index; embedding 30×16; one-layer GRU 16→16 over four presented records; final raw carrier width 16. Per-round reset. | C:16, C:49 |
| Sums output head on raw carrier | Linear 16→180, reshaped five×36. It is **not** `MemoryCore` and does not itself cross the round boundary in records → prediction+sums. | J:234, J:314 |
| Hard sums interface | Five 36-way one-hots, concatenated width 180; `hard + soft − stop_gradient(soft)` permits training gradients while the executed interface is hard. Bias-free Linear 180→32. No continuous per-slot state crosses the round boundary. | C:35; J:234 |
| Upper recurrent state / category head | GRUCell (32 sums projection +16 raw)=48→32; Linear32→3. State starts zero per episode. r10 adds public query one-hot width5: GRUCell53→32. | C:16, C:53; T:210 |
| Route versions | r8 sums → prediction masks raw; records → prediction masks sums; records+sums → prediction receives both. r11–r13 raw versions mask the sums interface; supervised sums output is an auxiliary loss unless explicitly connected. | R:68; J:234; V:123 |
| Connected (frozen) / Connected (live) | r13 access experiment starts from each seed's r12 records → prediction+sums 20k raw encoder/head. Frozen copy supplies detached hard sums; live head supplies straight-through hard sums. Both train the live raw head; frozen supplier is immobile. Disconnected comparison supplies zero sums. | XS:159; X:73, X:103 |
| Exact supplied / encoding comparison | Frozen learned `MemoryCore` supplies exact sums. One-hot encoding remains 36-wide/slot. Numerical encoding is `(s/36,1−s/36,0,…,0)` in that same width, with s in twelfths. | X:63, X:103 |

Parameter counts below count allocated scalar parameters using `sum(p.numel())`; unused or frozen modules are not evidence of executed computation. Counts follow the cited constructors; no checkpoint inference was needed.

| Construction | Allocated | Gradient-enabled at construction | Qualification / source |
|---|---:|---:|---|
| r8, each route version | 39,495 | 15,843 | Frozen `MemoryCore` 23,652; R:68 |
| r11 raw / erosion constructions | 42,555 | 42,555 | Raw versions do not execute `MemoryCore`; unused modules receive no loss gradient. Erosion executes it; J:234, J:328 |
| r12, each version | 42,555 | 18,903 | `MemoryCore` frozen; V:123 |
| r13 non-erosion, each condition | 47,727 | 18,903 | Frozen `MemoryCore` 23,652 + frozen supplier copy 5,172, including unused copies; X:73 |
| r13 erosion | 42,555 | condition-dependent | Same r11 construction; blocked prediction gradient is an update condition, not removal of parameters; XS:719 |
| r10, each version | 43,035 | 19,383 | Frozen `MemoryCore`; extra query input adds 480 upper parameters; T:210 |

## 4. Training, matching and erosion

| Fact | Source |
|---|---|
| r8/r10/r11/r12/r13 non-erosion: seeds 0,1,2; batch256; AdamW lr0.003, weight decay0.01, default β=(0.9,0.999), ε=10⁻⁸; fixed20,000 updates, subject to registered5k futility. No accuracy-based best-checkpoint selection. No warmup or gradient clipping in these loops. | R8/R10/R11/R12/R13 settings; R:548; XS:65 |
| Scheduled B audits: updates0,1000,2000,5000,10000,15000,20000. Report all; endpoint pass is not first crossing. r9 has no optimizer. r13 erosion is separately fixed at200 updates. | Registrations `settings`; D9:79; XS:65 |
| r8: prediction cross-entropy averaged over active rounds, no sums loss, frozen A in every route. r10: prediction cross-entropy at every round; records → prediction+sums additionally has sums coefficient1; the other versions have none. | R:68; R:548; T model/loss; R10 loss |
| r11 sums doses: nested seeded masks at1%,10%,100% of active rounds; summed sums loss divided by **all** active rounds ×five slots, not selected count. B loss remains normalized over active rounds. Erosion continuation with sums supervision uses coefficient1 on every active round. | J:225; JS:1017; J grouped loss; R11 loss |
| r12/r13 non-erosion prediction loss: 0.5×natural-position mean +0.5×coverage-endpoint mean. Sums-supervised versions: coefficient1, averaged over all active input rounds ×five slots. | V:134; XS:65 |
| r13 Probability targets: cross-entropy −Σp log q against exact probability rows; sampled-target comparison retains identical category draws and streams. Neither mode nor probability row enters the network. | X:123; R13 §Common design/target-noise experiment |
| r8 fresh online episode seed stream:202609290000+seed; each draw selects a fresh episode-batch seed. r11 separate device generators: category202609290000+seed+10000×equal; board202609300000+seed+100×draw-kind index+10000×equal; rendering202609310000 with the same offsets. r12/r13 replace these bases by202610110000/202610120000/202610130000. | O:33, O:204; J:95; V:34 |
| Dose-mask seed:2026101100+seed+100×equal+10000×update. Logged executed placements, orders, exposures and stream states allow replay; board labels for probes do not enter training. | JS:1017; J:150; R11 registration |
| Futility at5k: r8 stops when both prediction-loss gap and natural-KL gap close by less than10%. r11 also exempts improved supervised sums or changed erosion sums; r12 exempts improved supervised sums. r13 uses initial excess B₀−F₀ and the mean of the last100 per-batch excess prediction losses, retaining the KL check and supervised-sums exception; nonpositive initial excess cannot trigger that stop. | R:558; JS:997; VS:158; XS:478; R13 settings.futility |
| Executed training/evaluation precision: r8 float32 on CPU; r10–r13 float32 on CUDA. Evaluation/probe features float32; linear probe fitting CPU. Earlier conditional bf16 plans are not the executed fp32 evidence. | Run summaries `authority.precision` / `precision`; JS:1259; P:20 |
| r11 Erosion continuation starts with exact frozen-source weights but unfreezes the sums network. Compare prediction loss versus prediction + sums loss, original/equal laws,20k updates. Early readouts at1,5,10,50,100 use a fixed128-board panel; later census and local exactness have different denominators. | R11 erosion protocol; JS early erosion readouts |
| r13 erosion repeats original-law r11 sampling, not the r12 coverage sampler:200 updates, same exact sums start and fresh upper/raw modules per seed. AdamW sums lr0.003; reduced-lr AdamW sums lr0.0003; SGD momentum0 and fixed rate chosen on the first shared batch to match Adam's gradient-only displacement norm. Other parameters use AdamW0.003 throughout. | R13 §Early erosion mechanism; XS:719; X:178 |
| SGD sums decay multiplier0.99997 matches ordinary AdamW0.003×0.01 decay. Blocked prediction gradient uses explicit zero sums gradients with that AdamW decay retained. No sums-label loss in these four erosion conditions. | XS:719; R13 erosion optimizer table |
| Cumulative movement is Σupdates ‖Δθ‖₂ across all sums-network tensors; displacement from initialization is separately ‖θₜ−θ₀‖₂. Per-tensor paths, gradient/decay displacement, gradient size versus ε and answer margins are stored each update. | XS:805 |

## 5. Measurements and controls

| Measurement | Definition / support | Source |
|---|---|---|
| Natural / unseen KL | Mean KL(law ‖ prediction), base2, bits;60,000 natural positions and endpoint-tracked unseen positions as above. Probability clipping at10⁻¹² for KL. Original ideal loss1.5bits; witness JS deficit0.06127812445913283bits. | R:173; M:103; Ledger `TASK-ideal_loss_bits`, `TASK-witness_JS_bits` |
| Original-task law panels |32 variants per anchor L/H ×k=0…8:576 histories,64 endpoints per k. k=0 is single-round L/H. Report mean/max TV per case; short=L/H,N¹–N²; long=N³–N⁸. | C:206, C:491 |
| Witness recovery | Paired L/H histories followed by the same N board; loss against each exact row; recovery=1−loss/JS. Equal law instead tests near-identical predictions, not recovery from a zero deficit. | C:491; R:183 |
| Census |24,435 boards ×four fixed record renderings, each in off/on contexts. Closest two-context L/N/H signature gives categorical misread; max-context TV>0.02 gives separate TV-error count. Cutoff band11–13,23–25 has930 boards; other boards23,505. | JS:470, JS:559; Ledger `TASK-cutoff_band`, `TASK-complement` |
| Saved r9 cases | Same-board renderings used in r9 are scored separately, not replaced by the four-rendering census. r9 originally used one fixed census rendering and clear-N sums16–20 for drift tests. Equal-law categorical signatures are undefined. | D9:79; JS:559; glossary §Census |
| Original-task rerendering |48 boards (16/category), three alternative renderings, common future N,N,L; hard sums component differences must be0; prediction-TV bar0.02. Distinguish output-answer disagreement from prediction disagreement. | C:223, C:525 |
| Original-task swaps | Reset L and set H after varied prefixes:160 cases each; neutral N192; same-category substitution128; upper-state exchange before the same N64. These are law/state interventions, **not** the r10 aligned single-slot donor-follow experiment. | C:545 |
| Local / board exactness | Local: all1,555 per-slot histories, with1/6/36/216/1,296 histories at lengths0/1/2/3/4. Board-vector: allfive answers on24,435 completed sum boards, with rendering-specific counts. Exactness of an output does not certify a raw carrier. r11 early erosion readouts are sampled128-board counts. | G:23; JS:675; glossary §Local exactness |
| Probe split | r8-derived fixed2,048 training boards,512 disjoint held-out board identities; five slot targets; report correct/512 per slot. Probe-training split covers attainable classes, separately from network training. Seed2026100801; features raw16 or upper32. Original-task upper probes are after **one board from zero upper state**, not probes of remembered mode. | R:299, R:339; JS:388 |
| Linear readers | Fit-only standardization, C10, balanced classes, tolerance10⁻⁵,max5000 iterations. r8/r10 sklearn logistic regression; r11–r13 torch weighted cross-entropy +‖W‖²/(2CΣweights), unpenalized bias, CPU L-BFGS strong-Wolfe. Record iterations/warnings/convergence; nonconvergence cannot support readability gain. | R:366; TS:511; P:20 |
| MLP readers | One hidden layer64, ReLU,36-way sums output (later also three-way category);100 full-batch Adam updates at0.03. Later inputs standardized from training only. r8 MLP inputs are **not standardized**. | R:366; P:20 |
| Probe controls / intervals | Update0, training-majority class, shuffled labels and exact oracle. Paired accuracy-gain95% percentile CI:1,000 resamples of the same512 held-out board identities; not a CI over three seeds. Report per-seed values separately. | R:432, R:682; JS probe comparison |
| r10 additional probes | Upper32 state sampled over registered12-round recurrent histories/public queries. Rare sums28–36 have a separately labelled held-out-rendering panel,20 renderings; do not merge with board-held-out support. Decoders and alignment persist. | TS:99, TS:470, TS:511; R10 probe protocol |
| r10 aligned swaps | Fit training-only mean-centred orthogonal alignment into15 oracle coordinates +one residual coordinate. Replace the three-coordinate block for queried slot; inverse-transform patched state. Independent training-only float64 least-squares decoder to15 coordinates, then nearest prototype, checks the other slots. Logistic decoder supplementary. | TS:609, TS:636, TS:665 |
| r10 pair support / controls | Fixed1,024 distinct eligible pairs per slot, or all if fewer, chosen before predictions; same otherfour sums, different donor-slot values/law rows. Report conditional accurate-pair support, per-value coverage, Wilson95% intervals and saved pair predictions. Oracle hard-answer and rotated-carrier positives; no-op/shuffled alignment negatives; planted contamination tests selectivity. Trained positive is seed-matched20k records+sums → prediction only. | R10 interchange amendments; TS:475; TS alignment calibration |
| r10 use interpretation | Trained-positive donor-follow≥0.95 with≥20 accurate pairs/slot; evaluated donor-follow≥0.80; supported negative≤0.20; zero other-slot decoded changes. Insufficient support means uncalibrated. The hard-answer positive's shuffled **raw** negative is NOT_APPLICABLE. Calibration status and measured use-test result are separate. | R10 interchange decision rules; `study_r10_allslots/analysis_specification.json` |
| Deciding-function calibration | Execute positives/nulls through the same scorer and threshold/selection function that classifies saved networks; do not substitute a manually asserted ideal score. Require nonempty unseen and diagnostic support. Calibration pass establishes an instrument's discrimination, not a network result. | JS:637; VS:183; XS:338; TS:1111 |

## 6. Registered criteria and endpoints

| Study | Endpoint / runs | Prediction bars and pass definition | Authority |
|---|---|---|---|
| r8 |20k;3 versions ×2 laws ×3 seeds=18 | Natural and unseen KL≤0.01bits; law maxTV≤0.02; witness recovery≥0.8 original; equal-law witness TV≤0.02; rerender/swap≤0.02 with exact sums rerender. Conjunction at endpoint. | R8; R:183 |
| r9 | Read-only saved r8 original-law20k;9 networks | Diagnosis only; no new registered learning endpoint or pass. | D9:79 |
| r10 |20k;3 versions ×2 laws ×3 seeds=18 | Natural and covered-value KL≤10% mode-blind loss (equal law lower bound0.01bits); law-row/hold TV≤0.05 original,≤0.02 equal; same-board witness TV≤0.05 and original separation≥0.05/equal separation≤0.02. B pass separate from readability/use gates; equal-law control-only. | R10; TS:1111 |
| r11 |20k; rarity3 +erosion2 +dose3 conditions ×2 laws ×3 seeds=48 | Original-task r8 prediction bars; sums/probe/census achievements separately measured, not implied by B pass. | R11; JS:637 |
| r12 |20k;5 versions/conditions ×2 laws ×3 seeds=30 | Same original-task prediction bars; trained long panel still required. Diagnosis requires actual sequence violation, correct preceding constituents, valid anchors; concurrent board/recurrence evidence retained. | R12; VS:932 |
| r13 | Original-law target noise4×3seeds=12; original-law access4×3seeds=12; encoding numerical original3 +one-hot/numerical equal6=9; erosion4×3seeds=12:45 distinct runs. Original-law exact one-hot encoding comparator is the access exact condition. | Non-erosion20k with original-task bars; equal-law control-only. Erosion200updates, no B-pass endpoint claim. Geometry calibrated separately, not a training endpoint criterion. | R13 runs; XS:65 |

## 7. Recorded compute

These are recorded ranges, not sums over duplicated per-run group times. Device authority is not a record of GPU model/driver. Historical commands or hardware not recorded remain unknown.

| Study | Recorded execution / seconds | Evidence |
|---|---|---|
| r8 | CPU float32; per-run elapsed1,661.039–1,895.117s (18 summaries). CPU model unknown. | `study_r8_route_access/*/summary.json:elapsed_seconds`; e.g. Ledger `T-86308dd06c062406-elapsed_seconds` |
| r9 | CPU read-only diagnosis5.516428498s. CPU model unknown. | Ledger `T-r9-diagnosis` |
| r10 | CUDA float32; grouped training693.705–2,330.242s, audit time separate; width3 raw versions, width1 exact-supplied version. Configurable CUDA device; model/driver unknown in summaries. | `study_r10_allslots/*/summary.json:authority,training_seconds,audit_seconds`; `HOST_COMMANDS.md` |
| r11 | CUDA fp32, one CPU thread/process; group elapsed971.841–2,796.982s; training702.174–1,942.005s. Raw width3, Erosion continuation width1; at mostfive processes. | `study_r11_jagged/runs/*/summary.json:device,precision,CPU_threads,elapsed_group_seconds`; R11 execution |
| r12 | fp32; group update time842.100–2,102.450s; audits276.831–1,148.041s. One CPU thread; width3 raw,width1 supplied; Configurable CUDA device. GPU model/driver unknown. | `study_r12_coverage/*/summary.json:performance`; `HOST_COMMANDS.md` |
| r13 | Non-erosion group update time992.210–2,345.322s; audits284.607–978.416s. Erosion elapsed17.231–22.219s. One CPU thread; width3 target-noise,width1 access/encoding/erosion; at mostthree processes; Configurable CUDA device. | `study_r13_mechanism/*/summary.json:performance,elapsed_seconds`; R13 execution |

## 8. Differences and qualifications for the writer

- **Rendering scope:** record tensors use already resolved slots during training; this is not end-to-end prompt training. Prompt-resolver audits are separate. Four census record renderings must not be called four Stage-1 text templates. [C:123, C:145; JS:470]
- **Long-history scope:** r8/r11 exclude the third consecutive N during training; r12/r13 non-erosion explicitly train N¹–N⁸. Their long panel is not unseen-length extrapolation. These comparisons are historical, with curriculum and loss-weighting changes. [M:189; V:73; glossary §Studies]
- **Sampling exactness:** board counts and law definitions are exact enumerations/rationals. Device r11 sampler uses finite integer draws with modulo indexing; do not claim exact mathematical uniformity of its implemented draws. [J:150]
- **Unseen scope:** support depends on law, seed, board enrichment and active training positions. Do not use a universal unseen denominator or describe this as a held-out board split. [O:159; VS:555]
- **Probe comparability:** r8 MLP standardization differs from later instruments; upper probes for the original task are one-round states, whereas r10 uses recurrent histories. A probe CI is not seed variation, and recoverability does not establish use. [R:366; JS:388; TS upper probe protocol; glossary §Probe]
- **Convergence flag:** the torch linear reader accepts an optimizer stop before5000 iterations, whether by gradient or objective change; its flag is not an independent guarantee that the gradient norm is below10⁻⁵. MLP readers have a fixed fitting budget and `converged=null`. [P:73, P:86]
- **Supplier exactness:** the connected frozen raw supplier is the approximate r12 sums head, not the exact `MemoryCore` supplier. Preserve that distinction when describing access. [XS:159; X:103]
- **Task/pass differences:** r10 changes the law, query and remembered state; its KL and TV bars are not the original-task0.01/0.02 bars. Equal-law categorical signatures and mode-specific witness recovery are undefined, not failed computations. [T:23; TS:1111; glossary §Equal-law control]
- **Exactness scope:** an exact local sums output, a board-vector census and calibrated probe recovery are different achievements. None is an internal strict-extension certificate for these continuous/raw networks. [glossary §Measurements; R13 scope]
- **Runtime scope:** grouped timing appears in more than one seed summary; summing it would overcount. CUDA launch instructions alone do not identify the GPU model/driver or complete historical command. [run summaries; `paper/notes/evidence_manifest.json` hardware records]
