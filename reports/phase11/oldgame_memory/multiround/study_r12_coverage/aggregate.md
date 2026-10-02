# r12 aggregate

Within r12; r11 comparisons are historical: curriculum and loss weighting changed.

Detailed predictions, exposures and prefix observations are retained in the hash-bound audit JSON files and aggregate.json.

## Qualifications

- Supplied A is exact; A-target is approximate. This is an operational comparison, not a matched comparison of equally exact A interfaces.
- r11 comparisons are historical: curriculum and loss weighting changed.
- The long panel (N³–N⁸), formerly labelled extrapolation, is explicitly trained and does not test unseen lengths.
- Competition within the encoder is a hypothesis, not an established mechanism.
- Board and recurrence associations can coexist; three seeds do not establish population variability around the threshold.

## Registered readings (verbatim)

Predeclare these readings:

| Outcome | Conclusion |
|---|---|
| Uniform passes after explicit coverage | Raw B-only training can realize B under this history distribution; r11 does not isolate board rarity as the cause |
| Uniform still fails, with identifiable board errors preceding failures | Board computation remains a candidate limitation after history coverage |
| Uniform fails despite correct board responses, including clear-N tests | Upper recurrence remains a limitation |
| Cutoff improves census and B more than uniform and decoy | Targeted boundary exposure supports a rarity contribution |
| Cutoff improves census but not B | Board repair is insufficient for predictive closure |
| A-target improves A but not B | Readable/computable A does not ensure its predictive use |
| A-supplied outperforms A-target | Exact A access helps under these matched conditions; inspect learned-A errors before attributing the difference to pathway |
| Both A conditions succeed | Either supplied access or auxiliary supervision can support B here |
| Equal-law predictive split appears | Control failure; interpret affected comparisons separately |



## Selected reading

{
  "0": [
    "Cause unresolved",
    "Exact A access helps under these matched conditions; inspect learned-A errors before attributing the difference to pathway",
    "Readable/computable A does not ensure its predictive use"
  ],
  "1": [
    "Board computation remains a candidate limitation after history coverage",
    "Board repair is insufficient for predictive closure",
    "Exact A access helps under these matched conditions; inspect learned-A errors before attributing the difference to pathway",
    "Readable/computable A does not ensure its predictive use"
  ],
  "2": [
    "Board computation remains a candidate limitation after history coverage",
    "Board repair is insufficient for predictive closure",
    "Readable/computable A does not ensure its predictive use"
  ]
}

## Comparison across arms and seeds

Continuous TV values, not just threshold decisions. Swap summaries use only the five registered deciding cases.

| Arm | Law | Seed | Update | Endpoint | Short mean TV | Short max TV | Long mean TV | Long max TV | Rerender TV | A rerender differences | Swap mean TV | Swap max TV | Failed swap cases (max TV) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uniform | original | 0 | 20000 | B_INCOMPLETE | 0.007413625018671155 | 0.03338451683521271 | 0.005046089199216415 | 0.027952253818511963 | 0.09188701957464218 | 0 | 0.008377392183650623 | 0.22425882518291473 | neutral_N: 0.13118600845336914; reset_L: 0.22425882518291473; same_category_substitution: 0.10530678927898407; set_H: 0.026119664311408997; upper_state_exchange_same_N: 0.10913218557834625 |
| uniform | original | 1 | 20000 | B_INCOMPLETE | 0.008789582294411957 | 0.020324476063251495 | 0.009284821979235858 | 0.17173947393894196 | 0.03873249888420105 | 0 | 0.009717582756738093 | 0.24968640506267548 | neutral_N: 0.023808114230632782; reset_L: 0.24968640506267548; same_category_substitution: 0.0209796279668808 |
| uniform | original | 2 | 20000 | B_INCOMPLETE | 0.012580977675194541 | 0.06642723083496094 | 0.012606528975690404 | 0.04589046537876129 | 0.03342696279287338 | 0 | 0.011940551752393896 | 0.25196143984794617 | neutral_N: 0.02154780924320221; reset_L: 0.25196143984794617; set_H: 0.08264163136482239 |
| uniform | equal | 0 | 20000 | PASS | 0.0029031517139325538 | 0.0031950175762176514 | 0.002937273840264728 | 0.00339498370885849 | 0.00017489492893218994 | 0 | 0.0023748164425011387 | 0.0031903237104415894 | none |
| uniform | equal | 1 | 20000 | PASS | 0.0019152221890787284 | 0.0019450932741165161 | 0.001947633340023458 | 0.002002626657485962 | 1.2665987014770508e-05 | 0 | 0.0015704251868142323 | 0.0019521266222000122 | none |
| uniform | equal | 2 | 20000 | PASS | 0.007156679950033625 | 0.007227152585983276 | 0.007265751948580146 | 0.007417887449264526 | 7.75754451751709e-05 | 0 | 0.005861728155816143 | 0.007240921258926392 | none |
| cutoff | original | 0 | 20000 | B_INCOMPLETE | 0.005727736395783722 | 0.04572927951812744 | 0.005165706582677861 | 0.016568079590797424 | 0.08978728204965591 | 0 | 0.0049639279763637615 | 0.04226572811603546 | reset_L: 0.028874099254608154; set_H: 0.04226572811603546 |
| cutoff | original | 1 | 20000 | B_INCOMPLETE | 0.009047237030851344 | 0.05161401629447937 | 0.009112764130501697 | 0.025096088647842407 | 0.06417924910783768 | 0 | 0.008350340310822834 | 0.13025221228599548 | reset_L: 0.13025221228599548; set_H: 0.04111267626285553 |
| cutoff | original | 2 | 20000 | B_INCOMPLETE | 0.009551061317324638 | 0.051641061902046204 | 0.010144928043397764 | 0.09875798225402832 | 0.015297308564186096 | 0 | 0.00783743892415342 | 0.062349021434783936 | reset_L: 0.045818671584129333; set_H: 0.062349021434783936 |
| cutoff | equal | 0 | 20000 | PASS | 0.0028462797636166215 | 0.0029008015990257263 | 0.002866833043905596 | 0.002956882119178772 | 5.189329385757446e-05 | 0 | 0.0023361757312985983 | 0.002923138439655304 | none |
| cutoff | equal | 1 | 20000 | PASS | 0.001919643177340428 | 0.002197578549385071 | 0.002024526164556543 | 0.002433463931083679 | 0.00021539628505706787 | 0 | 0.0015954067930579185 | 0.0022965073585510254 | none |
| cutoff | equal | 2 | 20000 | PASS | 0.007041523388276498 | 0.007148116827011108 | 0.007069116031440596 | 0.007287308573722839 | 5.8084726333618164e-05 | 0 | 0.005771459461274472 | 0.007193833589553833 | none |
| decoy | original | 0 | 20000 | B_INCOMPLETE | 0.007230776362121105 | 0.03446929156780243 | 0.005417828312298904 | 0.028196007013320923 | 0.028301283717155457 | 0 | 0.006859777855094184 | 0.12227970361709595 | reset_L: 0.12227970361709595; set_H: 0.05569356679916382 |
| decoy | original | 1 | 20000 | B_INCOMPLETE | 0.009256046498194337 | 0.0352565199136734 | 0.009678501713400086 | 0.018922775983810425 | 0.043580397963523865 | 0 | 0.009183932254514233 | 0.2547232657670975 | neutral_N: 0.027319610118865967; reset_L: 0.2547232657670975; same_category_substitution: 0.026502899825572968; upper_state_exchange_same_N: 0.027319610118865967 |
| decoy | original | 2 | 20000 | B_INCOMPLETE | 0.010014361895931264 | 0.04688940942287445 | 0.014200326249313852 | 0.021056033670902252 | 0.020798683166503906 | 0 | 0.009617195866832679 | 0.22363954782485962 | neutral_N: 0.025949954986572266; reset_L: 0.22363954782485962; set_H: 0.03390657901763916; upper_state_exchange_same_N: 0.02236005663871765 |
| decoy | equal | 0 | 20000 | PASS | 0.003068273227351407 | 0.0031638890504837036 | 0.0030393127623635032 | 0.0031460747122764587 | 6.268173456192017e-05 | 0 | 0.002515115076676011 | 0.003154247999191284 | none |
| decoy | equal | 1 | 20000 | PASS | 0.0020656262834866843 | 0.0022769421339035034 | 0.0020442334547018013 | 0.0022693872451782227 | 0.00018766522407531738 | 0 | 0.001710757909511978 | 0.002374514937400818 | none |
| decoy | equal | 2 | 20000 | PASS | 0.007158747486149271 | 0.007271334528923035 | 0.007251297511781256 | 0.007412418723106384 | 0.00033177435398101807 | 0 | 0.0058862026569179516 | 0.00729583203792572 | none |
| a_target | original | 0 | 20000 | B_INCOMPLETE | 0.010459846506516138 | 0.04923337697982788 | 0.008902375625135997 | 0.06496517360210419 | 0.0827530175447464 | 0 | 0.01409400153947486 | 0.22685766220092773 | neutral_N: 0.0729793906211853; reset_L: 0.22685766220092773; same_category_substitution: 0.08126229792833328; set_H: 0.07225871086120605; upper_state_exchange_same_N: 0.0729793906211853 |
| a_target | original | 1 | 20000 | B_INCOMPLETE | 0.012984539265744388 | 0.13295167684555054 | 0.012942217484426996 | 0.08777578175067902 | 0.059101976454257965 | 0 | 0.015453536338596181 | 0.23946064710617065 | neutral_N: 0.03532147407531738; reset_L: 0.23946064710617065; same_category_substitution: 0.06946486979722977; set_H: 0.11944742500782013; upper_state_exchange_same_N: 0.024979323148727417 |
| a_target | original | 2 | 20000 | B_INCOMPLETE | 0.014934074987346927 | 0.03955024480819702 | 0.015978765945571165 | 0.044798895716667175 | 0.05525996536016464 | 0 | 0.01735164146785709 | 0.24878539144992828 | neutral_N: 0.03320574760437012; reset_L: 0.24878539144992828; same_category_substitution: 0.05893535912036896; set_H: 0.13066786527633667; upper_state_exchange_same_N: 0.03320574760437012 |
| a_target | equal | 0 | 20000 | PASS | 0.003048936720006168 | 0.004377022385597229 | 0.0029422289226204157 | 0.0044009387493133545 | 0.0007337331771850586 | 0 | 0.0024794110054658217 | 0.004686437547206879 | none |
| a_target | equal | 1 | 20000 | PASS | 0.0024357925479610762 | 0.009857654571533203 | 0.0037966297046902278 | 0.015835627913475037 | 0.003416404128074646 | 0 | 0.0022111624182963915 | 0.01209266483783722 | none |
| a_target | equal | 2 | 20000 | PASS | 0.0069964241702109575 | 0.010771289467811584 | 0.00744898725921909 | 0.010005339980125427 | 0.00034196674823760986 | 0 | 0.0056782040364024315 | 0.008482500910758972 | none |
| a_supplied | original | 0 | 20000 | PASS | 0.004211361287161708 | 0.015675947070121765 | 0.004136030193573485 | 0.0145573690533638 | 0.013107940554618835 | 0 | 0.0036470651922916823 | 0.014821663498878479 | none |
| a_supplied | original | 1 | 20000 | PASS | 0.008588017080910504 | 0.009386129677295685 | 0.008480760424087444 | 0.010587267577648163 | 0.003327876329421997 | 0 | 0.00700211762027307 | 0.009532265365123749 | none |
| a_supplied | original | 2 | 20000 | B_INCOMPLETE | 0.009117206248144308 | 0.012580350041389465 | 0.009573165560141206 | 0.012217998504638672 | 0.008957996964454651 | 0 | 0.007269865166480568 | 0.05903680622577667 | reset_L: 0.05903680622577667 |
| a_supplied | equal | 0 | 20000 | PASS | 0.0028858198396240673 | 0.0028898119926452637 | 0.0028858010191470385 | 0.002899445593357086 | 3.8743019104003906e-07 | 0 | 0.0023613220440562477 | 0.002898760139942169 | none |
| a_supplied | equal | 1 | 20000 | PASS | 0.0019127971803148587 | 0.0019131898880004883 | 0.0019128180962676804 | 0.0019133985042572021 | 7.450580596923828e-08 | 0 | 0.0015650295694781976 | 0.0019133985042572021 | none |
| a_supplied | equal | 2 | 20000 | PASS | 0.007175254092241327 | 0.007176026701927185 | 0.007175729842856526 | 0.007176518440246582 | 5.960464477539063e-08 | 0 | 0.005870655306022276 | 0.0071756839752197266 | none |

## Diagnosis counts and concurrent findings

Counts describe selected worst-prefix histories, not a random sample. Board and recurrence evidence are both retained when concurrent.

| Run | Histories | Board-associated | Recurrence-associated | Unresolved | Non-deviating | Preceding | Coincident | Clear-N recurrence panels | Concurrent findings |
|---|---|---|---|---|---|---|---|---|---|
| a_supplied_equal_seed0 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_supplied_equal_seed1 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_supplied_equal_seed2 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_supplied_original_seed0 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_supplied_original_seed1 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_supplied_original_seed2 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_target_equal_seed0 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_target_equal_seed1 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_target_equal_seed2 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| a_target_original_seed0 | 18 | 1 | 0 | 11 | 6 | 0 | 1 | 0 | Board computation remains a candidate limitation after history coverage |
| a_target_original_seed1 | 18 | 2 | 2 | 14 | 0 | 0 | 2 | 0 | Board computation remains a candidate limitation after history coverage; Upper recurrence remains a limitation |
| a_target_original_seed2 | 18 | 1 | 0 | 16 | 1 | 1 | 0 | 0 | Board computation remains a candidate limitation after history coverage |
| cutoff_equal_seed0 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| cutoff_equal_seed1 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| cutoff_equal_seed2 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| cutoff_original_seed0 | 18 | 2 | 0 | 1 | 15 | 0 | 2 | 0 | Board computation remains a candidate limitation after history coverage |
| cutoff_original_seed1 | 18 | 3 | 0 | 2 | 13 | 0 | 3 | 1 | Board computation remains a candidate limitation after history coverage; Upper recurrence remains a limitation |
| cutoff_original_seed2 | 18 | 7 | 0 | 1 | 10 | 0 | 7 | 0 | Board computation remains a candidate limitation after history coverage |
| decoy_equal_seed0 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| decoy_equal_seed1 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| decoy_equal_seed2 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| decoy_original_seed0 | 18 | 1 | 1 | 1 | 15 | 0 | 1 | 0 | Board computation remains a candidate limitation after history coverage; Upper recurrence remains a limitation |
| decoy_original_seed1 | 18 | 1 | 0 | 2 | 15 | 0 | 1 | 0 | Board computation remains a candidate limitation after history coverage |
| decoy_original_seed2 | 18 | 3 | 2 | 1 | 12 | 0 | 3 | 1 | Board computation remains a candidate limitation after history coverage; Upper recurrence remains a limitation |
| uniform_equal_seed0 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| uniform_equal_seed1 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| uniform_equal_seed2 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | Cause unresolved |
| uniform_original_seed0 | 18 | 0 | 0 | 4 | 14 | 0 | 0 | 0 | Cause unresolved |
| uniform_original_seed1 | 18 | 1 | 0 | 1 | 16 | 0 | 1 | 0 | Board computation remains a candidate limitation after history coverage |
| uniform_original_seed2 | 18 | 2 | 0 | 6 | 10 | 0 | 2 | 0 | Board computation remains a candidate limitation after history coverage |

Original-law raw totals: {"chronology": {"COINCIDENT": 20, "NO_OBSERVED_CONSTITUENT_ERROR": 141, "NO_SEQUENCE_DEVIATION": 1, "PRECEDING": 0}, "counts": {"board_associated": 20, "non_deviating": 120, "recurrence_associated": 3, "unresolved": 19}, "runs": 9, "selected_histories": 162}

## A-target joint errors (registered rendering, original law)

| Seed | Boards | A-head category errors | B-signature errors | B errors with correct A category |
|---|---|---|---|---|
| 0 | 24435 | 237 | 473 | 326 |
| 1 | 24435 | 44 | 648 | 617 |
| 2 | 24435 | 58 | 815 | 770 |

A-supplied original-law seed 2: reset_L maximum TV 0.05903680622577667 on 160 cases; endpoint B_INCOMPLETE. Short and long law panels pass: True.

## a_supplied_equal_seed0

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 2.6087360711950634e-05 | 2.6092778858780154e-05 | 20975 | None | True | 3.8743019104003906e-07 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.0029319152235984802 |
| 1 | 24435 | None | 0 | 0.0029330477118492126 |
| 2 | 24435 | None | 0 | 0.0029329881072044373 |
| 3 | 24435 | None | 0 | 0.002932809293270111 |
| saved r9 | 101 | None | 0 | 0.0028866231441497803 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 1555/1555 |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.002885747468098998 | 0.002885952591896057 |
| L_single_round | 32 | 0.0028858622536063194 | 0.0028878003358840942 |
| N_run_1 | 64 | 0.0028857055585831404 | 0.002887152135372162 |
| N_run_2 | 64 | 0.0028859490994364023 | 0.0028898119926452637 |
| N_run_3 | 64 | 0.0028858084697276354 | 0.0028888285160064697 |
| N_run_4 | 64 | 0.002885754336602986 | 0.0028865262866020203 |
| N_run_5 | 64 | 0.002885745372623205 | 0.0028870999813079834 |
| N_run_6 | 64 | 0.0028859423473477364 | 0.0028892606496810913 |
| N_run_7 | 64 | 0.0028857941506430507 | 0.002899445593357086 |
| N_run_8 | 64 | 0.0028857614379376173 | 0.0028888285160064697 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.0028858010191470385 | 0.002899445593357086 | True |
| short | 192 | 0.0028858198396240673 | 0.0028898119926452637 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0956440937519074 | 0.01977796362712979 | 0.019918695517393586 | False | 24435/24435 |
| 1000 | 1.082504189014435 | 0.0003345747851562919 | 0.0005807732900101683 | True | 24435/24435 |
| 2000 | 1.0820094382762908 | 0.00026011613274022237 | 0.00021761234753347262 | True | 24435/24435 |
| 5000 | 1.0829097890853883 | 8.377279266824189e-05 | 2.9788765990909658e-05 | True | 24435/24435 |
| 10000 | 1.0835926926136017 | 4.542435314398574e-05 | 0.00010621287164596736 | True | 24435/24435 |
| 15000 | 1.0831993794441224 | 0.00019606164161999117 | 8.96201437914066e-06 | True | 24435/24435 |
| 20000 | 1.0820258641242981 | 2.9551609334248496e-05 | 2.6087360711950634e-05 | True | 24435/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 0 | None | None |
| 0 | 1 | 24435 | 0 | None | None |
| 0 | 2 | 24435 | 0 | None | None |
| 0 | 3 | 24435 | 0 | None | None |
| 1000 | 0 | 24435 | 0 | None | None |
| 1000 | 1 | 24435 | 0 | None | None |
| 1000 | 2 | 24435 | 0 | None | None |
| 1000 | 3 | 24435 | 0 | None | None |
| 2000 | 0 | 24435 | 0 | None | None |
| 2000 | 1 | 24435 | 0 | None | None |
| 2000 | 2 | 24435 | 0 | None | None |
| 2000 | 3 | 24435 | 0 | None | None |
| 5000 | 0 | 24435 | 0 | None | None |
| 5000 | 1 | 24435 | 0 | None | None |
| 5000 | 2 | 24435 | 0 | None | None |
| 5000 | 3 | 24435 | 0 | None | None |
| 10000 | 0 | 24435 | 0 | None | None |
| 10000 | 1 | 24435 | 0 | None | None |
| 10000 | 2 | 24435 | 0 | None | None |
| 10000 | 3 | 24435 | 0 | None | None |
| 15000 | 0 | 24435 | 0 | None | None |
| 15000 | 1 | 24435 | 0 | None | None |
| 15000 | 2 | 24435 | 0 | None | None |
| 15000 | 3 | 24435 | 0 | None | None |
| 20000 | 0 | 24435 | 0 | None | None |
| 20000 | 1 | 24435 | 0 | None | None |
| 20000 | 2 | 24435 | 0 | None | None |
| 20000 | 3 | 24435 | 0 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 0.7734375 | 0.0078125 [-0.037109375, 0.050830078124999956] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.828125 | 0.048828125 [0.0078125, 0.087890625] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.767578125 | -0.005859375 [-0.048828125, 0.037109375] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.84375 | 0.04296875 [0.00390625, 0.08208007812499996] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.83203125 | 0.03515625 [-0.0020019531249999972, 0.072265625] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.453125 | 0.08984375 [0.037060546875, 0.142578125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.369140625 | 0.044921875 [-0.0020019531249999972, 0.095703125] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.265625 | 0.029296875 [-0.0234375, 0.080078125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.34375 | 0.044921875 [-0.0078125, 0.095703125] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.35546875 | 0.05859375 [0.007763671875000003, 0.10942382812499996] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.935546875 | 0.02734375 [0.00390625, 0.052734375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.919921875 | 0.001953125 [-0.021484375, 0.0234375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.931640625 | 0.005859375 [-0.015625, 0.025390625] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.94921875 | 0.02734375 [0.005859375, 0.048828125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.935546875 | 0.0 [-0.0234375, 0.021484375] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.697265625 | 0.13671875 [0.087890625, 0.185546875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.591796875 | 0.029296875 [-0.017578125, 0.080078125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.65625 | 0.02734375 [-0.01953125, 0.072265625] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.625 | 0.0 [-0.048828125, 0.050830078124999956] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.6015625 | 0.04296875 [-0.003955078124999997, 0.091796875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.8515625 | 0.634765625 | -0.216796875 [-0.26171875, -0.16796875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.845703125 | 0.755859375 | -0.08984375 [-0.138671875, -0.04296875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.91015625 | 0.775390625 | -0.134765625 [-0.177734375, -0.08984375] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.9453125 | 0.796875 | -0.1484375 [-0.185546875, -0.111328125] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8828125 | 0.755859375 | -0.126953125 [-0.169921875, -0.0859375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.88671875 | 0.685546875 | -0.201171875 [-0.248046875, -0.15625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.904296875 | 0.462890625 | -0.44140625 [-0.492236328125, -0.392578125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.86328125 | 0.529296875 | -0.333984375 [-0.386767578125, -0.28510742187500004] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.86328125 | 0.4453125 | -0.41796875 [-0.466845703125, -0.36713867187500004] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.884765625 | 0.466796875 | -0.41796875 [-0.466796875, -0.36328125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.951171875 | 0.912109375 | -0.0390625 [-0.060546875, -0.017578125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.955078125 | 0.931640625 | -0.0234375 [-0.044921875, -0.001953125] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.96875 | 0.9375 | -0.03125 [-0.05078125, -0.01171875] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.962890625 | 0.95703125 | -0.005859375 [-0.025439453124999997, 0.013671875] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.953125 | 0.939453125 | -0.013671875 [-0.03515625, 0.0078125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.892578125 | 0.822265625 | -0.0703125 [-0.10546875, -0.03515625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.853515625 | 0.72265625 | -0.130859375 [-0.17578125, -0.0859375] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.8828125 | 0.767578125 | -0.115234375 [-0.156298828125, -0.07612304687500004] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.8828125 | 0.646484375 | -0.236328125 [-0.287109375, -0.19140625] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.884765625 | 0.71484375 | -0.169921875 [-0.21484375, -0.12885742187500004] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.002885952591896057 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.0028861016035079956 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0028864890336990356 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0028866901993751526 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0028865262866020203 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.002886563539505005 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.002886474132537842 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0028865858912467957 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.002887248992919922 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.0028878003358840942 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.002887152135372162 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.0028898119926452637 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.0028888285160064697 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0028864964842796326 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.0028870999813079834 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.0028892606496810913 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.002899445593357086 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0028888285160064697 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.002886645495891571 | True | [0.0028858184814453125, 0.002886645495891571, 0.0028874650597572327, 0.0028882846236228943, 0.002889104187488556, 0.0028899237513542175, 0.0028907358646392822, 0.0028915703296661377, 0.0028923675417900085] | [] | False |
| 2 | 64 | None | 0.002886645495891571 | True | [0.0028857141733169556, 0.002886541187763214, 0.002887345850467682, 0.0028881877660751343, 0.002889007329940796, 0.0028898194432258606, 0.002890653908252716, 0.002891451120376587, 0.0028922706842422485] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0028859288819755116 | 0.0028920546174049377 |
| reset_L | 160 | 0.002886275667697191 | 0.002898760139942169 |
| same_category_substitution | 128 | 1.7386628314852715e-07 | 7.82310962677002e-07 |
| set_H | 160 | 0.0028859164100140332 | 0.0028922855854034424 |
| upper_state_exchange_same_N | 64 | 0.00288592791184783 | 0.0028920546174049377 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_supplied_equal_seed1

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 1.1738770243788577e-05 | 1.1742418162568256e-05 | 21140 | None | True | 7.450580596923828e-08 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.0019140243530273438 |
| 1 | 24435 | None | 0 | 0.0019140690565109253 |
| 2 | 24435 | None | 0 | 0.0019139498472213745 |
| 3 | 24435 | None | 0 | 0.0019140839576721191 |
| saved r9 | 101 | None | 0 | 0.0019128769636154175 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 1555/1555 |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.0019127978011965752 | 0.0019128024578094482 |
| L_single_round | 32 | 0.001912787090986967 | 0.0019129067659378052 |
| N_run_1 | 64 | 0.0019127919804304838 | 0.0019129663705825806 |
| N_run_2 | 64 | 0.0019128071144223213 | 0.0019131898880004883 |
| N_run_3 | 64 | 0.001912802690640092 | 0.0019129514694213867 |
| N_run_4 | 64 | 0.0019128117710351944 | 0.0019130557775497437 |
| N_run_5 | 64 | 0.001912826905027032 | 0.0019130706787109375 |
| N_run_6 | 64 | 0.0019128096755594015 | 0.0019129663705825806 |
| N_run_7 | 64 | 0.001912824809551239 | 0.0019131451845169067 |
| N_run_8 | 64 | 0.0019128327257931232 | 0.0019133985042572021 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.0019128180962676804 | 0.0019133985042572021 | True |
| short | 192 | 0.0019127971803148587 | 0.0019131898880004883 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.08812091588974 | 0.010503813540562987 | 0.00989187569868219 | False | 24435/24435 |
| 1000 | 1.081895455121994 | 0.0002952556609670864 | 0.00018996138903357783 | True | 24435/24435 |
| 2000 | 1.0814792776107789 | 0.00013245675663711153 | 8.244120831112782e-05 | True | 24435/24435 |
| 5000 | 1.0821773397922516 | 0.00010993484458595049 | 5.9992990681724993e-05 | True | 24435/24435 |
| 10000 | 1.0820451402664184 | 5.733364586120615e-05 | 0.00012575161899968943 | True | 24435/24435 |
| 15000 | 1.0814927446842193 | 5.8933730195676046e-05 | 2.1668014347664583e-05 | True | 24435/24435 |
| 20000 | 1.0825833547115327 | 9.460920584388077e-05 | 1.1738770243788577e-05 | True | 24435/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 0 | None | None |
| 0 | 1 | 24435 | 0 | None | None |
| 0 | 2 | 24435 | 0 | None | None |
| 0 | 3 | 24435 | 0 | None | None |
| 1000 | 0 | 24435 | 0 | None | None |
| 1000 | 1 | 24435 | 0 | None | None |
| 1000 | 2 | 24435 | 0 | None | None |
| 1000 | 3 | 24435 | 0 | None | None |
| 2000 | 0 | 24435 | 0 | None | None |
| 2000 | 1 | 24435 | 0 | None | None |
| 2000 | 2 | 24435 | 0 | None | None |
| 2000 | 3 | 24435 | 0 | None | None |
| 5000 | 0 | 24435 | 0 | None | None |
| 5000 | 1 | 24435 | 0 | None | None |
| 5000 | 2 | 24435 | 0 | None | None |
| 5000 | 3 | 24435 | 0 | None | None |
| 10000 | 0 | 24435 | 0 | None | None |
| 10000 | 1 | 24435 | 0 | None | None |
| 10000 | 2 | 24435 | 0 | None | None |
| 10000 | 3 | 24435 | 0 | None | None |
| 15000 | 0 | 24435 | 0 | None | None |
| 15000 | 1 | 24435 | 0 | None | None |
| 15000 | 2 | 24435 | 0 | None | None |
| 15000 | 3 | 24435 | 0 | None | None |
| 20000 | 0 | 24435 | 0 | None | None |
| 20000 | 1 | 24435 | 0 | None | None |
| 20000 | 2 | 24435 | 0 | None | None |
| 20000 | 3 | 24435 | 0 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.783203125 | -0.01953125 [-0.052783203125, 0.013671875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.759765625 | 0.02734375 [-0.017578125, 0.07036132812499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.78125 | 0.03125 [-0.003955078124999997, 0.0703125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.857421875 | 0.091796875 [0.054638671875, 0.1328125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.779296875 | 0.013671875 [-0.0234375, 0.050830078124999956] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.232421875 | -0.076171875 [-0.12109375, -0.025390625] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.357421875 | 0.09375 [0.044921875, 0.138671875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.34375 | 0.04296875 [-0.009765625, 0.09375] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.5 | 0.240234375 [0.189453125, 0.294921875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.306640625 | -0.060546875 [-0.115234375, -0.009765625] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.919921875 | 0.01171875 [-0.01171875, 0.041015625] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.919921875 | 0.0078125 [-0.01171875, 0.02734375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.927734375 | 0.01953125 [-0.001953125, 0.04296875] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.96484375 | 0.025390625 [0.005859375, 0.046875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.927734375 | 0.001953125 [-0.021484375, 0.023486328124999956] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.50390625 | -0.103515625 [-0.1484375, -0.0546875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.66796875 | 0.06640625 [0.02734375, 0.111328125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.54296875 | -0.03125 [-0.080078125, 0.017626953124999956] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.65234375 | 0.083984375 [0.037109375, 0.13481445312499996] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.587890625 | -0.109375 [-0.160205078125, -0.060546875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.884765625 | 0.876953125 | -0.0078125 [-0.046875, 0.027392578124999956] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.873046875 | 0.826171875 | -0.046875 [-0.082080078125, -0.009765625] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.8203125 | 0.78515625 | -0.03515625 [-0.078125, 0.009765625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.880859375 | 0.884765625 | 0.00390625 [-0.03125, 0.041015625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.90234375 | 0.765625 | -0.13671875 [-0.177734375, -0.09375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.859375 | 0.806640625 | -0.052734375 [-0.1015625, -0.00390625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.85546875 | 0.67578125 | -0.1796875 [-0.23046875, -0.126953125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.8828125 | 0.666015625 | -0.216796875 [-0.265673828125, -0.169921875] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.892578125 | 0.66015625 | -0.232421875 [-0.283203125, -0.18549804687500004] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.904296875 | 0.59765625 | -0.306640625 [-0.355517578125, -0.2578125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.955078125 | 0.974609375 | 0.01953125 [-0.001953125, 0.039111328124999956] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.9375 | 0.943359375 | 0.005859375 [-0.017578125, 0.033203125] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.9375 | 0.955078125 | 0.017578125 [-0.005859375, 0.039111328124999956] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.95703125 | 0.9453125 | -0.01171875 [-0.029296875, 0.005859375] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.9609375 | 0.9453125 | -0.015625 [-0.037109375, 0.005859375] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.876953125 | 0.912109375 | 0.03515625 [-0.001953125, 0.072265625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.849609375 | 0.833984375 | -0.015625 [-0.056640625, 0.025439453124999956] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.865234375 | 0.794921875 | -0.0703125 [-0.111376953125, -0.02734375] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.8984375 | 0.806640625 | -0.091796875 [-0.130908203125, -0.05078125] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.904296875 | 0.779296875 | -0.125 [-0.169921875, -0.087890625] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0019128024578094482 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.0019129365682601929 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0019128918647766113 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0019129067659378052 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0019129961729049683 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0019130706787109375 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.0019129663705825806 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0019131451845169067 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.0019129514694213867 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.0019129067659378052 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.0019129663705825806 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.0019131898880004883 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.0019129514694213867 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0019130557775497437 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.0019130706787109375 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.001912921667098999 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0019130110740661621 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0019133985042572021 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0019128769636154175 | True | [0.0019127875566482544, 0.0019128620624542236, 0.0019129514694213867, 0.001913025975227356, 0.0019131004810333252, 0.0019131749868392944, 0.0019132345914840698, 0.001913323998451233, 0.0019133836030960083] | [] | False |
| 2 | 64 | None | 0.0019128769636154175 | True | [0.0019128024578094482, 0.0019128769636154175, 0.0019129514694213867, 0.0019130110740661621, 0.0019131004810333252, 0.0019131749868392944, 0.0019132345914840698, 0.001913323998451233, 0.0019133836030960083] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0019128134784599145 | 0.0019130706787109375 |
| reset_L | 160 | 0.0019127821549773216 | 0.0019133985042572021 |
| same_category_substitution | 128 | 6.565824151039124e-08 | 2.086162567138672e-07 |
| set_H | 160 | 0.0019127958454191684 | 0.0019131004810333252 |
| upper_state_exchange_same_N | 64 | 0.0019128085114061832 | 0.0019130706787109375 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_supplied_equal_seed2

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0001994844987400705 | 0.00019949748466969246 | 20992 | None | True | 5.960464477539063e-08 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.007176443934440613 |
| 1 | 24435 | None | 0 | 0.007176414132118225 |
| 2 | 24435 | None | 0 | 0.00717635452747345 |
| 3 | 24435 | None | 0 | 0.007176309823989868 |
| saved r9 | 101 | None | 0 | 0.007175445556640625 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 1555/1555 |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.007175073027610779 | 0.0071751028299331665 |
| L_single_round | 32 | 0.007175212725996971 | 0.007175534963607788 |
| N_run_1 | 64 | 0.007175259059295058 | 0.007175564765930176 |
| N_run_2 | 64 | 0.007175360340625048 | 0.007176026701927185 |
| N_run_3 | 64 | 0.007175432285293937 | 0.007175743579864502 |
| N_run_4 | 64 | 0.007175572449341416 | 0.007176026701927185 |
| N_run_5 | 64 | 0.007175697945058346 | 0.007176414132118225 |
| N_run_6 | 64 | 0.007175803184509277 | 0.007176309823989868 |
| N_run_7 | 64 | 0.007175899809226394 | 0.007176250219345093 |
| N_run_8 | 64 | 0.007175973383709788 | 0.007176518440246582 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.007175729842856526 | 0.007176518440246582 | True |
| short | 192 | 0.007175254092241327 | 0.007176026701927185 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.1008573389053344 | 0.026155439112335442 | 0.027403986872437405 | False | 24435/24435 |
| 1000 | 1.0813204836845398 | 0.0001804156840807991 | 7.490210032022126e-05 | True | 24435/24435 |
| 2000 | 1.0833181762695312 | 0.00019064003725361545 | 0.00016205449083740158 | False | 24435/24435 |
| 5000 | 1.0814539754390717 | 7.903444224211853e-05 | 4.0298032964287305e-05 | True | 24435/24435 |
| 10000 | 1.081680530309677 | 3.0190477968972117e-05 | 2.7262250610544928e-05 | True | 24435/24435 |
| 15000 | 1.083449251651764 | 4.673030769936304e-05 | 2.3857595886902025e-05 | True | 24435/24435 |
| 20000 | 1.0834543848037719 | 0.0001312319591306732 | 0.0001994844987400705 | True | 24435/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 0 | None | None |
| 0 | 1 | 24435 | 0 | None | None |
| 0 | 2 | 24435 | 0 | None | None |
| 0 | 3 | 24435 | 0 | None | None |
| 1000 | 0 | 24435 | 0 | None | None |
| 1000 | 1 | 24435 | 0 | None | None |
| 1000 | 2 | 24435 | 0 | None | None |
| 1000 | 3 | 24435 | 0 | None | None |
| 2000 | 0 | 24435 | 0 | None | None |
| 2000 | 1 | 24435 | 0 | None | None |
| 2000 | 2 | 24435 | 0 | None | None |
| 2000 | 3 | 24435 | 0 | None | None |
| 5000 | 0 | 24435 | 0 | None | None |
| 5000 | 1 | 24435 | 0 | None | None |
| 5000 | 2 | 24435 | 0 | None | None |
| 5000 | 3 | 24435 | 0 | None | None |
| 10000 | 0 | 24435 | 0 | None | None |
| 10000 | 1 | 24435 | 0 | None | None |
| 10000 | 2 | 24435 | 0 | None | None |
| 10000 | 3 | 24435 | 0 | None | None |
| 15000 | 0 | 24435 | 0 | None | None |
| 15000 | 1 | 24435 | 0 | None | None |
| 15000 | 2 | 24435 | 0 | None | None |
| 15000 | 3 | 24435 | 0 | None | None |
| 20000 | 0 | 24435 | 0 | None | None |
| 20000 | 1 | 24435 | 0 | None | None |
| 20000 | 2 | 24435 | 0 | None | None |
| 20000 | 3 | 24435 | 0 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.671875 | -0.072265625 [-0.115234375, -0.02734375] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.787109375 | 0.029296875 [-0.013671875, 0.07421875] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.7890625 | 0.041015625 [0.001953125, 0.08203125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.693359375 | -0.123046875 [-0.16796875, -0.07416992187500004] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.759765625 | 0.0390625 [-0.005859375, 0.08203125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.232421875 | -0.021484375 [-0.064453125, 0.02734375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.330078125 | 0.0078125 [-0.041064453125, 0.0546875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.294921875 | 0.001953125 [-0.044921875, 0.046875] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.283203125 | -0.076171875 [-0.126953125, -0.027294921875000044] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.32421875 | 0.0546875 [0.00390625, 0.10546875] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.92578125 | 0.001953125 [-0.01953125, 0.0234375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.919921875 | -0.00390625 [-0.029296875, 0.01953125] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.91796875 | -0.01171875 [-0.03515625, 0.0078125] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.923828125 | -0.009765625 [-0.025439453124999997, 0.00390625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.921875 | 0.009765625 [-0.01171875, 0.033203125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.572265625 | 0.015625 [-0.029296875, 0.0625] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.53515625 | -0.068359375 [-0.115234375, -0.0234375] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.525390625 | -0.041015625 [-0.083984375, 0.005908203124999956] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.583984375 | -0.037109375 [-0.083984375, 0.011767578124999956] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.599609375 | -0.044921875 [-0.09375, 0.005859375] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.9296875 | 0.818359375 | -0.111328125 [-0.150390625, -0.07421875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.8515625 | 0.8828125 | 0.03125 [-0.009765625, 0.072265625] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.80859375 | 0.837890625 | 0.029296875 [-0.013671875, 0.072265625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.904296875 | 0.80859375 | -0.095703125 [-0.138671875, -0.0546875] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.84375 | 0.77734375 | -0.06640625 [-0.109375, -0.0234375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.873046875 | 0.828125 | -0.044921875 [-0.087890625, -0.0038574218750000444] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.888671875 | 0.720703125 | -0.16796875 [-0.21484375, -0.12299804687500004] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.880859375 | 0.783203125 | -0.09765625 [-0.142578125, -0.052734375] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.919921875 | 0.75 | -0.169921875 [-0.216796875, -0.12690429687500004] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.904296875 | 0.654296875 | -0.25 [-0.298828125, -0.201171875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.96484375 | 0.9609375 | -0.00390625 [-0.025390625, 0.015625] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.95703125 | 0.9609375 | 0.00390625 [-0.017578125, 0.025390625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.943359375 | 0.970703125 | 0.02734375 [0.0078125, 0.046875] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.953125 | 0.94140625 | -0.01171875 [-0.033203125, 0.007861328124999956] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.955078125 | 0.9453125 | -0.009765625 [-0.03125, 0.01171875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.859375 | 0.888671875 | 0.029296875 [-0.0078125, 0.068359375] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.865234375 | 0.814453125 | -0.05078125 [-0.08984375, -0.01171875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.876953125 | 0.87109375 | -0.005859375 [-0.044921875, 0.03125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.88671875 | 0.833984375 | -0.052734375 [-0.091845703125, -0.01171875] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.89453125 | 0.7578125 | -0.13671875 [-0.179736328125, -0.091796875] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0071751028299331665 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.007175266742706299 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.007175654172897339 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.007175564765930176 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.007175743579864502 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.007175877690315247 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.007176041603088379 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0071761757135391235 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.007176235318183899 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.007175534963607788 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.007175564765930176 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.007176026701927185 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.007175743579864502 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.007176026701927185 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.007176414132118225 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.007176309823989868 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.007176250219345093 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.007176518440246582 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.007175251841545105 | True | [0.007175058126449585, 0.007175222039222717, 0.0071754008531570435, 0.00717557966709137, 0.007175758481025696, 0.007175937294960022, 0.007176116108894348, 0.007176294922828674, 0.0071764737367630005] | [] | False |
| 2 | 64 | None | 0.007175251841545105 | True | [0.007175058126449585, 0.007175251841545105, 0.007175430655479431, 0.0071755945682525635, 0.00717577338218689, 0.00717596709728241, 0.007176145911216736, 0.007176324725151062, 0.007176488637924194] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.007175250289340814 | 0.007175669074058533 |
| reset_L | 160 | 0.007175273634493351 | 0.0071756839752197266 |
| same_category_substitution | 128 | 5.192123353481293e-08 | 2.2351741790771484e-07 |
| set_H | 160 | 0.007175180688500404 | 0.0071754902601242065 |
| upper_state_exchange_same_N | 64 | 0.0071752178482711315 | 0.007175445556640625 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_supplied_original_seed0

Endpoint: PASS; first crossing: 10000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.00011363189232178806 | 7.67220657098865e-05 | 24238 | 0.9985779601694657 | True | 0.013107940554618835 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 0 | 1 | 0.023040026426315308 |
| 1 | 24435 | 0 | 1 | 0.023291930556297302 |
| 2 | 24435 | 0 | 1 | 0.023040026426315308 |
| 3 | 24435 | 0 | 1 | 0.022867664694786072 |
| saved r9 | 101 | 0 | 0 | 0.010759010910987854 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 1555/1555 |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.007513071410357952 | 0.015675947070121765 |
| L_single_round | 32 | 0.00197647069580853 | 0.006852865219116211 |
| N_run_1 | 64 | 0.003987682284787297 | 0.00779271125793457 |
| N_run_2 | 64 | 0.0039016305236145854 | 0.009746775031089783 |
| N_run_3 | 64 | 0.0038940723752602935 | 0.007527992129325867 |
| N_run_4 | 64 | 0.003987123724073172 | 0.008550956845283508 |
| N_run_5 | 64 | 0.003951447666622698 | 0.007841460406780243 |
| N_run_6 | 64 | 0.004090500180609524 | 0.014130309224128723 |
| N_run_7 | 64 | 0.004551009740680456 | 0.0145573690533638 |
| N_run_8 | 64 | 0.004342027474194765 | 0.010807402431964874 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.004136030193573485 | 0.0145573690533638 | True |
| short | 192 | 0.004211361287161708 | 0.015675947070121765 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0972562050819397 | 0.08093677788972854 | 0.08378873735635023 | False | 24435/24435 |
| 1000 | 1.0389802193641662 | 0.0008049413045227993 | 0.0005536571367393466 | False | 24435/24435 |
| 2000 | 1.0421611452102661 | 0.0007200919622846414 | 0.00038817318842310645 | False | 24435/24435 |
| 5000 | 1.0389564669132232 | 0.0004160596203200839 | 0.0008181761802760089 | False | 24435/24435 |
| 10000 | 1.042756476998329 | 0.00028105681736633414 | 0.0002777106946376915 | True | 24435/24435 |
| 15000 | 1.0393416011333465 | 0.00032599238138573126 | 0.0006249453768922733 | False | 24435/24435 |
| 20000 | 1.0389464384317397 | 0.00012772782699357776 | 0.00011363189232178806 | True | 24435/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 0 | 24326 | 24326 |
| 0 | 1 | 24435 | 0 | 24326 | 24326 |
| 0 | 2 | 24435 | 0 | 24326 | 24326 |
| 0 | 3 | 24435 | 0 | 24326 | 24326 |
| 1000 | 0 | 24435 | 0 | 4 | 4 |
| 1000 | 1 | 24435 | 0 | 6 | 6 |
| 1000 | 2 | 24435 | 0 | 5 | 5 |
| 1000 | 3 | 24435 | 0 | 5 | 5 |
| 2000 | 0 | 24435 | 0 | 4 | 4 |
| 2000 | 1 | 24435 | 0 | 6 | 6 |
| 2000 | 2 | 24435 | 0 | 7 | 7 |
| 2000 | 3 | 24435 | 0 | 7 | 7 |
| 5000 | 0 | 24435 | 0 | 1 | 1 |
| 5000 | 1 | 24435 | 0 | 1 | 1 |
| 5000 | 2 | 24435 | 0 | 1 | 1 |
| 5000 | 3 | 24435 | 0 | 1 | 1 |
| 10000 | 0 | 24435 | 0 | 0 | 0 |
| 10000 | 1 | 24435 | 0 | 0 | 0 |
| 10000 | 2 | 24435 | 0 | 0 | 0 |
| 10000 | 3 | 24435 | 0 | 0 | 0 |
| 15000 | 0 | 24435 | 0 | 2 | 2 |
| 15000 | 1 | 24435 | 0 | 1 | 1 |
| 15000 | 2 | 24435 | 0 | 1 | 1 |
| 15000 | 3 | 24435 | 0 | 2 | 2 |
| 20000 | 0 | 24435 | 0 | 0 | 0 |
| 20000 | 1 | 24435 | 0 | 0 | 0 |
| 20000 | 2 | 24435 | 0 | 0 | 0 |
| 20000 | 3 | 24435 | 0 | 0 | 0 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 0.939453125 | 0.173828125 [0.1328125, 0.2109375] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.716796875 | -0.0625 [-0.111328125, -0.013671875] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.6953125 | -0.078125 [-0.12890625, -0.03125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.810546875 | 0.009765625 [-0.02734375, 0.048828125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.8515625 | 0.0546875 [0.013671875, 0.095703125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.70703125 | 0.34375 [0.291015625, 0.396484375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.24609375 | -0.078125 [-0.125, -0.025341796875000044] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.3046875 | 0.068359375 [0.017578125, 0.12109375] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.416015625 | 0.1171875 [0.0625, 0.169921875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.40234375 | 0.10546875 [0.046875, 0.162109375] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.98046875 | 0.072265625 [0.05078125, 0.095703125] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.91796875 | 0.0 [-0.0234375, 0.0234375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.92578125 | 0.0 [-0.021484375, 0.019580078124999956] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.935546875 | 0.013671875 [-0.01171875, 0.037109375] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.9375 | 0.001953125 [-0.01953125, 0.0234375] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.85546875 | 0.294921875 [0.248046875, 0.34375] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.568359375 | 0.005859375 [-0.046875, 0.05859375] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.619140625 | -0.009765625 [-0.0546875, 0.037109375] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.7109375 | 0.0859375 [0.033203125, 0.13676757812499996] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.62109375 | 0.0625 [0.005859375, 0.1171875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.8515625 | 0.998046875 | 0.146484375 [0.1171875, 0.1796875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.845703125 | 0.736328125 | -0.109375 [-0.15625, -0.060546875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.91015625 | 0.802734375 | -0.107421875 [-0.150390625, -0.068359375] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.9453125 | 0.818359375 | -0.126953125 [-0.162158203125, -0.09174804687500004] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8828125 | 0.828125 | -0.0546875 [-0.093798828125, -0.015625] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.88671875 | 0.880859375 | -0.005859375 [-0.041064453125, 0.029296875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.904296875 | 0.521484375 | -0.3828125 [-0.43359375, -0.33198242187500004] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.86328125 | 0.6875 | -0.17578125 [-0.2265625, -0.12890625] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.86328125 | 0.623046875 | -0.240234375 [-0.291015625, -0.18940429687500004] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.884765625 | 0.630859375 | -0.25390625 [-0.300830078125, -0.208984375] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.951171875 | 1.0 | 0.048828125 [0.03125, 0.068359375] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.955078125 | 0.916015625 | -0.0390625 [-0.060546875, -0.017578125] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.96875 | 0.951171875 | -0.017578125 [-0.0390625, 0.001953125] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.962890625 | 0.9453125 | -0.017578125 [-0.03515625, -0.00390625] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.953125 | 0.9453125 | -0.0078125 [-0.029296875, 0.017578125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.892578125 | 0.896484375 | 0.00390625 [-0.03125, 0.0390625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.853515625 | 0.724609375 | -0.12890625 [-0.1796875, -0.080078125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.8828125 | 0.837890625 | -0.044921875 [-0.08203125, -0.009765625] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.8828125 | 0.802734375 | -0.080078125 [-0.12109375, -0.037109375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.884765625 | 0.78125 | -0.103515625 [-0.146533203125, -0.060498046875000044] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.015675947070121765 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.00779271125793457 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.009746775031089783 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.007527992129325867 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.008550956845283508 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.007841460406780243 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.014130309224128723 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0145573690533638 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.010807402431964874 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.006852865219116211 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.0023944303393363953 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.0025078654289245605 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.002444632351398468 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0024158209562301636 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.002385735511779785 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.0026606693863868713 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0029127970337867737 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0031914636492729187 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.006628766655921936 | True | [0.0019121766090393066, 0.0024393796920776367, 0.002775929868221283, 0.0031140297651290894, 0.003470689058303833, 0.0038579627871513367, 0.004287056624889374, 0.0047687143087387085, 0.005313083529472351] | [] | False |
| 2 | 64 | 64 | 0.006628766655921936 | True | [0.006997063755989075, 0.006628766655921936, 0.006217479705810547, 0.0061746686697006226, 0.006168879568576813, 0.006181411445140839, 0.0062064528465271, 0.0062418654561042786, 0.006287045776844025] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.004149643549074729 | 0.009955406188964844 |
| reset_L | 160 | 0.0017188901547342539 | 0.00315268337726593 |
| same_category_substitution | 128 | 0.00048647040966898203 | 0.0036482661962509155 |
| set_H | 160 | 0.007281400635838509 | 0.014821663498878479 |
| upper_state_exchange_same_N | 64 | 0.0041951186722144485 | 0.009955406188964844 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_supplied_original_seed1

Endpoint: PASS; first crossing: 20000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0002950452335329064 | 0.00025944531571980617 | 24201 | 0.9951574548333649 | True | 0.003327876329421997 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 1 | 10 | 0.22755993157625198 |
| 1 | 24435 | 1 | 12 | 0.22853081673383713 |
| 2 | 24435 | 1 | 12 | 0.22935061156749725 |
| 3 | 24435 | 1 | 11 | 0.22678470611572266 |
| saved r9 | 101 | 0 | 0 | 0.009492509067058563 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 1555/1555 |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.00903556845150888 | 0.009285405278205872 |
| L_single_round | 32 | 0.008181477664038539 | 0.009315013885498047 |
| N_run_1 | 64 | 0.008613867103122175 | 0.009335674345493317 |
| N_run_2 | 64 | 0.008541661081835628 | 0.009386129677295685 |
| N_run_3 | 64 | 0.008542210794985294 | 0.009572409093379974 |
| N_run_4 | 64 | 0.00852981093339622 | 0.009375505149364471 |
| N_run_5 | 64 | 0.008506335667334497 | 0.010587267577648163 |
| N_run_6 | 64 | 0.008438533986918628 | 0.009278647601604462 |
| N_run_7 | 64 | 0.008467901730909944 | 0.009366832673549652 |
| N_run_8 | 64 | 0.008399769430980086 | 0.009389296174049377 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.008480760424087444 | 0.010587267577648163 | True |
| short | 192 | 0.008588017080910504 | 0.009386129677295685 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0869620990753175 | 0.07038284048438072 | 0.06464165389851868 | False | 24435/24435 |
| 1000 | 1.0388381272554397 | 0.001040211008657934 | 0.002423743909271209 | False | 24435/24435 |
| 2000 | 1.0381435000896453 | 0.0006271959260629956 | 0.0004571865193201663 | False | 24435/24435 |
| 5000 | 1.0415135717391968 | 0.0007016638063214487 | 0.000747573643166677 | False | 24435/24435 |
| 10000 | 1.0375515180826187 | 0.00036566390041116394 | 0.0004728809076459412 | False | 24435/24435 |
| 15000 | 1.039270293712616 | 0.0004186045387177728 | 0.00048508556572133383 | False | 24435/24435 |
| 20000 | 1.0414299833774567 | 0.0002104092063382268 | 0.0002950452335329064 | True | 24435/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 0 | 23308 | 23308 |
| 0 | 1 | 24435 | 0 | 23306 | 23306 |
| 0 | 2 | 24435 | 0 | 23304 | 23304 |
| 0 | 3 | 24435 | 0 | 23267 | 23267 |
| 1000 | 0 | 24435 | 0 | 4 | 4 |
| 1000 | 1 | 24435 | 0 | 3 | 3 |
| 1000 | 2 | 24435 | 0 | 3 | 3 |
| 1000 | 3 | 24435 | 0 | 4 | 4 |
| 2000 | 0 | 24435 | 0 | 2 | 2 |
| 2000 | 1 | 24435 | 0 | 2 | 2 |
| 2000 | 2 | 24435 | 0 | 2 | 2 |
| 2000 | 3 | 24435 | 0 | 2 | 2 |
| 5000 | 0 | 24435 | 0 | 0 | 0 |
| 5000 | 1 | 24435 | 0 | 0 | 0 |
| 5000 | 2 | 24435 | 0 | 0 | 0 |
| 5000 | 3 | 24435 | 0 | 0 | 0 |
| 10000 | 0 | 24435 | 0 | 0 | 0 |
| 10000 | 1 | 24435 | 0 | 0 | 0 |
| 10000 | 2 | 24435 | 0 | 0 | 0 |
| 10000 | 3 | 24435 | 0 | 0 | 0 |
| 15000 | 0 | 24435 | 0 | 5 | 5 |
| 15000 | 1 | 24435 | 0 | 5 | 5 |
| 15000 | 2 | 24435 | 0 | 7 | 7 |
| 15000 | 3 | 24435 | 0 | 7 | 7 |
| 20000 | 0 | 24435 | 0 | 1 | 1 |
| 20000 | 1 | 24435 | 0 | 1 | 1 |
| 20000 | 2 | 24435 | 0 | 1 | 1 |
| 20000 | 3 | 24435 | 0 | 1 | 1 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.927734375 | 0.125 [0.091796875, 0.15625] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.765625 | 0.033203125 [-0.013671875, 0.08203125] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.81640625 | 0.06640625 [0.02734375, 0.107421875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.82421875 | 0.05859375 [0.015625, 0.1015625] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.81640625 | 0.05078125 [0.009765625, 0.087890625] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.73828125 | 0.4296875 [0.37890625, 0.48046875] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.322265625 | 0.05859375 [0.005859375, 0.111328125] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.390625 | 0.08984375 [0.033203125, 0.146484375] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.48046875 | 0.220703125 [0.173779296875, 0.275390625] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.41796875 | 0.05078125 [-0.007861328124999997, 0.107421875] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.9609375 | 0.052734375 [0.029296875, 0.078125] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.904296875 | -0.0078125 [-0.03125, 0.015625] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.939453125 | 0.03125 [0.005859375, 0.0546875] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.951171875 | 0.01171875 [-0.009765625, 0.03125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.955078125 | 0.029296875 [0.0078125, 0.05078125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.8359375 | 0.228515625 [0.17578125, 0.27734375] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.560546875 | -0.041015625 [-0.091796875, 0.009765625] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.666015625 | 0.091796875 [0.0390625, 0.14067382812499996] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.7109375 | 0.142578125 [0.091796875, 0.193359375] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.712890625 | 0.015625 [-0.031298828125, 0.064453125] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.884765625 | 1.0 | 0.115234375 [0.087890625, 0.142578125] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.873046875 | 0.65625 | -0.216796875 [-0.261767578125, -0.169921875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.8203125 | 0.794921875 | -0.025390625 [-0.068359375, 0.021484375] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.880859375 | 0.83984375 | -0.041015625 [-0.080078125, 0.0] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.90234375 | 0.8125 | -0.08984375 [-0.130859375, -0.052685546875000044] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.859375 | 0.802734375 | -0.056640625 [-0.093798828125, -0.009765625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.85546875 | 0.48046875 | -0.375 [-0.423828125, -0.3203125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.8828125 | 0.515625 | -0.3671875 [-0.416064453125, -0.318359375] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.892578125 | 0.623046875 | -0.26953125 [-0.314501953125, -0.22065429687500004] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.904296875 | 0.513671875 | -0.390625 [-0.439453125, -0.341796875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.955078125 | 1.0 | 0.044921875 [0.02734375, 0.060546875] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.9375 | 0.919921875 | -0.017578125 [-0.039111328125, 0.005859375] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.9375 | 0.94921875 | 0.01171875 [-0.009765625, 0.03515625] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.95703125 | 0.951171875 | -0.005859375 [-0.025390625, 0.015625] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.9609375 | 0.935546875 | -0.025390625 [-0.048828125, -0.001953125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.876953125 | 0.87890625 | 0.001953125 [-0.037109375, 0.0390625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.849609375 | 0.6796875 | -0.169921875 [-0.218798828125, -0.12109375] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.865234375 | 0.74609375 | -0.119140625 [-0.158203125, -0.08203125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.8984375 | 0.818359375 | -0.080078125 [-0.119189453125, -0.04296875] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.904296875 | 0.767578125 | -0.13671875 [-0.175830078125, -0.09565429687500004] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.009285405278205872 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.009335674345493317 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.009386129677295685 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.009572409093379974 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.009375505149364471 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.010587267577648163 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.009278647601604462 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.009366832673549652 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.009389296174049377 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.009315013885498047 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.008489340543746948 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.008546136319637299 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.008283838629722595 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.008390344679355621 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.008323051035404205 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.008174300193786621 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.00833701342344284 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.008462727069854736 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.009440429508686066 | True | [0.010093063116073608, 0.008747853338718414, 0.008733808994293213, 0.0087197944521904, 0.008705899119377136, 0.008692041039466858, 0.008678264915943146, 0.008664578199386597, 0.008650913834571838] | [] | False |
| 2 | 64 | 64 | 0.009440429508686066 | True | [0.00893700122833252, 0.009440429508686066, 0.0094870924949646, 0.009503260254859924, 0.009510107338428497, 0.009513437747955322, 0.009515486657619476, 0.009517215192317963, 0.009519264101982117] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.008554953887748221 | 0.009532265365123749 |
| reset_L | 160 | 0.007799912476912141 | 0.009383931756019592 |
| same_category_substitution | 128 | 0.0005361985531635582 | 0.004257403314113617 |
| set_H | 160 | 0.008889173856005073 | 0.009492307901382446 |
| upper_state_exchange_same_N | 64 | 0.008563319221138954 | 0.00947793573141098 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_supplied_original_seed2

Endpoint: B_INCOMPLETE; first crossing: 10000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.00025690829292554116 | 0.0002014980922956429 | 24245 | 0.9946410798943296 | False | 0.008957996964454651 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 1 | 51 | 0.2491816133260727 |
| 1 | 24435 | 1 | 53 | 0.24912889301776886 |
| 2 | 24435 | 1 | 55 | 0.2491416335105896 |
| 3 | 24435 | 1 | 52 | 0.2491436004638672 |
| saved r9 | 101 | 0 | 0 | 0.01674117147922516 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 24435/24435 | 1555/1555 |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.010642311302945018 | 0.012580350041389465 |
| L_single_round | 32 | 0.006621388019993901 | 0.008210927248001099 |
| N_run_1 | 64 | 0.009405038435943425 | 0.011155977845191956 |
| N_run_2 | 64 | 0.009314730647020042 | 0.011663973331451416 |
| N_run_3 | 64 | 0.009549329406581819 | 0.011710211634635925 |
| N_run_4 | 64 | 0.009416512795723975 | 0.012217998504638672 |
| N_run_5 | 64 | 0.009552801260724664 | 0.0110931396484375 |
| N_run_6 | 64 | 0.00957456580363214 | 0.011308908462524414 |
| N_run_7 | 64 | 0.00964534399099648 | 0.011212944984436035 |
| N_run_8 | 64 | 0.009700440103188157 | 0.01156027615070343 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.009573165560141206 | 0.012217998504638672 | True |
| short | 192 | 0.009117206248144308 | 0.012580350041389465 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.09831152677536 | 0.08727588750422001 | 0.08465618434682416 | False | 24435/24435 |
| 1000 | 1.0393410110473633 | 0.0006408637770800852 | 0.0011232044785253763 | False | 24435/24435 |
| 2000 | 1.0386306858062744 | 0.0008562126850301865 | 0.0005336114506763226 | False | 24435/24435 |
| 5000 | 1.0412533098459245 | 0.00043638847451802574 | 0.0006764887618390387 | False | 24435/24435 |
| 10000 | 1.0380090117454528 | 0.0004372557910755859 | 0.00010290495057080095 | True | 24435/24435 |
| 15000 | 1.040923557281494 | 0.00013769730510830415 | 0.00013635594254088324 | True | 24435/24435 |
| 20000 | 1.0393814611434937 | 0.0004216120426281122 | 0.00025690829292554116 | False | 24435/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 0 | 1944 | 1944 |
| 0 | 1 | 24435 | 0 | 1944 | 1944 |
| 0 | 2 | 24435 | 0 | 1944 | 1944 |
| 0 | 3 | 24435 | 0 | 1944 | 1944 |
| 1000 | 0 | 24435 | 0 | 1 | 1 |
| 1000 | 1 | 24435 | 0 | 1 | 1 |
| 1000 | 2 | 24435 | 0 | 1 | 1 |
| 1000 | 3 | 24435 | 0 | 1 | 1 |
| 2000 | 0 | 24435 | 0 | 0 | 0 |
| 2000 | 1 | 24435 | 0 | 0 | 0 |
| 2000 | 2 | 24435 | 0 | 0 | 0 |
| 2000 | 3 | 24435 | 0 | 0 | 0 |
| 5000 | 0 | 24435 | 0 | 2 | 2 |
| 5000 | 1 | 24435 | 0 | 2 | 2 |
| 5000 | 2 | 24435 | 0 | 2 | 2 |
| 5000 | 3 | 24435 | 0 | 2 | 2 |
| 10000 | 0 | 24435 | 0 | 0 | 0 |
| 10000 | 1 | 24435 | 0 | 0 | 0 |
| 10000 | 2 | 24435 | 0 | 0 | 0 |
| 10000 | 3 | 24435 | 0 | 0 | 0 |
| 15000 | 0 | 24435 | 0 | 0 | 0 |
| 15000 | 1 | 24435 | 0 | 0 | 0 |
| 15000 | 2 | 24435 | 0 | 0 | 0 |
| 15000 | 3 | 24435 | 0 | 0 | 0 |
| 20000 | 0 | 24435 | 0 | 1 | 1 |
| 20000 | 1 | 24435 | 0 | 1 | 1 |
| 20000 | 2 | 24435 | 0 | 1 | 1 |
| 20000 | 3 | 24435 | 0 | 1 | 1 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.88671875 | 0.142578125 [0.1015625, 0.185546875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.78515625 | 0.02734375 [-0.01953125, 0.07626953124999991] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.83984375 | 0.091796875 [0.04296875, 0.138671875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.849609375 | 0.033203125 [-0.005908203124999997, 0.072265625] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.798828125 | 0.078125 [0.031201171875000003, 0.126953125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.681640625 | 0.427734375 [0.375, 0.478515625] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.3046875 | -0.017578125 [-0.068359375, 0.03515625] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.326171875 | 0.033203125 [-0.017578125, 0.08208007812499996] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.44921875 | 0.08984375 [0.031201171875000003, 0.1484375] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.431640625 | 0.162109375 [0.10546875, 0.21875] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.96484375 | 0.041015625 [0.01953125, 0.06254882812499996] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.921875 | -0.001953125 [-0.029296875, 0.025390625] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.9375 | 0.0078125 [-0.017578125, 0.03125] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.955078125 | 0.021484375 [0.001953125, 0.04296875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.9375 | 0.025390625 [0.0, 0.052734375] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.869140625 | 0.3125 [0.265625, 0.36333007812499996] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.53515625 | -0.068359375 [-0.126953125, -0.015625] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.638671875 | 0.072265625 [0.021435546875000003, 0.12309570312499996] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.673828125 | 0.052734375 [0.0, 0.107421875] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.69921875 | 0.0546875 [-0.005859375, 0.111328125] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.9296875 | 1.0 | 0.0703125 [0.048828125, 0.091796875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.8515625 | 0.798828125 | -0.052734375 [-0.09765625, -0.0078125] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.80859375 | 0.830078125 | 0.021484375 [-0.025390625, 0.068359375] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.904296875 | 0.8359375 | -0.068359375 [-0.107421875, -0.03125] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.84375 | 0.8046875 | -0.0390625 [-0.080078125, 0.005859375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.873046875 | 0.8125 | -0.060546875 [-0.103515625, -0.017578125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.888671875 | 0.49609375 | -0.392578125 [-0.443408203125, -0.34375] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.880859375 | 0.453125 | -0.427734375 [-0.478564453125, -0.37495117187500004] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.919921875 | 0.5078125 | -0.412109375 [-0.457080078125, -0.359375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.904296875 | 0.50390625 | -0.400390625 [-0.447265625, -0.34760742187500004] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.96484375 | 1.0 | 0.03515625 [0.01953125, 0.052734375] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.95703125 | 0.90625 | -0.05078125 [-0.078125, -0.025341796875000044] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.943359375 | 0.947265625 | 0.00390625 [-0.015625, 0.021484375] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.953125 | 0.9375 | -0.015625 [-0.03515625, 0.005859375] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.955078125 | 0.931640625 | -0.0234375 [-0.048828125, 0.0] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.859375 | 0.82421875 | -0.03515625 [-0.076171875, 0.005859375] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.865234375 | 0.6328125 | -0.232421875 [-0.27734375, -0.181640625] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.876953125 | 0.65625 | -0.220703125 [-0.265625, -0.173828125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.88671875 | 0.6875 | -0.19921875 [-0.244140625, -0.154296875] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.89453125 | 0.634765625 | -0.259765625 [-0.302734375, -0.2109375] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.012580350041389465 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.011155977845191956 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.011663973331451416 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.011710211634635925 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.012217998504638672 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0110931396484375 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.011308908462524414 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.011212944984436035 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.01156027615070343 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.008210927248001099 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.009847283363342285 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.009747177362442017 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.010469652712345123 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.009905390441417694 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.010334312915802002 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.01032315194606781 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.010388657450675964 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.011098980903625488 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.012378588318824768 | True | [0.007400177419185638, 0.009237349033355713, 0.009267203509807587, 0.009307004511356354, 0.0093507319688797, 0.00939430296421051, 0.009443722665309906, 0.009497642517089844, 0.009551286697387695] | [] | False |
| 2 | 64 | 64 | 0.012378588318824768 | True | [0.012141153216362, 0.012378588318824768, 0.01226159930229187, 0.012225568294525146, 0.012238308787345886, 0.012271195650100708, 0.01231202483177185, 0.01235605776309967, 0.012401476502418518] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.009278069987582663 | 0.010957673192024231 |
| reset_L | 160 | 0.006122065242379904 | 0.05903680622577667 |
| same_category_substitution | 128 | 0.00024154508719220757 | 0.002778865396976471 |
| set_H | 160 | 0.010830821190029382 | 0.018635734915733337 |
| upper_state_exchange_same_N | 64 | 0.009269000613130629 | 0.010884642601013184 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_target_equal_seed0

Endpoint: PASS; first crossing: 5000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 2.996826235054337e-05 | 2.9302228652679515e-05 | 20975 | None | True | 0.0007337331771850586 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.009242437779903412 |
| 1 | 24435 | None | 0 | 0.00727478414773941 |
| 2 | 24435 | None | 0 | 0.008736945688724518 |
| 3 | 24435 | None | 0 | 0.009589947760105133 |
| saved r9 | 101 | None | 0 | 0.003946855664253235 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 23672/24435 | 23411/24435 | 23561/24435 | 23624/24435 | 23498/24435 | 20143/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.003086000680923462 | 0.0035653337836265564 |
| L_single_round | 32 | 0.003066276665776968 | 0.003973625600337982 |
| N_run_1 | 64 | 0.0030881590209901333 | 0.003523208200931549 |
| N_run_2 | 64 | 0.0029825124656781554 | 0.004377022385597229 |
| N_run_3 | 64 | 0.002929226728156209 | 0.0038361772894859314 |
| N_run_4 | 64 | 0.002879540785215795 | 0.0038488954305648804 |
| N_run_5 | 64 | 0.0029985107248649 | 0.004121251404285431 |
| N_run_6 | 64 | 0.0028951234417036176 | 0.00392652302980423 |
| N_run_7 | 64 | 0.0029930351302027702 | 0.0044009387493133545 |
| N_run_8 | 64 | 0.002957936725579202 | 0.004184916615486145 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.0029422289226204157 | 0.0044009387493133545 | True |
| short | 192 | 0.003048936720006168 | 0.004377022385597229 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0980968952178956 | 0.02337919408455491 | 0.023685100186257385 | False | 0/24435 |
| 1000 | 1.08252312541008 | 0.0004574459002469666 | 0.000767083538792241 | False | 4467/24435 |
| 2000 | 1.0819841718673706 | 0.0003707547088561114 | 0.0002646421282259089 | False | 9200/24435 |
| 5000 | 1.0829278230667114 | 5.8452056609894495e-05 | 2.5172792491045388e-05 | True | 14916/24435 |
| 10000 | 1.083610430955887 | 5.189558668462269e-05 | 0.0001143787859260098 | True | 17944/24435 |
| 15000 | 1.0832108438014985 | 0.0002005323816922555 | 1.2634987959558823e-05 | True | 19327/24435 |
| 20000 | 1.0820273756980896 | 3.209504372534866e-05 | 2.996826235054337e-05 | True | 20143/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | None | None |
| 0 | 1 | 24435 | 17969 | None | None |
| 0 | 2 | 24435 | 17963 | None | None |
| 0 | 3 | 24435 | 17989 | None | None |
| 1000 | 0 | 24435 | 3995 | None | None |
| 1000 | 1 | 24435 | 3970 | None | None |
| 1000 | 2 | 24435 | 4033 | None | None |
| 1000 | 3 | 24435 | 4012 | None | None |
| 2000 | 0 | 24435 | 1855 | None | None |
| 2000 | 1 | 24435 | 1893 | None | None |
| 2000 | 2 | 24435 | 1908 | None | None |
| 2000 | 3 | 24435 | 1889 | None | None |
| 5000 | 0 | 24435 | 931 | None | None |
| 5000 | 1 | 24435 | 932 | None | None |
| 5000 | 2 | 24435 | 955 | None | None |
| 5000 | 3 | 24435 | 942 | None | None |
| 10000 | 0 | 24435 | 365 | None | None |
| 10000 | 1 | 24435 | 404 | None | None |
| 10000 | 2 | 24435 | 371 | None | None |
| 10000 | 3 | 24435 | 369 | None | None |
| 15000 | 0 | 24435 | 290 | None | None |
| 15000 | 1 | 24435 | 321 | None | None |
| 15000 | 2 | 24435 | 308 | None | None |
| 15000 | 3 | 24435 | 289 | None | None |
| 20000 | 0 | 24435 | 210 | None | None |
| 20000 | 1 | 24435 | 236 | None | None |
| 20000 | 2 | 24435 | 227 | None | None |
| 20000 | 3 | 24435 | 209 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 0.99609375 | 0.23046875 [0.19140625, 0.267578125] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.974609375 | 0.1953125 [0.158203125, 0.23247070312499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.96875 | 0.1953125 [0.158203125, 0.23046875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.9609375 | 0.16015625 [0.126953125, 0.1953125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.943359375 | 0.146484375 [0.109375, 0.18754882812499996] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.951171875 | 0.587890625 [0.537109375, 0.630859375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.90625 | 0.58203125 [0.541015625, 0.626953125] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.931640625 | 0.6953125 [0.65234375, 0.736328125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.93359375 | 0.634765625 [0.591748046875, 0.675830078125] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.947265625 | 0.650390625 [0.607421875, 0.69140625] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.994140625 | 0.0859375 [0.064453125, 0.111328125] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.98046875 | 0.0625 [0.0390625, 0.0859375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.984375 | 0.05859375 [0.0390625, 0.08203125] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.962890625 | 0.041015625 [0.015625, 0.064453125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.97265625 | 0.037109375 [0.017578125, 0.05859375] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.9453125 | 0.384765625 [0.34375, 0.427734375] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.9140625 | 0.3515625 [0.30859375, 0.39453125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.953125 | 0.32421875 [0.28515625, 0.365234375] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.9375 | 0.3125 [0.2734375, 0.353515625] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.931640625 | 0.373046875 [0.331982421875, 0.41796875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 0.904296875 | 0.111328125 [0.076171875, 0.150390625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.96484375 | 0.16796875 [0.1328125, 0.203125] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.943359375 | 0.140625 [0.099609375, 0.1796875] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.947265625 | 0.11328125 [0.080078125, 0.1484375] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.919921875 | 0.115234375 [0.068359375, 0.15434570312499996] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.763671875 | 0.3828125 [0.330029296875, 0.435546875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.806640625 | 0.466796875 [0.419921875, 0.519580078125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.783203125 | 0.5078125 [0.45703125, 0.556640625] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.86328125 | 0.56640625 [0.517578125, 0.61328125] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.83984375 | 0.53125 [0.48046875, 0.574267578125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.962890625 | 0.052734375 [0.02734375, 0.080078125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.982421875 | 0.064453125 [0.0390625, 0.08984375] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.982421875 | 0.056640625 [0.03515625, 0.07817382812499996] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.96875 | 0.03515625 [0.01171875, 0.060546875] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.970703125 | 0.048828125 [0.025390625, 0.07421875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.8671875 | 0.306640625 [0.2578125, 0.353515625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.8671875 | 0.30859375 [0.26171875, 0.357421875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.861328125 | 0.259765625 [0.212890625, 0.3046875] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.884765625 | 0.302734375 [0.2578125, 0.349609375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.89453125 | 0.345703125 [0.30078125, 0.392578125] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0035653337836265564 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.0035174116492271423 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0035700723528862 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0038361772894859314 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0038488954305648804 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.00373164564371109 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.00392652302980423 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0037270039319992065 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.0038266703486442566 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.003973625600337982 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.003523208200931549 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.004377022385597229 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.003588452935218811 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0035642609000205994 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.004121251404285431 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.0035776495933532715 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0044009387493133545 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.004184916615486145 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0036287307739257812 | True | [0.002860434353351593, 0.0030780285596847534, 0.0032940730452537537, 0.0035085976123809814, 0.0037216171622276306, 0.00393318384885788, 0.0041432976722717285, 0.004351995885372162, 0.004559323191642761] | [] | False |
| 2 | 64 | None | 0.0036287307739257812 | True | [0.0034125447273254395, 0.0036287307739257812, 0.0038433820009231567, 0.004056505858898163, 0.00426812469959259, 0.004478298127651215, 0.004687011241912842, 0.004894323647022247, 0.005100265145301819] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0029861503280699253 | 0.003827899694442749 |
| reset_L | 160 | 0.002876603463664651 | 0.004686437547206879 |
| same_category_substitution | 128 | 0.00012863666051998734 | 0.0004071146249771118 |
| set_H | 160 | 0.003149258205667138 | 0.004412174224853516 |
| upper_state_exchange_same_N | 64 | 0.0029931425815448165 | 0.0038136690855026245 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_target_equal_seed1

Endpoint: PASS; first crossing: 2000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 6.955808137494796e-05 | 7.98256417133372e-05 | 21140 | None | True | 0.003416404128074646 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.017601385712623596 |
| 1 | 24435 | None | 0 | 0.017178863286972046 |
| 2 | 24435 | None | 0 | 0.015853896737098694 |
| 3 | 24435 | None | 0 | 0.01592501997947693 |
| saved r9 | 101 | None | 0 | 0.007265836000442505 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 23748/24435 | 23056/24435 | 23289/24435 | 23272/24435 | 23421/24435 | 19299/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.0019277632236480713 | 0.0028939545154571533 |
| L_single_round | 32 | 0.00271284650079906 | 0.009857654571533203 |
| N_run_1 | 64 | 0.0022688162280246615 | 0.004551351070404053 |
| N_run_2 | 64 | 0.002718256553635001 | 0.00799337774515152 |
| N_run_3 | 64 | 0.0024946510093286633 | 0.004920870065689087 |
| N_run_4 | 64 | 0.003397831111215055 | 0.010343998670578003 |
| N_run_5 | 64 | 0.00400737370364368 | 0.015835627913475037 |
| N_run_6 | 64 | 0.0037077328888699412 | 0.009679198265075684 |
| N_run_7 | 64 | 0.0041380226612091064 | 0.011307649314403534 |
| N_run_8 | 64 | 0.005034166853874922 | 0.011317886412143707 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.0037966297046902278 | 0.015835627913475037 | True |
| short | 192 | 0.0024357925479610762 | 0.009857654571533203 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0897325658798218 | 0.012910984400659799 | 0.01256583943681835 | False | 0/24435 |
| 1000 | 1.0820075321197509 | 0.0004436632845317945 | 0.00037099129601038616 | False | 4576/24435 |
| 2000 | 1.0815258252620696 | 0.00018995072474353947 | 0.00011205128088853363 | True | 8103/24435 |
| 5000 | 1.0821989858150483 | 0.00013793258258374408 | 0.00017707032454754857 | True | 13522/24435 |
| 10000 | 1.0820711624622346 | 6.142958622604055e-05 | 0.00012554231474166686 | True | 16468/24435 |
| 15000 | 1.0814947259426118 | 6.20641548613321e-05 | 2.3428588031888055e-05 | True | 18141/24435 |
| 20000 | 1.082573765516281 | 0.00012842340982388123 | 6.955808137494796e-05 | True | 19299/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | None | None |
| 0 | 1 | 24435 | 14906 | None | None |
| 0 | 2 | 24435 | 14976 | None | None |
| 0 | 3 | 24435 | 14881 | None | None |
| 1000 | 0 | 24435 | 2987 | None | None |
| 1000 | 1 | 24435 | 3043 | None | None |
| 1000 | 2 | 24435 | 3059 | None | None |
| 1000 | 3 | 24435 | 3032 | None | None |
| 2000 | 0 | 24435 | 1620 | None | None |
| 2000 | 1 | 24435 | 1632 | None | None |
| 2000 | 2 | 24435 | 1653 | None | None |
| 2000 | 3 | 24435 | 1639 | None | None |
| 5000 | 0 | 24435 | 826 | None | None |
| 5000 | 1 | 24435 | 802 | None | None |
| 5000 | 2 | 24435 | 803 | None | None |
| 5000 | 3 | 24435 | 837 | None | None |
| 10000 | 0 | 24435 | 391 | None | None |
| 10000 | 1 | 24435 | 404 | None | None |
| 10000 | 2 | 24435 | 387 | None | None |
| 10000 | 3 | 24435 | 396 | None | None |
| 15000 | 0 | 24435 | 273 | None | None |
| 15000 | 1 | 24435 | 278 | None | None |
| 15000 | 2 | 24435 | 279 | None | None |
| 15000 | 3 | 24435 | 306 | None | None |
| 20000 | 0 | 24435 | 258 | None | None |
| 20000 | 1 | 24435 | 255 | None | None |
| 20000 | 2 | 24435 | 248 | None | None |
| 20000 | 3 | 24435 | 279 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.98828125 | 0.185546875 [0.150390625, 0.220703125] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.95703125 | 0.224609375 [0.183544921875, 0.267578125] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.97265625 | 0.22265625 [0.185546875, 0.26171875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.974609375 | 0.208984375 [0.171875, 0.24609375] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.96875 | 0.203125 [0.164013671875, 0.240234375] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.958984375 | 0.650390625 [0.609326171875, 0.693359375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.904296875 | 0.640625 [0.595703125, 0.68359375] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.91796875 | 0.6171875 [0.57421875, 0.66015625] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.927734375 | 0.66796875 [0.62890625, 0.708984375] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.923828125 | 0.556640625 [0.50390625, 0.603515625] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.982421875 | 0.07421875 [0.052734375, 0.099609375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.9609375 | 0.048828125 [0.0234375, 0.07231445312499996] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.9765625 | 0.068359375 [0.04296875, 0.09375] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.97265625 | 0.033203125 [0.01171875, 0.052734375] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.97265625 | 0.046875 [0.0234375, 0.0703125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.962890625 | 0.35546875 [0.31640625, 0.39653320312499996] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.912109375 | 0.310546875 [0.267578125, 0.35161132812499996] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.912109375 | 0.337890625 [0.296826171875, 0.380859375] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.92578125 | 0.357421875 [0.314453125, 0.40234375] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.92578125 | 0.228515625 [0.1875, 0.271484375] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 0.875 | 0.064453125 [0.02734375, 0.1015625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.892578125 | 0.126953125 [0.081982421875, 0.16997070312499996] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.89453125 | 0.142578125 [0.099609375, 0.1875] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.955078125 | 0.208984375 [0.169921875, 0.25] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.87890625 | 0.087890625 [0.05078125, 0.126953125] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.841796875 | 0.49609375 [0.447265625, 0.544921875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.712890625 | 0.412109375 [0.357421875, 0.466796875] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.7109375 | 0.38671875 [0.337841796875, 0.43754882812499996] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.8203125 | 0.53515625 [0.48828125, 0.583984375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.7421875 | 0.33984375 [0.287109375, 0.39262695312499996] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 0.96484375 | 0.041015625 [0.015625, 0.0625] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.947265625 | 0.044921875 [0.015625, 0.072265625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.974609375 | 0.0546875 [0.03125, 0.078125] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.970703125 | 0.0390625 [0.01953125, 0.064453125] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.970703125 | 0.046875 [0.021484375, 0.07421875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.923828125 | 0.322265625 [0.28125, 0.365234375] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.796875 | 0.25 [0.203125, 0.296875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.849609375 | 0.287109375 [0.240234375, 0.33403320312499996] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.87109375 | 0.291015625 [0.24609375, 0.3359375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.84765625 | 0.16015625 [0.1171875, 0.20317382812499996] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0028939545154571533 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.004551351070404053 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.00799337774515152 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.004119858145713806 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.010343998670578003 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0075095295906066895 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.007844895124435425 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.009133651852607727 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.010061956942081451 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.009857654571533203 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.004493460059165955 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.006024882197380066 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.004920870065689087 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.007139243185520172 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.015835627913475037 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.009679198265075684 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.011307649314403534 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.011317886412143707 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.003048941493034363 | True | [0.0018038451671600342, 0.00253121554851532, 0.003922455012798309, 0.00571267306804657, 0.0074942633509635925, 0.00926719605922699, 0.011031314730644226, 0.012786559760570526, 0.014532819390296936] | [] | False |
| 2 | 64 | None | 0.003048941493034363 | True | [0.0018757283687591553, 0.003048941493034363, 0.004841715097427368, 0.00662587583065033, 0.008401311933994293, 0.010167963802814484, 0.011925719678401947, 0.013674482703208923, 0.015414200723171234] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0024772935236493745 | 0.01209266483783722 |
| reset_L | 160 | 0.002786976285278797 | 0.007601983845233917 |
| same_category_substitution | 128 | 0.0008030332392081618 | 0.004139013588428497 |
| set_H | 160 | 0.0023947178386151792 | 0.009060099720954895 |
| upper_state_exchange_same_N | 64 | 0.0023306042421609163 | 0.007194600999355316 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_target_equal_seed2

Endpoint: PASS; first crossing: 2000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.00020328896403610204 | 0.00020349606005727288 | 20992 | None | True | 0.00034196674823760986 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.012144908308982849 |
| 1 | 24435 | None | 0 | 0.013073667883872986 |
| 2 | 24435 | None | 0 | 0.011861458420753479 |
| 3 | 24435 | None | 0 | 0.012457087635993958 |
| saved r9 | 101 | None | 0 | 0.00793340802192688 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24111/24435 | 23454/24435 | 23397/24435 | 23312/24435 | 23326/24435 | 19988/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.006915797013789415 | 0.007330149412155151 |
| L_single_round | 32 | 0.0068036033771932125 | 0.007568269968032837 |
| N_run_1 | 64 | 0.007037639617919922 | 0.010771289467811584 |
| N_run_2 | 64 | 0.007091932697221637 | 0.009631484746932983 |
| N_run_3 | 64 | 0.0071849641390144825 | 0.008445203304290771 |
| N_run_4 | 64 | 0.007357905386015773 | 0.010005339980125427 |
| N_run_5 | 64 | 0.007436495972797275 | 0.009142950177192688 |
| N_run_6 | 64 | 0.007430735044181347 | 0.008624613285064697 |
| N_run_7 | 64 | 0.0075902019161731005 | 0.008824154734611511 |
| N_run_8 | 64 | 0.007693621097132564 | 0.00921843945980072 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.00744898725921909 | 0.010005339980125427 | True |
| short | 192 | 0.0069964241702109575 | 0.010771289467811584 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.1007735872268676 | 0.0261952000297606 | 0.026562348597121994 | False | 0/24435 |
| 1000 | 1.081331672668457 | 0.00031785141487489455 | 0.0001946272465790267 | False | 3853/24435 |
| 2000 | 1.0834221315383912 | 0.00019244045310188085 | 0.00015832963899148111 | True | 8282/24435 |
| 5000 | 1.0814806401729584 | 0.00011425958808104043 | 4.988574580486745e-05 | True | 14500/24435 |
| 10000 | 1.081681374311447 | 3.276860778896662e-05 | 5.1144913155719636e-05 | True | 17631/24435 |
| 15000 | 1.0834450900554657 | 5.397206474071936e-05 | 3.029958961411845e-05 | True | 19195/24435 |
| 20000 | 1.0834725761413575 | 0.00014022472981196189 | 0.00020328896403610204 | True | 19988/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | None | None |
| 0 | 1 | 24435 | 16708 | None | None |
| 0 | 2 | 24435 | 16621 | None | None |
| 0 | 3 | 24435 | 16820 | None | None |
| 1000 | 0 | 24435 | 3608 | None | None |
| 1000 | 1 | 24435 | 3527 | None | None |
| 1000 | 2 | 24435 | 3550 | None | None |
| 1000 | 3 | 24435 | 3531 | None | None |
| 2000 | 0 | 24435 | 1355 | None | None |
| 2000 | 1 | 24435 | 1356 | None | None |
| 2000 | 2 | 24435 | 1341 | None | None |
| 2000 | 3 | 24435 | 1398 | None | None |
| 5000 | 0 | 24435 | 534 | None | None |
| 5000 | 1 | 24435 | 550 | None | None |
| 5000 | 2 | 24435 | 546 | None | None |
| 5000 | 3 | 24435 | 534 | None | None |
| 10000 | 0 | 24435 | 292 | None | None |
| 10000 | 1 | 24435 | 328 | None | None |
| 10000 | 2 | 24435 | 311 | None | None |
| 10000 | 3 | 24435 | 321 | None | None |
| 15000 | 0 | 24435 | 177 | None | None |
| 15000 | 1 | 24435 | 166 | None | None |
| 15000 | 2 | 24435 | 170 | None | None |
| 15000 | 3 | 24435 | 187 | None | None |
| 20000 | 0 | 24435 | 171 | None | None |
| 20000 | 1 | 24435 | 162 | None | None |
| 20000 | 2 | 24435 | 162 | None | None |
| 20000 | 3 | 24435 | 160 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.966796875 | 0.22265625 [0.187451171875, 0.26171875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.955078125 | 0.197265625 [0.158203125, 0.236328125] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.9765625 | 0.228515625 [0.19140625, 0.265625] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.947265625 | 0.130859375 [0.09375, 0.16796875] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.984375 | 0.263671875 [0.224609375, 0.30078125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.9765625 | 0.72265625 [0.685546875, 0.761767578125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.9296875 | 0.607421875 [0.564453125, 0.654296875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.927734375 | 0.634765625 [0.593701171875, 0.6796875] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.921875 | 0.5625 [0.51953125, 0.60546875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.94921875 | 0.6796875 [0.638671875, 0.72265625] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.978515625 | 0.0546875 [0.029296875, 0.080078125] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.9609375 | 0.037109375 [0.013671875, 0.060546875] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.97265625 | 0.04296875 [0.01953125, 0.06450195312499996] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.982421875 | 0.048828125 [0.025390625, 0.072265625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.98828125 | 0.076171875 [0.05078125, 0.103515625] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.978515625 | 0.421875 [0.3828125, 0.46484375] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.919921875 | 0.31640625 [0.275390625, 0.357421875] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.92578125 | 0.359375 [0.318359375, 0.40625] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.919921875 | 0.298828125 [0.255859375, 0.341796875] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.943359375 | 0.298828125 [0.251953125, 0.341796875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.8984375 | 0.125 [0.0859375, 0.1640625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.94921875 | 0.1484375 [0.115185546875, 0.185546875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.921875 | 0.150390625 [0.115234375, 0.193359375] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.93359375 | 0.08984375 [0.052734375, 0.126953125] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.947265625 | 0.205078125 [0.1640625, 0.24614257812499996] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.82421875 | 0.556640625 [0.505859375, 0.609375] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.767578125 | 0.4140625 [0.361328125, 0.470703125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.78515625 | 0.4765625 [0.42578125, 0.527392578125] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.82421875 | 0.443359375 [0.398388671875, 0.494140625] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.74609375 | 0.458984375 [0.406201171875, 0.515625] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.958984375 | 0.05078125 [0.0234375, 0.076171875] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.962890625 | 0.046875 [0.01953125, 0.07421875] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.962890625 | 0.046875 [0.025390625, 0.068359375] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.97265625 | 0.03125 [0.009765625, 0.0546875] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.9609375 | 0.05859375 [0.031201171875000003, 0.087890625] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.916015625 | 0.40234375 [0.35546875, 0.451171875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.82421875 | 0.224609375 [0.177734375, 0.267578125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.8671875 | 0.291015625 [0.24609375, 0.337890625] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.90234375 | 0.26171875 [0.216796875, 0.302734375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.861328125 | 0.2265625 [0.181640625, 0.271484375] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.007330149412155151 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.007629811763763428 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.00794568657875061 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.008445203304290771 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.008334308862686157 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.008183673024177551 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.00845097005367279 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.008645027875900269 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.008827641606330872 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.007568269968032837 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.010771289467811584 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.009631484746932983 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.008054673671722412 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.010005339980125427 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.009142950177192688 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.008624613285064697 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.008824154734611511 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.00921843945980072 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.007603377103805542 | True | [0.006812825798988342, 0.007555365562438965, 0.008283600211143494, 0.008997946977615356, 0.009698748588562012, 0.010386437177658081, 0.011061310768127441, 0.011723726987838745, 0.012373998761177063] | [] | False |
| 2 | 64 | None | 0.007603377103805542 | True | [0.006861001253128052, 0.007603377103805542, 0.008331477642059326, 0.009045630693435669, 0.009746268391609192, 0.010433763265609741, 0.011108458042144775, 0.011770680546760559, 0.012420788407325745] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.006949940153087179 | 0.008377134799957275 |
| reset_L | 160 | 0.006757350917905569 | 0.008482500910758972 |
| same_category_substitution | 128 | 0.00018899573478847742 | 0.000658378005027771 |
| set_H | 160 | 0.006970700807869434 | 0.007914260029792786 |
| upper_state_exchange_same_N | 64 | 0.006912303157150745 | 0.007778763771057129 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_target_original_seed0

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.001589838035379567 | 0.0014232375348111896 | 24238 | 0.990078968197485 | False | 0.0827530175447464 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 473 | 1888 | 0.25262725353240967 |
| 1 | 24435 | 479 | 1898 | 0.2544999122619629 |
| 2 | 24435 | 450 | 1877 | 0.25427696108818054 |
| 3 | 24435 | 459 | 1919 | 0.25353723764419556 |
| saved r9 | 101 | 1 | 27 | 0.1657009869813919 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 23405/24435 | 23472/24435 | 23282/24435 | 23656/24435 | 23021/24435 | 19269/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.018735754303634167 | 0.03145463764667511 |
| L_single_round | 32 | 0.008489840663969517 | 0.01732708513736725 |
| N_run_1 | 64 | 0.009194093872793019 | 0.04923337697982788 |
| N_run_2 | 64 | 0.008572648162953556 | 0.02726764976978302 |
| N_run_3 | 64 | 0.008082676795311272 | 0.02798314392566681 |
| N_run_4 | 64 | 0.00861726829316467 | 0.043844714760780334 |
| N_run_5 | 64 | 0.007990140584297478 | 0.017293669283390045 |
| N_run_6 | 64 | 0.009353387169539928 | 0.034967586398124695 |
| N_run_7 | 64 | 0.009007572662085295 | 0.022882521152496338 |
| N_run_8 | 64 | 0.010363208246417344 | 0.06496517360210419 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.008902375625135997 | 0.06496517360210419 | False |
| short | 192 | 0.010459846506516138 | 0.04923337697982788 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0997808074951172 | 0.08463870391249656 | 0.08735795786694404 | False | 0/24435 |
| 1000 | 1.045709595680237 | 0.005646497134584934 | 0.012727675082993724 | False | 4764/24435 |
| 2000 | 1.0459566581249238 | 0.003449554496910423 | 0.007258499403138974 | False | 8744/24435 |
| 5000 | 1.040285725593567 | 0.001675738082267344 | 0.004894957824072101 | False | 14185/24435 |
| 10000 | 1.043865076303482 | 0.0011610894242767246 | 0.00234008240663044 | False | 17161/24435 |
| 15000 | 1.0399691271781921 | 0.0009113583390717395 | 0.001993640586934169 | False | 18506/24435 |
| 20000 | 1.0396279889345168 | 0.0007155912603775505 | 0.001589838035379567 | False | 19269/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | 24326 | 6326 |
| 0 | 1 | 24435 | 17969 | 24326 | 6391 |
| 0 | 2 | 24435 | 17963 | 24326 | 6400 |
| 0 | 3 | 24435 | 17989 | 24326 | 6371 |
| 1000 | 0 | 24435 | 3068 | 12609 | 9609 |
| 1000 | 1 | 24435 | 3061 | 12643 | 9663 |
| 1000 | 2 | 24435 | 3028 | 12694 | 9732 |
| 1000 | 3 | 24435 | 3042 | 12659 | 9686 |
| 2000 | 0 | 24435 | 1805 | 4689 | 2962 |
| 2000 | 1 | 24435 | 1808 | 4663 | 2946 |
| 2000 | 2 | 24435 | 1795 | 4623 | 2906 |
| 2000 | 3 | 24435 | 1797 | 4661 | 2960 |
| 5000 | 0 | 24435 | 701 | 1405 | 792 |
| 5000 | 1 | 24435 | 731 | 1460 | 802 |
| 5000 | 2 | 24435 | 704 | 1417 | 794 |
| 5000 | 3 | 24435 | 729 | 1427 | 769 |
| 10000 | 0 | 24435 | 401 | 635 | 371 |
| 10000 | 1 | 24435 | 418 | 668 | 393 |
| 10000 | 2 | 24435 | 418 | 639 | 351 |
| 10000 | 3 | 24435 | 419 | 649 | 374 |
| 15000 | 0 | 24435 | 331 | 861 | 606 |
| 15000 | 1 | 24435 | 338 | 908 | 651 |
| 15000 | 2 | 24435 | 335 | 831 | 569 |
| 15000 | 3 | 24435 | 332 | 856 | 606 |
| 20000 | 0 | 24435 | 237 | 473 | 326 |
| 20000 | 1 | 24435 | 257 | 479 | 337 |
| 20000 | 2 | 24435 | 221 | 450 | 321 |
| 20000 | 3 | 24435 | 233 | 459 | 331 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 0.986328125 | 0.220703125 [0.181640625, 0.25590820312499996] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.955078125 | 0.17578125 [0.140625, 0.21484375] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.98046875 | 0.20703125 [0.171875, 0.240234375] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.935546875 | 0.134765625 [0.1015625, 0.16997070312499996] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.966796875 | 0.169921875 [0.134765625, 0.205078125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.943359375 | 0.580078125 [0.533154296875, 0.623046875] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.9140625 | 0.58984375 [0.552685546875, 0.63671875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.921875 | 0.685546875 [0.642529296875, 0.724658203125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.9375 | 0.638671875 [0.595703125, 0.681640625] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.931640625 | 0.634765625 [0.589794921875, 0.677734375] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.9921875 | 0.083984375 [0.060546875, 0.111328125] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.970703125 | 0.052734375 [0.025390625, 0.078125] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.98828125 | 0.0625 [0.041015625, 0.0859375] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.974609375 | 0.052734375 [0.025390625, 0.076171875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.966796875 | 0.03125 [0.01171875, 0.05078125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.923828125 | 0.36328125 [0.322216796875, 0.408203125] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.896484375 | 0.333984375 [0.291015625, 0.376953125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.904296875 | 0.275390625 [0.236279296875, 0.318359375] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.9453125 | 0.3203125 [0.279248046875, 0.359375] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.927734375 | 0.369140625 [0.326171875, 0.41796875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 0.984375 | 0.19140625 [0.15625, 0.22856445312499996] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.9296875 | 0.1328125 [0.095654296875, 0.171875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.97265625 | 0.169921875 [0.130859375, 0.205078125] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.90234375 | 0.068359375 [0.027294921875000003, 0.10942382812499996] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.94921875 | 0.14453125 [0.107421875, 0.181640625] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.92578125 | 0.544921875 [0.505810546875, 0.58984375] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.71875 | 0.37890625 [0.328125, 0.43359375] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.798828125 | 0.5234375 [0.46875, 0.57421875] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.81640625 | 0.51953125 [0.46875, 0.5703125] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.80078125 | 0.4921875 [0.441357421875, 0.541015625] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.990234375 | 0.080078125 [0.0546875, 0.10546875] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.9453125 | 0.02734375 [0.001953125, 0.0546875] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.97265625 | 0.046875 [0.021484375, 0.0703125] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.96484375 | 0.03125 [0.0078125, 0.056640625] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.970703125 | 0.048828125 [0.02734375, 0.0703125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.916015625 | 0.35546875 [0.30859375, 0.40043945312499996] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.841796875 | 0.283203125 [0.238232421875, 0.328125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.845703125 | 0.244140625 [0.199169921875, 0.28911132812499996] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.880859375 | 0.298828125 [0.25390625, 0.34184570312499996] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.857421875 | 0.30859375 [0.26171875, 0.35747070312499996] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.03145463764667511 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N1 | 0.04923337697982788 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N2 | 0.02726764976978302 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N3 | 0.02798314392566681 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N4 | 0.043844714760780334 | 5 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N5 | 0.014821842312812805 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N6 | 0.034967586398124695 | 7 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N7 | 0.022882521152496338 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N8 | 0.06496517360210419 | 9 | 9 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| L_N0 | 0.01732708513736725 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.03133705258369446 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N2 | 0.020703613758087158 | 3 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N3 | 0.022145479917526245 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N4 | 0.01903323084115982 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.017293669283390045 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.014441005885601044 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.014438115060329437 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.01667557656764984 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.02706938236951828 | True | [0.006351351737976074, 0.021755889058113098, 0.015477322041988373, 0.01767510175704956, 0.018554724752902985, 0.019041046500205994, 0.019373200833797455, 0.019636079668998718, 0.01989252120256424] | [1] | False |
| 2 | 64 | 64 | 0.02706938236951828 | True | [0.003654971718788147, 0.02706938236951828, 0.01967955380678177, 0.017969876527786255, 0.01672733575105667, 0.015807747840881348, 0.015048988163471222, 0.014398328959941864, 0.013824552297592163] | [1] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.009598400521402558 | 0.0729793906211853 |
| reset_L | 160 | 0.01932039512321353 | 0.22685766220092773 |
| same_category_substitution | 128 | 0.009829222923144698 | 0.08126229792833328 |
| set_H | 160 | 0.019231754727661608 | 0.07225871086120605 |
| upper_state_exchange_same_N | 64 | 0.010199994896538556 | 0.0729793906211853 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_target_original_seed1

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.002004391312113188 | 0.0018357943851765608 | 24201 | 0.974956506994697 | False | 0.059101976454257965 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 648 | 2786 | 0.27142801880836487 |
| 1 | 24435 | 678 | 2788 | 0.2688809633255005 |
| 2 | 24435 | 639 | 2827 | 0.27095580101013184 |
| 3 | 24435 | 651 | 2794 | 0.269091434776783 |
| saved r9 | 101 | 2 | 26 | 0.23224008828401566 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24341/24435 | 23375/24435 | 23583/24435 | 23385/24435 | 23438/24435 | 20516/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.01845748769119382 | 0.04156697541475296 |
| L_single_round | 32 | 0.010756804374977946 | 0.035407379269599915 |
| N_run_1 | 64 | 0.012841215124353766 | 0.13295167684555054 |
| N_run_2 | 64 | 0.011505256639793515 | 0.04980568587779999 |
| N_run_3 | 64 | 0.01326642429921776 | 0.08777578175067902 |
| N_run_4 | 64 | 0.012618904351256788 | 0.02670435607433319 |
| N_run_5 | 64 | 0.012624903582036495 | 0.05193610489368439 |
| N_run_6 | 64 | 0.012279918300919235 | 0.02652723342180252 |
| N_run_7 | 64 | 0.01277236605528742 | 0.03638693690299988 |
| N_run_8 | 64 | 0.014090788317844272 | 0.05801810324192047 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.012942217484426996 | 0.08777578175067902 | False |
| short | 192 | 0.012984539265744388 | 0.13295167684555054 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.088587999343872 | 0.07273375444114208 | 0.06714723890445831 | False | 0/24435 |
| 1000 | 1.0439758145809173 | 0.004883669828996062 | 0.012863406445895776 | False | 3929/24435 |
| 2000 | 1.0412151288986207 | 0.002551726563833654 | 0.0063998806752358535 | False | 7269/24435 |
| 5000 | 1.0429486978054046 | 0.0013014178184675984 | 0.0036610380289375834 | False | 14322/24435 |
| 10000 | 1.0384858322143555 | 0.0011062622655299492 | 0.0023993718432080845 | False | 17938/24435 |
| 15000 | 1.040202068090439 | 0.0011336914810817689 | 0.0021520933175154964 | False | 19578/24435 |
| 20000 | 1.042305873632431 | 0.0008204592452966609 | 0.002004391312113188 | False | 20516/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | 23817 | 9230 |
| 0 | 1 | 24435 | 14906 | 23813 | 9365 |
| 0 | 2 | 24435 | 14976 | 23791 | 9290 |
| 0 | 3 | 24435 | 14881 | 23822 | 9382 |
| 1000 | 0 | 24435 | 2225 | 6186 | 4039 |
| 1000 | 1 | 24435 | 2248 | 6227 | 4068 |
| 1000 | 2 | 24435 | 2259 | 6143 | 3979 |
| 1000 | 3 | 24435 | 2231 | 6166 | 4010 |
| 2000 | 0 | 24435 | 1440 | 1397 | 353 |
| 2000 | 1 | 24435 | 1477 | 1379 | 334 |
| 2000 | 2 | 24435 | 1481 | 1405 | 354 |
| 2000 | 3 | 24435 | 1454 | 1414 | 382 |
| 5000 | 0 | 24435 | 358 | 787 | 575 |
| 5000 | 1 | 24435 | 347 | 790 | 583 |
| 5000 | 2 | 24435 | 349 | 756 | 556 |
| 5000 | 3 | 24435 | 370 | 790 | 567 |
| 10000 | 0 | 24435 | 91 | 459 | 428 |
| 10000 | 1 | 24435 | 87 | 471 | 433 |
| 10000 | 2 | 24435 | 81 | 443 | 415 |
| 10000 | 3 | 24435 | 86 | 466 | 435 |
| 15000 | 0 | 24435 | 47 | 631 | 605 |
| 15000 | 1 | 24435 | 39 | 678 | 658 |
| 15000 | 2 | 24435 | 34 | 658 | 637 |
| 15000 | 3 | 24435 | 29 | 663 | 645 |
| 20000 | 0 | 24435 | 44 | 648 | 617 |
| 20000 | 1 | 24435 | 61 | 678 | 632 |
| 20000 | 2 | 24435 | 49 | 639 | 603 |
| 20000 | 3 | 24435 | 51 | 651 | 615 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.978515625 | 0.17578125 [0.140625, 0.208984375] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.966796875 | 0.234375 [0.1953125, 0.27543945312499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.9609375 | 0.2109375 [0.171875, 0.251953125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.984375 | 0.21875 [0.181640625, 0.255859375] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.98046875 | 0.21484375 [0.17578125, 0.251953125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.994140625 | 0.685546875 [0.646484375, 0.728515625] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.916015625 | 0.65234375 [0.609375, 0.691455078125] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.93359375 | 0.6328125 [0.58984375, 0.673828125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.931640625 | 0.671875 [0.630859375, 0.712890625] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.921875 | 0.5546875 [0.50390625, 0.599658203125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.990234375 | 0.08203125 [0.060546875, 0.107421875] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.962890625 | 0.05078125 [0.025390625, 0.07421875] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.966796875 | 0.05859375 [0.033203125, 0.08203125] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.98046875 | 0.041015625 [0.01953125, 0.064453125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.9765625 | 0.05078125 [0.02734375, 0.07421875] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.98828125 | 0.380859375 [0.341748046875, 0.423828125] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.919921875 | 0.318359375 [0.275341796875, 0.36328125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.931640625 | 0.357421875 [0.3125, 0.400390625] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.935546875 | 0.3671875 [0.322265625, 0.416015625] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.923828125 | 0.2265625 [0.183544921875, 0.26953125] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 0.984375 | 0.173828125 [0.138671875, 0.20703125] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.923828125 | 0.158203125 [0.119140625, 0.19921875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.939453125 | 0.1875 [0.1484375, 0.2265625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.966796875 | 0.220703125 [0.183544921875, 0.26171875] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.943359375 | 0.15234375 [0.115234375, 0.189453125] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.958984375 | 0.61328125 [0.570263671875, 0.65625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.8125 | 0.51171875 [0.464794921875, 0.5625] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.783203125 | 0.458984375 [0.412060546875, 0.5078125] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.779296875 | 0.494140625 [0.443359375, 0.54296875] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.80078125 | 0.3984375 [0.34375, 0.453125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 0.978515625 | 0.0546875 [0.03125, 0.076171875] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.962890625 | 0.060546875 [0.033203125, 0.087890625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.962890625 | 0.04296875 [0.017578125, 0.068359375] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.984375 | 0.052734375 [0.03125, 0.076171875] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.96484375 | 0.041015625 [0.017578125, 0.068359375] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.962890625 | 0.361328125 [0.3203125, 0.404296875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.8515625 | 0.3046875 [0.255859375, 0.34965820312499996] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.845703125 | 0.283203125 [0.23828125, 0.330078125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.8515625 | 0.271484375 [0.224609375, 0.31640625] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.875 | 0.1875 [0.140625, 0.232421875] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.04156697541475296 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N1 | 0.13295167684555054 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N2 | 0.02298475056886673 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N3 | 0.022471562027931213 | 4 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N4 | 0.026546314358711243 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N5 | 0.024131692945957184 | 5 | 5 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N6 | 0.02652723342180252 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N7 | 0.02288948744535446 | 8 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N8 | 0.05743734538555145 | 9 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N0 | 0.035407379269599915 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N1 | 0.020333528518676758 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N2 | 0.04980568587779999 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N3 | 0.08777578175067902 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N4 | 0.02670435607433319 | 5 | None | NO_OBSERVED_CONSTITUENT_ERROR | RECURRENCE_ASSOCIATED_FAILURE |
| L_N5 | 0.05193610489368439 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N6 | 0.02619636058807373 | 7 | None | NO_OBSERVED_CONSTITUENT_ERROR | RECURRENCE_ASSOCIATED_FAILURE |
| L_N7 | 0.03638693690299988 | 8 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N8 | 0.05801810324192047 | 7 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.03944157809019089 | True | [0.008228540420532227, 0.03306020796298981, 0.04133428633213043, 0.038879722356796265, 0.03469476103782654, 0.03135104477405548, 0.03233584761619568, 0.033227160573005676, 0.0341239869594574] | [1, 2, 3, 4, 5, 6, 7, 8] | False |
| 2 | 64 | 64 | 0.03944157809019089 | True | [0.017193421721458435, 0.03944157809019089, 0.04634521156549454, 0.04692540317773819, 0.04482971876859665, 0.04112467169761658, 0.03659864515066147, 0.03197222948074341, 0.027858905494213104] | [1, 2, 3, 4, 5, 6, 7, 8] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.01182440590734283 | 0.03532147407531738 |
| reset_L | 160 | 0.01835728227160871 | 0.23946064710617065 |
| same_category_substitution | 128 | 0.008008571749087423 | 0.06946486979722977 |
| set_H | 160 | 0.024356012837961315 | 0.11944742500782013 |
| upper_state_exchange_same_N | 64 | 0.01171530073042959 | 0.024979323148727417 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## a_target_original_seed2

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0022981237937159233 | 0.002046076463956234 | 24245 | 0.9836141987211591 | False | 0.05525996536016464 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 815 | 4272 | 0.2549508512020111 |
| 1 | 24435 | 810 | 4234 | 0.2558114752173424 |
| 2 | 24435 | 831 | 4243 | 0.2550186216831207 |
| 3 | 24435 | 832 | 4247 | 0.25442206859588623 |
| saved r9 | 101 | 2 | 90 | 0.24521206319332123 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 24282/24435 | 23380/24435 | 23424/24435 | 23167/24435 | 22859/24435 | 19544/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.022173233330249786 | 0.03904527425765991 |
| L_single_round | 32 | 0.008027010364457965 | 0.014156430959701538 |
| N_run_1 | 64 | 0.014804017031565309 | 0.03955024480819702 |
| N_run_2 | 64 | 0.014898086083121598 | 0.027203276753425598 |
| N_run_3 | 64 | 0.01437727315351367 | 0.02539968490600586 |
| N_run_4 | 64 | 0.01496593642514199 | 0.032064229249954224 |
| N_run_5 | 64 | 0.014862516080029309 | 0.03164488077163696 |
| N_run_6 | 64 | 0.016790412249974906 | 0.026566728949546814 |
| N_run_7 | 64 | 0.016613051178865135 | 0.02776595950126648 |
| N_run_8 | 64 | 0.018263406585901976 | 0.044798895716667175 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.015978765945571165 | 0.044798895716667175 | False |
| short | 192 | 0.014934074987346927 | 0.03955024480819702 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0980093252658845 | 0.08718953408300877 | 0.08387336464419716 | False | 0/24435 |
| 1000 | 1.0456763434410095 | 0.005936840118374675 | 0.013905546359900439 | False | 3762/24435 |
| 2000 | 1.04152041554451 | 0.0025577511452138423 | 0.006695629631832974 | False | 7933/24435 |
| 5000 | 1.0425792026519776 | 0.0012190502882003784 | 0.0030356027360021872 | False | 13483/24435 |
| 10000 | 1.0390735673904419 | 0.0012968164368066936 | 0.0025781693447621194 | False | 16608/24435 |
| 15000 | 1.041784678697586 | 0.0006667078704049345 | 0.0020787642026327347 | False | 17913/24435 |
| 20000 | 1.040218568444252 | 0.0009923567993973847 | 0.0022981237937159233 | False | 19544/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | 1944 | 226 |
| 0 | 1 | 24435 | 16708 | 1944 | 196 |
| 0 | 2 | 24435 | 16621 | 1944 | 228 |
| 0 | 3 | 24435 | 16820 | 1944 | 196 |
| 1000 | 0 | 24435 | 3017 | 5786 | 2945 |
| 1000 | 1 | 24435 | 3001 | 5777 | 2933 |
| 1000 | 2 | 24435 | 3003 | 5851 | 3007 |
| 1000 | 3 | 24435 | 3042 | 5837 | 2963 |
| 2000 | 0 | 24435 | 1651 | 2108 | 807 |
| 2000 | 1 | 24435 | 1656 | 2114 | 817 |
| 2000 | 2 | 24435 | 1644 | 2136 | 825 |
| 2000 | 3 | 24435 | 1636 | 2099 | 808 |
| 5000 | 0 | 24435 | 935 | 695 | 165 |
| 5000 | 1 | 24435 | 933 | 683 | 162 |
| 5000 | 2 | 24435 | 924 | 689 | 180 |
| 5000 | 3 | 24435 | 935 | 688 | 162 |
| 10000 | 0 | 24435 | 212 | 540 | 420 |
| 10000 | 1 | 24435 | 213 | 512 | 384 |
| 10000 | 2 | 24435 | 229 | 534 | 393 |
| 10000 | 3 | 24435 | 221 | 535 | 409 |
| 15000 | 0 | 24435 | 114 | 848 | 757 |
| 15000 | 1 | 24435 | 132 | 849 | 738 |
| 15000 | 2 | 24435 | 125 | 859 | 748 |
| 15000 | 3 | 24435 | 126 | 847 | 742 |
| 20000 | 0 | 24435 | 58 | 815 | 770 |
| 20000 | 1 | 24435 | 66 | 810 | 756 |
| 20000 | 2 | 24435 | 67 | 831 | 776 |
| 20000 | 3 | 24435 | 67 | 832 | 779 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.984375 | 0.240234375 [0.203125, 0.279296875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.958984375 | 0.201171875 [0.1640625, 0.23828125] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.962890625 | 0.21484375 [0.173828125, 0.251953125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.978515625 | 0.162109375 [0.130859375, 0.197265625] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.974609375 | 0.25390625 [0.21484375, 0.291015625] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.986328125 | 0.732421875 [0.697216796875, 0.771484375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.923828125 | 0.6015625 [0.560546875, 0.644580078125] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.923828125 | 0.630859375 [0.589794921875, 0.673828125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.9140625 | 0.5546875 [0.51171875, 0.599609375] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.912109375 | 0.642578125 [0.595703125, 0.689453125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.9765625 | 0.052734375 [0.02734375, 0.078125] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.97265625 | 0.048828125 [0.025390625, 0.07231445312499996] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.96875 | 0.0390625 [0.015625, 0.0625] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.98828125 | 0.0546875 [0.03515625, 0.076171875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.990234375 | 0.078125 [0.052734375, 0.10546875] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.9921875 | 0.435546875 [0.39453125, 0.48046875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.93359375 | 0.330078125 [0.289013671875, 0.373046875] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.912109375 | 0.345703125 [0.3046875, 0.388671875] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.9296875 | 0.30859375 [0.267578125, 0.3515625] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.9296875 | 0.28515625 [0.236279296875, 0.330078125] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.984375 | 0.2109375 [0.173828125, 0.248046875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.943359375 | 0.142578125 [0.10546875, 0.17973632812499996] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.9609375 | 0.189453125 [0.154296875, 0.23046875] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.97265625 | 0.12890625 [0.095703125, 0.1640625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.912109375 | 0.169921875 [0.130859375, 0.208984375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.947265625 | 0.6796875 [0.638623046875, 0.720703125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.75390625 | 0.400390625 [0.34375, 0.458984375] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.798828125 | 0.490234375 [0.439453125, 0.541015625] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.8203125 | 0.439453125 [0.392578125, 0.486328125] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.763671875 | 0.4765625 [0.423828125, 0.525390625] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.990234375 | 0.08203125 [0.0546875, 0.107421875] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.958984375 | 0.04296875 [0.017578125, 0.0703125] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.96875 | 0.052734375 [0.029248046875000003, 0.078125] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.982421875 | 0.041015625 [0.01953125, 0.064453125] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.9765625 | 0.07421875 [0.044921875, 0.10546875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.97265625 | 0.458984375 [0.412109375, 0.50390625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.8515625 | 0.251953125 [0.206982421875, 0.294921875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.869140625 | 0.29296875 [0.248046875, 0.33984375] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.87890625 | 0.23828125 [0.1953125, 0.28325195312499996] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.859375 | 0.224609375 [0.181640625, 0.26958007812499996] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.03904527425765991 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N1 | 0.03955024480819702 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N2 | 0.025095030665397644 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N3 | 0.02539968490600586 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N4 | 0.02333463728427887 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N5 | 0.03164488077163696 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N6 | 0.026566728949546814 | 6 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N7 | 0.02776595950126648 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N8 | 0.033084094524383545 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N0 | 0.014156430959701538 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.028611361980438232 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N2 | 0.027203276753425598 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N3 | 0.02416159212589264 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N4 | 0.032064229249954224 | 4 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N5 | 0.02113451063632965 | 5 | 1 | PRECEDING | BOARD_ASSOCIATED_FAILURE |
| L_N6 | 0.02430643141269684 | 7 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N7 | 0.02565709501504898 | 7 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N8 | 0.044798895716667175 | 5 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.0952616035938263 | False | [0.00848434865474701, 0.02465902268886566, 0.03003016859292984, 0.028455644845962524, 0.02604711800813675, 0.024145402014255524, 0.0228838250041008, 0.023047253489494324, 0.024493642151355743] | [1, 2, 3, 4, 5, 6, 7, 8] | False |
| 2 | 64 | 64 | 0.0952616035938263 | False | [0.022266022861003876, 0.0952616035938263, 0.08148841559886932, 0.06048639118671417, 0.04406030476093292, 0.03485803306102753, 0.03048752248287201, 0.028527215123176575, 0.027736544609069824] | [0, 1, 2, 3, 4, 5, 6, 7, 8] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.01664715982042253 | 0.03320574760437012 |
| reset_L | 160 | 0.018911110097542407 | 0.24878539144992828 |
| same_category_substitution | 128 | 0.007861811318434775 | 0.05893535912036896 |
| set_H | 160 | 0.024607105646282434 | 0.13066786527633667 |
| upper_state_exchange_same_N | 64 | 0.01640741468872875 | 0.03320574760437012 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## cutoff_equal_seed0

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 2.575903539163763e-05 | 2.588015998324967e-05 | 23067 | None | True | 5.189329385757446e-05 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.002950727939605713 |
| 1 | 24435 | None | 0 | 0.0029558688402175903 |
| 2 | 24435 | None | 0 | 0.0029712840914726257 |
| 3 | 24435 | None | 0 | 0.002968035638332367 |
| saved r9 | 101 | None | 0 | 0.002912178635597229 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 168/24435 | 20/24435 | 1008/24435 | 4/24435 | 396/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.00284471083432436 | 0.0028920918703079224 |
| L_single_round | 32 | 0.002849073614925146 | 0.002898074686527252 |
| N_run_1 | 64 | 0.0028452477417886257 | 0.0029008015990257263 |
| N_run_2 | 64 | 0.0028466993244364858 | 0.0028849244117736816 |
| N_run_3 | 64 | 0.002854742924682796 | 0.0029153674840927124 |
| N_run_4 | 64 | 0.002858380088582635 | 0.002945244312286377 |
| N_run_5 | 64 | 0.0028643038822337985 | 0.002929382026195526 |
| N_run_6 | 64 | 0.0028688281308859587 | 0.0029176846146583557 |
| N_run_7 | 64 | 0.0028763076988980174 | 0.002935171127319336 |
| N_run_8 | 64 | 0.00287843553815037 | 0.002956882119178772 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.002866833043905596 | 0.002956882119178772 | True |
| short | 192 | 0.0028462797636166215 | 0.0029008015990257263 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0981094789505006 | 0.023292734958231448 | 0.023685100186257385 | False | 0/24435 |
| 1000 | 1.082456841468811 | 0.00024336736878467492 | 0.0005916166381380589 | True | 0/24435 |
| 2000 | 1.0820243072509765 | 0.00022685444801027189 | 0.00011426201841237873 | True | 0/24435 |
| 5000 | 1.0828974771499633 | 8.844281546544153e-05 | 5.2679180892228525e-06 | True | 0/24435 |
| 10000 | 1.0835972237586975 | 5.200295832139545e-05 | 0.00011222945141056177 | True | 0/24435 |
| 15000 | 1.0831805276870727 | 0.0002454875872922457 | 1.749882739871025e-05 | True | 0/24435 |
| 20000 | 1.0820293426513672 | 3.323864587400749e-05 | 2.575903539163763e-05 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | None | None |
| 0 | 1 | 24435 | 17969 | None | None |
| 0 | 2 | 24435 | 17963 | None | None |
| 0 | 3 | 24435 | 17989 | None | None |
| 1000 | 0 | 24435 | 18634 | None | None |
| 1000 | 1 | 24435 | 18521 | None | None |
| 1000 | 2 | 24435 | 18465 | None | None |
| 1000 | 3 | 24435 | 18542 | None | None |
| 2000 | 0 | 24435 | 19814 | None | None |
| 2000 | 1 | 24435 | 19766 | None | None |
| 2000 | 2 | 24435 | 19802 | None | None |
| 2000 | 3 | 24435 | 19797 | None | None |
| 5000 | 0 | 24435 | 20760 | None | None |
| 5000 | 1 | 24435 | 20673 | None | None |
| 5000 | 2 | 24435 | 20704 | None | None |
| 5000 | 3 | 24435 | 20756 | None | None |
| 10000 | 0 | 24435 | 20667 | None | None |
| 10000 | 1 | 24435 | 20632 | None | None |
| 10000 | 2 | 24435 | 20727 | None | None |
| 10000 | 3 | 24435 | 20684 | None | None |
| 15000 | 0 | 24435 | 23527 | None | None |
| 15000 | 1 | 24435 | 23510 | None | None |
| 15000 | 2 | 24435 | 23554 | None | None |
| 15000 | 3 | 24435 | 23498 | None | None |
| 20000 | 0 | 24435 | 22231 | None | None |
| 20000 | 1 | 24435 | 22236 | None | None |
| 20000 | 2 | 24435 | 22210 | None | None |
| 20000 | 3 | 24435 | 22212 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 0.73046875 | -0.03515625 [-0.083984375, 0.009814453124999956] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.798828125 | 0.01953125 [-0.02734375, 0.06645507812499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.806640625 | 0.033203125 [-0.009814453124999997, 0.07622070312499996] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.818359375 | 0.017578125 [-0.021484375, 0.05859375] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.939453125 | 0.142578125 [0.109375, 0.17578125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.4140625 | 0.05078125 [-0.001953125, 0.107421875] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.396484375 | 0.072265625 [0.01953125, 0.125] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.388671875 | 0.15234375 [0.097607421875, 0.20708007812499996] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.51953125 | 0.220703125 [0.169921875, 0.267578125] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.650390625 | 0.353515625 [0.296875, 0.408203125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.904296875 | -0.00390625 [-0.029345703124999997, 0.025390625] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.931640625 | 0.013671875 [-0.009765625, 0.03515625] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.953125 | 0.02734375 [0.0078125, 0.046923828124999956] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.953125 | 0.03125 [0.009765625, 0.052783203124999956] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.970703125 | 0.03515625 [0.015625, 0.0546875] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.6171875 | 0.056640625 [0.0078125, 0.109375] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.5859375 | 0.0234375 [-0.027392578124999997, 0.076171875] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.759765625 | 0.130859375 [0.0859375, 0.181640625] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.763671875 | 0.138671875 [0.09375, 0.18754882812499996] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.841796875 | 0.283203125 [0.236328125, 0.33012695312499996] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 0.72265625 | -0.0703125 [-0.115234375, -0.025390625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.794921875 | -0.001953125 [-0.046875, 0.044921875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.82421875 | 0.021484375 [-0.01953125, 0.064453125] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.826171875 | -0.0078125 [-0.046875, 0.033203125] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.919921875 | 0.115234375 [0.083984375, 0.1484375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.328125 | -0.052734375 [-0.105517578125, -0.001953125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.376953125 | 0.037109375 [-0.017578125, 0.09375] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.41015625 | 0.134765625 [0.080078125, 0.189453125] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.451171875 | 0.154296875 [0.099609375, 0.208984375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.5 | 0.19140625 [0.140576171875, 0.2421875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.90625 | -0.00390625 [-0.03125, 0.021533203124999956] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.919921875 | 0.001953125 [-0.021484375, 0.025390625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.93359375 | 0.0078125 [-0.013671875, 0.03125] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.935546875 | 0.001953125 [-0.0234375, 0.025439453124999956] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.974609375 | 0.052734375 [0.033203125, 0.07421875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.515625 | -0.044921875 [-0.091796875, 0.001953125] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.52734375 | -0.03125 [-0.08203125, 0.017578125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.677734375 | 0.076171875 [0.029296875, 0.126953125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.666015625 | 0.083984375 [0.03515625, 0.134765625] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.69921875 | 0.150390625 [0.09765625, 0.20122070312499996] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0028920918703079224 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.002888292074203491 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0028849244117736816 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0029144734144210815 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.002945244312286377 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.002929382026195526 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.0029176846146583557 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0029349476099014282 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.002956882119178772 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.002898074686527252 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.0029008015990257263 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.0028760209679603577 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.0029153674840927124 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0029063373804092407 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.002901814877986908 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.0029058605432510376 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.002935171127319336 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0029359981417655945 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0029057636857032776 | True | [0.00282365083694458, 0.002905525267124176, 0.0029194653034210205, 0.002937130630016327, 0.002959132194519043, 0.0029806196689605713, 0.0030016228556632996, 0.003022119402885437, 0.0030421391129493713] | [] | False |
| 2 | 64 | None | 0.0029057636857032776 | True | [0.0028613880276679993, 0.0029057636857032776, 0.0029209479689598083, 0.0029384344816207886, 0.002960316836833954, 0.0029816851019859314, 0.003002569079399109, 0.0030229687690734863, 0.0030428990721702576] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0028451595765848956 | 0.0029095634818077087 |
| reset_L | 160 | 0.002844509109854698 | 0.002918645739555359 |
| same_category_substitution | 128 | 3.208749694749713e-05 | 8.715689182281494e-05 |
| set_H | 160 | 0.0028576458804309367 | 0.002923138439655304 |
| upper_state_exchange_same_N | 64 | 0.002842891844920814 | 0.0028974488377571106 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## cutoff_equal_seed1

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 1.4260618111537249e-05 | 1.4263384995946688e-05 | 23105 | None | True | 0.00021539628505706787 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.002293989062309265 |
| 1 | 24435 | None | 0 | 0.0022973716259002686 |
| 2 | 24435 | None | 0 | 0.002296164631843567 |
| 3 | 24435 | None | 0 | 0.002293989062309265 |
| saved r9 | 101 | None | 0 | 0.0022938698530197144 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 304/24435 | 934/24435 | 1731/24435 | 1166/24435 | 63/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.0019236588850617409 | 0.0020828843116760254 |
| L_single_round | 32 | 0.0018449435010552406 | 0.0019910335540771484 |
| N_run_1 | 64 | 0.001919121714308858 | 0.002129167318344116 |
| N_run_2 | 64 | 0.0019555066246539354 | 0.002197578549385071 |
| N_run_3 | 64 | 0.001962826121598482 | 0.002207621932029724 |
| N_run_4 | 64 | 0.001993398880586028 | 0.0022563189268112183 |
| N_run_5 | 64 | 0.0020077715162187815 | 0.0024278610944747925 |
| N_run_6 | 64 | 0.0020478295627981424 | 0.00242750346660614 |
| N_run_7 | 64 | 0.0020942608825862408 | 0.002433463931083679 |
| N_run_8 | 64 | 0.0020410700235515833 | 0.0023588985204696655 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.002024526164556543 | 0.002433463931083679 | True |
| short | 192 | 0.001919643177340428 | 0.002197578549385071 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0901241731643676 | 0.013401637077331543 | 0.01256583943681835 | False | 0/24435 |
| 1000 | 1.0819247770309448 | 0.00026651242700609145 | 0.00011545447425259177 | True | 0/24435 |
| 2000 | 1.081440303325653 | 0.0001410573500834289 | 5.23265258841154e-05 | True | 0/24435 |
| 5000 | 1.0821896588802338 | 4.258134232259181e-05 | 6.1030586282390735e-05 | True | 0/24435 |
| 10000 | 1.0820525455474854 | 6.397946233164475e-05 | 0.0001241405918053998 | True | 0/24435 |
| 15000 | 1.0814974403381348 | 6.450315872086776e-05 | 1.4910463314763904e-05 | True | 0/24435 |
| 20000 | 1.0825850462913513 | 9.473197493207408e-05 | 1.4260618111537249e-05 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | None | None |
| 0 | 1 | 24435 | 14906 | None | None |
| 0 | 2 | 24435 | 14976 | None | None |
| 0 | 3 | 24435 | 14881 | None | None |
| 1000 | 0 | 24435 | 17326 | None | None |
| 1000 | 1 | 24435 | 17231 | None | None |
| 1000 | 2 | 24435 | 17281 | None | None |
| 1000 | 3 | 24435 | 17234 | None | None |
| 2000 | 0 | 24435 | 18244 | None | None |
| 2000 | 1 | 24435 | 18160 | None | None |
| 2000 | 2 | 24435 | 18235 | None | None |
| 2000 | 3 | 24435 | 18237 | None | None |
| 5000 | 0 | 24435 | 16432 | None | None |
| 5000 | 1 | 24435 | 16294 | None | None |
| 5000 | 2 | 24435 | 16394 | None | None |
| 5000 | 3 | 24435 | 16391 | None | None |
| 10000 | 0 | 24435 | 16101 | None | None |
| 10000 | 1 | 24435 | 15993 | None | None |
| 10000 | 2 | 24435 | 15968 | None | None |
| 10000 | 3 | 24435 | 16076 | None | None |
| 15000 | 0 | 24435 | 15817 | None | None |
| 15000 | 1 | 24435 | 15791 | None | None |
| 15000 | 2 | 24435 | 15781 | None | None |
| 15000 | 3 | 24435 | 15837 | None | None |
| 20000 | 0 | 24435 | 17628 | None | None |
| 20000 | 1 | 24435 | 17655 | None | None |
| 20000 | 2 | 24435 | 17614 | None | None |
| 20000 | 3 | 24435 | 17589 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.759765625 | -0.04296875 [-0.087890625, 0.00390625] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.884765625 | 0.15234375 [0.109375, 0.19536132812499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.83203125 | 0.08203125 [0.0390625, 0.125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.84765625 | 0.08203125 [0.041015625, 0.125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.873046875 | 0.107421875 [0.0703125, 0.14458007812499996] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.44921875 | 0.140625 [0.0859375, 0.1953125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.63671875 | 0.373046875 [0.318359375, 0.421875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.482421875 | 0.181640625 [0.126904296875, 0.234375] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.46875 | 0.208984375 [0.162109375, 0.265625] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.513671875 | 0.146484375 [0.08984375, 0.201171875] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.916015625 | 0.0078125 [-0.015673828124999997, 0.03515625] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.951171875 | 0.0390625 [0.015625, 0.060546875] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.9453125 | 0.037109375 [0.013671875, 0.060546875] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.962890625 | 0.0234375 [0.001953125, 0.046875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.95703125 | 0.03125 [0.0078125, 0.056640625] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.630859375 | 0.0234375 [-0.021533203124999997, 0.068359375] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.79296875 | 0.19140625 [0.148388671875, 0.23828125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.6796875 | 0.10546875 [0.0546875, 0.15629882812499996] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.6953125 | 0.126953125 [0.078125, 0.177734375] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.822265625 | 0.125 [0.08203125, 0.171875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 0.767578125 | -0.04296875 [-0.0859375, 0.0] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.896484375 | 0.130859375 [0.091796875, 0.171875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.83984375 | 0.087890625 [0.046875, 0.12890625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.841796875 | 0.095703125 [0.056640625, 0.140625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.869140625 | 0.078125 [0.037109375, 0.119140625] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.373046875 | 0.02734375 [-0.025390625, 0.08203125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.58984375 | 0.2890625 [0.234375, 0.34379882812499996] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.4296875 | 0.10546875 [0.048828125, 0.15825195312499996] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.40625 | 0.12109375 [0.068310546875, 0.171875] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.505859375 | 0.103515625 [0.048779296875, 0.16015625] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 0.921875 | -0.001953125 [-0.029296875, 0.021533203124999956] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.9375 | 0.03515625 [0.0078125, 0.0625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.935546875 | 0.015625 [-0.005859375, 0.035205078124999956] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.953125 | 0.021484375 [0.001953125, 0.04296875] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.94921875 | 0.025390625 [0.0, 0.05078125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.525390625 | -0.076171875 [-0.125048828125, -0.029296875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.7109375 | 0.1640625 [0.115185546875, 0.212890625] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.564453125 | 0.001953125 [-0.044921875, 0.046875] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.62890625 | 0.048828125 [0.001953125, 0.095703125] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.76171875 | 0.07421875 [0.03125, 0.119140625] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0020828843116760254 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.002129167318344116 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.002186328172683716 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0021732598543167114 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0022563189268112183 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0024278610944747925 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.00242750346660614 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0023059695959091187 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.002297237515449524 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.0019910335540771484 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.0020960569381713867 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.002197578549385071 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.002207621932029724 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0021827667951583862 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.0022208690643310547 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.002360120415687561 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.002433463931083679 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0023588985204696655 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0022512078285217285 | True | [0.0018596053123474121, 0.0020811110734939575, 0.0022307485342025757, 0.002346351742744446, 0.0024445801973342896, 0.002532854676246643, 0.00261475145816803, 0.0026920288801193237, 0.0027655959129333496] | [] | False |
| 2 | 64 | None | 0.0022512078285217285 | True | [0.00208909809589386, 0.0022512078285217285, 0.002372264862060547, 0.002472609281539917, 0.0025614649057388306, 0.002643182873725891, 0.0027199238538742065, 0.002792760729789734, 0.002862408757209778] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0019155634411921103 | 0.002201169729232788 |
| reset_L | 160 | 0.0018649675883352756 | 0.002093002200126648 |
| same_category_substitution | 128 | 0.00010287784971296787 | 0.0003021359443664551 |
| set_H | 160 | 0.002010377962142229 | 0.0022965073585510254 |
| upper_state_exchange_same_N | 64 | 0.0019086648244410753 | 0.002118736505508423 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## cutoff_equal_seed2

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0002046267858759082 | 0.00020487099886117688 | 23183 | None | True | 5.8084726333618164e-05 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.007162421941757202 |
| 1 | 24435 | None | 0 | 0.007162421941757202 |
| 2 | 24435 | None | 0 | 0.007162421941757202 |
| 3 | 24435 | None | 0 | 0.007162421941757202 |
| saved r9 | 101 | None | 0 | 0.007122397422790527 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 235/24435 | 82/24435 | 239/24435 | 215/24435 | 20/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.00704749533906579 | 0.0070722103118896484 |
| L_single_round | 32 | 0.007018717937171459 | 0.0070901960134506226 |
| N_run_1 | 64 | 0.00704062613658607 | 0.007129505276679993 |
| N_run_2 | 64 | 0.007050837390124798 | 0.007148116827011108 |
| N_run_3 | 64 | 0.007052912842482328 | 0.007188394665718079 |
| N_run_4 | 64 | 0.007062639808282256 | 0.00719664990901947 |
| N_run_5 | 64 | 0.007061469601467252 | 0.0072412192821502686 |
| N_run_6 | 64 | 0.007086648140102625 | 0.007252678275108337 |
| N_run_7 | 64 | 0.00707241939380765 | 0.007287308573722839 |
| N_run_8 | 64 | 0.007078606402501464 | 0.007264718413352966 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.007069116031440596 | 0.007287308573722839 | True |
| short | 192 | 0.007041523388276498 | 0.007148116827011108 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.100609505176544 | 0.02608873972669244 | 0.026562348597121994 | False | 0/24435 |
| 1000 | 1.081280355453491 | 0.00016319199250574456 | 9.173954415991621e-05 | True | 0/24435 |
| 2000 | 1.0833565962314606 | 9.839459777140291e-05 | 6.173298282708684e-05 | True | 0/24435 |
| 5000 | 1.0814116716384887 | 5.147704126102326e-05 | 1.286689580555651e-05 | True | 0/24435 |
| 10000 | 1.0816819894313812 | 3.210930033446857e-05 | 4.5944682057709274e-05 | True | 0/24435 |
| 15000 | 1.083450400829315 | 4.934594621204269e-05 | 2.45202045091831e-05 | True | 0/24435 |
| 20000 | 1.0834586703777314 | 0.0001440011140266506 | 0.0002046267858759082 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | None | None |
| 0 | 1 | 24435 | 16708 | None | None |
| 0 | 2 | 24435 | 16621 | None | None |
| 0 | 3 | 24435 | 16820 | None | None |
| 1000 | 0 | 24435 | 13781 | None | None |
| 1000 | 1 | 24435 | 13576 | None | None |
| 1000 | 2 | 24435 | 13659 | None | None |
| 1000 | 3 | 24435 | 13776 | None | None |
| 2000 | 0 | 24435 | 13336 | None | None |
| 2000 | 1 | 24435 | 13139 | None | None |
| 2000 | 2 | 24435 | 13227 | None | None |
| 2000 | 3 | 24435 | 13271 | None | None |
| 5000 | 0 | 24435 | 14367 | None | None |
| 5000 | 1 | 24435 | 14291 | None | None |
| 5000 | 2 | 24435 | 14177 | None | None |
| 5000 | 3 | 24435 | 14340 | None | None |
| 10000 | 0 | 24435 | 10795 | None | None |
| 10000 | 1 | 24435 | 10810 | None | None |
| 10000 | 2 | 24435 | 10671 | None | None |
| 10000 | 3 | 24435 | 10792 | None | None |
| 15000 | 0 | 24435 | 16389 | None | None |
| 15000 | 1 | 24435 | 16376 | None | None |
| 15000 | 2 | 24435 | 16364 | None | None |
| 15000 | 3 | 24435 | 16327 | None | None |
| 20000 | 0 | 24435 | 12293 | None | None |
| 20000 | 1 | 24435 | 12216 | None | None |
| 20000 | 2 | 24435 | 12201 | None | None |
| 20000 | 3 | 24435 | 12234 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.71875 | -0.025390625 [-0.062548828125, 0.01953125] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.875 | 0.1171875 [0.076171875, 0.158203125] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.833984375 | 0.0859375 [0.041015625, 0.12890625] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.8671875 | 0.05078125 [0.009716796875000003, 0.09184570312499996] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.751953125 | 0.03125 [-0.021533203124999997, 0.078125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.404296875 | 0.150390625 [0.1015625, 0.201171875] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.62890625 | 0.306640625 [0.2578125, 0.357421875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.46484375 | 0.171875 [0.12109375, 0.2265625] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.634765625 | 0.275390625 [0.2265625, 0.32426757812499996] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.47265625 | 0.203125 [0.150390625, 0.255859375] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.919921875 | -0.00390625 [-0.025390625, 0.021484375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.93359375 | 0.009765625 [-0.015625, 0.033251953124999956] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.9453125 | 0.015625 [-0.005859375, 0.037109375] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.9609375 | 0.02734375 [0.0078125, 0.044921875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.9453125 | 0.033203125 [0.01171875, 0.056689453124999956] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.619140625 | 0.0625 [0.015625, 0.1171875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.75390625 | 0.150390625 [0.103515625, 0.197265625] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.6875 | 0.12109375 [0.072265625, 0.16997070312499996] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.82421875 | 0.203125 [0.16015625, 0.25] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.802734375 | 0.158203125 [0.111328125, 0.20703125] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.716796875 | -0.056640625 [-0.1015625, -0.015576171875000044] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.861328125 | 0.060546875 [0.0234375, 0.099609375] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.83203125 | 0.060546875 [0.021484375, 0.10546875] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.87890625 | 0.03515625 [-0.00390625, 0.07421875] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.748046875 | 0.005859375 [-0.041015625, 0.0546875] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.337890625 | 0.0703125 [0.01953125, 0.119140625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.576171875 | 0.22265625 [0.16796875, 0.27934570312499996] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.357421875 | 0.048828125 [-0.0078125, 0.099609375] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.59765625 | 0.216796875 [0.1640625, 0.26953125] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.37109375 | 0.083984375 [0.029296875, 0.138671875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.93359375 | 0.025390625 [0.001953125, 0.046875] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.912109375 | -0.00390625 [-0.029296875, 0.021484375] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.93359375 | 0.017578125 [-0.00390625, 0.0390625] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.958984375 | 0.017578125 [0.0019042968750000028, 0.03515625] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.92578125 | 0.0234375 [0.0, 0.048828125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.53125 | 0.017578125 [-0.03125, 0.072265625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.68359375 | 0.083984375 [0.03515625, 0.1328125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.568359375 | -0.0078125 [-0.056689453125, 0.043017578124999956] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.736328125 | 0.095703125 [0.048828125, 0.138671875] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.708984375 | 0.07421875 [0.025390625, 0.123046875] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0070722103118896484 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.007111579179763794 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.007148116827011108 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.007188394665718079 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.00719664990901947 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0072412192821502686 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.007252678275108337 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.007287308573722839 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.007264718413352966 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.0070901960134506226 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.007129505276679993 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.007139131426811218 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.0071630775928497314 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.007193610072135925 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.007154643535614014 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.007237955927848816 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.007194578647613525 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.007234707474708557 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.007124453783035278 | True | [0.0069956183433532715, 0.007069393992424011, 0.0071382224559783936, 0.0072030723094940186, 0.007264554500579834, 0.007323145866394043, 0.00737917423248291, 0.0074329674243927, 0.007484719157218933] | [] | False |
| 2 | 64 | None | 0.007124453783035278 | True | [0.007051557302474976, 0.007124453783035278, 0.0071921199560165405, 0.007255524396896362, 0.007315501570701599, 0.00737251341342926, 0.007426992058753967, 0.007479235529899597, 0.007529452443122864] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.007048762869089842 | 0.007174327969551086 |
| reset_L | 160 | 0.007027224916964769 | 0.007193833589553833 |
| same_category_substitution | 128 | 4.0760147385299206e-05 | 0.0001526474952697754 |
| set_H | 160 | 0.007058525923639536 | 0.007158011198043823 |
| upper_state_exchange_same_N | 64 | 0.0070438680704683065 | 0.0071263909339904785 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## cutoff_original_seed0

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.00039672736774656674 | 0.00034469879969708654 | 25670 | 0.9978231246539979 | False | 0.08978728204965591 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 80 | 242 | 0.24221038073301315 |
| 1 | 24435 | 86 | 250 | 0.24185234308242798 |
| 2 | 24435 | 87 | 224 | 0.24168427288532257 |
| 3 | 24435 | 98 | 242 | 0.24313142150640488 |
| saved r9 | 101 | 1 | 6 | 0.13384301960468292 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 12/24435 | 653/24435 | 5942/24435 | 336/24435 | 1015/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.00863872212357819 | 0.04572927951812744 |
| L_single_round | 32 | 0.004764956189319491 | 0.007008224725723267 |
| N_run_1 | 64 | 0.005316895199939609 | 0.012581303715705872 |
| N_run_2 | 64 | 0.0051644748309627175 | 0.01334218680858612 |
| N_run_3 | 64 | 0.0051907075103372335 | 0.016568079590797424 |
| N_run_4 | 64 | 0.005075779743492603 | 0.01011495292186737 |
| N_run_5 | 64 | 0.0048786180559545755 | 0.0084124356508255 |
| N_run_6 | 64 | 0.005322009441442788 | 0.01063518226146698 |
| N_run_7 | 64 | 0.005278978147543967 | 0.009986087679862976 |
| N_run_8 | 64 | 0.0052481465972959995 | 0.009478449821472168 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.005165706582677861 | 0.016568079590797424 | True |
| short | 192 | 0.005727736395783722 | 0.04572927951812744 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0997870326042176 | 0.08449851863086223 | 0.08735795786694404 | False | 0/24435 |
| 1000 | 1.043487523794174 | 0.0028323842538520694 | 0.005956179706074321 | False | 0/24435 |
| 2000 | 1.0440831291675567 | 0.0019972872541984543 | 0.0026822271037563344 | False | 0/24435 |
| 5000 | 1.0393960750102997 | 0.0007939525628171396 | 0.001717417992043368 | False | 0/24435 |
| 10000 | 1.0430330431461334 | 0.0005645343979267636 | 0.0006599315177472038 | False | 0/24435 |
| 15000 | 1.0394188785552978 | 0.0003766262483986793 | 0.0009591691942388727 | False | 0/24435 |
| 20000 | 1.0392236018180847 | 0.00028693753163679505 | 0.00039672736774656674 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | 24326 | 6326 |
| 0 | 1 | 24435 | 17969 | 24326 | 6391 |
| 0 | 2 | 24435 | 17963 | 24326 | 6400 |
| 0 | 3 | 24435 | 17989 | 24326 | 6371 |
| 1000 | 0 | 24435 | 23218 | 737 | 99 |
| 1000 | 1 | 24435 | 23154 | 752 | 118 |
| 1000 | 2 | 24435 | 23214 | 723 | 85 |
| 1000 | 3 | 24435 | 23236 | 731 | 94 |
| 2000 | 0 | 24435 | 23012 | 439 | 73 |
| 2000 | 1 | 24435 | 22978 | 425 | 92 |
| 2000 | 2 | 24435 | 22984 | 418 | 83 |
| 2000 | 3 | 24435 | 23040 | 416 | 99 |
| 5000 | 0 | 24435 | 22971 | 50 | 6 |
| 5000 | 1 | 24435 | 23039 | 49 | 7 |
| 5000 | 2 | 24435 | 23022 | 48 | 6 |
| 5000 | 3 | 24435 | 23049 | 63 | 12 |
| 10000 | 0 | 24435 | 23372 | 35 | 8 |
| 10000 | 1 | 24435 | 23386 | 35 | 5 |
| 10000 | 2 | 24435 | 23365 | 34 | 6 |
| 10000 | 3 | 24435 | 23405 | 40 | 6 |
| 15000 | 0 | 24435 | 23380 | 24 | 2 |
| 15000 | 1 | 24435 | 23382 | 22 | 3 |
| 15000 | 2 | 24435 | 23385 | 18 | 1 |
| 15000 | 3 | 24435 | 23388 | 22 | 5 |
| 20000 | 0 | 24435 | 22797 | 80 | 4 |
| 20000 | 1 | 24435 | 22775 | 86 | 11 |
| 20000 | 2 | 24435 | 22803 | 87 | 1 |
| 20000 | 3 | 24435 | 22836 | 98 | 7 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 1.0 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.541015625 | -0.23828125 [-0.291015625, -0.18359375] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.595703125 | -0.177734375 [-0.228515625, -0.12890625] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.5625 | -0.23828125 [-0.287109375, -0.1875] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.630859375 | -0.166015625 [-0.21484375, -0.1171875] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.9765625 | 0.61328125 [0.568359375, 0.654296875] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.068359375 | -0.255859375 [-0.29296875, -0.208984375] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.064453125 | -0.171875 [-0.21484375, -0.12885742187500004] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.068359375 | -0.23046875 [-0.2734375, -0.18359375] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.09375 | -0.203125 [-0.250048828125, -0.158203125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 1.0 | 0.091796875 [0.068359375, 0.11723632812499996] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.904296875 | -0.013671875 [-0.037109375, 0.007861328124999956] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.923828125 | -0.001953125 [-0.017578125, 0.013671875] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.935546875 | 0.013671875 [-0.001953125, 0.029345703124999956] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.939453125 | 0.00390625 [-0.013671875, 0.021484375] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.98828125 | 0.427734375 [0.384765625, 0.46879882812499996] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.33984375 | -0.22265625 [-0.271484375, -0.171875] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.4140625 | -0.21484375 [-0.26171875, -0.169921875] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.4296875 | -0.1953125 [-0.246142578125, -0.14453125] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.443359375 | -0.115234375 [-0.166015625, -0.062451171875000044] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 1.0 | 0.20703125 [0.173828125, 0.244140625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.578125 | -0.21875 [-0.271484375, -0.162109375] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.609375 | -0.193359375 [-0.24609375, -0.14453125] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.62890625 | -0.205078125 [-0.251953125, -0.15625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.71875 | -0.0859375 [-0.12890625, -0.04296875] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.982421875 | 0.6015625 [0.560546875, 0.642626953125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.08203125 | -0.2578125 [-0.302783203125, -0.2109375] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.060546875 | -0.21484375 [-0.259814453125, -0.171875] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.06640625 | -0.23046875 [-0.27734375, -0.18359375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.087890625 | -0.220703125 [-0.265625, -0.1796875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.998046875 | 0.087890625 [0.0625, 0.11328125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.90625 | -0.01171875 [-0.03515625, 0.01171875] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.931640625 | 0.005859375 [-0.01171875, 0.0234375] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.9296875 | -0.00390625 [-0.0234375, 0.015625] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.9296875 | 0.0078125 [-0.013671875, 0.03125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.990234375 | 0.4296875 [0.38671875, 0.47265625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.337890625 | -0.220703125 [-0.26953125, -0.169921875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.416015625 | -0.185546875 [-0.234375, -0.134765625] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.40234375 | -0.1796875 [-0.230517578125, -0.130859375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.4140625 | -0.134765625 [-0.189453125, -0.08198242187500004] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.04572927951812744 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N1 | 0.012581303715705872 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.011034280061721802 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.016568079590797424 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.01011495292186737 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0084124356508255 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.01063518226146698 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.009986087679862976 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N8 | 0.009478449821472168 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.007008224725723267 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.005540087819099426 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.01334218680858612 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.005330897867679596 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0038540586829185486 | None | 1 | NO_SEQUENCE_DEVIATION | NO_DEVIATION |
| L_N5 | 0.004918776452541351 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N6 | 0.004773370921611786 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.005529925227165222 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0056752413511276245 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.011949539184570312 | True | [0.005188316106796265, 0.005707956850528717, 0.004469104111194611, 0.0033026114106178284, 0.0035414472222328186, 0.004404120147228241, 0.005158744752407074, 0.0058208853006362915, 0.006401725113391876] | [] | False |
| 2 | 64 | 64 | 0.011949539184570312 | True | [0.008185729384422302, 0.011949539184570312, 0.010050714015960693, 0.00949297845363617, 0.009465523064136505, 0.009412959218025208, 0.00973847508430481, 0.010107487440109253, 0.010493189096450806] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.005461969956134756 | 0.015080079436302185 |
| reset_L | 160 | 0.0025272467639297245 | 0.028874099254608154 |
| same_category_substitution | 128 | 0.0013198602246120572 | 0.011320069432258606 |
| set_H | 160 | 0.009483797335997224 | 0.04226572811603546 |
| upper_state_exchange_same_N | 64 | 0.0055499671725556254 | 0.015080079436302185 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## cutoff_original_seed1

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0005351497545774281 | 0.0005611990282236382 | 25613 | 0.9943184735518152 | False | 0.06417924910783768 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 60 | 395 | 0.24218400567770004 |
| 1 | 24435 | 54 | 390 | 0.24087056517601013 |
| 2 | 24435 | 56 | 376 | 0.23959754407405853 |
| 3 | 24435 | 67 | 399 | 0.24061042070388794 |
| saved r9 | 101 | 1 | 5 | 0.17574648559093475 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 88/24435 | 179/24435 | 402/24435 | 293/24435 | 463/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.011451560538262129 | 0.05161401629447937 |
| L_single_round | 32 | 0.007351699052378535 | 0.007903598248958588 |
| N_run_1 | 64 | 0.008954026270657778 | 0.019406966865062714 |
| N_run_2 | 64 | 0.008786055026575923 | 0.011426270008087158 |
| N_run_3 | 64 | 0.009378911345265806 | 0.025096088647842407 |
| N_run_4 | 64 | 0.009235984180122614 | 0.012370496988296509 |
| N_run_5 | 64 | 0.009313715738244355 | 0.015386432409286499 |
| N_run_6 | 64 | 0.009305135463364422 | 0.014090046286582947 |
| N_run_7 | 64 | 0.008790532359853387 | 0.011223435401916504 |
| N_run_8 | 64 | 0.008652305696159601 | 0.01718159019947052 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.009112764130501697 | 0.025096088647842407 | False |
| short | 192 | 0.009047237030851344 | 0.05161401629447937 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0894742166996003 | 0.07334316402673721 | 0.06714723890445831 | False | 0/24435 |
| 1000 | 1.041846021413803 | 0.0026584820065181703 | 0.004815838784952358 | False | 0/24435 |
| 2000 | 1.0398234558105468 | 0.0017006221128394827 | 0.0021381721286117083 | False | 0/24435 |
| 5000 | 1.04191277384758 | 0.0014666902944736647 | 0.0011039039114516744 | False | 0/24435 |
| 10000 | 1.037952663898468 | 0.0007364012184552848 | 0.0007989970411594918 | False | 0/24435 |
| 15000 | 1.039535448551178 | 0.0008824716956587508 | 0.0005820657952106738 | False | 0/24435 |
| 20000 | 1.0416797065734864 | 0.0005082855352884507 | 0.0005351497545774281 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | 23817 | 9230 |
| 0 | 1 | 24435 | 14906 | 23813 | 9365 |
| 0 | 2 | 24435 | 14976 | 23791 | 9290 |
| 0 | 3 | 24435 | 14881 | 23822 | 9382 |
| 1000 | 0 | 24435 | 23645 | 607 | 192 |
| 1000 | 1 | 24435 | 23643 | 643 | 200 |
| 1000 | 2 | 24435 | 23629 | 602 | 198 |
| 1000 | 3 | 24435 | 23632 | 644 | 201 |
| 2000 | 0 | 24435 | 23861 | 310 | 88 |
| 2000 | 1 | 24435 | 23871 | 329 | 93 |
| 2000 | 2 | 24435 | 23868 | 293 | 80 |
| 2000 | 3 | 24435 | 23853 | 353 | 95 |
| 5000 | 0 | 24435 | 23791 | 46 | 20 |
| 5000 | 1 | 24435 | 23796 | 46 | 20 |
| 5000 | 2 | 24435 | 23837 | 52 | 24 |
| 5000 | 3 | 24435 | 23777 | 51 | 23 |
| 10000 | 0 | 24435 | 23436 | 128 | 63 |
| 10000 | 1 | 24435 | 23510 | 150 | 81 |
| 10000 | 2 | 24435 | 23461 | 123 | 59 |
| 10000 | 3 | 24435 | 23491 | 148 | 73 |
| 15000 | 0 | 24435 | 23914 | 10 | 2 |
| 15000 | 1 | 24435 | 23923 | 8 | 1 |
| 15000 | 2 | 24435 | 23924 | 9 | 2 |
| 15000 | 3 | 24435 | 23963 | 11 | 0 |
| 20000 | 0 | 24435 | 23366 | 60 | 22 |
| 20000 | 1 | 24435 | 23390 | 54 | 15 |
| 20000 | 2 | 24435 | 23337 | 56 | 28 |
| 20000 | 3 | 24435 | 23351 | 67 | 21 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 1.0 | 0.197265625 [0.162109375, 0.232421875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.64453125 | -0.087890625 [-0.138671875, -0.037060546875000044] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.49609375 | -0.25390625 [-0.3046875, -0.203125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.630859375 | -0.134765625 [-0.1875, -0.08203125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.751953125 | -0.013671875 [-0.0625, 0.033251953124999956] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.978515625 | 0.669921875 [0.62890625, 0.712939453125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.083984375 | -0.1796875 [-0.22265625, -0.138671875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.05078125 | -0.25 [-0.29296875, -0.20703125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.076171875 | -0.18359375 [-0.224609375, -0.140625] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.103515625 | -0.263671875 [-0.314453125, -0.212890625] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 1.0 | 0.091796875 [0.0703125, 0.119140625] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.91015625 | -0.001953125 [-0.021484375, 0.015625] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.935546875 | 0.02734375 [0.0078125, 0.044970703124999956] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.93359375 | -0.005859375 [-0.01953125, 0.0078125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.92578125 | 0.0 [-0.01953125, 0.021484375] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.98046875 | 0.373046875 [0.33203125, 0.41411132812499996] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.392578125 | -0.208984375 [-0.259765625, -0.162109375] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.384765625 | -0.189453125 [-0.242236328125, -0.140625] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.412109375 | -0.15625 [-0.207080078125, -0.10546875] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.380859375 | -0.31640625 [-0.3671875, -0.263671875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 1.0 | 0.189453125 [0.154248046875, 0.224609375] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.669921875 | -0.095703125 [-0.144580078125, -0.04296875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.58203125 | -0.169921875 [-0.222705078125, -0.111328125] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.6796875 | -0.06640625 [-0.12109375, -0.011669921875000044] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.658203125 | -0.1328125 [-0.18359375, -0.083984375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.982421875 | 0.63671875 [0.595703125, 0.6796875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.09375 | -0.20703125 [-0.25390625, -0.16401367187500004] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.046875 | -0.27734375 [-0.318359375, -0.23432617187500004] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.091796875 | -0.193359375 [-0.2421875, -0.1484375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.087890625 | -0.314453125 [-0.361328125, -0.265625] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 1.0 | 0.076171875 [0.052734375, 0.09765625] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.90234375 | 0.0 [-0.02734375, 0.025390625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.9296875 | 0.009765625 [-0.009765625, 0.029296875] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.935546875 | 0.00390625 [-0.01171875, 0.021484375] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.9296875 | 0.005859375 [-0.015625, 0.02734375] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.98046875 | 0.37890625 [0.341748046875, 0.41796875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.400390625 | -0.146484375 [-0.193359375, -0.1015625] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.40625 | -0.15625 [-0.205078125, -0.11328125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.390625 | -0.189453125 [-0.240234375, -0.13666992187500004] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.396484375 | -0.291015625 [-0.337939453125, -0.240234375] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.05161401629447937 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N1 | 0.019406966865062714 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N2 | 0.010790534317493439 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.025096088647842407 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N4 | 0.010975465178489685 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.011407062411308289 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.011790409684181213 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N7 | 0.009730607271194458 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.009966231882572174 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.007903598248958588 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.00959824025630951 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.011426270008087158 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.0132284015417099 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.012370496988296509 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.015386432409286499 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.014090046286582947 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.011223435401916504 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.01718159019947052 | 8 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.016347244381904602 | True | [0.007394321262836456, 0.008548855781555176, 0.00947299599647522, 0.010862290859222412, 0.01314137876033783, 0.01655218005180359, 0.019999206066131592, 0.02364964783191681, 0.02842642366886139] | [7, 8] | True |
| 2 | 64 | 64 | 0.016347244381904602 | True | [0.014501884579658508, 0.016347229480743408, 0.015783369541168213, 0.01437772810459137, 0.013498634099960327, 0.01329747587442398, 0.013132058084011078, 0.013007692992687225, 0.012924633920192719] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.008829233469441533 | 0.014689072966575623 |
| reset_L | 160 | 0.010844753542914986 | 0.13025221228599548 |
| same_category_substitution | 128 | 0.0020194327807985246 | 0.009292379021644592 |
| set_H | 160 | 0.010192331951111555 | 0.04111267626285553 |
| upper_state_exchange_same_N | 64 | 0.008734463714063168 | 0.013451702892780304 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## cutoff_original_seed2

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0006230062270850802 | 0.0004502420427238316 | 25704 | 0.9940972421075507 | False | 0.015297308564186096 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 39 | 251 | 0.24935947358608246 |
| 1 | 24435 | 34 | 222 | 0.2497510015964508 |
| 2 | 24435 | 33 | 250 | 0.2477235645055771 |
| 3 | 24435 | 33 | 228 | 0.24502773582935333 |
| saved r9 | 101 | 3 | 8 | 0.2012481391429901 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 252/24435 | 266/24435 | 523/24435 | 1359/24435 | 25/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.01226063072681427 | 0.051641061902046204 |
| L_single_round | 32 | 0.007115864427760243 | 0.00841251015663147 |
| N_run_1 | 64 | 0.00974256219342351 | 0.033267274498939514 |
| N_run_2 | 64 | 0.009222374181263149 | 0.02019357681274414 |
| N_run_3 | 64 | 0.010272576939314604 | 0.0632152110338211 |
| N_run_4 | 64 | 0.009344287682324648 | 0.01862652599811554 |
| N_run_5 | 64 | 0.011081771808676422 | 0.09875798225402832 |
| N_run_6 | 64 | 0.009914303780533373 | 0.030017659068107605 |
| N_run_7 | 64 | 0.010225638747215271 | 0.03017614781856537 |
| N_run_8 | 64 | 0.010030989302322268 | 0.014017954468727112 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.010144928043397764 | 0.09875798225402832 | False |
| short | 192 | 0.009551061317324638 | 0.051641061902046204 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0978339660167693 | 0.08705484949052333 | 0.08387336464419716 | False | 0/24435 |
| 1000 | 1.0423351001739503 | 0.002620603189570829 | 0.005277742223368894 | False | 0/24435 |
| 2000 | 1.0404817152023316 | 0.002228339833964128 | 0.002248977105729353 | False | 0/24435 |
| 5000 | 1.0417590534687042 | 0.0007653276153723709 | 0.001472541165083759 | False | 0/24435 |
| 10000 | 1.038776091337204 | 0.001685889056243468 | 0.0009716896525547753 | False | 0/24435 |
| 15000 | 1.0412000179290772 | 0.00024858966120518746 | 0.00045320621109649933 | False | 0/24435 |
| 20000 | 1.0395915246009826 | 0.00047164014918962496 | 0.0006230062270850802 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | 1944 | 226 |
| 0 | 1 | 24435 | 16708 | 1944 | 196 |
| 0 | 2 | 24435 | 16621 | 1944 | 228 |
| 0 | 3 | 24435 | 16820 | 1944 | 196 |
| 1000 | 0 | 24435 | 21255 | 265 | 46 |
| 1000 | 1 | 24435 | 21270 | 259 | 47 |
| 1000 | 2 | 24435 | 21238 | 247 | 44 |
| 1000 | 3 | 24435 | 21255 | 283 | 54 |
| 2000 | 0 | 24435 | 20946 | 311 | 70 |
| 2000 | 1 | 24435 | 20864 | 313 | 96 |
| 2000 | 2 | 24435 | 20890 | 281 | 74 |
| 2000 | 3 | 24435 | 20989 | 323 | 89 |
| 5000 | 0 | 24435 | 20996 | 49 | 20 |
| 5000 | 1 | 24435 | 20960 | 56 | 22 |
| 5000 | 2 | 24435 | 21022 | 49 | 11 |
| 5000 | 3 | 24435 | 21036 | 60 | 22 |
| 10000 | 0 | 24435 | 18930 | 54 | 33 |
| 10000 | 1 | 24435 | 18985 | 63 | 40 |
| 10000 | 2 | 24435 | 19079 | 61 | 43 |
| 10000 | 3 | 24435 | 18991 | 62 | 36 |
| 15000 | 0 | 24435 | 18378 | 35 | 28 |
| 15000 | 1 | 24435 | 18427 | 29 | 22 |
| 15000 | 2 | 24435 | 18483 | 26 | 21 |
| 15000 | 3 | 24435 | 18423 | 41 | 34 |
| 20000 | 0 | 24435 | 18495 | 39 | 25 |
| 20000 | 1 | 24435 | 18554 | 34 | 19 |
| 20000 | 2 | 24435 | 18623 | 33 | 19 |
| 20000 | 3 | 24435 | 18576 | 33 | 23 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.998046875 | 0.25390625 [0.216796875, 0.291015625] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.546875 | -0.2109375 [-0.263671875, -0.162109375] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.736328125 | -0.01171875 [-0.060546875, 0.033203125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.65625 | -0.16015625 [-0.2109375, -0.107421875] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.744140625 | 0.0234375 [-0.02734375, 0.072265625] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.966796875 | 0.712890625 [0.67578125, 0.751953125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.083984375 | -0.23828125 [-0.283251953125, -0.19331054687500004] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.16796875 | -0.125 [-0.171875, -0.080078125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.10546875 | -0.25390625 [-0.302734375, -0.201171875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.134765625 | -0.134765625 [-0.181640625, -0.08984375] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.998046875 | 0.07421875 [0.05078125, 0.09770507812499996] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.91015625 | -0.013671875 [-0.03515625, 0.0078125] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.93359375 | 0.00390625 [-0.015625, 0.021484375] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.93359375 | 0.0 [-0.015625, 0.015625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.935546875 | 0.0234375 [0.001953125, 0.044921875] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.98046875 | 0.423828125 [0.386669921875, 0.466796875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.41015625 | -0.193359375 [-0.244189453125, -0.14453125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.40234375 | -0.1640625 [-0.2109375, -0.111328125] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.453125 | -0.16796875 [-0.220703125, -0.11328125] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.490234375 | -0.154296875 [-0.208984375, -0.10541992187500004] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.998046875 | 0.224609375 [0.1875, 0.26171875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.671875 | -0.12890625 [-0.177734375, -0.08203125] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.75390625 | -0.017578125 [-0.064501953125, 0.03515625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.7109375 | -0.1328125 [-0.1796875, -0.08198242187500004] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.7421875 | 0.0 [-0.046923828125, 0.048828125] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.9765625 | 0.708984375 [0.669873046875, 0.748095703125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.087890625 | -0.265625 [-0.314501953125, -0.21875] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.140625 | -0.16796875 [-0.214892578125, -0.123046875] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.095703125 | -0.28515625 [-0.33203125, -0.23828125] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.107421875 | -0.1796875 [-0.2265625, -0.1328125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.998046875 | 0.08984375 [0.064453125, 0.115234375] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.916015625 | 0.0 [-0.0234375, 0.021484375] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.935546875 | 0.01953125 [0.0, 0.0390625] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.935546875 | -0.005859375 [-0.0234375, 0.01171875] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.908203125 | 0.005859375 [-0.0234375, 0.037109375] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.984375 | 0.470703125 [0.42578125, 0.515625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.4140625 | -0.185546875 [-0.234375, -0.138671875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.43359375 | -0.142578125 [-0.193359375, -0.091796875] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.404296875 | -0.236328125 [-0.2890625, -0.18359375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.431640625 | -0.203125 [-0.255859375, -0.1541992187500001] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.051641061902046204 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N1 | 0.033267274498939514 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N2 | 0.02019357681274414 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N3 | 0.0632152110338211 | 4 | 4 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N4 | 0.01862652599811554 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N5 | 0.09875798225402832 | 3 | 3 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N6 | 0.030017659068107605 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N7 | 0.03017614781856537 | 7 | 7 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N8 | 0.014017954468727112 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.00841251015663147 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.01057734340429306 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.011174522340297699 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.015160292387008667 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.012759946286678314 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.015433169901371002 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.012304797768592834 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.012862764298915863 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.012721724808216095 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.011234097182750702 | True | [0.007095865905284882, 0.008727572858333588, 0.009453840553760529, 0.010168708860874176, 0.010874390602111816, 0.011567816138267517, 0.012375235557556152, 0.013287588953971863, 0.014188893139362335] | [] | False |
| 2 | 64 | 64 | 0.011234097182750702 | True | [0.011300995945930481, 0.011234097182750702, 0.011184580624103546, 0.011208668351173401, 0.01127665489912033, 0.011369563639163971, 0.011476375162601471, 0.011590778827667236, 0.012040853500366211] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.009457385710751018 | 0.016476526856422424 |
| reset_L | 160 | 0.0053473393432796005 | 0.045818671584129333 |
| same_category_substitution | 128 | 0.0011460603564046323 | 0.009049244225025177 |
| set_H | 160 | 0.013071327423676848 | 0.062349021434783936 |
| upper_state_exchange_same_N | 64 | 0.009500883403234184 | 0.015714868903160095 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## decoy_equal_seed0

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 2.8890752244500824e-05 | 2.8774338675001586e-05 | 23197 | None | True | 6.268173456192017e-05 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.003269083797931671 |
| 1 | 24435 | None | 0 | 0.003269083797931671 |
| 2 | 24435 | None | 0 | 0.003269083797931671 |
| 3 | 24435 | None | 0 | 0.003269083797931671 |
| saved r9 | 101 | None | 0 | 0.0031998753547668457 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 4/24435 | 1/24435 | 982/24435 | 22/24435 | 178/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.0030723828822374344 | 0.003099776804447174 |
| L_single_round | 32 | 0.0030743228271603584 | 0.0031119659543037415 |
| N_run_1 | 64 | 0.003071390208788216 | 0.003115147352218628 |
| N_run_2 | 64 | 0.003060076618567109 | 0.0031638890504837036 |
| N_run_3 | 64 | 0.0030556649435311556 | 0.0031460747122764587 |
| N_run_4 | 64 | 0.0030456578824669123 | 0.0031261146068573 |
| N_run_5 | 64 | 0.003040516749024391 | 0.003127552568912506 |
| N_run_6 | 64 | 0.0030267349211499095 | 0.0031317993998527527 |
| N_run_7 | 64 | 0.0030336625641211867 | 0.003134496510028839 |
| N_run_8 | 64 | 0.003033639513887465 | 0.00313655287027359 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.0030393127623635032 | 0.0031460747122764587 | True |
| short | 192 | 0.003068273227351407 | 0.0031638890504837036 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0981433188915253 | 0.02326986173167825 | 0.023685100186257385 | False | 0/24435 |
| 1000 | 1.0825128185749053 | 0.0002783216683201317 | 0.0006143301969076876 | True | 0/24435 |
| 2000 | 1.082012437582016 | 0.0002531489393186348 | 0.00013565093802464983 | True | 0/24435 |
| 5000 | 1.0828935348987578 | 8.418545849281145e-05 | 4.85758784215877e-06 | True | 0/24435 |
| 10000 | 1.0836002814769745 | 4.916204004075553e-05 | 0.00011737985895829631 | True | 0/24435 |
| 15000 | 1.0831867265701294 | 0.0002364059993101364 | 1.6907825550622498e-05 | True | 0/24435 |
| 20000 | 1.082031593322754 | 3.911481543809714e-05 | 2.8890752244500824e-05 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | None | None |
| 0 | 1 | 24435 | 17969 | None | None |
| 0 | 2 | 24435 | 17963 | None | None |
| 0 | 3 | 24435 | 17989 | None | None |
| 1000 | 0 | 24435 | 19007 | None | None |
| 1000 | 1 | 24435 | 18973 | None | None |
| 1000 | 2 | 24435 | 19114 | None | None |
| 1000 | 3 | 24435 | 19021 | None | None |
| 2000 | 0 | 24435 | 19505 | None | None |
| 2000 | 1 | 24435 | 19397 | None | None |
| 2000 | 2 | 24435 | 19495 | None | None |
| 2000 | 3 | 24435 | 19521 | None | None |
| 5000 | 0 | 24435 | 22894 | None | None |
| 5000 | 1 | 24435 | 22891 | None | None |
| 5000 | 2 | 24435 | 22959 | None | None |
| 5000 | 3 | 24435 | 22938 | None | None |
| 10000 | 0 | 24435 | 23327 | None | None |
| 10000 | 1 | 24435 | 23309 | None | None |
| 10000 | 2 | 24435 | 23351 | None | None |
| 10000 | 3 | 24435 | 23358 | None | None |
| 15000 | 0 | 24435 | 23942 | None | None |
| 15000 | 1 | 24435 | 23942 | None | None |
| 15000 | 2 | 24435 | 23938 | None | None |
| 15000 | 3 | 24435 | 23945 | None | None |
| 20000 | 0 | 24435 | 23839 | None | None |
| 20000 | 1 | 24435 | 23835 | None | None |
| 20000 | 2 | 24435 | 23851 | None | None |
| 20000 | 3 | 24435 | 23853 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 0.810546875 | 0.044921875 [-0.001953125, 0.091796875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.822265625 | 0.04296875 [0.005859375, 0.08203125] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.80078125 | 0.02734375 [-0.013671875, 0.0703125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.83203125 | 0.03125 [-0.009765625, 0.0703125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.87109375 | 0.07421875 [0.035107421875, 0.111328125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.443359375 | 0.080078125 [0.023388671875000003, 0.1328125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.45703125 | 0.1328125 [0.0859375, 0.18359375] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.494140625 | 0.2578125 [0.208984375, 0.30859375] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.677734375 | 0.37890625 [0.324169921875, 0.431640625] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.599609375 | 0.302734375 [0.24609375, 0.361328125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.9296875 | 0.021484375 [-0.00390625, 0.046875] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.93359375 | 0.015625 [-0.009765625, 0.0390625] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.96484375 | 0.0390625 [0.01953125, 0.05859375] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.966796875 | 0.044921875 [0.0234375, 0.06640625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.94921875 | 0.013671875 [-0.0078125, 0.033251953124999956] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.5625 | 0.001953125 [-0.048828125, 0.05078125] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.693359375 | 0.130859375 [0.080078125, 0.181640625] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.76953125 | 0.140625 [0.099609375, 0.18359375] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.84765625 | 0.22265625 [0.177734375, 0.26958007812499996] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.80078125 | 0.2421875 [0.193359375, 0.291015625] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 0.7890625 | -0.00390625 [-0.048876953125, 0.046875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.8125 | 0.015625 [-0.0234375, 0.056640625] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.814453125 | 0.01171875 [-0.033203125, 0.0546875] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.787109375 | -0.046875 [-0.091796875, 0.0] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.859375 | 0.0546875 [0.017578125, 0.091796875] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.267578125 | -0.11328125 [-0.166015625, -0.0625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.423828125 | 0.083984375 [0.03125, 0.13872070312499996] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.353515625 | 0.078125 [0.025390625, 0.12504882812499996] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.572265625 | 0.275390625 [0.216796875, 0.330078125] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.52734375 | 0.21875 [0.164013671875, 0.279296875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.912109375 | 0.001953125 [-0.0234375, 0.02734375] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.916015625 | -0.001953125 [-0.025390625, 0.021533203124999956] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.94140625 | 0.015625 [-0.00390625, 0.033203125] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.94921875 | 0.015625 [-0.001953125, 0.03515625] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.943359375 | 0.021484375 [0.0, 0.044921875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.40234375 | -0.158203125 [-0.208984375, -0.107421875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.576171875 | 0.017578125 [-0.03125, 0.0703125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.623046875 | 0.021484375 [-0.025390625, 0.0703125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.7421875 | 0.16015625 [0.109375, 0.20708007812499996] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.685546875 | 0.13671875 [0.08203125, 0.185546875] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.003099776804447174 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.003115147352218628 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0031638890504837036 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.003118455410003662 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0031153708696365356 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.003127552568912506 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.0031276121735572815 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0031303241848945618 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.0031344518065452576 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.0031119659543037415 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.003114067018032074 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.0031322911381721497 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.0031460747122764587 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0031261146068573 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.003108479082584381 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.0031317993998527527 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.003134496510028839 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.00313655287027359 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0032141506671905518 | True | [0.00317537784576416, 0.0032141506671905518, 0.0032495111227035522, 0.0032822638750076294, 0.003312930464744568, 0.0033418312668800354, 0.0033691972494125366, 0.0033952370285987854, 0.0034200772643089294] | [] | False |
| 2 | 64 | None | 0.0032141506671905518 | True | [0.003086276352405548, 0.003126703202724457, 0.0031647905707359314, 0.0032007992267608643, 0.0032348930835723877, 0.0032672137022018433, 0.00329793244600296, 0.0033271461725234985, 0.0033550038933753967] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0030709707255785665 | 0.0031413808465003967 |
| reset_L | 160 | 0.0030653250869363546 | 0.003154247999191284 |
| same_category_substitution | 128 | 2.106948522850871e-05 | 5.1081180572509766e-05 |
| set_H | 160 | 0.003070704033598304 | 0.0031393468379974365 |
| upper_state_exchange_same_N | 64 | 0.0030711418949067593 | 0.0031235292553901672 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## decoy_equal_seed1

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 1.379940892511012e-05 | 1.3908592128823175e-05 | 23214 | None | True | 0.00018766522407531738 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.002355247735977173 |
| 1 | 24435 | None | 0 | 0.0023746639490127563 |
| 2 | 24435 | None | 0 | 0.0023514479398727417 |
| 3 | 24435 | None | 0 | 0.0023617595434188843 |
| saved r9 | 101 | None | 0 | 0.0022136718034744263 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 624/24435 | 182/24435 | 1915/24435 | 706/24435 | 24/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.0020235776901245117 | 0.0021468698978424072 |
| L_single_round | 32 | 0.002099634613841772 | 0.002226725220680237 |
| N_run_1 | 64 | 0.002079504542052746 | 0.0022769421339035034 |
| N_run_2 | 64 | 0.0020557681564241648 | 0.0022483915090560913 |
| N_run_3 | 64 | 0.002050605369731784 | 0.0022158771753311157 |
| N_run_4 | 64 | 0.0020547150634229183 | 0.0022273361682891846 |
| N_run_5 | 64 | 0.0020398120395839214 | 0.002230048179626465 |
| N_run_6 | 64 | 0.0020377389155328274 | 0.002235502004623413 |
| N_run_7 | 64 | 0.002053768141195178 | 0.0022464245557785034 |
| N_run_8 | 64 | 0.002028761198744178 | 0.0022693872451782227 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.0020442334547018013 | 0.0022693872451782227 | True |
| short | 192 | 0.0020656262834866843 | 0.0022769421339035034 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0901658248901367 | 0.012829127395525575 | 0.01256583943681835 | False | 0/24435 |
| 1000 | 1.0819025123119355 | 0.00025949394610506714 | 0.0001336857671081442 | True | 0/24435 |
| 2000 | 1.081422040462494 | 0.00011896771289684693 | 6.002620173468941e-05 | True | 0/24435 |
| 5000 | 1.082174801826477 | 5.583082688644936e-05 | 7.971790844617112e-05 | True | 0/24435 |
| 10000 | 1.0820493268966676 | 6.371847271680053e-05 | 0.00012080156247987081 | True | 0/24435 |
| 15000 | 1.0814929723739624 | 6.0519391318791804e-05 | 1.93753678340793e-05 | True | 0/24435 |
| 20000 | 1.0825829434394836 | 9.75216353867836e-05 | 1.379940892511012e-05 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | None | None |
| 0 | 1 | 24435 | 14906 | None | None |
| 0 | 2 | 24435 | 14976 | None | None |
| 0 | 3 | 24435 | 14881 | None | None |
| 1000 | 0 | 24435 | 17618 | None | None |
| 1000 | 1 | 24435 | 17626 | None | None |
| 1000 | 2 | 24435 | 17632 | None | None |
| 1000 | 3 | 24435 | 17585 | None | None |
| 2000 | 0 | 24435 | 19758 | None | None |
| 2000 | 1 | 24435 | 19794 | None | None |
| 2000 | 2 | 24435 | 19855 | None | None |
| 2000 | 3 | 24435 | 19748 | None | None |
| 5000 | 0 | 24435 | 19690 | None | None |
| 5000 | 1 | 24435 | 19749 | None | None |
| 5000 | 2 | 24435 | 19739 | None | None |
| 5000 | 3 | 24435 | 19768 | None | None |
| 10000 | 0 | 24435 | 18426 | None | None |
| 10000 | 1 | 24435 | 18453 | None | None |
| 10000 | 2 | 24435 | 18455 | None | None |
| 10000 | 3 | 24435 | 18463 | None | None |
| 15000 | 0 | 24435 | 17455 | None | None |
| 15000 | 1 | 24435 | 17517 | None | None |
| 15000 | 2 | 24435 | 17460 | None | None |
| 15000 | 3 | 24435 | 17539 | None | None |
| 20000 | 0 | 24435 | 18473 | None | None |
| 20000 | 1 | 24435 | 18519 | None | None |
| 20000 | 2 | 24435 | 18462 | None | None |
| 20000 | 3 | 24435 | 18498 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.748046875 | -0.0546875 [-0.095703125, -0.021435546875000044] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.880859375 | 0.1484375 [0.107421875, 0.19536132812499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.84765625 | 0.09765625 [0.05859375, 0.13671875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.912109375 | 0.146484375 [0.10546875, 0.185546875] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.8359375 | 0.0703125 [0.027294921875000003, 0.10942382812499996] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.373046875 | 0.064453125 [0.01171875, 0.119140625] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.451171875 | 0.1875 [0.1328125, 0.23828125] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.4765625 | 0.17578125 [0.12109375, 0.2265625] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.748046875 | 0.48828125 [0.4453125, 0.537158203125] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.51171875 | 0.14453125 [0.0859375, 0.205078125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.912109375 | 0.00390625 [-0.01953125, 0.029296875] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.94921875 | 0.037109375 [0.013671875, 0.05859375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.951171875 | 0.04296875 [0.021484375, 0.06450195312499996] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.958984375 | 0.01953125 [0.0, 0.0390625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.935546875 | 0.009765625 [-0.01171875, 0.03125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.6328125 | 0.025390625 [-0.023486328124999997, 0.07421875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.671875 | 0.0703125 [0.021484375, 0.115234375] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.734375 | 0.16015625 [0.115234375, 0.203125] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.857421875 | 0.2890625 [0.244140625, 0.33598632812499996] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.765625 | 0.068359375 [0.023388671875000003, 0.1171875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 0.76953125 | -0.041015625 [-0.080078125, -0.005859375] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.865234375 | 0.099609375 [0.058544921875, 0.142578125] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.806640625 | 0.0546875 [0.013671875, 0.095703125] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.90625 | 0.16015625 [0.1171875, 0.203125] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.83203125 | 0.041015625 [0.0, 0.080078125] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.3671875 | 0.021484375 [-0.03125, 0.078125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.390625 | 0.08984375 [0.03515625, 0.14262695312499996] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.361328125 | 0.037109375 [-0.013720703124999997, 0.087890625] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.625 | 0.33984375 [0.287109375, 0.396484375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.42578125 | 0.0234375 [-0.029345703124999997, 0.08203125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 0.91796875 | -0.005859375 [-0.033203125, 0.017578125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.90234375 | 0.0 [-0.025390625, 0.025390625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.927734375 | 0.0078125 [-0.01171875, 0.02734375] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.94921875 | 0.017578125 [0.0, 0.037109375] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.93359375 | 0.009765625 [-0.01171875, 0.03125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.517578125 | -0.083984375 [-0.130859375, -0.041015625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.5390625 | -0.0078125 [-0.05859375, 0.04296875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.619140625 | 0.056640625 [0.009765625, 0.103515625] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.796875 | 0.216796875 [0.173828125, 0.259765625] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.6484375 | -0.0390625 [-0.08984375, 0.011767578124999956] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0021468698978424072 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.0022208988666534424 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0021552741527557373 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0022158771753311157 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0022273361682891846 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0022169500589370728 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.002235502004623413 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0022464245557785034 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.0022265762090682983 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.002226725220680237 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.0022769421339035034 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.0022483915090560913 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.002199918031692505 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.0021977126598358154 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.002230048179626465 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.002187967300415039 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0022407621145248413 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0022693872451782227 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0022682547569274902 | True | [0.0020440518856048584, 0.0022552162408828735, 0.0023238956928253174, 0.002357661724090576, 0.0023830533027648926, 0.002406001091003418, 0.0024278759956359863, 0.0024490654468536377, 0.00246979296207428] | [] | False |
| 2 | 64 | None | 0.0022682547569274902 | True | [0.0020302683115005493, 0.0022682547569274902, 0.0023400038480758667, 0.0023742616176605225, 0.002399921417236328, 0.0024230778217315674, 0.0024449825286865234, 0.002466052770614624, 0.002486616373062134] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.002081560203805566 | 0.002259090542793274 |
| reset_L | 160 | 0.002080056816339493 | 0.002374514937400818 |
| same_category_substitution | 128 | 8.205813355743885e-05 | 0.00015553832054138184 |
| set_H | 160 | 0.0020516909658908843 | 0.0022061318159103394 |
| upper_state_exchange_same_N | 64 | 0.0020801706705242395 | 0.002218469977378845 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## decoy_equal_seed2

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.00020884871765609655 | 0.0002098666603715628 | 23191 | None | True | 0.00033177435398101807 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.007326975464820862 |
| 1 | 24435 | None | 0 | 0.007326975464820862 |
| 2 | 24435 | None | 0 | 0.007326975464820862 |
| 3 | 24435 | None | 0 | 0.007326975464820862 |
| saved r9 | 101 | None | 0 | 0.00725710391998291 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 205/24435 | 224/24435 | 43/24435 | 114/24435 | 1/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.007123962044715881 | 0.0071886032819747925 |
| L_single_round | 32 | 0.007149151060730219 | 0.0072247982025146484 |
| N_run_1 | 64 | 0.007153198355808854 | 0.007226735353469849 |
| N_run_2 | 64 | 0.00718648754991591 | 0.007271334528923035 |
| N_run_3 | 64 | 0.007205673027783632 | 0.007284954190254211 |
| N_run_4 | 64 | 0.00721895694732666 | 0.0073098838329315186 |
| N_run_5 | 64 | 0.007238196209073067 | 0.007341727614402771 |
| N_run_6 | 64 | 0.00726752751506865 | 0.007350444793701172 |
| N_run_7 | 64 | 0.0072766023222357035 | 0.007358655333518982 |
| N_run_8 | 64 | 0.0073008290491998196 | 0.007412418723106384 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.007251297511781256 | 0.007412418723106384 | True |
| short | 192 | 0.007158747486149271 | 0.007271334528923035 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.1010004878044128 | 0.02686053104698658 | 0.026562348597121994 | False | 0/24435 |
| 1000 | 1.0812574517726898 | 0.00016110901524371 | 7.533283311854062e-05 | True | 0/24435 |
| 2000 | 1.0833534014225006 | 0.00010022875416325405 | 5.873781372798255e-05 | True | 0/24435 |
| 5000 | 1.0814197397232055 | 5.472937107697362e-05 | 4.83884679906724e-06 | True | 0/24435 |
| 10000 | 1.0816944110393525 | 3.483685524429347e-05 | 3.2150718192490615e-05 | True | 0/24435 |
| 15000 | 1.0834506738185883 | 5.055672627122476e-05 | 2.4085645780118444e-05 | True | 0/24435 |
| 20000 | 1.0834568059444427 | 0.00013705899477827187 | 0.00020884871765609655 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | None | None |
| 0 | 1 | 24435 | 16708 | None | None |
| 0 | 2 | 24435 | 16621 | None | None |
| 0 | 3 | 24435 | 16820 | None | None |
| 1000 | 0 | 24435 | 13719 | None | None |
| 1000 | 1 | 24435 | 13679 | None | None |
| 1000 | 2 | 24435 | 13595 | None | None |
| 1000 | 3 | 24435 | 13753 | None | None |
| 2000 | 0 | 24435 | 15530 | None | None |
| 2000 | 1 | 24435 | 15436 | None | None |
| 2000 | 2 | 24435 | 15407 | None | None |
| 2000 | 3 | 24435 | 15560 | None | None |
| 5000 | 0 | 24435 | 16533 | None | None |
| 5000 | 1 | 24435 | 16604 | None | None |
| 5000 | 2 | 24435 | 16500 | None | None |
| 5000 | 3 | 24435 | 16622 | None | None |
| 10000 | 0 | 24435 | 15463 | None | None |
| 10000 | 1 | 24435 | 15626 | None | None |
| 10000 | 2 | 24435 | 15639 | None | None |
| 10000 | 3 | 24435 | 15547 | None | None |
| 15000 | 0 | 24435 | 15063 | None | None |
| 15000 | 1 | 24435 | 15092 | None | None |
| 15000 | 2 | 24435 | 15086 | None | None |
| 15000 | 3 | 24435 | 14981 | None | None |
| 20000 | 0 | 24435 | 16198 | None | None |
| 20000 | 1 | 24435 | 16222 | None | None |
| 20000 | 2 | 24435 | 16249 | None | None |
| 20000 | 3 | 24435 | 16175 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.759765625 | 0.015625 [-0.02734375, 0.060546875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.90234375 | 0.14453125 [0.10546875, 0.185546875] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.890625 | 0.142578125 [0.105419921875, 0.1796875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.884765625 | 0.068359375 [0.03125, 0.107421875] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.814453125 | 0.09375 [0.048828125, 0.14067382812499996] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.375 | 0.12109375 [0.068359375, 0.173828125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.5625 | 0.240234375 [0.189404296875, 0.294921875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.5390625 | 0.24609375 [0.197265625, 0.294921875] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.517578125 | 0.158203125 [0.103515625, 0.20708007812499996] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.51171875 | 0.2421875 [0.185546875, 0.29497070312499996] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.927734375 | 0.00390625 [-0.017626953124999997, 0.02734375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.9609375 | 0.037109375 [0.015625, 0.05859375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.970703125 | 0.041015625 [0.01953125, 0.064453125] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.955078125 | 0.021484375 [0.001953125, 0.041015625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.9375 | 0.025390625 [0.00390625, 0.05078125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.662109375 | 0.10546875 [0.0546875, 0.154296875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.759765625 | 0.15625 [0.11328125, 0.203125] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.728515625 | 0.162109375 [0.119091796875, 0.212890625] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.759765625 | 0.138671875 [0.091748046875, 0.185546875] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.775390625 | 0.130859375 [0.08203125, 0.17973632812499996] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.740234375 | -0.033203125 [-0.08203125, 0.013671875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.884765625 | 0.083984375 [0.044921875, 0.12109375] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.890625 | 0.119140625 [0.083984375, 0.158203125] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.8671875 | 0.0234375 [-0.009765625, 0.05859375] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.81640625 | 0.07421875 [0.03125, 0.1171875] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.328125 | 0.060546875 [0.01171875, 0.11328125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.552734375 | 0.19921875 [0.14453125, 0.25395507812499996] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.51171875 | 0.203125 [0.15234375, 0.251953125] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.48828125 | 0.107421875 [0.056591796875, 0.158203125] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.51953125 | 0.232421875 [0.177685546875, 0.28515625] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.896484375 | -0.01171875 [-0.0390625, 0.015625] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.947265625 | 0.03125 [0.0078125, 0.056640625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.95703125 | 0.041015625 [0.021484375, 0.0625] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.94921875 | 0.0078125 [-0.011767578124999997, 0.02734375] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.9375 | 0.03515625 [0.007763671875000003, 0.06640625] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.513671875 | 0.0 [-0.046875, 0.05078125] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.708984375 | 0.109375 [0.064453125, 0.158203125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.603515625 | 0.02734375 [-0.021484375, 0.07622070312499996] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.64453125 | 0.00390625 [-0.044921875, 0.05078125] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.693359375 | 0.05859375 [0.01171875, 0.10546875] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0071886032819747925 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.007210820913314819 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.007242858409881592 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.007262036204338074 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0073098838329315186 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.007341727614402771 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.007350444793701172 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.007358655333518982 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.007412418723106384 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.0072247982025146484 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.007226735353469849 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.007271334528923035 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.007284954190254211 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.007309660315513611 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.007310092449188232 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.007346451282501221 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0073564499616622925 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.0074102431535720825 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0072541385889053345 | True | [0.007278501987457275, 0.007237613201141357, 0.007227256894111633, 0.007223367691040039, 0.007222399115562439, 0.0072389692068099976, 0.00725536048412323, 0.007279485464096069, 0.0073048025369644165] | [] | False |
| 2 | 64 | None | 0.0072541385889053345 | True | [0.007131755352020264, 0.0072541385889053345, 0.007276177406311035, 0.007279306650161743, 0.007279694080352783, 0.0072953104972839355, 0.007310450077056885, 0.007332712411880493, 0.007356598973274231] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.007162021705880761 | 0.0072498619556427 |
| reset_L | 160 | 0.007185253500938416 | 0.00729583203792572 |
| same_category_substitution | 128 | 0.00013405014760792255 | 0.00043508410453796387 |
| set_H | 160 | 0.007150744181126356 | 0.007228657603263855 |
| upper_state_exchange_same_N | 64 | 0.007154069608077407 | 0.007236167788505554 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## decoy_original_seed0

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0004423902234806756 | 0.0004231577136193119 | 25613 | 0.9956730880605786 | False | 0.028301283717155457 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 20 | 183 | 0.23962707817554474 |
| 1 | 24435 | 19 | 181 | 0.238646999001503 |
| 2 | 24435 | 23 | 166 | 0.24370773136615753 |
| 3 | 24435 | 21 | 172 | 0.24169528484344482 |
| saved r9 | 101 | 0 | 8 | 0.09880872070789337 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 22/24435 | 350/24435 | 6463/24435 | 97/24435 | 753/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.010429127141833305 | 0.019670411944389343 |
| L_single_round | 32 | 0.0073055485263466835 | 0.0100136399269104 |
| N_run_1 | 64 | 0.007005699444562197 | 0.03446929156780243 |
| N_run_2 | 64 | 0.005819291807711124 | 0.018829718232154846 |
| N_run_3 | 64 | 0.005608187057077885 | 0.012551113963127136 |
| N_run_4 | 64 | 0.005956175155006349 | 0.014562532305717468 |
| N_run_5 | 64 | 0.0056585336569696665 | 0.028196007013320923 |
| N_run_6 | 64 | 0.0047664158046245575 | 0.00913672149181366 |
| N_run_7 | 64 | 0.005290451576001942 | 0.010927662253379822 |
| N_run_8 | 64 | 0.005227206624113023 | 0.012950971722602844 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.005417828312298904 | 0.028196007013320923 | False |
| short | 192 | 0.007230776362121105 | 0.03446929156780243 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0999106407165526 | 0.08446962840855121 | 0.08735795786694404 | False | 0/24435 |
| 1000 | 1.0409842312335968 | 0.0023516584117896856 | 0.0046178373855127845 | False | 0/24435 |
| 2000 | 1.0437782144546508 | 0.0015426710608880967 | 0.0023214753812669103 | False | 0/24435 |
| 5000 | 1.0396065312623977 | 0.0011370385521877323 | 0.0020593008862869007 | False | 0/24435 |
| 10000 | 1.0430915731191635 | 0.0006842228994355537 | 0.0009605572802306641 | False | 0/24435 |
| 15000 | 1.0399892449378967 | 0.0013176045320869888 | 0.001466690271999598 | False | 0/24435 |
| 20000 | 1.0391719043254852 | 0.00031326171454566066 | 0.0004423902234806756 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | 24326 | 6326 |
| 0 | 1 | 24435 | 17969 | 24326 | 6391 |
| 0 | 2 | 24435 | 17963 | 24326 | 6400 |
| 0 | 3 | 24435 | 17989 | 24326 | 6371 |
| 1000 | 0 | 24435 | 23336 | 2788 | 368 |
| 1000 | 1 | 24435 | 23357 | 2808 | 362 |
| 1000 | 2 | 24435 | 23301 | 2808 | 373 |
| 1000 | 3 | 24435 | 23371 | 2806 | 342 |
| 2000 | 0 | 24435 | 23546 | 411 | 34 |
| 2000 | 1 | 24435 | 23540 | 435 | 41 |
| 2000 | 2 | 24435 | 23570 | 423 | 37 |
| 2000 | 3 | 24435 | 23614 | 404 | 41 |
| 5000 | 0 | 24435 | 23241 | 177 | 25 |
| 5000 | 1 | 24435 | 23255 | 169 | 24 |
| 5000 | 2 | 24435 | 23249 | 180 | 31 |
| 5000 | 3 | 24435 | 23245 | 184 | 34 |
| 10000 | 0 | 24435 | 23578 | 21 | 0 |
| 10000 | 1 | 24435 | 23584 | 16 | 1 |
| 10000 | 2 | 24435 | 23618 | 17 | 0 |
| 10000 | 3 | 24435 | 23579 | 11 | 0 |
| 15000 | 0 | 24435 | 23026 | 203 | 27 |
| 15000 | 1 | 24435 | 23030 | 227 | 26 |
| 15000 | 2 | 24435 | 22986 | 209 | 31 |
| 15000 | 3 | 24435 | 22986 | 232 | 35 |
| 20000 | 0 | 24435 | 22724 | 20 | 4 |
| 20000 | 1 | 24435 | 22697 | 19 | 6 |
| 20000 | 2 | 24435 | 22692 | 23 | 4 |
| 20000 | 3 | 24435 | 22697 | 21 | 6 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 1.0 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.62109375 | -0.158203125 [-0.212890625, -0.109375] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.5703125 | -0.203125 [-0.255859375, -0.1484375] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.685546875 | -0.115234375 [-0.1640625, -0.068359375] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.859375 | 0.0625 [0.025390625, 0.1015625] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.98828125 | 0.625 [0.58203125, 0.664111328125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.0703125 | -0.25390625 [-0.294921875, -0.208984375] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.099609375 | -0.13671875 [-0.1796875, -0.091796875] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.083984375 | -0.21484375 [-0.259814453125, -0.16796875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.17578125 | -0.12109375 [-0.169921875, -0.07416992187500004] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 1.0 | 0.091796875 [0.068359375, 0.11723632812499996] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.904296875 | -0.013671875 [-0.037109375, 0.0078125] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.9296875 | 0.00390625 [-0.009765625, 0.01953125] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.93359375 | 0.01171875 [-0.00390625, 0.029296875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.958984375 | 0.0234375 [0.00390625, 0.044921875] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.982421875 | 0.421875 [0.37890625, 0.462890625] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.373046875 | -0.189453125 [-0.240234375, -0.13671875] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.453125 | -0.17578125 [-0.2265625, -0.12495117187500004] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.41796875 | -0.20703125 [-0.26171875, -0.15424804687500004] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.43359375 | -0.125 [-0.17578125, -0.07421875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 1.0 | 0.20703125 [0.173828125, 0.244140625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.650390625 | -0.146484375 [-0.19921875, -0.091796875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.69921875 | -0.103515625 [-0.15625, -0.050732421875000044] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.720703125 | -0.11328125 [-0.158203125, -0.06640625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.8515625 | 0.046875 [0.0078125, 0.083984375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.984375 | 0.603515625 [0.5625, 0.646484375] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.091796875 | -0.248046875 [-0.294921875, -0.197265625] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.103515625 | -0.171875 [-0.218798828125, -0.125] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.087890625 | -0.208984375 [-0.25390625, -0.162109375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.119140625 | -0.189453125 [-0.234375, -0.146484375] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.998046875 | 0.087890625 [0.0625, 0.11328125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.90625 | -0.01171875 [-0.03515625, 0.01171875] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.923828125 | -0.001953125 [-0.01953125, 0.017578125] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.935546875 | 0.001953125 [-0.017578125, 0.021484375] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.94921875 | 0.02734375 [0.005859375, 0.048828125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.98828125 | 0.427734375 [0.38671875, 0.47075195312499996] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.396484375 | -0.162109375 [-0.2109375, -0.111328125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.4296875 | -0.171875 [-0.218798828125, -0.123046875] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.427734375 | -0.154296875 [-0.203125, -0.103515625] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.41796875 | -0.130859375 [-0.185546875, -0.08002929687500004] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.019670411944389343 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.03446929156780243 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N2 | 0.018829718232154846 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.012551113963127136 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.014562532305717468 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.013769209384918213 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.00913672149181366 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.010927662253379822 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.012950971722602844 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.0100136399269104 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.008303381502628326 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.008368045091629028 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.008297935128211975 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | RECURRENCE_ASSOCIATED_FAILURE |
| L_N4 | 0.01356399804353714 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.028196007013320923 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N6 | 0.006122976541519165 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0072901323437690735 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.00796404480934143 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.01923571527004242 | True | [0.005758635699748993, 0.006817720830440521, 0.007952891290187836, 0.00810115784406662, 0.008139461278915405, 0.00957779586315155, 0.011073596775531769, 0.012346401810646057, 0.01341981440782547] | [] | False |
| 2 | 64 | 64 | 0.01923571527004242 | True | [0.017113327980041504, 0.01923571527004242, 0.019700676202774048, 0.019587025046348572, 0.019281134009361267, 0.01890648901462555, 0.018502235412597656, 0.018082767724990845, 0.01765553653240204] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.006251204254416128 | 0.01610836386680603 |
| reset_L | 160 | 0.00640592286363244 | 0.12227970361709595 |
| same_category_substitution | 128 | 0.002169850456994027 | 0.007503338158130646 |
| set_H | 160 | 0.011972361430525779 | 0.05569356679916382 |
| upper_state_exchange_same_N | 64 | 0.006418531993404031 | 0.01610836386680603 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## decoy_original_seed1

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.000516116307756775 | 0.0004772477995033775 | 25634 | 0.9944251877171898 | False | 0.043580397963523865 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 99 | 510 | 0.24322021752595901 |
| 1 | 24435 | 94 | 510 | 0.24402940273284912 |
| 2 | 24435 | 100 | 508 | 0.24266202747821808 |
| 3 | 24435 | 98 | 511 | 0.2431277111172676 |
| saved r9 | 101 | 0 | 6 | 0.10814231634140015 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 131/24435 | 340/24435 | 1688/24435 | 256/24435 | 547/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.00955766998231411 | 0.0352565199136734 |
| L_single_round | 32 | 0.008717466378584504 | 0.010340258479118347 |
| N_run_1 | 64 | 0.009167426149360836 | 0.017019547522068024 |
| N_run_2 | 64 | 0.009463145164772868 | 0.01445811241865158 |
| N_run_3 | 64 | 0.009739847970195115 | 0.017930567264556885 |
| N_run_4 | 64 | 0.009668330429121852 | 0.012600310146808624 |
| N_run_5 | 64 | 0.00963830214459449 | 0.018922775983810425 |
| N_run_6 | 64 | 0.009560219943523407 | 0.013340964913368225 |
| N_run_7 | 64 | 0.0095792047213763 | 0.012895315885543823 |
| N_run_8 | 64 | 0.00988510507158935 | 0.013872489333152771 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.009678501713400086 | 0.018922775983810425 | True |
| short | 192 | 0.009256046498194337 | 0.0352565199136734 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0878647530078889 | 0.07260968677699565 | 0.06714723890445831 | False | 0/24435 |
| 1000 | 1.0403180468082427 | 0.0018908850982552394 | 0.0042608571431228546 | False | 0/24435 |
| 2000 | 1.0392063021659852 | 0.0017720112283132038 | 0.0023306179149695364 | False | 0/24435 |
| 5000 | 1.0417386174201966 | 0.0008737547197961249 | 0.0015129018351993594 | False | 0/24435 |
| 10000 | 1.037877591252327 | 0.0005768462806008757 | 0.0008410603449033959 | False | 0/24435 |
| 15000 | 1.0393367159366607 | 0.0006616076888167299 | 0.00069949584414646 | False | 0/24435 |
| 20000 | 1.041575917005539 | 0.00023306436283746735 | 0.000516116307756775 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | 23817 | 9230 |
| 0 | 1 | 24435 | 14906 | 23813 | 9365 |
| 0 | 2 | 24435 | 14976 | 23791 | 9290 |
| 0 | 3 | 24435 | 14881 | 23822 | 9382 |
| 1000 | 0 | 24435 | 21937 | 1878 | 1441 |
| 1000 | 1 | 24435 | 21958 | 1857 | 1425 |
| 1000 | 2 | 24435 | 21947 | 1840 | 1427 |
| 1000 | 3 | 24435 | 21904 | 1881 | 1477 |
| 2000 | 0 | 24435 | 22918 | 745 | 361 |
| 2000 | 1 | 24435 | 22946 | 738 | 359 |
| 2000 | 2 | 24435 | 22902 | 712 | 380 |
| 2000 | 3 | 24435 | 22929 | 725 | 354 |
| 5000 | 0 | 24435 | 23565 | 372 | 181 |
| 5000 | 1 | 24435 | 23604 | 372 | 180 |
| 5000 | 2 | 24435 | 23551 | 374 | 193 |
| 5000 | 3 | 24435 | 23578 | 380 | 192 |
| 10000 | 0 | 24435 | 23536 | 263 | 134 |
| 10000 | 1 | 24435 | 23581 | 260 | 129 |
| 10000 | 2 | 24435 | 23549 | 276 | 134 |
| 10000 | 3 | 24435 | 23575 | 257 | 127 |
| 15000 | 0 | 24435 | 23688 | 94 | 86 |
| 15000 | 1 | 24435 | 23718 | 96 | 81 |
| 15000 | 2 | 24435 | 23724 | 95 | 86 |
| 15000 | 3 | 24435 | 23717 | 97 | 83 |
| 20000 | 0 | 24435 | 23734 | 99 | 86 |
| 20000 | 1 | 24435 | 23766 | 94 | 80 |
| 20000 | 2 | 24435 | 23750 | 100 | 84 |
| 20000 | 3 | 24435 | 23755 | 98 | 84 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.998046875 | 0.1953125 [0.160107421875, 0.23046875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.6171875 | -0.115234375 [-0.16796875, -0.060546875] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.6171875 | -0.1328125 [-0.18359375, -0.078125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.72265625 | -0.04296875 [-0.091796875, 0.009765625] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.650390625 | -0.115234375 [-0.1640625, -0.068359375] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.970703125 | 0.662109375 [0.622998046875, 0.705126953125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.099609375 | -0.1640625 [-0.2109375, -0.119140625] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.060546875 | -0.240234375 [-0.28515625, -0.197265625] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.15625 | -0.103515625 [-0.146533203125, -0.0546875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.0859375 | -0.28125 [-0.328125, -0.232421875] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.998046875 | 0.08984375 [0.068359375, 0.1171875] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.90625 | -0.005859375 [-0.023486328124999997, 0.01171875] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.931640625 | 0.0234375 [0.001953125, 0.04296875] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.93359375 | -0.005859375 [-0.021484375, 0.01171875] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.94921875 | 0.0234375 [0.005859375, 0.041015625] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.98828125 | 0.380859375 [0.33984375, 0.423828125] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.419921875 | -0.181640625 [-0.234375, -0.134765625] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.42578125 | -0.1484375 [-0.19921875, -0.09765625] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.4453125 | -0.123046875 [-0.175830078125, -0.07221679687500004] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.443359375 | -0.25390625 [-0.306640625, -0.201171875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 0.998046875 | 0.1875 [0.150390625, 0.22270507812499996] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.677734375 | -0.087890625 [-0.130859375, -0.041015625] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.65234375 | -0.099609375 [-0.154296875, -0.048779296875000044] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.654296875 | -0.091796875 [-0.144580078125, -0.035107421875000044] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.673828125 | -0.1171875 [-0.1640625, -0.072265625] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.9765625 | 0.630859375 [0.591796875, 0.671875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.0859375 | -0.21484375 [-0.259814453125, -0.17377929687500004] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.099609375 | -0.224609375 [-0.267578125, -0.177734375] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.13671875 | -0.1484375 [-0.197314453125, -0.099609375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.09375 | -0.30859375 [-0.35546875, -0.2578125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 0.998046875 | 0.07421875 [0.052685546875, 0.095703125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.908203125 | 0.005859375 [-0.021484375, 0.029345703124999956] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.927734375 | 0.0078125 [-0.01171875, 0.027392578124999956] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.93359375 | 0.001953125 [-0.01171875, 0.017578125] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.9375 | 0.013671875 [-0.005859375, 0.033203125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.98046875 | 0.37890625 [0.33984375, 0.41796875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.40234375 | -0.14453125 [-0.19140625, -0.09765625] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.3984375 | -0.1640625 [-0.212890625, -0.11328125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.3828125 | -0.197265625 [-0.24609375, -0.1484375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.412109375 | -0.275390625 [-0.326171875, -0.2265625] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0352565199136734 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N1 | 0.017019547522068024 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N2 | 0.01220037043094635 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.01139833778142929 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.012600310146808624 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.011457547545433044 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.013340964913368225 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.011951468884944916 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.012397252023220062 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.010340258479118347 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.00941060483455658 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.01445811241865158 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.017930567264556885 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.012437120079994202 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.018922775983810425 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N6 | 0.011235877871513367 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.012895315885543823 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.013872489333152771 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.009188264608383179 | True | [0.008806020021438599, 0.009188279509544373, 0.00925416499376297, 0.009846732020378113, 0.011025354266166687, 0.012083858251571655, 0.013051286339759827, 0.01393747329711914, 0.014746606349945068] | [] | False |
| 2 | 64 | 64 | 0.009188264608383179 | True | [0.008218169212341309, 0.008377157151699066, 0.009400323033332825, 0.010220780968666077, 0.010859310626983643, 0.011344864964485168, 0.011705644428730011, 0.011966250836849213, 0.012147165834903717] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.009548870807824036 | 0.027319610118865967 |
| reset_L | 160 | 0.015006091073155403 | 0.2547232657670975 |
| same_category_substitution | 128 | 0.0016122442320920527 | 0.026502899825572968 |
| set_H | 160 | 0.008860708912834525 | 0.014919131994247437 |
| upper_state_exchange_same_N | 64 | 0.009485153947025537 | 0.027319610118865967 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## decoy_original_seed2

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0008024388826359392 | 0.0006983608284716699 | 25645 | 0.9924204232179206 | False | 0.020798683166503906 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 59 | 472 | 0.25008440762758255 |
| 1 | 24435 | 62 | 478 | 0.22743362188339233 |
| 2 | 24435 | 63 | 457 | 0.24396082758903503 |
| 3 | 24435 | 83 | 471 | 0.24950066208839417 |
| saved r9 | 101 | 0 | 8 | 0.08962206542491913 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 23/24435 | 61/24435 | 775/24435 | 1447/24435 | 73/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.010480702156201005 | 0.04688940942287445 |
| L_single_round | 32 | 0.005183369619771838 | 0.010566890239715576 |
| N_run_1 | 64 | 0.01040215720422566 | 0.03911878168582916 |
| N_run_2 | 64 | 0.01180889259558171 | 0.018499158322811127 |
| N_run_3 | 64 | 0.013111859443597496 | 0.02045493572950363 |
| N_run_4 | 64 | 0.013915694085881114 | 0.018928393721580505 |
| N_run_5 | 64 | 0.014110308955423534 | 0.019753284752368927 |
| N_run_6 | 64 | 0.014769521309062839 | 0.021056033670902252 |
| N_run_7 | 64 | 0.014620845089666545 | 0.0191522017121315 |
| N_run_8 | 64 | 0.01467372861225158 | 0.019368819892406464 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.014200326249313852 | 0.021056033670902252 | False |
| short | 192 | 0.010014361895931264 | 0.04688940942287445 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0985110712051391 | 0.08787287183105946 | 0.08387336464419716 | False | 0/24435 |
| 1000 | 1.0412948250770568 | 0.002385885612166021 | 0.005430022852639416 | False | 0/24435 |
| 2000 | 1.0394576716423034 | 0.001443439011927694 | 0.0023544400900846483 | False | 0/24435 |
| 5000 | 1.041641230583191 | 0.0005781275169283618 | 0.0014100170767337716 | False | 0/24435 |
| 10000 | 1.0383320701122285 | 0.0007194871918909484 | 0.0007790609424509874 | False | 0/24435 |
| 15000 | 1.0417881095409394 | 0.0012292320305277826 | 0.0038833119683249757 | False | 0/24435 |
| 20000 | 1.0396544641256333 | 0.0005656937390449457 | 0.0008024388826359392 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | 1944 | 226 |
| 0 | 1 | 24435 | 16708 | 1944 | 196 |
| 0 | 2 | 24435 | 16621 | 1944 | 228 |
| 0 | 3 | 24435 | 16820 | 1944 | 196 |
| 1000 | 0 | 24435 | 20530 | 1349 | 361 |
| 1000 | 1 | 24435 | 20535 | 1282 | 343 |
| 1000 | 2 | 24435 | 20488 | 1337 | 357 |
| 1000 | 3 | 24435 | 20467 | 1320 | 343 |
| 2000 | 0 | 24435 | 20973 | 1708 | 318 |
| 2000 | 1 | 24435 | 20995 | 1709 | 314 |
| 2000 | 2 | 24435 | 20895 | 1744 | 335 |
| 2000 | 3 | 24435 | 21001 | 1739 | 308 |
| 5000 | 0 | 24435 | 22033 | 307 | 125 |
| 5000 | 1 | 24435 | 22031 | 312 | 135 |
| 5000 | 2 | 24435 | 21985 | 290 | 115 |
| 5000 | 3 | 24435 | 22135 | 315 | 121 |
| 10000 | 0 | 24435 | 21613 | 205 | 62 |
| 10000 | 1 | 24435 | 21501 | 210 | 63 |
| 10000 | 2 | 24435 | 21539 | 197 | 59 |
| 10000 | 3 | 24435 | 21563 | 231 | 63 |
| 15000 | 0 | 24435 | 21160 | 132 | 53 |
| 15000 | 1 | 24435 | 21041 | 137 | 66 |
| 15000 | 2 | 24435 | 20973 | 128 | 45 |
| 15000 | 3 | 24435 | 21040 | 144 | 60 |
| 20000 | 0 | 24435 | 21420 | 59 | 14 |
| 20000 | 1 | 24435 | 21417 | 62 | 12 |
| 20000 | 2 | 24435 | 21349 | 63 | 18 |
| 20000 | 3 | 24435 | 21431 | 83 | 15 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.998046875 | 0.25390625 [0.216796875, 0.291015625] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.658203125 | -0.099609375 [-0.154296875, -0.046875] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.7265625 | -0.021484375 [-0.076171875, 0.029296875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.71484375 | -0.1015625 [-0.150390625, -0.056640625] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.533203125 | -0.1875 [-0.240234375, -0.134765625] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.962890625 | 0.708984375 [0.671875, 0.74609375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.08984375 | -0.232421875 [-0.277392578125, -0.18940429687500004] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.12890625 | -0.1640625 [-0.2109375, -0.11518554687500004] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.162109375 | -0.197265625 [-0.250048828125, -0.14448242187500004] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.095703125 | -0.173828125 [-0.220703125, -0.12890625] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.998046875 | 0.07421875 [0.05078125, 0.09770507812499996] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.9140625 | -0.009765625 [-0.033203125, 0.01171875] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.939453125 | 0.009765625 [-0.009765625, 0.029296875] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.923828125 | -0.009765625 [-0.029296875, 0.0078125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.923828125 | 0.01171875 [-0.009765625, 0.03515625] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.984375 | 0.427734375 [0.388671875, 0.47265625] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.427734375 | -0.17578125 [-0.232421875, -0.119140625] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.4609375 | -0.10546875 [-0.152392578125, -0.056591796875000044] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.52734375 | -0.09375 [-0.150390625, -0.03515625] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.462890625 | -0.181640625 [-0.234375, -0.12890625] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.998046875 | 0.224609375 [0.1875, 0.26171875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.669921875 | -0.130859375 [-0.1796875, -0.078125] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.69921875 | -0.072265625 [-0.123046875, -0.015625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.708984375 | -0.134765625 [-0.181640625, -0.087890625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.623046875 | -0.119140625 [-0.16796875, -0.0703125] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.96875 | 0.701171875 [0.66015625, 0.7421875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.09765625 | -0.255859375 [-0.3046875, -0.20703125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.115234375 | -0.193359375 [-0.2421875, -0.14838867187500004] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.12890625 | -0.251953125 [-0.298828125, -0.20307617187500004] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.09765625 | -0.189453125 [-0.236328125, -0.142578125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.99609375 | 0.087890625 [0.0625, 0.11328125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.908203125 | -0.0078125 [-0.033203125, 0.017578125] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.939453125 | 0.0234375 [0.0038574218750000028, 0.04296875] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.9296875 | -0.01171875 [-0.03125, 0.005908203124999956] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.927734375 | 0.025390625 [0.0, 0.048828125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.978515625 | 0.46484375 [0.419921875, 0.509765625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.400390625 | -0.19921875 [-0.25, -0.15234375] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.43359375 | -0.142578125 [-0.185595703125, -0.09375] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.423828125 | -0.216796875 [-0.271533203125, -0.16206054687500004] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.46875 | -0.166015625 [-0.212890625, -0.11713867187500004] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.04688940942287445 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N1 | 0.03911878168582916 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N2 | 0.014109961688518524 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.018900007009506226 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N4 | 0.01703900843858719 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.01638007164001465 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.01753554493188858 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.017696678638458252 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.017193026840686798 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.010566890239715576 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.019451797008514404 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.018499158322811127 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.02045493572950363 | 4 | None | NO_OBSERVED_CONSTITUENT_ERROR | RECURRENCE_ASSOCIATED_FAILURE |
| L_N4 | 0.018928393721580505 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.019753284752368927 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.021056033670902252 | 7 | None | NO_OBSERVED_CONSTITUENT_ERROR | RECURRENCE_ASSOCIATED_FAILURE |
| L_N7 | 0.0191522017121315 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.019368819892406464 | 3 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.011220559477806091 | True | [0.004339039325714111, 0.010389648377895355, 0.015210635960102081, 0.018040478229522705, 0.01994367688894272, 0.021331794559955597, 0.022436030209064484, 0.023342296481132507, 0.024135522544384003] | [5, 6, 7, 8] | True |
| 2 | 64 | 64 | 0.011220559477806091 | True | [0.007387034595012665, 0.011220559477806091, 0.013638250529766083, 0.015220776200294495, 0.016354098916053772, 0.017177961766719818, 0.017797037959098816, 0.018274791538715363, 0.0186518132686615] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.010701315671515962 | 0.025949954986572266 |
| reset_L | 160 | 0.011696814792230725 | 0.22363954782485962 |
| same_category_substitution | 128 | 0.002718507719691843 | 0.017113372683525085 |
| set_H | 160 | 0.01158827100880444 | 0.03390657901763916 |
| upper_state_exchange_same_N | 64 | 0.010035477578639984 | 0.02236005663871765 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## uniform_equal_seed0

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 2.6928639321057036e-05 | 2.6596453305912105e-05 | 20975 | None | True | 0.00017489492893218994 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.0031903088092803955 |
| 1 | 24435 | None | 0 | 0.0031952261924743652 |
| 2 | 24435 | None | 0 | 0.00318947434425354 |
| 3 | 24435 | None | 0 | 0.0031918585300445557 |
| saved r9 | 101 | None | 0 | 0.003171876072883606 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 38/24435 | 1/24435 | 1212/24435 | 183/24435 | 298/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.0029090112075209618 | 0.003006666898727417 |
| L_single_round | 32 | 0.0028640623204410076 | 0.003003515303134918 |
| N_run_1 | 64 | 0.002907475456595421 | 0.003078959882259369 |
| N_run_2 | 64 | 0.0029154429212212563 | 0.0031950175762176514 |
| N_run_3 | 64 | 0.0028862206963822246 | 0.0032832473516464233 |
| N_run_4 | 64 | 0.002937580458819866 | 0.003314785659313202 |
| N_run_5 | 64 | 0.0029404262313619256 | 0.0033636316657066345 |
| N_run_6 | 64 | 0.0029677337734028697 | 0.0033371523022651672 |
| N_run_7 | 64 | 0.0029556502122431993 | 0.0033000707626342773 |
| N_run_8 | 64 | 0.0029360316693782806 | 0.00339498370885849 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.002937273840264728 | 0.00339498370885849 | True |
| short | 192 | 0.0029031517139325538 | 0.0031950175762176514 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0980968952178956 | 0.02337919408455491 | 0.023685100186257385 | False | 0/24435 |
| 1000 | 1.08248419880867 | 0.000252321165316971 | 0.0005795369151624616 | True | 0/24435 |
| 2000 | 1.0820181572437286 | 0.0002468793238949729 | 0.00013134699808715447 | True | 0/24435 |
| 5000 | 1.0828877568244935 | 8.743967719283318e-05 | 6.101608740178203e-06 | True | 0/24435 |
| 10000 | 1.0835913574695588 | 6.658667444980892e-05 | 0.00011699335439216345 | True | 0/24435 |
| 15000 | 1.0831958377361297 | 0.00020751827892581787 | 1.773979944056215e-05 | True | 0/24435 |
| 20000 | 1.0820272839069367 | 3.326253949126112e-05 | 2.6928639321057036e-05 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | None | None |
| 0 | 1 | 24435 | 17969 | None | None |
| 0 | 2 | 24435 | 17963 | None | None |
| 0 | 3 | 24435 | 17989 | None | None |
| 1000 | 0 | 24435 | 20465 | None | None |
| 1000 | 1 | 24435 | 20379 | None | None |
| 1000 | 2 | 24435 | 20461 | None | None |
| 1000 | 3 | 24435 | 20407 | None | None |
| 2000 | 0 | 24435 | 21336 | None | None |
| 2000 | 1 | 24435 | 21258 | None | None |
| 2000 | 2 | 24435 | 21272 | None | None |
| 2000 | 3 | 24435 | 21309 | None | None |
| 5000 | 0 | 24435 | 21275 | None | None |
| 5000 | 1 | 24435 | 21184 | None | None |
| 5000 | 2 | 24435 | 21275 | None | None |
| 5000 | 3 | 24435 | 21258 | None | None |
| 10000 | 0 | 24435 | 22022 | None | None |
| 10000 | 1 | 24435 | 21898 | None | None |
| 10000 | 2 | 24435 | 21976 | None | None |
| 10000 | 3 | 24435 | 22000 | None | None |
| 15000 | 0 | 24435 | 22591 | None | None |
| 15000 | 1 | 24435 | 22505 | None | None |
| 15000 | 2 | 24435 | 22590 | None | None |
| 15000 | 3 | 24435 | 22584 | None | None |
| 20000 | 0 | 24435 | 23601 | None | None |
| 20000 | 1 | 24435 | 23575 | None | None |
| 20000 | 2 | 24435 | 23576 | None | None |
| 20000 | 3 | 24435 | 23612 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 0.7265625 | -0.0390625 [-0.08984375, 0.0078125] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.8203125 | 0.041015625 [-0.00390625, 0.08793945312499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.80859375 | 0.03515625 [-0.009765625, 0.080078125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.875 | 0.07421875 [0.037060546875, 0.11328125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.865234375 | 0.068359375 [0.03125, 0.103515625] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.337890625 | -0.025390625 [-0.080078125, 0.029296875] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.306640625 | -0.017578125 [-0.06640625, 0.037109375] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.40234375 | 0.166015625 [0.1171875, 0.220703125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.689453125 | 0.390625 [0.341796875, 0.443359375] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.576171875 | 0.279296875 [0.228515625, 0.330078125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.91796875 | 0.009765625 [-0.013671875, 0.037109375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.939453125 | 0.021484375 [-0.001953125, 0.044921875] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.93359375 | 0.0078125 [-0.013671875, 0.027392578124999956] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.962890625 | 0.041015625 [0.01953125, 0.0625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.94921875 | 0.013671875 [-0.009765625, 0.03515625] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.583984375 | 0.0234375 [-0.025390625, 0.07421875] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.68359375 | 0.12109375 [0.072265625, 0.169921875] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.708984375 | 0.080078125 [0.033203125, 0.125] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.83984375 | 0.21484375 [0.169921875, 0.259765625] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.826171875 | 0.267578125 [0.220654296875, 0.31640625] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 0.76171875 | -0.03125 [-0.076220703125, 0.015673828124999956] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.80078125 | 0.00390625 [-0.0390625, 0.048828125] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.796875 | -0.005859375 [-0.048876953125, 0.03515625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.845703125 | 0.01171875 [-0.03125, 0.056640625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.861328125 | 0.056640625 [0.01953125, 0.09375] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.33984375 | -0.041015625 [-0.095703125, 0.011767578124999956] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.28125 | -0.05859375 [-0.109423828125, -0.009716796875000044] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.326171875 | 0.05078125 [-4.8828124999997224e-05, 0.1015625] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.580078125 | 0.283203125 [0.2265625, 0.33793945312499996] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.50390625 | 0.1953125 [0.142578125, 0.248046875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.916015625 | 0.005859375 [-0.01953125, 0.03125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.908203125 | -0.009765625 [-0.033203125, 0.013671875] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.935546875 | 0.009765625 [-0.0078125, 0.02734375] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.951171875 | 0.017578125 [-0.00390625, 0.0390625] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.95703125 | 0.03515625 [0.017578125, 0.0546875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.48046875 | -0.080078125 [-0.127001953125, -0.031201171875000044] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.541015625 | -0.017578125 [-0.068359375, 0.033203125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.58984375 | -0.01171875 [-0.060595703125, 0.03515625] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.73046875 | 0.1484375 [0.103515625, 0.19140625] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.71875 | 0.169921875 [0.1171875, 0.220703125] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.003006666898727417 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.003078959882259369 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0031950175762176514 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0032832473516464233 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0032123327255249023 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0033636316657066345 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.0033371523022651672 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0033000707626342773 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.0033637061715126038 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.003003515303134918 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.003029279410839081 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.003100872039794922 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.003163769841194153 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.003314785659313202 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.003210291266441345 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.00324065238237381 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0032665878534317017 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.00339498370885849 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0031553879380226135 | True | [0.0027526766061782837, 0.0029205605387687683, 0.0030732527375221252, 0.0032127872109413147, 0.0033408626914024353, 0.0034589096903800964, 0.003568112850189209, 0.0036695674061775208, 0.003764115273952484] | [] | False |
| 2 | 64 | None | 0.0031553879380226135 | True | [0.003007657825946808, 0.0031553879380226135, 0.003290221095085144, 0.0034138262271881104, 0.003527633845806122, 0.0036328881978988647, 0.0037306100130081177, 0.003821730613708496, 0.003906950354576111] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0028826633545880518 | 0.003184206783771515 |
| reset_L | 160 | 0.002821076242253184 | 0.003182359039783478 |
| same_category_substitution | 128 | 9.012629743665457e-05 | 0.00026691704988479614 |
| set_H | 160 | 0.0029447511304169895 | 0.0031903237104415894 |
| upper_state_exchange_same_N | 64 | 0.002880169777199626 | 0.0030846595764160156 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## uniform_equal_seed1

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 1.2273623765071686e-05 | 1.2401118625256733e-05 | 21140 | None | True | 1.2665987014770508e-05 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.001937568187713623 |
| 1 | 24435 | None | 0 | 0.0019381344318389893 |
| 2 | 24435 | None | 0 | 0.0019378960132598877 |
| 3 | 24435 | None | 0 | 0.0019383430480957031 |
| saved r9 | 101 | None | 0 | 0.0019324123859405518 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 769/24435 | 215/24435 | 1841/24435 | 1697/24435 | 18/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.0019062552601099014 | 0.0019178390502929688 |
| L_single_round | 32 | 0.0019087442196905613 | 0.001921623945236206 |
| N_run_1 | 64 | 0.001914564985781908 | 0.0019333064556121826 |
| N_run_2 | 64 | 0.0019236018415540457 | 0.0019450932741165161 |
| N_run_3 | 64 | 0.0019321271684020758 | 0.001961424946784973 |
| N_run_4 | 64 | 0.0019375653937458992 | 0.0019690394401550293 |
| N_run_5 | 64 | 0.0019476963207125664 | 0.0019830167293548584 |
| N_run_6 | 64 | 0.0019499813206493855 | 0.002002626657485962 |
| N_run_7 | 64 | 0.0019556381739676 | 0.0019904226064682007 |
| N_run_8 | 64 | 0.0019627916626632214 | 0.0019911527633666992 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.001947633340023458 | 0.002002626657485962 | True |
| short | 192 | 0.0019152221890787284 | 0.0019450932741165161 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0897325658798218 | 0.012910984400659799 | 0.01256583943681835 | False | 0/24435 |
| 1000 | 1.0818768489360808 | 0.00027547657937248004 | 0.0001759863748546194 | True | 0/24435 |
| 2000 | 1.0814136958122254 | 0.00012150697927609144 | 6.0778117364513324e-05 | True | 0/24435 |
| 5000 | 1.0821698641777038 | 4.061865080075222e-05 | 7.453373382563475e-05 | True | 0/24435 |
| 10000 | 1.0820740795135497 | 8.762530378589873e-05 | 0.00012274688086679893 | True | 0/24435 |
| 15000 | 1.0814952409267427 | 6.213160798452577e-05 | 1.6638864023856218e-05 | True | 0/24435 |
| 20000 | 1.0825833475589752 | 9.458236427235533e-05 | 1.2273623765071686e-05 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | None | None |
| 0 | 1 | 24435 | 14906 | None | None |
| 0 | 2 | 24435 | 14976 | None | None |
| 0 | 3 | 24435 | 14881 | None | None |
| 1000 | 0 | 24435 | 18623 | None | None |
| 1000 | 1 | 24435 | 18582 | None | None |
| 1000 | 2 | 24435 | 18504 | None | None |
| 1000 | 3 | 24435 | 18483 | None | None |
| 2000 | 0 | 24435 | 16657 | None | None |
| 2000 | 1 | 24435 | 16576 | None | None |
| 2000 | 2 | 24435 | 16616 | None | None |
| 2000 | 3 | 24435 | 16562 | None | None |
| 5000 | 0 | 24435 | 16057 | None | None |
| 5000 | 1 | 24435 | 16119 | None | None |
| 5000 | 2 | 24435 | 16055 | None | None |
| 5000 | 3 | 24435 | 16138 | None | None |
| 10000 | 0 | 24435 | 16868 | None | None |
| 10000 | 1 | 24435 | 16836 | None | None |
| 10000 | 2 | 24435 | 16830 | None | None |
| 10000 | 3 | 24435 | 16770 | None | None |
| 15000 | 0 | 24435 | 18480 | None | None |
| 15000 | 1 | 24435 | 18554 | None | None |
| 15000 | 2 | 24435 | 18453 | None | None |
| 15000 | 3 | 24435 | 18507 | None | None |
| 20000 | 0 | 24435 | 14774 | None | None |
| 20000 | 1 | 24435 | 14716 | None | None |
| 20000 | 2 | 24435 | 14722 | None | None |
| 20000 | 3 | 24435 | 14718 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 0.708984375 | -0.09375 [-0.14453125, -0.046875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.8046875 | 0.072265625 [0.029296875, 0.119140625] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.802734375 | 0.052734375 [0.009765625, 0.095703125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.888671875 | 0.123046875 [0.080078125, 0.16796875] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.865234375 | 0.099609375 [0.064453125, 0.13671875] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.26953125 | -0.0390625 [-0.08984375, 0.013720703124999956] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.39453125 | 0.130859375 [0.078125, 0.18359375] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.572265625 | 0.271484375 [0.21484375, 0.326171875] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.501953125 | 0.2421875 [0.193310546875, 0.298828125] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.5234375 | 0.15625 [0.091796875, 0.212890625] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.91796875 | 0.009765625 [-0.015625, 0.037109375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.927734375 | 0.015625 [-0.009765625, 0.037109375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.9375 | 0.029296875 [0.0038574218750000028, 0.052734375] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.953125 | 0.013671875 [-0.0078125, 0.033203125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.953125 | 0.02734375 [0.001953125, 0.05078125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.65234375 | 0.044921875 [-0.0020019531249999972, 0.09375] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.728515625 | 0.126953125 [0.076171875, 0.177734375] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.751953125 | 0.177734375 [0.1328125, 0.224609375] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.69140625 | 0.123046875 [0.072265625, 0.171875] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.798828125 | 0.1015625 [0.056640625, 0.146484375] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 0.705078125 | -0.10546875 [-0.154296875, -0.060546875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.79296875 | 0.02734375 [-0.01171875, 0.06640625] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.810546875 | 0.05859375 [0.013671875, 0.09965820312499996] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.869140625 | 0.123046875 [0.080078125, 0.16411132812499996] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.880859375 | 0.08984375 [0.0546875, 0.125] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.25390625 | -0.091796875 [-0.14453125, -0.041015625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.40234375 | 0.1015625 [0.048779296875, 0.158203125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.53125 | 0.20703125 [0.15234375, 0.263671875] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.478515625 | 0.193359375 [0.138671875, 0.24223632812499996] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.53125 | 0.12890625 [0.068359375, 0.1875] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 0.875 | -0.048828125 [-0.083984375, -0.017578125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.927734375 | 0.025390625 [0.0, 0.05078125] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.931640625 | 0.01171875 [-0.01171875, 0.03515625] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.9453125 | 0.013671875 [-0.0078125, 0.037109375] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.955078125 | 0.03125 [0.0078125, 0.0546875] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.546875 | -0.0546875 [-0.103564453125, -0.009765625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.666015625 | 0.119140625 [0.064453125, 0.173828125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.728515625 | 0.166015625 [0.111279296875, 0.21484375] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.646484375 | 0.06640625 [0.013671875, 0.11918945312499996] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.74609375 | 0.05859375 [0.015625, 0.103515625] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.0019178390502929688 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.0019295811653137207 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.0019426792860031128 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0019613653421401978 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.0019690394401550293 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.0019830167293548584 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.0019729435443878174 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.0019759386777877808 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.0019911527633666992 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.001921623945236206 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.0019333064556121826 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.0019450932741165161 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.001961424946784973 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.001960277557373047 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.001975134015083313 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.002002626657485962 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.0019904226064682007 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.001990199089050293 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.0019284039735794067 | True | [0.0019098073244094849, 0.0019284039735794067, 0.0019463002681732178, 0.0019635558128356934, 0.0019801557064056396, 0.001996144652366638, 0.0020115822553634644, 0.002026468515396118, 0.0020408332347869873] | [] | False |
| 2 | 64 | None | 0.0019284039735794067 | True | [0.0019048452377319336, 0.0019237548112869263, 0.0019419342279434204, 0.0019594579935073853, 0.001976311206817627, 0.0019925832748413086, 0.0020082443952560425, 0.00202333927154541, 0.002037942409515381] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.0019192599381009738 | 0.0019518285989761353 |
| reset_L | 160 | 0.0019189019687473774 | 0.0019502341747283936 |
| same_category_substitution | 128 | 7.222173735499382e-06 | 2.0265579223632812e-05 |
| set_H | 160 | 0.0019154886715114117 | 0.0019521266222000122 |
| upper_state_exchange_same_N | 64 | 0.0019164762925356627 | 0.0019334405660629272 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## uniform_equal_seed2

Endpoint: PASS; first crossing: 1000

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.00020470689463761413 | 0.00020600474844567187 | 20992 | None | True | 7.75754451751709e-05 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | None | 0 | 0.0072327107191085815 |
| 1 | 24435 | None | 0 | 0.007234945893287659 |
| 2 | 24435 | None | 0 | 0.0072274357080459595 |
| 3 | 24435 | None | 0 | 0.007234752178192139 |
| saved r9 | 101 | None | 0 | 0.007210642099380493 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 303/24435 | 444/24435 | 88/24435 | 330/24435 | 5/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.007128821685910225 | 0.007153332233428955 |
| L_single_round | 32 | 0.007133696228265762 | 0.007179632782936096 |
| N_run_1 | 64 | 0.007157136453315616 | 0.007208019495010376 |
| N_run_2 | 64 | 0.007181644439697266 | 0.007227152585983276 |
| N_run_3 | 64 | 0.007200798485428095 | 0.0072517842054367065 |
| N_run_4 | 64 | 0.007229692302644253 | 0.007293105125427246 |
| N_run_5 | 64 | 0.007256315089762211 | 0.0073297470808029175 |
| N_run_6 | 64 | 0.007275740150362253 | 0.007339596748352051 |
| N_run_7 | 64 | 0.007304053753614426 | 0.007390052080154419 |
| N_run_8 | 64 | 0.007327911909669638 | 0.007417887449264526 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.007265751948580146 | 0.007417887449264526 | True |
| short | 192 | 0.007156679950033625 | 0.007227152585983276 | True |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.1007735872268676 | 0.0261952000297606 | 0.026562348597121994 | False | 0/24435 |
| 1000 | 1.0812905323505402 | 0.0001547212221339578 | 7.165094567700724e-05 | True | 0/24435 |
| 2000 | 1.0833294868469239 | 0.00010369129011451151 | 8.329416518512249e-05 | True | 0/24435 |
| 5000 | 1.081431475877762 | 5.914707634474325e-05 | 7.878120247863179e-06 | True | 0/24435 |
| 10000 | 1.0816840171813964 | 3.2523816245202397e-05 | 3.124576366725908e-05 | True | 0/24435 |
| 15000 | 1.0834487879276276 | 5.229529857274429e-05 | 2.4652603669034672e-05 | True | 0/24435 |
| 20000 | 1.0834568440914154 | 0.00013440391143376473 | 0.00020470689463761413 | True | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | None | None |
| 0 | 1 | 24435 | 16708 | None | None |
| 0 | 2 | 24435 | 16621 | None | None |
| 0 | 3 | 24435 | 16820 | None | None |
| 1000 | 0 | 24435 | 12848 | None | None |
| 1000 | 1 | 24435 | 12815 | None | None |
| 1000 | 2 | 24435 | 12790 | None | None |
| 1000 | 3 | 24435 | 12769 | None | None |
| 2000 | 0 | 24435 | 12832 | None | None |
| 2000 | 1 | 24435 | 12866 | None | None |
| 2000 | 2 | 24435 | 12920 | None | None |
| 2000 | 3 | 24435 | 12999 | None | None |
| 5000 | 0 | 24435 | 11633 | None | None |
| 5000 | 1 | 24435 | 11538 | None | None |
| 5000 | 2 | 24435 | 11529 | None | None |
| 5000 | 3 | 24435 | 11465 | None | None |
| 10000 | 0 | 24435 | 15451 | None | None |
| 10000 | 1 | 24435 | 15466 | None | None |
| 10000 | 2 | 24435 | 15487 | None | None |
| 10000 | 3 | 24435 | 15394 | None | None |
| 15000 | 0 | 24435 | 13838 | None | None |
| 15000 | 1 | 24435 | 13749 | None | None |
| 15000 | 2 | 24435 | 13748 | None | None |
| 15000 | 3 | 24435 | 13712 | None | None |
| 20000 | 0 | 24435 | 11332 | None | None |
| 20000 | 1 | 24435 | 11313 | None | None |
| 20000 | 2 | 24435 | 11346 | None | None |
| 20000 | 3 | 24435 | 11472 | None | None |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.685546875 | -0.05859375 [-0.109375, -0.01171875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.875 | 0.1171875 [0.076171875, 0.15434570312499996] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.89453125 | 0.146484375 [0.111279296875, 0.18359375] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.939453125 | 0.123046875 [0.091796875, 0.158203125] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.798828125 | 0.078125 [0.031201171875000003, 0.125] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.2578125 | 0.00390625 [-0.04296875, 0.0546875] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.533203125 | 0.2109375 [0.164013671875, 0.26171875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.623046875 | 0.330078125 [0.279296875, 0.3828125] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.6953125 | 0.3359375 [0.28515625, 0.38671875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.5390625 | 0.26953125 [0.21875, 0.3203125] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 0.90625 | -0.017578125 [-0.041015625, 0.00390625] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.951171875 | 0.02734375 [0.001953125, 0.052734375] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.955078125 | 0.025390625 [0.001953125, 0.046923828124999956] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.970703125 | 0.037109375 [0.017578125, 0.056640625] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.9375 | 0.025390625 [0.001953125, 0.05078125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.6171875 | 0.060546875 [0.01171875, 0.11328125] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.72265625 | 0.119140625 [0.072216796875, 0.16796875] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.765625 | 0.19921875 [0.154296875, 0.248046875] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.828125 | 0.20703125 [0.164013671875, 0.25] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.796875 | 0.15234375 [0.105419921875, 0.1953125] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.732421875 | -0.041015625 [-0.0859375, 0.00390625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.900390625 | 0.099609375 [0.064453125, 0.13671875] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.89453125 | 0.123046875 [0.08984375, 0.1640625] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.9453125 | 0.1015625 [0.06640625, 0.134765625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.818359375 | 0.076171875 [0.033154296875, 0.123046875] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.298828125 | 0.03125 [-0.01953125, 0.087890625] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.509765625 | 0.15625 [0.103515625, 0.212890625] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.58984375 | 0.28125 [0.232421875, 0.333984375] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.681640625 | 0.30078125 [0.248046875, 0.353515625] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.537109375 | 0.25 [0.197265625, 0.30078125] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.904296875 | -0.00390625 [-0.029296875, 0.0234375] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.95703125 | 0.041015625 [0.015625, 0.06640625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.94921875 | 0.033203125 [0.0078125, 0.056640625] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.97265625 | 0.03125 [0.01171875, 0.05078125] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.9453125 | 0.04296875 [0.015625, 0.0703125] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.50390625 | -0.009765625 [-0.05859375, 0.041015625] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.65625 | 0.056640625 [0.001953125, 0.107421875] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.7265625 | 0.150390625 [0.1015625, 0.1953125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.806640625 | 0.166015625 [0.125, 0.20903320312499996] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.712890625 | 0.078125 [0.02734375, 0.130859375] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.007153332233428955 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N1 | 0.007202088832855225 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.007227152585983276 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.0072517842054367065 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.007293105125427246 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.007310062646865845 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.007339596748352051 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.007343083620071411 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.007417887449264526 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.007179632782936096 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.007208019495010376 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.007225245237350464 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.007239148020744324 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.007283329963684082 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.0073297470808029175 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N6 | 0.007329225540161133 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.007390052080154419 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.007399916648864746 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | None | 0.007202953100204468 | True | [0.007092013955116272, 0.007202953100204468, 0.007271245121955872, 0.007331043481826782, 0.007393211126327515, 0.0074530839920043945, 0.007511347532272339, 0.007568195462226868, 0.007623776793479919] | [] | False |
| 2 | 64 | None | 0.007202953100204468 | True | [0.007120728492736816, 0.007177338004112244, 0.00722898542881012, 0.007287517189979553, 0.00734904408454895, 0.00740949809551239, 0.0074686408042907715, 0.007526487112045288, 0.007583007216453552] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.007162047860523065 | 0.007234558463096619 |
| reset_L | 160 | 0.007159162126481533 | 0.007240921258926392 |
| same_category_substitution | 128 | 2.8209295123815536e-05 | 6.279349327087402e-05 |
| set_H | 160 | 0.00715435529127717 | 0.007226243615150452 |
| upper_state_exchange_same_N | 64 | 0.007152653997763991 | 0.0071995556354522705 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## uniform_original_seed0

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0005292083515170533 | 0.0004752794716771835 | 24238 | 0.997959492752293 | False | 0.09188701957464218 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 58 | 237 | 0.24241852760314941 |
| 1 | 24435 | 60 | 232 | 0.24159598350524902 |
| 2 | 24435 | 59 | 251 | 0.24255622923374176 |
| 3 | 24435 | 60 | 238 | 0.2421785593032837 |
| saved r9 | 101 | 1 | 8 | 0.16932359337806702 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 31/24435 | 482/24435 | 6582/24435 | 215/24435 | 251/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.013177345506846905 | 0.03338451683521271 |
| L_single_round | 32 | 0.01031545689329505 | 0.014417469501495361 |
| N_run_1 | 64 | 0.005255021387711167 | 0.009931400418281555 |
| N_run_2 | 64 | 0.00523945246823132 | 0.028164073824882507 |
| N_run_3 | 64 | 0.005182033404707909 | 0.02215074747800827 |
| N_run_4 | 64 | 0.00488216825760901 | 0.010246306657791138 |
| N_run_5 | 64 | 0.005104709998704493 | 0.027952253818511963 |
| N_run_6 | 64 | 0.005025301245041192 | 0.010239459574222565 |
| N_run_7 | 64 | 0.005089280428364873 | 0.010032601654529572 |
| N_run_8 | 64 | 0.004993041860871017 | 0.007446855306625366 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.005046089199216415 | 0.027952253818511963 | False |
| short | 192 | 0.007413625018671155 | 0.03338451683521271 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0997808074951172 | 0.08463870391249656 | 0.08735795786694404 | False | 0/24435 |
| 1000 | 1.0408995759487152 | 0.0023566087288782 | 0.0035924283305754303 | False | 0/24435 |
| 2000 | 1.0437790656089783 | 0.0019736496399855243 | 0.0029573397224093023 | False | 0/24435 |
| 5000 | 1.0394749110937118 | 0.0011553493337123654 | 0.0025056766329383446 | False | 0/24435 |
| 10000 | 1.0431262350082398 | 0.0009901852266921197 | 0.0018811468913638922 | False | 0/24435 |
| 15000 | 1.0395417416095734 | 0.0004613775964389788 | 0.0011604761406378231 | False | 0/24435 |
| 20000 | 1.0391195011138916 | 0.00026926423226541373 | 0.0005292083515170533 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 18030 | 24326 | 6326 |
| 0 | 1 | 24435 | 17969 | 24326 | 6391 |
| 0 | 2 | 24435 | 17963 | 24326 | 6400 |
| 0 | 3 | 24435 | 17989 | 24326 | 6371 |
| 1000 | 0 | 24435 | 22221 | 1018 | 58 |
| 1000 | 1 | 24435 | 22153 | 1053 | 53 |
| 1000 | 2 | 24435 | 22193 | 995 | 46 |
| 1000 | 3 | 24435 | 22170 | 1060 | 58 |
| 2000 | 0 | 24435 | 23220 | 521 | 13 |
| 2000 | 1 | 24435 | 23152 | 550 | 23 |
| 2000 | 2 | 24435 | 23209 | 509 | 13 |
| 2000 | 3 | 24435 | 23197 | 564 | 14 |
| 5000 | 0 | 24435 | 21546 | 224 | 47 |
| 5000 | 1 | 24435 | 21569 | 202 | 48 |
| 5000 | 2 | 24435 | 21584 | 225 | 47 |
| 5000 | 3 | 24435 | 21617 | 205 | 39 |
| 10000 | 0 | 24435 | 19765 | 366 | 86 |
| 10000 | 1 | 24435 | 19740 | 376 | 83 |
| 10000 | 2 | 24435 | 19762 | 364 | 87 |
| 10000 | 3 | 24435 | 19780 | 376 | 89 |
| 15000 | 0 | 24435 | 19665 | 253 | 70 |
| 15000 | 1 | 24435 | 19626 | 240 | 66 |
| 15000 | 2 | 24435 | 19634 | 232 | 56 |
| 15000 | 3 | 24435 | 19639 | 234 | 69 |
| 20000 | 0 | 24435 | 19467 | 58 | 30 |
| 20000 | 1 | 24435 | 19433 | 60 | 33 |
| 20000 | 2 | 24435 | 19445 | 59 | 28 |
| 20000 | 3 | 24435 | 19449 | 60 | 32 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.765625 | 1.0 | 0.234375 [0.1953125, 0.26953125] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.779296875 | 0.59765625 | -0.181640625 [-0.23046875, -0.13081054687500004] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.7734375 | 0.47265625 | -0.30078125 [-0.35546875, -0.24604492187500004] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.80078125 | 0.556640625 | -0.244140625 [-0.29296875, -0.193359375] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.796875 | 0.798828125 | 0.001953125 [-0.04296875, 0.044970703124999956] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.36328125 | 0.96875 | 0.60546875 [0.560546875, 0.6484375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.32421875 | 0.08984375 | -0.234375 [-0.27734375, -0.185546875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.236328125 | 0.044921875 | -0.19140625 [-0.232421875, -0.150390625] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.298828125 | 0.09765625 | -0.201171875 [-0.25, -0.154296875] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.296875 | 0.130859375 | -0.166015625 [-0.212890625, -0.1171875] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.998046875 | 0.08984375 [0.06640625, 0.11528320312499996] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.91796875 | 0.90625 | -0.01171875 [-0.03515625, 0.009765625] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.92578125 | 0.927734375 | 0.001953125 [-0.013671875, 0.017578125] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.921875 | 0.931640625 | 0.009765625 [-0.005859375, 0.02734375] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.935546875 | 0.9453125 | 0.009765625 [-0.013671875, 0.033203125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.560546875 | 0.984375 | 0.423828125 [0.3828125, 0.462890625] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.5625 | 0.4140625 | -0.1484375 [-0.201171875, -0.09765625] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.62890625 | 0.39453125 | -0.234375 [-0.283203125, -0.1875] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.625 | 0.412109375 | -0.212890625 [-0.265625, -0.16010742187500004] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.55859375 | 0.45703125 | -0.1015625 [-0.154345703125, -0.046826171875000044] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.79296875 | 0.998046875 | 0.205078125 [0.171875, 0.24223632812499996] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.796875 | 0.658203125 | -0.138671875 [-0.189453125, -0.09370117187500004] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.802734375 | 0.580078125 | -0.22265625 [-0.281298828125, -0.17377929687500004] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.833984375 | 0.646484375 | -0.1875 [-0.234423828125, -0.138671875] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.8046875 | 0.802734375 | -0.001953125 [-0.044921875, 0.04296875] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.380859375 | 0.97265625 | 0.591796875 [0.55078125, 0.6328125] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.33984375 | 0.119140625 | -0.220703125 [-0.271484375, -0.169921875] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.275390625 | 0.048828125 | -0.2265625 [-0.26953125, -0.185546875] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.296875 | 0.08984375 | -0.20703125 [-0.253955078125, -0.162109375] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.30859375 | 0.107421875 | -0.201171875 [-0.244140625, -0.16015625] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.91015625 | 0.998046875 | 0.087890625 [0.0625, 0.11328125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.91796875 | 0.90234375 | -0.015625 [-0.0390625, 0.009765625] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.92578125 | 0.9296875 | 0.00390625 [-0.013671875, 0.021484375] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.93359375 | 0.931640625 | -0.001953125 [-0.021484375, 0.017578125] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.921875 | 0.94140625 | 0.01953125 [-0.001953125, 0.043017578124999956] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.560546875 | 0.984375 | 0.423828125 [0.382763671875, 0.46875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.55859375 | 0.38671875 | -0.171875 [-0.220703125, -0.125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.6015625 | 0.400390625 | -0.201171875 [-0.25390625, -0.150390625] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.58203125 | 0.375 | -0.20703125 [-0.2578125, -0.15815429687500004] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.548828125 | 0.404296875 | -0.14453125 [-0.197265625, -0.091796875] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.03338451683521271 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N1 | 0.009931400418281555 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.009303271770477295 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.009667187929153442 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.008252114057540894 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.008494585752487183 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.007983207702636719 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.007377937436103821 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.0070951879024505615 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.014417469501495361 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.004471778869628906 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.028164073824882507 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N3 | 0.02215074747800827 | 3 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N4 | 0.010246306657791138 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.027952253818511963 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N6 | 0.010239459574222565 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.010032601654529572 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.007446855306625366 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.01078885793685913 | True | [0.009705759584903717, 0.002646304666996002, 0.0034604892134666443, 0.004478462040424347, 0.00539948046207428, 0.006226010620594025, 0.006962239742279053, 0.007613472640514374, 0.008185312151908875] | [] | False |
| 2 | 64 | 64 | 0.01078885793685913 | True | [0.014260008931159973, 0.01078885793685913, 0.009791135787963867, 0.009185537695884705, 0.008742913603782654, 0.008337914943695068, 0.007960200309753418, 0.007607072591781616, 0.007275253534317017] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.006755926568681995 | 0.13118600845336914 |
| reset_L | 160 | 0.010562765365466475 | 0.22425882518291473 |
| same_category_substitution | 128 | 0.002918402082286775 | 0.10530678927898407 |
| set_H | 160 | 0.01315482473000884 | 0.026119664311408997 |
| upper_state_exchange_same_N | 64 | 0.006752754910849035 | 0.10913218557834625 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## uniform_original_seed1

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0005425570838622351 | 0.00042406204936636224 | 24201 | 0.9946948793391007 | False | 0.03873249888420105 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 328 | 4047 | 0.2556018680334091 |
| 1 | 24435 | 341 | 4078 | 0.2548995018005371 |
| 2 | 24435 | 330 | 4095 | 0.25550152361392975 |
| 3 | 24435 | 312 | 4138 | 0.25564686954021454 |
| saved r9 | 101 | 1 | 4 | 0.21106624603271484 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 12/24435 | 26/24435 | 443/24435 | 295/24435 | 20/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.009987258818000555 | 0.020324476063251495 |
| L_single_round | 32 | 0.007421270478516817 | 0.007602065801620483 |
| N_run_1 | 64 | 0.00878867320716381 | 0.012454226613044739 |
| N_run_2 | 64 | 0.008875809027813375 | 0.011150896549224854 |
| N_run_3 | 64 | 0.008853292325511575 | 0.011478617787361145 |
| N_run_4 | 64 | 0.008777754264883697 | 0.011684820055961609 |
| N_run_5 | 64 | 0.011467740754596889 | 0.17173947393894196 |
| N_run_6 | 64 | 0.008873176877386868 | 0.011714473366737366 |
| N_run_7 | 64 | 0.008928924798965454 | 0.011518560349941254 |
| N_run_8 | 64 | 0.008808042854070663 | 0.011603310704231262 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.009284821979235858 | 0.17173947393894196 | False |
| short | 192 | 0.008789582294411957 | 0.020324476063251495 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.088587999343872 | 0.07273375444114208 | 0.06714723890445831 | False | 0/24435 |
| 1000 | 1.0401296561956406 | 0.0021206773043377326 | 0.0038483428811491574 | False | 0/24435 |
| 2000 | 1.0393495351076125 | 0.0013974199880613014 | 0.002193118763746952 | False | 0/24435 |
| 5000 | 1.0416607892513274 | 0.0006601188429340254 | 0.0012652195883413881 | False | 0/24435 |
| 10000 | 1.037768634557724 | 0.000519243729140726 | 0.000687118939915725 | False | 0/24435 |
| 15000 | 1.0394057464599609 | 0.0006131036920123733 | 0.000648225680181568 | False | 0/24435 |
| 20000 | 1.0416059648990632 | 0.00021351901265006745 | 0.0005425570838622351 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 15035 | 23817 | 9230 |
| 0 | 1 | 24435 | 14906 | 23813 | 9365 |
| 0 | 2 | 24435 | 14976 | 23791 | 9290 |
| 0 | 3 | 24435 | 14881 | 23822 | 9382 |
| 1000 | 0 | 24435 | 17838 | 990 | 560 |
| 1000 | 1 | 24435 | 17901 | 985 | 542 |
| 1000 | 2 | 24435 | 17863 | 987 | 564 |
| 1000 | 3 | 24435 | 17852 | 1004 | 575 |
| 2000 | 0 | 24435 | 20604 | 590 | 298 |
| 2000 | 1 | 24435 | 20572 | 590 | 330 |
| 2000 | 2 | 24435 | 20611 | 566 | 316 |
| 2000 | 3 | 24435 | 20582 | 577 | 307 |
| 5000 | 0 | 24435 | 21952 | 167 | 83 |
| 5000 | 1 | 24435 | 21844 | 150 | 79 |
| 5000 | 2 | 24435 | 21847 | 158 | 71 |
| 5000 | 3 | 24435 | 21873 | 154 | 79 |
| 10000 | 0 | 24435 | 21339 | 120 | 92 |
| 10000 | 1 | 24435 | 21301 | 111 | 89 |
| 10000 | 2 | 24435 | 21331 | 112 | 89 |
| 10000 | 3 | 24435 | 21318 | 119 | 94 |
| 15000 | 0 | 24435 | 14335 | 207 | 165 |
| 15000 | 1 | 24435 | 14304 | 193 | 154 |
| 15000 | 2 | 24435 | 14227 | 206 | 168 |
| 15000 | 3 | 24435 | 14359 | 201 | 165 |
| 20000 | 0 | 24435 | 11987 | 328 | 219 |
| 20000 | 1 | 24435 | 12035 | 341 | 231 |
| 20000 | 2 | 24435 | 12012 | 330 | 206 |
| 20000 | 3 | 24435 | 12055 | 312 | 220 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.802734375 | 1.0 | 0.197265625 [0.162109375, 0.232421875] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.732421875 | 0.6484375 | -0.083984375 [-0.134765625, -0.03125] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.75 | 0.556640625 | -0.193359375 [-0.244140625, -0.142578125] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.765625 | 0.55859375 | -0.20703125 [-0.265625, -0.150390625] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.765625 | 0.677734375 | -0.087890625 [-0.13671875, -0.040966796875000044] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.30859375 | 0.97265625 | 0.6640625 [0.622998046875, 0.705126953125] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.263671875 | 0.1171875 | -0.146484375 [-0.19140625, -0.103515625] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.30078125 | 0.05078125 | -0.25 [-0.29296875, -0.208984375] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.259765625 | 0.11328125 | -0.146484375 [-0.19140625, -0.09765625] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.3671875 | 0.099609375 | -0.267578125 [-0.3203125, -0.22065429687500004] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.908203125 | 0.998046875 | 0.08984375 [0.068359375, 0.1171875] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.912109375 | 0.91015625 | -0.001953125 [-0.021484375, 0.017578125] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.908203125 | 0.927734375 | 0.01953125 [0.0, 0.037158203124999956] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.939453125 | 0.93359375 | -0.005859375 [-0.01953125, 0.0078125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.92578125 | 0.9375 | 0.01171875 [-0.0078125, 0.033203125] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.607421875 | 0.984375 | 0.376953125 [0.337890625, 0.41801757812499996] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.6015625 | 0.4609375 | -0.140625 [-0.1953125, -0.08984375] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.57421875 | 0.3828125 | -0.19140625 [-0.240234375, -0.142578125] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.568359375 | 0.35546875 | -0.212890625 [-0.263671875, -0.162109375] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.697265625 | 0.427734375 | -0.26953125 [-0.322314453125, -0.216796875] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.810546875 | 0.998046875 | 0.1875 [0.15234375, 0.22265625] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.765625 | 0.6484375 | -0.1171875 [-0.16796875, -0.0703125] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.751953125 | 0.568359375 | -0.18359375 [-0.232470703125, -0.13081054687500004] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.74609375 | 0.56640625 | -0.1796875 [-0.2421875, -0.12104492187500004] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.791015625 | 0.689453125 | -0.1015625 [-0.1484375, -0.054638671875000044] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.345703125 | 0.9765625 | 0.630859375 [0.58984375, 0.671875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.30078125 | 0.11328125 | -0.1875 [-0.23046875, -0.142578125] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.32421875 | 0.041015625 | -0.283203125 [-0.322265625, -0.240234375] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.28515625 | 0.076171875 | -0.208984375 [-0.25390625, -0.1640625] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.40234375 | 0.08984375 | -0.3125 [-0.361328125, -0.26362304687500004] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.923828125 | 0.998046875 | 0.07421875 [0.05078125, 0.095703125] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.90234375 | 0.90625 | 0.00390625 [-0.0234375, 0.027392578124999956] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.919921875 | 0.9296875 | 0.009765625 [-0.009765625, 0.029296875] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.931640625 | 0.93359375 | 0.001953125 [-0.01171875, 0.017578125] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.923828125 | 0.92578125 | 0.001953125 [-0.01953125, 0.0234375] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.6015625 | 0.98046875 | 0.37890625 [0.339794921875, 0.419921875] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.546875 | 0.392578125 | -0.154296875 [-0.201171875, -0.109375] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.5625 | 0.390625 | -0.171875 [-0.21875, -0.126953125] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.580078125 | 0.37109375 | -0.208984375 [-0.255859375, -0.16401367187500004] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.6875 | 0.396484375 | -0.291015625 [-0.33984375, -0.240234375] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.020324476063251495 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N1 | 0.012454226613044739 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N2 | 0.011150896549224854 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N3 | 0.011478617787361145 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.011684820055961609 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.011478729546070099 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N6 | 0.011714473366737366 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N7 | 0.011518560349941254 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.011603310704231262 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N0 | 0.007602065801620483 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.007851749658584595 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.00893189013004303 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.009546175599098206 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.008522644639015198 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.17173947393894196 | 2 | 2 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| L_N6 | 0.008935347199440002 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.011334165930747986 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N8 | 0.008543893694877625 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.011102661490440369 | True | [0.007413908839225769, 0.009866297245025635, 0.011149674654006958, 0.01101614534854889, 0.009850740432739258, 0.00849868357181549, 0.00848369300365448, 0.008357703685760498, 0.008257687091827393] | [] | False |
| 2 | 64 | 64 | 0.011102661490440369 | True | [0.010658122599124908, 0.011102661490440369, 0.01111360639333725, 0.011288397014141083, 0.011519744992256165, 0.011780373752117157, 0.012050315737724304, 0.01231750100851059, 0.012575268745422363] | [] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.009025230499294897 | 0.023808114230632782 |
| reset_L | 160 | 0.017230862379074098 | 0.24968640506267548 |
| same_category_substitution | 128 | 0.0013084059464745224 | 0.0209796279668808 |
| set_H | 160 | 0.010059846052899956 | 0.018770024180412292 |
| upper_state_exchange_same_N | 64 | 0.008974135853350163 | 0.016250066459178925 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.

## uniform_original_seed2

Endpoint: B_INCOMPLETE; first crossing: None

| Natural KL bits | Unseen KL bits | Unseen count | Witness recovery | Swap pass | Prediction rerender TV | A rerender differences |
|---|---|---|---|---|---|---|
| 0.0009570500712769281 | 0.0006747302536488847 | 24245 | 0.9909050944203344 | False | 0.03342696279287338 | 0 |

| Rendering | Boards/cases | B category errors | TV > .02 | Maximum TV |
|---|---|---|---|---|
| 0 | 24435 | 87 | 613 | 0.25117359310388565 |
| 1 | 24435 | 84 | 633 | 0.25069759786129 |
| 2 | 24435 | 85 | 646 | 0.2515562027692795 |
| 3 | 24435 | 90 | 620 | 0.25106802582740784 |
| saved r9 | 101 | 0 | 16 | 0.09011982381343842 |

| A slot 1 | A slot 2 | A slot 3 | A slot 4 | A slot 5 | A vector | Local A histories |
|---|---|---|---|---|---|---|
| 27/24435 | 39/24435 | 1453/24435 | 1483/24435 | 14/24435 | 0/24435 | not operative |

| Law case | Count | Mean TV | Max TV |
|---|---|---|---|
| H_single_round | 32 | 0.013936032308265567 | 0.02436770498752594 |
| L_single_round | 32 | 0.010151613969355822 | 0.017361700534820557 |
| N_run_1 | 64 | 0.012672673910856247 | 0.02653181552886963 |
| N_run_2 | 64 | 0.013026435975916684 | 0.06642723083496094 |
| N_run_3 | 64 | 0.012066005379892886 | 0.01809483766555786 |
| N_run_4 | 64 | 0.011750514036975801 | 0.01712195575237274 |
| N_run_5 | 64 | 0.012563386699184775 | 0.02752736210823059 |
| N_run_6 | 64 | 0.012832110049203038 | 0.029618069529533386 |
| N_run_7 | 64 | 0.013376983115449548 | 0.04589046537876129 |
| N_run_8 | 64 | 0.01305017457343638 | 0.028090789914131165 |

| Law panel | Count | Mean TV | Max TV | Pass |
|---|---|---|---|---|
| long | 384 | 0.012606528975690404 | 0.04589046537876129 | False |
| short | 192 | 0.012580977675194541 | 0.06642723083496094 | False |

| Anchor | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 |
|---|---|---|---|---|---|---|---|---|
| L | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |
| H | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 | 160000 |

| Update | B loss | Coverage endpoint KL | Natural KL | B pass | A vector |
|---|---|---|---|---|---|
| 0 | 1.0980093252658845 | 0.08718953408300877 | 0.08387336464419716 | False | 0/24435 |
| 1000 | 1.0409793114662171 | 0.0017564571209368297 | 0.004165190595132086 | False | 0/24435 |
| 2000 | 1.039423134326935 | 0.0012057124395505525 | 0.002431350384859406 | False | 0/24435 |
| 5000 | 1.0415971285104753 | 0.0006765658369113225 | 0.0014666567300655842 | False | 0/24435 |
| 10000 | 1.0383632361888886 | 0.0007909219895373098 | 0.0010893017637781711 | False | 0/24435 |
| 15000 | 1.0411885273456574 | 0.0003211012692918302 | 0.0007999594716933683 | False | 0/24435 |
| 20000 | 1.0398379921913148 | 0.0008852113950706552 | 0.0009570500712769281 | False | 0/24435 |

| Update | Rendering | Boards | A-head category errors | B-signature errors | B errors with A category correct |
|---|---|---|---|---|---|
| 0 | 0 | 24435 | 16804 | 1944 | 226 |
| 0 | 1 | 24435 | 16708 | 1944 | 196 |
| 0 | 2 | 24435 | 16621 | 1944 | 228 |
| 0 | 3 | 24435 | 16820 | 1944 | 196 |
| 1000 | 0 | 24435 | 21830 | 1727 | 402 |
| 1000 | 1 | 24435 | 21835 | 1742 | 391 |
| 1000 | 2 | 24435 | 21814 | 1758 | 405 |
| 1000 | 3 | 24435 | 21791 | 1788 | 409 |
| 2000 | 0 | 24435 | 22669 | 772 | 187 |
| 2000 | 1 | 24435 | 22690 | 785 | 194 |
| 2000 | 2 | 24435 | 22614 | 749 | 183 |
| 2000 | 3 | 24435 | 22656 | 800 | 193 |
| 5000 | 0 | 24435 | 22743 | 154 | 18 |
| 5000 | 1 | 24435 | 22679 | 143 | 13 |
| 5000 | 2 | 24435 | 22664 | 147 | 10 |
| 5000 | 3 | 24435 | 22717 | 151 | 15 |
| 10000 | 0 | 24435 | 21870 | 222 | 79 |
| 10000 | 1 | 24435 | 21775 | 229 | 87 |
| 10000 | 2 | 24435 | 21736 | 207 | 75 |
| 10000 | 3 | 24435 | 21713 | 229 | 97 |
| 15000 | 0 | 24435 | 22454 | 207 | 102 |
| 15000 | 1 | 24435 | 22420 | 204 | 110 |
| 15000 | 2 | 24435 | 22369 | 199 | 94 |
| 15000 | 3 | 24435 | 22357 | 213 | 120 |
| 20000 | 0 | 24435 | 23202 | 87 | 9 |
| 20000 | 1 | 24435 | 23202 | 84 | 3 |
| 20000 | 2 | 24435 | 23197 | 85 | 9 |
| 20000 | 3 | 24435 | 23166 | 90 | 5 |

| Carrier | Reader | Target | Slot | Start | End | Gain (95% CI) | Majority | Oracle | Converged |
|---|---|---|---|---|---|---|---|---|---|
| raw | linear | category3 | 1 | 0.744140625 | 0.998046875 | 0.25390625 [0.216796875, 0.291015625] | 0.919921875 | 0.998046875 | True |
| raw | linear | category3 | 2 | 0.7578125 | 0.6328125 | -0.125 [-0.177783203125, -0.07026367187500004] | 0.90625 | 1.0 | True |
| raw | linear | category3 | 3 | 0.748046875 | 0.8046875 | 0.056640625 [0.005859375, 0.10546875] | 0.9296875 | 1.0 | True |
| raw | linear | category3 | 4 | 0.81640625 | 0.658203125 | -0.158203125 [-0.208984375, -0.10932617187500004] | 0.93359375 | 1.0 | True |
| raw | linear | category3 | 5 | 0.720703125 | 0.666015625 | -0.0546875 [-0.107421875, 0.0] | 0.927734375 | 1.0 | True |
| raw | linear | sum36 | 1 | 0.25390625 | 0.958984375 | 0.705078125 [0.665966796875, 0.74609375] | 0.33984375 | 1.0 | True |
| raw | linear | sum36 | 2 | 0.322265625 | 0.08984375 | -0.232421875 [-0.27734375, -0.1875] | 0.35546875 | 1.0 | True |
| raw | linear | sum36 | 3 | 0.29296875 | 0.2265625 | -0.06640625 [-0.115234375, -0.013671875] | 0.40625 | 1.0 | True |
| raw | linear | sum36 | 4 | 0.359375 | 0.126953125 | -0.232421875 [-0.28515625, -0.177734375] | 0.375 | 0.998046875 | True |
| raw | linear | sum36 | 5 | 0.26953125 | 0.205078125 | -0.064453125 [-0.119140625, -0.013671875] | 0.404296875 | 0.998046875 | True |
| raw | mlp64 | category3 | 1 | 0.923828125 | 1.0 | 0.076171875 [0.052734375, 0.099609375] | 0.919921875 | 0.998046875 | None |
| raw | mlp64 | category3 | 2 | 0.923828125 | 0.91796875 | -0.005859375 [-0.02734375, 0.015625] | 0.90625 | 0.998046875 | None |
| raw | mlp64 | category3 | 3 | 0.9296875 | 0.951171875 | 0.021484375 [0.0, 0.04296875] | 0.9296875 | 1.0 | None |
| raw | mlp64 | category3 | 4 | 0.93359375 | 0.935546875 | 0.001953125 [-0.015625, 0.017578125] | 0.93359375 | 1.0 | None |
| raw | mlp64 | category3 | 5 | 0.912109375 | 0.927734375 | 0.015625 [-0.0078125, 0.04296875] | 0.927734375 | 1.0 | None |
| raw | mlp64 | sum36 | 1 | 0.556640625 | 0.982421875 | 0.42578125 [0.384765625, 0.470703125] | 0.33984375 | 0.998046875 | None |
| raw | mlp64 | sum36 | 2 | 0.603515625 | 0.4296875 | -0.173828125 [-0.2265625, -0.12495117187500004] | 0.35546875 | 1.0 | None |
| raw | mlp64 | sum36 | 3 | 0.56640625 | 0.4765625 | -0.08984375 [-0.140625, -0.040966796875000044] | 0.40625 | 1.0 | None |
| raw | mlp64 | sum36 | 4 | 0.62109375 | 0.505859375 | -0.115234375 [-0.181640625, -0.052685546875000044] | 0.375 | 1.0 | None |
| raw | mlp64 | sum36 | 5 | 0.64453125 | 0.486328125 | -0.158203125 [-0.216796875, -0.10737304687500004] | 0.404296875 | 1.0 | None |
| upper | linear | category3 | 1 | 0.7734375 | 0.998046875 | 0.224609375 [0.1875, 0.26171875] | 0.919921875 | 0.998046875 | True |
| upper | linear | category3 | 2 | 0.80078125 | 0.66796875 | -0.1328125 [-0.181640625, -0.08198242187500004] | 0.90625 | 1.0 | True |
| upper | linear | category3 | 3 | 0.771484375 | 0.80859375 | 0.037109375 [-0.01171875, 0.08984375] | 0.9296875 | 1.0 | True |
| upper | linear | category3 | 4 | 0.84375 | 0.708984375 | -0.134765625 [-0.181640625, -0.087890625] | 0.93359375 | 1.0 | True |
| upper | linear | category3 | 5 | 0.7421875 | 0.67578125 | -0.06640625 [-0.115283203125, -0.01171875] | 0.927734375 | 1.0 | True |
| upper | linear | sum36 | 1 | 0.267578125 | 0.97265625 | 0.705078125 [0.666015625, 0.748046875] | 0.33984375 | 1.0 | True |
| upper | linear | sum36 | 2 | 0.353515625 | 0.08984375 | -0.263671875 [-0.310546875, -0.21674804687500004] | 0.35546875 | 1.0 | True |
| upper | linear | sum36 | 3 | 0.30859375 | 0.189453125 | -0.119140625 [-0.169921875, -0.0703125] | 0.40625 | 1.0 | True |
| upper | linear | sum36 | 4 | 0.380859375 | 0.115234375 | -0.265625 [-0.31640625, -0.21284179687500004] | 0.375 | 0.998046875 | True |
| upper | linear | sum36 | 5 | 0.287109375 | 0.150390625 | -0.13671875 [-0.187548828125, -0.0859375] | 0.404296875 | 0.998046875 | True |
| upper | mlp64 | category3 | 1 | 0.908203125 | 0.998046875 | 0.08984375 [0.064453125, 0.115234375] | 0.919921875 | 1.0 | None |
| upper | mlp64 | category3 | 2 | 0.916015625 | 0.916015625 | 0.0 [-0.0234375, 0.021484375] | 0.90625 | 1.0 | None |
| upper | mlp64 | category3 | 3 | 0.916015625 | 0.93359375 | 0.017578125 [-0.007861328124999997, 0.04296875] | 0.9296875 | 0.998046875 | None |
| upper | mlp64 | category3 | 4 | 0.94140625 | 0.935546875 | -0.005859375 [-0.025390625, 0.01171875] | 0.93359375 | 0.998046875 | None |
| upper | mlp64 | category3 | 5 | 0.90234375 | 0.931640625 | 0.029296875 [0.005859375, 0.052734375] | 0.927734375 | 1.0 | None |
| upper | mlp64 | sum36 | 1 | 0.513671875 | 0.978515625 | 0.46484375 [0.419921875, 0.5078125] | 0.33984375 | 1.0 | None |
| upper | mlp64 | sum36 | 2 | 0.599609375 | 0.419921875 | -0.1796875 [-0.226611328125, -0.1328125] | 0.35546875 | 1.0 | None |
| upper | mlp64 | sum36 | 3 | 0.576171875 | 0.4609375 | -0.115234375 [-0.166064453125, -0.06640625] | 0.40625 | 1.0 | None |
| upper | mlp64 | sum36 | 4 | 0.640625 | 0.484375 | -0.15625 [-0.209033203125, -0.099609375] | 0.375 | 1.0 | None |
| upper | mlp64 | sum36 | 5 | 0.634765625 | 0.46875 | -0.166015625 [-0.220703125, -0.111328125] | 0.404296875 | 1.0 | None |

| Worst prefix | TV | First deviation | Earliest incorrect constituent | Chronology | Descriptive hypothesis |
|---|---|---|---|---|---|
| H_N0 | 0.02436770498752594 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N1 | 0.02653181552886963 | 1 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N2 | 0.06642723083496094 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N3 | 0.01809483766555786 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N4 | 0.01712195575237274 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N5 | 0.019270315766334534 | 3 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| H_N6 | 0.029618069529533386 | 1 | 1 | COINCIDENT | BOARD_ASSOCIATED_FAILURE |
| H_N7 | 0.017980992794036865 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| H_N8 | 0.028090789914131165 | 9 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N0 | 0.017361700534820557 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N1 | 0.018507525324821472 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N2 | 0.01454276591539383 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N3 | 0.016089431941509247 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N4 | 0.013368621468544006 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N5 | 0.02752736210823059 | 2 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N6 | 0.014743871986865997 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |
| L_N7 | 0.04589046537876129 | 8 | None | NO_OBSERVED_CONSTITUENT_ERROR | CAUSE_UNRESOLVED |
| L_N8 | 0.01660560816526413 | None | None | NO_OBSERVED_CONSTITUENT_ERROR | NO_DEVIATION |

| Clear-N anchor | Boards | Correct N signatures | Response TV | Valid anchor | N0–N8 maximum TVs | Violating N lengths | Recurrence evidence |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 64 | 0.03285872936248779 | True | [0.00924595445394516, 0.01335945725440979, 0.013414032757282257, 0.013708576560020447, 0.014262184500694275, 0.01497059315443039, 0.015769310295581818, 0.01661914587020874, 0.017542175948619843] | [] | False |
| 2 | 64 | 64 | 0.03285872936248779 | True | [0.013562686741352081, 0.03285872936248779, 0.04785199463367462, 0.05418199300765991, 0.05363927781581879, 0.04879830777645111, 0.042354270815849304, 0.03641875088214874, 0.03182747960090637] | [1, 2, 3, 4, 5, 6, 7, 8] | False |

| Registered swap case | Count | Mean TV | Max TV |
|---|---|---|---|
| neutral_N | 192 | 0.01223893091082573 | 0.02154780924320221 |
| reset_L | 160 | 0.013203625520691275 | 0.25196143984794617 |
| same_category_substitution | 128 | 0.0018004734884016216 | 0.009896256029605865 |
| set_H | 160 | 0.01829311461187899 | 0.08264163136482239 |
| upper_state_exchange_same_N | 64 | 0.012286479235626757 | 0.017141632735729218 |

Exposure, complete clear-neutral responses and route damage: see the complete numerical records in aggregate.json.
