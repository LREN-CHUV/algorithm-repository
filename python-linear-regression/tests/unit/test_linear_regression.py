import mock
import json
import copy
from . import fixtures as fx
from linear_regression import main


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_results')
def test_main(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs
    main()
    output = json.loads(mock_save_results.call_args[0][0])

    assert _round_dict(fx.outputs) == _round_dict(output)


def _round_dict(d, precision=3):
    d = copy.deepcopy(d)
    for k, v in d.items():
        try:
            d[k] = round(v, precision)
        except TypeError:
            d[k] = _round_dict(v)
    return d
