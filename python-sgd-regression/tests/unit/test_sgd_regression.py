from sklearn.linear_model import SGDRegressor
from pandas.io import json
import mock
import pytest
from . import fixtures as fx
from sgd_regression import main, serialize_sklearn_estimator, deserialize_sklearn_estimator, _parse_parameters
from sklearn import datasets


@pytest.mark.parametrize(
    "method,name", [
        ("linear_model", "SGDRegressor"),
        ("neural_network", "MLPRegressor"),
        ("gradient_boosting", "GradientBoostingRegressor"),
    ]
)
@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.parameters.fetch_parameters')
def test_main_regression(mock_parameters, mock_save_results, mock_get_results, mock_fetch_data, method, name):
    # create mock objects from database
    mock_parameters.return_value = {'type': method}
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    pfa = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa)

    # NOTE: this does not work due to bug in jsonpickle
    # deserialize model
    # estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
    # assert estimator.__class__.__name__ == name

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'agegroup': '-50y'})


@pytest.mark.parametrize("method,name", [
    ("linear_model", "SGDRegressor"),
    ("neural_network", "MLPRegressor"),
])
@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.parameters.fetch_parameters')
def test_main_partial(mock_parameters, mock_save_results, mock_get_results, mock_fetch_data, method, name):
    # create mock objects from database
    mock_parameters.return_value = {'type': method}
    mock_fetch_data.return_value = fx.inputs_regression()
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=False)

    js = json.loads(mock_save_results.call_args[0][0])
    estimator = deserialize_sklearn_estimator(js['estimator'])
    assert estimator.__class__.__name__ == name


@pytest.mark.parametrize(
    "method,name", [
        ("linear_model", "SGDClassifier"), ("neural_network", "MLPClassifier"),
        ("gradient_boosting", "GradientBoostingClassifier"), ('naive_bayes', 'MixedNB')
    ]
)
@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.parameters.fetch_parameters')
def test_main_classification(mock_parameters, mock_save_results, mock_get_results, mock_fetch_data, method, name):
    # create mock objects from database
    mock_parameters.return_value = {'type': method}
    mock_fetch_data.return_value = fx.inputs_classification(include_categorical=True)
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    pfa = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa)

    # NOTE: this does not work due to bug in jsonpickle
    # deserialize model
    # estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
    # assert estimator.__class__.__name__ == name

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'agegroup': '50-59y'})


@pytest.mark.parametrize(
    "method,name", [
        ("linear_model", "SGDClassifier"),
        ("neural_network", "MLPClassifier"),
        # ("gradient_boosting", "GradientBoostingClassifier"),
        ('naive_bayes', 'MixedNB')
    ]
)
@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.parameters.fetch_parameters')
def test_main_classification_single_class(mock_parameters, mock_save_results, mock_get_results, mock_fetch_data, method, name):
    # create mock objects from database
    mock_parameters.return_value = {'type': method}
    data = fx.inputs_classification(include_categorical=True)
    data['data']['dependent'][0]['series'] = len(data['data']['dependent'][0]['series']) * ['AD']
    mock_fetch_data.return_value = data
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    pfa = mock_save_results.call_args[0][0]
    pfa_dict = json.loads(pfa)

    # NOTE: this does not work due to bug in jsonpickle
    # deserialize model
    # estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
    # assert estimator.__class__.__name__ == name

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'agegroup': '50-59y'})


@pytest.mark.parametrize(
    "method,name", [
        ("linear_model", "SGDClassifier"), ("neural_network", "MLPClassifier"),
        ("gradient_boosting", "GradientBoostingClassifier"), ('naive_bayes', 'MixedNB')
    ]
)
@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.io_helper.save_error')
@mock.patch('sgd_regression.parameters.fetch_parameters')
@mock.patch('sys.exit')
def test_main_classification_empty(
    mock_exit, mock_parameters, mock_save_error, mock_save_results, mock_get_results, mock_fetch_data, method, name
):
    # create mock objects from database
    mock_parameters.return_value = {'type': method}

    # one column has all NULL values
    data = fx.inputs_classification(include_categorical=True)
    data['data']['independent'][0]['series'] = [None] * len(data['data']['independent'][0]['series'])

    mock_fetch_data.return_value = data
    mock_get_results.return_value = None

    main(job_id=None, generate_pfa=True)

    mock_exit.assert_called_once_with(1)
    assert mock_save_error.call_args[0] == ('Model was not fitted on any data, cannot generate PFA.', )


@pytest.mark.parametrize("method,name", [
    ("linear_model", "SGDRegressor"),
    ("neural_network", "MLPRegressor"),
])
@mock.patch('sgd_regression.io_helper.fetch_data')
@mock.patch('sgd_regression.io_helper.get_results')
@mock.patch('sgd_regression.io_helper.save_results')
@mock.patch('sgd_regression.parameters.fetch_parameters')
def test_main_distributed(mock_parameters, mock_save_results, mock_get_results, mock_fetch_data, method, name):
    mock_parameters.return_value = {'type': method}
    mock_fetch_data.return_value = fx.inputs_regression()
    mock_get_results.return_value = None

    # run intermediate job
    main(job_id=None, generate_pfa=False)

    mock_get_results.return_value = mock.MagicMock(data=mock_save_results.call_args[0][0])

    # generate PFA
    main(job_id='1', generate_pfa=True)

    pfa = mock_save_results.call_args_list[1][0][0]
    pfa_dict = json.loads(pfa)

    # make some prediction with PFA
    from titus.genpy import PFAEngine
    engine, = PFAEngine.fromJson(pfa_dict)
    engine.action({'stress_before_test1': 10., 'iq': 10., 'agegroup': '-50y'})


def test_deserialize_sklearn_estimator():
    X, y = datasets.make_regression(n_samples=100, n_features=10)
    estimator = SGDRegressor().fit(X, y)

    serialized = serialize_sklearn_estimator(estimator)
    original = deserialize_sklearn_estimator(serialized)
    for col in ('intercept_', 'coef_'):
        del original.__dict__[col]
        del estimator.__dict__[col]
    assert original.__dict__ == estimator.__dict__


def test_parse_parameters():
    assert _parse_parameters({'class_prior': '0.5, 0.5'}) == {'class_prior': [0.5, 0.5]}
    assert _parse_parameters({'class_prior': '1.'}) == {'class_prior': [1]}
    assert _parse_parameters({'class_prior': '1'}) == {'class_prior': [1]}
    assert _parse_parameters({'hidden_layer_sizes': '10, 50, 10'}) == {'hidden_layer_sizes': [10, 50, 10]}
    assert _parse_parameters({
        'alpha': '0.05',
        'max_depth': '3',
        'penalty': 'l1'
    }) == {
        'alpha': 0.05,
        'max_depth': 3,
        'penalty': 'l1'
    }
