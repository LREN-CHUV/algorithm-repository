#!/usr/bin/env python3

from mip_helper import io_helper, shapes
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa

import logging
import json

import pandas as pd
from sklearn.linear_model import SGDRegressor, SGDClassifier
import patsy
import titus.prettypfa
import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
jsonpickle_numpy.register_handlers()


DEFAULT_DOCKER_IMAGE = "python-sgd-regression"


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Get existing results with partial model if they exist
    job_result = io_helper.get_results()

    if job_result:
        logging.info('Loading existing estimator')
        # reconstruct estimator from metadata in PFA
        pfa = _extract_metadata(job_result.data)['estimator']
        estimator = deserialize_sklearn_estimator(pfa)
    else:
        logging.info('Creating new estimator')
        # TODO: SGD-type algorithms require normalized data! how do we do that in incremental learning?
        #   see http://dask-ml.readthedocs.io/en/latest/modules/generated/dask_ml.preprocessing.StandardScaler.html#dask_ml.preprocessing.StandardScaler.partial_fit
        #   for inspiration
        # TODO: add optional parameters to `SGDRegressor`

        job_type = 'regression'

        if job_type == 'regression':
            estimator = SGDRegressor()
        elif job_type == 'classification':
            estimator = SGDClassifier()

        inputs = io_helper.fetch_data()

        dep_var = inputs["data"]["dependent"][0]
        indep_vars = inputs["data"]["independent"]

        # Check dependent variable type (should be continuous)
        if job_type == 'regression':
            if dep_var["type"]["name"] not in ["integer", "real"]:
                logging.warning("Dependent variable should be continuous!")
                return None
        elif job_type == 'classification':
            if dep_var["type"]["name"] not in ['polynominal', 'binominal']:
                logging.warning("Dependent variable needs to be categorical!")
                return None

        # Select dependent and independent variables with patsy
        # TODO: how to treat missing variables?
        X, y = get_Xy(dep_var, indep_vars)

        # Train single step
        if job_type == 'classification':
            estimator.partial_fit(X, y, classes=dep_var['type']['enumeration'])
        else:
            estimator.partial_fit(X, y)

        # Create PFA from the estimator
        types = [(var['name'], var['type']['name']) for var in indep_vars if var['name'] in X.columns]
        pretty_pfa = sklearn_to_pfa(estimator, types)
        pfa = titus.prettypfa.jsonNode(pretty_pfa)

        # Add serialized model as metadata for next partial fit
        serialized_estimator = serialize_sklearn_estimator(estimator)
        pfa['metadata'] = {
            'estimator': serialized_estimator
        }

        # Save or update job_result
        logging.info('Saving PFA to job_results table')
        pfa = json.dumps(pfa)
        io_helper.save_results(pfa, '', shapes.Shapes.PFA)


def _extract_metadata(pfa):
    """Extract metadata from PrettyPFA."""
    return json.loads(pfa)['metadata']


def serialize_sklearn_estimator(estimator):
    """Serialize model to JSON, see https://cmry.github.io/notes/serialize for inspiration."""
    return jsonpickle.encode(estimator)


def deserialize_sklearn_estimator(js):
    """Deserialize model from JSON."""
    return jsonpickle.decode(js)


def get_Xy(dep_var, indep_vars, dropna=True):
    """Create feature matrix and target from data.
    :param dep_var:
    :param indep_vars:
    :param data:
    :param dropna: drop rows with NULL values
    """
    data = generate_data(dep_var, indep_vars)

    formula = generate_formula(indep_vars, intercept=False)
    logging.info("Formula: %s" % formula)

    if dropna:
        NA_action = 'drop'
        # TODO: check NULL values and raise warning if you find them
    else:
        NA_action = 'raise'

    X = patsy.dmatrix(formula, data, NA_action=NA_action, return_type='dataframe')
    y = data[dep_var['name']]

    return X, y


def generate_data(dep_var, indep_vars):
    """Create dataframe from input data.
    :param dep_var:
    :param indep_vars:
    :return: dataframe with data from all variables
    """
    df = {}
    for var in [dep_var] + indep_vars:
        # categorical variable - we need to add all categories to make one-hot encoding work right
        if 'enumeration' in var['type']:
            df[var['name']] = pd.Categorical(var['series'], categories=var['type']['enumeration'])
        else:
            # infer type automatically
            df[var['name']] = var['series']

    return pd.DataFrame(df)


def generate_formula(indep_vars, intercept=True):
    op = " + "
    indep_vars = [v["name"] if v["type"]["name"] in ["integer", "real"]
                  else str.format("C(%s)" % v["name"]) for v in indep_vars]
    indep_vars = op.join(indep_vars).strip(op)

    if intercept:
        return indep_vars
    else:
        return "0 + {}".format(indep_vars)


if __name__ == '__main__':
    main()
