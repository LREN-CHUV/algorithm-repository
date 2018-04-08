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
import argparse

from mip_helper import io_helper, shapes, utils, parameters, errors
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
    params = parameters.fetch_parameters()

    if dep_var['type']['name'] in ('polynominal', 'binominal'):
        job_type = 'classification'
    else:
        job_type = 'regression'

    logging.info('Creating new estimator')
    estimator = _create_estimator(job_type, params)
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


def aggregate_knn(job_ids):
    """Get all kNN from all nodes and create one model from them.
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    pfas = _load_intermediate_data(job_ids)

    # Put all PFAs together by combining `points`
    pfa = _combine_knn_pfas(pfas)

    # Save job_result
    logging.info('Saving PFA to job_results table...')
    pfa = json.dumps(pfa)
    logging.info("Results:\n{}".format(pfa))
    io_helper.save_results(pfa, '', shapes.Shapes.PFA)


def _combine_knn_pfas(pfas):
    # assume that all PFAs are the same except of codebook
    combined_pfa = pfas[0]
    for pfa in pfas[1:]:
        combined_pfa['cells']['codebook']['init'] += pfa['cells']['codebook']['init']
    return combined_pfa


def _load_intermediate_data(job_ids):
    data = []
    for job_id in job_ids:
        job_result = io_helper.get_results(job_id)

        # log errors (e.g. about missing data), but do not reraise them
        if job_result.error:
            logging.warning(job_result.error)
        else:
            pfa = json.loads(job_result.data)
            data.append(pfa)

    if not data:
        raise errors.UserError('All jobs {} returned an error.'.format(job_ids))

    return data


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
    parser = argparse.ArgumentParser()
    parser.add_argument('compute', choices=['compute'])
    parser.add_argument('--mode', choices=['intermediate', 'aggregate'], default='intermediate')
    # QUESTION: (job_id, node) is a primary key of `job_result` table. Does it mean I'll need node ids as well in order
    # to query unique job?
    parser.add_argument('--job-ids', type=str, nargs="*", default=[])

    args = parser.parse_args()

    # > compute --mode intermediate
    if args.mode == 'intermediate':
        compute()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_knn(args.job_ids)
