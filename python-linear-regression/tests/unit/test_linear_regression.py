import mock
import json
from . import fixtures as fx
from linear_regression import main


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_results')
def test_main(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs
    main()
    mock_save_results.assert_called_with(json.dumps(fx.outputs), '', 'application/json')
