import pytest
import mock
import json
import numpy as np
from . import fixtures as fx
from histograms import main, compute_categories, UserError, aggregate_histograms

OUTPUT_REAL = [
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
                '700.00 - 730.00', '730.00 - 760.00', '760.00 - 790.00', '790.00 - 820.00', '820.00 - 850.00',
                '850.00 - 880.00', '880.00 - 910.00', '910.00 - 940.00', '940.00 - 970.00', '970.00 - 1000.00',
                '1000.00 - 1030.00', '1030.00 - 1060.00', '1060.00 - 1090.00', '1090.00 - 1120.00', '1120.00 - 1150.00',
                '1150.00 - 1180.00', '1180.00 - 1210.00', '1210.00 - 1240.00', '1240.00 - 1270.00', '1270.00 - 1300.00'
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
            'data': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0]
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
                '700.00 - 730.00', '730.00 - 760.00', '760.00 - 790.00', '790.00 - 820.00', '820.00 - 850.00',
                '850.00 - 880.00', '880.00 - 910.00', '910.00 - 940.00', '940.00 - 970.00', '970.00 - 1000.00',
                '1000.00 - 1030.00', '1030.00 - 1060.00', '1060.00 - 1090.00', '1090.00 - 1120.00', '1120.00 - 1150.00',
                '1150.00 - 1180.00', '1180.00 - 1210.00', '1210.00 - 1240.00', '1240.00 - 1270.00', '1270.00 - 1300.00'
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
                'data': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
            }, {
                'name': '50-59y',
                'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
            }
        ]
    }
]


@mock.patch('histograms.io_helper.fetch_data')
@mock.patch('histograms.io_helper.get_results')
@mock.patch('histograms.io_helper.save_results')
def test_main_real(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)
    mock_get_results.return_value = None

    main()

    js = json.loads(mock_save_results.call_args[0][0])
    assert js == OUTPUT_REAL


OUTPUT_NOMINAL = [
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


@mock.patch('histograms.io_helper.fetch_data')
@mock.patch('histograms.io_helper.get_results')
@mock.patch('histograms.io_helper.save_results')
def test_main_nominal(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_classification(include_categorical=True)
    mock_get_results.return_value = None

    main()

    js = json.loads(mock_save_results.call_args[0][0])
    assert js == OUTPUT_NOMINAL


OUTPUT_AGGREGATE = [
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
                '700.00 - 730.00', '730.00 - 760.00', '760.00 - 790.00', '790.00 - 820.00', '820.00 - 850.00',
                '850.00 - 880.00', '880.00 - 910.00', '910.00 - 940.00', '940.00 - 970.00', '970.00 - 1000.00',
                '1000.00 - 1030.00', '1030.00 - 1060.00', '1060.00 - 1090.00', '1090.00 - 1120.00', '1120.00 - 1150.00',
                '1150.00 - 1180.00', '1180.00 - 1210.00', '1210.00 - 1240.00', '1240.00 - 1270.00', '1270.00 - 1300.00'
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
            'data': [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 2, 0]
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
                '700.00 - 730.00', '730.00 - 760.00', '760.00 - 790.00', '790.00 - 820.00', '820.00 - 850.00',
                '850.00 - 880.00', '880.00 - 910.00', '910.00 - 940.00', '940.00 - 970.00', '970.00 - 1000.00',
                '1000.00 - 1030.00', '1030.00 - 1060.00', '1060.00 - 1090.00', '1090.00 - 1120.00', '1120.00 - 1150.00',
                '1150.00 - 1180.00', '1180.00 - 1210.00', '1210.00 - 1240.00', '1240.00 - 1270.00', '1270.00 - 1300.00'
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
                'data': [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0]
            }, {
                'name': '50-59y',
                'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0]
            }
        ]
    }
]


@mock.patch('histograms.io_helper.get_results')
@mock.patch('histograms.io_helper.save_results')
def test_aggregate_histograms(mock_save_results, mock_get_results):

    def mock_results(job_id):
        data = OUTPUT_REAL
        if job_id in ('1', '2'):
            return mock.MagicMock(data=json.dumps(data))

    mock_get_results.side_effect = mock_results

    aggregate_histograms(['1', '2'])
    results = json.loads(mock_save_results.call_args[0][0])
    assert results == OUTPUT_AGGREGATE


def test_compute_categories_empty():
    dep_var = {'name': 'tiv', 'type': {'name': 'real'}, 'series': []}
    nb_bins = 20
    with pytest.raises(UserError):
        compute_categories(dep_var, nb_bins)


def test_compute_categories_null():
    dep_var = {'name': 'tiv', 'type': {'name': 'real'}, 'series': [np.nan, np.nan, np.nan]}
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
