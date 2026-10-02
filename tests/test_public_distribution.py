"""Publication-scope and portable-data regressions."""
from pathlib import Path
import json

from recombination_promotion import public_paths

ROOT=Path(__file__).resolve().parents[1]

def test_bulk_directory_is_configurable_and_repository_relative(monkeypatch,tmp_path):
    monkeypatch.delenv('SBML_DATA',raising=False)
    assert public_paths.public_path('bulk/example/input.json') == ROOT/'evidence/bulk/example/input.json'
    monkeypatch.setenv('SBML_DATA',str(tmp_path))
    assert public_paths.public_path('bulk/example/input.json') == tmp_path/'example/input.json'
    assert public_paths.public_path('repo/README.md') == ROOT/'README.md'

def test_only_six_study_trees_and_one_parent_are_retained():
    base=ROOT/'reports/phase11/oldgame_memory/multiround'
    expected={'study_r8_route_access','study_r9_raw_diagnosis','study_r10_allslots',
              'study_r11_jagged','study_r12_coverage','study_r13_mechanism'}
    assert {p.name for p in base.iterdir()} == expected
    for name in ('docs','templates','github_templates','lean'):
        assert not (ROOT/name).exists()
    reports=[p for p in (ROOT/'reports').rglob('*') if p.is_file() and not p.is_relative_to(base)]
    assert len(reports)==1 and reports[0].name=='parent_A_step_002000.pt'

def test_hash_projection_is_explicit_and_does_not_accept_arbitrary_identity(tmp_path,monkeypatch):
    (tmp_path/'evidence').mkdir()
    (tmp_path/'evidence/identity_projections.json').write_text(json.dumps({'bindings':{'old':'portable'}}))
    monkeypatch.setattr(public_paths,'ROOT',tmp_path)
    assert public_paths.identity_matches('old','portable')
    assert not public_paths.identity_matches('unknown','portable')
    assert not public_paths.identity_matches('old','tampered')

def test_fixed_panel_manifest_is_verified():
    from scripts import multiround_panels
    result=multiround_panels.verify_panels(ROOT/'evidence/panels')
    assert result['test_seeds']['natural']==2026100101


def test_saved_audit_uses_configurable_bulk_path(tmp_path,monkeypatch):
    import hashlib
    from scripts import oldgame_multiround_coverage as coverage
    path=tmp_path/'audit.json'
    path.write_text('{"correct": 3, "total": 4}')
    monkeypatch.setenv('SBML_DATA',str(tmp_path))
    ref={'path':'bulk/audit.json','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    assert coverage._load_audit(ref)=={'correct':3,'total':4}
    path.write_text('{"correct": 4, "total": 4}')
    import pytest
    with pytest.raises(ValueError,match='digest differs'):
        coverage._load_audit(ref)


def test_projected_metadata_does_not_relax_numerical_settings(tmp_path,monkeypatch):
    (tmp_path/'evidence').mkdir()
    (tmp_path/'evidence/identity_projections.json').write_text(json.dumps({'bindings':{'old':'portable'}}))
    monkeypatch.setattr(public_paths,'ROOT',tmp_path)
    saved={'seed':1,'law':'original','registration_sha256':'old'}
    projected={'seed':1,'law':'original','registration_sha256':'portable'}
    assert public_paths.metadata_matches(saved,projected)
    assert not public_paths.metadata_matches(saved,dict(projected,seed=2))
    assert not public_paths.metadata_matches(saved,dict(projected,law='equal'))
    assert not public_paths.metadata_matches(saved,dict(projected,registration_sha256='unknown'))


def test_public_source_arxiv_replay_preserves_submitted_pdfs():
    import importlib.util
    import hashlib
    import shutil
    import pytest
    if shutil.which('pdflatex') is None or shutil.which('latexmk') is None:
        pytest.skip('requires TeX Live and Poppler')
    path=ROOT/'paper/scripts/build_arxiv.py'
    spec=importlib.util.spec_from_file_location('public_arxiv',path)
    module=importlib.util.module_from_spec(spec)
    import sys
    sys.path.insert(0,str(path.parent))
    spec.loader.exec_module(module)
    submitted=list((ROOT/'paper/submission/artifacts').glob('*.pdf'))
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in submitted}
    receipt=module.public_source(ROOT/'paper')
    assert receipt['verification']['result']=='PASS'
    result=module.public_source(ROOT/'paper',checking=True)
    assert result['result']=='PASS' and result['included_graphics']
    assert result['paper_identifier_check'].startswith('PASS')
    assert {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in submitted}==before
