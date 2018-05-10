import mock
import json
import copy
import numpy as np
import pandas as pd
from . import fixtures as fx
from correlation_heatmap import intermediate_stats, aggregate_stats, compute


# TODO: put into io_helper.testing when convenient
def round_dict(d, precision=3):
    """Round all numerical values in a dictionary recursively."""
    d = copy.deepcopy(d)
    if isinstance(d, dict):
        for k, v in d.items():
            try:
                d[k] = round(v, precision)
            except TypeError:
                d[k] = round_dict(v)
        return d
    elif isinstance(d, list):
        return [round_dict(v) for v in d]
    elif isinstance(d, tuple):
        return tuple([round_dict(v) for v in d])
    elif isinstance(d, float):
        return round(d, precision)

    return d


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute_heatmap(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=False)

    compute('correlation_heatmap')
    results = json.loads(mock_save_results.call_args[0][0])
    assert round_dict(results) == [
        {
            'type': 'heatmap',
            'z': [[-0.429, -0.543, 1.0], [0.417, 1.0, -0.543], [1.0, 0.417, -0.429]],
            'x': ['iq', 'score_test1', 'stress_before_test1'],
            'y': ['stress_before_test1', 'score_test1', 'iq'],
            'zmin': -1,
            'zmax': 1
        }
    ]


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
    assert np.array(results[0]['z']).shape == (3, 3)
    assert pd.isnull(results[0]['z']).all()


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_intermediate_stats(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=False)

    intermediate_stats()
    results = json.loads(mock_save_results.call_args[0][0])
    assert round_dict(results) == {
        'columns': ['iq', 'score_test1', 'stress_before_test1'],
        'means': [73.882, 1096.505, 52.93],
        'X^T * X':
        [[32751.417, 486164.936, 23458.891], [486164.936, 7321018.913, 345715.383], [23458.891, 345715.383, 17009.122]],
        'count':
        6
    }


def intermediate_data_1():
    return {
        'columns': ['iq', 'stress_before_test1'],
        'means': [73.8815754762, 52.9296397352],
        'X^T * X': [[32751.4170961055, 23458.8913944936], [23458.8913944936, 17009.1219934008]],
        'count': 6
    }


def intermediate_data_2():
    return intermediate_data_1()


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.get_results')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_aggregate_stats(mock_save_results, mock_get_results, mock_fetch):

    def mock_results(job_id):
        job_id = str(job_id)
        if job_id == '1':
            return mock.MagicMock(data=json.dumps(intermediate_data_1()))
        elif job_id == '2':
            return mock.MagicMock(data=json.dumps(intermediate_data_2()))

    mock_get_results.side_effect = mock_results

    aggregate_stats([1, 2])
    results = json.loads(mock_save_results.call_args[0][0])
    assert round_dict(results) == [
        {
            'type': 'heatmap',
            'z': [[-0.429, 1.0], [1.0, -0.429]],
            'x': ['iq', 'stress_before_test1'],
            'y': ['stress_before_test1', 'iq'],
            'zmin': -1,
            'zmax': 1
        }
    ]
