import mock
import json
import copy
from . import fixtures as fx
from linear_regression import main, intermediate, aggregate


def _round_dict(d, precision=3):
    d = copy.deepcopy(d)
    if isinstance(d, dict):
        for k, v in d.items():
            try:
                d[k] = round(v, precision)
            except TypeError:
                d[k] = _round_dict(v)
    return d


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_results')
def test_main(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)
    main()
    output = json.loads(mock_save_results.call_args[0][0])

    assert _round_dict(fx.output()) == _round_dict(output)


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_results')
def test_main_empty(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True, limit_to=0)
    main()
    output = json.loads(mock_save_results.call_args[0][0])

    assert output == {}


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.get_results')
@mock.patch('linear_regression.io_helper.save_results')
def test_aggregate(mock_save_results, mock_get_results, mock_fetch_data):
    # run partial jobs
    inputs_1 = fx.inputs_regression(limit_from=0, limit_to=8, include_categorical=True)
    mock_fetch_data.return_value = inputs_1
    intermediate()
    output_1 = mock_save_results.call_args[0][0]

    inputs_2 = fx.inputs_regression(limit_from=8, limit_to=20, include_categorical=True)
    mock_fetch_data.return_value = inputs_2
    intermediate()
    output_2 = mock_save_results.call_args[0][0]

    mock_get_results.side_effect = [
        mock.MagicMock(data=output_1, error=''),
        mock.MagicMock(data=output_2, error=''),
    ]

    # run computations
    aggregate(['1', '2'])
    output_agg = json.loads(mock_save_results.call_args[0][0])
    beta_agg = {k: v['coef'] for k, v in output_agg.items()}

    # calculate coefficients from single-node regression
    mock_fetch_data.return_value = fx.inputs_regression(limit_to=20, include_categorical=True)
    main()
    output_single = json.loads(mock_save_results.call_args[0][0])
    beta_single = {k: v['coef'] for k, v in output_single.items()}

    assert _round_dict(beta_agg) == _round_dict(beta_single)


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.get_results')
@mock.patch('linear_regression.io_helper.save_results')
def test_aggregate_single(mock_save_results, mock_get_results, mock_fetch_data):
    """Aggregation on single node should give same results as ordinary linear regression."""
    # run partial jobs
    inputs = fx.inputs_regression(limit_from=0, limit_to=20)
    mock_fetch_data.return_value = inputs
    intermediate()
    output = mock_save_results.call_args[0][0]

    mock_get_results.side_effect = [
        mock.MagicMock(data=output, error=''),
    ]

    # run computations
    aggregate(['1'])
    output_agg = json.loads(mock_save_results.call_args[0][0])

    # calculate coefficients from single-node regression
    mock_fetch_data.return_value = fx.inputs_regression(limit_to=20)
    main()
    output_single = json.loads(mock_save_results.call_args[0][0])

    assert _round_dict(output_agg) == _round_dict(output_single)
