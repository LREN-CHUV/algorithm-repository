import mock
import json
import numpy as np
import pandas as pd
from . import fixtures as fx
from correlation_heatmap import intermediate_stats, aggregate_stats, compute


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=False)

    compute()
    results = json.loads(mock_save_results.call_args[0][0])
    assert results == [
        {
            'type': 'heatmap',
            'z': [[1.0, -0.4287450417], [-0.4287450417, 1.0]],
            'x': ['iq', 'stress_before_test1'],
            'y': ['iq', 'stress_before_test1']
        }
    ]


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_compute_empty(mock_save_results, mock_fetch_data):
    data = fx.inputs_regression(include_categorical=False)
    # all data are null
    data['data']['independent'][0]['series'] = [None] * len(data['data']['independent'][0]['series'])

    mock_fetch_data.return_value = data

    compute()
    results = json.loads(mock_save_results.call_args[0][0])
    assert np.array(results[0]['z']).shape == (2, 2)
    assert pd.isnull(results[0]['z']).all()


@mock.patch('correlation_heatmap.io_helper.fetch_data')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_intermediate_stats(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=False)

    intermediate_stats()
    results = json.loads(mock_save_results.call_args[0][0])
    assert results == {
        'columns': ['iq', 'stress_before_test1'],
        'means': [73.8815754762, 52.9296397352],
        'X^T * X': [[32751.4170961055, 23458.8913944936], [23458.8913944936, 17009.1219934008]],
        'count': 6
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
    assert results == [
        {
            'type': 'heatmap',
            'x': ['iq', 'stress_before_test1'],
            'y': ['iq', 'stress_before_test1'],
            'z': [[1.0, -0.4287450502], [-0.4287450502, 1.0]]
        }
    ]
