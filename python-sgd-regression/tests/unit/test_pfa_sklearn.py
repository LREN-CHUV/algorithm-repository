# TODO: run pytest command `python -m pytest tests/test_pfa_sklearn.py --capture=no` from docker

import numpy as np
import pandas as pd
import titus.prettypfa as prettypfa
from titus.genpy import PFAEngine
from sklearn.linear_model import SGDRegressor, SGDClassifier
from sklearn import datasets

from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa


def _sgd_regressor(X, y):
    estimator = SGDRegressor()
    estimator.partial_fit(X, y)
    return estimator


def _sgd_classifier(X, y, **kwargs):
    estimator = SGDClassifier()
    estimator.partial_fit(X, y, **kwargs)
    return estimator


def _predict_pfa(X, types, pfa):
    engine, = PFAEngine.fromJson(pfa)
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
    X, y = datasets.make_regression(n_samples=100, n_features=N_FEATURES)
    estimator = _sgd_regressor(X, y)

    types = [('feature{}'.format(i), 'double') for i in range(N_FEATURES)]

    pfa = sklearn_to_pfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pfa)

    assert _arrays_equal(estimator_pred, pfa_pred)


def test_estimator_to_prettypfa_sgd_classifier():
    """Check that converted PFA is giving the same results as SGDClassifier"""
    N_FEATURES = 5
    X, y = datasets.make_classification(n_samples=100, n_features=N_FEATURES, n_redundant=0, n_informative=N_FEATURES, n_classes=3)
    y = pd.Series(y).map({0: 'a', 1: 'b', 2: 'c'}).values

    estimator = _sgd_classifier(X, y, classes=['a', 'b', 'c'])

    types = [('feature{}'.format(i), 'double') for i in range(N_FEATURES)]

    pfa = sklearn_to_pfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pfa)

    assert all(estimator_pred == pfa_pred)
