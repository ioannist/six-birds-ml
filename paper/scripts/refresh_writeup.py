"""Serial local write-up refresh: pin, assets, release, arXiv, then checks.

This command neither edits manuscript inputs nor invokes remote release tools.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from asset_inputs import Inputs, verify_receipts
from build_ledger import ROOT, MANIFEST, sha


def source_snapshot(root):
    manifest = json.loads((root / MANIFEST).read_text())
    sources = {}
    for item in manifest['artifacts']:
        name = item['archive_path']
        if name.startswith('repo/paper/'):
            path = root / name.removeprefix('repo/')
            if path.is_file():
                if sha(path) != item['sha256']:
                    raise ValueError(f'write-up input changed after pin: {name}')
                sources[name] = item['sha256']
    return {'manifest': sha(root / MANIFEST),
            'ledger': sha(root / 'paper/notes/claims_ledger.json'), 'sources': sources}


def check_snapshot(root, frozen):
    if source_snapshot(root) != frozen:
        raise ValueError('write-up authority changed during refresh; restart from the explicit pin step')


def check_assets(root):
    ctx = Inputs(root)
    for category, folder in (('figure', 'figures'), ('table', 'tables')):
        inventory = json.loads((root / f'paper/notes/{category}_assets.json').read_text())
        if inventory['ledger_sha256'] != ctx.ledger_sha256:
            raise ValueError(f'{category} inventory has stale ledger identity')
        for asset in inventory['assets']:
            path = root / 'paper' / asset['file']
            receipt = path.with_suffix('.values.json')
            if sha(path) != asset['sha256'] or sha(receipt) != asset['receipt_sha256']:
                raise ValueError(f'asset inventory differs: {path.name}')
            verify_receipts(ctx, json.loads(receipt.read_text()))
        print(f'{category} authority: PASS ({len(inventory["assets"])} assets)', flush=True)


def planned_commands(root, python, release_tool):
    """The order is executable and independently regression-tested."""
    script = lambda name: str(root / 'paper/scripts' / name)
    return [
        ('pin', [python, script('build_ledger.py'), '--pin'], root),
        ('figures', [python, script('build_figures.py'), '--verify-rebuild'], root),
        ('tables', [python, script('build_tables.py'), '--verify-rebuild'], root),
        ('ledger', [python, script('build_ledger.py'), '--check', '--verify-all'], root),
        ('release', [python, str(release_tool), '--build'], root),
        ('supplement', ['latexmk', '-pdf', '-jobname=supplement', 'supplement/supplement.tex'], root / 'paper'),
        ('arxiv', [python, script('build_arxiv.py')], root),
        ('arxiv_check', [python, script('build_arxiv.py'), '--check'], root),
        ('clean_tex', [python, script('check_package.py'), '--output',
                       str(root / 'paper/build/layout_receipt.json')], root),
        ('writeup_tests', [python, '-m', 'pytest', 'tests/test_paper_writeup.py',
                           'tests/test_paper_assets.py', '-q'], root),
        ('multiround_tests', [python, '-m', 'pytest',
                             *[str(p.relative_to(root)) for p in sorted((root / 'tests').glob('test_oldgame_multiround*.py'))], '-q'], root),
        ('ruff', ['ruff', 'check', '--select', 'F,E9', 'paper/scripts',
                  'tests/test_paper_writeup.py', 'tests/test_paper_assets.py'], root),
        ('diff', ['git', 'diff', '--check'], root),
    ]


def refresh(root, release_tool, python=sys.executable):
    build = root / 'paper/build'
    build.mkdir(parents=True, exist_ok=True)
    logs = build / 'writeup_refresh_logs'
    logs.mkdir(exist_ok=True)
    env = dict(os.environ, OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               CUDA_VISIBLE_DEVICES='', PYTHONPATH=str(root / 'src'), ZENODO_PAPER_REPO=str(root))
    report = {'result': 'RUNNING', 'stages': [], 'remote_actions': 0}
    receipt = build / 'writeup_refresh.json'
    with (build / 'writeup_refresh.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('another write-up refresh is active') from exc
        frozen = None
        try:
            for name, command, cwd in planned_commands(root, python, release_tool):
                if frozen is not None:
                    check_snapshot(root, frozen)
                if name == 'release':
                    check_assets(root)
                print(f'START {name}', flush=True)
                start = time.monotonic()
                logfile = logs / (name + '.log')
                with logfile.open('w') as stream:
                    completed = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                               stderr=subprocess.STDOUT, check=False)
                report['stages'].append({'stage': name, 'exit_code': completed.returncode,
                                         'seconds': time.monotonic() - start,
                                         'log': logfile.relative_to(root).as_posix()})
                receipt.write_text(json.dumps(report, indent=2) + '\n')
                if completed.returncode:
                    raise ValueError(f'{name} failed; see {logfile}\n{logfile.read_text()[-6000:]}')
                if name == 'pin':
                    frozen = source_snapshot(root)
                    report['authority'] = frozen
                else:
                    check_snapshot(root, frozen)
                if name == 'arxiv':
                    package = json.loads((root / 'paper/submission/arxiv_package_receipt.json').read_text())
                    source = root / 'paper/build/supplement.pdf'
                    destination = root / 'paper/submission/artifacts' / (
                        Path(package['release']).stem + '_Supplement.pdf')
                    shutil.copyfile(source, destination)
                    report['supplement'] = {'path': destination.relative_to(root).as_posix(), 'sha256': sha(destination)}
                print(f'PASS {name} ({time.monotonic()-start:.1f}s)', flush=True)
            check_assets(root)
            report['result'] = 'PASS'
        except Exception as exc:
            report['result'] = 'FAIL'
            report['error'] = str(exc)
            raise
        finally:
            receipt.write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-tool', type=Path, required=True,
                        help='local paper_build_release.py (no remote commands)')
    args = parser.parse_args()
    if args.release_tool.name != 'paper_build_release.py' or not args.release_tool.is_file():
        parser.error('--release-tool must name the local paper_build_release.py')
    refresh(ROOT, args.release_tool.resolve())
