#!/usr/bin/env python3
# Copyright (C) 2017  LREN CHUV for Human Brain Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from mip_helper import io_helper, shapes, utils, errors

import argparse
import logging
from pandas.io import json
import plotly.graph_objs as go
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)


@utils.catch_user_error
def compute():
    """Perform both intermediate step and aggregation at once."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()

    result = _compute_intermediate_result(inputs)
    corr, columns = _aggregate_results([result])
    _save_corr_heatmap(corr, columns)


@utils.catch_user_error
def intermediate_stats():
    """Calculate X*X^T, means and count for single node that will be later used to construct covariance matrix."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()

    result = _compute_intermediate_result(inputs)
    io_helper.save_results(json.dumps(result), '', shapes.Shapes.JSON)
    logging.info("DONE")


def _compute_intermediate_result(inputs):
    indep_vars = inputs["data"]["independent"]

    # it works with independent variables only
    if inputs["data"]["dependent"]:
        logging.warning('Correlation heatmap does not use dependent variable.')

    # Check that all independent variables are numeric
    for var in indep_vars:
        if utils.is_nominal(var):
            raise errors.UserError('Independent variables needs to be numeric ({} is {})'.format(var['name'], var['type']['name']))

    # Load data into a Pandas dataframe
    logging.info("Loading data...")
    X = utils.fetch_dataframe(variables=indep_vars)

    logging.info('Dropping NULL values')
    X = utils.remove_nulls(X, errors='ignore')

    # Generate results
    logging.info("Generating results...")
    if len(X):
        result = {
            'columns': list(X.columns),
            'means': X.mean().values,
            'X^T * X': X.T.dot(X.values).values,
            'count': len(X),
        }
    else:
        logging.warning('All values are NAN, returning zero values')
        k = X.shape[1]
        result = {
            'columns': list(X.columns),
            'means': np.zeros(k),
            'X^T * X': np.zeros((k, k)),
            'count': 0,
        }
    return result


@utils.catch_user_error
def aggregate_stats(job_ids):
    """Get all partial statistics from all nodes and aggregate them.
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    results = [json.loads(io_helper.get_results(str(job_id)).data) for job_id in job_ids]

    corr, columns = _aggregate_results(results)

    _save_corr_heatmap(corr, columns)


def _aggregate_results(results):
    logging.info("Aggregating results...")
    XXT = 0
    n = 0
    sumx = 0
    columns = None
    for result in results:
        # make sure columns are consistent
        columns = columns or result['columns']
        assert columns == result['columns']

        XXT += np.array(result['X^T * X'])
        n += np.array(result['count'])
        sumx += np.array(result['means']) * result['count']

    mu = sumx / n
    cov = (XXT - n * np.outer(mu, mu)) / (n - 1)

    # create correlation matrix
    sigma = np.sqrt(np.diag(cov))
    corr = np.diag(1 / sigma) @ cov @ np.diag(1 / sigma)
    return corr, columns


def _save_corr_heatmap(corr, columns):
    """Generate heatmap from correlation matrix and return it in plotly format"""
    trace = go.Heatmap(z=corr,
                       x=columns,
                       y=columns)
    data = [trace]

    logging.info("Results:\n{}".format(data))
    io_helper.save_results(json.dumps(data), '', shapes.Shapes.PLOTLY)
    logging.info("DONE")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('compute', choices=['compute'])
    parser.add_argument('--mode', choices=['single', 'intermediate', 'aggregate'], default='single')
    # QUESTION: (job_id, node) is a primary key of `job_result` table. Does it mean I'll need node ids as well in order
    # to query unique job?
    parser.add_argument('--job-ids', type=str, nargs="*", default=[])

    args = parser.parse_args()

    # > compute
    if args.mode == 'single':
        compute()
    # > compute --mode intermediate
    elif args.mode == 'intermediate':
        intermediate_stats()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_stats(args.job_ids)
