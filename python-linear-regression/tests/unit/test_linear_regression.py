import mock
import json
from mip_helper import testing as t
from linear_regression import main, intermediate, aggregate
from . import fixtures as fx


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_results')
def test_main(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(include_nominal=True)
    main()
    output = json.loads(mock_save_results.call_args[0][0])

    assert t.round_dict(fx.output_regression()) == t.round_dict(output)


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_results')
def test_main_logistic(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_classification(limit_to=50, include_nominal=True)
    main()
    output = json.loads(mock_save_results.call_args[0][0])

    assert t.round_dict(fx.output_classification()) == t.round_dict(output)


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_error')
@mock.patch('sys.exit')
def test_main_logistic_single_category(mock_exit, mock_save_error, mock_fetch_data):
    data = t.inputs_classification(limit_to=5, include_nominal=True)
    # single output
    data['data']['dependent'][0]['series'] = len(data['data']['dependent'][0]['series']) * ['AD']

    mock_fetch_data.return_value = data
    main()
    assert mock_save_error.call_args[0] == ('Not enough data to apply logistic regression.',)


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.save_results')
def test_main_empty(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = t.inputs_regression(include_nominal=True, limit_to=0)
    main()
    output = json.loads(mock_save_results.call_args[0][0])

    assert output == {}


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.get_results')
@mock.patch('linear_regression.io_helper.save_results')
def test_aggregate(mock_save_results, mock_get_results, mock_fetch_data):
    # run partial jobs
    inputs_1 = t.inputs_regression(limit_from=0, limit_to=8, include_nominal=True)
    mock_fetch_data.return_value = inputs_1
    intermediate()
    output_1 = mock_save_results.call_args[0][0]

    inputs_2 = t.inputs_regression(limit_from=8, limit_to=20, include_nominal=True)
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
    mock_fetch_data.return_value = t.inputs_regression(limit_to=20, include_nominal=True)
    main()
    output_single = json.loads(mock_save_results.call_args[0][0])
    beta_single = {k: v['coef'] for k, v in output_single.items()}

    assert t.round_dict(beta_agg) == t.round_dict(beta_single)


@mock.patch('linear_regression.io_helper.fetch_data')
@mock.patch('linear_regression.io_helper.get_results')
@mock.patch('linear_regression.io_helper.save_results')
def test_aggregate_single(mock_save_results, mock_get_results, mock_fetch_data):
    """Aggregation on single node should give same results as ordinary linear regression."""
    # run partial jobs
    inputs = t.inputs_regression(limit_from=0, limit_to=20)
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
    mock_fetch_data.return_value = t.inputs_regression(limit_to=20)
    main()
    output_single = json.loads(mock_save_results.call_args[0][0])

    assert t.round_dict(output_agg) == t.round_dict(output_single)
