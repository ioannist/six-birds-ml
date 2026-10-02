"""Read-only r13 reporting, fixed cutoff identities and observed-range checks."""

import copy
import json

import pytest

from scripts import oldgame_mechanism_report as report


def test_supplementary_pairs_fixed_legal_and_separated():
    boards = report.study.r11.enumerate_boards().boards
    split = json.loads((report.study.r11.r8.OUTPUT / 'probe_split.json').read_text())
    rows = report.panel_pairs(boards, split['heldout_board_ids'])
    assert rows == report.panel_pairs(boards, split['heldout_board_ids'])
    assert [r['legal_pairs'] for r in rows] == [285, 25]
    assert [(len(r['train_pairs']), len(r['heldout_pairs'])) for r in rows] == [(135, 150), (12, 13)]
    for row in rows:
        fitting = {i for p in row['train_pairs'] for i in p}
        evaluation = {i for p in row['heldout_pairs'] for i in p}
        assert not fitting & evaluation
        assert not fitting & set(split['heldout_board_ids'])
        for a, b in row['train_pairs'] + row['heldout_pairs']:
            assert boards[a][0] == row['sums'][0]
            assert boards[b][0] == row['sums'][1]
            assert boards[a][1:] == boards[b][1:]
        assert sorted(row['label_permutation']) == list(range(2 * len(row['train_pairs'])))


def test_supplementary_panel_refuses_empty_fitting_support():
    boards = [(12, 0, 0, 0, 0), (13, 0, 0, 0, 0)]
    with pytest.raises(ValueError, match='support or separation'):
        report.panel_pairs(boards, [0, 1])


def census_panel():
    return {'boards': 7, 'categorical_misreads': 2, 'above_0_02_TV': 5,
        'category_status': 'MEASURED', 'by_slot1_sum_twelfths': {
            '12': {'boards': 3, 'categorical_misreads': 1, 'above_0_02_TV': 3},
            '8': {'boards': 4, 'categorical_misreads': 1, 'above_0_02_TV': 2}}}


def test_cutoff_categorical_counts_not_prediction_tv_counts():
    panel = census_panel()
    census = {'registered_rendering': panel, 'additional_fixed_renderings': [panel] * 3}
    rows = report.census_counts(census)
    assert len(rows) == 4
    for row in rows:
        assert row['cutoff'] == {'boards': 3, 'categorical_misreads': 1, 'prediction_TV_errors': 3}
        assert row['complement'] == {'boards': 4, 'categorical_misreads': 1, 'prediction_TV_errors': 2}
        assert row['categorical_misreads'] == 2 and row['prediction_TV_errors'] == 5
    equal = copy.deepcopy(census)
    for value in equal['registered_rendering']['by_slot1_sum_twelfths'].values():
        value['categorical_misreads'] = None
    equal['registered_rendering']['categorical_misreads'] = None
    assert report.census_counts(equal)[0]['cutoff']['categorical_misreads'] is None


def test_blocked_excluded_from_pairwise_and_three_arm_ranges():
    rows = []
    for seed in range(3):
        for condition, path in (('adam', 12.), ('sgd', 11.), ('reduced', 2.5), ('blocked', .01)):
            rows.append({'run': {'condition': condition, 'seed': seed}, 'trajectory': [
                {'step': 0, 'correct': 1555, 'cumulative_path': 0.},
                {'step': 1, 'correct': 1500, 'cumulative_path': path / 2},
                {'step': 2, 'correct': 100, 'cumulative_path': path}]})
    result = report.erosion_comparison(rows)
    for row in result:
        assert row['observed_ranges']['adam--sgd']['range'] == [0., 11.]
        assert row['observed_ranges']['adam--sgd--reduced']['range'] == [0., 2.5]
        assert row['blocked_control']['run']['condition'] == 'blocked'
        assert row['observed_ranges']['adam--sgd--reduced']['curves']['adam'] == [rows[0]['trajectory'][0]]
        for item in row['observed_ranges'].values():
            assert 'blocked' not in item['curves']
            for curve in item['curves'].values():
                assert all(p['step'] in (0, 1, 2) for p in curve)


def test_failed_b_bars_include_values_not_only_labels():
    values = {'count': 1, 'maximum_TV': .25, 'mean_TV': .1}
    audit = {'criteria': {key: False for key in ('natural_KL', 'unseen_KL', 'witness', 'law_TV', 'rerender', 'swaps')},
        'natural_excess_KL_bits': .1, 'unseen_excess_KL_bits': .2, 'unseen_count': 4,
        'mode_law': {'maximum_TV': .25, 'witness_recovery_fraction': .6,
                     'witness_pair_mean_prediction_TV': .04, 'cases': {'N_run_8': values}},
        'rerender': {'maximum_TV': .3, 'A_answer_mismatched_components': 35},
        'swaps': {'cases': {'reset_L': values}}}
    failed = report.failed_b_bars(audit, 'original')
    assert set(failed) == set(audit['criteria'])
    assert failed['law_TV']['value'] == .25
    assert failed['rerender']['A_answer_mismatched_components'] == 35
    assert failed['swaps']['cases']['reset_L']['maximum_TV'] == .25
    assert report.failed_b_bars(audit, 'equal')['witness']['value'] == .04


def test_encoding_and_access_readings_keep_measurements_despite_b_failure():
    def row(condition, misreads, kl):
        return {'run': {'condition': condition, 'seed': 0, 'law': 'original'},
            'census_counts': [{'categorical_misreads': misreads}],
            'prediction': {'natural_excess_KL_bits': kl},
            'law': {'panels': {'long': {'maximum_TV': .25}}}, 'endpoint_status': 'INCOMPLETE'}
    groups = {'noise': [], 'access': [], 'encoding': []}
    for seed in range(3):
        for condition, count in (('disconnected', 58), ('frozen', 30), ('live', 15), ('exact', 0)):
            r = row(condition, count, .001)
            r['run']['seed'] = seed
            groups['access'].append(r)
        r = row('numerical', 317, .002)
        r['run']['seed'] = seed
        groups['encoding'].append(r)
    result = report.readings(groups)['0']
    assert result['encoding']['measurements']['numerical']['categorical_misreads'] == 317
    assert result['encoding']['measurements']['onehot']['categorical_misreads'] == 0
    assert 'including seeds 0–1 where both fail B' in result['encoding']['reading']
    assert 'access' in result['access'] and 'recurrence' in result['access']


def test_saved_report_bindings_labels_and_support():
    saved = json.loads((report.OUTPUT / 'aggregate.json').read_text())
    assert report.study.r11.sha(report.OUTPUT / 'registration.json') == saved['registration']['sha256']
    panel = report.load(saved['supplementary']['panel'])
    assert report.reference(saved['supplementary_executed_source']['path'])['sha256'] == panel['analysis_source_sha256']
    earlier = report.load(next(r for r in saved['preserved_reports'] if r['path'].endswith('.json')))
    for experiment in ('noise', 'access', 'encoding'):
        old = {report.study.Run(**r['run']).name: r for r in earlier['experiments'][experiment]}
        for row in saved['experiments'][experiment]:
            original = old[report.study.Run(**row['run']).name]
            assert row['endpoint_status'] == original['endpoint_status']
            assert row['failed_B_bars'].keys() == {
                k for k, v in original['endpoint_prediction']['criteria'].items() if not v}
            if row['geometry']:
                assert all(r['measured_rows'] == 19 and r['missing_support_rows'] == 578 for r in row['geometry'])
                assert all([r['sums'] for r in geo['cutoff_missing']] == [[12, 13], [23, 24]]
                           for geo in row['geometry'])
    text = (report.OUTPUT / 'aggregate.md').read_text()
    assert report.CONCLUSION in text
    assert 'All active conditions lose exactness at update 1' in text
    assert 'Categorical misreads' in text and 'TV errors' in text
    assert saved['registered_readings_verbatim'] in text
    assert (report.OUTPUT / 'aggregate.md').stat().st_size < 1_000_000
    assert (report.OUTPUT / 'aggregate.json').stat().st_size < 1_000_000


def test_recorded_registration_preserves_training_authority():
    reg = report.recorded_registration()
    assert reg['settings'] == report.study.settings()
    assert report.reference(report.STAGING / 'training_executed_source.py')['sha256'] == reg['source_sha256']['script']


def test_aggregate_entry_calls_saved_report(monkeypatch, tmp_path):
    called = []
    monkeypatch.setattr(report, 'aggregate', lambda output: called.append(output) or {
        'experiments': {'erosion': []}, 'details': {'sha256': 'fixed'}})
    assert report.study.aggregate(tmp_path, tmp_path / 'bulk') == {
        'experiments': {'erosion': 0}, 'details': {'sha256': 'fixed'}}
    assert called == [tmp_path]


def test_recorded_registration_refuses_threshold_change(monkeypatch):
    settings = copy.deepcopy(report.study.settings())
    settings['criteria']['TV'] = .5
    monkeypatch.setattr(report.study, 'settings', lambda: settings)
    with pytest.raises(ValueError, match='settings or registered readings differ'):
        report.recorded_registration()


def test_hash_bound_detail_refuses_mutation(tmp_path):
    path = tmp_path / 'detail.json'
    ref = report.publish(path, {'value': 2})
    path.write_text('{"value": 3}')
    with pytest.raises(ValueError, match='digest differs'):
        report.load(ref)
