import mock
import json
from . import fixtures as fx
from statistics import intermediate_stats, aggregate_stats


@mock.patch('statistics.io_helper.fetch_data')
@mock.patch('statistics.io_helper.save_results')
def test_intermediate_stats_real(mock_save_results, mock_fetch_data):
    # input data with some null values
    data = fx.inputs_regression(include_categorical=True, add_null=True)
    data['data']['dependent'][0]['series'][0] = None
    data['data']['independent'][1]['series'][0] = None

    mock_fetch_data.return_value = data

    intermediate_stats()
    results = json.loads(mock_save_results.call_args[0][0])
    assert len(results['data']) == 16
    assert results['data'][:2] == [
        {
            'index': 'agegroup',
            'label': 'Age group',
            'group': ['-50y'],
            'group_variables': ['Age group'],
            'count': 3,
            'unique': 1,
            'top': '-50y',
            'frequency': {
                '-50y': 3,
                '59y-': 0,
                '50-59y': 0
            },
            'null_count': 0
        }, {
            'index': 'iq',
            'label': 'IQ',
            'group': ['-50y'],
            'group_variables': ['Age group'],
            'count': 3,
            'mean': 73.8895774452,
            'std': 0.1412026822,
            'min': 73.7897320711,
            '25%': 73.8396547582,
            '50%': 73.8895774452,
            '75%': 73.9395001323,
            'max': 73.9894228193,
            'EX^2': 5459.6796241289,
            'null_count': 1
        }
    ]


@mock.patch('statistics.io_helper.fetch_data')
@mock.patch('statistics.io_helper.save_results')
def test_intermediate_stats_nominal(mock_save_results, mock_fetch_data):
    # input data with some null values
    data = fx.inputs_classification(include_categorical=True)
    # data['data']['dependent'][0]['series'][0] = None
    # data['data']['independent'][1]['series'][0] = None

    mock_fetch_data.return_value = data

    intermediate_stats()
    results = json.loads(mock_save_results.call_args[0][0])
    assert len(results['data']) == 16
    assert results['data'][:2] == [
        {
            'index': 'adnicategory',
            'label': 'ADNI category',
            'group': ['-50y'],
            'group_variables': ['Age group'],
            'count': 3,
            'unique': 3,
            'top': 'Other',
            'frequency': {
                'Other': 1,
                'CN': 1,
                'AD': 1
            },
            'null_count': 0
        }, {
            'index': 'agegroup',
            'label': 'Age group',
            'group': ['-50y'],
            'group_variables': ['Age group'],
            'count': 3,
            'unique': 1,
            'top': '-50y',
            'frequency': {
                '-50y': 3,
                '59y-': 0,
                '50-59y': 0
            },
            'null_count': 0
        }
    ]


@mock.patch('statistics.io_helper.fetch_data')
@mock.patch('statistics.io_helper.save_results')
def test_intermediate_stats_empty(mock_save_results, mock_fetch_data):
    data = fx.inputs_regression(include_categorical=True, add_null=True)
    data['data']['dependent'][0]['series'] = []
    mock_fetch_data.return_value = data

    with mock.patch('sys.exit'):
        intermediate_stats()

    error = mock_save_results.call_args[0][1]
    assert error == 'Dependent variable has no values, check your SQL query.'


def intermediate_data_1():
    return {
        'schema': {},
        'data': [
            {
                'index': 'iq',
                'label': 'IQ',
                'group': ['all'],
                'group_variables': [],
                'count': 3,
                'mean': 80,
                'std': 10,
                'min': 70,
                'max': 120,
                'EX^2': 8000,
                'null_count': 1,
            }
        ]
    }


def intermediate_data_2():
    return {
        'schema': {},
        'data': [
            {
                'index': 'iq',
                'label': 'IQ',
                'group': ['all'],
                'group_variables': [],
                'count': 5,
                'mean': 100,
                'std': 20,
                'min': 80,
                'max': 130,
                'EX^2': 12000,
                'null_count': 0,
            }
        ]
    }


@mock.patch('statistics.io_helper.get_results')
@mock.patch('statistics.io_helper.save_results')
def test_aggregate_stats_real(mock_save_results, mock_get_results):

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
            'label': 'IQ',
            'group': ['all'],
            'group_variables': [],
            'mean': 92.5,
            'std': 44.0879802214,
            'min': 70,
            'max': 130,
            'count': 8,
            'null_count': 1
        }
    ]


def intermediate_data_1_nominal():
    return {
        'schema': {},
        'data': [
            {
                'count': 6,
                'frequency': {
                    'AD': 1,
                    'CN': 2,
                    'Other': 3
                },
                'label': 'Score test',
                'group': ['59y-'],
                'group_variables': ['Age group'],
                'index': 'score_test1',
                'null_count': 2,
                'unique': 3
            }
        ]
    }


@mock.patch('statistics.io_helper.get_results')
@mock.patch('statistics.io_helper.save_results')
def test_aggregate_stats_nominal(mock_save_results, mock_get_results):

    def mock_results(job_id):
        if job_id == '1':
            return mock.MagicMock(data=json.dumps(intermediate_data_1_nominal()))
        elif job_id == '2':
            return mock.MagicMock(data=json.dumps(intermediate_data_1_nominal()))

    mock_get_results.side_effect = mock_results

    aggregate_stats(['1', '2'])
    results = json.loads(mock_save_results.call_args[0][0])
    assert results['data'] == [
        {
            'index': 'score_test1',
            'label': 'Score test',
            'group': ['59y-'],
            'group_variables': ['Age group'],
            'count': 12,
            'null_count': 4,
            'frequency': {
                'AD': 2,
                'CN': 4,
                'Other': 6
            }
        }
    ]
