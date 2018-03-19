import pytest
import mock
import json
from . import fixtures as fx
from histograms import main, compute_categories, UserError


@mock.patch('histograms.io_helper.fetch_data')
@mock.patch('histograms.io_helper.get_results')
@mock.patch('histograms.io_helper.save_results')
def test_main_real(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)
    mock_get_results.return_value = None

    main()

    js = json.loads(mock_save_results.call_args[0][0])
    assert js == [
        {
            'chart': {
                'type': 'column'
            },
            'label': 'Histogram',
            'title': {
                'text': 'score_test1 histogram'
            },
            'xAxis': {
                'categories': [
                    '846.26 - 866.84', '866.84 - 887.42', '887.42 - 908.00', '908.00 - 928.58', '928.58 - 949.16',
                    '949.16 - 969.74', '969.74 - 990.32', '990.32 - 1010.90', '1010.90 - 1031.48', '1031.48 - 1052.06',
                    '1052.06 - 1072.64', '1072.64 - 1093.22', '1093.22 - 1113.80', '1113.80 - 1134.38',
                    '1134.38 - 1154.96', '1154.96 - 1175.54', '1175.54 - 1196.12', '1196.12 - 1216.70',
                    '1216.70 - 1237.28', '1237.28 - 1257.86'
                ]
            },
            'yAxis': {
                'allowDecimals': False,
                'min': 0,
                'title': {
                    'text': 'Number of participants'
                }
            },
            'series': [{
                'name': 'all',
                'data': [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
            }]
        }, {
            'chart': {
                'type': 'column'
            },
            'label': 'Histogram - agegroup',
            'title': {
                'text': 'score_test1 histogram by agegroup'
            },
            'xAxis': {
                'categories': [
                    '846.26 - 866.84', '866.84 - 887.42', '887.42 - 908.00', '908.00 - 928.58', '928.58 - 949.16',
                    '949.16 - 969.74', '969.74 - 990.32', '990.32 - 1010.90', '1010.90 - 1031.48', '1031.48 - 1052.06',
                    '1052.06 - 1072.64', '1072.64 - 1093.22', '1093.22 - 1113.80', '1113.80 - 1134.38',
                    '1134.38 - 1154.96', '1154.96 - 1175.54', '1175.54 - 1196.12', '1196.12 - 1216.70',
                    '1216.70 - 1237.28', '1237.28 - 1257.86'
                ]
            },
            'yAxis': {
                'allowDecimals': False,
                'min': 0,
                'title': {
                    'text': 'Number of participants'
                }
            },
            'series': [
                {
                    'name': '-50y',
                    'data': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
                }, {
                    'name': '50-59y',
                    'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
                }
            ]
        }
    ]


@mock.patch('histograms.io_helper.fetch_data')
@mock.patch('histograms.io_helper.get_results')
@mock.patch('histograms.io_helper.save_results')
def test_main_nominal(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_classification(include_categorical=True)
    mock_get_results.return_value = None

    main()

    js = json.loads(mock_save_results.call_args[0][0])
    assert js == [
        {
            'chart': {
                'type': 'column'
            },
            'label': 'Histogram',
            'title': {
                'text': 'score_test1 histogram'
            },
            'xAxis': {
                'categories': ['AD', 'CN', 'Other']
            },
            'yAxis': {
                'allowDecimals': False,
                'min': 0,
                'title': {
                    'text': 'Number of participants'
                }
            },
            'series': [{
                'name': 'all',
                'data': [2, 2, 2]
            }]
        }, {
            'chart': {
                'type': 'column'
            },
            'label': 'Histogram - agegroup',
            'title': {
                'text': 'score_test1 histogram by agegroup'
            },
            'xAxis': {
                'categories': ['AD', 'CN', 'Other']
            },
            'yAxis': {
                'allowDecimals': False,
                'min': 0,
                'title': {
                    'text': 'Number of participants'
                }
            },
            'series': [{
                'name': '-50y',
                'data': [1, 1, 1]
            }, {
                'name': '50-59y',
                'data': [1, 1, 1]
            }]
        }
    ]


def test_compute_categories_empty():
    dep_var = {'name': 'tiv', 'type': {'name': 'real'}, 'series': []}
    nb_bins = 20
    with pytest.raises(UserError):
        compute_categories(dep_var, nb_bins)

@mock.patch('histograms.io_helper.fetch_data')
@mock.patch('histograms.io_helper.get_results')
@mock.patch('histograms.io_helper.save_results')
def test_main_categories_empty(mock_save_results, mock_get_results, mock_fetch_data):

    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_no_values()
    mock_get_results.return_value = None

    main()

    js = json.loads(mock_save_results.call_args[0][0])
    assert js == [
        {
            'chart': {'type': 'column'},
            'label': 'Histogram',
            'title': {'text': 'tiv histogram (no data or error)'},
            'xAxis': {'categories': []},
            'yAxis': {
                'allowDecimals': False,
                'min': 0,
                'title': {'text': 'Number of participants'}
            },
            'series': []
        }
    ]
