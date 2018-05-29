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
from pandas.io import json
import argparse
import numpy as np

from mip_helper import io_helper, shapes, parameters, utils
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
DEFAULT_N_CLUSTERS = 8

# if `mean` and `std` are not available in metadata, normalize variables if DEFAULT_NORMALIZE is True, if False then
# keep them as they are
DEFAULT_NORMALIZE = True


@utils.catch_user_error
def compute():
    """Create PFA for kNN."""
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")

    inputs = io_helper.fetch_data()
    indep_vars = inputs["data"]["independent"]

    # Extract hyperparameters from ENV variables
    k = parameters.get_param('n_clusters', int, DEFAULT_N_CLUSTERS)

    # featurization
    featurizer = _create_featurizer(indep_vars)

    # convert variables into dataframe
    X = io_helper.fetch_dataframe(variables=indep_vars)
    X = utils.remove_nulls(X, errors='ignore')
    X = featurizer.transform(X)

    estimator = KMeans(n_clusters=k)
    estimator.fit(X)

    # Generate PFA for kmeans
    types = [(var['name'], var['type']['name']) for var in indep_vars]
    pfa = sklearn_to_pfa(estimator, types, featurizer.generate_pretty_pfa())

    # Add centroids as metadata
    pfa['metadata'] = {'centroids': json.dumps(estimator.cluster_centers_.tolist())}

    # Save or update job_result
    logging.info('Saving PFA to job_results table')
    io_helper.save_results(json.dumps(pfa), shapes.Shapes.PFA)
    logging.info("DONE")


@utils.catch_user_error
def intermediate_kmeans():
    """Calculate k-Means locally."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()
    indep_vars = inputs["data"]["independent"]

    # Extract hyperparameters from ENV variables
    k = parameters.get_param('n_clusters', int, DEFAULT_N_CLUSTERS)

    # Load data into a Pandas dataframe
    logging.info("Loading data...")
    X = io_helper.fetch_dataframe(variables=indep_vars)

    # Return variables info, but remove actual data points
    results = {'indep_vars': []}
    for var in indep_vars:
        if var['type']['name'] in ('integer', 'real'):
            new_var = {k: v for k, v in var.items() if k != 'series'}
            mean, std = _get_moments(var)
            new_var['mean'] = mean
            new_var['std'] = std
        else:
            new_var = var

        results['indep_vars'].append(new_var)

    # Drop NaN values
    X = utils.remove_nulls(X, errors='ignore')
    if len(X) == 0:
        logging.warning("All data are NULL, returning empty centroids.")
        results['centroids'] = []
        io_helper.save_results(json.dumps(results), shapes.Shapes.JSON)
        return

    # Generate results
    logging.info("Generating results...")

    # featurization
    featurizer = _create_featurizer(indep_vars)
    X = featurizer.transform(X)

    m, n = X.shape
    num_iter = 0
    not_converged = True

    # Run k-Means locally
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
    io_helper.save_results(json.dumps(results), shapes.Shapes.JSON)
    logging.info("DONE")


def aggregate_kmeans(job_ids):
    """Compute merging of clusters according to least merging error (e.g. smallest distance betweeen centroids)
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    data = [json.loads(io_helper.get_results(str(job_id)).data) for job_id in job_ids]

    local_centroids = [np.array(x['centroids']) for x in data if x['centroids']]
    logging.info('Local centroids:\n{}'.format(local_centroids))
    indep_vars = data[0]['indep_vars']

    # Aggregate clusters remotely
    remote_centroids = remote.aggregate_clusters(local_centroids)
    logging.info("Remote centroids:\n{}".format(remote_centroids))

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
    io_helper.save_results(pfa, shapes.Shapes.PFA)
    logging.info("DONE")


def _create_featurizer(indep_vars):
    transforms = []
    for var in indep_vars:
        if var['type']['name'] in ('integer', 'real'):
            mean, std = _get_moments(var)
            tf = Standardize(var['name'], mean, std)
            transforms.append(tf)
        elif var["type"]["name"] in ['polynominal', 'binominal']:
            transforms.append(OneHotEncoding(var['name'], var['type']['enumeration']))

    return Featurizer(transforms)


def _get_moments(var):
    # TODO: DRY with the same function in `sgd_regression.py`
    s = [x for x in var.get('series', []) if x is not None]

    if 'mean' in var:
        mean = var['mean']
    else:
        if DEFAULT_NORMALIZE and len(s):
            mean = np.mean(s)
        else:
            mean = 0.
        logging.warning('Mean not available for variable {}, using default value {}.'.format(var['name'], mean))

    if 'std' in var:
        std = var['std']
    else:
        if DEFAULT_NORMALIZE and len(s):
            std = np.std(s)
        else:
            std = 1.
        logging.warning('Standard deviation not available for variable {}, using default value {}'.format(var['name'], std))
    return mean, std


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('compute', choices=['compute'])
    parser.add_argument('--mode', choices=['single', 'intermediate', 'aggregate'], default='single')
    parser.add_argument('--job-ids', type=str, nargs="*", default=[])

    args = parser.parse_args()

    # > compute
    if args.mode == 'single':
        compute()
    # > compute --mode intermediate
    elif args.mode == 'intermediate':
        intermediate_kmeans()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_kmeans(args.job_ids)
