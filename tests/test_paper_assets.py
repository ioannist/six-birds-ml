"""Asset receipts, manuscript inclusion and deterministic public rebuilds."""
from pathlib import Path
import copy
import json
import os
import re
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'paper/scripts'))
from asset_inputs import Inputs, verify_receipts
from build_ledger import sha
from figure_assets import FIGURES
from table_assets import TABLES


@pytest.fixture(scope='module')
def inputs():return Inputs()


@pytest.mark.parametrize('folder,name', [('figures',n) for n in FIGURES]+[('tables',n) for n in TABLES])
def test_each_asset_values_match_ledger_and_verified_sources(inputs,folder,name):
    data=json.loads((ROOT/f'paper/{folder}/{name}.values.json').read_text())
    verify_receipts(inputs,data)
    assert data['receipts'],name
    if folder=='figures':
        assert data['minimum_font_pt']>=7
        assert data['width_inches']==6.5
    else:
        assert data['font_pt']>=7
        assert data['width_inches']<=6.5+1e-12
        assert data['rows'],name


@pytest.mark.parametrize('folder,name', [('figures',n) for n in FIGURES]+[('tables',n) for n in TABLES])
def test_each_asset_referenced_in_manuscript(folder,name):
    sources=[p for p in (ROOT/'paper').rglob('*.tex') if 'build' not in p.parts]
    assert any('\\input{'+folder+'/'+name+'}' in p.read_text() for p in sources),name
    if folder=='figures':
        assert '\\includegraphics[width=\\textwidth]{figures/'+name+'.pdf}' in (ROOT/f'paper/figures/{name}.tex').read_text()


def test_mutated_plot_value_is_refused(inputs):
    data=json.loads((ROOT/'paper/figures/fig3.values.json').read_text())
    bad=copy.deepcopy(data)
    r=next(r for r in bad['receipts'] if r.get('value') is not None and not r.get('manifest_only'))
    r['value']='changed while original hashes remain unchanged'
    with pytest.raises(ValueError,match='plotted value differs'):verify_receipts(inputs,bad)


def test_receipt_ledger_identity_is_required(inputs):
    data=json.loads((ROOT/'paper/figures/fig3.values.json').read_text())
    data['ledger_sha256']='0'*64
    with pytest.raises(ValueError,match='ledger identity differs'):verify_receipts(inputs,data)


@pytest.mark.parametrize('authority',['claims_ledger.json','evidence_manifest.json'])
def test_asset_build_refuses_authority_change_before_publication(tmp_path,authority):
    notes=tmp_path/'paper/notes'
    notes.mkdir(parents=True)
    for name in ('claims_ledger.json','evidence_manifest.json'):
        (notes/name).write_text('{}\n')
    ctx=Inputs.__new__(Inputs)
    ctx.root=tmp_path
    ctx.ledger_sha256=sha(notes/'claims_ledger.json')
    ctx.manifest_file_sha256=sha(notes/'evidence_manifest.json')
    ctx.assert_current()
    (notes/authority).write_text('{"changed":true}\n')
    with pytest.raises(ValueError,match='authority changed during build'):
        ctx.save_receipts('fixture','figures','fixture')
    assert not (tmp_path/'paper/figures/fixture.values.json').exists()


def test_text_relevant_panel_inputs_are_named_computations():
    checks={'fig1':['task','theory_nonfactorization'],'fig3':['r8_probes','r8_raw_KL','r8_law_TV','r10_free_probes'],
            'fig4':['r13_noise','r13_access','r13_encoding'],'fig5':['r13_erosion']}
    for asset,keys in checks.items():
        rows=json.loads((ROOT/f'paper/figures/{asset}.values.json').read_text())['receipts']
        for key in keys:
            bound=[r for r in rows if r['source']=='quantities' and r['pointer'][0]==key]
            assert bound and all(r['ledger_ids'] for r in bound),(asset,key)


def test_main_numbers_and_caption_controls():
    main=(ROOT/'paper/sections/05_results.tex').read_text()
    assert main.index('figures/fig3')<main.index('figures/fig4')<main.index('figures/fig5')
    captions=(ROOT/'paper/figures/captions.tex').read_text()
    for n in range(1,6):assert '\\csname captionfig'+str(n)+'\\endcsname' in captions
    for n in (3,4,5):
        c=json.loads((ROOT/f'paper/figures/fig{n}.values.json').read_text())['description'].lower()
        assert 'seed' in c and 'oracle' in c
        assert 'control' in c or 'floor' in c
    assert '0.02' in captions and 'historical' in captions and 'misreads' in captions


def test_two_layer_task_witness_is_legal_and_ledger_bound(inputs):
    from figure_assets import fig1_witness_records, fig1_mass_vocabulary
    from recombination_promotion.oldgame_ext.game import MASSES, whole_endpoints
    task = inputs.at(('quantities', 'task'))
    witness = inputs.at(('quantities', 'theory_nonfactorization'))
    assert fig1_mass_vocabulary(ROOT / 'src/recombination_promotion/serialization/minimal_recombination.py') == MASSES
    rows = fig1_witness_records(task, witness)
    boards, _ = whole_endpoints()
    assert [r['board'][0] for r in rows] == [8, 13, 36]
    assert [r['category'] for r in rows] == ['L', 'N', 'H']
    for row in rows:
        assert len(row['records']) == 4
        assert all(slot == 0 and mass in MASSES for slot, mass in row['records'])
        assert tuple(row['board']) in boards
        assert sum(mass for _, mass in row['records']) == row['board'][0]
    bad = copy.deepcopy(task); bad['records'] = 3
    with pytest.raises(ValueError, match='task support differs'):
        fig1_witness_records(bad, witness)


def test_two_layer_figure_specification_and_separate_training_strip(inputs, monkeypatch):
    import matplotlib.pyplot as plt
    import figure_assets
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.path import Path as PlotPath
    captured = {}

    def inspect(ctx, name, fig, caption, preview, **kwargs):
        captured.update(figure=fig, caption=caption, checks=kwargs['task_checks'])
        return {'name': name}

    monkeypatch.setattr(figure_assets, 'save', inspect)
    figure_assets.fig1(inputs, ROOT / 'unused-preview')
    fig = captured['figure']
    try:
        assert tuple(fig.get_size_inches()) == (6.5, 3.3)
        left, right = fig.axes
        text = [' '.join(t.get_text().split()) for ax in fig.axes for t in ax.texts]
        for required in ('Layer A: current-round computation', 'Layer B: computation across rounds',
                         'B consumes the slot-1 category', 'previous mode', 'next round',
                         'L: off · H: on · N: unchanged', 'Availability of A during training',
                         'Prediction loss only: A not supervised or supplied.',
                         'Exact sums supplied: A available as input.',
                         'Sums also supervised: output disconnected / connected.',
                         'same current A', 'different B', 'Both start with mode off',
                         'next-category law over (L, N, H)',
                         'Four records in slot 1 masses 2, 3, 4, 4 (twelfths)'):
            assert required in text
        assert left.get_position().width / right.get_position().width == pytest.approx(2.05)
        # The training strip occupies y <= .785. No graph edge reaches it.
        for edge in left.patches:
            if isinstance(edge, FancyArrowPatch):
                path = edge.get_path()
                # CLOSEPOLY carries a dummy vertex, not an executed edge.
                visible = path.vertices[path.codes != PlotPath.CLOSEPOLY]
                assert visible[:, 1].min() > .8
        assert captured['checks']['training_strip_has_no_edges']
        assert captured['checks']['category_arrow_source_slot'] == 1
        link = next(p for p in left.patches if p.get_gid() == 'fig1_a_to_b')
        slot1 = next(p for p in left.patches if p.get_gid() == 'fig1_slot1_sum')
        category = next(p for p in left.patches if p.get_gid() == 'fig1_category')
        x = slot1.get_x() + slot1.get_width()/2
        end = category.get_y() - .006
        assert x == pytest.approx(category.get_x()+category.get_width()/2)
        for actual, expected in zip(link._paper_vertices,
                [(x, slot1.get_y()+slot1.get_height()+.006), (x, end)], strict=True):
            assert actual == pytest.approx(expected)
        # The source is the first sum, not an edge of the five-sum row.
        assert x == pytest.approx(.68)
        for patch in left.patches:
            if hasattr(patch, 'get_x') and patch is not slot1 and patch.get_edgecolor()[3] > 0:
                assert not (patch.get_x() < x < patch.get_x()+patch.get_width()
                            and patch.get_y() < end and patch.get_y()+patch.get_height() > 1.286)
        feedback = next(p for p in left.patches if p.get_gid() == 'fig1_mode_feedback')
        previous = next(p for p in left.patches if p.get_gid() == 'fig1_previous_mode')
        updated = next(p for p in left.patches if p.get_gid() == 'fig1_updated_mode')
        assert feedback._paper_vertices[0][1] > updated.get_y()+updated.get_height()
        assert feedback._paper_vertices[-1][1] > previous.get_y()+previous.get_height()
        assert max(y for _, y in feedback._paper_vertices) < 2.80
        for gid in ('fig1_previous_to_updated', 'fig1_category_to_updated', 'fig1_updated_to_law'):
            edge = next(p for p in left.patches if p.get_gid() == gid)
            assert edge._posA_posB[0][0] < edge._posA_posB[1][0]
        assert next(t for t in left.texts if t.get_text() == 'Layer A: current-round computation').get_fontsize() == 9
        assert len(right.lines) == 2
        n_boxes = sorted((p for p in right.patches if p.get_gid() == 'fig1_witness_N'), key=lambda p:p.get_y())
        same = next(line for line in right.lines if line.get_gid() == 'fig1_same_A_connector')
        assert min(same.get_ydata()) > n_boxes[0].get_y()+n_boxes[0].get_height()
        assert max(same.get_ydata()) < n_boxes[1].get_y()
        assert same.get_xdata() == pytest.approx([n_boxes[0].get_x()+n_boxes[0].get_width()]*2)
        different = next(line for line in right.lines if line.get_gid() == 'fig1_different_B_connector')
        assert min(different.get_xdata()) > n_boxes[0].get_x()+n_boxes[0].get_width()
        assert sorted(set(different.get_ydata())) == [1.20, 2.45]
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        for label in left.texts:
            bounds = label.get_window_extent(renderer).transformed(left.transData.inverted())
            assert not (bounds.x0 < x < bounds.x1 and bounds.y0 < end and bounds.y1 > 1.286)
        law = next(p for p in left.patches if p.get_gid() == 'fig1_law_block')
        assert law.get_y() > 1.94+.05
        for label in left.texts:
            if label.get_text().startswith(('next-category law', 'off:', 'on:')):
                bounds = label.get_window_extent(renderer).transformed(left.transData.inverted())
                assert bounds.y0 > law.get_y() and bounds.y1 < law.get_y()+law.get_height()
        assert 'The annotations identify training conditions, not evidence that a network learned' in captured['caption']
        assert 'Everything shown is exact task ground truth, not model output.' in captured['caption']
    finally:
        plt.close(fig)


def test_compact_caption_provenance_and_log_oracle(inputs,monkeypatch):
    import figure_assets
    fig3=json.loads((ROOT/'paper/figures/fig3.values.json').read_text())['description']
    assert '(f) r12 uniform categorical misreads' in fig3
    captured={}
    def inspect(ctx,name,fig,caption,preview):
        try:
            captured['caption']=caption
            captured['scale']=fig.axes[3].get_yscale()
            captured['limits']=fig.axes[3].get_ylim()
        finally:figure_assets.plt.close(fig)
    monkeypatch.setattr(figure_assets,'save',inspect)
    figure_assets.fig4(inputs,None)
    assert captured['scale']=='log' and captured['limits'][0]>0
    assert 'except in (d), whose 0-bit oracle lies outside the logarithmic axis' in captured['caption']
    assert '24,435 boards, rendering 0' in captured['caption']
    assert 'Matched r13 comparisons' in captured['caption']
    fig5=json.loads((ROOT/'paper/figures/fig5.values.json').read_text())['description']
    assert 'every tested active optimizer' in fig5
    assert 'Blocked prediction gradient' in fig5 and 'weight-decay control' in fig5
    assert '128-board subset' in fig5 and 'r11/r13 is historical' in fig5


def test_rebuild_level_and_file_hashes():
    for category in ('figure','table'):
        result=json.loads((ROOT/f'paper/notes/{category}_reproducibility.json').read_text())
        assert result['level'].startswith('byte-identical')
        inventory=json.loads((ROOT/f'paper/notes/{category}_assets.json').read_text())
        assert result['assets']==len(inventory['assets'])
        for item in inventory['assets']:
            path=ROOT/'paper'/item['file']
            assert sha(path)==item['sha256']==result['sha256'][item['name']]
            assert sha(path.with_suffix('.values.json'))==item['receipt_sha256']


def test_geometry_missing_support_is_not_success():
    data=json.loads((ROOT/'paper/tables/appendix_E_original_geometry.values.json').read_text())
    missing=[r for r in data['rows'] if r[3]=='all unsupported']
    assert len(missing)==18 and all(r[4]==578 and r[5]=='MISSING_SUPPORT' for r in missing)
    assert any(r[3]==[12,13] and r[5]=='MISSING_SUPPORT' for r in data['rows'])


def test_public_package_rebuilds_assets_without_original_checkout(tmp_path):
    target=tmp_path/'archive'
    env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'}
    result=subprocess.run([sys.executable,'paper/scripts/build_ledger.py','--check','--public-package',str(target)],
        cwd=ROOT,env=env,capture_output=True,text=True,timeout=300)
    assert result.returncode==0,result.stdout+result.stderr
    for script in ('build_figures','build_tables'):
        args=[sys.executable,'-I',str(target/f'repo/paper/scripts/{script}.py')]
        if script=='build_figures':args+=['--preview-dir',str(tmp_path/'previews')]
        result=subprocess.run(args,cwd=tmp_path,env=env,capture_output=True,text=True,timeout=300)
        assert result.returncode==0,result.stdout+result.stderr
    for category in ('figure','table'):
        before=json.loads((ROOT/f'paper/notes/{category}_assets.json').read_text())
        after=json.loads((target/f'repo/paper/notes/{category}_assets.json').read_text())
        assert [(r['name'],r['sha256']) for r in before['assets']]==[(r['name'],r['sha256']) for r in after['assets']]
        for item in before['assets']:
            name=item['name'];folder='figures' if category=='figure' else 'tables'
            original=json.loads((ROOT/f'paper/{folder}/{name}.values.json').read_text())
            rebuilt=json.loads((target/f'repo/paper/{folder}/{name}.values.json').read_text())
            if category=='table':assert original['rows']==rebuilt['rows'],name
            else:
                assert [(r['source'],r['pointer'],r.get('value')) for r in original['receipts']]==[
                    (r['source'],r['pointer'],r.get('value')) for r in rebuilt['receipts']],name


def test_no_private_paths_or_bitmaps_in_tex():
    for p in (ROOT/'paper').rglob('*.tex'):
        if 'build' in p.parts:continue
        for arg in re.findall(r'\\(?:input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}',p.read_text()):
            assert not Path(arg).is_absolute()
            assert not arg.endswith('.png')


def test_vector_pdfs_have_no_raster_image_objects():
    for name in FIGURES:
        assert b'/Subtype /Image' not in (ROOT/f'paper/figures/{name}.pdf').read_bytes(),name


def test_preservation_and_mlp_scope_are_not_overstated():
    from table_assets import reader_status
    assert reader_status('linear',False) is False
    assert reader_status('mlp64',True)=='fixed budget; convergence not assessed'
    data=json.loads((ROOT/'paper/tables/table1_full.values.json').read_text())
    blocked=next(r for r in data['rows'] if r[0]=='r13: blocked prediction gradient')
    assert blocked[2]=='supported' and blocked[4]=='supported'
    a_plus_b=next(r for r in data['rows'] if r[0]=='r11: records → prediction+sums (Erosion continuation)')
    assert a_plus_b[4]=='not supported (inexact)'


@pytest.mark.parametrize('name', list(FIGURES))
def test_panel_letters_and_shared_legend_checks(name):
    data=json.loads((ROOT/f'paper/figures/{name}.values.json').read_text())
    count={'fig1':2,'fig2':2,'fig3':6,'fig4':6,'fig5':6,'appendix_D_movement':3,'appendix_C_methods':2,
           'appendix_D_r13_noise':3,'appendix_D_r13_access':3}.get(name,6)
    assert data['panel_letters']==[chr(ord('a')+i) for i in range(count)]
    assert data['legend_outside_axes'] is True
    assert data['panel_text_disjoint'] is True
    assert data['text_in_canvas'] is True
    # Captions identify every panel, either explicitly or by a letter range.
    caption=data['description']
    for letter in data['panel_letters']:
        ranges=re.findall(r'([a-i])–([a-i])',caption)
        assert re.search(r'\([^)]*\b'+letter+r'\b',caption) or any(a<=letter<=b for a,b in ranges)


def test_display_strings_use_glossary_and_real_inequalities():
    import ast
    source=(ROOT/'paper/scripts/figure_assets.py').read_text()
    strings=[n.value for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
    for value in strings:
        assert not any(term in value for term in ('B only','B-only','A+B','records to prediction','sums to prediction','<=','>=')),value
        # Dashes in line-style syntax and original source lookup keys are not text.
        assert '--' not in value or value in ('--','adam--sgd--reduced'),value
    assert r'$s\leq12$' in source and r'$s\geq24$' in source and '13–23' in source


@pytest.mark.parametrize('seed', range(3))
@pytest.mark.parametrize('condition', ['b_only','a_plus_b'])
def test_r11_exact_start_and_post_update_indices(inputs,seed,condition):
    from figure_assets import erosion_readouts
    steps,scores=erosion_readouts(inputs,seed,condition)
    assert steps==[0,1,5,10,50,100] and scores[0]==1.0
    assert scores[1]<1.0
    receipt=json.loads((ROOT/'paper/figures/fig5.values.json').read_text())
    key=f'erosion_{condition}_original_seed{seed}'
    assert any(r['source']=='control' and r['pointer']==['11',key,'B_A_curve',0]
               for r in receipt['receipts'])


def test_r11_inexact_start_is_not_silently_replaced_by_oracle():
    from figure_assets import erosion_readouts
    class BadStart:
        def ref(self,*path):return {'step':0,'A_vector_accuracy':.9}
    with pytest.raises(ValueError,match='update-0 board audit is not exact'):
        erosion_readouts(BadStart(),0,'b_only')


def test_in_axes_legend_is_refused(tmp_path):
    from types import SimpleNamespace
    from figure_assets import save, plt
    fig,ax=plt.subplots()
    ax.plot([0,1],[0,1],label='data');ax.legend()
    try:
        with pytest.raises(ValueError,match='shared and outside data axes'):
            save(SimpleNamespace(root=tmp_path),'test',fig,'caption',tmp_path/'preview')
    finally:plt.close(fig)


def test_cross_panel_text_collision_is_refused(tmp_path):
    from types import SimpleNamespace
    from figure_assets import save, plt
    fig,axes=plt.subplots(2,1)
    for ax in axes:ax.text(.5,.5,'collision',transform=fig.transFigure)
    try:
        with pytest.raises(ValueError,match='text overlaps across figure panels'):
            save(SimpleNamespace(root=tmp_path),'test',fig,'caption',tmp_path/'preview')
    finally:plt.close(fig)


def test_cross_panel_tick_label_collision_is_refused(tmp_path):
    from types import SimpleNamespace
    from figure_assets import save, plt
    fig,axes=plt.subplots(2,1)
    axes[0].set_xticks([.5],labels=['tick collision'])
    fig.canvas.draw()
    bounds=axes[0].get_xticklabels()[0].get_window_extent(fig.canvas.get_renderer())
    x,y=fig.transFigure.inverted().transform(bounds.get_points().mean(axis=0))
    axes[1].text(x,y,'neighbouring panel',transform=fig.transFigure,ha='center',va='center')
    try:
        with pytest.raises(ValueError,match='text overlaps across figure panels'):
            save(SimpleNamespace(root=tmp_path),'test',fig,'caption',tmp_path/'preview')
    finally:plt.close(fig)


def test_empty_series_is_refused():
    from figure_assets import require_series
    with pytest.raises(ValueError,match='empty measured series'):
        require_series([], 'unrecorded condition')


def test_geometry_build_refuses_an_empty_condition(tmp_path):
    from types import SimpleNamespace
    from figure_assets import geometry,plt,ledger_supplement
    ctx=SimpleNamespace(begin=lambda:None,
        evidence=SimpleNamespace(load=lambda name:{'supplementary':{'rows':[]}},
            entries={'repo/'+ledger_supplement(None):{'id':'fixture'}}),
        manifest_json=lambda entry:None)
    try:
        with pytest.raises(ValueError,match='empty measured series: geometry raw_sampled seed 0'):
            geometry(ctx,tmp_path)
    finally:plt.close('all')


def test_geometry_has_only_recorded_raw_conditions():
    data=json.loads((ROOT/'paper/figures/appendix_E_geometry.values.json').read_text())
    assert 'sampled- and probability-target' in data['description']
    assert 'prediction+sums readers' not in data['description']
    source=(ROOT/'paper/scripts/figure_assets.py').read_text().split('def geometry(')[1]
    assert 'for condition in ("raw_sampled", "raw_probability")' in source
    assert 'require_series(selected' in source


def test_text_outside_canvas_is_refused(tmp_path):
    from types import SimpleNamespace
    from figure_assets import save, plt
    fig,ax=plt.subplots();fig.text(1.2,.5,'clipped title')
    try:
        with pytest.raises(ValueError,match='text outside canvas'):
            save(SimpleNamespace(root=tmp_path),'test',fig,'caption',tmp_path/'preview')
    finally:plt.close(fig)


def test_recovery_marks_use_counts_floors_and_convergence(inputs):
    from table_assets import recovery
    for seed,correct in enumerate((483,509,505)):
        key=f'a_target_original_seed{seed}'
        row=inputs.sources['control']['12'][key]
        assert row['probes']['raw']['linear']['sum36'][0]['endpoint_counts']['correct']==correct
        measured=recovery(inputs,12,key,row)
        assert measured.startswith('supported') and f'{correct}/512' in measured
    class Mock:
        def ref(self,*args):return {'raw':{'linear':{'sum36':[dict(converged=False,
            endpoint_accuracy=1,majority_floor=.5,shuffled_floor=.2,paired_CI95=[.3,.4],
            endpoint_counts={'correct':512})]}}}
    assert recovery(Mock(),12,'example',{'probes':True}).startswith('not supported')


def test_mixed_computation_is_not_erased(inputs):
    from table_assets import endpoint
    counts=[endpoint(inputs,11,k,inputs.sources['control']['11'][k])['sum_vector']
        for k in [f'erosion_a_plus_b_original_seed{s}' for s in range(3)]]
    assert counts==[24434,24435,24419]
    data=json.loads((ROOT/'paper/tables/table1_full.values.json').read_text())
    row=next(r for r in data['rows'] if r[0]=='r11: records → prediction+sums (Erosion continuation)')
    assert row[2].startswith('supported 1/3; audited sum-output')
    assert 'rendering 0' in data['description']


def test_endpoint_labels_and_r11_law_are_recorded(inputs):
    from table_assets import endpoint
    for seed in range(3):
        k=f'rarity_uniform_original_seed{seed}';r=inputs.sources['control']['11'][k]
        assert endpoint(inputs,11,k,r)['long']==r['B_law']['maximum_TV']
    k='raw_only_seed0'
    assert endpoint(inputs,9,k,inputs.sources['control']['9'][k])['label']=='not assessed in r9'


def test_study_specific_law_bars_and_group_keys():
    fig=json.loads((ROOT/'paper/figures/fig3.values.json').read_text())
    assert '0.05 bar' in fig['description'] and 'equal-law bar is 0.02' in fig['description']
    for name in ('table2','table2_full','appendix_B_laws'):
        caption=json.loads((ROOT/f'paper/tables/{name}.values.json').read_text())['description']
        assert '0.05' in caption and '0.02' in caption


def test_r13_update_one_counts_bind_original_records(inputs):
    from figure_assets import run13
    expected={'adam':[393,5,518],'reduced':[1554,1468,1553],'sgd':[1440,89,1495],'blocked':[1555]*3}
    for condition,counts in expected.items():
        for seed,count in enumerate(counts):
            key=run13(inputs,'erosion',condition,seed)
            rows,eid=inputs.referenced(inputs.sources['control']['13'][key]['records'])
            row=next(r for r in rows if r['step']==1)
            assert row['local']['correct']==count and row['local']['total']==1555
    caption=json.loads((ROOT/'paper/figures/fig5.values.json').read_text())['description']
    assert 'every tested active optimizer' in caption.lower()
    assert '393 / 5 / 518' in caption and '1,554 / 1,468 / 1,553' in caption


def test_exhaustive_tables_are_separate_with_fixed_public_numbers():
    from table_assets import SUPPLEMENT_TABLES
    content=(ROOT/'paper/supplement/table_inputs.tex').read_text()
    assert [m for m in re.findall(r'\\input\{tables/([^}]+)\}',content)]==SUPPLEMENT_TABLES
    appendix='\n'.join(p.read_text() for p in (ROOT/'paper/appendices').glob('*.tex'))
    assert 'tables/appendix_D_erosion' not in appendix
    assert 'Supplement Table S27' in appendix and 'tables/compact_D' in appendix
    assert SUPPLEMENT_TABLES[21:24]==['appendix_E_probes','appendix_E_r11_probes','appendix_E_r12_probes']


def test_overfull_decision_refuses_oversize_boxes():
    from check_package import overfull_boxes
    assert overfull_boxes(r'Overfull \hbox (9.5pt too wide)')==[9.5]
    with pytest.raises(ValueError,match='exceeds 10 pt'):
        overfull_boxes(r'Overfull \hbox (10.1pt too wide)')
    with pytest.raises(ValueError,match='caption exceed'):
        overfull_boxes('LaTeX Warning: Float too large for page')


def test_all_condition_labels_are_explicit_glossary_members():
    from condition_labels import NAMES,validate_label,condition_name
    for label in NAMES.values():
        validate_label(label)
        validate_label('r13: '+label+' / seed 2')
    assert condition_name('frozen')=='Connected (frozen)'
    assert condition_name('live')=='Connected (live)'
    assert condition_name('disconnected')=='records → prediction+sums'
    with pytest.raises(ValueError,match='glossary'):validate_label('records+sums → prediction (live supplier)')
    with pytest.raises(ValueError,match='unknown condition'):condition_name('invented_variant')


def test_condition_labels_in_built_tables_match_glossary():
    from condition_labels import validate_label
    names=['table1','table1_full','table2','table2_full','appendix_B_census',
           'appendix_B_laws','appendix_B_support','appendix_C_interchange',
           'appendix_E_probes','appendix_E_r11_probes','appendix_E_r12_probes',
           *[f'appendix_B_r{n}' for n in (8,9,10,11,12,13)]]
    controls={'r8 board-only calibration','r8 board-only control','exact task oracle'}
    for name in names:
        data=json.loads((ROOT/f'paper/tables/{name}.values.json').read_text())
        for row in data['rows']:
            if row[0] not in controls:validate_label(row[0])


def test_supported_slot_counts_remain_per_seed(inputs):
    from table_assets import recovery
    expected={(10,'free'):[5,5,5],(10,'free_a'):[5,5,5],
              (11,'erosion_b_only'):[1,1,1],(11,'erosion_a_plus_b'):[3,1,1],(12,'a_target'):[5,5,5]}
    data=json.loads((ROOT/'paper/tables/table1.values.json').read_text())
    from condition_labels import condition_name
    for (n,condition),counts in expected.items():
        row=next(r for r in data['rows'] if r[0]==f'r{n}: '+condition_name(condition))
        assert row[1]=='supported slots: '+' / '.join(f'{x}/5' for x in counts)
        for seed,count in enumerate(counts):
            key=f'{condition}_original_seed{seed}'
            assert f'{count}/5' in recovery(inputs,n,key,inputs.sources['control'][str(n)][key])
        complete=json.loads((ROOT/'paper/tables/table1_full.values.json').read_text())
        printed=next(r for r in complete['displayed_rows'] if r[0]==f'r{n}: '+condition_name(condition))
        assert printed[1]==row[1]
    assert '512 held-out boards/slot' in data['note'] and 'Raw-carrier linear' in data['note']
    r8=next(r for r in data['rows'] if r[0]=='r8: records → prediction')
    assert r8[1]=='supported slots: 1/5 / 1/5 / 1/5 (slot 1)'
    assert 'not established: available evidence does not establish this achievement' in (ROOT/'paper/tables/table1.tex').read_text()


def test_prose_words_never_have_forced_internal_breaks():
    from table_assets import cell_tex
    from asset_inputs import number
    for word in ('recoverability','continuation','convergence','probability'):
        assert cell_tex(word,.3)==word
    assert number(24435)=='24,435' and number([1555,393])=='1,555/393'
    assert '\\hyphenpenalty=10000' in (ROOT/'paper/tables/table1.tex').read_text()


def test_main_assets_have_compact_float_layout():
    table=(ROOT/'paper/tables/table1.tex').read_text()
    assert '\\begin{table}[tb]' in table and '\\begin{longtable}' not in table
    receipt=json.loads((ROOT/'paper/tables/table1.values.json').read_text())
    assert len(receipt['rows'])==len(receipt['displayed_rows'])==13
    assert receipt['layout']=='single-page compact float'
    for full,short in zip(receipt['rows'],receipt['displayed_rows'],strict=True):
        assert full[0]==short[0]
        slots=re.findall(r'(\d)/5',full[1])
        assert re.findall(r'(\d)/5',short[1])==slots
        seed_count=re.search(r'(\d)/3',full[2])
        if seed_count:assert seed_count.group(0) in short[2]
        if full[2].startswith('not established'):assert short[2]=='–'
        elif full[2].startswith('not supported'):assert '\\times' in short[2]
        else:assert '\\checkmark' in short[2]
    for n,limit in ((1,3.5),(2,4),(3,4.6),(4,4.6),(5,4.0)):
        data=json.loads((ROOT/f'paper/figures/fig{n}.values.json').read_text())
        assert data['height_inches']<=limit and data['minimum_font_pt']>=7
        assert '\\begin{figure}[tb]' in (ROOT/f'paper/figures/fig{n}.tex').read_text()


def test_table1_achievement_names_and_distinct_access_evidence():
    data=json.loads((ROOT/'paper/tables/table1.values.json').read_text())
    assert data['displayed_headers'][1:]==['recoverability','computation','access','preservation','reliable prediction']
    for full,short in zip(data['rows'],data['displayed_rows'],strict=True):
        if full[3].startswith('supported by design'):
            assert short[3]==r'$\checkmark^{D}$'
        elif full[3].startswith('demonstrated by matched'):
            assert short[3]==r'$\checkmark^{I}$'
        else:
            assert short[3]=='–'
    assert 'by design (exact sums supplied)' in data['description']
    assert 'matched connection intervention' in data['description']
    assert 'Computation: the audited sums output' in data['note']
    assert 'does not establish selective use' in data['note']


def test_movement_panels_are_preserved_in_appendix_d():
    receipt=json.loads((ROOT/'paper/figures/appendix_D_movement.values.json').read_text())
    assert receipt['panel_letters']==['a','b','c']
    assert receipt['minimum_font_pt']>=7
    assert 'three-active-arm common range' in receipt['description']
    assert 'not interpolated' in receipt['description']
    assert 'figures/appendix_D_movement' in (ROOT/'paper/appendices/D_learning_curves.tex').read_text()
    main=json.loads((ROOT/'paper/figures/fig5.values.json').read_text())
    assert r'\cref{fig:appendix_D_movement}' in main['description']
    assert any('erosion_comparisons' in str(r) for r in receipt['receipts'])


def test_released_details_are_complete_and_hash_bound():
    import hashlib
    import gzip
    index=json.loads((ROOT/'paper/data/release/index.json').read_text())
    from table_assets import SUPPLEMENT_TABLES
    assert len(index['files'])==len(SUPPLEMENT_TABLES)
    for item in index['files']:
        path=ROOT/'paper'/item['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        detail=json.loads(gzip.decompress(path.read_bytes()))
        receipt=json.loads((ROOT/f'paper/tables/{detail["table"]}.values.json').read_text())
        assert detail['rows']==receipt['rows'] and len(detail['rows'])==item['rows']
        assert detail['ledger_sha256']==sha(ROOT/'paper/notes/claims_ledger.json')
        assert item['path'] in receipt['description']
    assert (ROOT/'paper/data/release/README.md').exists()


def test_scientific_calibration_selection_has_positives_and_nulls(inputs):
    from table_summaries import calibration_rows
    rows=calibration_rows(inputs)
    for study in ('r8','r10','r11','r12','r13'):
        original=[r for r in rows if r[0]==study and r[1]=='original']
        assert any(r[4] is True for r in original)
        assert any(r[4] is False for r in original)
        assert all(r[5] for r in original)
    text=(ROOT/'paper/scripts/table_assets.py').read_text()
    assert 'if len(rows)==8:break' not in text and ">=3:break" not in text


def test_compute_selection_identifies_runs_and_is_not_a_total(inputs):
    data=json.loads((ROOT/'paper/tables/compact_F.values.json').read_text())
    assert data['rows']
    assert all(r[0] in ('r8','r13') and r[4]=='examples, not totals' for r in data['rows'])
    assert all('T-' not in r[1] and r[3] for r in data['rows'])


def test_heading_only_page_detection():
    from check_package import heading_only_pages
    assert heading_only_pages('Title\fAll recorded learning curves\n628\f')==[2]
    assert heading_only_pages('Title\f'+'A measured comparison with rows '*15+'\f')==[]


def test_figure_five_colours_have_one_meaning():
    from figure_assets import PALETTE
    keys=('records','sums','adam','reduced','sgd','blocked')
    assert len({PALETTE[k] for k in keys})==len(keys)
