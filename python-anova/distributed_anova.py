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

from mip_helper import io_helper, errors, utils, parameters
from mip_helper.shapes import Shapes
import anova

import logging
from pandas.io import json
import numpy as np
import pandas as pd
import patsy
import re
from scipy import stats
from collections import defaultdict


@utils.catch_user_error
def intermediate_models():
    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]
    design = parameters.get_parameter(anova.DESIGN_PARAM, str, anova.DEFAULT_DESIGN)

    # Check dependent variable type (should be continuous)
    if utils.is_nominal(dep_var):
        raise errors.UserError('Dependent variable should be continuous!')

    # Create dataframe from data
    X, y = _get_Xy(dep_var, indep_vars, design)

    # Construct matrices for normal equations
    if not X.empty:
        result = {
            'XtX': X.T.values.dot(X.values),
            'Xty': X.T.values.dot(y.values),
            'y_mean': y.mean(),
            'columns': list(X.columns),
            'count': len(X),
        }
    else:
        logging.warning('All values are NAN, returning zero values')
        result = {
            'XtX': 0,
            'Xty': 0,
            'y_mean': 0,
            'columns': list(X.columns),
            'count': 0,
        }

    # Store results
    io_helper.save_results(json.dumps(result), 'application/json')


@utils.catch_user_error
def aggregate_models(job_ids):
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    results = io_helper.load_intermediate_json_results(map(str, job_ids))

    # Aggregate matrices for normal equations
    XtX, Xty, y_mean, n = _combine_estimates(results)

    # Create sub_models
    columns = results[0]['columns']
    sub_models = []
    for k in range(1, len(columns) + 1):
        beta = np.linalg.pinv(XtX[:k, :k]) @ Xty[:k]
        sub_models.append({'beta': beta, 'columns': columns[:k]})

    result = {
        'y_mean': y_mean,
        'dof': n - sum(abs(sub_models[-1]['beta']) > 1e-10),
        'sub_models': sub_models,
    }

    # Store models
    io_helper.save_results(json.dumps(result), 'application/json')


@utils.catch_user_error
def intermediate_anova(job_ids):
    assert len(job_ids) == 1, 'Input should be only a single job ID'

    # Read nested models
    logging.info("Fetching intermediate data...")
    result = io_helper.load_intermediate_json_results(str(job_ids[0]))[0]
    y_mean = result['y_mean']
    dof = result['dof']
    sub_models = result['sub_models']

    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]
    design = parameters.get_parameter(anova.DESIGN_PARAM, str, anova.DEFAULT_DESIGN)

    # Check dependent variable type (should be continuous)
    if dep_var["type"]["name"] not in ["integer", "real"]:
        raise errors.UserError('Dependent variable should be continuous!')

    # Create dataframe from data
    X, y = _get_Xy(dep_var, indep_vars, design)

    # Make prediction on data
    ss_list = []
    for lm in sub_models:
        y_hat = X[lm['columns']].dot(lm['beta'])

        # Calculate decomposition of sum of squares
        ss = {
            'columns': lm['columns'],
            'dof': dof,
            **_sum_of_squares(y_hat, y, y_mean)
        }
        ss_list.append(ss)

    # Store squares
    io_helper.save_results(json.dumps(ss_list), 'application/json')


@utils.catch_user_error
def aggregate_anova(job_ids):
    # Load squares decomposition
    logging.info("Fetching intermediate data...")
    results = io_helper.load_intermediate_json_results(map(str, job_ids))

    # Construct ANOVA table
    sub_ss = _combine_squares(results)
    anova_tab = anova_models(sub_ss)

    # Store ANOVA table
    anova_results = anova.format_output(anova_tab.to_dict())

    # Store results
    io_helper.save_results(anova_results, Shapes.JSON)


def _combine_squares(local_ss_list):
    """Pool sum of squares from local nodes."""
    full_model = local_ss_list[0][-1]
    n_models = len(full_model['columns'])
    sub_ss = []
    for k in range(n_models):
        agg_ss = defaultdict(float)
        for ss_list in local_ss_list:
            agg_ss['rss'] += ss_list[k]['rss']
            agg_ss['tss'] += ss_list[k]['tss']
            agg_ss['ess'] += ss_list[k]['ess']
        agg_ss['columns'] = ss_list[k]['columns']
        agg_ss['dof'] = ss_list[k]['dof']
        sub_ss.append(agg_ss)
    return sub_ss


def _get_Xy(dep_var, indep_vars, design):
    data = io_helper.fetch_dataframe(variables=[dep_var] + indep_vars)

    # Get formula for model
    formula = anova.generate_formula(dep_var, indep_vars, design)

    # Create design matrix
    y, X = patsy.dmatrices(formula, data=data, return_type='dataframe')

    return X, y.iloc[:, 0]


def _combine_estimates(results):
    """Pool normal equations from multiple nodes. The pooling is based on partioning normal equations
    (Xt @ X) @ beta = Xt @ y.
    """
    # make sure all have the same columns
    if results:
        assert all(r['columns'] == results[0]['columns'] for r in results)

    Xty = 0
    XtX = 0
    y_sum = 0
    n = 0
    for res in results:
        XtX += np.array(res['XtX'])
        Xty += np.array(res['Xty'])
        y_sum += res['y_mean'] * res['count']
        n += res['count']

    y_mean = y_sum / n

    return XtX, Xty, y_mean, n


def _sum_of_squares(y_hat, y, y_mean):
    """Partition of sum of squares https://en.wikipedia.org/wiki/Partition_of_sums_of_squares."""
    return {
        # residual sum of squares (rss)
        'rss': sum((y - y_hat)**2),
        # total sum of squares (rss)
        'tss': sum((y - y_mean)**2),
        # explained sum of squares (ess)
        'ess': sum((y_hat - y_mean)**2),
    }


def anova_models(sub_ss):
    """Create ANOVA table from multiple nested linear models (their sum of square to be more precise).
    :param sub_ss: sum of squares for sub_models, list of dicts with {'n': ..., 'columns': ..., 'rss': ..., 'ess': ..., 'tss': ...}
    :return: ANOVA table same as output of statsmodels.stats.anova.anova_lm
    """
    # make sure all models are nested
    for k in range(1, len(sub_ss)):
        assert set(sub_ss[k - 1]['columns']) < set(sub_ss[k]['columns'])

    dof_resid = sub_ss[-1]['dof']
    full_model_columns = sub_ss[-1]['columns']
    rss = sub_ss[-1]['rss']

    # aggregate explained sum of squares
    ess = pd.Series([lm['ess'] for lm in sub_ss], index=full_model_columns)

    # get differences in sum of squares
    ess = ess.diff().drop('Intercept')

    # group together same categories, e.g. C(a)[x] and C(a)[y]
    category_name = ess.index.map(lambda x: re.sub(r'\)\[.+?\]', ')', x))
    ess = ess.groupby(category_name).sum()

    # degrees of freedom
    dof = category_name.value_counts()

    # ANOVA table`
    tab = pd.DataFrame({
        'df': dof,
        'sum_sq': ess,
    }).reindex(category_name.unique())

    # add Residual
    resid = pd.Series(
        {
            'df': dof_resid,
            'sum_sq': rss,
        }, name='Residual'
    )
    tab = tab.append(resid)

    # average square error
    tab['mean_sq'] = tab['sum_sq'] / tab['df']

    # calculate F-stat and p-values
    model_df_resid = tab.loc['Residual', 'df']

    tab['F'] = tab['mean_sq'] / tab.loc['Residual', 'mean_sq']
    tab['PR(>F)'] = stats.f.sf(tab["F"], tab["df"], model_df_resid)
    tab.loc['Residual', ['F', 'PR(>F)']] = np.nan

    return tab
