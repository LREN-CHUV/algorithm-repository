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

from mip_helper import io_helper, shapes, utils, errors, parameters

import argparse
import logging
import itertools
from pandas.io import json
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
import plotly.figure_factory as ff
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)


@utils.catch_user_error
def compute(graph_type=None):
    """Perform both intermediate step and aggregation at once."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    result = _compute_intermediate_result(inputs)
    corr, columns, crosstab = _aggregate_results([result])

    graph_type = graph_type or parameters.get_parameter('graph', str, 'correlation_heatmap')

    if graph_type == 'correlation_heatmap':
        fig = _fig_corr_heatmap(corr, columns, crosstab)
    elif graph_type == 'pca':
        X = io_helper.fetch_dataframe([dep_var] + indep_vars)
        fig = _fig_pca(corr, columns, X)
    else:
        raise errors.UserError('MODEL_PARAM_graph only supports values `correlation_heatmap` and `pca`')

    logging.info("Results:\n{}".format(fig))
    io_helper.save_results(json.dumps(fig), shapes.Shapes.PLOTLY)
    logging.info("DONE")


@utils.catch_user_error
def intermediate_stats():
    """Calculate X*X^T, means and count for single node that will be later used to construct covariance matrix."""
    # Read inputs
    logging.info("Fetching data...")
    inputs = io_helper.fetch_data()

    result = _compute_intermediate_result(inputs)
    io_helper.save_results(json.dumps(result), shapes.Shapes.JSON)
    logging.info("DONE")


def _compute_intermediate_result(inputs):
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    nominal_vars = []
    numeric_vars = []
    for var in [dep_var] + indep_vars:
        if utils.is_nominal(var):
            nominal_vars.append(var['name'])
        else:
            numeric_vars.append(var['name'])

    # Load data into a Pandas dataframe
    logging.info("Loading data...")
    X = io_helper.fetch_dataframe(variables=[dep_var] + indep_vars)

    logging.info('Dropping NULL values')
    X = utils.remove_nulls(X, errors='ignore')

    # Generate results
    logging.info("Generating results...")
    result = {
        'columns': numeric_vars,
        'nominal_columns': nominal_vars,
    }
    if len(X):
        result.update({
            'means': X[numeric_vars].mean().values,
            'X^T * X': X[numeric_vars].T.dot(X[numeric_vars].values).values,
            'count': len(X),
        })
        if nominal_vars:
            result['crosstab'] = X[nominal_vars].groupby(nominal_vars).size()\
                                                .reset_index()\
                                                .rename(columns={0: 'count'})\
                                                .to_dict(orient='records')
        else:
            result['crosstab'] = []
    else:
        logging.warning('All values are NAN, returning zero values')
        k = len(result['columns'])
        result.update({
            'means': np.zeros(k),
            'X^T * X': np.zeros((k, k)),
            'count': 0,
            'crosstab': [],
        })
    return result


@utils.catch_user_error
def aggregate_stats(job_ids, graph_type=None):
    """Get all partial statistics from all nodes and aggregate them.
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    results = io_helper.load_intermediate_json_results(map(str, job_ids))

    corr, columns, crosstab = _aggregate_results(results)

    graph_type = graph_type or parameters.get_parameter('graph', str, 'correlation_heatmap')

    if graph_type == 'correlation_heatmap':
        fig = _fig_corr_heatmap(corr, columns, crosstab)
    elif graph_type == 'pca':
        # save PCA graphs, but leave out the one with PCA scores
        logging.warning('Sample scores graph is not yet implemented for distributed PCA.')
        fig = _fig_pca(corr, columns, X=None)
    else:
        raise errors.UserError('MODEL_PARAM_graph only supports values `correlation_heatmap` and `pca`')

    logging.info("Results:\n{}".format(fig))
    io_helper.save_results(json.dumps(fig), shapes.Shapes.PLOTLY)
    logging.info("DONE")


def _aggregate_results(results):
    logging.info("Aggregating results...")
    XXT = 0
    n = 0
    sumx = 0
    columns = None
    nominal_columns = None
    crosstab = []
    for result in results:
        # make sure columns are consistent
        columns = columns or result['columns']
        assert columns == result['columns']

        nominal_columns = nominal_columns or result['nominal_columns']
        assert nominal_columns == result['nominal_columns']

        XXT += np.array(result['X^T * X'])
        n += np.array(result['count'])
        sumx += np.array(result['means']) * result['count']

        crosstab += result['crosstab']

    mu = sumx / n
    cov = (XXT - n * np.outer(mu, mu)) / (n - 1)

    # create correlation matrix
    sigma = np.sqrt(np.diag(cov))
    corr = np.diag(1 / sigma) @ cov @ np.diag(1 / sigma)
    return corr, columns, crosstab


def _fig_corr_heatmap(corr, columns, crosstab):
    """Generate heatmap from correlation matrix and return it in plotly format"""
    # create correlation heatmap figure
    fig = _corr_heatmap(corr, columns)

    crosstab = pd.DataFrame(crosstab)

    # add crosstabs to figure for all pairs of nominal variables
    if not crosstab.empty:
        k = 2
        for a, b in itertools.combinations(crosstab.columns.drop('count'), 2):
            ct = _make_crosstab(crosstab, a, b, xaxis=f'x{k}', yaxis=f'y{k}')
            fig = _update_fig_with_crosstab(fig, ct, k, a, b)
            k += 1

    return fig


def _update_fig_with_crosstab(fig, ct, k, col_a, col_b):
    for anot in ct.layout.annotations:
        anot.update(xref=f'x{k}', yref=f'y{k}')

    fig.data[0].update(colorbar={'len': 1 / k, 'y': 1 - 0.5 / k})

    fig['data'].extend(ct.data)
    fig.layout.annotations.extend(ct.layout.annotations)
    fig.layout[f'xaxis{k}'] = ct.layout.xaxis
    fig.layout[f'yaxis{k}'] = ct.layout.yaxis

    # Edit layout for subplots
    rr = np.linspace(0, 1, k + 1)
    for i in range(k):
        ax = 'yaxis' if k - i == 1 else 'yaxis{}'.format(k - i)
        lower = rr[i] + 0.1 / k if rr[i] != 0 else 0
        upper = rr[i + 1] - 0.05 / k if rr[i + 1] != 1 else 1
        fig.layout[ax].update({'domain': [lower, upper]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis.update({'anchor': 'x1'})
    fig.layout.xaxis.update({'anchor': 'y1'})
    fig.layout[f'yaxis{k}'].update({'anchor': f'x{k}'})
    fig.layout[f'xaxis{k}'].update({'anchor': f'y{k}'})
    fig.layout[f'yaxis{k}'].update({'title': col_a, 'anchor': f'x{k}'})
    ax = 'xaxis' if k - 1 == 1 else f'xaxis{k-1}'

    fig.layout[ax].update({'title': col_b})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t': 75, 'l': 120})
    fig.layout.update({'height': k * 500, 'width': 800})

    return fig


def _make_crosstab(df, col_a, col_b, **kwargs):
    ct = df.groupby([col_a, col_b])['count'].sum().unstack().fillna(0).astype(int)
    ct['All'] = ct.sum(axis=1)
    s = ct.sum(axis=0)
    s.name = 'All'
    ct = ct.append(s)

    ct = ct.astype(str)
    ct.iloc[-1] = ['<b>{}</b>'.format(x) for x in ct.iloc[-1]]
    ct.iloc[:, -1] = ['<b>{}</b>'.format(x) for x in ct.iloc[:, -1]]

    return ff.create_table(ct, index=True, **kwargs)


def _corr_heatmap(corr, columns):
    # revert y-axis so that diagonal goes from top left to bottom right
    trace = go.Heatmap(
        z=corr[::-1, :],
        x=columns,
        y=columns[::-1],
        zmin=-1,
        zmax=1,
        xaxis='x1',
        yaxis='y1',
    )
    fig = go.Figure(data=[trace])
    fig.layout.update({'title': 'Correlation heatmap'})
    return fig


def _pca(corr, X=None):
    # calculate eigenvectors and eigenvalues
    eig_vals, eig_vecs = np.linalg.eig(corr)

    # order eigenvectors and eigenvalues by eigenvectors
    eig_pairs = [(eig_vals[i], eig_vecs[:, i]) for i in range(len(eig_vals))]
    eig_pairs = sorted(eig_pairs, key=lambda val_pair: -abs(val_pair[0]))
    eig_vals, eig_vecs = zip(*eig_pairs)
    eig_vecs = np.vstack(eig_vecs).T

    logging.info('Eigenvectors:\n{}'.format(eig_vecs))
    logging.info('\nEigenvalues:\n{}'.format(eig_vals))

    # projection matrix with 2 components
    W = eig_vecs[:, :2]
    logging.info('\Projection matrix W:\n{}'.format(W))

    # convert original data to scores
    # NOTE: since we are working with correlation matrix, original data must be standardized first!
    if X is not None:
        X_std = (X - X.mean()) / X.std()
        Y = X_std.dot(W)
    else:
        Y = None

    return eig_vals, eig_vecs, Y


def _figure(eig_vals, eig_vecs, Y, columns):
    show_scores = Y is not None

    titles = ['Scree plot', 'Eigen-components', 'Variables scores']
    titles.append('Samples scores' if show_scores else 'Samples scores <br>(not available in distributed mode)')

    # plotting
    fig = tools.make_subplots(
        rows=2, cols=2, subplot_titles=titles
    )

    for d in _screeplot(eig_vals):
        fig.append_trace(d, 1, 1)

    for d in _eigencomponents(eig_vecs, columns):
        fig.append_trace(d, 1, 2)

    for d in _biplot_variables(eig_vecs, columns):
        fig.append_trace(d, 2, 1)

    # only show sample scores in single node mode
    if show_scores:
        for d in _biplot_samples(Y.values):
            fig.append_trace(d, 2, 2)

    var_exp = _explained_variance(eig_vals)

    fig['layout']['yaxis1'].update(title='Explained variance in percent')
    fig['layout']['xaxis3'].update(title='PC1 ({:.1%})'.format(var_exp[0]), range=[-1.05, 1.05])
    fig['layout']['yaxis3'].update(title='PC2 ({:.1%})'.format(var_exp[1]), range=[-1.05, 1.05])

    if show_scores:
        fig['layout']['xaxis4'].update(title='PC1 ({:.1%})'.format(var_exp[0]))
        fig['layout']['yaxis4'].update(title='PC2 ({:.1%})'.format(var_exp[1]))

    # unit-circle for biplot
    circle = {
        'type': 'circle',
        'xref': 'x3',
        'yref': 'y3',
        'x0': -1,
        'y0': -1,
        'x1': 1,
        'y1': 1,
        'line': {
            'color': 'red',
        },
    }

    fig['layout'].update(height=800, width=800, title='Principal Component Analysis', shapes=[circle])

    return fig


def _fig_pca(corr, columns, X=None):
    """Generate PCA visualization in plotly format. Inspired by https://plot.ly/ipython-notebooks/principal-component-analysis/"""
    eig_vals, eig_vecs, Y = _pca(corr, X)
    fig = _figure(eig_vals, eig_vecs, Y, columns)
    return fig


def _screeplot(eig_vals, max_components=5):
    """Explained variance by principal components.
    See https://plot.ly/ipython-notebooks/principal-component-analysis/#2--selecting-principal-components
    """
    var_exp = _explained_variance(eig_vals) * 100
    cum_var_exp = np.cumsum(var_exp)

    x = ['PC {}'.format(i) for i in range(1, max_components + 1)]

    trace1 = go.Bar(
        x=x,
        y=var_exp,
        showlegend=False,
        name='explained variance',
    )

    trace2 = go.Scatter(
        x=x,
        y=cum_var_exp,
        showlegend=False,
        name='cumulative explained variance',
    )

    return go.Data([trace1, trace2])


def _biplot_samples(Y):
    traces = [
        go.Scatter(
            x=Y[:, 0],
            y=Y[:, 1],
            mode='markers',
            marker=go.Marker(size=12, line=go.Line(color='rgba(217, 217, 217, 0.14)', width=0.5), opacity=0.6),
            showlegend=False,
        )
    ]
    return go.Data(traces)


def _biplot_variables(eig_vecs, variable_names):
    traces = []

    for k in range(len(variable_names)):
        traces.append(
            go.Scatter(
                x=[0, eig_vecs[k, 0]],  # first component
                y=[0, eig_vecs[k, 1]],  # second component
                mode='lines+markers+text',
                marker={'color': 'black'},
                text=[None, variable_names[k]],
                # textposition='bottom',
                showlegend=False,
            )
        )
    return go.Data(traces)


def _eigencomponents(W, variable_names):
    # show first two principal components and all their loadings as a bar graph
    trace1 = go.Bar(
        x=variable_names,
        y=W[:, 0],
        showlegend=False,
        name='PC1',
    )
    trace2 = go.Bar(
        x=variable_names,
        y=W[:, 1],
        showlegend=False,
        name='PC2',
    )
    return go.Data([trace1, trace2])


def _explained_variance(eig_vals):
    return eig_vals / np.sum(eig_vals)


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
        intermediate_stats()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_stats(args.job_ids)
