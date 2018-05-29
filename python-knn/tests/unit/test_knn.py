import mock
import json
from . import fixtures as fx
from knn import compute, aggregate_knn


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.get_results')
@mock.patch('knn.io_helper.save_results')
def test_compute_regression(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_regression(include_integer=True)
    mock_get_results.return_value = None

    compute()

    pfa = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa)

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    # try prediction (PFA correctness is tested in sklearn_to_pfa)
    pred = engine.action({'stress_before_test1': 10., 'iq': 10., 'subjectageyears': 70})
    assert round(pred) == 1102


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.get_results')
@mock.patch('knn.io_helper.save_results')
def test_compute_classification(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_classification(include_integer=True)
    mock_get_results.return_value = None

    compute()

    pfa = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa)

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    # try prediction (PFA correctness is tested in sklearn_to_pfa)
    pred = engine.action({'stress_before_test1': 10., 'iq': 10., 'subjectageyears': 70})
    assert pred == 'AD'


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.save_error')
@mock.patch('sys.exit')
def test_compute_empty(mock_exit, mock_save_error, mock_fetch_data):
    # create mock objects from database
    data = fx.inputs_classification()

    # all NULLs
    data['data']['independent'][0]['series'] = [None] * len(data['data']['independent'][0]['series'])

    mock_fetch_data.return_value = data

    compute()

    mock_exit.assert_called_once_with(1)
    assert mock_save_error.call_args[0] == ('No data left after removing NULL values, cannot fit model.',)


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.save_results')
@mock.patch('knn.io_helper.load_intermediate_json_results')
def test_aggregate_knn(mock_load_intermediate_json_results, mock_save_results, mock_fetch_data):
    # get one PFA
    mock_fetch_data.return_value = fx.inputs_regression(include_integer=True)
    mock_load_intermediate_json_results.return_value = None
    compute()
    pfa = mock_save_results.call_args[0][0]

    mock_load_intermediate_json_results.return_value = [
        json.loads(pfa), json.loads(pfa)
    ]

    aggregate_knn(['1', '2'])

    pfa_combined = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa_combined)
    assert len(pfa_dict['cells']['codebook']['init']) == 2 * len(json.loads(pfa)['cells']['codebook']['init'])

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'subjectageyears': 70})
