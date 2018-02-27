#!/usr/bin/env python3

from io_helper import io_helper
from sklearn_to_pfa import sklearn_to_pfa

import logging
import json

import pandas as pd
from sklearn.linear_model import SGDRegressor
import patsy
import jsonpickle


DEFAULT_DOCKER_IMAGE = "python-sgd-regression"


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Get existing results with partial model if they exist
    job_result = io_helper.get_results()

    if job_result:
        # reconstruct estimator from metadata in PFA
        pfa = json.loads(job_result.data)
        estimator = deserialize_sklearn_estimator(pfa['metadata'])
    else:
        # TODO: SGD-type algorithms require normalized data! how do we do that in incremental learning?
        #   see http://dask-ml.readthedocs.io/en/latest/modules/generated/dask_ml.preprocessing.StandardScaler.html#dask_ml.preprocessing.StandardScaler.partial_fit
        #   for inspiration
        # TODO: add optional parameters to `SGDRegressor`
        estimator = SGDRegressor()

        inputs = io_helper.fetch_data()

        dep_var = inputs["data"]["dependent"][0]
        inped_vars = inputs["data"]["independent"]

        # Check dependent variable type (should be continuous)
        if dep_var["type"]["name"] not in ["integer", "real"]:
            logging.warning("Dependent variable should be continuous !")
            return None

        # Extract data and parameters from inputs
        data = format_data(inputs["data"])

        # Select dependent and independent variables with patsy
        X, y = get_Xy(dep_var, inped_vars, data)

        # Train single step
        estimator.partial_fit(X, y)

        # Create PFA from the estimator and add serialized model as metadata for next partial fit
        pfa = sklearn_to_pfa(estimator)
        pfa += '\nmetadata: {}'.format(serialize_sklearn_estimator(estimator))

        # Save or update job_result
        # TODO: if woken cannnot convert `pfa_pretty` format we might have to do it here either with titus
        # and python 2 or its python 3 fork https://github.com/animator/hadrian
        io_helper.save_results(pfa, '', 'pfa_pretty')

    # Generate PFA output from the final model and save it
    pfa = sklearn_to_pfa(estimator)
    io_helper.save_results(pfa, '', 'pfa_json')


def serialize_sklearn_estimator(estimator):
    """Serialize model to JSON, see https://cmry.github.io/notes/serialize for inspiration."""
    return jsonpickle.encode(estimator)


def deserialize_sklearn_estimator(js):
    """Deserialize model from JSON."""
    return jsonpickle.decode(js)


def format_data(input_data):
    all_vars = input_data["dependent"] + input_data["independent"]
    data = {v["name"]: v["series"] for v in all_vars}
    return data


def format_output(statsmodels_dict):
    return json.dumps(pd.DataFrame.from_dict(statsmodels_dict).transpose().fillna("NaN").to_dict())


def get_Xy(dep_var, indep_vars, data):
    formula = generate_formula(dep_var, indep_vars)
    logging.info("Formula: %s" % formula)
    return patsy.dmatrices(formula, data, NA_action='raise', return_type='dataframe')


def generate_formula(dep_var, indep_vars):
    op = " + "
    dep_var = dep_var["name"]
    indep_vars = [v["name"] if v["type"]["name"] in ["integer", "real"]
                  else str.format("C(%s)" % v["name"]) for v in indep_vars]
    indep_vars = op.join(indep_vars)
    indep_vars = indep_vars.strip(op)
    return str.format("%s ~ %s" % (dep_var, indep_vars))


if __name__ == '__main__':
    main()
