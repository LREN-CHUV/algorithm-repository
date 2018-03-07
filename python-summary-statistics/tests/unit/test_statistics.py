import mock
import json
from . import fixtures as fx
from statistics import intermediate_stats, aggregate_stats, get_X


@mock.patch('statistics.io_helper.fetch_data')
@mock.patch('statistics.io_helper.save_results')
def test_intermediate_stats(mock_save_results, mock_fetch_data):
    mock_fetch_data.return_value = fx.inputs_regression(include_categorical=True)

    intermediate_stats()
    results = json.loads(mock_save_results.call_args[0][0])
    assert len(results['data']) == 16
    assert results['data'][:2] == [
        {
            'index': 'agegroup',
            'group': ['-50y'],
            'count': 3,
            'unique': 1,
            'top': '-50y',
            'freq': 3,
            'frequency': {
                '-50y': 3,
                '59y-': 0,
                '50-59y': 0
            }
        }, {
            'index': 'iq',
            'group': ['-50y'],
            'count': 3,
            'mean': 73.7882673088,
            'std': 0.2018918769,
            'min': 73.5856470359,
            '25%': 73.6876895535,
            '50%': 73.7897320711,
            '75%': 73.8895774452,
            'max': 73.9894228193,
            'EX^2': 5444.7355659833
        }
    ]


def intermediate_data_1():
    return [{'index': 'iq', 'group': ['-50y'], 'count': 3, 'mean': 80, 'std': 10, 'min': 70, 'max': 120, 'EX^2': 8000}]


def intermediate_data_2():
    return [
        {
            'index': 'iq',
            'group': ['-50y'],
            'count': 5,
            'mean': 100,
            'std': 20,
            'min': 80,
            'max': 130,
            'EX^2': 12000
        }
    ]


@mock.patch('statistics.io_helper.get_results')
@mock.patch('statistics.io_helper.save_results')
def test_aggregate_stats(mock_save_results, mock_get_results):

    def mock_results(job_id):
        if job_id == 1:
            return {'data': json.dumps(intermediate_data_1())}
        elif job_id == 2:
            return {'data': json.dumps(intermediate_data_2())}

    mock_get_results.side_effect = mock_results

    aggregate_stats([1, 2])
    results = json.loads(mock_save_results.call_args[0][0])
    assert results['data'] == [
        {
            'index': 'iq',
            'group': ['-50y'],
            'mean': 92.5,
            'std': 44.0879802214,
            'min': 70,
            'max': 130,
            'count': 8
        }, {
            'index': 'iq',
            'group': ['all'],
            'mean': 92.5,
            'std': 44.0879802214,
            'min': 70,
            'max': 130,
            'count': 8
        }
    ]


def test_get_X():
    inputs = fx.inputs_regression(include_categorical=True)
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]
    X = get_X(dep_var, indep_vars)

    assert list(X.columns) == ['agegroup', 'iq', 'score_test1', 'stress_before_test1']
    assert list(X.agegroup.cat.categories) == ['-50y', '50-59y', '59y-']
    assert X.shape == (6, 4)


# @mock.patch('sgd_regression.io_helper.fetch_data')
# @mock.patch('sgd_regression.io_helper.get_results')
# @mock.patch('sgd_regression.io_helper.save_results')
# def test_main_regression(mock_save_results, mock_get_results, mock_fetch_data):
#     # create mock objects from database
#     mock_fetch_data.return_value = fx.inputs_regression()
#     mock_get_results.return_value = None
#
#     main()
#
#     pfa = mock_save_results.call_args[0][0]
#     # TODO: convert PFA first and check individual sections instead
#     pfa_dict = json.loads(pfa)
#
#     # deserialize model
#     estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
#     assert estimator.__class__.__name__ == 'SGDRegressor'
#
#     # make some prediction with PFA
#     from titus.genpy import PFAEngine
#     engine, = PFAEngine.fromJson(pfa_dict)
#     engine.action({'stress_before_test1': 10., 'iq': 10.})
#
#
# @mock.patch('sgd_regression.io_helper.fetch_data')
# @mock.patch('sgd_regression.io_helper.get_results')
# @mock.patch('sgd_regression.io_helper.save_results')
# def test_main_classification(mock_save_results, mock_get_results, mock_fetch_data):
#     # TODO: DRY both test_main_* methods
#     # create mock objects from database
#     mock_fetch_data.return_value = fx.inputs_classification()
#     mock_get_results.return_value = None
#
#     main()
#
#     pfa = mock_save_results.call_args[0][0]
#     # TODO: convert PFA first and check individual sections instead
#     pfa_dict = json.loads(pfa)
#
#     # deserialize model
#     estimator = deserialize_sklearn_estimator(pfa_dict['metadata']['estimator'])
#     assert estimator.__class__.__name__ == 'SGDClassifier'
#
#     # make some prediction with PFA
#     from titus.genpy import PFAEngine
#     engine, = PFAEngine.fromJson(pfa_dict)
#     engine.action({'stress_before_test1': 10., 'iq': 10.})
#
#
# def test_deserialize_sklearn_estimator():
#     X, y = datasets.make_regression(n_samples=100, n_features=10)
#     estimator = SGDRegressor().fit(X, y)
#
#     serialized = serialize_sklearn_estimator(estimator)
#     original = deserialize_sklearn_estimator(serialized)
#     for col in ('intercept_', 'coef_'):
#         del original.__dict__[col]
#         del estimator.__dict__[col]
#     assert original.__dict__ == estimator.__dict__
#
#
# def test_get_Xy():
#     inputs = fx.inputs_regression()
#     X, y = get_Xy(inputs['data']['dependent'][0], inputs['data']['independent'])
#     assert list(X.columns) == ['iq', 'stress_before_test1']
#     assert len(X) == len(y) == 6
