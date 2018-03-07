#!/usr/bin/env python3

from mip_helper import io_helper, shapes

import argparse
import itertools
import logging
import json
import copy
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)

# TODO: use something more fancy like schematics instead of dict?
OUTPUT_SCHEMA_INTERMEDIATE = {
    'schema': {
        'field': [
            {'name': 'group', 'type': 'list'},
            {'name': 'index', 'type': 'string'},
            {'name': 'count', 'type': 'int'},
            {'name': 'unique', 'type': 'int'},
            {'name': 'top', 'type': 'string'},
            {'name': 'frequency', 'type': 'object'},
            {'name': 'mean', 'type': 'number'},
            {'name': 'std', 'type': 'number'},
            {'name': 'EX^2', 'type': 'number'},
            {'name': 'min', 'type': 'number'},
            {'name': 'max', 'type': 'number'},
            {'name': '25%', 'type': 'number'},
            {'name': '50%', 'type': 'number'},
            {'name': '75%', 'type': 'number'},
        ]
    },
    'data': []
}


# TODO: for distributed case calculate percentiles using Q-Digest or T-Digest algorithm
OUTPUT_SCHEMA_AGGREGATE = {
    'schema': {
        'field': [
            {'name': 'group', 'type': 'list'},
            {'name': 'index', 'type': 'string'},
            {'name': 'count', 'type': 'int'},
            {'name': 'frequency', 'type': 'object'},
            {'name': 'mean', 'type': 'number'},
            {'name': 'std', 'type': 'number'},
            {'name': 'min', 'type': 'number'},
            {'name': 'max', 'type': 'number'}
        ]
    },
    'data': []
}


def intermediate_stats():
    """Calculate summary statistics for single node."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    # Check that dependent variable is numeric
    assert ~is_nominal(dep_var['type']['name']), 'Dependent variable needs to be numeric'

    # Load data into a Pandas dataframe
    logging.info("Loading data...")
    df = get_X(dep_var, indep_vars)

    # Generate results
    logging.info("Generating results...")
    results = copy.deepcopy(OUTPUT_SCHEMA_INTERMEDIATE)
    nominal_cols = df.dtypes == 'category'

    # grouped statistics
    if nominal_cols.any():
        for group_name, group in df.groupby(list(df.columns[nominal_cols])):
            # if there's only one nominal column
            if not isinstance(group_name, tuple):
                group_name = (group_name,)

            results['data'] += _calc_stats(group, group_name)

    # overall statistics
    results['data'] += _calc_stats(df, ('all',))

    logging.info("Results:\n{}".format(results))
    io_helper.save_results(pd.json.dumps(results), '', shapes.Shapes.JSON)
    logging.info("DONE")


def _calc_stats(group, group_name):
    results = []
    for name, x in group.items():
        result = {
            'index': name,
            'group': group_name,
        }

        # add all stats from pandas
        result.update(x.describe())

        if x.dtype.name == 'category':
            result['frequency'] = dict(x.value_counts())
        else:
            # add EX^2 for calculation of std in distributed scenario
            result['EX^2'] = np.mean(x**2)

        result['count'] = len(x)
        results.append(result)

    return results


def aggregate_stats(job_ids):
    """Get all partial statistics from all nodes and aggregate them.
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    data = itertools.chain(*[json.loads(io_helper.get_results(job_id)['data']) for job_id in job_ids])
    df = pd.DataFrame(list(data))
    df['group'] = df['group'].map(tuple)

    # Aggregate summary statistics
    logging.info("Aggregating results...")
    results = copy.deepcopy(OUTPUT_SCHEMA_AGGREGATE)
    for (group_name, index), gf in df.groupby(['group', 'index']):
        results['data'].append(_agg_stats(gf, group_name, index))

    # aggregate all intermediate results into special group `all`
    for index, gf in df.groupby('index'):
        results['data'].append(_agg_stats(gf, ('all',), index))

    logging.info("Results:\n{}".format(results))
    io_helper.save_results(pd.json.dumps(results), '', shapes.Shapes.JSON)
    logging.info("DONE")


def _agg_stats(gf, group_name, index):
    mean = (gf['mean'] * gf['count']).sum() / gf['count'].sum()
    return {
        'index': index,
        'group': group_name,
        'mean': mean,
        # std = EX^2 - (EX)^2
        'std': np.sqrt((gf['EX^2'] * gf['count']).sum() / gf['count'].sum() - mean**2),
        'min': gf['min'].min(),
        'max': gf['max'].max(),
        'count': gf['count'].sum(),
    }


def is_nominal(var_type):
    return var_type in ['binominal', 'polynominal']


def update_schema_field(fields, name, value):
    for field in fields:
        if field['name'] == name:
            field['type'] = value


def get_X(dep_var, indep_vars):
    """Create dataframe from input data.
    :param dep_var:
    :param indep_vars:
    :return: dataframe with data from all variables

    TODO: move this function to `io_helper` and reuse it in python-sgd-regressor
    """
    df = {}
    for var in [dep_var] + indep_vars:
        # categorical variable - we need to add all categories to make one-hot encoding work right
        if is_nominal(var['type']['name']):
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

    # > compute intermediate
    if args.mode == 'intermediate':
        intermediate_stats()
    # > compute aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_stats(args.job_ids)
