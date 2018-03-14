import mock
import json
from . import fixtures as fx
from distributed_kmeans import intermediate_kmeans, aggregate_kmeans


@mock.patch('distributed_kmeans.io_helper.fetch_data')
@mock.patch('distributed_kmeans.io_helper.save_results')
def test_intermediate_kmeans(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)

    intermediate_kmeans()
    results = json.loads(mock_save_results.call_args[0][0])

    assert len(results['centroids']) == 5


def intermediate_data_1():
    return {
        'centroids':
        [[0.043368447347499915, 0.17402365634999983, 0.0, 1.0], [-0.29034167028999996, 0.24441778038000023, 0.0, 1.0]]
    }


def intermediate_data_2():
    return {'centroids': [[0.0, 0.0, 0.0, 0.0], [-0.3704973316875002, 0.18895774452000041, 1.0, 0.0]]}


@mock.patch('distributed_kmeans.io_helper.get_results')
@mock.patch('distributed_kmeans.io_helper.save_results')
def test_aggregate_kmeans(mock_save_results, mock_get_results):

    def mock_results(job_id):
        if job_id == 1:
            return mock.MagicMock(data=json.dumps(intermediate_data_1()))
        elif job_id == 2:
            return mock.MagicMock(data=json.dumps(intermediate_data_2()))

    mock_get_results.side_effect = mock_results

    aggregate_kmeans([1, 2])
    results = json.loads(mock_save_results.call_args[0][0])
    assert results == {'centroids': [[-0.1234866115, 0.2092207184, 0.0, 1.0], [-0.1852486658, 0.0944788723, 0.5, 0.0]]}
