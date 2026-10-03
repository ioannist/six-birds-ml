"""Build and execute the reader notebook, including all released-evidence cells."""
import importlib.util
import json
import logging
import os
from pathlib import Path
import socket
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location('notebook_' + name, ROOT / 'notebook' / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def test_notebook_build_and_source_contract():
    import nbformat
    built = module('build').build()
    nbformat.validate(nbformat.from_dict(built))
    assert json.loads((ROOT / 'notebook/jagged_competence.ipynb').read_text()) == built
    code = [c for c in built['cells'] if c['cell_type'] == 'code']
    assert len(code) == 10
    assert all(c['outputs'] == [] and c['execution_count'] is None for c in code)
    assert all('# @title' in c['source'] for c in code)
    assert 'INLINE_RUNTIME' not in ''.join(c['source'] for c in code)
    assert 'MODE = "quick"' in code[0]['source']
    assert len(module('runtime').SOURCE_COMMIT) == 40
    readme = (ROOT / 'README.md').read_text()
    assert readme.index('## Run it yourself') < readme.index('| Directory')
    assert 'colab.research.google.com/github/ioannist/six-birds-ml/blob/main/notebook/jagged_competence.ipynb' in readme


def test_notebook_comparison_refuses_changed_paper_number():
    session = module('runtime').Session()
    with pytest.raises(AssertionError, match='ledger reference'):
        session.compare('boards', 24436, 24435)
    assert session.compare('boards', 24435, 24435)


def test_fresh_erosion_is_descriptive_without_weakening_checks(capsys):
    session = module('runtime').Session()
    assert session.compare('saved paper', 393, 393)
    assert not session.compare('fresh first batch', 148, 393, strict=False, fresh_batch=True)
    text = capsys.readouterr().out
    assert 'MATCH' in text and 'fresh measurement (different first batch;' in text
    assert 'DIFFERENT' not in text
    assert session.comparisons[-1]['comparison_kind'] == 'fresh_batch'
    with pytest.raises(AssertionError):
        session.compare('blocked control', 1554, 1555, fresh_batch=True)


def test_timestamp_filter_is_narrow_and_temporary(caplog):
    runtime = module('runtime')
    logger = logging.getLogger('fontTools.ttLib.tables._h_e_a_d')
    created = "'created' timestamp seems very low; regarding as unix timestamp"
    modified = "'modified' timestamp seems very low; regarding as unix timestamp"
    before = list(logger.filters)
    with caplog.at_level(logging.WARNING):
        with runtime.quiet_font_timestamps():
            logger.warning(created)
            logger.warning(modified)
            logger.warning('other font diagnostic')
            logging.getLogger('fontTools.other').warning(created)
        logger.warning(modified)
    assert logger.filters == before
    assert [r.getMessage() for r in caplog.records] == ['other font diagnostic', created, modified]


def test_outside_checkout_clone_install_setup(tmp_path, monkeypatch):
    """Exercise hosted setup; network/install commands are substituted, not setup."""
    runtime = module('runtime')
    outside = tmp_path / 'outside'
    outside.mkdir()
    monkeypatch.chdir(outside)
    monkeypatch.delenv('SBML_REPO', raising=False)
    monkeypatch.setenv('SBML_DEVICE', 'cpu')
    monkeypatch.setenv('SBML_NOTEBOOK_OUTPUT', str(tmp_path / 'session'))
    monkeypatch.syspath_prepend(str(ROOT / 'paper/scripts'))
    monkeypatch.setattr(runtime.Session, 'font_setup', lambda self: None)
    actual_run = subprocess.run
    calls = []
    cloned = []

    def run(args, **kwargs):
        calls.append((args, kwargs))
        if args[:2] == ['git', 'clone']:
            root = Path(args[-1])
            cloned.append(root)
            (root / 'src').mkdir(parents=True)
            notes = root / 'paper/notes'
            notes.mkdir(parents=True)
            (notes / 'claims_ledger.json').write_text(json.dumps({'recomputed_outline_quantities': {}}))
            (notes / 'evidence_manifest.json').write_text(json.dumps({'artifacts': []}))
            return subprocess.CompletedProcess(args, 0)
        if args[:2] == ['git', 'checkout'] or args[1:4] == ['-m', 'pip', 'install']:
            return subprocess.CompletedProcess(args, 0)
        if args[:2] == ['git', '-C']:
            if args[-1] == '--show-toplevel':
                value = str(cloned[0])
            elif args[-1] == 'HEAD':
                value = runtime.SOURCE_COMMIT
            else:
                value = ''
            return subprocess.CompletedProcess(args, 0, stdout=value, stderr='')
        return actual_run(args, **kwargs)

    monkeypatch.setattr(runtime.subprocess, 'run', run)
    session = runtime.Session()
    session.setup()
    assert session.root == cloned[0]
    assert runtime.find_repo(session.root) == session.root
    assert session.source_mode == 'hosted_pinned_clone'
    assert session.checkout == {'kind': 'git_checkout', 'commit': runtime.SOURCE_COMMIT,
                                'working_tree_dirty': False}
    assert calls[0][0] == ['git', 'clone', '--no-checkout', '--filter=blob:none', runtime.SOURCE_URL, str(session.root)]
    assert calls[1][0] == ['git', 'checkout', '--detach', runtime.SOURCE_COMMIT]
    assert calls[1][1]['cwd'] == session.root
    # All scientific packages are present, so nothing is installed or upgraded
    # (upgrading preloaded packages in a hosted runtime mixes versions).
    assert not any(c[0][1:4] == ['-m', 'pip', 'install'] for c in calls)


def test_hosted_setup_installs_only_missing_packages(monkeypatch):
    import importlib.util
    runtime = module('runtime')
    real = importlib.util.find_spec
    monkeypatch.setattr(importlib.util, 'find_spec',
                        lambda name, *a, **k: None if name == 'sklearn' else real(name, *a, **k))
    missing = [pkg for mod, pkg in runtime.INSTALL_IF_MISSING if importlib.util.find_spec(mod) is None]
    assert missing == ['scikit-learn']
    assert all('==' not in pkg for _, pkg in runtime.INSTALL_IF_MISSING)


def test_actual_local_identity_is_separate_from_hosted_pin(tmp_path):
    runtime = module('runtime')
    identity = runtime.checkout_identity(ROOT)
    actual = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    assert identity['commit'] == actual
    assert identity['kind'] == 'git_checkout'
    assert isinstance(identity['working_tree_dirty'], bool)
    assert runtime.checkout_identity(tmp_path) == {'kind': 'source_directory', 'commit': None,
                                                   'working_tree_dirty': None}


def test_access_table_includes_per_seed_census_counts(monkeypatch):
    runtime = module('runtime')
    session = runtime.Session()
    session.root = ROOT
    session.q = json.loads((ROOT / 'paper/notes/claims_ledger.json').read_text())['recomputed_outline_quantities']
    shown = []
    monkeypatch.setattr(runtime, 'table', lambda headers, rows: shown.append((headers, rows)))
    import matplotlib.pyplot as plt
    monkeypatch.setattr(session, 'show', plt.close)
    session.mechanisms()
    headers, rows = shown[0]
    assert headers[4] == 'Ledger categorical misreads / 24,435'
    assert len(rows) == 12
    conditions = ('disconnected', 'frozen', 'live', 'exact')
    for i, condition in enumerate(conditions):
        for seed in range(3):
            assert rows[3 * i + seed][4] == session.q['r13_access'][condition][seed]['categorical_misreads']


def test_notebook_run_all_cpu(tmp_path, monkeypatch):
    """Same Run-All path; only the new live-training budget is shortened to 25 updates."""
    import nbformat
    from nbclient import NotebookClient
    from jupyter_client.kernelspec import KernelSpecManager

    try:
        sock = socket.socket()
        sock.bind(('127.0.0.1', 0))
        sock.close()
    except PermissionError:
        pytest.skip('Kernel sockets prohibited by execution environment; all cells exercised by the IPython test')

    kernel = tmp_path / 'kernels' / 'sbml-test'
    kernel.mkdir(parents=True)
    env = dict(os.environ)
    env.update(SBML_NOTEBOOK_FAST='1', SBML_DEVICE='cpu', SBML_REPO=str(ROOT),
               SBML_NOTEBOOK_OUTPUT=str(tmp_path / 'session'), OMP_NUM_THREADS='1',
               MKL_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    (kernel / 'kernel.json').write_text(json.dumps({
        'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'display_name': 'Scientific notebook test', 'language': 'python', 'env': env}))
    manager = KernelSpecManager(kernel_dirs=[str(tmp_path / 'kernels')])
    notebook = nbformat.read(ROOT / 'notebook/jagged_competence.ipynb', as_version=4)
    nbformat.validate(notebook)
    client = NotebookClient(notebook, timeout=1200, kernel_name='sbml-test',
                            resources={'metadata': {'path': str(ROOT)}})
    client.km = client.create_kernel_manager()
    client.km.kernel_spec_manager = manager
    client.execute()
    assert all(c.execution_count is not None for c in notebook.cells if c.cell_type == 'code')
    assert not any(o.output_type == 'error' for c in notebook.cells if c.cell_type == 'code' for o in c.outputs)
    receipt = json.loads((tmp_path / 'session/session_results.json').read_text())
    assert receipt['mode'] == 'quick' and receipt['live']['steps'] == 25
    assert receipt['execution_source'] == 'local'
    assert receipt['hosted_source_pin'] == module('runtime').SOURCE_COMMIT
    assert receipt['checkout_identity']['commit'] == module('runtime').checkout_identity(ROOT)['commit']
    assert len(receipt['released_probes']) == 30
    assert len(receipt['erosion']) == 4
    checks = receipt['comparisons']
    assert len(checks) >= 30 and all(c['match'] for c in checks if c['required_match'])
    assert all(c['match'] for c in checks if c['label'].startswith('r8 raw linear'))
    assert next(c for c in checks if c['label'] == 'All legal boards')['observed'] == 24435
    assert 'COMPLETE:' in ''.join(o.get('text', '') for c in notebook.cells if c.cell_type == 'code' for o in c.outputs)


def test_notebook_every_cell_in_ipython(tmp_path, monkeypatch):
    """Socket-independent Run-All validation; the nbclient test remains separate."""
    from IPython.core.interactiveshell import InteractiveShell
    monkeypatch.chdir(ROOT)
    for key, value in {'SBML_NOTEBOOK_FAST': '1', 'SBML_DEVICE': 'cpu', 'SBML_REPO': str(ROOT),
                       'SBML_NOTEBOOK_OUTPUT': str(tmp_path / 'session')}.items():
        monkeypatch.setenv(key, value)
    shell = InteractiveShell()
    cells = module('build').build()['cells']
    for cell in cells:
        if cell['cell_type'] == 'code':
            outcome = shell.run_cell(cell['source'])
            outcome.raise_error()
    receipt = json.loads((tmp_path / 'session/session_results.json').read_text())
    assert len(receipt['released_probes']) == 30
    assert receipt['live']['steps'] == 25
    assert len(receipt['erosion']) == 4
    assert receipt['execution_source'] == 'local'
    assert receipt['hosted_source_pin'] == module('runtime').SOURCE_COMMIT
    assert receipt['checkout_identity']['commit'] == module('runtime').checkout_identity(ROOT)['commit']
    assert all(c['match'] for c in receipt['comparisons'] if c['required_match'])
    assert all(c['match'] for c in receipt['comparisons'] if c['label'].startswith('r8 raw linear'))


def test_hosted_pin_matches_current_code():
    """Colab clones SOURCE_COMMIT; its code must equal the code the notebook expects."""
    runtime = module('runtime')
    if not (ROOT / '.git').exists():
        pytest.skip('not a git checkout')
    known = subprocess.run(['git', '-C', str(ROOT), 'cat-file', '-e', runtime.SOURCE_COMMIT + '^{commit}'])
    if known.returncode:
        pytest.skip('pinned commit not present in this checkout')
    diff = subprocess.run(['git', '-C', str(ROOT), 'diff', '--name-only', runtime.SOURCE_COMMIT, '--',
                           'paper/scripts', 'src', 'scripts'], capture_output=True, text=True, check=True)
    assert diff.stdout.strip() == '', 'code changed since the hosted pin; update SOURCE_COMMIT: ' + diff.stdout
