from sklearn.linear_model import SGDRegressor
import json
import mock
from . import fixtures as fx
from sgd_regression import main, serialize_sklearn_estimator, deserialize_sklearn_estimator
from sklearn import datasets


@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
def test_main_regression(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    pfa = mock_save_results.call_args[0][0]
    # TODO: convert PFA first and check individual sections instead
    pfa_dict = json.loads(pfa)

    # deserialize model
    estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
    assert estimator.__class__.__name__ == 'SGDRegressor'

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'agegroup': '-50y'})


@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
def test_main_partial(mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_regression()
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=False)

    js = mock_save_results.call_args[0][0]
    estimator = deserialize_sklearn_estimator(js['estimator'])
    assert estimator.__class__.__name__ == 'SGDRegressor'


@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
def test_main_classification(mock_save_results, mock_get_results, mock_fetch_data):
    # TODO: DRY both test_main_* methods
    # create mock objects from database
    mock_fetch_data.return_value = fx.inputs_classification()
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    pfa = mock_save_results.call_args[0][0]
    # TODO: convert PFA first and check individual sections instead
    pfa_dict = json.loads(pfa)

    # deserialize model
    estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
    assert estimator.__class__.__name__ == 'SGDClassifier'

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10.})


@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.parameters.fetch_parameters')
def test_main_classification_naive_bayes(mock_parameters, mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_parameters.return_value = {'type': 'naive_bayes'}
    mock_fetch_data.return_value = fx.inputs_classification(include_categorical=True)
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    pfa = mock_save_results.call_args[0][0]
    # TODO: convert PFA first and check individual sections instead
    pfa_dict = json.loads(pfa)

    # deserialize model
    estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
    assert estimator.__class__.__name__ == 'MixedNB'

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'agegroup': '50-59y'})


@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.parameters.fetch_parameters')
@mock.patch('sys.exit')
def test_main_classification_naive_bayes_empty(mock_exit, mock_parameters, mock_save_results, mock_get_results, mock_fetch_data):
    # create mock objects from database
    mock_parameters.return_value = {'type': 'naive_bayes'}

    # one column has all NULL values
    data = fx.inputs_classification(include_categorical=True)
    data['data']['independent'][0]['series'] = [None] * len(data['data']['independent'][0]['series'])

    mock_fetch_data.return_value = data
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    mock_exit.assert_called_once_with(1)
    assert mock_save_results.call_args[0] == (
        '', 'Model was not fitted on any data, cannot generate PFA.', 'text/plain+error'
    )


def test_deserialize_sklearn_estimator():
    X, y = datasets.make_regression(n_samples=100, n_features=10)
    estimator = SGDRegressor().fit(X, y)

    serialized = serialize_sklearn_estimator(estimator)
    original = deserialize_sklearn_estimator(serialized)
    for col in ('intercept_', 'coef_'):
        del original.__dict__[col]
        del estimator.__dict__[col]
    assert original.__dict__ == estimator.__dict__
