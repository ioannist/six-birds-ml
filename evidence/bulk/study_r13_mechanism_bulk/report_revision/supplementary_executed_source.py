"""Read-only r13 reporting and predeclared saved-checkpoint cutoff analysis.

Training operations are unchanged; the original instrument remains an archived
executed authority. This analysis has its own source and identity bindings.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import shutil
import time
from pathlib import Path

import numpy as np
import torch

from scripts import oldgame_multiround_mechanism as study
from recombination_promotion.oldgame_ext.mechanism_geometry import (
    discrimination_decision, score_pair_discrimination,
)


OUTPUT = study.OUTPUT
STAGING = study.ROOT / 'evidence/bulk/study_r13_mechanism_bulk/report_revision'
DESTINATION = study.BULK / 'report_revision'
CONCLUSION = ('Target noise, access and encoding affect measured errors; none alone '
              'guarantees B closure, and erosion is gradient-mediated without being uniquely Adam-specific.')


def reference(path):
    path = study.public_path(path).resolve()
    row = {'path': str(path), 'sha256': study.r11.sha(path), 'bytes': path.stat().st_size}
    if path.is_relative_to(STAGING):
        row['host_bulk_path'] = str(DESTINATION / path.relative_to(STAGING))
    return row


def load(ref):
    return study.load_reference(ref)


def publish(path, row):
    study.r11.write_json(path, row)
    return reference(path)


def recorded_registration():
    """Authenticate completed training; only the report entry may differ now."""
    import ast
    reg = json.loads((OUTPUT / 'registration.json').read_text())
    current = study.identities()
    for key, digest in reg['source_sha256'].items():
        if key != 'script' and current[key] != digest:
            raise ValueError('recorded training dependency differs: ' + key)
    archive = STAGING / 'training_executed_source.py'
    if study.r11.sha(archive) != reg['source_sha256']['script']:
        raise ValueError('recorded training source digest differs')
    def training_body(path):
        tree = ast.parse(path.read_text())
        tree.body = [n for n in tree.body if not (isinstance(n, ast.FunctionDef) and n.name == 'aggregate')]
        return ast.dump(tree)
    if training_body(archive) != training_body(Path(study.__file__)):
        raise ValueError('non-report training code differs from the executed instrument')
    if reg['settings'] != study.settings() or reg['specification_verbatim'] != study.SPEC.read_text():
        raise ValueError('recorded settings or registered readings differ')
    calibration = json.loads((OUTPUT / 'calibration.json').read_text())
    if calibration['registration_sha256'] != study.r11.sha(OUTPUT / 'registration.json'):
        raise ValueError('recorded calibration binding differs')
    return reg


def panel_pairs(boards, probe_heldout):
    """All legal matched pairs, sorted before states; no accuracy-dependent choice."""
    lookup = {b: i for i, b in enumerate(boards)}
    rows = []
    for a, b in ((12, 13), (23, 24)):
        pairs = [[i, lookup[(b, *board[1:])]] for i, board in enumerate(boards)
                 if board[0] == a and (b, *board[1:]) in lookup]
        eligible = [p for p in pairs if not set(p) & set(probe_heldout)]
        fitting = eligible[:len(eligible) // 2]
        selected = {tuple(p) for p in fitting}
        evaluation = [p for p in pairs if tuple(p) not in selected]
        fit_ids = {i for p in fitting for i in p}
        held_ids = {i for p in evaluation for i in p}
        if not fitting or not evaluation or fit_ids & held_ids or fit_ids & set(probe_heldout):
            raise ValueError('supplementary legal pair support or separation fails')
        rng = np.random.default_rng(130016 + a)
        rows.append({'sums': [a, b], 'legal_pairs': len(pairs),
                     'train_pairs': fitting, 'heldout_pairs': evaluation,
                     'label_permutation': rng.permutation(2 * len(fitting)).tolist()})
    return rows


def rendering_hash(records):
    import hashlib
    return hashlib.sha256(np.ascontiguousarray(records).tobytes()).hexdigest()


def declare(output=OUTPUT):
    """No checkpoint states are opened by this stage."""
    reg = recorded_registration()
    boards = study.r11.enumerate_boards()
    split_path = study.r11.r8.OUTPUT / 'probe_split.json'
    split = json.loads(split_path.read_text())
    rows = panel_pairs(boards.boards, split['heldout_board_ids'])
    hashes = {}
    for name, key in (('train', 'train_pairs'), ('heldout', 'heldout_pairs')):
        ids = sorted({i for row in rows for p in row[key] for i in p})
        hashes[name] = {'board_ids': ids, 'renderings': []}
        for rendering in range(4):
            records = study.r11._census_records(boards, np.array(ids), render_offset=rendering)
            hashes[name]['renderings'].append({'rendering': rendering,
                'records_sha256': rendering_hash(records), 'shape': list(records.shape),
                'dtype': str(records.dtype)})
    path = output / 'supplementary_cutoff_panel.json'
    source_hash = study.r11.sha(Path(__file__))
    if path.exists():
        retained_hash = json.loads(path.read_text())['analysis_source_sha256']
        if retained_hash != source_hash:
            # Report formatting may change after capture. The executed capture
            # source stays archived, and its identity-selection/extraction code
            # must still be identical to the current analysis implementation.
            import ast
            archived = STAGING / 'supplementary_executed_source.py'
            if study.r11.sha(archived) != retained_hash:
                raise ValueError('supplementary executed source digest differs')
            def functions(file):
                return {f.name: ast.dump(f) for f in ast.parse(file.read_text()).body
                        if isinstance(f, ast.FunctionDef)}
            before, after = functions(archived), functions(Path(__file__))
            for name in ('panel_pairs', 'rendering_hash', 'extract'):
                if before[name] != after[name]:
                    raise ValueError('supplementary executed computation differs')
            source_hash = retained_hash
    row = {'scope': 'Supplementary cutoff geometry; no training or endpoint changes.',
           'registration_sha256': study.r11.sha(output / 'registration.json'),
           'analysis_source_sha256': source_hash,
           'training_source_sha256': reg['source_sha256'],
           'review': reference(output / 'analysis_specification.json'),
           'probe_split': reference(split_path), 'pairs': rows, 'inputs': hashes,
           'checkpoints': [0, 5000, 20000],
           'conditions': ['raw_sampled', 'raw_probability'], 'seeds': [0, 1, 2],
           'choices': ['All legal pairs with identical other four slot sums, sorted by board ID.',
                       'First half of pairs without any probe-held-out endpoint fit; all remaining pairs evaluate.',
                       'All four fixed census renderings; discrimination fits and scores rendering 0 only.',
                       'Means/scales use fitting identities only; distances are descriptive.',
                       'Fixed seed-130016+lower-sum training-label permutation; no support resampling.',
                       'Use the unchanged calibrated pair scorer and thresholds; report failed decisions.']}
    if path.exists() and json.loads(path.read_text()) != row:
        raise ValueError('supplementary panel binding differs; do not replace after states')
    publish(path, row)
    return reference(path)


def compact_geometry(geometry):
    supported, missing = [], []
    for row in geometry['rows']:
        base = {k: row[k] for k in ('sums', 'status', 'train_pairs', 'heldout_pairs')}
        if row['status'] == 'MISSING_SUPPORT':
            missing.append(base)
        else:
            base.update({k: row[k] for k in ('discrimination', 'distance_mean',
                                            'distance_quantiles', 'rerender_distance_mean')})
            for key in ('reader', 'label_permutation_floor'):
                base[key] = {k: row[key][k] for k in ('accuracy', 'correct', 'total',
                    'cross_entropy_nats', 'converged', 'n_iter')}
            supported.append(base)
    return {'measured_rows': len(supported), 'missing_support_rows': len(missing),
            'measured': supported, 'missing_sums': [r['sums'] for r in missing],
            'cutoff_missing': [r for r in missing if r['sums'] in ([12, 13], [23, 24])]}


def extract(output=OUTPUT, staging=STAGING):
    start = time.monotonic()
    panel_path = output / 'supplementary_cutoff_panel.json'
    panel = json.loads(panel_path.read_text())
    # Rebuild the identity-only declaration before opening any checkpoint.
    if declare(output)['sha256'] != study.r11.sha(panel_path):
        raise ValueError('supplementary declaration changed')
    boards = study.r11.enumerate_boards()
    ids = {key: panel['inputs'][key]['board_ids'] for key in ('train', 'heldout')}
    inputs = {}
    for key in ids:
        inputs[key] = []
        for rendering in range(4):
            records = study.r11._census_records(boards, np.array(ids[key]), render_offset=rendering)
            if rendering_hash(records) != panel['inputs'][key]['renderings'][rendering]['records_sha256']:
                raise ValueError('supplementary executed rendering differs')
            inputs[key].append(torch.from_numpy(records))
    results = []
    staging.mkdir(parents=True, exist_ok=True)
    for condition, seed, step in itertools.product(panel['conditions'], panel['seeds'], panel['checkpoints']):
        run = study.Run('noise', condition, seed)
        summary = json.loads((output / run.name / 'summary.json').read_text())
        checkpoint = Path(summary['bulk_directory']) / f'checkpoint_step_{step:06d}.pt'
        saved = study.r12._bound_load(checkpoint)
        if saved['authority'] != summary['authority'] or saved['step'] != step or \
                saved['authority']['registration_sha256'] != panel['registration_sha256']:
            raise ValueError('supplementary checkpoint authority differs')
        model = study.MechanismNetwork(condition).eval()
        model.load_state_dict(saved['model'], strict=True)
        arrays = {}
        with torch.no_grad():
            for key in ids:
                arrays[key] = [torch.cat([model.raw_state(x[a:a + 256])
                    for a in range(0, len(x), 256)]) for x in inputs[key]]
        mean, scale = arrays['train'][0].mean(0), arrays['train'][0].std(0, unbiased=False)
        scale = torch.where(scale == 0, 1, scale)
        features = {key: [(x - mean) / scale for x in xs] for key, xs in arrays.items()}
        feature_path = staging / f'{run.name}_step_{step:06d}_cutoff.npz'
        np.savez_compressed(feature_path, mean=mean.numpy(), scale=scale.numpy(),
            **{f'{key}_{r}': x.numpy() for key, xs in arrays.items() for r, x in enumerate(xs)})
        lookups = {key: {i: at for at, i in enumerate(v)} for key, v in ids.items()}
        measured = []
        for pairs in panel['pairs']:
            def data(key, pair_key):
                identities = [i for p in pairs[pair_key] for i in p]
                indices = [lookups[key][i] for i in identities]
                return features[key][0][indices], torch.tensor([0, 1] * len(pairs[pair_key])), identities
            x, y, train_ids = data('train', 'train_pairs')
            z, w, held_ids = data('heldout', 'heldout_pairs')
            kwargs = {'train_ids': train_ids, 'heldout_ids': held_ids, 'seed': 130014}
            positive = score_pair_discrimination(x, y, z, w, **kwargs)
            negative = score_pair_discrimination(x, y[pairs['label_permutation']], z, w, **kwargs)
            distances = (z[::2] - z[1::2]).norm(dim=-1) / math.sqrt(z.shape[-1])
            indices = [lookups['heldout'][i] for i in held_ids]
            variations = torch.cat([(features['heldout'][r][indices] - z).norm(dim=-1)
                                    / math.sqrt(z.shape[-1]) for r in (1, 2, 3)])
            measured.append({'sums': pairs['sums'], 'status': 'MEASURED',
                'train_pairs': len(pairs['train_pairs']), 'heldout_pairs': len(pairs['heldout_pairs']),
                'reader': positive, 'label_permutation_floor': negative,
                'discrimination': discrimination_decision(positive, [negative]),
                'distance_mean': float(distances.mean()),
                'distance_quantiles': torch.quantile(distances, torch.tensor([0., .5, 1.])).tolist(),
                'rerender_distance_mean': float(variations.mean())})
        results.append({'run': run.__dict__, 'step': step, 'checkpoint': reference(checkpoint),
                        'features': reference(feature_path), 'rows': measured})
        print(f'CUT_OFF {run.name} step={step} ' + ' '.join(
            f"{r['sums']}={r['reader']['correct']}/{r['reader']['total']} "
            f"CE={r['reader']['cross_entropy_nats']:.6f} pass={r['discrimination']['pass']}"
            for r in measured), flush=True)
    details = publish(staging / 'supplementary_cutoff_details.json', results)
    report = {'panel': reference(panel_path), 'details': details,
              'elapsed_seconds': time.monotonic() - start,
              'rows': [{**{k: r[k] for k in ('run', 'step', 'checkpoint', 'features')},
                        **compact_geometry(r)} for r in results]}
    publish(output / 'supplementary_cutoff_results.json', report)
    return report


def census_counts(census):
    panels = [census['registered_rendering'], *census['additional_fixed_renderings']]
    result = []
    for rendering, panel in enumerate(panels):
        counts = {key: {'boards': 0, 'categorical_misreads': 0, 'prediction_TV_errors': 0}
                  for key in ('cutoff', 'complement')}
        for value, row in panel['by_slot1_sum_twelfths'].items():
            band = 'cutoff' if int(value) in (11, 12, 13, 23, 24, 25) else 'complement'
            counts[band]['boards'] += row['boards']
            if row['categorical_misreads'] is None:
                counts[band]['categorical_misreads'] = None
            elif counts[band]['categorical_misreads'] is not None:
                counts[band]['categorical_misreads'] += row['categorical_misreads']
            counts[band]['prediction_TV_errors'] += row['above_0_02_TV']
        assert sum(v['boards'] for v in counts.values()) == panel['boards']
        result.append({'rendering': rendering, **counts,
                       'categorical_misreads': panel['categorical_misreads'],
                       'prediction_TV_errors': panel['above_0_02_TV'],
                       'category_status': panel['category_status']})
    return result


def failed_b_bars(audit, law):
    criteria = audit['criteria']
    values = {'natural_KL': {'value': audit['natural_excess_KL_bits'], 'bound': .01},
              'unseen_KL': {'value': audit['unseen_excess_KL_bits'], 'bound': .01,
                            'count': audit['unseen_count']},
              'witness': {'value': audit['mode_law']['witness_pair_mean_prediction_TV'] if law == 'equal'
                          else audit['mode_law']['witness_recovery_fraction'],
                          'bound': .02 if law == 'equal' else .8,
                          'relation': '<=' if law == 'equal' else '>='},
              'law_TV': {'value': audit['mode_law']['maximum_TV'], 'bound': .02,
                         'cases': audit['mode_law']['cases']},
              'swaps': {'bound': .02, 'cases': {k: v for k, v in audit['swaps']['cases'].items()
                  if k in ('reset_L', 'set_H', 'neutral_N', 'same_category_substitution',
                           'upper_state_exchange_same_N')}},
              'rerender': audit['rerender']}
    return {key: values[key] for key, passed in criteria.items() if not passed}


def erosion_comparison(rows):
    active = ('adam', 'sgd', 'reduced')
    output = []
    for seed in range(3):
        curves = {r['run']['condition']: r for r in rows if r['run']['seed'] == seed}
        ranges = {}
        for names in (*itertools.combinations(active, 2), active):
            low = max(curves[c]['trajectory'][0]['cumulative_path'] for c in names)
            high = min(curves[c]['trajectory'][-1]['cumulative_path'] for c in names)
            ranges['--'.join(names)] = {'range': [low, high], 'curves': {
                c: [r for r in curves[c]['trajectory'] if low <= r['cumulative_path'] <= high]
                for c in names}}
        output.append({'seed': seed, 'observed_ranges': ranges,
                       'blocked_control': curves['blocked'],
                       'scope': 'Recorded points only, no interpolation or retrospective SGD adjustment.'})
    return output


def erosion_summary(rows):
    trajectory = [{k: r[k] for k in ('step', 'cumulative_path')} | {
        'correct': r['local']['correct'], 'total': r['local']['total'],
        'displacement_from_initialization': r.get('displacement_from_initialization', 0)} for r in rows]
    margins = [{'step': r['step'], 'quantiles': np.quantile(r['local']['margins'], [0, .1, .5, .9, 1]).tolist(),
                'nonpositive': sum(v <= 0 for v in r['local']['margins']),
                'total': r['local']['total'], 'first_flips': len(r.get('first_flips', []))} for r in rows]
    names = sorted(rows[-1].get('tensors', {}))
    gradients = {}
    for name in names:
        observations = [r['tensors'][name]['gradient'] for r in rows[1:]]
        gradients[name] = {key: {'minimum': min(o[key] for o in observations),
            'maximum': max(o[key] for o in observations), 'mean': float(np.mean([o[key] for o in observations]))}
            for key in ('norm', 'zero', 'le_eps', 'eps_to_10eps', 'gt_10eps')}
    return {'trajectory': trajectory, 'margin_curve': margins, 'gradient_epsilon_summary': gradients,
            'epsilon': 1e-8, 'onset': next((r['step'] for r in trajectory if r['correct'] < r['total']), None)}


def readings(experiments):
    result = {}
    for seed in range(3):
        groups = {name: {r['run']['condition']: r for r in rows if r['run']['seed'] == seed
                        and r['run']['law'] == 'original'} for name, rows in experiments.items()}
        def measures(row):
            return {'categorical_misreads': row['census_counts'][0]['categorical_misreads'],
                    'KL_bits': row['prediction']['natural_excess_KL_bits'],
                    'long_TV': row['law']['panels']['long']['maximum_TV'],
                    'endpoint_label': row['endpoint_status']}
        result[str(seed)] = {'noise': {'measurements': {c: measures(r) for c, r in groups['noise'].items()},
            'reading': 'Target noise contributes; probability targets do not uniformly repair B or the sums-loss disadvantage.'},
            'access': {'measurements': {c: measures(r) for c, r in groups['access'].items()},
                'access': 'Connection improves categorical responses and natural KL; live beats frozen on those two measures.',
                'recurrence': 'Keep law and swap defects alongside access evidence; exact supplied sums pass B only in seed 2.'},
            'encoding': {'measurements': {'numerical': measures(groups['encoding']['numerical']),
                                          'onehot': measures(groups['access']['exact'])},
                'reading': 'Numerical versus one-hot differences support encoding sensitivity at this budget, including seeds 0–1 where both fail B; not a precision ceiling.'}}
    return result


def aggregate(output=OUTPUT, staging=STAGING):
    start = time.monotonic()
    reg = recorded_registration()
    staging.mkdir(parents=True, exist_ok=True)
    preserved = []
    for filename in ('aggregate.md', 'aggregate.json'):
        path = output / filename
        destination = staging / ('earlier_' + filename)
        if not destination.exists():
            shutil.copy2(path, destination)
        preserved.append(reference(destination))
    calibration = json.loads((output / 'geometry_calibration.json').read_text())
    if calibration['amendment_sha256'] != study.r11.sha(output / 'geometry_amendment.json'):
        raise ValueError('recorded geometry calibration amendment differs')
    experiments = {key: [] for key in ('erosion', 'noise', 'access', 'encoding')}
    detail_rows = []
    for run in study.all_runs():
        summary_path = output / run.name / 'summary.json'
        summary = json.loads(summary_path.read_text())
        if summary['authority']['registration_sha256'] != study.r11.sha(output / 'registration.json'):
            raise ValueError('recorded summary registration differs')
        compact = {'run': run.__dict__, 'step': summary['step'], 'summary': reference(summary_path)}
        if run.experiment == 'erosion':
            rows = load(summary['records'])
            compact.update(erosion_summary(rows))
            compact['records'] = summary['records']
            detail_rows.append({'run': run.__dict__, 'erosion_reference': summary['records']})
        else:
            rows = [load(ref) for ref in summary['curve']]
            last = rows[-1]
            audit = last['audit']
            law = study.r11._aggregate_law(audit['mode_law'])
            law['panels']['long'] = law['panels'].pop('extrapolation')
            compact.update({'endpoint_status': 'REDUCED_SMOKE' if last['reduced_smoke'] else
                'CONTROL_ONLY' if run.law == 'equal' else 'FUTILITY_STOP' if summary['futility_stop'] else
                'PASS' if audit['B_pass'] and last['step'] == 20000 else 'INCOMPLETE',
                'failed_B_bars': failed_b_bars(audit, run.law),
                'prediction': {k: audit[k] for k in ('B_pass', 'criteria', 'natural_excess_KL_bits',
                    'unseen_excess_KL_bits', 'unseen_count', 'rerender', 'swaps')},
                'law': law, 'census_counts': census_counts(audit['board_census']),
                'saved_r9': {k: v for k, v in audit['board_census']['saved_r9_failed_renderings'].items()
                             if k != 'rows'},
                'sums': last['A_board_accuracy'], 'supplier': last['supplier_accuracy'],
                'joint_errors': last['category_error_decomposition'],
                'diagnosis': study.r12.aggregate_diagnosis(last['prefix_diagnosis']),
                'learning_curve': [{'step': r['step'], 'train_parts': r['train_parts'],
                    'natural_KL_bits': r['audit']['natural_excess_KL_bits'], 'B_pass': r['audit']['B_pass'],
                    'law_maximum_TV': r['audit']['mode_law']['maximum_TV'],
                    'categorical_misreads': r['audit']['board_census']['registered_rendering']['categorical_misreads'],
                    'sums': r['A_board_accuracy'], 'supplier': r['supplier_accuracy']} for r in rows],
                'audit_references': summary['curve'],
                'geometry_calibration_status': 'CALIBRATED' if calibration['pass'] else 'BLOCKED',
                'geometry': [{'step': r['step'], **compact_geometry(r['geometry'])} for r in rows
                             if r['step'] in (0, 5000, 20000) and 'geometry' in r],
                'first_crossing': next((r['step'] for r in rows if r['audit']['B_pass']), None)})
            detail_rows.append({'run': run.__dict__, 'audit_references': summary['curve']})
        experiments[run.experiment].append(compact)
    comparisons = erosion_comparison(experiments['erosion'])
    detail_ref = publish(staging / 'aggregate_details.json', {
        'recorded_artifacts': detail_rows, 'experiments': experiments,
        'erosion_comparisons': comparisons})
    # Full per-update curves and repeated support inventories are detailed
    # tables, not compact report content. Their numbers remain hash-bound.
    for row in experiments['erosion']:
        row['margin_summary'] = {
            'initial': row['margin_curve'][0], 'first_update': row['margin_curve'][1],
            'final': row['margin_curve'][-1]}
        row.pop('margin_curve')
        row['accuracy_curve'] = [[p['step'], p['correct']] for p in row['trajectory']]
        row['final_path'] = row['trajectory'][-1]['cumulative_path']
        row.pop('trajectory')
    for comparison in comparisons:
        comparison['blocked_control'] = {'run': comparison['blocked_control']['run'],
                                        'records': comparison['blocked_control']['records']}
        for item in comparison['observed_ranges'].values():
            item['recorded_summary'] = {c: {
                'points': len(points), 'correct_minimum': min(p['correct'] for p in points),
                'correct_maximum': max(p['correct'] for p in points),
                'first': points[0], 'last': points[-1]}
                for c, points in item.pop('curves').items()}
    for experiment in ('noise', 'access', 'encoding'):
        for row in experiments[experiment]:
            for geo in row['geometry']:
                geo.pop('missing_sums')
    report = {'registration': reference(output / 'registration.json'),
              'report_source': reference(Path(__file__)),
              'training_executed_source': reference(staging / 'training_executed_source.py'),
              'registered_readings_verbatim': reg['specification_verbatim'],
              'conclusion': CONCLUSION, 'experiments': experiments,
              'selected_readings': readings(experiments),
              'erosion_comparisons': comparisons,
              'geometry_calibration': reference(output / 'geometry_calibration.json'),
              'supplementary': json.loads((output / 'supplementary_cutoff_results.json').read_text()),
              'supplementary_executed_source': reference(staging / 'supplementary_executed_source.py'),
              'details': detail_ref, 'preserved_reports': preserved,
              'storage': {'staged_directory': str(staging), 'host_destination': str(DESTINATION),
                'reason': 'Bulk directory is read-only in this session; copy staged details on the host.'},
              'elapsed_seconds': time.monotonic() - start}
    # Compact JSON, with readable tables in Markdown and full arrays in bulk.
    (output / 'aggregate.json').write_text(json.dumps(report, sort_keys=True, separators=(',', ':')) + '\n')
    (output / 'aggregate.md').write_text(markdown(report))
    # Relative-name checks permit the host copy to be verified in either place.
    checksum_rows = [f'{study.r11.sha(p)}  {p.name}' for p in sorted(staging.iterdir())
                     if p.is_file() and p.name != 'SHA256SUMS' and p.suffix != '.log']
    (staging / 'SHA256SUMS').write_text('\n'.join(checksum_rows) + '\n')
    print(json.dumps({'experiments': {k: len(v) for k, v in experiments.items()},
                      'details': detail_ref, 'elapsed_seconds': report['elapsed_seconds']}, indent=2))
    return report


def format_failures(row):
    parts = []
    for name, failed in row['failed_B_bars'].items():
        if 'value' in failed:
            parts.append(f"{name}={failed['value']:.6g}")
        elif name == 'swaps':
            parts.append('swaps: ' + ', '.join(f"{k}={v['maximum_TV']:.6g}"
                         for k, v in failed['cases'].items() if v['maximum_TV'] > .02))
        elif name == 'rerender':
            parts.append(f"rerender TV={failed['maximum_TV']:.6g}; A differences={failed['A_answer_mismatched_components']}")
    return '; '.join(parts) or 'none'


def geometry_table(lines, rows):
    lines += ['', '| Sums | Fit / evaluation pairs | Correct / total | Accuracy | CE (nats) | Floor CE | Converged | Decision | Distance min/median/max | Rerender mean |',
              '|---|---|---|---|---|---|---|---|---|---|']
    for row in rows:
        reader = row['reader']
        lines.append(f"| {row['sums']} | {row['train_pairs']} / {row['heldout_pairs']} | "
            f"{reader['correct']}/{reader['total']} | {reader['accuracy']:.6g} | "
            f"{reader['cross_entropy_nats']:.6g} | {row['label_permutation_floor']['cross_entropy_nats']:.6g} | "
            f"{reader['converged']} | {row['discrimination']['pass']} | "
            f"{[round(v, 6) for v in row['distance_quantiles']]} | {row['rerender_distance_mean']:.6g} |")


def markdown(report):
    lines = ['# r13 saved-state analysis', '', report['conclusion'], '',
        'Runs, endpoint labels, thresholds and the training instrument are unchanged. '
        'Equal-law runs are controls only. Access benefits and remaining recurrence defects are concurrent findings. '
        'Geometry calibration status does not imply discrimination or support in a measured row. '
        'Prediction TV errors (>0.02) and categorical misreads are different measurements. '
        'Categorical signatures are not defined in the equal-law control; its entries are None. '
        'A non-operative supplier is a diagnostic head, not an input route.', '',
        '## Registered readings (verbatim)', '', report['registered_readings_verbatim']]
    for experiment, rows in report['experiments'].items():
        lines += ['', f'## {experiment}', '']
        if experiment == 'erosion':
            lines += ['All active conditions lose exactness at update 1. Blocked is a separate decay-only control. '
                      'Gradients, displacement and small answer margins are not isolated explanations.', '',
                '| Seed | Arm | Onset | Update-1 correct / 1555 | Final correct / 1555 | Path | Initial margin min / median | Final margin min / median |',
                '|---|---|---|---|---|---|---|---|']
            for r in rows:
                lines.append(f"| {r['run']['seed']} | {r['run']['condition']} | {r['onset']} | "
                    f"{r['accuracy_curve'][1][1]}/1555 | "
                    f"{r['accuracy_curve'][-1][1]}/1555 | {r['final_path']:.6g} | "
                    f"{r['margin_summary']['initial']['quantiles'][0]:.6g} / {r['margin_summary']['initial']['quantiles'][2]:.6g} | "
                    f"{r['margin_summary']['final']['quantiles'][0]:.6g} / {r['margin_summary']['final']['quantiles'][2]:.6g} |")
            lines += ['', '| Seed | Active arms | Observed common path range | Recorded points: count, correct min–max |',
                      '|---|---|---|---|']
            for comparison in report['erosion_comparisons']:
                for name, item in comparison['observed_ranges'].items():
                    summary = '; '.join(f"{c}: {p['points']}, {p['correct_minimum']}–"
                        f"{p['correct_maximum']}" for c, p in item['recorded_summary'].items())
                    lines.append(f"| {comparison['seed']} | {name} | {item['range']} | {summary} |")
            lines += ['', 'All 201 recorded accuracy counts and per-tensor gradient/epsilon summaries '
                      'are in compact JSON; full margin curves, per-update records and matched-range points are hash-bound below. '
                      'No answer-accuracy interpolation is used.']
            lines += ['', '| Seed / arm | Tensor | Gradient norm min / mean / max | Mean fraction ≤ epsilon | Mean fraction > 10 epsilon |',
                      '|---|---|---|---|---|']
            for r in rows:
                for name, gradient in r['gradient_epsilon_summary'].items():
                    norm = gradient['norm']
                    lines.append(f"| {r['run']['seed']} / {r['run']['condition']} | {name} | "
                        f"{norm['minimum']:.6g} / {norm['mean']:.6g} / {norm['maximum']:.6g} | "
                        f"{gradient['le_eps']['mean']:.6g} | {gradient['gt_10eps']['mean']:.6g} |")
            lines += ['', 'Epsilon = 1e-8. Component fractions are averaged over the 200 recorded updates, '
                      'separately for each tensor, not weighted across tensors. True-class logit margins '
                      'at update 0, update 1 and update 200 are retained in JSON; negative margins mean an incorrect answer.']
            continue
        lines += ['| Seed | Condition / law | Label | Failed B bars (values) | Categorical misreads | TV errors | Sums vector | Supplier vector |',
                  '|---|---|---|---|---|---|---|---|']
        for r in rows:
            sums, supplier = r['sums']['vector'], r['supplier'].get('vector')
            lines.append(f"| {r['run']['seed']} | {r['run']['condition']} / {r['run']['law']} | {r['endpoint_status']} | "
                f"{format_failures(r)} | {r['census_counts'][0]['categorical_misreads']} | "
                f"{r['census_counts'][0]['prediction_TV_errors']} | {sums['correct']}/{sums['total']} | "
                f"{str(supplier['correct']) + '/' + str(supplier['total']) if supplier else 'not operative'} |")
        for r in rows:
            lines += ['', f"### {study.Run(**r['run']).name}", '',
                '| Rendering | Cutoff categorical / boards | Other categorical / boards | Cutoff TV / boards | Other TV / boards |',
                '|---|---|---|---|---|']
            for c in r['census_counts']:
                a, b = c['cutoff'], c['complement']
                lines.append(f"| {c['rendering']} | {a['categorical_misreads']}/{a['boards']} | "
                    f"{b['categorical_misreads']}/{b['boards']} | {a['prediction_TV_errors']}/{a['boards']} | "
                    f"{b['prediction_TV_errors']}/{b['boards']} |")
            lines += ['', '| Update | Prediction loss / floor | Natural KL | Law max TV | Categorical misreads | Sums vector |',
                      '|---|---|---|---|---|---|']
            for point in r['learning_curve']:
                vector = point['sums']['vector']
                lines.append(f"| {point['step']} | {point['train_parts']['B']:.6g} / {point['train_parts']['target_floor']:.6g} | "
                    f"{point['natural_KL_bits']:.6g} | {point['law_maximum_TV']:.6g} | {point['categorical_misreads']} | "
                    f"{vector['correct']}/{vector['total']} |")
            lines += ['', f"Concurrent diagnosis: {r['diagnosis']['concurrent_findings']}. "
                      f"Counts: {r['diagnosis']['counts']}; chronology: {r['diagnosis']['chronology']}."]
            for geo in r['geometry']:
                lines += ['', f"Geometry update {geo['step']}: calibration {r['geometry_calibration_status']}; "
                    f"{geo['measured_rows']} measured, {geo['missing_support_rows']} missing. "
                    f"Critical absent support: {geo['cutoff_missing']}. "
                    'The complete missing pair inventory is in the hash-bound detailed JSON.']
                geometry_table(lines, geo['measured'])
    lines += ['', '## Concurrent selected readings', '']
    for seed, reading in report['selected_readings'].items():
        lines += [f"Seed {seed}: {reading['noise']['reading']} {reading['access']['access']} "
                  f"{reading['access']['recurrence']} {reading['encoding']['reading']}", '']
    lines += ['| Seed | Encoding | Categorical misreads | Natural KL | Long-panel TV | Endpoint label |',
              '|---|---|---|---|---|---|']
    for seed, reading in report['selected_readings'].items():
        for encoding, measured in reading['encoding']['measurements'].items():
            lines.append(f"| {seed} | {encoding} | {measured['categorical_misreads']} | "
                f"{measured['KL_bits']:.6g} | {measured['long_TV']:.6g} | {measured['endpoint_label']} |")
    lines += ['', '| Seed | Access condition | Categorical misreads | Natural KL | Long-panel TV | Endpoint label |',
              '|---|---|---|---|---|---|']
    for seed, reading in report['selected_readings'].items():
        for condition, measured in reading['access']['measurements'].items():
            lines.append(f"| {seed} | {condition} | {measured['categorical_misreads']} | "
                f"{measured['KL_bits']:.6g} | {measured['long_TV']:.6g} | {measured['endpoint_label']} |")
    lines += ['']
    lines += ['## Supplementary cutoff geometry', '',
        'Panel identities and fixed rendering hashes were bound before checkpoint states were read. '
        'Fitting excludes every existing probe-held-out identity. No resampling or network training. '
        'Distances are descriptive; a failed discrimination decision remains a failed decision.', '']
    for r in report['supplementary']['rows']:
        lines += [f"### {study.Run(**r['run']).name}, update {r['step']}"]
        geometry_table(lines, r['measured'])
    lines += ['', '## Storage and bindings', '',
        f"Details: `{report['details']['path']}`, SHA-256 `{report['details']['sha256']}`.", '',
        'Earlier reports and detailed numerical artifacts are hash-bound in JSON. '
        'The bulk artifact directory is configurable through SBML_DATA.']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=('declare', 'extract', 'aggregate'), required=True)
    parser.add_argument('--staging', type=Path, default=STAGING)
    args = parser.parse_args()
    torch.set_num_threads(1)
    if args.stage == 'declare':
        print(json.dumps(declare(), indent=2))
    elif args.stage == 'extract':
        extract(staging=args.staging)
    else:
        aggregate(staging=args.staging)


if __name__ == '__main__':
    main()
