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

import logging
import json
import argparse
import numpy as np
import pandas as pd

from mip_helper import io_helper, shapes
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa
from sklearn_to_pfa.featurizer import Featurizer, Standardize, OneHotEncoding
import dkmeans.local_computations as local
import dkmeans.remote_computations as remote
from sklearn.cluster import KMeans


# Configure logging
logging.basicConfig(level=logging.INFO)


# Hardcoded constants for single-shot Lloyd's algorithm, can be put into MODEL_PARAM_* envs if needed
OPTIMIZATION = 'lloyd'
EPSILON = 0.00001
LR = 0.01  # learning rate for gradient descent, not used for Lloyd version


def intermediate_kmeans():
    """Calculate kNN locally."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()
    indep_vars = inputs["data"]["independent"]

    # Extract hyperparameters from ENV variables
    params = {x['name']: x['value'] for x in inputs['parameters']}
    k = int(params.get('n_clusters', 8))

    # Load data into a Pandas dataframe
    logging.info("Loading data...")
    X = get_X(indep_vars)

    # Return variables info, but remove actual data points
    results = {'indep_vars': []}
    for iv in indep_vars:
        del iv['series']
        results['indep_vars'].append(iv)

    # Drop NaN values
    # TODO: how should we treat NaNs?
    X = X.dropna()
    if len(X) == 0:
        logging.warning("All data are NULL, returning empty centroids.")
        results['centroids'] = []
        io_helper.save_results(pd.json.dumps(results), '', shapes.Shapes.JSON)
        return

    # Generate results
    logging.info("Generating results...")

    # featurization
    featurizer = _create_featurizer(indep_vars)
    X = featurizer.transform(X)

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
        if OPTIMIZATION == 'lloyd':
            # Computes its local mean if doing lloyd, and updates centroids
            local_means = local.compute_mean(X, cluster_labels, k)
            local_centroids, previous_centroids = local.mean_step(local_means, local_centroids)
        elif OPTIMIZATION == 'gradient':
            # Computes the local gradient if doing GD, and takes a GD step
            local_grad = local.compute_gradient(X, cluster_labels, local_centroids, LR)
            local_centroids, previous_centroids = local.gradient_step(local_grad, local_centroids)

        # Check local stopping conditions
        not_converged, local_delta = local.check_stopping(local_centroids, previous_centroids, EPSILON)

        num_iter += 1
        logging.info("Single-Shot {} ; iter : {} delta : {}".format(OPTIMIZATION, num_iter, local_delta))

    results['centroids'] = [lc.tolist() for lc in local_centroids]

    logging.info("Results:\n{}".format(results))
    io_helper.save_results(pd.json.dumps(results), '', shapes.Shapes.JSON)
    logging.info("DONE")


def aggregate_kmeans(job_ids):
    """Compute merging of clusters according to least merging error (e.g. smallest distance betweeen centroids)
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    data = [json.loads(io_helper.get_results(str(job_id)).data) for job_id in job_ids]

    local_centroids = [np.array(x['centroids']) for x in data if x['centroids']]
    indep_vars = data[0]['indep_vars']

    # Aggregate clusters remotely
    remote_centroids = remote.aggregate_clusters(local_centroids)
    logging.info("Centroids:\n{}".format(remote_centroids))

    # Create fake KMeans estimator and assign it our centroids
    estimator = KMeans()
    estimator.cluster_centers_ = np.array(remote_centroids)

    # Generate PFA for kmeans and add centroids to metadata
    featurizer = _create_featurizer(indep_vars)
    types = [(var['name'], var['type']['name']) for var in indep_vars]
    pfa = sklearn_to_pfa(estimator, types, featurizer.generate_pretty_pfa())

    # Add serialized model as metadata
    pfa['metadata'] = {'centroids': json.dumps(np.array(remote_centroids).tolist())}

    # Save or update job_result
    logging.info('Saving PFA to job_results table')
    pfa = json.dumps(pfa)
    io_helper.save_results(pfa, '', shapes.Shapes.PFA)
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


def _create_featurizer(indep_vars):
    transforms = []
    for var in indep_vars:
        if var['type']['name'] in ('integer', 'real'):
            transforms.append(Standardize(var['name'], var['mean'], var['std']))
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
        intermediate_kmeans()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_kmeans(args.job_ids)
