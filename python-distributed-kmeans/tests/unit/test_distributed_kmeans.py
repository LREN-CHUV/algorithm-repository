import mock
import json
import numpy as np
from . import fixtures as fx
from distributed_kmeans import intermediate_kmeans, aggregate_kmeans
import dkmeans.local_computations as local


@mock.patch('distributed_kmeans.io_helper.fetch_data')
@mock.patch('distributed_kmeans.io_helper.save_results')
def test_intermediate_kmeans(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)

    intermediate_kmeans()
    results = json.loads(mock_save_results.call_args[0][0])

    assert len(results['centroids']) == 8


def indep_vars():
    return [
        {
            'name': 'stress_before_test1',
            'type': {
                'name': 'real'
            },
            'mean': 55,
            'std': 20.0
        }, {
            'name': 'iq',
            'type': {
                'name': 'real'
            },
            'mean': 72,
            'std': 10.0
        }, {
            'name': 'agegroup',
            'type': {
                'name': 'polynominal',
                'enumeration': ['-50y', '50-59y']
            }
        }
    ]


def intermediate_data_1():
    return {
        'centroids':
        [[0.043368447347499915, 0.17402365634999983, 0.0, 1.0], [-0.29034167028999996, 0.24441778038000023, 0.0, 1.0]],
        'indep_vars': indep_vars()
    }


def intermediate_data_2():
    return {
        'centroids': [[0.0, 0.0, 0.0, 0.0], [-0.3704973316875002, 0.18895774452000041, 1.0, 0.0]],
        'indep_vars': indep_vars()
    }


@mock.patch('distributed_kmeans.io_helper.fetch_data')
@mock.patch('distributed_kmeans.io_helper.load_intermediate_json_results')
@mock.patch('distributed_kmeans.io_helper.save_results')
def test_aggregate_kmeans(mock_save_results, mock_load_intermediate_json_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)

    mock_load_intermediate_json_results.return_value = [
        intermediate_data_1(), intermediate_data_2()
    ]

    aggregate_kmeans([1, 2])
    pfa_dict = json.loads(mock_save_results.call_args[0][0])

    np.testing.assert_allclose(
        json.loads(pfa_dict['metadata']['centroids']),
        np.array(
            [
                [-0.12348661147125002, 0.20922071836500003, 0.0, 1.0],
                [-0.1852486658437501, 0.09447887226000021, 0.5, 0.0]
            ]
        ), 1e-5
    )

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    ret = engine.action({'stress_before_test1': 10., 'iq': 10., 'agegroup': '-50y'})
    assert ret == 1


def test_dkmeans_zero_arrays():
    k = 8
    X = np.random.random((4, 4))

    cluster_labels = [0] * len(X)
    local_means = local.compute_mean(X, cluster_labels, k)

    assert np.array(local_means).shape == (k, 4)
