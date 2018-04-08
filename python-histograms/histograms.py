#!/usr/bin/env python3

from mip_helper import io_helper, shapes, errors, utils, parameters

import logging
from pandas.io import json
import math
import copy
import argparse
import itertools

from collections import OrderedDict
from numpy import arange
from numpy import histogram
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)

BINS_PARAM = "bins"
STRICT_PARAM = "strict"
DEFAULT_BINS = 20
DEFAULT_STRICT = False
# include `No data` column in histogram for null values
INCLUDE_NO_DATA = False


@utils.catch_user_error
def main():
    """Calculate histogram of dependent variable in a single-node mode and return output in highcharts JSON."""
    try:
        # Read inputs
        inputs = io_helper.fetch_data()
        try:
            dep_var = inputs["data"]["dependent"][0]
        except KeyError:
            logging.warning("Cannot find dependent variables data")
            dep_var = []
        try:
            indep_vars = inputs["data"]["independent"]
        except KeyError:
            logging.warning("Cannot find independent variables data")
            indep_vars = []
        nb_bins = parameters.get_param(BINS_PARAM, int, DEFAULT_BINS)

        # Compute histograms (JSON formatted for HighCharts)
        histograms_results = compute_histograms(dep_var, indep_vars, nb_bins)

        if not INCLUDE_NO_DATA:
            histograms_results = [_remove_no_data(hist) for hist in histograms_results]

        # Store results
        io_helper.save_results(json.dumps(histograms_results), '', shapes.Shapes.HIGHCHARTS)
    except errors.UserError as e:
        logging.error(e)
        strict = parameters.get_boolean_param(STRICT_PARAM, DEFAULT_STRICT)
        if strict:
            # Will be handled by catch_user_error
            raise e
        else:
            # Display something to the user and then exit
            histograms_results = error_histograms(dep_var, indep_vars)
            io_helper.save_results(histograms_results, '', 'application/highcharts+json')
            utils.exit_on_error()


@utils.catch_user_error
def aggregate_histograms(job_ids):
    """Get all histograms from all nodes and sum them together.
    :input job_ids: list of job_ids with intermediate results
    """
    # Read intermediate inputs from jobs
    logging.info("Fetching intermediate data...")
    data = _load_intermediate_data(job_ids)

    # group by label (e.g. `Histogram - agegroup`)
    results = []
    data = sorted(data, key=lambda d: d['label'])
    for key, hists in itertools.groupby(data, key=lambda d: d['label']):
        hists = list(hists)

        # add data from other histograms
        result = hists[0]
        for hist in hists[1:]:
            hist, result = _align_categories(hist, result)
            assert hist['xAxis']['categories'] == result['xAxis']['categories']

            # use pandas for easier manipulation
            series = {s['name']: np.array(s['data']) for s in result['series']}

            for s in hist['series']:
                if s['name'] not in series:
                    series[s['name']] = s['data']
                else:
                    series[s['name']] += s['data']

            # turn series into original form
            result['series'] = [{'name': k, 'data': list(v)} for k, v in series.items()]

        if not INCLUDE_NO_DATA:
            result = _remove_no_data(result)

        results.append(result)

    logging.info("Results:\n{}".format(results))
    io_helper.save_results(json.dumps(results), '', shapes.Shapes.HIGHCHARTS)


def _load_intermediate_data(job_ids):
    jobs_data = [io_helper.get_results(job_id).data for job_id in job_ids]
    # chain all results together, ignore empty results
    data = list(itertools.chain(*[json.loads(d) for d in jobs_data if d]))

    if not data:
        raise errors.UserError('Intermediate jobs {} do not have any data.'.format(job_ids))

    return data


def compute_histograms(dep_var, indep_vars, nb_bins=DEFAULT_BINS):
    histograms = list()
    if len(dep_var) > 0:
        histograms.append(compute_histogram(dep_var, nb_bins=nb_bins))
        grouping_vars = [indep_var for indep_var in indep_vars if utils.is_nominal(indep_var)]
        for grouping_var in grouping_vars:
            histograms.append(compute_histogram(dep_var, grouping_var, nb_bins))
    return histograms


def compute_histogram(dep_var, grouping_var=None, nb_bins=DEFAULT_BINS):
    label = "Histogram"
    title = '%s histogram' % get_var_label(dep_var)
    if grouping_var:
        label += " - %s" % get_var_label(grouping_var)
        title += " by %s" % get_var_label(grouping_var)
    categories, categories_labels = compute_categories(dep_var, nb_bins)
    series = compute_series(dep_var, categories, grouping_var)
    histo = {
        "chart": {"type": 'column'},
        "label": label,
        "title": {"text": title},
        "xAxis": {"categories": categories_labels},
        "yAxis": {
            "allowDecimals": False,
            "min": 0,
            "title": {
                "text": 'Number of participants'
            }
        },
        "series": series
    }
    return histo


def error_histograms(dep_var, indep_vars):
    histograms = list()
    if len(dep_var) > 0:
        histograms.append(error_histogram(dep_var))
        grouping_vars = [indep_var for indep_var in indep_vars if utils.is_nominal(indep_var)]
        for grouping_var in grouping_vars:
            histograms.append(error_histogram(dep_var, grouping_var))
    return json.dumps(histograms)


def error_histogram(dep_var, grouping_var=None):
    label = "Histogram"
    title = '%s histogram (no data or error)' % dep_var['name']
    if grouping_var:
        label += " - %s" % get_var_label(grouping_var)
        title += " by %s" % get_var_label(grouping_var)
    histo = {
        "chart": {"type": 'column'},
        "label": label,
        "title": {"text": title},
        "xAxis": {"categories": []},
        "yAxis": {
            "allowDecimals": False,
            "min": 0,
            "title": {
                "text": 'Number of participants'
            }
        },
        "series": []
    }
    return histo


def compute_categories(dep_var, nb_bins=DEFAULT_BINS):
    values = pd.Series(dep_var['series'])

    if len(values) == 0:
        raise errors.UserError('Dependent variable {} is empty.'.format(dep_var['name']))

    # TODO: dep_var['series'] can contain both np.nan (in numerical variables) and None (in nominal), pd.isnull
    # can handle them both
    has_nulls = pd.isnull(dep_var['series']).any()
    if utils.is_nominal(dep_var):
        categories = [str(c) for c in dep_var['type']['enumeration']]
        if 'enumeration_labels' in dep_var['type']:
            categories_labels = [str(c) for c in dep_var['type']['enumeration_labels']]
        else:
            categories_labels = categories

        if has_nulls:
            categories.append('None')
            categories_labels.append('No data')
    else:
        # calculate min and max if not available in variable (ignore null values)
        values = pd.Series(dep_var['series'])
        minimum = dep_var.get('minValue', values.min())
        maximum = dep_var.get('maxValue', values.max())

        all_nulls = values.isnull().all()

        if all_nulls:
            categories = ['None']
            categories_labels = ['No data']
        else:
            if utils.is_integer(dep_var):
                step = math.ceil((maximum - minimum) / nb_bins)
                categories = list(arange(minimum, maximum, step).tolist())
                categories_labels = ["%d - %d" % (v, v + step) for v in categories]
            else:
                step = (maximum - minimum) / nb_bins
                categories = list(arange(minimum, maximum, step).tolist())
                categories_labels = ["%s - %s" % ("{:.2f}".format(v), "{:.2f}".format(v + step)) for v in categories]
                categories.append(categories[-1] + step)

            if has_nulls:
                categories.append('None')
                categories_labels.append('No data')

    return categories, categories_labels


def compute_series(dep_var, categories, grouping_var=None):
    series = list()
    has_nulls = pd.isnull(dep_var['series']).any()
    if utils.is_nominal(dep_var):
        if not grouping_var:
            series.append({"name": "all", "data": count(dep_var['series'], categories)})
        else:
            for series_name in grouping_var['type']['enumeration']:
                filtered_data = [v for v, d in zip(dep_var['series'], grouping_var['series']) if d == series_name]
                series.append({"name": series_name, "data": count(filtered_data, categories)})
    else:
        if not grouping_var:
            values = pd.Series(dep_var['series'])

            if has_nulls:
                data = [int(i) for i in histogram(values.dropna(), categories[:-1])[0]] + [int(values.isnull().sum())]
            else:
                data = [int(i) for i in histogram(values, categories)[0]]

            series.append({"name": 'all', "data": data})
        else:
            values = pd.Series(dep_var['series'])
            grouping_values = pd.Series(grouping_var['series']).fillna('No data')

            for series_name in grouping_var['type']['enumeration']:
                filtered_data = pd.Series([v for v, d in zip(values, grouping_values) if d == series_name])
                if has_nulls:
                    data = [int(i) for i in histogram(filtered_data.dropna(), categories[:-1])[0]] + [int(filtered_data.isnull().sum())]
                else:
                    data = [int(i) for i in histogram(filtered_data, categories)[0]]

                series.append({"name": series_name, "data": data})
    return series


def _remove_no_data(chart):
    """Remove `No data` column from highcharts chart."""
    if chart['xAxis']['categories'] and chart['xAxis']['categories'][-1] == 'No data':
        chart['xAxis']['categories'] = chart['xAxis']['categories'][:-1]
        for serie in chart['series']:
            serie['data'] = serie['data'][:-1]
    return chart


def count(data, categories):
    items_count = OrderedDict([(c, 0) for c in categories])
    for v in data:
        try:
            if v is None:
                items_count['None'] += 1
            else:
                items_count[str(v)] += 1
        except KeyError:
            logging.warning("Unknown category %s" % str(v))
            logging.warning("Data: %s" % data)
    return list(items_count.values())


def get_var_label(var):
    return var.get('label', var['name'])


def _align_categories(ha, hb):
    """Align categories of two results from different nodes in case one contains null values."""
    ha = copy.deepcopy(ha)
    hb = copy.deepcopy(hb)

    if ha['xAxis']['categories'] and ha['xAxis']['categories'][-1] == 'No data' and hb['xAxis']['categories'][-1] != 'No data':
        hb['xAxis']['categories'].append('No data')
        for s in hb['series']:
            s['data'].append(0)

    elif hb['xAxis']['categories'] and hb['xAxis']['categories'][-1] == 'No data' and ha['xAxis']['categories'][-1] != 'No data':
        ha['xAxis']['categories'].append('No data')
        for s in ha['series']:
            s['data'].append(0)

    # edge case when one has only NULL values
    if ha['xAxis']['categories'] in (['No data'], []):
        ha['xAxis']['categories'] = hb['xAxis']['categories']
        for s in ha['series']:
            s['data'] = [0] * (len(ha['xAxis']['categories']) - len(s['data'])) + s['data']
    if hb['xAxis']['categories'] in (['No data'], []):
        hb['xAxis']['categories'] = ha['xAxis']['categories']
        for s in hb['series']:
            s['data'] = [0] * (len(hb['xAxis']['categories']) - len(s['data'])) + s['data']

    return ha, hb


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
        main()
    # > compute --mode aggregate --job-ids 12 13 14
    elif args.mode == 'aggregate':
        aggregate_histograms(args.job_ids)
