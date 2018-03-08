import mock
import json
from . import fixtures as fx
from correlation_heatmap import intermediate_stats, aggregate_stats, get_X


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


@mock.patch('correlation_heatmap.io_helper.get_results')
@mock.patch('correlation_heatmap.io_helper.save_results')
def test_aggregate_stats(mock_save_results, mock_get_results):

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
