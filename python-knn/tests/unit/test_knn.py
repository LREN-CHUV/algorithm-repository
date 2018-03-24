import mock
import json
from . import fixtures as fx
from knn import compute


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.get_results')
@mock.patch('knn.io_helper.save_results')
def test_compute_regression(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_regression()
    mock_get_results.return_value = None

    compute()

    pfa = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa)

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10.})


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.get_results')
@mock.patch('knn.io_helper.save_results')
def test_compute_classification(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_classification()
    mock_get_results.return_value = None

    compute()

    pfa = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa)

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10.})
