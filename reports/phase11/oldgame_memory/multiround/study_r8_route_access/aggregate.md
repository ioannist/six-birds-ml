# r8 route-access aggregate

## Registered readings (verbatim)

A-only learns B faster or passes when raw-only does not: access to completed A objects helps realize the predictive extension; it does not show spontaneous A formation.
Raw-only passes B; only slot-1 A improves: B-only training organized the rewarded slot-1 information, not a full five-slot A layer.
Raw-only passes B; all five sums improve: full A became readable in those states; readability alone does not establish causal use.
Raw-only passes B; no sum improves: B was learned without measured new A readability; report any high baseline decodability.
Dual outperforms both: access to both routes helps under this architecture; interpret interventions with the deterministic-overlap caveat.
Equal-law witness split or route-dependent gain: control failure.

## Selected applicable reading

Original-law raw-only is B-incomplete in all three seeds: the worst-case mode-law and causal-swap bars fail. Its increased measured slot-1 A readability is conditional on that B failure; the registered readings requiring raw-only to pass B do not apply. Other slots' reduced probe accuracy does not establish information absence or erasure. Equal-law slot-1 gains are also reported.

## B endpoints

| Run | First crossing | Endpoint |
|---|---:|---|
| a_only_equal_seed0 | 1000 | B_PASS |
| a_only_equal_seed1 | 1000 | B_PASS |
| a_only_equal_seed2 | 1000 | B_PASS |
| a_only_original_seed0 | 10000 | B_PASS |
| a_only_original_seed1 | 20000 | B_PASS |
| a_only_original_seed2 | None | B_INCOMPLETE |
| dual_equal_seed0 | 1000 | B_PASS |
| dual_equal_seed1 | 1000 | B_PASS |
| dual_equal_seed2 | 1000 | B_PASS |
| dual_original_seed0 | 15000 | B_PASS |
| dual_original_seed1 | 20000 | B_PASS |
| dual_original_seed2 | 20000 | B_PASS |
| raw_only_equal_seed0 | 1000 | B_PASS |
| raw_only_equal_seed1 | 1000 | B_PASS |
| raw_only_equal_seed2 | 1000 | B_PASS |
| raw_only_original_seed0 | None | B_INCOMPLETE |
| raw_only_original_seed1 | None | B_INCOMPLETE |
| raw_only_original_seed2 | None | B_INCOMPLETE |

## Raw-only original-law failed bars at 20,000 updates

| Seed | Law maximum TV (limit 0.020) | Failed swap cases: maximum TV (limit 0.020) |
|---:|---:|---|
| 0 | 0.249996 (fail) | neutral_N 0.141083, same_category_substitution 0.116653, set_H 0.028796, upper_state_exchange_same_N 0.047081 |
| 1 | 0.254798 (fail) | same_category_substitution 0.022050 |
| 2 | 0.256485 (fail) | neutral_N 0.236966, same_category_substitution 0.109714, upper_state_exchange_same_N 0.105554 |

## Raw-only endpoint probe measurements

Each law cell gives update-0 → 20,000 held-out accuracy; paired gain [saved 95% interval]; majority floor; linear-fit convergence. The MLP is fixed-budget, with convergence not assessed.

| Seed | Carrier | Probe | Slot | Original law | Equal law |
|---:|---|---|---:|---|---|
| 0 | raw | linear | 1 | 0.365 → 0.969; Δ +0.604 [+0.557, +0.646]; floor 0.340; converged | 0.365 → 0.426; Δ +0.061 [+0.008, +0.113]; floor 0.340; converged |
| 0 | raw | linear | 2 | 0.326 → 0.086; Δ -0.240 [-0.279, -0.189]; floor 0.355; converged | 0.326 → 0.500; Δ +0.174 [+0.125, +0.229]; floor 0.355; converged |
| 0 | raw | linear | 3 | 0.236 → 0.064; Δ -0.172 [-0.213, -0.125]; floor 0.406; converged | 0.236 → 0.611; Δ +0.375 [+0.324, +0.428]; floor 0.406; converged |
| 0 | raw | linear | 4 | 0.299 → 0.104; Δ -0.195 [-0.240, -0.148]; floor 0.375; converged | 0.299 → 0.584; Δ +0.285 [+0.227, +0.338]; floor 0.375; converged |
| 0 | raw | linear | 5 | 0.297 → 0.078; Δ -0.219 [-0.266, -0.176]; floor 0.404; converged | 0.297 → 0.533; Δ +0.236 [+0.187, +0.283]; floor 0.404; converged |
| 0 | raw | mlp64 | 1 | 0.590 → 0.980; Δ +0.391 [+0.350, +0.432]; floor 0.340; fixed budget; convergence not assessed | 0.590 → 0.373; Δ -0.217 [-0.262, -0.176]; floor 0.340; fixed budget; convergence not assessed |
| 0 | raw | mlp64 | 2 | 0.578 → 0.352; Δ -0.227 [-0.272, -0.182]; floor 0.355; fixed budget; convergence not assessed | 0.578 → 0.508; Δ -0.070 [-0.119, -0.021]; floor 0.355; fixed budget; convergence not assessed |
| 0 | raw | mlp64 | 3 | 0.605 → 0.400; Δ -0.205 [-0.244, -0.160]; floor 0.406; fixed budget; convergence not assessed | 0.605 → 0.584; Δ -0.021 [-0.062, +0.023]; floor 0.406; fixed budget; convergence not assessed |
| 0 | raw | mlp64 | 4 | 0.627 → 0.371; Δ -0.256 [-0.301, -0.215]; floor 0.375; fixed budget; convergence not assessed | 0.627 → 0.580; Δ -0.047 [-0.094, +0.002]; floor 0.375; fixed budget; convergence not assessed |
| 0 | raw | mlp64 | 5 | 0.613 → 0.400; Δ -0.213 [-0.264, -0.162]; floor 0.404; fixed budget; convergence not assessed | 0.613 → 0.477; Δ -0.137 [-0.189, -0.084]; floor 0.404; fixed budget; convergence not assessed |
| 0 | upper | linear | 1 | 0.381 → 0.967; Δ +0.586 [+0.539, +0.627]; floor 0.340; converged | 0.381 → 0.303; Δ -0.078 [-0.129, -0.027]; floor 0.340; converged |
| 0 | upper | linear | 2 | 0.340 → 0.059; Δ -0.281 [-0.326, -0.234]; floor 0.355; converged | 0.340 → 0.426; Δ +0.086 [+0.033, +0.143]; floor 0.355; converged |
| 0 | upper | linear | 3 | 0.275 → 0.041; Δ -0.234 [-0.277, -0.189]; floor 0.406; converged | 0.275 → 0.480; Δ +0.205 [+0.150, +0.266]; floor 0.406; converged |
| 0 | upper | linear | 4 | 0.295 → 0.068; Δ -0.227 [-0.271, -0.182]; floor 0.375; converged | 0.295 → 0.510; Δ +0.215 [+0.160, +0.266]; floor 0.375; converged |
| 0 | upper | linear | 5 | 0.309 → 0.074; Δ -0.234 [-0.277, -0.188]; floor 0.404; converged | 0.309 → 0.320; Δ +0.012 [-0.045, +0.070]; floor 0.404; converged |
| 0 | upper | mlp64 | 1 | 0.553 → 0.592; Δ +0.039 [-0.010, +0.086]; floor 0.340; fixed budget; convergence not assessed | 0.553 → 0.340; Δ -0.213 [-0.250, -0.176]; floor 0.340; fixed budget; convergence not assessed |
| 0 | upper | mlp64 | 2 | 0.543 → 0.355; Δ -0.188 [-0.223, -0.152]; floor 0.355; fixed budget; convergence not assessed | 0.543 → 0.355; Δ -0.188 [-0.223, -0.152]; floor 0.355; fixed budget; convergence not assessed |
| 0 | upper | mlp64 | 3 | 0.557 → 0.406; Δ -0.150 [-0.186, -0.115]; floor 0.406; fixed budget; convergence not assessed | 0.557 → 0.406; Δ -0.150 [-0.186, -0.115]; floor 0.406; fixed budget; convergence not assessed |
| 0 | upper | mlp64 | 4 | 0.539 → 0.375; Δ -0.164 [-0.203, -0.127]; floor 0.375; fixed budget; convergence not assessed | 0.539 → 0.375; Δ -0.164 [-0.203, -0.127]; floor 0.375; fixed budget; convergence not assessed |
| 0 | upper | mlp64 | 5 | 0.541 → 0.404; Δ -0.137 [-0.170, -0.103]; floor 0.404; fixed budget; convergence not assessed | 0.541 → 0.416; Δ -0.125 [-0.160, -0.090]; floor 0.404; fixed budget; convergence not assessed |
| 1 | raw | linear | 1 | 0.309 → 0.971; Δ +0.662 [+0.619, +0.705]; floor 0.340; converged | 0.309 → 0.467; Δ +0.158 [+0.111, +0.215]; floor 0.340; converged |
| 1 | raw | linear | 2 | 0.264 → 0.084; Δ -0.180 [-0.219, -0.137]; floor 0.355; converged | 0.264 → 0.410; Δ +0.146 [+0.098, +0.197]; floor 0.355; converged |
| 1 | raw | linear | 3 | 0.301 → 0.066; Δ -0.234 [-0.279, -0.191]; floor 0.406; converged | 0.301 → 0.469; Δ +0.168 [+0.113, +0.219]; floor 0.406; converged |
| 1 | raw | linear | 4 | 0.258 → 0.094; Δ -0.164 [-0.211, -0.115]; floor 0.375; converged | 0.258 → 0.596; Δ +0.338 [+0.285, +0.393]; floor 0.375; converged |
| 1 | raw | linear | 5 | 0.367 → 0.078; Δ -0.289 [-0.336, -0.242]; floor 0.404; converged | 0.367 → 0.574; Δ +0.207 [+0.150, +0.266]; floor 0.404; converged |
| 1 | raw | mlp64 | 1 | 0.609 → 0.979; Δ +0.369 [+0.326, +0.412]; floor 0.340; fixed budget; convergence not assessed | 0.609 → 0.494; Δ -0.115 [-0.164, -0.068]; floor 0.340; fixed budget; convergence not assessed |
| 1 | raw | mlp64 | 2 | 0.607 → 0.354; Δ -0.254 [-0.293, -0.213]; floor 0.355; fixed budget; convergence not assessed | 0.607 → 0.471; Δ -0.137 [-0.176, -0.094]; floor 0.355; fixed budget; convergence not assessed |
| 1 | raw | mlp64 | 3 | 0.564 → 0.404; Δ -0.160 [-0.203, -0.115]; floor 0.406; fixed budget; convergence not assessed | 0.564 → 0.547; Δ -0.018 [-0.064, +0.033]; floor 0.406; fixed budget; convergence not assessed |
| 1 | raw | mlp64 | 4 | 0.604 → 0.367; Δ -0.236 [-0.281, -0.195]; floor 0.375; fixed budget; convergence not assessed | 0.604 → 0.482; Δ -0.121 [-0.168, -0.076]; floor 0.375; fixed budget; convergence not assessed |
| 1 | raw | mlp64 | 5 | 0.686 → 0.402; Δ -0.283 [-0.332, -0.236]; floor 0.404; fixed budget; convergence not assessed | 0.686 → 0.619; Δ -0.066 [-0.111, -0.021]; floor 0.404; fixed budget; convergence not assessed |
| 1 | upper | linear | 1 | 0.346 → 0.977; Δ +0.631 [+0.588, +0.672]; floor 0.340; converged | 0.346 → 0.461; Δ +0.115 [+0.059, +0.166]; floor 0.340; converged |
| 1 | upper | linear | 2 | 0.301 → 0.082; Δ -0.219 [-0.266, -0.174]; floor 0.355; converged | 0.301 → 0.398; Δ +0.098 [+0.043, +0.152]; floor 0.355; converged |
| 1 | upper | linear | 3 | 0.324 → 0.045; Δ -0.279 [-0.320, -0.236]; floor 0.406; converged | 0.324 → 0.455; Δ +0.131 [+0.080, +0.182]; floor 0.406; converged |
| 1 | upper | linear | 4 | 0.283 → 0.053; Δ -0.230 [-0.271, -0.188]; floor 0.375; converged | 0.283 → 0.574; Δ +0.291 [+0.234, +0.344]; floor 0.375; converged |
| 1 | upper | linear | 5 | 0.402 → 0.066; Δ -0.336 [-0.387, -0.289]; floor 0.404; converged | 0.402 → 0.525; Δ +0.123 [+0.070, +0.176]; floor 0.404; converged |
| 1 | upper | mlp64 | 1 | 0.566 → 0.672; Δ +0.105 [+0.059, +0.150]; floor 0.340; fixed budget; convergence not assessed | 0.566 → 0.340; Δ -0.227 [-0.268, -0.189]; floor 0.340; fixed budget; convergence not assessed |
| 1 | upper | mlp64 | 2 | 0.549 → 0.355; Δ -0.193 [-0.229, -0.160]; floor 0.355; fixed budget; convergence not assessed | 0.549 → 0.355; Δ -0.193 [-0.229, -0.160]; floor 0.355; fixed budget; convergence not assessed |
| 1 | upper | mlp64 | 3 | 0.535 → 0.406; Δ -0.129 [-0.166, -0.096]; floor 0.406; fixed budget; convergence not assessed | 0.535 → 0.406; Δ -0.129 [-0.166, -0.096]; floor 0.406; fixed budget; convergence not assessed |
| 1 | upper | mlp64 | 4 | 0.525 → 0.375; Δ -0.150 [-0.182, -0.117]; floor 0.375; fixed budget; convergence not assessed | 0.525 → 0.375; Δ -0.150 [-0.182, -0.117]; floor 0.375; fixed budget; convergence not assessed |
| 1 | upper | mlp64 | 5 | 0.605 → 0.404; Δ -0.201 [-0.238, -0.160]; floor 0.404; fixed budget; convergence not assessed | 0.605 → 0.404; Δ -0.201 [-0.238, -0.160]; floor 0.404; fixed budget; convergence not assessed |
| 2 | raw | linear | 1 | 0.256 → 0.977; Δ +0.721 [+0.684, +0.756]; floor 0.340; converged | 0.256 → 0.275; Δ +0.020 [-0.033, +0.072]; floor 0.340; converged |
| 2 | raw | linear | 2 | 0.322 → 0.074; Δ -0.248 [-0.297, -0.207]; floor 0.355; converged | 0.322 → 0.504; Δ +0.182 [+0.125, +0.238]; floor 0.355; converged |
| 2 | raw | linear | 3 | 0.293 → 0.084; Δ -0.209 [-0.254, -0.168]; floor 0.406; converged | 0.293 → 0.537; Δ +0.244 [+0.188, +0.299]; floor 0.406; converged |
| 2 | raw | linear | 4 | 0.359 → 0.051; Δ -0.309 [-0.352, -0.260]; floor 0.375; converged | 0.359 → 0.562; Δ +0.203 [+0.152, +0.254]; floor 0.375; converged |
| 2 | raw | linear | 5 | 0.270 → 0.053; Δ -0.217 [-0.258, -0.174]; floor 0.404; converged | 0.270 → 0.600; Δ +0.330 [+0.271, +0.389]; floor 0.404; converged |
| 2 | raw | mlp64 | 1 | 0.557 → 0.977; Δ +0.420 [+0.379, +0.461]; floor 0.340; fixed budget; convergence not assessed | 0.557 → 0.473; Δ -0.084 [-0.129, -0.039]; floor 0.340; fixed budget; convergence not assessed |
| 2 | raw | mlp64 | 2 | 0.617 → 0.352; Δ -0.266 [-0.309, -0.223]; floor 0.355; fixed budget; convergence not assessed | 0.617 → 0.480; Δ -0.137 [-0.186, -0.092]; floor 0.355; fixed budget; convergence not assessed |
| 2 | raw | mlp64 | 3 | 0.586 → 0.393; Δ -0.193 [-0.232, -0.152]; floor 0.406; fixed budget; convergence not assessed | 0.586 → 0.561; Δ -0.025 [-0.065, +0.014]; floor 0.406; fixed budget; convergence not assessed |
| 2 | raw | mlp64 | 4 | 0.654 → 0.369; Δ -0.285 [-0.330, -0.242]; floor 0.375; fixed budget; convergence not assessed | 0.654 → 0.576; Δ -0.078 [-0.119, -0.037]; floor 0.375; fixed budget; convergence not assessed |
| 2 | raw | mlp64 | 5 | 0.633 → 0.400; Δ -0.232 [-0.277, -0.180]; floor 0.404; fixed budget; convergence not assessed | 0.633 → 0.625; Δ -0.008 [-0.057, +0.047]; floor 0.404; fixed budget; convergence not assessed |
| 2 | upper | linear | 1 | 0.268 → 0.977; Δ +0.709 [+0.672, +0.744]; floor 0.340; converged | 0.268 → 0.221; Δ -0.047 [-0.096, +0.004]; floor 0.340; converged |
| 2 | upper | linear | 2 | 0.354 → 0.055; Δ -0.299 [-0.344, -0.252]; floor 0.355; converged | 0.354 → 0.422; Δ +0.068 [+0.014, +0.121]; floor 0.355; converged |
| 2 | upper | linear | 3 | 0.309 → 0.061; Δ -0.248 [-0.293, -0.201]; floor 0.406; converged | 0.309 → 0.379; Δ +0.070 [+0.010, +0.125]; floor 0.406; converged |
| 2 | upper | linear | 4 | 0.381 → 0.062; Δ -0.318 [-0.363, -0.268]; floor 0.375; converged | 0.381 → 0.449; Δ +0.068 [+0.016, +0.121]; floor 0.375; converged |
| 2 | upper | linear | 5 | 0.287 → 0.045; Δ -0.242 [-0.283, -0.201]; floor 0.404; converged | 0.287 → 0.588; Δ +0.301 [+0.242, +0.361]; floor 0.404; converged |
| 2 | upper | mlp64 | 1 | 0.498 → 0.709; Δ +0.211 [+0.164, +0.258]; floor 0.340; fixed budget; convergence not assessed | 0.498 → 0.340; Δ -0.158 [-0.193, -0.125]; floor 0.340; fixed budget; convergence not assessed |
| 2 | upper | mlp64 | 2 | 0.615 → 0.355; Δ -0.260 [-0.299, -0.221]; floor 0.355; fixed budget; convergence not assessed | 0.615 → 0.355; Δ -0.260 [-0.299, -0.221]; floor 0.355; fixed budget; convergence not assessed |
| 2 | upper | mlp64 | 3 | 0.545 → 0.406; Δ -0.139 [-0.176, -0.104]; floor 0.406; fixed budget; convergence not assessed | 0.545 → 0.406; Δ -0.139 [-0.176, -0.104]; floor 0.406; fixed budget; convergence not assessed |
| 2 | upper | mlp64 | 4 | 0.588 → 0.375; Δ -0.213 [-0.250, -0.178]; floor 0.375; fixed budget; convergence not assessed | 0.588 → 0.375; Δ -0.213 [-0.250, -0.178]; floor 0.375; fixed budget; convergence not assessed |
| 2 | upper | mlp64 | 5 | 0.596 → 0.404; Δ -0.191 [-0.230, -0.154]; floor 0.404; fixed budget; convergence not assessed | 0.596 → 0.404; Δ -0.191 [-0.230, -0.154]; floor 0.404; fixed budget; convergence not assessed |

Because A is determined by the raw records, no such crossed-input test alone can establish which route a free network would choose on consistent data.
