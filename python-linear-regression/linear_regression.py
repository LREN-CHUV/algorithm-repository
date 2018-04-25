#!/usr/bin/env python3

from mip_helper import io_helper, utils, errors, shapes

import logging
from pandas.io import json
import numpy as np
from scipy import stats
import argparse
import pandas as pd
from statsmodels.api import OLS

from sklearn.linear_model import SGDRegressor
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa
from sklearn_to_pfa.featurizer import Featurizer, OneHotEncoding, Transform


DEFAULT_DOCKER_IMAGE = "python-linear-regression"

# Configure logging
logging.basicConfig(level=logging.INFO)


# TODO: replace by from sklearn_to_pfa.featurizer import DummyTransform when it gets
# updated
class DummyTransform(Transform):

    def __init__(self, col):
        self.col = col

    @property
    def columns(self):
        return [self.col]

    def transform(self, X):
        return X[[self.col]]

    def pfa(self):
        return 'u.arr(cast.double(input.{col}))'.format(
            col=self.col
        )


@utils.catch_user_error
def main():
    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    # Check dependent variable type (should be continuous)
    if utils.is_nominal(dep_var):
        raise errors.UserError('Dependent variable should be continuous!')

    if not indep_vars:
        raise errors.UserError('No covariables selected.')

    data = io_helper.fetch_dataframe(variables=[dep_var] + indep_vars)
    data = utils.remove_nulls(data, errors='ignore')
    y = data.pop(dep_var['name'])

    featurizer = _create_featurizer(indep_vars)
    X = pd.DataFrame(featurizer.transform(data), columns=featurizer.columns)

    if X.empty:
        logging.warning('All values are NAN, returning zero values')
        result = {}
        pfa = None

    else:
        # Add intercept
        X.insert(loc=0, column='intercept', value=1.)

        # Remove linearly dependent columns
        X = X.iloc[:, _independent_columns(X)]

        # Fit regresssion
        lm = OLS(y, X)
        flm = lm.fit()
        logging.info(flm.summary())
        result = format_output(flm)

        # Generate PFA for predictions
        pfa = _generate_pfa(result, indep_vars, featurizer)

    # Store results
    io_helper.save_results(json.dumps(result), 'application/json')


def _independent_columns(X):
    """Find linearly independent columns."""
    indep = [False] * X.shape[1]
    for k in range(X.shape[1]):
        indep[k] = True
        if np.linalg.matrix_rank(X.iloc[:, indep]) < sum(indep):
            indep[k] = False
    return indep


def _generate_pfa(result, indep_vars, featurizer):
    # Create mock SGDRegressor for sklearn_to_pfa
    estimator = SGDRegressor()
    estimator.intercept_ = [result['intercept']]
    # NOTE: linearly dependent columns will be assigned 0
    estimator.coef_ = [result.get(c, {'coef': 0.})['coef'] for c in featurizer.columns if c != 'intercept']

    # Create PFA from coefficients
    types = [(var['name'], var['type']['name']) for var in indep_vars]
    return sklearn_to_pfa(estimator, types, featurizer.generate_pretty_pfa())


def _create_featurizer(indep_vars):
    transforms = []
    for var in indep_vars:
        if utils.is_nominal(var):
            transforms.append(OneHotEncoding(var['name'], var['type']['enumeration']))
        else:
            transforms.append(DummyTransform(var['name']))
    return Featurizer(transforms)


@utils.catch_user_error
def intermediate():
    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    data = io_helper.fetch_dataframe(variables=[dep_var] + indep_vars)
    data = utils.remove_nulls(data, errors='ignore')
    y = data.pop(dep_var['name'])

    featurizer = _create_featurizer(indep_vars)
    X = pd.DataFrame(featurizer.transform(data), columns=featurizer.columns, index=data.index)

    if not indep_vars:
        raise errors.UserError('No covariables selected.')

    # Check dependent variable type (should be continuous)
    if utils.is_nominal(dep_var):
        raise errors.UserError('Dependent variable should be continuous!')

    if data.empty:
        logging.warning('All values are NAN, returning zero values')
        result = {
            'summary': {},
            'columns': [],
            'means': 0,
            'X^T * X': 0,
            'count': 0,
            'scale': 0,
        }

    else:
        # Compute linear-regression
        X.insert(loc=0, column='intercept', value=1.)
        lm = OLS(y, X)
        flm = lm.fit()
        logging.info(flm.summary())
        output = format_output(flm)

        result = {
            'summary': output,
            'columns': list(X.columns),
            'means': X.mean().values,
            'X^T * X': X.T.values.dot(X.values),
            'count': len(X),
            'scale': flm.scale,
        }

    # Store results
    io_helper.save_results(json.dumps(result), 'application/json')


def format_output(flm):
    statsmodels_dict = {
        "coef": dict(flm.params),
        "std_err": dict(flm.bse),
        "t_values": dict(flm.tvalues),
        "p_values": dict(flm.pvalues),
    }
    ret = pd.DataFrame.from_dict(statsmodels_dict).transpose().fillna("NaN").to_dict()
    return ret


@utils.catch_user_error
def aggregate(job_ids):
    """Get partial regression coefficients together with covaraince matrix from all nodes and combine them into
    single estimate.
    :input job_ids: list of job_ids with intermediate results
    """
    # Read inputs
    inputs = io_helper.fetch_data()
    indep_vars = inputs["data"]["independent"]

    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    results = _load_intermediate_data(job_ids)

    # Pool results
    result = _combine_estimates(results)

    # Generate PFA from coefficients
    featurizer = _create_featurizer(indep_vars)
    pfa = _generate_pfa(result, indep_vars, featurizer)

    # Save job_result
    logging.info('Saving PFA to job_results table...')
    io_helper.save_results(json.dumps(result), shapes.Shapes.PFA)


def _combine_estimates(results):
    """Combine partial estimates of linear regression coefficients from nodes into a single estimate.
    Inspired by https://github.com/LREN-CHUV/hbplregress/blob/master/R/LRegress_group.R

    The pooling is based on partioning normal equations (Xt @ X) @ beta = Xt @ y
    """
    Xty = 0
    XtX = 0
    mu_sum = 0
    n = 0
    scale_sum = 0
    for res in results:
        # skip empty nodes
        if not res['summary']:
            continue

        beta_k = pd.Series({key: res['summary'][key].get('coef', 0) for key in res['summary']})
        XtX_k = pd.DataFrame(res['X^T * X'], index=res['columns'], columns=res['columns'])

        Xty += XtX_k.dot(beta_k)
        XtX += XtX_k
        mu_sum += pd.Series(res['means'], index=res['columns']) * res['count']
        n += res['count']
        scale_sum += res['scale'] * (res['count'] - len(beta_k))

    dof = n - len(XtX)
    mu = mu_sum / n
    scale = scale_sum / dof

    # remove linearly dependent columns
    cols = XtX.columns[_independent_columns(XtX)]

    # make sure columns match
    Xty = Xty.loc[cols]
    mu = mu.loc[cols]
    XtX = XtX.loc[cols, cols]

    # coefficients
    XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv.dot(Xty)

    # p-val and t-stat
    std_err = np.sqrt(scale * np.diag(XtX_inv))
    t_values = beta / std_err
    p_values = 2 * np.minimum(1 - stats.t.cdf(t_values, dof), stats.t.cdf(t_values, dof))

    return {
        cols[k]: {
            "coef": beta[k],
            "std_err": std_err[k],
            "t_values": t_values[k],
            "p_values": p_values[k],
        }
        for k in range(len(cols))
    }


def _load_intermediate_data(job_ids):
    data = []
    for job_id in job_ids:
        job_result = io_helper.get_results(job_id)

        # log errors (e.g. about missing data), but do not reraise them
        if job_result.error:
            logging.warning(job_result.error)
        else:
            results = json.loads(job_result.data)
            data.append(results)

    if not data:
        raise errors.UserError('All jobs {} returned an error.'.format(job_ids))

    return data


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
        main()
    # > compute --mode intermediate
    if args.mode == 'intermediate':
        intermediate()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate(args.job_ids)
