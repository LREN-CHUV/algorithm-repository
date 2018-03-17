import mock
import json
from . import fixtures as fx
from statistics import intermediate_stats, aggregate_stats, get_X


@mock.patch('statistics.io_helper.fetch_data')
@mock.patch('statistics.io_helper.save_results')
def test_intermediate_stats(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)

    intermediate_stats()
    results = json.loads(mock_save_results.call_args[0][0])
    assert len(results['data']) == 16
    assert results['data'][:2] == [
        {
            'index': 'agegroup',
            'group': ['-50y'],
            'group_variables': ['agegroup'],
            'count': 3,
            'unique': 1,
            'top': '-50y',
            'freq': 3,
            'frequency': {
                '-50y': 3,
                '59y-': 0,
                '50-59y': 0
            }
        }, {
            'index': 'iq',
            'group': ['-50y'],
            'group_variables': ['agegroup'],
            'count': 3,
            'mean': 73.7882673088,
            'std': 0.2018918769,
            'min': 73.5856470359,
            '25%': 73.6876895535,
            '50%': 73.7897320711,
            '75%': 73.8895774452,
            'max': 73.9894228193,
            'EX^2': 5444.7355659833
        }
    ]


@mock.patch('statistics.io_helper.fetch_data')
@mock.patch('statistics.io_helper.save_results')
def test_intermediate_stats_empty(mock_save_results, mock_fetch_data):
    data = fx.inputs_regression(include_categorical=True)
    data['data']['dependent'][0]['series'] = []
    mock_fetch_data.return_value = data

    intermediate_stats()
    error = mock_save_results.call_args[0][1]
    assert error == 'Dependent variable has no values, check your SQL query.'


def intermediate_data_1():
    return {
        'schema': {},
        'data':
        [{
            'index': 'iq',
            'group': ['-50y'],
            'group_variables': ['agegroup'],
            'count': 3,
            'mean': 80,
            'std': 10,
            'min': 70,
            'max': 120,
            'EX^2': 8000
        }]
    }


def intermediate_data_2():
    return {
        'schema': {},
        'data':
        [{
            'index': 'iq',
            'group': ['-50y'],
            'group_variables': ['agegroup'],
            'count': 5,
            'mean': 100,
            'std': 20,
            'min': 80,
            'max': 130,
            'EX^2': 12000
        }]
    }


@mock.patch('statistics.io_helper.get_results')
@mock.patch('statistics.io_helper.save_results')
def test_aggregate_stats(mock_save_results, mock_get_results):

    def mock_results(job_id):
        if job_id == '1':
            return mock.MagicMock(data=json.dumps(intermediate_data_1()))
        elif job_id == '2':
            return mock.MagicMock(data=json.dumps(intermediate_data_2()))

    mock_get_results.side_effect = mock_results

    aggregate_stats(['1', '2'])
    results = json.loads(mock_save_results.call_args[0][0])
    assert results['data'] == [
        {
            'index': 'iq',
            'group': ['-50y'],
            'group_variables': ['agegroup'],
            'mean': 92.5,
            'std': 44.0879802214,
            'min': 70,
            'max': 130,
            'count': 8
        }, {
            'index': 'iq',
            'group': ['all'],
            'group_variables': ['agegroup'],
            'mean': 92.5,
            'std': 44.0879802214,
            'min': 70,
            'max': 130,
            'count': 8
        }
    ]


def test_get_X():
    inputs = fx.inputs_regression(include_categorical=True)
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]
    X = get_X(dep_var, indep_vars)

    assert list(X.columns) == ['agegroup', 'iq', 'score_test1', 'stress_before_test1']
    assert list(X.agegroup.cat.categories) == ['-50y', '50-59y', '59y-']
    assert X.shape == (6, 4)
