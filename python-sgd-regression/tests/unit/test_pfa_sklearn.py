# TODO: run pytest command `python -m pytest tests/test_pfa_sklearn.py --capture=no` from docker

import numpy as np
import titus.prettypfa as prettypfa
from sklearn.linear_model import SGDRegressor
from sklearn.datasets import make_regression

from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_prettypfa


def _sgd_regressor(X, y):
    estimator = SGDRegressor()
    estimator.fit(X, y)
    return estimator


def _predict_pfa(X, types, pretty_pfa):
    engine, = prettypfa.engine(pretty_pfa)
    columns = [c for c, _ in types]

    pfa_pred = []
    for x in X:
        pfa_pred.append(engine.action(dict(zip(columns, x))))
    return np.array(pfa_pred)


def _arrays_equal(x, y):
    return all(abs(x - y) < 1e-5)


def test_estimator_to_prettypfa_sgd_regressor():
    """Check that converted PFA is giving the same results as SGDRegressor"""
    N_FEATURES = 10
    X, y = make_regression(n_samples=100, n_features=N_FEATURES)
    estimator = _sgd_regressor(X, y)

    types = [('feature{}'.format(i), 'double') for i in range(N_FEATURES)]

    pretty_pfa = sklearn_to_prettypfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pretty_pfa)

    assert _arrays_equal(estimator_pred, pfa_pred)
