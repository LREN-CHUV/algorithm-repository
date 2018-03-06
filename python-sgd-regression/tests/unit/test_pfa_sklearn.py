# TODO: run pytest command `python -m pytest tests/test_pfa_sklearn.py --capture=no` from docker

import numpy as np
import pandas as pd
from titus.genpy import PFAEngine
from sklearn.linear_model import SGDRegressor, SGDClassifier
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import datasets

from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa


def _sgd_regressor(X, y):
    estimator = SGDRegressor()
    estimator.partial_fit(X, y)
    return estimator


def _mlp_regressor(X, y):
    estimator = MLPRegressor(hidden_layer_sizes=(3, 3))
    estimator.partial_fit(X, y)
    return estimator


def _sgd_classifier(X, y, **kwargs):
    estimator = SGDClassifier()
    estimator.partial_fit(X, y, **kwargs)
    return estimator


def _mlp_classifier(X, y, **kwargs):
    estimator = MLPClassifier(hidden_layer_sizes=(3, 3))
    estimator.partial_fit(X, y, **kwargs)
    return estimator


def _multinomialnb(X, y, **kwargs):
    estimator = MultinomialNB()
    estimator.partial_fit(X, y, **kwargs)
    return estimator


def _predict_pfa(X, types, pfa):
    engine, = PFAEngine.fromJson(pfa)
    columns = [c for c, _ in types]

    pfa_pred = []
    for x in X:
        pfa_pred.append(engine.action(dict(zip(columns, x))))
    return np.array(pfa_pred)


def _regression_task(n_features=10):
    X, y = datasets.make_regression(n_samples=100, n_features=n_features)
    types = [('feature{}'.format(i), 'double') for i in range(n_features)]
    return X, y, types


def _arrays_equal(x, y):
    return all(abs(x - y) < 1e-5)


def test_estimator_to_pfa_sgd_regressor():
    """Check that converted PFA is giving the same results as SGDRegressor"""
    X, y, types = _regression_task()
    estimator = _sgd_regressor(X, y)

    pfa = sklearn_to_pfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pfa)

    assert _arrays_equal(estimator_pred, pfa_pred)


def test_estimator_to_pfa_mlp_regressor():
    """Check that converted PFA is giving the same results as MLPRegressor"""
    X, y, types = _regression_task()
    estimator = _mlp_regressor(X, y)

    pfa = sklearn_to_pfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pfa)

    assert _arrays_equal(estimator_pred, pfa_pred)


def _classification_task(n_features=5):
    X, y = datasets.make_classification(n_samples=100, n_features=n_features, n_redundant=0, n_informative=n_features, n_classes=3)
    y = pd.Series(y).map({0: 'a', 1: 'b', 2: 'c'}).values

    types = [('feature{}'.format(i), 'double') for i in range(n_features)]
    return X, y, types


def test_estimator_to_pfa_sgd_classifier():
    """Check that converted PFA is giving the same results as SGDClassifier"""
    X, y, types = _classification_task()
    estimator = _sgd_classifier(X, y, classes=['a', 'b', 'c'])

    pfa = sklearn_to_pfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pfa)

    assert all(estimator_pred == pfa_pred)


def test_estimator_to_pfa_mlp_classifier():
    """Check that converted PFA is giving the same results as MLPClassifier"""
    X, y, types = _classification_task()
    estimator = _mlp_classifier(X, y, classes=['a', 'b', 'c'])

    pfa = sklearn_to_pfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pfa)

    assert all(estimator_pred == pfa_pred)


def test_estimator_to_pfa_multinomialnb():
    """Check that converted PFA is giving the same results as MultinomialNB"""
    X, y, types = _classification_task()

    # artifically create 0, 1 inputs from X because `MultinomialNB` works only with counts
    X = (X > 0).astype(int)

    estimator = _multinomialnb(X, y, classes=['a', 'b', 'c'])

    pfa = sklearn_to_pfa(estimator, types)

    estimator_pred = estimator.predict(X)
    pfa_pred = _predict_pfa(X, types, pfa)

    assert all(estimator_pred == pfa_pred)
