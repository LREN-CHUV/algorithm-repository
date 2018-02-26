#!/usr/bin/env python3

# QUESTION: when creating files in python-sgd-regression I copied folder python-linear-regression and just renamed
# `linear-regression` to `sgd-regression`. Is there another way? e.g. cookiecutter template or something?

# QUESTION: I'd like to create some python unit tests in py.test (to speed up development), any suggestions where should
# I put them?

from io_helper import io_helper
from db_models import JobResult

import logging
import json

import pandas as pd
from sklearn.linear_model import SGDRegressor
import patsy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DEFAULT_DOCKER_IMAGE = "python-sgd-regression"


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    job_id = io_helper._get_job_id()
    partial_job_id = None

    # Start reading stream of inputs
    # QUESTION: the tables `cde_*` are just for a proof of concept? How is the data going to be distributed in
    # production? Probably not as tables in a single database (in that case we wouldn't need all the serialization
    # of models and storing intermediate results in `job_result` table). In separate databases? Or is this just a
    # preparation for federated learning where each docker container (running on hospital's servers)
    # will save its intermediate results? Thanks for explanation!

    # QUESTION: related to the question above - if we indeed have all the tables in a single DB, why do we have to
    # store intermediate results to `job_result` table? Can't we just keep everything in memory?

    # TODO: we'd want to perform partial_fit multiple times on each database
    # TODO: choose table randomly on each iteration (wrap it in a generator)
    tables = ['cde_features_a', 'cde_features_b', 'cde_features_c']
    for k, table in enumerate(tables):
        # Load partial model
        if partial_job_id:
            estimator = _load_partial_estimator(partial_job_id)
        else:
            # TODO: add optional parameters to `SGDRegressor`
            estimator = SGDRegressor()

        # TODO: normalize estimator

        # TODO: PARAM_query can only handle single table -> we need to generalize this somehow
        query = io_helper._get_query()
        query_table = query.replace('FROM SAMPLE_DATA', 'FROM {}'.format(table))

        # TODO: `fetch_data` needs `sql` as optional parameter instead of hardcoded `_get_query`
        inputs = io_helper.fetch_data(sql=query_table)

        # TODO: following is copied from python-linear-regression -> DRY it and put into common library (either
        # io_helpers or a new util library in `algorithm-repository`)
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

        # Save intermediate serialized model into job_result table
        # TODO: skip this step if this is the last iteration
        estimator_json = serialize_sklearn_estimator(estimator)

        # Create new job with job_id in format `[job_id]-[iteration]` for storing partial results
        partial_job_id = '{}-{}'.format(job_id, k)

        # TODO: `save_results` need `job_id` as optional argument
        io_helper.save_results(estimator_json, '', 'json', job_id=partial_job_id)

    # Generate PFA output from the final model and save it
    pfa = sklearn_to_pfa(estimator)
    io_helper.save_results(pfa, '', 'pfa_json')


def _load_partial_estimator(job_id):
    engine = create_engine(io_helper._get_output_jdbc_url())
    session = sessionmaker(bind=engine)()

    job_result = session.query(JobResult).filter_by(job_id=job_id).first()
    deserialize_sklearn_estimator(job_result.data)
    raise NotImplementedError()


def serialize_sklearn_estimator(estimator):
    """Serialize model to JSON, see https://cmry.github.io/notes/serialize for inspiration."""
    raise NotImplementedError()


def deserialize_sklearn_estimator(js):
    """Init model from JSON."""
    raise NotImplementedError()


def sklearn_to_pfa(estimator):
    """Convert scikit-learn to PFA."""
    # QUESTION: What's the best way for generating PFA code from scikit models in your opinion? Should I use PrettyPFA
    # or generate raw JSON? Or would it be easier to write it in R and use Auerlius?
    raise NotImplementedError()


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
