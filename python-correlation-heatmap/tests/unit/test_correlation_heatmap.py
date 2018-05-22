import mock
import json
import numpy as np
import pandas as pd
from . import fixtures as fx
from mip_helper import testing as t
from correlation_heatmap import intermediate_stats, aggregate_stats, compute


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute_heatmap_continuous(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(include_nominal=True)

    compute('correlation_heatmap')
    results = json.loads(mock_save_results.call_args[0][0])
    assert t.round_dict(results) == {
        'data': [
            {
                'type': 'heatmap',
                'x': ['lefthippocampus', 'subjectage', 'minimentalstate'],
                'xaxis': 'x1',
                'y': ['minimentalstate', 'subjectage', 'lefthippocampus'],
                'yaxis': 'y1',
                'z': [[0.959, -0.343, 1.0], [-0.254, 1.0, -0.343], [1.0, -0.254, 0.959]],
                'zmax': 1,
                'zmin': -1
            }
        ],
        'layout': {
            'title': 'Correlation heatmap'
        }
    }


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute_heatmap_nominal(mock_save_results, mock_fetch_data):
    # TODO: should work only for nominal variables
    pass


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute_heatmap_mix(mock_save_results, mock_fetch_data):
    # two categorical variables
    data = t.inputs_classification(include_nominal=True)
    mock_fetch_data.return_value = data

    compute('correlation_heatmap')
    results = json.loads(mock_save_results.call_args[0][0])
    assert t.round_dict(results['data'][0]) == {
        'type': 'heatmap',
        'z': [[-0.343, 1.0], [1.0, -0.343]],
        'x': ['subjectage', 'minimentalstate'],
        'y': ['minimentalstate', 'subjectage'],
        'zmin': -1,
        'zmax': 1,
        'xaxis': 'x1',
        'yaxis': 'y1',
        'colorbar': {
            'len': 0.5,
            'y': 0.75
        }
    }
    assert t.round_dict(results['data'][1]) == {
        'type': 'heatmap',
        'z': [[0, 0, 0, 0], [0, 0.5, 0.5, 0.5], [0, 1, 1, 1], [0, 0.5, 0.5, 0.5], [0, 1, 1, 1]],
        'opacity': 0.75,
        'colorscale': [[0, '#00083e'], [0.5, '#ededee'], [1, '#ffffff']],
        'showscale': 0,
        'hoverinfo': 'none',
        'xaxis': 'x2',
        'yaxis': 'y2'
    }


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute_pca(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=False)

    compute('pca')
    results = json.loads(mock_save_results.call_args[0][0])
    assert set(results.keys()) == {'layout', 'data'}


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute_empty(mock_save_results, mock_fetch_data):
    data = fx.inputs_regression(include_categorical=False)
    # all data are null
    data['data']['independent'][0]['series'] = [None] * len(data['data']['independent'][0]['series'])

    mock_fetch_data.return_value = data

    compute()
    results = json.loads(mock_save_results.call_args[0][0])
    assert np.array(results['data'][0]['z']).shape == (3, 3)
    assert pd.isnull(results['data'][0]['z']).all()


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_intermediate_stats(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(include_nominal=True)

    intermediate_stats()
    results = json.loads(mock_save_results.call_args[0][0])
    assert t.round_dict(results) == {
        'X^T * X': [[44.891, 1055.621, 317.732], [1055.621, 25462.015, 7279.928], [317.732, 7279.928, 2354.0]],
        'columns': ['lefthippocampus', 'subjectage', 'minimentalstate'],
        'count': 5,
        'crosstab': [{
            'agegroup': '-50y',
            'count': 3
        }, {
            'agegroup': '50-59y',
            'count': 2
        }],
        'means': [2.987, 70.86, 20.8],
        'nominal_columns': ['agegroup']
    }


def intermediate_data_1():
    return {
        'columns': ['iq', 'stress_before_test1'],
        'means': [73.8815754762, 52.9296397352],
        'X^T * X': [[32751.4170961055, 23458.8913944936], [23458.8913944936, 17009.1219934008]],
        'count': 6,
        'nominal_columns': ['agegroup'],
        'crosstab': [{
            'agegroup': '-50y',
            'count': 3
        }, {
            'agegroup': '50-59y',
            'count': 2
        }],
    }


def intermediate_data_2():
    return intermediate_data_1()


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.get_results')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_aggregate_stats_correlation_heatmap(mock_save_results, mock_get_results, mock_fetch):

    def mock_results(job_id):
        job_id = str(job_id)
        if job_id == '1':
            return mock.MagicMock(data=json.dumps(intermediate_data_1()))
        elif job_id == '2':
            return mock.MagicMock(data=json.dumps(intermediate_data_2()))

    mock_get_results.side_effect = mock_results

    aggregate_stats([1, 2], graph_type='correlation_heatmap')
    results = json.loads(mock_save_results.call_args[0][0])
    assert t.round_dict(results) == {
        'data': [
            {
                'type': 'heatmap',
                'x': ['iq', 'stress_before_test1'],
                'xaxis': 'x1',
                'y': ['stress_before_test1', 'iq'],
                'yaxis': 'y1',
                'z': [[-0.429, 1.0], [1.0, -0.429]],
                'zmax': 1,
                'zmin': -1
            }
        ],
        'layout': {
            'title': 'Correlation heatmap'
        }
    }


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.get_results')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_aggregate_stats_pca(mock_save_results, mock_get_results, mock_fetch):

    def mock_results(job_id):
        job_id = str(job_id)
        if job_id == '1':
            return mock.MagicMock(data=json.dumps(intermediate_data_1()))
        elif job_id == '2':
            return mock.MagicMock(data=json.dumps(intermediate_data_2()))

    mock_get_results.side_effect = mock_results

    aggregate_stats([1, 2], graph_type='pca')
    results = json.loads(mock_save_results.call_args[0][0])
    assert set(results.keys()) == {'layout', 'data'}
