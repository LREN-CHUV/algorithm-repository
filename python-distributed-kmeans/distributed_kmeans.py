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
"""
See original repository: https://github.com/MRN-Code/dkmeans/blob/master/dkmeans_singleshot.py

Compute Single-Shot K-Means with LLoyd's Algorithm or Gradient Descent
Algorithm Flow -
    1: On each site, initialize Random Centroids
    2: On each site, compute a clustering with k-many clusters
    [lloyd's algorithm]
        3: On each site, compute a local mean for each cluster
        4: On each site, recompute centroids as equal to local means
    [gradient descent]
        3: On each site, compute a local gradient for each cluster
        4: On each site, update centroids via gradient descent
    5: On each site,
        if change in centroids below some epsilon, STOP, report STOPPED
        else GOTO step 3
    6: On each site, broadcast local centroids to aggregator
    7: On the aggregator, compute merging of clusters according to
        least merging error (e.g. smallest distance betweeen centroids)
    8: Broadcast merged centroids to all sites
"""

from mip_helper import io_helper, shapes
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa
from sklearn_to_pfa.featurizer import Featurizer, Standardize, OneHotEncoding
from sklearn_to_pfa.mixed_nb import MixedNB

import logging
import json
import argparse
import numpy as np
import pandas as pd

import dkmeans.local_computations as local
import dkmeans.remote_computations as remote

# Configure logging
logging.basicConfig(level=logging.INFO)


def main(job_id, generate_pfa):
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    if dep_var['type']['name'] in ('polynominal', 'binominal'):
        job_type = 'classification'
    else:
        job_type = 'regression'

    # Get existing results with partial model if they exist
    if job_id:
        job_result = io_helper.get_results(job_id=str(job_id))

        logging.info('Loading existing estimator')
        estimator = deserialize_sklearn_estimator(job_result.data)
    else:
        logging.info('Creating new estimator')
        estimator = _create_estimator(job_type)

    # featurization
    transforms = []
    for var in indep_vars:
        if var['type']['name'] in ('integer', 'real'):
            transforms.append(Standardize(var['name'], var['mean'], var['std']))
        elif var["type"]["name"] in ['polynominal', 'binominal']:
            transforms.append(OneHotEncoding(var['name'], var['type']['enumeration']))

    # for NaiveBayes, continuous variables must go before nominal ones
    if isinstance(estimator, MixedNB):
        transforms = sorted(transforms, key=lambda x: not isinstance(x, Standardize))
        is_nominal = []
        for tf in transforms:
            if isinstance(tf, Standardize):
                is_nominal.append(False)
            elif isinstance(tf, OneHotEncoding):
                is_nominal += [True] * len(tf.enumerations)
        estimator.is_nominal = is_nominal

    featurizer = Featurizer(transforms)

    # convert variables into dataframe
    X, y = get_Xy(dep_var, indep_vars)
    X = featurizer.transform(X)

    # Drop NaN values
    # TODO: how should we treat NaNs?
    is_null = (pd.isnull(X).any(1) | pd.isnull(y)).values
    X = X[~is_null, :]
    y = y[~is_null]

    if len(X) == 0:
        logging.warning("All data are NULL, cannot fit model")
    else:
        # Train single step
        if job_type == 'classification':
            estimator.partial_fit(X, y, classes=dep_var['type']['enumeration'])
        else:
            estimator.partial_fit(X, y)

    serialized_estimator = serialize_sklearn_estimator(estimator)

    if generate_pfa:
        # Create PFA from the estimator
        types = [(var['name'], var['type']['name']) for var in indep_vars]
        pfa = sklearn_to_pfa(estimator, types, featurizer.generate_pretty_pfa())

        # Add serialized model as metadata
        pfa['metadata'] = {'estimator': serialized_estimator}

        # Save or update job_result
        logging.info('Saving PFA to job_results table')
        pfa = json.dumps(pfa)
        io_helper.save_results(pfa, '', shapes.Shapes.PFA)
    else:
        # Save or update job_result
        logging.info('Saving serialized estimator into job_results table')
        io_helper.save_results(serialized_estimator, '', shapes.Shapes.JSON)


def intermediate_kmeans():
    """Calculate kNN locally."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()
    indep_vars = inputs["data"]["independent"]

    # Load data into a Pandas dataframe
    logging.info("Loading data...")
    X = get_X(indep_vars)

    # Drop NaN values
    # TODO: how should we treat NaNs?
    X = X.dropna()
    if len(X) == 0:
        logging.warning("All data are NULL, cannot fit model")
        return

    # Generate results
    logging.info("Generating results...")

    # featurization
    transforms = []
    for var in indep_vars:
        if var['type']['name'] in ('integer', 'real'):
            transforms.append(Standardize(var['name'], var['mean'], var['std']))
        elif var["type"]["name"] in ['polynominal', 'binominal']:
            transforms.append(OneHotEncoding(var['name'], var['type']['enumeration']))
    featurizer = Featurizer(transforms)

    X = featurizer.transform(X)

    # TODO: set centroids dynamically
    k = 5
    optimization = 'lloyd'
    epsilon = 0.00001
    lr = 0.01

    m, n = X.shape
    num_iter = 0
    not_converged = True

    # Run kNN locally
    # Have each site compute k initial clusters locally
    local_centroids = local.initialize_own_centroids(X, k)

    # Local Optimization Loop
    while not_converged:
        # Each local site computes its cluster
        cluster_labels = local.compute_clustering(X, local_centroids)
        if optimization == 'lloyd':
            # Computes its local mean if doing lloyd, and updates centroids
            local_means = local.compute_mean(X, cluster_labels, k)
            local_centroids, previous_centroids = local.mean_step(local_means, local_centroids)
        elif optimization == 'gradient':
            # Computes the local gradient if doing GD, and takes a GD step
            local_grad = local.compute_gradient(X, cluster_labels, local_centroids, lr)
            local_centroids, previous_centroids = local.gradient_step(local_grad, local_centroids)

        # Check local stopping conditions
        not_converged, local_delta = local.check_stopping(local_centroids, previous_centroids, epsilon)

        num_iter += 1
        logging.info("Single-Shot {} ; iter : {} delta : {}".format(optimization, num_iter, local_delta))

    results = {'centroids': [lc.tolist() for lc in local_centroids]}

    logging.info("Results:\n{}".format(results))
    io_helper.save_results(pd.json.dumps(results), '', shapes.Shapes.JSON)
    logging.info("DONE")


def aggregate_kmeans(job_ids):
    """Compute merging of clusters according to least merging error (e.g. smallest distance betweeen centroids)
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    data = [json.loads(io_helper.get_results(job_id).data) for job_id in job_ids]

    local_centroids = [np.array(x['centroids']) for x in data]

    # Aggregate clusters remotely
    remote_centroids = remote.aggregate_clusters(local_centroids)

    results = {'centroids': remote_centroids}

    logging.info("Results:\n{}".format(results))
    io_helper.save_results(pd.json.dumps(results), '', shapes.Shapes.JSON)
    logging.info("DONE")


def get_X(indep_vars):
    """Create dataframe from input data.
    :param dep_var:
    :param indep_vars:
    :return: dataframe with data from all variables

    TODO: move this function to `io_helper` and reuse it in python-sgd-regressor
    """
    df = {}
    for var in indep_vars:
        # categorical variable - we need to add all categories to make one-hot encoding work right
        if 'enumeration' in var['type']:
            df[var['name']] = pd.Categorical(var['series'], categories=var['type']['enumeration'])
        else:
            # infer type automatically
            df[var['name']] = var['series']
    X = pd.DataFrame(df)
    return X


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('compute', choices=['compute'])
    parser.add_argument('--mode', choices=['intermediate', 'aggregate'], default='intermediate')
    # QUESTION: (job_id, node) is a primary key of `job_result` table. Does it mean I'll need node ids as well in order
    # to query unique job?
    parser.add_argument('--job-ids', type=int, nargs="*", default=[])

    args = parser.parse_args()

    # > compute --mode intermediate
    if args.mode == 'intermediate':
        intermediate_kmeans()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_kmeans(args.job_ids)
