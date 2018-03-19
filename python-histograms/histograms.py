#!/usr/bin/env python3

from mip_helper import io_helper

import logging
import json
import math

from collections import OrderedDict
from numpy import arange
from numpy import histogram


BINS_PARAM = "bins"
STRICT_PARAM = "strict"
DEFAULT_BINS = 20
DEFAULT_STRICT = False


class UserError(Exception):

    pass


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

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
    nb_bins = get_bins_param(inputs["parameters"], BINS_PARAM)

    # Compute histograms (JSON formatted for HighCharts)
    histograms_results = compute_histograms(dep_var, indep_vars, nb_bins)

    # Store results
    io_helper.save_results(histograms_results, '', 'application/highcharts+json')
    except UserError as e:
        logging.error(e)
        strict = get_strict_param(inputs["parameters"], STRICT_PARAM)
        if (strict):
            # Store error
            io_helper.save_results('', str(e), 'text/plain+error')
        else:
            # Display something to the user
            histograms_results = error_histograms(dep_var, indep_vars, nb_bins)
            io_helper.save_results(histograms_results, '', 'application/highcharts+json')


def compute_histograms(dep_var, indep_vars, nb_bins=DEFAULT_BINS):
    histograms = list()
    if len(dep_var) > 0:
        histograms.append(compute_histogram(dep_var, nb_bins=nb_bins))
        grouping_vars = [indep_var for indep_var in indep_vars if is_nominal(indep_var)]
        for grouping_var in grouping_vars:
            histograms.append(compute_histogram(dep_var, grouping_var, nb_bins))
    return json.dumps(histograms)


def compute_histogram(dep_var, grouping_var=None, nb_bins=DEFAULT_BINS):
    label = "Histogram"
    title = '%s histogram' % dep_var['name']
    if grouping_var:
        label += " - %s" % grouping_var["name"]
        title += " by %s" % grouping_var["name"]
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

def error_histograms(dep_var, grouping_var=None, nb_bins=DEFAULT_BINS):
    label = "Histogram"
    title = '%s histogram (no data or error)' % dep_var['name']
    if grouping_var:
        label += " - %s" % grouping_var["name"]
        title += " by %s" % grouping_var["name"]
    categories, categories_labels = compute_categories(dep_var, nb_bins)
    series = []
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

def compute_categories(dep_var, nb_bins=DEFAULT_BINS):
    if len(dep_var['series']) == 0:
        raise UserError('Dependent variable {} is empty.'.format(dep_var['name']))
    if is_nominal(dep_var):
        categories = [str(c) for c in dep_var['type']['enumeration']]
        categories_labels = categories
    elif is_integer(dep_var):
        values = dep_var['series']
        minimum = min(values)
        maximum = max(values)
        step = math.ceil((maximum - minimum) / nb_bins)
        categories = list(arange(minimum, maximum, step).tolist())
        categories_labels = ["%d - %d" % (v, v + step) for v in categories]
    else:
        values = dep_var['series']
        minimum = min(values)
        maximum = max(values)
        step = (maximum - minimum) / nb_bins
        categories = list(arange(minimum, maximum, step).tolist())
        categories_labels = ["%s - %s" % ("{:.2f}".format(v), "{:.2f}".format(v + step)) for v in categories]
        categories.append(categories[-1] + step)
    return categories, categories_labels


def compute_series(dep_var, categories, grouping_var=None):
    series = list()
    if is_nominal(dep_var):
        if not grouping_var:
            series.append({"name": "all", "data": count(dep_var['series'], categories)})
        else:
            for series_name in grouping_var['type']['enumeration']:
                filtered_data = [v for v, d in zip(dep_var['series'], grouping_var['series']) if d == series_name]
                series.append({"name": series_name, "data": count(filtered_data, categories)})
    else:
        if not grouping_var:
            series.append({"name": 'all', "data": [int(i) for i in histogram(dep_var['series'], categories)[0]]})
        else:
            for series_name in grouping_var['type']['enumeration']:
                filtered_data = [v for v, d in zip(dep_var['series'], grouping_var['series']) if d == series_name]
                series.append({"name": series_name, "data": [int(i) for i in histogram(filtered_data, categories)[0]]})
    return series


def count(data, categories):
    items_count = OrderedDict([(c, 0) for c in categories])
    for v in data:
        try:
            items_count[str(v)] += 1
        except KeyError:
            logging.warning("Unknown category %s" % str(v))
    return list(items_count.values())


def get_bins_param(params_list, param_name):
    for p in params_list:
        if p["name"] == param_name:
            try:
                return int(p["value"])
            except ValueError:
                logging.warning("%s cannot be cast to integer !")
    logging.info("Using default number of bins: %s" % DEFAULT_BINS)
    return DEFAULT_BINS

def get_strict_param(params_list, param_name):
    for p in params_list:
        if p["name"] == param_name:
            try:
                return boolean(p["value"])
            except ValueError:
                logging.warning("%s cannot be cast to boolean !")
    logging.info("Using default number of bins: %s" % DEFAULT_BINS)
    return DEFAULT_BINS

def is_nominal(var):
    return var['type']['name'] in ['binominal', 'polynominal']


def is_integer(var):
    return var['type']['name'] in ['integer']


if __name__ == '__main__':
    main()
