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
    engine.action({'stress_before_test1': 10., 'iq': 10., 'subjectageyears': 70})


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
    engine.action({'stress_before_test1': 10., 'iq': 10., 'subjectageyears': 70})


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.save_results')
@mock.patch('sys.exit')
def test_compute_empty(mock_exit, mock_save_results, mock_fetch_data):
    # create mock objects from database
    data = fx.inputs_classification()

    # all NULLs
    data['data']['independent'][0]['series'] = [None] * len(data['data']['independent'][0]['series'])

    mock_fetch_data.return_value = data

    compute()

    mock_exit.assert_called_once_with(1)
    assert mock_save_results.call_args[0] == (
        '', 'No data left after removing NULL values, cannot fit model.', 'text/plain+error'
    )


@mock.patch('knn.io_helper.fetch_data')
@mock.patch('knn.io_helper.get_results')
@mock.patch('knn.io_helper.save_results')
def test_aggregate_knn(mock_save_results, mock_get_results, mock_fetch_data):
    # get one PFA
    mock_fetch_data.return_value = fx.inputs_regression(include_integer=True)
    mock_get_results.return_value = None
    compute()
    pfa = mock_save_results.call_args[0][0]

    def mock_results(job_id):
        if job_id == '1':
            return mock.MagicMock(data=pfa, error='')
        elif job_id == '2':
            return mock.MagicMock(data=pfa, error='')

    mock_get_results.side_effect = mock_results

    aggregate_knn(['1', '2'])

    pfa_combined = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa_combined)
    assert len(pfa_dict['cells']['codebook']['init']) == 2 * len(json.loads(pfa)['cells']['codebook']['init'])

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'subjectageyears': 70})
