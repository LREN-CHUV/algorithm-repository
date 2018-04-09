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

from mip_helper import io_helper, shapes, utils
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa
from sklearn_to_pfa.featurizer import Featurizer, Standardize, OneHotEncoding
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier


# Configure logging
logging.basicConfig(level=logging.INFO)


@utils.catch_user_error
def compute():
    """Create PFA for kNN."""
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
    X = io_helper.fetch_dataframe(variables=[dep_var] + indep_vars)
    X = utils.remove_nulls(X)
    y = X.pop(dep_var['name'])
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


def _create_estimator(job_type, parameters):
    n_neighbors = int(parameters.get('k', 5))

    if job_type == 'regression':
        return KNeighborsRegressor(n_neighbors=n_neighbors)
    elif job_type == 'classification':
        return KNeighborsClassifier(n_neighbors=n_neighbors)


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


if __name__ == '__main__':
    compute()
