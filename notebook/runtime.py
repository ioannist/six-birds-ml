"""Reader experiment: verified released evidence and explicitly separate live fits."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import html
import importlib.metadata
import io
import json
import logging
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import time

SOURCE_COMMIT = '3c35f5800d758db1fe9594b46648b16756c639f5'
SOURCE_URL = 'https://github.com/ioannist/six-birds-ml'
INSTALL_IF_MISSING = (('numpy', 'numpy'), ('scipy', 'scipy'), ('sklearn', 'scikit-learn'),
                      ('matplotlib', 'matplotlib'))


def find_repo(start):
    for p in (Path(start).resolve(), *Path(start).resolve().parents):
        if (p / 'paper/notes/claims_ledger.json').is_file() and (p / 'src').is_dir():
            return p
    return None


def table(headers, rows):
    from IPython.display import HTML, display
    def escaped(x):
        return html.escape(str(x))
    text = '<table><thead><tr>' + ''.join('<th>' + escaped(x) + '</th>' for x in headers)
    text += '</tr></thead><tbody>'
    text += ''.join('<tr>' + ''.join('<td>' + escaped(x) + '</td>' for x in row) + '</tr>' for row in rows)
    display(HTML(text + '</tbody></table>'))


def same_value(a, b, tolerance=1e-10):
    if isinstance(a, (float, int)) and isinstance(b, (float, int)):
        return abs(float(a) - float(b)) <= tolerance
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same_value(x, y, tolerance) for x, y in zip(a, b))
    return a == b


def checkout_identity(root):
    """Record the executing checkout, not the pin used by hosted setup."""
    def git(*args):
        return subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)

    try:
        top = git('rev-parse', '--show-toplevel')
        if top.returncode or Path(top.stdout.strip()).resolve() != root.resolve():
            return {'kind': 'source_directory', 'commit': None, 'working_tree_dirty': None}
        head = git('rev-parse', 'HEAD')
        status = git('status', '--porcelain', '--untracked-files=normal')
        return {'kind': 'git_checkout', 'commit': head.stdout.strip() if head.returncode == 0 else None,
                'working_tree_dirty': bool(status.stdout.strip()) if status.returncode == 0 else None}
    except OSError:
        return {'kind': 'source_directory', 'commit': None, 'working_tree_dirty': None}


class LowFontTimestampFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage() not in {
            "'created' timestamp seems very low; regarding as unix timestamp",
            "'modified' timestamp seems very low; regarding as unix timestamp",
        }


@contextlib.contextmanager
def quiet_font_timestamps():
    """Mute only the two harmless font-header timestamp diagnostics, locally."""
    logger = logging.getLogger('fontTools.ttLib.tables._h_e_a_d')
    timestamp_filter = LowFontTimestampFilter()
    logger.addFilter(timestamp_filter)
    try:
        yield
    finally:
        logger.removeFilter(timestamp_filter)


class Session:
    def __init__(self, mode='quick'):
        if mode not in ('quick', 'full'):
            raise ValueError('MODE must be quick or full')
        self.mode = mode
        self.fast = os.environ.get('SBML_NOTEBOOK_FAST') == '1'
        self.started = time.monotonic()
        self.timings = {}
        self.comparisons = []
        self.results = []
        self.versions = {}

    @contextlib.contextmanager
    def section(self, name):
        started = time.monotonic()
        yield
        self.timings[name] = time.monotonic() - started
        print(f'{name}: {self.timings[name]:.1f} seconds')

    def compare(self, label, observed, reference, *, strict=True, tolerance=1e-10, fresh_batch=False):
        match = same_value(observed, reference, tolerance)
        status = 'MATCH' if match else 'DIFFERENT: fresh measurement, not the saved paper run'
        if fresh_batch:
            status = "fresh measurement (different first batch; the paper's saved count is shown above)"
        self.comparisons.append({'label': label, 'observed': observed, 'ledger': reference,
                                 'match': match, 'required_match': strict,
                                 'comparison_kind': 'fresh_batch' if fresh_batch else 'paper_replay'})
        print(f'{label}: measured={observed}; ledger={reference}; {status}')
        if strict and not match:
            raise AssertionError(f'{label}: measured value differs from its ledger reference')
        return match

    def setup(self):
        with self.section('setup'):
            for key in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
                os.environ[key] = '1'
            configured = os.environ.get('SBML_REPO')
            self.root = find_repo(configured or Path.cwd())
            self.source_mode = 'local' if self.root is not None else 'hosted_pinned_clone'
            if configured and self.root is None:
                raise ValueError('SBML_REPO is not a scientific source checkout')
            if self.root is None:
                checkout = Path(tempfile.mkdtemp(prefix='sbml-source-')) / 'repository'
                subprocess.run(['git', 'clone', '--no-checkout', '--filter=blob:none', SOURCE_URL,
                                str(checkout)], check=True)
                subprocess.run(['git', 'checkout', '--detach', SOURCE_COMMIT], cwd=checkout, check=True)
                self.root = checkout
                # Hosted runtimes (e.g. Colab) already import their own numpy/matplotlib;
                # upgrading them mid-session mixes versions. Install only what is missing.
                from importlib.util import find_spec as _find_spec
                missing = [pkg for module, pkg in INSTALL_IF_MISSING
                           if _find_spec(module) is None]
                if missing:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', *missing], check=True)
            self.checkout = checkout_identity(self.root)
            import numpy as np
            import torch
            if torch.get_num_threads() != 1:
                torch.set_num_threads(1)
            requested = os.environ.get('SBML_DEVICE', 'auto')
            if requested not in ('auto', 'cpu', 'cuda'):
                raise ValueError('SBML_DEVICE must be auto, cpu or cuda')
            self.device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu')
                                       if requested == 'auto' else requested)
            if self.device.type == 'cuda' and not torch.cuda.is_available():
                raise ValueError('CUDA requested but unavailable')
            random.seed(0)
            np.random.seed(0)
            torch.manual_seed(0)
            if self.device.type == 'cuda':
                torch.cuda.manual_seed_all(0)
                torch.backends.cuda.matmul.allow_tf32 = False
                torch.backends.cudnn.allow_tf32 = False
            self.work = Path(os.environ.get('SBML_NOTEBOOK_OUTPUT', tempfile.mkdtemp(prefix='sbml-notebook-')))
            self.work.mkdir(parents=True, exist_ok=True)
            sys.path[:0] = [str(self.root), str(self.root / 'src'), str(self.root / 'paper/scripts')]
            import build_ledger
            self.ledger_module = build_ledger
            self.ledger = json.loads((self.root / 'paper/notes/claims_ledger.json').read_text())
            self.q = self.ledger['recomputed_outline_quantities']
            manifest = json.loads((self.root / 'paper/notes/evidence_manifest.json').read_text())
            self.evidence = build_ledger.Evidence(self.root, manifest)
            self.font_setup()
            for name in ('numpy', 'torch', 'scikit-learn', 'matplotlib'):
                self.versions[name] = importlib.metadata.version(name)
            print(f'Hosted source pin: {SOURCE_COMMIT}')
            print(f'Executing source: {self.source_mode}; actual commit={self.checkout["commit"]}; '
                  f'working tree modified={self.checkout["working_tree_dirty"]}')
            print(f'MODE={self.mode}; live device={self.device}; replay precision=CPU float32; threads=1')
            print('Package versions:', self.versions)
            print('SBML_DATA:', os.environ.get('SBML_DATA', 'repository evidence/bulk'))
            self.results.append(['Setup', str(self.device), 'Live device; released replays use CPU fp32'])

    def font_setup(self):
        # Only the font package is needed, not a TeX installation in Colab.
        if shutil.which('kpsewhich'):
            return
        candidates = [Path(os.environ.get('SBML_LATIN_MODERN', '')),
                      Path('/usr/share/texmf/fonts/opentype/public/lm/lmroman10-regular.otf')]
        if not any(p.is_file() for p in candidates) and os.environ.get('COLAB_RELEASE_TAG'):
            subprocess.run(['apt-get', 'update', '-qq'], check=True, stdout=subprocess.DEVNULL)
            subprocess.run(['apt-get', 'install', '-y', '-qq', 'fonts-lmodern'], check=True,
                           stdout=subprocess.DEVNULL)
        font = next((p for p in candidates if p.is_file()), None)
        if font is None:
            raise RuntimeError('Install fonts-lmodern (Linux), TeX Live, or set SBML_LATIN_MODERN to the font file')
        binary = self.work / 'bin'
        binary.mkdir(exist_ok=True)
        shim = binary / 'kpsewhich'
        shim.write_text('#!' + sys.executable + '\nimport sys\n'
                        + 'print(' + repr(str(font)) + " if sys.argv[1:] == ['lmroman10-regular.otf'] else '')\n")
        shim.chmod(0o755)
        os.environ['PATH'] = str(binary) + os.pathsep + os.environ.get('PATH', '')

    def verified_path(self, key):
        from recombination_promotion.public_paths import data_root
        if key.startswith('bulk/') and key not in self.evidence.entries:
            key = 'repo/evidence/' + key
        entry = self.evidence.entries[key]
        if key.startswith('repo/evidence/bulk/') and os.environ.get('SBML_DATA'):
            path = data_root() / key.removeprefix('repo/evidence/bulk/')
            if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('External checkpoint hash differs from released evidence')
            return path
        self.evidence.verify(entry)
        return self.evidence.path(entry)

    def read(self, key):
        return json.loads(self.verified_path(key).read_text())

    def task(self):
        import numpy as np
        import matplotlib.pyplot as plt
        from recombination_promotion.oldgame_ext import game, multiround as task
        with self.section('task'):
            self.boards = task.enumerate_boards()
            self.compare('All legal boards', len(self.boards.boards), self.q['task']['boards'])
            self.compare('L/N/H board counts', list(map(len, self.boards.by_category)), self.q['task']['category_counts'])
            self.compare('Local histories', len(game.histories()), self.q['task']['histories'])
            example = (2, 3, 4, 4)
            current = (game.sigma(example), 0, 0, 0, 0)
            rows = []
            for label, history in (('L → N', ((8, 0, 0, 0, 0), current)),
                                   ('H → N', ((36, 0, 0, 0, 0), current))):
                for board in history:
                    if board not in self.boards.placements:
                        raise AssertionError('witness board is not a legal four-record board')
                mode = 0
                for board in history:
                    mode = task.update_mode(mode, task.board_category(board))
                law = list(map(float, task.P[mode]))
                self.compare(label + ' law', law, self.q['task']['p1' if mode else 'p0'])
                rows.append([label, list(current), ('off', 'on')[mode], law])
            self.compare('Ideal prediction loss (bits)', task.oracle()['ideal_loss_bits'], self.q['task']['ideal_loss_bits'])
            self.compare('Same-board witness deficit (bits)', task.oracle()['witness_JS_bits'], self.q['task']['witness_JS_bits'])
            fig, axes = plt.subplots(1, 2, figsize=(10, 2.7))
            axes[0].bar(np.arange(1, 6), current, color=['#0072B2'] + ['#cccccc'] * 4)
            axes[0].set(xlabel='Slot', ylabel='Sum (twelfths)', title='Current round: four masses 2, 3, 4, 4')
            for row, color in zip(rows, ('#0072B2', '#D55E00')):
                axes[1].plot(('L', 'N', 'H'), row[-1], 'o-', label=row[0], color=color)
            axes[1].set(ylabel='Next-category probability', title='Same A, different B')
            axes[1].legend()
            fig.tight_layout()
            self.show(fig)
            table(['History', 'Final sums A', 'Final mode', 'Law over L/N/H'], rows)
            self.results.append(['Task', f'{len(self.boards.boards):,} boards', 'Exhaustive; ledger match'])

    def show(self, fig):
        from IPython.display import display
        import matplotlib.pyplot as plt
        display(self.figure_image(fig))
        plt.close(fig)

    @staticmethod
    def figure_image(fig):
        # Explicit PNG display works even when the kernel has no inline backend.
        from IPython.display import Image
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        return Image(data=buffer.getvalue())

    def paper_assets(self):
        from IPython.display import Image, display
        from asset_inputs import Inputs, verify_receipts
        from figure_assets import FIGURES, style
        from table_assets import TABLES
        with self.section('ledger and assets'), quiet_font_timestamps():
            result = subprocess.run([sys.executable, 'paper/scripts/build_ledger.py', '--check'],
                                    cwd=self.root, capture_output=True, text=True, check=True, timeout=1200)
            print(result.stdout)
            if 'outline mismatches 0' not in result.stdout:
                raise AssertionError('ledger did not verify all outline numbers')
            self.ctx = Inputs(self.root)
            style()
            previews = self.work / 'figures'
            previews.mkdir(exist_ok=True)
            for number in range(1, 6):
                name = f'fig{number}'
                asset = FIGURES[name](self.ctx, previews)
                receipt = json.loads((self.root / 'paper' / asset['file']).with_suffix('.values.json').read_text())
                verify_receipts(self.ctx, receipt)
                print(f'Figure {number}: rebuilt; every plotted receipt verified against ledger/evidence')
                display(Image(filename=str(previews / (name + '.png'))))
            asset = TABLES['table1'](self.ctx)
            receipt = json.loads((self.root / 'paper' / asset['file']).with_suffix('.values.json').read_text())
            verify_receipts(self.ctx, receipt)
            table(receipt['headers'], receipt['rows'])
            print('Table 1: rebuilt evidence-derived achievement cells (same definitions as the paper)')
            self.results.append(['Paper evidence', f'{len(self.ledger["claims"])} ledger entries', 'Recomputed; 0 outline mismatches'])

    def load_r8(self, seed, step):
        import torch
        from scripts import oldgame_multiround_route_access as r8
        from recombination_promotion.public_paths import identity_matches
        key = f'repo/{r8.OUTPUT.relative_to(self.root)}/raw_only_original_seed{seed}/checkpoint_step_{step:06d}.pt'
        path = self.verified_path(key)
        saved = torch.load(path, map_location='cpu', weights_only=False)
        if (saved['route'], saved['law'], saved['seed'], saved['step']) != ('raw_only', 'original', seed, step):
            raise AssertionError('checkpoint run identity differs')
        if not identity_matches(saved['registration_sha256'], r8.sha(r8.OUTPUT / 'registration.json')):
            raise AssertionError('checkpoint registration differs')
        model = r8.RouteNetwork('raw_only', seed, verify_source=False)
        model.load_state_dict(saved['model'], strict=True)
        return model.eval()

    def raw_probes(self, model):
        import torch
        from scripts import oldgame_multiround_route_access as r8
        split = self.read('repo/' + str(r8.OUTPUT.relative_to(self.root) / 'probe_split.json'))
        (train_records, train_y), (held_records, held_y) = r8._probe_data(split)
        with torch.no_grad():
            train = r8._carrier(model, train_records)[0]
            held = r8._carrier(model, held_records)[0]
        return [r8._fit_probe(train, train_y[:, k], held, held_y[:, k],
                              family='linear', seed=2026100802 + k) for k in range(5)]

    def released_networks(self):
        import torch
        import matplotlib.pyplot as plt
        from scripts import oldgame_multiround_route_access as r8
        from scripts import multiround_panels as panels
        with self.section('released probes and B replay'):
            probes = []
            b_rows = []
            natural, records, prefixes, lengths, meta = r8._panels('original')
            for seed in range(3):
                for step in (0, 20000):
                    model = self.load_r8(seed, step)
                    fits = self.raw_probes(model)
                    for slot, fit in enumerate(fits, 1):
                        expected = next(x['original']['endpoint_accuracy' if step else 'update0_accuracy']
                                        for x in self.q['r8_probes'] if x['seed'] == seed and x['slot'] == slot
                                        and x['carrier'] == 'raw' and x['probe_family'] == 'linear')
                        self.compare(f'r8 raw linear seed {seed} slot {slot} update {step}', fit['accuracy'], expected,
                                     strict=False)
                        probes.append({'seed': seed, 'step': step, 'slot': slot, **fit})
                    if step == 20000:
                        with torch.no_grad():
                            prediction, _ = panels.predict_panel(model, records, natural.lengths)
                            prefix, _ = panels.predict_panel(model, prefixes, lengths)
                        kl = r8._kl(prediction, natural, 'original')
                        law = panels.prefix_score(prefix, lengths, meta, equal=False)['maximum_TV']
                        self.compare(f'r8 natural KL seed {seed}', kl, self.q['r8_raw_KL'][seed],
                                     strict=False, tolerance=1e-7)
                        self.compare(f'r8 constructed law TV seed {seed}', law, self.q['r8_law_TV'][seed],
                                     strict=False, tolerance=1e-6)
                        b_rows.append([seed, kl, self.q['r8_raw_KL'][seed], law, self.q['r8_law_TV'][seed]])
            self.probes = probes
            rows = [[p['seed'], p['step'], p['slot'], f"{p['correct']}/{p['total']}", p['converged'], p['n_iter']]
                    for p in probes]
            table(['Seed', 'Update', 'Slot', 'Fresh held-out accuracy', 'Converged', 'Iterations'], rows)
            fig, axes = plt.subplots(1, 3, figsize=(11, 3))
            for seed in range(3):
                for step, style_ in ((0, '--'), (20000, '-')):
                    values = [p['accuracy'] for p in probes if p['seed'] == seed and p['step'] == step]
                    axes[0].plot(range(1, 6), values, style_, marker=('o', 's', '^')[seed],
                                 label=f'seed {seed}, {step}', alpha=.8)
            axes[0].axhline(1, color='k', linestyle=':', label='exact oracle')
            floors = [x['original']['majority_floor'] for x in self.q['r8_probes']
                      if x['seed'] == 0 and x['probe_family'] == 'linear' and x['carrier'] == 'raw']
            axes[0].plot(range(1, 6), floors, color='grey', linestyle=':', label='majority floor, seed 0')
            axes[0].set(xlabel='Slot', ylabel='Sum probe accuracy', title='Raw-state readability', ylim=(0, 1.05))
            axes[0].legend(fontsize=7, ncol=2, loc='upper center', bbox_to_anchor=(.5, -.27))
            axes[1].scatter(range(3), [r[1] for r in b_rows], color='#0072B2')
            axes[1].axhline(0, linestyle=':', color='k', label='oracle')
            axes[1].set(xlabel='Seed', ylabel='Natural KL (bits)', title='Low average prediction error')
            axes[2].scatter(range(3), [r[3] for r in b_rows], color='#D55E00')
            axes[2].axhline(.02, linestyle='--', color='k', label='registered bar')
            axes[2].axhline(0, linestyle=':', color='grey', label='oracle')
            axes[2].set(xlabel='Seed', ylabel='Maximum constructed law TV', title='Yet long-history failures')
            axes[2].legend(fontsize=7)
            fig.tight_layout()
            self.show(fig)
            table(['Seed', 'Fresh KL', 'Ledger KL', 'Fresh law TV', 'Ledger law TV'], b_rows)
            self.results.append(['Released r8', str([p['correct'] for p in probes if p['step'] == 20000 and p['slot'] == 1]) + '/512',
                                 'Refitted raw linear probes, seeds 0–2; convergence recorded'])

    def census(self):
        import torch
        import matplotlib.pyplot as plt
        from scripts import oldgame_multiround_jagged as r11
        with self.section('board census'):
            path = self.verified_path('bulk/study_r12_coverage_bulk/a_target_original_seed0/checkpoint_step_020000.pt')
            saved = torch.load(path, map_location='cpu', weights_only=False)
            model = r11.new_model(0, False, repo_root=self.root)
            model.load_state_dict(saved['model'], strict=True)
            model.eval()
            census = r11.board_census(model, 'original', torch.device('cpu'))
            source = self.read('repo/reports/phase11/oldgame_memory/multiround/study_r12_coverage/aggregate.json')
            expected = source['runs']['a_target_original_seed0']['census_all_four_renderings_and_r9']
            if census['registered_rendering']['categorical_misreads'] != expected['registered_rendering']['categorical_misreads']:
                print('Fresh fp32 replay has a numerical difference from the saved audit; both are retained.')
            first = census['registered_rendering']
            observed = first['categorical_misreads']
            self.compare('r12 sums-target seed 0 census misreads', observed, self.q['r12_target_misreads'][0], strict=False)
            values = first['by_slot1_sum_twelfths']
            fig, ax = plt.subplots(figsize=(9, 2.8))
            keys = sorted(values, key=int)
            ax.bar(list(map(int, keys)), [values[k]['categorical_misreads'] for k in keys], color='#0072B2')
            for left, right in ((11, 13), (23, 25)):
                ax.axvspan(left - .5, right + .5, alpha=.15, color='#D55E00')
            ax.set(xlabel='Slot-1 sum (twelfths); shaded bands 11–13 and 23–25',
                   ylabel='Categorical misreads (count)', title='r12 records → prediction+sums, seed 0: exhaustive boards')
            fig.tight_layout()
            self.show(fig)
            renderings = [first] + census['additional_fixed_renderings']
            table(['Rendering', 'Boards', 'Categorical misreads', 'Probability TV > 0.02'],
                  [[r['rendering'], r['boards'], r['categorical_misreads'], r['above_0_02_TV']] for r in renderings])
            def band_counts(rows):
                bands = ([], [])
                for key, row in rows.items():
                    bands[0 if 11 <= int(key) <= 13 or 23 <= int(key) <= 25 else 1].append(row)
                return [[sum(r['categorical_misreads'] for r in group), sum(r['boards'] for r in group)]
                        for group in bands]
            actual_bands = band_counts(values)
            self.compare('r12 cutoff-band and complement census counts', actual_bands,
                         band_counts(expected['registered_rendering']['by_slot1_sum_twelfths']))
            table(['Region', 'Misreads / boards', 'Misread fraction'],
                  [[label, f'{wrong}/{total}', f'{wrong / total:.3%}']
                   for label, (wrong, total) in zip(('11–13 and 23–25', 'Other slot-1 sums'), actual_bands)])
            uniform = source['runs']['uniform_original_seed0']['census_all_four_renderings_and_r9']['registered_rendering']
            print('Separate saved paper Fig. 3(f) provenance: r12 uniform records → prediction, seed 0:',
                  uniform['categorical_misreads'], '/', uniform['boards'], 'misreads; not a fresh checkpoint replay.')
            self.census_result = census
            self.results.append(['Released r12 census', f'{observed}/{first["boards"]}', 'Fresh categorical misreads; four renderings; TV counts separate'])

    def evaluate_live(self, model, count):
        import torch
        from scripts import oldgame_multiround_route_access as r8
        from scripts import multiround_scoring as scoring
        from recombination_promotion.oldgame_ext.multiround import P
        panel, records, _, _, _ = r8._panels('original')
        probabilities = []
        with torch.no_grad():
            for at in range(0, count, 64):
                _, logits = model(torch.tensor(records[at:at + 64], device=self.device),
                                  torch.tensor(panel.lengths[at:at + 64].astype('int64'), device=self.device))
                probabilities.append(logits.softmax(-1).cpu())
        p = torch.cat(probabilities).numpy()[:count]
        active = scoring._active(panel)[:count]
        import numpy as np
        exact = np.asarray(P, dtype=float)[panel.modes[:count][active]]
        return float((exact * np.log2(exact / np.clip(p[active], 1e-12, 1))).sum(-1).mean())

    def train_live(self):
        import torch
        from torch.nn import functional as F
        import matplotlib.pyplot as plt
        from IPython.display import display
        from recombination_promotion.oldgame_ext.multiround_jagged import BoardTables, DeviceStream, new_model
        from scripts import oldgame_multiround_jagged as r11
        with self.section('live training and audit'):
            steps = 20000 if self.mode == 'full' else (1000 if self.device.type == 'cuda' else 400)
            if self.fast:
                steps = 25
            batch_size = 16 if self.fast else (256 if self.mode == 'full' or self.device.type == 'cuda' else 64)
            model = new_model(0, False).to(self.device)
            model.memory.requires_grad_(False)
            optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=.003, weight_decay=.01)
            tables = BoardTables(self.device, self.boards)
            self.device_tables = tables
            stream = DeviceStream(tables, 0, 'original', 'uniform', batch=batch_size)
            cadence = max(1, steps // 10)
            curves = []
            fig, axes = plt.subplots(1, 2, figsize=(9, 2.5))
            handle = display(self.figure_image(fig), display_id=True)
            training_seconds = 0.0
            for step in range(steps + 1):
                if step:
                    update_started = time.monotonic()
                    model.train()
                    batch = stream.draw_batch()
                    optimizer.zero_grad(set_to_none=True)
                    _, logits = model(batch.records, batch.lengths)
                    loss = F.cross_entropy(logits[batch.active], batch.targets[batch.active])
                    if not torch.isfinite(loss):
                        raise ValueError('non-finite live loss')
                    loss.backward()
                    if any(p.grad is not None for p in model.memory.parameters()):
                        raise AssertionError('prediction-only raw run sent a gradient into the sums core')
                    optimizer.step()
                    training_seconds += time.monotonic() - update_started
                if step % cadence == 0 or step == steps:
                    model.eval()
                    kl = self.evaluate_live(model, 128 if self.fast else 512)
                    curves.append({'step': step, 'prediction_loss_nats': None if step == 0 else float(loss.detach()),
                                   'natural_KL_bits': kl, 'test_episodes': 128 if self.fast else 512})
                    for ax in axes:
                        ax.clear()
                    axes[0].plot([r['step'] for r in curves[1:]], [r['prediction_loss_nats'] for r in curves[1:]], 'o-')
                    axes[0].axhline(1.5 * __import__('math').log(2), linestyle=':', color='grey', label='ideal expected floor')
                    axes[0].set(xlabel='Fresh updates', ylabel='Prediction loss (nats)')
                    axes[1].plot([r['step'] for r in curves], [r['natural_KL_bits'] for r in curves], 'o-')
                    axes[1].axhline(.01, linestyle='--', color='grey', label='paper bar')
                    axes[1].set(xlabel='Fresh updates', ylabel='Natural KL (bits)',
                                title=f'{128 if self.fast else 512} fixed test episodes')
                    for ax in axes:
                        ax.legend(fontsize=7)
                    fig.tight_layout()
                    if handle is not None:
                        handle.update(self.figure_image(fig))
                    print(f'live update {step}/{steps}: natural KL={kl:.6g} bits')
            plt.close(fig)
            model = model.cpu().eval()
            fits = self.raw_probes(model)
            with torch.no_grad():
                census = r11.board_census(model, 'original', torch.device('cpu'), smoke=True)
            table(['Slot', 'Held-out sum probe', 'Converged'],
                  [[i + 1, f"{r['correct']}/{r['total']}", r['converged']] for i, r in enumerate(fits)])
            print('Reduced census:', census['registered_rendering']['categorical_misreads'], '/',
                  census['registered_rendering']['boards'], 'misreads; this is not an exhaustive paper census.')
            self.live = {'steps': steps, 'batch': batch_size, 'lr': .003, 'weight_decay': .01,
                         'seed': 0, 'sum_loss_coefficient': 0, 'curve': curves, 'probes': fits,
                         'stream': stream.state()['rolling'], 'census': census,
                         'training_seconds': training_seconds, 'updates_per_second': steps / training_seconds}
            print(f'Live training: {steps / training_seconds:.1f} updates/s; audits and fitting excluded')
            torch.save({'model': model.state_dict(), 'settings': {k: self.live[k] for k in ('steps', 'batch', 'lr', 'weight_decay', 'seed')},
                        'optimizer': optimizer.state_dict(), 'stream': stream.state()}, self.work / 'live_final.pt')
            self.results.append(['Fresh training', f'{steps} updates, KL {curves[-1]["natural_KL_bits"]:.6g}', 'New short run, not a paper endpoint'])

    def erosion(self):
        import torch
        from recombination_promotion.oldgame_ext.multiround_jagged import BoardTables, DeviceStream, new_model
        from recombination_promotion.oldgame_ext.multiround_mechanism import histories_logits, margin_counts
        from scripts.oldgame_multiround_mechanism import erosion_step
        from figure_assets import run13
        with self.section('one-update erosion'):
            # Canonical CPU replay for the fresh minibatch, explicitly distinct
            # from the historical CUDA sample stream.
            base = new_model(0, True, repo_root=self.root)
            for p in base.memory.parameters():
                p.requires_grad_(True)
            with torch.no_grad():
                first = margin_counts(histories_logits(base.memory))['correct']
            self.compare('Exact parent local sums', first, self.q['task']['histories'])
            batch = DeviceStream(BoardTables(torch.device('cpu'), self.boards), 0, 'original', 'uniform').draw_batch()
            rows = []
            for condition, label in (('adam', 'AdamW'), ('reduced', 'reduced-lr AdamW'),
                                     ('sgd', 'SGD matched first displacement'), ('blocked', 'blocked gradient + weight decay')):
                model = copy.deepcopy(base)
                optimizer = torch.optim.AdamW(model.memory.parameters(), lr=.0003 if condition == 'reduced' else .003, weight_decay=.01)
                other = torch.optim.AdamW([p for n, p in model.named_parameters() if not n.startswith('memory.')], lr=.003, weight_decay=.01)
                erosion_step(model, batch, optimizer, other, blocked=condition == 'blocked', sgd=condition == 'sgd')
                with torch.no_grad():
                    correct = margin_counts(histories_logits(model.memory))['correct']
                key = run13(self.ctx, 'erosion', condition, 0)
                records, _ = self.ctx.referenced(self.ctx.sources['control']['13'][key]['records'])
                paper = next(r['local']['correct'] for r in records if r['step'] == 1)
                curve = self.ctx.ref('control', '13', key, 'accuracy_curve')
                expected = next(r[1] for r in curve if r[0] == 1)
                self.compare(label + ' paper update-1 record', paper, expected)
                self.compare(label + ' fresh CPU update-1', correct, expected,
                             strict=condition == 'blocked', fresh_batch=True)
                rows.append([label, first, correct, paper, self.q['task']['histories']])
            table(['Condition', 'Exact start', 'Fresh CPU update 1', 'Paper CUDA update 1, seed 0', 'Denominator'], rows)
            self.erosion_rows = rows
            self.results.append(['Erosion', str([r[2] for r in rows]), 'Fresh CPU counts; historical CUDA counts shown separately'])

    def mechanisms(self):
        import matplotlib.pyplot as plt
        with self.section('released access and encoding'):
            recorded = json.loads((self.root / 'paper/data/reported_outline_quantities.json').read_text())
            for key in ('r13_access', 'r13_encoding'):
                if recorded[key] != self.q[key]:
                    raise AssertionError('reported mechanism numbers differ from the ledger')
            access = self.q['r13_access']
            encoding = self.q['r13_encoding']
            fig, axes = plt.subplots(1, 3, figsize=(12, 3))
            conditions = ('disconnected', 'frozen', 'live', 'exact')
            labels = ('Disconnected', 'Connected (frozen)', 'Connected (live)', 'Exact sums supplied')
            for seed in range(3):
                axes[0].plot(range(4), [access[c][seed]['long_TV'] for c in conditions], 'o-', label=f'seed {seed}')
                axes[1].plot(range(4), [access[c][seed]['categorical_misreads'] for c in conditions],
                             'o-', label=f'seed {seed}')
                axes[2].plot(range(2), [encoding[c][seed] for c in ('onehot', 'numerical')], 'o-', label=f'seed {seed}')
            for ax in axes[:2]:
                ax.set_xticks(range(4), ('Disconnected', 'Connected\n(frozen)', 'Connected\n(live)', 'Exact sums\nsupplied'))
            axes[0].set(ylabel='Maximum long-panel law TV', title='Access affects prediction errors')
            axes[0].axhline(.02, color='k', linestyle='--', label='registered bar')
            axes[1].set(ylabel='Categorical misreads / 24,435 boards', title='Connection affects census errors')
            axes[2].set_xticks(range(2), ('One-hot sums', 'Numerical sums'))
            axes[2].set(ylabel='Categorical misreads / 24,435 boards', title='Encoding changes census errors')
            for ax in axes:
                ax.axhline(0, color='grey', linestyle=':', label='exact oracle')
                ax.legend(fontsize=7)
            fig.tight_layout()
            self.show(fig)
            table(['Condition', 'Seed', 'Ledger natural KL', 'Ledger long TV',
                   'Ledger categorical misreads / 24,435', 'Endpoint (all bars)'],
                  [[label, s, access[c][s]['KL_bits'], access[c][s]['long_TV'],
                    access[c][s]['categorical_misreads'], access[c][s]['endpoint_label']]
                   for c, label in zip(conditions, labels) for s in range(3)])
            self.compare('Numerical encoding misreads, seeds 0–2', recorded['r13_encoding']['numerical'], encoding['numerical'])
            self.compare('One-hot encoding misreads, seeds 0–2', recorded['r13_encoding']['onehot'], encoding['onehot'])
            print('Takeaway: access and encoding change measured errors, but neither guarantees all prediction criteria.')
            self.results.append(['Released mechanisms', str(encoding), 'Ledger values, seeds shown separately; no new fitting'])

    def study_commands(self):
        commands = [
            ('r8', 'PYTHONPATH=src:. python -m scripts.oldgame_multiround_route_access run --route raw_only --law original --seed 0 --output-root build/full-studies/r8', '20k; CPU-era implementation'),
            ('r9', "PYTHONPATH=src:. python -c \"from pathlib import Path; from scripts import oldgame_multiround_raw_diagnosis as d; d.OUTPUT=Path('build/full-studies/r9'); d.main()\"", 'Inference only; fixed released checkpoints'),
            ('r10', 'PYTHONPATH=src:. python -m scripts.oldgame_multiround_allslots run --device cuda --arm free --law original --seed 0 --output-root build/full-studies/r10 --bulk-root build/full-bulk/r10', '20k; run verify-gpu first'),
            ('r11', 'PYTHONPATH=src:. python -m scripts.oldgame_multiround_jagged run --device cuda --runs rarity --chunk-runs 3 --output-root build/full-studies/r11', '20k; registered seed/condition groups'),
            ('r12', 'PYTHONPATH=src:. python -m scripts.oldgame_multiround_coverage --stage run --device cuda --runs rarity --chunk-runs 3 --output-root build/full-studies/r12 --bulk-root build/full-bulk/r12', '20k; 50/50 natural/coverage'),
            ('r13', 'PYTHONPATH=src:. python -m scripts.oldgame_multiround_mechanism --stage run --device cuda --experiment full --process 0 --output-root build/full-studies/r13 --bulk-root build/full-bulk/r13', '20k; erosion separately 200 updates'),
        ]
        print('Set CUDA_VISIBLE_DEVICES to your chosen accelerator; set OMP/MKL/OPENBLAS_NUM_THREADS=1.')
        print('Example commands are not executed. notebook/README.md lists the complete conditions, controls and seeds; '
              'each study registration fixes the endpoint and criteria.')
        table(['Study', 'Command', 'Endpoint / scope'], commands)
        print('GPU wall time depends on hardware and audits; no T4 full-fleet measurement is available.')
        print('The session records its live throughput below. r8 is CPU-era; r9 is inference; r10–r13 use one visible GPU.')
        self.full_commands = commands
        records = json.loads((self.root / 'paper/data/compute_records.json').read_text())
        compute_rows = []
        for study in (8, 9, 10, 11, 12, 13):
            rows = [r for r in records if r['study'] == study]
            seconds = []
            for r in rows:
                entry = next(a for a in self.evidence.entries.values() if a['id'] == r['evidence_id'])
                self.evidence.verify(entry)
                measurements = r['measurements']
                elapsed = measurements.get('elapsed_seconds', measurements.get('elapsed_group_seconds'))
                if elapsed is not None:
                    seconds.append(elapsed)
                elif 'training_seconds' in measurements:
                    audits = measurements.get('audit_seconds', 0)
                    seconds.append(measurements['training_seconds'] + (sum(audits) if isinstance(audits, list) else audits))
            compute_rows.append([f'r{study}',
                f'{min(seconds)/60:.1f}–{max(seconds)/60:.1f} minutes' if seconds else 'Not recorded in this table',
                'Available per-run/group records (r13: erosion only); not a full-fleet or T4 estimate'])
        table(['Study', 'Recorded compute range', 'Qualification'], compute_rows)
        print(f'Fresh training rate here: {self.live["updates_per_second"]:.1f} updates/s; '
              f'20k live updates alone ≈{20000/self.live["updates_per_second"]/60:.1f} minutes on this device, excluding all study audits.')

    def finish(self):
        elapsed = time.monotonic() - self.started
        table(['Section', 'Computed result', 'Scope'], self.results)
        receipt = {'mode': self.mode, 'fast_test': self.fast, 'hosted_source_pin': SOURCE_COMMIT,
                   'execution_source': self.source_mode, 'checkout_identity': self.checkout,
                   'ledger_sha256': hashlib.sha256((self.root / 'paper/notes/claims_ledger.json').read_bytes()).hexdigest(),
                   'device': str(self.device), 'versions': self.versions, 'elapsed_seconds': elapsed,
                   'section_seconds': self.timings, 'comparisons': self.comparisons,
                   'summary': self.results, 'live': self.live, 'erosion': self.erosion_rows,
                   'released_probes': self.probes}
        path = self.work / 'session_results.json'
        path.write_text(json.dumps(receipt, indent=2, allow_nan=False) + '\n')
        print(f'COMPLETE: {len(self.results)} result rows; {len(self.comparisons)} ledger comparisons; {elapsed:.1f} seconds')
        print('Receipt:', path)
        from IPython.display import FileLink, display
        display(FileLink(str(path)))
        if 'google.colab' in sys.modules:
            from google.colab import files
            files.download(str(path))
