"""Predeclared analytical reductions; complete rows remain in released JSON.

No selection by position. Studies, quantities, conditions and checkpoints are
named below. Ranges describe cells, never a pooled estimate or confidence band.
"""
from collections import defaultdict
import hashlib
import gzip
from pathlib import Path
import re

from asset_inputs import number
from build_ledger import canonical
from condition_labels import condition_name


def span(values):
    values=[v for v in values if isinstance(v,(int,float)) and not isinstance(v,bool)]
    return 'not recorded' if not values else number(min(values))+' – '+number(max(values))


def publish_detail(ctx,name,headers,rows):
    folder=ctx.root/'paper/data/release';folder.mkdir(parents=True,exist_ok=True)
    payload={'schema':'jagged-table-rows-v1','table':name,'headers':headers,'rows':rows,
             'ledger_sha256':hashlib.sha256((ctx.root/'paper/notes/claims_ledger.json').read_bytes()).hexdigest(),
             'source_bindings':[{'source':r['source'],'pointer':r['pointer'],'sha256':r.get('sha256'),
                                 'ledger_ids':r.get('ledger_ids',[])} for r in ctx.receipts]}
    path=folder/(name+'.json.gz')
    path.write_bytes(gzip.compress(canonical(payload).encode(),mtime=0))
    return {'path':str(path.relative_to(ctx.root/'paper')),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,
            'rows':len(rows)}


def calibration_rows(ctx):
    """Positive and matched null for each law through the B deciding functions.

    Also show the supported r10 no-op/shuffled/selectivity calibration. Selecting
    all named positives avoids privileging one interface or the equal law.
    """
    rows=[]
    for n in (8,10,11,12,13):
        if n==10:
            for law in ('original','equal'):
                for control in ('exact_oracle','mode_blind','untrained'):
                    d=ctx.ref('calibration','10','calibration','decisions',law,control)
                    maximum=ctx.ref('calibration','10','calibration',control,law,'law_rows','maximum_TV')
                    rows.append(['r10',law,control,'B deciding criteria',all(v for k,v in d.items() if k!='bounds'),
                                 '180 law rows',maximum])
            data=ctx.ref('calibration','10','calibration','intervention_calibration_status')
            for slot,d in data.items():
                rows.append(['r10','original',f'slot {int(slot)+1}: hard / rotated / no-op / shuffled',
                    'donor-follow and selectivity',d['passes'],1024,
                    number([d['rates'][k] for k in ('hard','rotated','noop','shuffled')])])
            data=ctx.sources['calibration']['10']['calibration']['interchange']['contaminating']['slots']
            changes=[ctx.ref('calibration','10','calibration','interchange','contaminating','slots',slot,'other_slot_probe_changes')
                     for slot in data]
            rows.append(['r10','original','planted contamination','other-slot changes detected',
                all(v>0 for v in changes),1024,number(changes)])
        else:
            for law in ('original','equal'):
                d=ctx.sources['calibration'][str(n)]['calibration']['B'][law]
                for control,v in d.items():
                    base=('calibration',str(n),'calibration','B',law,control)
                    cases=ctx.ref(*base,'mode_law','cases') if 'mode_law' in v else {}
                    support=sum(c['count'] for c in cases.values()) if cases else '576 history endpoints'
                    passed=ctx.ref(*base,'B_pass' if 'B_pass' in v else 'pass')
                    maximum=ctx.ref(*base,'law_maximum_TV') if 'law_maximum_TV' in v else ctx.ref(*base,'mode_law','maximum_TV')
                    rows.append([f'r{n}',law,control,'B deciding criteria',passed,support,maximum])
        if n in (8,10,11,12):
            field='probes' if n==12 else 'probe'
            for control in ('oracle','update0' if n==8 else 'untrained'):
                base=('calibration',str(n),'calibration',field,control)
                d=ctx.sources['calibration'][str(n)]['calibration'][field][control]
                data=d['sites']['raw']['linear']
                suffix=('sites','raw','linear')
                if n!=8:
                    task='sum' if n==10 else 'sum36';data=data[task];suffix=(*suffix,task)
                observed=[{k:ctx.ref(*base,*suffix,j,k) for k in ('accuracy','converged','correct')}
                          for j in range(len(data))]
                passed=all(v['accuracy']>=.99 and v['converged'] for v in observed)
                rows.append([f'r{n}','both',control,'raw linear sum calibration (≥0.99; convergence)',
                    passed,ctx.ref(*base,'heldout_boards'),number([v['correct'] for v in observed])+' / 512'])
    return rows


def compute_rows(ctx):
    """All recorded training timings, with the actual run and execution scope.

    Per-update/group/audit quantities remain distinct. Repeated group timings
    are not added. This selects by quantity and scope, not first ledger rows.
    """
    rows=[]
    for c in ctx.ledger['claims']:
        if c['category']!='compute_measurement' or c['units']!='seconds':continue
        key=c['computation']['key']
        if key not in ('training_seconds','elapsed_seconds','elapsed_group_seconds','training_seconds_per_update'):continue
        entry=next((ctx.by_id[e] for e in c['evidence_ids'] if ctx.by_id[e]['archive_path'].endswith('/summary.json')),None)
        if entry is None:continue
        path=Path(entry['archive_path']);run=path.parent.name
        # Identify production endpoints separately from bounded smoke records.
        if not re.search(r'_seed[012]$',run):continue
        label=run
        match=re.match(r'(.+)_(original|equal)_seed([012])$',run)
        if match:
            cond,law,seed=match.groups()
            if c['study']==13:
                cond=re.sub(r'^(noise|access|encoding|erosion)_','',cond)
            label=condition_name(cond)+f' / {seed} {law}'
        rows.append([f'r{c["study"]}',label,key,c['rebuilt_value'],'recorded endpoint; not a study total'])
        ctx.receipts.append({'source':'claims_ledger','pointer':['claims',ctx.ledger['claims'].index(c)],
            'value':c,'sha256':__import__('asset_inputs').digest(c),'ledger_ids':[c['id']]})
    return sorted(rows,key=lambda r:(r[0],r[1],r[2]))


def analytical_rows(ctx,name,headers,rows,widths):
    """Reduce only declared dimensions; the JSON retains the unreduced rows."""
    if name=='table1_full':
        result=[]
        for r in rows:
            counts=re.findall(r'(?:not supported|supported):?\s+([0-5])/5(?:\s|;)',r[1])
            recovery='supported slots: '+' / '.join(x+'/5' for x in counts) if counts else (
                'slot 1; raw linear' if 'slots 1;' in r[1] else 'not established')
            comp=r[2].split(';')[0]
            result.append([r[0],recovery,comp,r[3],r[4],r[5]])
        return ['condition','recoverability','computation','access','preservation','reliable prediction'],result,[1.5,.95,.85,.85,.85,.85]
    if name.startswith('prepared_r'):
        # Settings, criteria, sampling and explicitly declared choices only;
        # exclude the detailed run registry and verbatim interpretation prose.
        result=[r for r in rows if r[0].split('/')[0] in
                ('settings','criteria','choices','probe_settings','linear_probe_settings','board_counts','type','scope')
                and len(str(r[1]))<=300]
        return headers,result,widths
    if name=='appendix_C_calibration':
        return ['study','law','positive / null','deciding quantity','pass','support','law max / rates'],calibration_rows(ctx),[.35,.4,1.35,1.1,.35,1.0,1.4]
    if name=='appendix_F_compute':
        groups=defaultdict(list)
        for r in compute_rows(ctx):groups[r[0],r[2]].append(r)
        result=[[n,k,len(v),span(r[3] for r in v),'endpoint examples, not summed group/study totals'] for (n,k),v in sorted(groups.items())]
        return ['study','recorded quantity','run records','seconds range','execution scope'],result,[.4,1.4,.6,1.0,2.4]
    if name=='appendix_B_census':
        groups=defaultdict(lambda:defaultdict(list))
        for r in rows:
            who,seed=r[0].rsplit(' / ',1);groups[who,r[1]][int(seed)].append(r)
        result=[[who,law,'; '.join('s'+str(s)+': '+span(r[4] for r in v) for s,v in sorted(seeds.items())),
                 '; '.join('s'+str(s)+': '+span(r[5] for r in v) for s,v in sorted(seeds.items()))]
                for (who,law),seeds in groups.items()]
        return ['condition','law','misread counts: range across renderings per seed','TV-error counts: range across renderings per seed'],result,[1.7,.4,2.0,2.0]
    if name=='appendix_B_support':
        # Preserve actual vectors/local audits/suppliers/r9 counts, not the
        # subsidiary accuracy percentages or per-category metadata arrays.
        result=[r for r in rows if re.search(r'(vector|local)',r[1],re.I) and
                re.search(r'/ (correct|total)$',r[1])]
        groups=defaultdict(list)
        for r in result:groups[r[0]].append(r)
        return ['run / seed / law','exact vector / local audited quantities'],[
            [who,'; '.join(r[1]+': '+number(r[2]) for r in v)] for who,v in groups.items()],[1.8,4.2]
    if name=='appendix_B_laws':
        groups=defaultdict(lambda:defaultdict(list))
        for r in rows:
            case=r[1];panel=('short L/H,N1–N2' if case.endswith('single_round') or case in ('N_run_1','N_run_2') else
                'long N3–N8' if case.startswith('N_run_') else case)
            match=re.match(r'(.+)/(\d+) (original|equal)$',r[0])
            if not match:raise ValueError('law run identity is not parseable')
            who,seed,law=match.groups();groups[who,law,panel][int(seed)].append(r)
        result=[]
        for (who,law,panel),seeds in groups.items():
            if panel=='long N3–N8':continue
            v=next(iter(seeds.values()))
            other=groups.get((who,law,'long N3–N8')) if panel=='short L/H,N1–N2' else None
            support=sum(r[2] for r in v if isinstance(r[2],int))
            means=span(r[3] for v in seeds.values() for r in v)
            maxima=number([max(r[4] for r in v) for s,v in sorted(seeds.items())])
            long_max=None
            if other:
                panel='short / long'
                support=str(support)+' / '+str(sum(r[2] for r in next(iter(other.values())) if isinstance(r[2],int)))
                means='short '+means+'; long '+span(r[3] for v in other.values() for r in v)
                long_max=number([max(r[4] for r in v) for s,v in sorted(other.items())])
            result.append([who+' '+law,panel,support,means,maxima,long_max])
        return ['condition / law','panel','presentations per seed','case-mean TV ranges (all seeds)','worst TV seeds 0/1/2','long worst TV seeds 0/1/2'],result,[1.6,.8,.7,1.2,.85,.85]
    if name=='appendix_B_r10_coverage':
        groups=defaultdict(list)
        for r in rows:groups[r[0]].append(r)
        result=[]
        for who,v in groups.items():
            by=[ [r for r in v if r[1]==slot] for slot in range(1,6)]
            result.append([who,number([sum(r[3] for r in s) for s in by]),
                number([sum(r[4] for r in s) for s in by]),
                number([sum(r[3]>0 for r in s) for s in by]),number([sum(r[4]>0 for r in s) for s in by])])
        return ['run / seed / law','current occurrences s1–s5','remembered occurrences s1–s5','current values covered','remembered values covered'],result,[1.8,1.3,1.3,.75,.75]
    if name=='appendix_C_interchange':
        groups=defaultdict(list)
        for r in rows:groups[r[0]].append(r)
        result=[]
        for who,v in groups.items():
            result.append([who,number([r[4] for r in v]),number([r[5] for r in v]),
                number([r[7] for r in v]),'; '.join(sorted(set(str(r[8]) for r in v))),
                '; '.join(sorted(set(str(r[10]) for r in v)))])
        return ['run / seed / law','accurate pairs s1–s5','donor-follow counts','other-slot changes','positive validity','use decision'],result,[1.75,.9,.9,.85,.85,.95]
    if name in ('appendix_E_probes','appendix_E_r11_probes','appendix_E_r12_probes'):
        groups=defaultdict(list)
        for r in rows:
            # Sum readers are the paper's endpoint; categorical readers remain
            # released. Each row retains every slot and seed, not a pooled mean.
            if 'category' in r[1]:continue
            reader=re.sub(r' s\d+$','',r[1])
            groups[r[0],reader].append(r)
        result=[]
        for (who,reader),v in groups.items():
            old=name=='appendix_E_probes'
            start=[r[2] for r in v];end=[r[4] if old else r[3] for r in v]
            majority=[r[5] if old else r[4] for r in v]
            shuffle=[r[6] if old else r[5] for r in v]
            oracle=[r[7] if old else r[6] for r in v]
            cis=[r[8] if old else r[7] for r in v]
            status=[r[9] if old else r[8] for r in v]
            result.append([who,reader,number(start),number(end),
                'majority '+span(majority)+'; shuffled '+span(shuffle)+'; oracle '+span(oracle),
                span(x for ci in cis for x in ci),str(all(x is True for x in status)) if 'linear' in reader else 'fixed budget'])
        # Display all seeds, with ranges across the five slots rather than a
        # pooled mean. Detailed files retain each exact count and interval.
        grouped=defaultdict(dict)
        for row in result:
            match=re.match(r'(.+)/(\d+) (original|equal)$',row[0])
            if not match:raise ValueError('probe run identity is not parseable')
            cond,seed,law=match.groups();grouped[cond,law,row[1]][int(seed)]=row
        reduced=[]
        def accuracy_range(text):
            # The r8 source has accuracies; other sources have count pairs.
            bits=text.split('/')
            if len(bits)==10:return span(int(bits[j].replace(',',''))/int(bits[j+1].replace(',','')) for j in range(0,10,2))
            return span(float(b.replace(',','')) for b in bits)
        for (cond,law,reader),seeds in grouped.items():
            reduced.append([cond+' '+law,reader,
                '; '.join('s'+str(s)+': '+accuracy_range(r[2]) for s,r in sorted(seeds.items())),
                '; '.join('s'+str(s)+': '+accuracy_range(r[3]) for s,r in sorted(seeds.items())),
                '; '.join(label+' '+span(float(x) for r in seeds.values() for x in
                    re.findall(r'[0-9]+(?:\.[0-9]+)?',r[4].split(label+' ',1)[1].split(';',1)[0]))
                    for label in ('majority','shuffled','oracle')),
                '; '.join('s'+str(s)+': '+r[5] for s,r in sorted(seeds.items())),
                'all seeds' if all(r[6]=='True' for r in seeds.values()) else 'fixed budget' if 'mlp' in reader else 'not all seeds'])
        return ['condition / law','reader','start accuracy: slot ranges per seed','end accuracy: slot ranges per seed','floors / ceiling ranges','gain CI envelopes per seed','converged'],reduced,[1.45,.6,.85,.85,1.0,.9,.6]
    if name=='appendix_E_original_geometry':
        groups=defaultdict(list)
        for r in rows:groups[tuple(r[:3])].append(r)
        result=[]
        for (cond,seed,step),v in groups.items():
            measured=[r for r in v if isinstance(r[5],str) and '/' in r[5]]
            missing=next(r[4] for r in v if r[3]=='all unsupported')
            result.append([cond,seed,step,len(measured),missing,sum(r[7] is True for r in measured),
                           span(r[6] for r in measured),span(r[8] for r in measured),span(r[9] for r in measured)])
        return ['condition','seed','update','measured pairs','missing support','passes','loss range','distance range','rerender range'],result,[1.5,.3,.4,.6,.6,.4,.75,.75,.75]
    if name=='appendix_D_erosion':
        groups=defaultdict(list)
        for r in rows:groups[r[0],r[1]].append(r)
        result=[]
        for (cond,seed),v in groups.items():
            by={r[2]:r for r in v}
            result.append([cond,seed,by[0][3],by[1][3],min(r[3] for r in v),v[-1][3],v[-1][5]])
        return ['condition','seed','update 0','update 1','minimum correct','final correct','final movement'],result,[1.6,.4,.65,.65,.8,.8,1.0]
    return headers,rows,widths
