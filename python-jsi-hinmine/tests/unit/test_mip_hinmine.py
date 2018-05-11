import mock
import json
from mip_helper import testing as t
from mip_hinmine import main


@mock.patch('mip_hinmine.io_helper.fetch_data')
@mock.patch('mip_hinmine.io_helper.get_results')
@mock.patch('mip_hinmine.io_helper.save_results')
@mock.patch('mip_hinmine.parameters.fetch_parameters')
def test_main(mock_parameters, mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = t.inputs_regression(include_nominal=False, limit_to=5)
    mock_get_results.return_value = None

    main()

    results = json.loads(mock_save_results.call_args[0][0])

    assert t.round_dict(results) == {
        'profile':
        'tabular-data-resource',
        'name':
        'hinmine-features',
        'data': [
            {
                'f_1': 0.0,
                'f_2': 0.51,
                'f_3': 0.496,
                'f_4': 0.49,
                'f_5': 0.504,
                'id': 0.0
            }, {
                'f_1': 0.509,
                'f_2': 0.0,
                'f_3': 0.496,
                'f_4': 0.492,
                'f_5': 0.503,
                'id': 1.0
            }, {
                'f_1': 0.506,
                'f_2': 0.506,
                'f_3': 0.0,
                'f_4': 0.484,
                'f_5': 0.504,
                'id': 2.0
            }, {
                'f_1': 0.505,
                'f_2': 0.508,
                'f_3': 0.49,
                'f_4': 0.0,
                'f_5': 0.497,
                'id': 3.0
            }, {
                'f_1': 0.508,
                'f_2': 0.508,
                'f_3': 0.498,
                'f_4': 0.486,
                'f_5': 0.0,
                'id': 4.0
            }
        ],
        'schema': {
            'fields': [
                {
                    'name': 'f_1',
                    'type': 'float'
                }, {
                    'name': 'f_2',
                    'type': 'float'
                }, {
                    'name': 'f_3',
                    'type': 'float'
                }, {
                    'name': 'f_4',
                    'type': 'float'
                }, {
                    'name': 'f_5',
                    'type': 'float'
                }
            ],
            'primaryKey':
            'id'
        }
    }
