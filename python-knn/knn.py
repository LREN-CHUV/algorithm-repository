#!/usr/bin/env python3
# Copyright (c) 2017 LREN CHUV for Human Brain Project
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
from pandas.io import json
import pandas as pd
import sys

from mip_helper import io_helper, shapes
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa
from sklearn_to_pfa.featurizer import Featurizer, Standardize, OneHotEncoding
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier


# Configure logging
logging.basicConfig(level=logging.INFO)


# TODO: put into mip_helper/utils.py
class UserError(Exception):

    pass


EXIT_ON_ERROR_PARAM = "exit_on_error"
DEFAULT_EXIT_ON_ERROR = True


def compute():
    """Create PFA for kNN."""
    try:
        inputs = io_helper.fetch_data()
        dep_var = inputs["data"]["dependent"][0]
        indep_vars = inputs["data"]["independent"]
        parameters = {x['name']: x['value'] for x in inputs['parameters']}

        if dep_var['type']['name'] in ('polynominal', 'binominal'):
            job_type = 'classification'
        else:
            job_type = 'regression'

        logging.info('Creating new estimator')
        estimator = _create_estimator(job_type, parameters)
        featurizer = _create_featurizer(indep_vars)

        # convert variables into dataframe
        X, y = get_Xy(dep_var, indep_vars)
        X, y = _remove_nulls(X, y)
        X = featurizer.transform(X)

        # Drop NaN values
        estimator.fit(X, y)

        # Create PFA from the estimator
        types = [(var['name'], var['type']['name']) for var in indep_vars]
        pfa = sklearn_to_pfa(estimator, types, featurizer.generate_pretty_pfa())
        pfa['name'] = "kNN"

        # Save or update job_result
        logging.info('Saving PFA to job_results table...')
        pfa = json.dumps(pfa)
        io_helper.save_results(pfa, '', shapes.Shapes.PFA)
    except UserError as e:
        # TODO: put into mip_helper/utils as a decorator
        logging.error(e)
        io_helper.save_results('', str(e), shapes.Shapes.ERROR)

        exit_on_error = get_boolean_param(inputs["parameters"], EXIT_ON_ERROR_PARAM, DEFAULT_EXIT_ON_ERROR)
        if exit_on_error:
            sys.exit(1)


def _create_estimator(job_type, parameters):
    n_neighbors = int(parameters.get('k', 5))

    if job_type == 'regression':
        return KNeighborsRegressor(n_neighbors=n_neighbors)
    elif job_type == 'classification':
        return KNeighborsClassifier(n_neighbors=n_neighbors)


def _remove_nulls(X, y):
    is_null = (pd.isnull(X).any(1) | pd.isnull(y)).values
    X = X.loc[~is_null, :]
    y = y.loc[~is_null]
    if len(X) == 0:
        raise UserError('No data left after removing NULL values, cannot fit model.')
    return X, y


def get_Xy(dep_var, indep_vars):
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
    X = pd.DataFrame(df)
    y = X[dep_var['name']]
    del X[dep_var['name']]
    return X, y


def _create_featurizer(indep_vars):
    transforms = []
    for var in indep_vars:
        if var['type']['name'] in ('integer', 'real'):
            if 'mean' not in var:
                logging.warning('Mean not available for variable {}, using default value 0.'.format(var['name']))
            if 'std' not in var:
                logging.warning('Standard deviation not available for variable {}, using default value 1.'.format(var['name']))

            transforms.append(Standardize(var['name'], var.get('mean', 0), var.get('std', 1)))
        elif var["type"]["name"] in ['polynominal', 'binominal']:
            transforms.append(OneHotEncoding(var['name'], var['type']['enumeration']))
    return Featurizer(transforms)


# TODO: put into mip_helper/io_helper
def get_boolean_param(params_list, param_name, default_value):
    for p in params_list:
        if p["name"] == param_name:
            try:
                return p["value"].lower() in ("yes", "true", "t", "1")
            except ValueError:
                logging.warning("%s cannot be cast to boolean !")
    logging.info("Using default value: %s for %s" % (default_value, param_name))
    return default_value


if __name__ == '__main__':
    compute()
