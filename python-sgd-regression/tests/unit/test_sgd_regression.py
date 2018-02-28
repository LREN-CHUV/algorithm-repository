# TODO: run from python-sgd-regression directory with `python -m pytest tests/unit/ --capture=no`

from sklearn.linear_model import SGDRegressor
import mock
from .fixtures import inputs


def test_main(inputs):
    # create mock objects from database
    io_helper = mock.MagicMock()
    job_result = mock.MagicMock()
    job_result.data = None

    with mock.patch.dict('sys.modules', io_helper=io_helper):
        # TODO: it is imported here to avoid importing io_helpers which are not available. Fix it in docker container
        from sgd_regression import main
        io_helper.io_helper.fetch_data.return_value = inputs
        io_helper.io_helper.get_results.return_value = None

        main()

        pfa = io_helper.io_helper.save_results.call_args[0][0]
        # TODO: convert PFA first and check individual sections instead
        assert pfa.startswith("""
input: record(Data,
    stress_before_test1: real,
    iq: real
)
output: double
action:
    2986436262.26812 + 191016471927.55804 * input.stress_before_test1 + 141237784325.43924 * input.iq
metadata: {"py/object": "sklearn.linear_model.stochastic_gradient.SGDRegressor"
        """.strip())


def test_deserialize_sklearn_estimator():
    from sgd_regression import serialize_sklearn_estimator, deserialize_sklearn_estimator
    estimator = SGDRegressor()
    serialized = serialize_sklearn_estimator(estimator)
    original = deserialize_sklearn_estimator(serialized)
    assert original.__dict__ == estimator.__dict__
