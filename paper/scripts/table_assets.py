"""One entry point per main/prepared/appendix table, using verified cells only."""
from __future__ import annotations

from collections import defaultdict
import json
import re

from asset_inputs import tex, number
from build_ledger import contract
from condition_labels import condition_name


def cell_tex(value,width=.5):
    # Only opaque identifiers/paths may break internally. Never split prose
    # words or numbers into arbitrary chunks to make a narrow column fit.
    text=str(value)
    return tex(text)


def write(ctx, name, title, headers, rows, caption, widths=None, note=None):
    rows=contract.sanitize(rows)
    full_headers=headers
    from table_summaries import analytical_rows, publish_detail
    detail = None
    displayed = rows
    if name in SUPPLEMENT_TABLES:
        detail = publish_detail(ctx, name, headers, rows)
        headers, displayed, widths = analytical_rows(ctx, name, headers, rows, widths)
        caption += ' Analytical reduction only; exact per-cell and per-update rows remain released.'
        if name in ('appendix_E_probes','appendix_E_r11_probes','appendix_E_r12_probes'):
            caption += ' Printed sum-reader ranges retain seed identities; category readers remain in the detailed file. Gain CI envelopes span the five saved slot intervals and are not new confidence intervals. Floor ranges span seeds and slots.'
        caption += f' Detailed records: paper/{detail["path"]} (schema and SHA-256 in release/index.json).'
    folder = ctx.root / "paper/tables"; folder.mkdir(parents=True, exist_ok=True)
    widths = widths or [5.9/len(headers)]*len(headers)
    available=6.5-6*(len(headers)-1)/72.27
    if sum(widths)>available:widths=[w*available/sum(widths) for w in widths]
    fmt = "@{}" + "".join(r">{\raggedright\arraybackslash}"+f"p{{{w:.3f}in}}" for w in widths) + "@{}"
    # Single-column width; no resizebox or sub-7pt type. Long tables paginate.
    head = " & ".join(r"\textbf{"+cell_tex(s,w)+"}" for s,w in zip(headers,widths)) + r" \\"
    lines = ["% Built from ledger-bound values; edit the script, not this table.",
             r"\begingroup\fontsize{8}{9.5}\selectfont\setlength{\tabcolsep}{3pt}\emergencystretch=1em\hyphenpenalty=10000\exhyphenpenalty=10000",
             r"\begin{longtable}{"+fmt+"}", r"\caption{"+tex(title)+". "+tex(caption)+r"}\label{tab:"+name+r"}\\",
             r"\toprule", head, r"\midrule\endfirsthead", r"\toprule", head, r"\midrule\endhead",
             r"\midrule\multicolumn{"+str(len(headers))+r"}{r}{Continued on next page}\\\endfoot",
             r"\bottomrule\endlastfoot"]
    for row_index,row in enumerate(displayed):
        if len(row) != len(headers): raise ValueError("table row width differs")
        def display(v,w):
            if name=='table2' and isinstance(v,list):
                return r'\begin{tabular}[t]{@{}l@{}}'+r'\\'.join(cell_tex(number(x),w) for x in v)+r'\end{tabular}'
            return cell_tex(number(v),w)
        # Keep the final three rows together: a last header plus one lone row
        # is not a useful analytical supplement page.
        ending=r" \\*" if len(displayed)-3<=row_index<len(displayed)-1 else r" \\"
        lines.append(" & ".join(display(v,w) for v,w in zip(row,widths)) + ending)
    lines += [r"\end{longtable}"]
    if note:lines += [r'\noindent\textit{Table note.} '+tex(note)+r'\par']
    lines += [r"\endgroup", ""]
    path = folder / (name+".tex"); path.write_text("\n".join(lines))
    ctx.save_receipts(name, "tables", title+". "+caption,
                      {"headers": full_headers, "rows": rows, "displayed_headers": headers, "displayed_rows": displayed,
                       "detailed_file": detail, "note": note, "font_pt": 8,
                       "width_inches":sum(widths)+6*(len(headers)-1)/72.27,
                       "float_display": "five significant digits; all counts exact; unrounded receipts retained"})
    return {"name": name, "file": str(path.relative_to(ctx.root / "paper")), "caption": caption}


def info(n, key, row):
    if n == 13: return row["run"]["condition"], row["run"]["law"], row["run"]["seed"]
    if n == 9: return key.rsplit("_seed", 1)[0], "original", int(key[-1])
    law = "equal" if "_equal_" in key else "original"
    return key.split("_"+law+"_")[0], law, int(key[-1])


def get(d, *p, default=None):
    for k in p:
        if not isinstance(d, dict) or k not in d: return default
        d = d[k]
    return d


def reader_status(family,flag):
    return flag if family=='linear' else 'fixed budget; convergence not assessed'


def endpoint(ctx, n, key, r):
    """Recorded endpoint view. Missing panels stay missing, never become zero."""
    for field in r:
        if field in {"endpoint_label", "endpoint_status", "B_pass", "B_criteria", "prediction_checks", "prediction",
                     "board_census", "census_all_four_renderings_and_r9", "census_counts", "law_panels", "B_law",
                     "law_cases", "endpoint_B_bars", "endpoint_B_pass", "saved_r8", "board_effects", "A_exact_counts",
                     "A_components", "A_local_histories", "local_history_counts", "sums", "supplier",
                     "loss_KL_curve", "B_curve", "B_A_curve", "fixed_endpoint_label", "summary", "run"}:
            ctx.ref("control", str(n), key, field)
    law = info(n, key, r)[1]
    curve = next((r[k] for k in ("loss_KL_curve", "B_curve", "B_A_curve", "learning_curve") if k in r), [])
    last = curve[-1] if curve else {}
    prediction = r.get("prediction", r.get("prediction_checks", {}))
    kl = prediction.get("natural_excess_KL_bits", prediction.get("natural_KL_bits",
         get(r, "saved_r8", "natural_KL_bits", default=last.get("natural_excess_KL_bits",
             last.get("natural_KL_bits", last.get("natural_KL"))))))
    census = get(r, "census_all_four_renderings_and_r9", "registered_rendering",
                  default=get(r, "board_census", "registered_rendering", default={}))
    if "census_counts" in r: census = r["census_counts"][0]
    if "board_effects" in r:
        census = {"categorical_misreads": sum(v["signature_misreads"] for v in r["board_effects"]["by_slot1_sum_twelfths"].values()),
                  "above_0_02_TV": r["board_effects"]["above_TV_limit"]}
    a = r.get("A_exact_counts", r.get("sums", r.get("A_components", {})))
    vector = get(a, "vector", "correct")
    total = get(a, "vector", "total")
    criteria = prediction.get("criteria", r.get("criteria", r.get("endpoint_B_bars", r.get("B_criteria", {}))))
    passed = prediction.get("B_pass", r.get("B_pass", r.get("endpoint_B_pass")))
    label = r.get("endpoint_label", r.get("fixed_endpoint_label", r.get("endpoint_status", "")))
    if passed is None and n == 8: passed = label == "B_PASS"
    if passed is None and criteria and all(isinstance(v, bool) for v in criteria.values()):
        passed = all(criteria.values())
    short = get(r, "law_panels", "panels", "short", "maximum_TV")
    long = get(r, "law_panels", "panels", "long", "maximum_TV")
    if n == 11:
        cases=r['B_law']['cases']
        short=max(v['maximum_TV'] for k,v in cases.items() if k.endswith('single_round') or k in ('N_run_1','N_run_2'))
        long=r['B_law']['maximum_TV']
    if n == 13:
        rec = r["audit_references"][-1]; audit, eid = ctx.referenced(rec)
        ctx.ref(eid, "audit", "mode_law")
        cases = audit["audit"]["mode_law"]["cases"]
        short = max(v["maximum_TV"] for k,v in cases.items() if k.endswith("single_round") or k in ("N_run_1", "N_run_2"))
        long = max(cases[f"N_run_{j}"]["maximum_TV"] for j in range(3, 9))
    if n == 10:
        long = get(r, "law_cases", "law_rows", "maximum_TV")
    if n == 8 and law == "original":
        diagnostic = ctx.sources["control"]["9"][info(n,key,r)[0]+f"_seed{info(n,key,r)[2]}"]
        ctx.ref("control", "9", info(n,key,r)[0]+f"_seed{info(n,key,r)[2]}", "saved_r8")
        long = diagnostic["saved_r8"]["law_maximum_TV"]  # full panel, explicitly labelled below
    return {"KL": kl, "short": short, "long": long, "misreads": census.get("categorical_misreads"),
            "TV_errors": census.get("prediction_TV_errors", census.get("above_0_02_TV")),
            "sum_vector": vector, "sum_total": total, "passed": passed, "criteria": criteria,
            "law": law, "label": ('not assessed in r9' if n==9 else label or ("PASS" if passed else "INCOMPLETE"))}


def recovery(ctx,n,key,row):
    """A scoped measured reader, not a claim about all internal information."""
    field='probe_changes' if n==11 else 'probes'
    if n in (11,12) and field in row:
        data=ctx.ref('control',str(n),key,field)
        slots=get(data,'raw','linear','sum36',default=[])
        good=[v for v in slots if v['converged'] and
              v['endpoint_accuracy']>max(v['majority_floor'],v['shuffled_floor']) and v['paired_CI95'][0]>0]
        counts=', '.join(f"{v['endpoint_counts']['correct']}/512" for v in slots)
        return ('supported' if good else 'not supported')+f' {len(good)}/5 slots; raw linear sum reader [{counts}]; converged gains above majority/shuffled floors'
    if n==8 and 'raw_only' in key:
        data=ctx.ref('quantities','r8_probes')
        seed=int(key[-1]);floors=ctx.ref('calibration','8','calibration','probe','oracle','floors')
        good=[p for p in data if p['seed']==seed and p['probe_family']=='linear' and
              p['original']['converged'] and p['original']['paired_gain_CI95'][0]>0 and
              p['original']['endpoint_accuracy']>max(p['original']['majority_floor'],floors[p['slot']-1]['shuffled_accuracy'])]
        return ('supported' if good else 'not supported')+': raw linear sum reader, slots '+', '.join(str(p['slot']) for p in good)+'; 512 held-out boards; majority/shuffled controls, convergence'
    if n==10 and 'probe_summary' in row:
        data=ctx.ref('control','10',key,'probe_summary')
        slots=[v for v in data if v['site']=='raw' and v['family']=='linear' and v['task']=='sum']
        good=[v for v in slots if v['fits_converged'] and v['readability_gain'] and
              v['endpoint']>max(v['majority_floor'],v['shuffled_accuracy'])]
        return ('supported' if good else 'not supported')+f': {len(good)}/5 raw linear sum readers; '+', '.join(f"{v['correct']}/{v['total']}" for v in slots)+' held-out boards; majority/shuffled controls, convergence'
    return 'not established (no scoped sum reader)'


def full_table1(ctx):
    ctx.begin(); groups = defaultdict(list)
    for n in (8, 10, 11, 12, 13):
        for key, row in ctx.sources["control"][str(n)].items():
            condition, law, seed = info(n, key, row)
            if law != "original": continue
            groups[n, condition].append((seed, key, row))
    rows = []
    for (n, condition), runs in groups.items():
        runs.sort()
        views = [endpoint(ctx, n, key, row) if not (n == 13 and row["run"]["experiment"] == "erosion")
                 else {"passed": None, "sum_vector": None} for s,key,row in runs]
        supplied = condition in {"a_only", "dual", "a_forced", "a_supplied", "exact", "onehot", "numerical"}
        connected = condition in {"frozen", "live"}
        read='; '.join(f'seed {s}: '+recovery(ctx,n,k,r) for s,k,r in runs)
        if n == 8 and condition == "raw_only": ctx.ref("quantities", "r8_probes")
        if n == 10 and condition in {"free", "free_a"}:
            for s,k,r in runs: ctx.ref("control", "10", k, "probe_summary")
        comp = "supported (frozen)" if supplied else "not established"
        if any(v.get("sum_vector") is not None for v in views):
            exact=[v.get('sum_total') and v.get('sum_vector')==v.get('sum_total') for v in views]
            count=sum(bool(x) for x in exact)
            comp = f"{'supported' if count else 'not supported'} {count}/3; audited sum-output vectors: "+' / '.join(str(v.get('sum_vector')) for v in views)+' of 24,435; '+('unsupervised output head' if condition not in ('a_target','erosion_a_plus_b') and not condition.startswith('dose_') else 'supervised output head')
        access = "supported by design (exact sums supplied)" if supplied else "demonstrated by matched connection intervention (not selective use)" if connected else "not established"
        preserve = "supported (frozen)" if supplied or condition == "frozen" else "not established"
        if n == 13 and runs[0][2]["run"]["experiment"] == "erosion":
            for s,k,r in runs: ctx.ref("control", "13", k, "accuracy_curve")
            preserve = "supported" if condition == "blocked" else "not supported"
            comp = "supported" if all(r['accuracy_curve'][-1][1]==1555 for s,k,r in runs) else "not supported"
        elif n == 11 and condition.startswith("erosion_"):
            preserve = "not supported (inexact)"
        count = sum(v["passed"] is True for v in views)
        reliable = "not established" if all(v["passed"] is None for v in views) else (
            f"supported {count}/3" if count else "not supported 0/3")
        support = "1,555 histories (erosion)" if n == 13 and condition in {"adam","sgd","reduced","blocked"} else (
            "512 probe boards; registered B panels" if n in (8,10) else "24,435 boards; registered B panels")
        rows.append([f"r{n}: {condition_name(condition)}", read, comp, access, preserve, reliable, support])
    return write(ctx, "table1_full", "Five achievements: complete scoped condition matrix", ["study / condition", "recoverability", "computation",
        "access", "preservation", "reliable prediction", "support / evidence"], rows,
        "Original-law conditions; three seeds each. Supported is limited to the named measurement and support, "
        "not supported means a tested criterion failed, and not established means it was not established by the "
        "available measure. Mixed pass counts retain failing seeds. Frozen preservation is by verified design, "
        "not evidence that further training would preserve a live computation. Probe recovery is not use. "
        "Computation marks refer only to the audited sums output; failure does not establish that no internal computation exists. "
        "Board-output counts refer to rendering 0; other renderings are reported separately in Supplement Table S16. Local erosion uses 1,555 histories, not a board census. "
        "Full per-seed counts, controls and ceilings follow in this supplement.", [.9,1.55,1.25,.60,.60,.65,.65])


def table1(ctx):
    ctx.begin();rows=[]
    for n,condition in ((8,'raw_only'),(10,'free'),(10,'free_a'),
                        (11,'erosion_b_only'),(11,'erosion_a_plus_b'),
                        (12,'a_target'),(12,'a_supplied'),
                        (13,'disconnected'),(13,'frozen'),(13,'live'),(13,'exact'),(13,'numerical'),(13,'blocked')):
        runs=sorted((info(n,k,r)[2],k,r) for k,r in ctx.sources['control'][str(n)].items()
                    if info(n,k,r)[:2]==(condition,'original'))
        rs=[recovery(ctx,n,k,r) for s,k,r in runs]
        if n==13 and condition=='blocked':
            counts=[ctx.ref('control','13',k,'accuracy_curve')[-1][1] for s,k,r in runs]
            comp='supported: '+number(counts)+' / 1,555';reliable='not assessed';preserve='supported (blocked control)'
        else:
            views=[endpoint(ctx,n,k,r) for s,k,r in runs]
            counts=[v['sum_vector'] for v in views]
            exact_count=sum(x==24435 for x in counts)
            comp='not established' if all(x is None for x in counts) else f"{'supported' if exact_count else 'not supported'} {exact_count}/3: "+number(counts)+' / 24,435'
            reliable=f"{sum(v['passed'] is True for v in views)}/3 seeds pass"
            preserve='supported (supplier frozen)' if condition in ('a_supplied','frozen','exact','numerical') else 'not supported (erosion)' if condition.startswith('erosion_') else 'not established'
        supported=[re.search(r'(\d)/5',x) for x in rs]
        read=('supported slots: '+ ' / '.join(m.group(1)+'/5' for m in supported)
              if all(supported) else 'supported slots: 1/5 / 1/5 / 1/5 (slot 1)' if n==8 else 'not established')
        access='supported by design: exact sums supplied' if condition in ('a_supplied','exact','numerical') else 'demonstrated by matched connection intervention; selective use not established' if condition in ('live','frozen') else 'not established'
        rows.append([f'r{n}: '+condition_name(condition),read,comp,access,preserve,reliable])
    return compact_table1(ctx,rows)


def compact_table1(ctx, rows):
    """Display compression only: the evidence-derived full cells stay in receipts."""
    headers=['condition','recoverability','computation','access','preservation','reliable prediction']
    displayed=[]
    for condition,read,comp,access,preserve,reliable in rows:
        slots=re.findall(r'(\d)/5',read)
        read_cell=(r'$\checkmark$ '+r'$\cdot$'.join(x+'/5' for x in slots)
                   if slots else '–')
        seed_count=re.search(r'(\d)/3',comp)
        comp_cell=('–' if comp.startswith('not established') else
                   (r'$\checkmark$' if comp.startswith('supported') else r'$\times$'))
        if seed_count:comp_cell+=' '+seed_count.group(0)
        if '1,555' in comp:
            local_counts=[int(x.replace(',','')) for x in re.findall(r'\d[\d,]*',comp)]
            comp_cell+=r' $'+str(sum(x==1555 for x in local_counts[:-1]))+r'/3^{\ell}$'
        access_cell=(r'$\checkmark^{D}$' if access.startswith('supported by design') else
                     r'$\checkmark^{I}$' if access.startswith('demonstrated by matched') else '–')
        preserve_cell=(r'$\checkmark^{f}$' if preserve.startswith('supported (supplier') else
                       r'$\checkmark^{b}$' if preserve.startswith('supported') else
                       r'$\times$' if preserve.startswith('not supported') else '–')
        passed=re.match(r'(\d)/3',reliable)
        prediction_cell=((r'$\checkmark$' if int(passed.group(1)) else r'$\times$')+' '+passed.group(0)
                         if passed else '–')
        displayed.append([condition,read_cell,comp_cell,access_cell,preserve_cell,prediction_cell])
    caption=('Five achievements, original law. '+r'$\checkmark$ supported; $\times$ not supported; '
             '– not established: available evidence does not establish this achievement. '
             'Fractions are seeds passing out of three, except recoverability: supported slots out of five in seed order 0/1/2. '
             r'Access: $D$ by design (exact sums supplied); $I$ demonstrated by a matched connection intervention. '
             'Complete scope, counts and controls: Supplement Table S1.')
    note=('Raw-carrier linear readers: 512 held-out boards/slot. Computation: the audited sums output, exact vectors on rendering 0 (24,435 boards); '
          r'$\ell$: 1,555 local histories. The connection intervention does not establish selective use. '
          r'$f$: frozen supplier; $b$: blocked-gradient control. Frozen preservation is design-limited.')
    # The full glossary label receives half the width; no tiny type or resizebox.
    widths=[2.5,.91,.78,.43,.72,.74]
    fmt='@{}'+''.join(r'>{\raggedright\arraybackslash}p{'+f'{w:.3f}in'+'}' for w in widths)+'@{}'
    lines=['% Built from the same scoped evidence as Supplement Table S1.',r'\begin{table}[tb]',r'\centering',
           r'\caption{'+caption+r'}\label{tab:table1}',
           r'\begingroup\fontsize{8}{9.5}\selectfont\setlength{\tabcolsep}{3pt}\emergencystretch=1em\hyphenpenalty=10000\exhyphenpenalty=10000',
           r'\begin{tabular}{'+fmt+'}',r'\toprule',
           ' & '.join(r'\textbf{'+tex(h)+'}' for h in headers)+r' \\',r'\midrule']
    for row in displayed:
        lines.append(tex(row[0])+' & '+' & '.join(row[1:])+r' \\')
    lines += [r'\bottomrule',r'\end{tabular}',r'\par\smallskip',
              r'\begin{minipage}{\textwidth}\textit{Note.} '+note+r'\end{minipage}',r'\endgroup',r'\end{table}','']
    path=ctx.root/'paper/tables/table1.tex';path.write_text('\n'.join(lines))
    ctx.save_receipts('table1','tables',caption,{'headers':headers,'rows':rows,
        'displayed_headers':headers,'displayed_rows':displayed,'detailed_file':None,'note':note,
        'font_pt':8,'width_inches':sum(widths)+30/72.27,'layout':'single-page compact float',
        'float_display':'symbols compress the full evidence-derived cells; all counts retained in S1'})
    return {'name':'table1','file':'tables/table1.tex','caption':caption}


def full_table2(ctx):
    ctx.begin(); rows = []
    selections = {8: ["raw_only", "a_only", "dual"], 10: ["free", "free_a", "a_forced"],
                  12: ["a_target", "a_supplied"], 13: ["disconnected", "frozen", "live", "exact", "numerical"]}
    for n, wanted in selections.items():
        for key, r in sorted(ctx.sources["control"][str(n)].items(),key=lambda p:info(n,*p)):
            condition, law, seed = info(n,key,r)
            if law != "original" or condition not in wanted: continue
            v = endpoint(ctx,n,key,r)
            rows.append([f"r{n} {condition_name(condition)} / {seed}", v['passed'], v['KL'], v['misreads'],
                         v['short'], v['long'], v['label']])
    floor = ctx.ref("calibration","8","calibration","B","original","current_board_null")
    rows += [["r8 board-only control", floor["B_pass"], floor["natural_excess_KL_bits"], None, None,
              floor["mode_law"]["maximum_TV"], "null, calibration"],
             ["exact task oracle", True, 0, 0, 0, 0, "ceiling, not trained"]]
    return write(ctx,"table2_full","Access and supplied sums: complete per-seed comparison",
        ["study / condition / seed","B pass","natural KL (bits)","misreads (boards)","short TV max","long TV max*","endpoint label"],rows,
        "Every seed is explicit; compare access variants within r13 and supplied versus target sums within r12. "
        "Across studies these are historical, not matched comparisons; r10 is a different all-slots task. "
        "Counts use rendering 0 where recorded; missing census counts are not zero. *r8 reports full-law maximum, "
        "r10 law-row maximum, r12/r13 N3--N8 maximum. Original-task history TV bar is 0.02; r10 original-law law-row bar is 0.05, equal-law 0.02. "
        "Finite KL/TV use five significant digits; counts are exact. A pass is not correctness everywhere.",
        [1.4,.43,.78,.65,.66,.66,1.1])


def table2(ctx):
    ctx.begin();rows=[]
    for n,conditions in ((8,('raw_only','a_only','dual')),(10,('free','free_a','a_forced')),
                         (12,('a_target','a_supplied')),(13,('disconnected','frozen','live','exact','numerical'))):
        for cond in conditions:
            runs=sorted((info(n,k,r)[2],k,r) for k,r in ctx.sources['control'][str(n)].items() if info(n,k,r)[:2]==(cond,'original'))
            views=[endpoint(ctx,n,k,r) for s,k,r in runs]
            rows.append([f'r{n}: '+condition_name(cond),[v['KL'] for v in views],[v['long'] for v in views],f"{sum(v['passed'] is True for v in views)}/3"])
    floor=ctx.ref('calibration','8','calibration','B','original','current_board_null')
    rows+=[['r8 board-only calibration',floor['natural_excess_KL_bits'],floor['mode_law']['maximum_TV'],'0/1'],['exact task oracle',0,0,'ceiling']]
    return write(ctx,'table2','Access does not guarantee registered reliability',
        ['condition','natural KL (bits)','law TV (maximum)','B passes'],rows,
        'Each vertically ordered triple is seeds 0/1/2, never a pooled mean. Compare within study; cross-study comparisons are historical. r8 full history maximum, r12/r13 long N3–N8 maximum: bar 0.02. '
        'r10 is a different task: 180 law rows, original bar 0.05 (equal bar 0.02). Natural panels: 5,000 episodes × 12 rounds. Complete per-seed failed bars, census support and labels: Supplement Table S2.',[2.0,1.7,1.8,.7])


def study_table(ctx,n):
    ctx.begin(); rows=[]
    for key, r in ctx.sources["control"][str(n)].items():
        cond, law, seed = info(n,key,r)
        if n==13 and r['run']['experiment']=='erosion':
            ctx.ref('control','13',key,'accuracy_curve');ctx.ref('control','13',key,'run')
            rows.append([condition_name(cond),law,seed,"not measured",None,None,"see erosion table",None,None]);continue
        v=endpoint(ctx,n,key,r)
        failed = [k for k,value in v['criteria'].items() if value is False]
        rows.append([condition_name(cond),law,seed,v['passed'],v['KL'],v['misreads'],
                     v['TV_errors'],v['long'],', '.join(failed) or v['label']])
    return write(ctx,f"appendix_B_r{n}",f"r{n} complete endpoint version matrix",
        ["condition","law","seed","B pass","KL bits","misreads","TV-error count","law TV max*","failed bars / label"],rows,
        "All recorded conditions and seeds, including equal-law controls; no endpoint is selected. "
        "Equal-law category signatures are undefined, not zero. Five significant digits for continuous values. "
        "*Full-law / long / law-row support follows Table 2. Exact-oracle errors are zero; matched initial "
        "controls and complete deciding-function calibration are in Appendix C. Census counts are rendering 0; "
        "all four renderings and saved-r9 counts are in the census table. r11 reports B_law.maximum_TV on all history cases. Missing measurements stay not recorded.",
        [1.03,.40,.29,.39,.58,.55,.57,.57,1.30])


def leaves(value, path=()):
    if isinstance(value,dict):
        for key,child in value.items(): yield from leaves(child,(*path,key))
    elif isinstance(value,list) and any(isinstance(v,(dict,list)) for v in value):
        for j,child in enumerate(value): yield from leaves(child,(*path,j))
    else: yield path,value


def settings_table(ctx,n):
    ctx.begin()
    if n==9:
        ctx.ref('control','9','raw_only_seed0','source')
        rows=[["type","Read-only diagnosis of saved r8 networks; no updates"],
              ["scope","Completed boards, clear-neutral runs and failing saved histories; per-seed support is retained below"]]
    else:
        reg=ctx.registered(n);rows=[]
        skip={"source_identities","source_files","claims_verbatim","readings","readings_verbatim","registration_sha256",
              "A_source","frozen_A_source","Gate_A_sha256","calibration","sources","implementation_sources"}
        for path,v in leaves(reg):
            if not path or path[0] in skip or any('sha256' in str(k) or 'hash' in str(k) for k in path):continue
            if isinstance(v,str) and len(v)>700:continue
            if isinstance(v,list) and len(v)>36:continue
            if path[0]=='conditional_frequency_table':continue
            rows.append(['/'.join(map(str,path)), v if not isinstance(v,list) else json.dumps(v)])
    return write(ctx,f"prepared_r{n}",f"r{n} sampling, training and registered criteria",["registered property","value"],rows,
        "Read directly from the hash-verified registration (r9: read-only scope). This table retains declared "
        "sampling, truncation, coverage, loss, settings and criteria, not inferred hardware. Long verbatim "
        "readings, r10's full rational conditional-frequency table and source identities remain in the "
        "manifest-bound registration; r10 is a different task.",[2.0,3.9])


def census(ctx):
    ctx.begin(); rows=[]
    for n in (9,11,12,13):
        for key,r in ctx.sources['control'][str(n)].items():
            cond,law,seed=info(n,key,r)
            if n==9:
                data=ctx.ref('control','9',key,'board_effects'); entries=[(0,{'boards':24435,
                    'categorical_misreads':sum(v['signature_misreads'] for v in data['by_slot1_sum_twelfths'].values()),
                    'above_0_02_TV':data['above_TV_limit']})]
            elif n==11:
                d=ctx.ref('control','11',key,'census_renderings');entries=list(enumerate(d))
            elif n==12:
                d=ctx.ref('control','12',key,'census_all_four_renderings_and_r9')
                entries=[(0,d['registered_rendering']),*[(j+1,v) for j,v in enumerate(d['additional_fixed_renderings'])]]
            elif 'census_counts' in r:
                entries=list(enumerate(ctx.ref('control','13',key,'census_counts')))
            else:continue
            for j,v in entries:
                rows.append([f'r{n} {condition_name(cond)} / {seed}',law,j,v.get('boards',24435),v.get('categorical_misreads'),
                    v.get('prediction_TV_errors',v.get('above_0_02_TV')),str(v.get('cutoff',{})) or 'see per-sum source'])
    return write(ctx,'appendix_B_census','Census measures remain distinct',["run / seed","law","rendering","boards","misreads","TV errors","cutoff support"],rows,
        "Counts, not percentages; original/equal laws separate. Misreads are undefined in equal-law controls. "
        "The cutoff band contains 930 boards and its complement 23,505. Complete per-sum and saved-r9 "
        "records remain hash-bound in the source tables; no rendering is substituted for another.",[1.35,.4,.5,.5,.5,.55,2.1])


def probes(ctx):
    ctx.begin(); rows=[]
    for n in (8,10):
        for key,r in ctx.sources['control'][str(n)].items():
            cond,law,seed=info(n,key,r)
            if n==10:
                for p in ctx.ref('control','10',key,'probe_summary'):
                    rows.append([f'r{n} {condition_name(cond)}/{seed} {law}',f"{p['site']} {p['family']} {p['task']} s{p['slot']+1}",
                        p['before'],f"{p['correct']}/{p['total']}",p['endpoint'],p['majority_floor'],p.get('shuffled_accuracy'),
                        p['positive_accuracy'],p['paired_CI95'],reader_status(p['family'],p['fits_converged'])])
            else:
                if 'probe_table' not in r: continue
                pts=ctx.ref('control','8',key,'probe_table');before,end=pts[0],pts[-1]
                floors=ctx.ref('calibration','8','calibration','probe','oracle','floors')
                for site in ('raw','upper'):
                    for family in ('linear','mlp64'):
                        for j,gain in enumerate(end['gain'][site][family]):
                            # Preserve the precision of the historical table;
                            # the outline uses its separate unrounded authority.
                            oracle=ctx.ref('calibration','8','calibration','probe','oracle','sites',site,family,j,'accuracy')
                            initial = before['heldout'][site][family][j]
                            final=end['heldout'][site][family][j]
                            rows.append([f'r8 {condition_name(cond)}/{seed} {law}',f'{site} {family} s{j+1}', initial,'512 sampled boards',final,
                                floors[j]['majority_accuracy'],floors[j]['shuffled_accuracy'],oracle,gain['gain_CI95'],reader_status(family,gain['fits_converged'])])
    return write(ctx,'appendix_E_probes','Full probes: carrier, reader, controls and paired intervals',
        ['run / seed / law','reader / slot','update 0','support','20k','majority','shuffled','oracle','gain CI95','converged'],rows,
        "Every slot and seed for both carriers and readout families in r8/r10; 512 held-out board identities "
        "per cell. r8 historical heldout fields retain their saved five-decimal precision; raw-only "
        "outline endpoints use the ledger's unrounded fields. Gain intervals are paired board-bootstrap "
        "intervals, not endpoint intervals or seed variation. Rare r10 values remain outside registered "
        "readability support; see the per-value coverage table. MLP fits have a fixed budget, not "
        "a solver-convergence assessment.",[1.1,.8,.40,.68,.4,.4,.4,.4,.9,.42])


def calibration(ctx):
    ctx.begin();rows=[]
    for n in (8,10,11,12,13):
        d=ctx.sources['calibration'][str(n)]['calibration']
        for key,value in d.items():
            if ('calibration',str(n),'calibration',key) not in ctx.bindings:continue
            for p,v in leaves(value):
                # Per-presentation arrays belong in the full archived records,
                # not a multi-megabyte manuscript table. Preserve only named
                # scalar summaries here; per-slot floors have their own table.
                if len(p)>6 or any(isinstance(k,int) or str(k).isdigit() for k in p):continue
                if any(k in ('predictions','labels','records','positions','probabilities') for k in p):continue
                if isinstance(v,bool) or (isinstance(v,(int,float)) and any(word in '/'.join(map(str,p)).lower()
                     for word in ('accuracy','correct','total','count','tv','kl','pass','pairs','converg','support'))):
                    ctx.ref('calibration',str(n),'calibration',key,*p)
                    rows.append([f'r{n}',key+' / '+' / '.join(map(str,p)),v])
    return write(ctx,'appendix_C_calibration','Deciding-function calibration: positives, negatives and support',
        ['study','condition / deciding quantity','recorded value'],rows,
        "Named scalar calibration summaries, with exact counts and original/equal "
        "law-aware decisions. A successful calibration is not a successful trained model. Unsupported/empty "
        "nulls do not pass; the r10 trained positive is a fixed-endpoint condition. Floors and exact-oracle "
        "ceilings are retained in the named condition rows. Per-presentation and per-slot arrays remain "
        "in the hash-verified full calibration records; slot floors are in the probe table. "
        "Five significant digits for continuous values.",[.45,4.4,1.05])


def geometry_table(ctx):
    ctx.begin();entry=ctx.evidence.entries['repo/reports/phase11/oldgame_memory/multiround/study_r13_mechanism/aggregate.json']
    d=ctx.manifest_json(entry);rows=[]
    for r in d['supplementary']['rows']:
        for m in r['measured']:
            rows.append([f"{condition_name(r['run']['condition'])} / {r['run']['seed']}",r['step'],m['sums'],
                f"{m['train_pairs']}/{m['heldout_pairs']}",f"{m['reader']['correct']}/{m['reader']['total']}",
                m['reader']['cross_entropy_nats'],m['label_permutation_floor']['accuracy'],
                m['discrimination']['pass'],m['distance_mean'],m['rerender_distance_mean']])
    ctx.ref(entry['id'],'supplementary','rows')
    return write(ctx,'appendix_E_geometry','Supplementary cutoff discrimination and geometry support',
        ['condition / seed','update','pair','fit/eval pairs','correct/total','loss nats','shuffled accuracy','decision','distance','rerender distance'],rows,
        "Fixed, separately bound supplementary pairs: 135/150 for 12/13 and 12/13 for 23/24. "
        "No resampling, network updates or endpoint selection. Distances are descriptive, not a proof of "
        "absence; the calibrated decision also requires convergence and log-loss separation. Exact ceiling "
        "is accuracy 1/loss 0; constant balanced floor is 0.5/ln 2. Original support gaps (578 missing rows) "
        "remain recorded in the original geometry-support table.",[1.08,.40,.4,.55,.65,.48,.52,.47,.53,.82])


def erosion(ctx):
    ctx.begin();rows=[]
    for key,r in ctx.sources['control']['13'].items():
        if r['run']['experiment']!='erosion':continue
        raw,eid=ctx.referenced(ctx.ref('control','13',key,'records'))
        for j,p in enumerate(raw):
            ctx.ref(eid,j,'step');ctx.ref(eid,j,'local','correct');ctx.ref(eid,j,'cumulative_path')
            rows.append([condition_name(r['run']['condition']),r['run']['seed'],p['step'],p['local']['correct'],
                         p['local']['total'],p['cumulative_path']])
    return write(ctx,'appendix_D_erosion','r13 erosion: exact starts, first updates, minima and endpoints',
        ['condition','seed','update','correct','total histories','cumulative movement'],rows,
        "Complete updates 0--200 remain in the detailed file; no interpolation or selected checkpoint. Update 0 is the matched "
        "exact-A reference; the oracle is 1,555/1,555. Blocked prediction gradients form the separate decay "
        "control, excluded from active-arm movement intersections.",[1.0,.5,.6,.6,1.1,2.1])


def history(ctx):
    ctx.begin();rows=[]
    for h in ctx.manifest['study_history']:
        rows.append([f"r{h['study']}",h['hardware'],len(h['versions_and_specifications']),h['interpretation']])
    ctx.receipts.append({'source':'evidence_manifest','pointer':['study_history'],'value':ctx.manifest['study_history'],
                         'sha256':__import__('asset_inputs').digest(ctx.manifest['study_history']),'ledger_ids':['study_inventory']})
    return write(ctx,'appendix_A_history','Registered studies, corrected audits and supplementary analyses',
        ['study','recorded hardware','specification versions','historical scope'],rows,
        "r8/r9 are CPU-era; later GPU execution metadata are kept distinct. Counts inventory manifest "
        "authorities, not independent experiments. Exact historical commands/hardware absent from run "
        "summaries remain unknown; instruction files are not proof of execution.",[.4,2.0,.7,2.8])


def compute(ctx):
    ctx.begin();rows=[]
    for c in ctx.ledger['claims']:
        if c['category']=='compute_measurement':
            rows.append([c['study'],c['id'],c['rebuilt_value'],c['units'],c['scope']])
    ctx.receipts.append({'source':'claims_ledger','pointer':['claims'],'ledger_ids':[r[1] for r in rows]})
    return write(ctx,'appendix_F_compute','Recorded compute and reproduction measurements',
        ['study','evidence / entry','recorded value','units','scope'],rows,
        "Recorded measurements only; grouped process timings are not summed as independent training "
        "time. Unknown historical processor/GPU models remain unknown. Counts and sizes are exact, "
        "continuous values use five significant digits. Hashes, commands and the minimal archive inputs "
        "are in the portable manifest; no new training or inference occurred for these assets.",[.4,1.8,1.1,.9,1.7])


def later_probes(ctx,n):
    ctx.begin();rows=[]
    for key,r in ctx.sources['control'][str(n)].items():
        field='probe_changes' if n==11 else 'probes'
        p=ctx.ref('control',str(n),key,field);cond,law,seed=info(n,key,r)
        for site,readers in p.items():
            for family,targets in readers.items():
                for task,slots in targets.items():
                    for v in slots:
                        rows.append([f'{condition_name(cond)}/{seed} {law}',f"{site} {family} {task} s{v['slot']}",
                            f"{v['update0_counts']['correct']}/{v['update0_counts']['total']}",
                            f"{v['endpoint_counts']['correct']}/{v['endpoint_counts']['total']}",
                            v['majority_floor'],v['shuffled_floor'],v['oracle_floor'],v['paired_CI95'],reader_status(family,v['converged'])])
    return write(ctx,f'appendix_E_r{n}_probes',f'r{n} all recorded probes',
        ['condition / seed / law','carrier / reader / target / slot','start count','end count','majority','shuffled','oracle','gain CI95','converged'],rows,
        "Training-only fitting; board-identity held-out scoring. All slots, both carriers and both readout "
        "families; sum36 and category3 are separate targets. Counts retain each cell's own denominator. "
        "Intervals are saved paired board-bootstrap gain intervals, not across-seed bands. Calibration "
        "floors do not imply predictive use; linear convergence is necessary, not sufficient, for "
        "readability. MLP convergence is not assessed under its fixed training budget.",
        [1.08,1.03,.58,.58,.4,.4,.4,1.0,.43])


def support_counts(ctx):
    ctx.begin();rows=[]
    for n in (10,11,12,13):
        for key,r in ctx.sources['control'][str(n)].items():
            cond,law,seed=info(n,key,r);who=f'r{n} {condition_name(cond)}/{seed} {law}'
            for field in ('A_interface','A_components','A_exact_counts','sums','supplier','A_local_histories',
                          'local_history_counts','saved_r9'):
                if field not in r or r[field] is None:continue
                v=ctx.ref('control',str(n),key,field)
                if isinstance(v,dict):
                    for path,value in leaves(v):
                        if isinstance(value,(int,float)) and not isinstance(value,bool):
                            rows.append([who,field+' / '+' / '.join(map(str,path)),value])
                        elif isinstance(value,list) and all(isinstance(x,int) for x in value):
                            for j,x in enumerate(value):rows.append([who,field+' / '+' / '.join(map(str,path))+f' / slot {j+1}',x])
            census=r.get('board_census',r.get('census_all_four_renderings_and_r9'))
            if census and 'saved_r9' in census:
                name='board_census' if 'board_census' in r else 'census_all_four_renderings_and_r9'
                v=ctx.ref('control',str(n),key,name,'saved_r9')
                for path,x in leaves(v):
                    if isinstance(x,(int,float)) and not isinstance(x,bool):rows.append([who,'saved r9 / '+' / '.join(map(str,path)),x])
    return write(ctx,'appendix_B_support','Exact support: sums, supplier, local histories and saved-r9 cases',
        ['condition / seed / law','measured quantity','count / recorded value'],rows,
        "Slot components and whole-vector counts are separate. Denominators follow the named quantity; "
        "a frozen supplier is not the same as an approximate sums output. Saved-r9 rows are constructed "
        "historical failing renderings, not new random samples. Missing local-history audits are not zero errors.",[1.7,3.4,.8])


def laws(ctx):
    ctx.begin();rows=[]
    for n in (10,11,12,13):
        for key,r in ctx.sources['control'][str(n)].items():
            cond,law,seed=info(n,key,r);who=f'r{n} {condition_name(cond)}/{seed} {law}'
            if n==10:
                data=ctx.ref('control','10',key,'law_cases')
                for case,v in data.items():
                    if isinstance(v,dict) and 'maximum_TV' in v:
                        rows.append([who,case,v.get('rounds'),v.get('mean_TV'),v['maximum_TV'],v.get('KL_bits')])
            elif n==13:
                if r['run']['experiment']=='erosion':continue
                audit,eid=ctx.referenced(r['audit_references'][-1]);data=ctx.ref(eid,'audit','mode_law','cases')
                for case,v in data.items():rows.append([who,case,v.get('count'),v.get('mean_TV'),v['maximum_TV'],None])
            else:
                field='B_law' if n==11 else 'prediction_checks'
                data=r.get('B_law',r.get('prediction_checks',{}).get('mode_law'))
                if data is None:
                    # Both studies retain the case rows inside the law-panel view.
                    data=r['law_panels'].get('cases',{})
                else:data=data.get('cases',{})
                if field=='B_law':ctx.ref('control',str(n),key,field)
                else:ctx.ref('control',str(n),key,'law_panels')
                for case,v in data.items():
                    if isinstance(v,dict) and 'maximum_TV' in v:rows.append([who,case,v.get('count'),v.get('mean_TV'),v['maximum_TV'],None])
    return write(ctx,'appendix_B_laws','Continuous law errors, by case',
        ['run / seed / law','case','presentations','mean TV','max TV','KL bits'],rows,
        "L/H and N1--N2 form the short panel; N3--N8 form the long panel. The r12 long panel is trained, "
        "not unseen-length extrapolation. The original-task TV bar is 0.02; r10 original-law law rows use 0.05 and equal-law rows 0.02. The exact ceiling is zero. "
        "r10 law rows are a different all-slots task, not the same denominator as r8/r11--r13 histories. "
        "Mean TV is not reconstructed when absent from the saved summary.",[1.65,1.35,.70,.65,.65,.9])


def original_geometry(ctx):
    ctx.begin();rows=[];missing=0
    for key,r in ctx.sources['control']['13'].items():
        if not r.get('geometry'):continue
        data=ctx.ref('control','13',key,'geometry')
        for audit in data:
            step=audit['step']
            rows.append([condition_name(r['run']['condition']),r['run']['seed'],step,'all unsupported',
                audit['missing_support_rows'],'MISSING_SUPPORT',None,None,None,None])
            for m in audit['measured']:
                rows.append([condition_name(r['run']['condition']),r['run']['seed'],step,m['sums'],
                    f"{m['train_pairs']}/{m['heldout_pairs']}",f"{m['reader']['correct']}/{m['reader']['total']}",
                    m['reader']['cross_entropy_nats'],m['discrimination']['pass'],m['distance_mean'],m['rerender_distance_mean']])
            for m in audit.get('cutoff_missing',[]):
                missing+=1
                rows.append([condition_name(r['run']['condition']),r['run']['seed'],step,m['sums'],
                    f"{m['train_pairs']}/{m['heldout_pairs']}",'MISSING_SUPPORT',None,None,None,None])
    return write(ctx,'appendix_E_original_geometry','Original fixed-pair support and discrimination',
        ['condition','seed','update','pair','fit/eval','correct/total','loss nats','decision','distance','rerender distance'],rows,
        "Original registered pairs at 0/5k/20k; missing support is not a successful negative. Cutoff pairs "
        "12/13 and 23/24 with zero held-out support are retained in the source's cutoff_missing rows. "
        "Each recorded geometry audit has 578 missing-support pair rows; repeated audits are not "
        "independent support. The supplementary panel is separate and does not "
        "replace them. Distances and rendering variation are descriptive. Exact accuracy ceiling is 1 "
        "and balanced constant/shuffled controls calibrate the discrimination scorer.",[1.10,.30,.40,.45,.65,.75,.55,.45,.6,.65])


def interchange(ctx):
    ctx.begin();rows=[]
    for key,r in ctx.sources['control']['10'].items():
        cond,law,seed=info(10,key,r)
        data=ctx.ref('control','10',key,'interchange_summary');decisions=ctx.ref('control','10',key,'patches')
        for slot,v in data.items():
            d=decisions[slot]
            rows.append([f'{condition_name(cond)}/{seed} {law}',int(slot)+1,v['eligible_pairs'],v['evaluated_pairs'],
                v['accurate_unpatched_pairs'],v['donor_follow_count'],v['donor_follow_CI95'],
                v['other_slot_probe_changes'],d['trained_positive']['status'],d['negative_calibration']['status'],d['status']])
    return write(ctx,'appendix_C_interchange','Interchange support, calibration and selectivity are separate',
        ['arm / seed / law','slot','eligible','fixed pairs','accurate','follow','CI95','other-slot changes','positive','negative','decision'],rows,
        "Fixed prediction-independent pair lists, 1,024 per slot; no resampling. Conditional donor-follow "
        "uses accurate unpatched pairs as its denominator, not all eligible pairs. Positive validity, "
        "supported negative calibration and zero-spillover selectivity are separate gates. The oracle "
        "ceiling is exact donor-follow with zero other-slot changes; no-op/shuffled floors are in Table C "
        "calibration. Equal-law rows are control-only. a_forced's shuffled raw negative is not applicable.",
        [1.05,.28,.4,.4,.45,.4,.65,.45,.63,.63,.78])


def coverage(ctx):
    ctx.begin();rows=[]
    for key,r in ctx.sources['control']['10'].items():
        cond,law,seed=info(10,key,r)
        currents=ctx.ref('control','10',key,'observed_current_query_value_counts')
        memories=ctx.ref('control','10',key,'observed_remembered_query_value_counts')
        for slot,(now,past) in enumerate(zip(currents,memories)):
            for value,(a,b) in enumerate(zip(now,past)):
                rows.append([f'{condition_name(cond)}/{seed} {law}',slot+1,value,a,b])
    return write(ctx,'appendix_B_r10_coverage','Current versus remembered value exposure',
        ['arm / seed / law','queried slot','value index','current occurrences','remembered occurrences'],rows,
        "Actual online-training exposures, not independent sample sizes or inference counts. The current "
        "and remembered value arrays are separate. Readability support is board-identity held out; values "
        "missing from the registered fit/score panel, especially 28--36, are supplementary rendering support, "
        "not established by the registered probe gain.",[1.9,.6,.6,1.4,1.4])


def compact_summary(ctx,letter):
    ctx.begin();rows=[]
    if letter=='A':
        for h in ctx.manifest['study_history']:
            rows.append([f"r{h['study']}",h['hardware'],len(h['versions_and_specifications'])])
        ctx.receipts.append({'source':'evidence_manifest','pointer':['study_history'],'value':ctx.manifest['study_history'],
            'sha256':__import__('asset_inputs').digest(ctx.manifest['study_history']),'ledger_ids':['study_inventory']})
        headers=['study','recorded compute','specification versions']
    elif letter=='B':
        for n in (8,10,11,12,13):
            views=[endpoint(ctx,n,k,r) for k,r in ctx.sources['control'][str(n)].items() if
                info(n,k,r)[1]=='original' and not(n==13 and r['run']['experiment']=='erosion')]
            rows.append([f'r{n}',sum(v['passed'] is True for v in views),len(views),
                         '0.05 (180 law rows)' if n==10 else '0.02 (576 history endpoints)'])
        headers=['study','registered passes','original-law runs','law TV bar / support']
    elif letter=='C':
        from table_summaries import calibration_rows
        # Every original-law B positive and its null; not the first pass flags.
        rows=[r for r in calibration_rows(ctx) if r[1]=='original']
        headers=['study','law','positive / null','deciding quantity','pass','support','measured value']
    elif letter=='D':
        for cond in ('adam','reduced','sgd','blocked'):
            counts=[]
            for seed in range(3):
                k=next(k for k,r in ctx.sources['control']['13'].items() if r['run']==dict(experiment='erosion',condition=cond,law='original',seed=seed))
                raw,eid=ctx.referenced(ctx.ref('control','13',k,'records'))
                p=next(j for j,r in enumerate(raw) if r['step']==1)
                counts.append(ctx.ref(eid,p,'local','correct'))
            rows.append([condition_name(cond),' / '.join(map(str,counts)),1555])
        headers=['update-1 condition','correct counts (seeds 0/1/2)','histories per seed']
    elif letter=='E':
        for n,cond in ((11,'dose_dose100'),(12,'a_target')):
            for seed in range(3):
                k=f'{cond}_original_seed{seed}'
                field='probe_changes' if n==11 else 'probes'
                v=ctx.ref('control',str(n),k,field,'raw','linear','sum36',0)
                rows.append([f'r{n} '+condition_name(cond),seed,v['endpoint_counts']['correct'],512,v['paired_CI95'],v['converged']])
        headers=['raw linear slot-1 sums reader','seed','correct','boards','gain CI95','converged']
    else:
        from table_summaries import compute_rows
        # Two explicitly scoped examples: r8 CPU endpoints and the r13 erosion
        # series. Include every original-law condition/seed in those scopes.
        groups=defaultdict(list)
        for r in compute_rows(ctx):
            if r[0] in ('r8','r13') and r[2]=='elapsed_seconds' and r[1].endswith('original'):
                if r[0]=='r13' and not r[1].startswith(('AdamW','reduced-lr AdamW','SGD','blocked prediction gradient')):continue
                groups[r[0],r[1].rsplit(' / ',1)[0]].append(r)
        rows=[[n,cond,number([r[3] for r in sorted(v,key=lambda x:x[1])]),
               'CPU endpoint' if n=='r8' else '200-update erosion; recorded execution', 'examples, not totals']
              for (n,cond),v in sorted(groups.items())]
        headers=['study','condition (all seeds)','seconds (0/1/2)','execution scope','aggregation']
    return write(ctx,f'compact_{letter}',f'Analytical appendix {letter}',headers,rows,
        'Exact recorded counts or decisions; no pooled reader accuracies. Complete support, settings, controls and per-seed records are in the numbered supplementary tables and released data.')


TABLES={'table1':table1,'table2':table2,'table1_full':full_table1,'table2_full':full_table2,'appendix_B_census':census,'appendix_E_probes':probes,
        'appendix_C_calibration':calibration,'appendix_E_geometry':geometry_table,'appendix_D_erosion':erosion,
        'appendix_A_history':history,'appendix_F_compute':compute}
TABLES.update({'appendix_E_r11_probes':lambda ctx:later_probes(ctx,11),
    'appendix_E_r12_probes':lambda ctx:later_probes(ctx,12),'appendix_B_support':support_counts,
    'appendix_B_laws':laws,'appendix_E_original_geometry':original_geometry})
TABLES.update({'appendix_C_interchange':interchange,'appendix_B_r10_coverage':coverage})
for _n in (8,9,10,11,12,13):
    TABLES[f'appendix_B_r{_n}']=lambda ctx,n=_n:study_table(ctx,n)
    TABLES[f'prepared_r{_n}']=lambda ctx,n=_n:settings_table(ctx,n)
for _letter in 'ABCDEF':TABLES[f'compact_{_letter}']=lambda ctx,l=_letter:compact_summary(ctx,l)


# Fixed public numbering; tables are exhaustive only in the audit supplement.
SUPPLEMENT_TABLES=['table1_full','table2_full','appendix_A_history',
    *[name for n in (8,9,10,11,12,13) for name in (f'prepared_r{n}',f'appendix_B_r{n}')],
    'appendix_B_census','appendix_B_support','appendix_B_laws','appendix_B_r10_coverage',
    'appendix_C_calibration','appendix_C_interchange','appendix_E_probes','appendix_E_r11_probes',
    'appendix_E_r12_probes','appendix_E_original_geometry','appendix_E_geometry','appendix_D_erosion','appendix_F_compute']
