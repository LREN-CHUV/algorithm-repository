#!/usr/bin/env python3

from mip_helper import io_helper, utils, errors, shapes

import logging
from pandas.io import json
import numpy as np
from scipy import stats
import argparse
import pandas as pd
from statsmodels.api import OLS, Logit
from statsmodels.tools.sm_exceptions import PerfectSeparationError

from sklearn.linear_model import SGDRegressor, SGDClassifier
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa
from sklearn_to_pfa.featurizer import Featurizer, OneHotEncoding, DummyTransform

# BUG: workaround from https://github.com/statsmodels/statsmodels/issues/3931 before new version of statsmodels get
# released
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)

DEFAULT_DOCKER_IMAGE = "python-linear-regression"

# Configure logging
logging.basicConfig(level=logging.INFO)


@utils.catch_user_error
def main():
    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    if not indep_vars:
        raise errors.UserError('No covariables selected.')

    if utils.is_nominal(dep_var):
        job_type = 'classification'
    else:
        job_type = 'regression'

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
        if job_type == 'regression':
            result, metadata = _fit_regression(X, y)

            # Generate PFA for predictions
            pfa = _generate_pfa_regressor(result, indep_vars, featurizer)

        elif job_type == 'classification':
            # Run one-vs-others for each class
            result = {}
            metadata = {}
            for cat in y.cat.categories:
                r, m = _fit_logit(X, y == cat)
                result[cat] = r
                metadata[cat] = m

            if all(result[cat]['intercept']['coef'] is None for cat in y.cat.categories):
                raise errors.UserError('Not enough data to apply logistic regression.')

            # Generate PFA for predictions
            pfa = _generate_pfa_classifier(result, indep_vars, featurizer, y.cat.categories)

        # Add metadata from model
        pfa['metadata'] = metadata

    logging.info('Saving to job_results table...')
    _store_multiple_results(result, pfa)


def _store_multiple_results(result, pfa):
    io_helper.save_results(
        json.dumps(result), shapes.Shapes.JSON, result_name='coefficients', result_title='Linear regression summary'
    )
    io_helper.save_results(
        json.dumps(pfa), shapes.Shapes.PFA, result_name='model', result_title='PFA'
    )
    io_helper.results_complete()


def _fit_regression(X, y):
    lm = OLS(y, X)
    flm = lm.fit()
    logging.info(flm.summary())
    metadata = {'summary': str(flm.summary()), 'summary2': str(flm.summary2())}
    return format_output(flm), metadata


def _fit_logit(X, y):
    metadata = {}
    lm = Logit(y, X)
    try:
        flm = lm.fit(method='bfgs')
        logging.info(flm.summary())
        output = format_output(flm)
        metadata = {'summary': str(flm.summary()), 'summary2': str(flm.summary2())}
    except (np.linalg.linalg.LinAlgError, PerfectSeparationError, ValueError) as e:
        # Perfect separation or singular matrix - use NaN
        logging.warning(e)
        output = {col: {
            "coef": None,
            "std_err": None,
            "t_values": None,
            "p_values": None,
        }
                  for col in X.columns}

    return output, metadata


def _independent_columns(X):
    """Find linearly independent columns."""
    indep = [False] * X.shape[1]
    for k in range(X.shape[1]):
        indep[k] = True
        if np.linalg.matrix_rank(X.iloc[:, indep]) < sum(indep):
            indep[k] = False
    return indep


def _generate_pfa_regressor(result, indep_vars, featurizer):
    # Create mock SGDRegressor for sklearn_to_pfa
    estimator = SGDRegressor()
    estimator.intercept_ = [result['intercept']]
    # NOTE: linearly dependent columns will be assigned 0
    estimator.coef_ = [result.get(c, {'coef': 0.})['coef'] for c in featurizer.columns if c != 'intercept']

    types = [(var['name'], var['type']['name']) for var in indep_vars]
    return sklearn_to_pfa(estimator, types, featurizer.generate_pretty_pfa())


def _generate_pfa_classifier(result, indep_vars, featurizer, classes):
    # Create mock SGDRegressor for sklearn_to_pfa
    estimator = SGDClassifier()
    estimator.classes_ = classes
    estimator.intercept_ = [result[cat]['intercept'] for cat in classes]
    # NOTE: linearly dependent columns will be assigned 0
    estimator.coef_ = [
        [result[cat].get(c, {'coef': 0.})['coef'] for c in featurizer.columns if c != 'intercept'] for cat in classes
    ]

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

    # Distributed linear regression only works for continuous variables
    if utils.is_nominal(dep_var):
        raise errors.UserError(
            'Dependent variable must be continuous in distributed mode. Use SGD Regression for '
            'nominal variables instead.'
        )

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
    io_helper.save_results(json.dumps(result), shapes.Shapes.JSON)


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
    pfa = _generate_pfa_regressor(result, indep_vars, featurizer)

    # Save job_result
    logging.info('Saving PFA to job_results table...')
    _store_multiple_results(result, pfa)


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
