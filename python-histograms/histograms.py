#!/usr/bin/env python3

import json
import numpy

import database_connector


# Settings and global variables
bins = 50  # Number of bins


def main():

    # Get inputs
    var = database_connector.get_var()
    groups = [x for x in (database_connector.get_covars() + database_connector.get_gvars()) if len(x) > 0]
    fetched_data = database_connector.fetch_data()
    data = fetched_data['data']
    data_columns = fetched_data['columns']

    # Compute results
    pfa = generate_pfa(database_connector.get_code(), database_connector.get_name(),
                       database_connector.get_docker_image(), database_connector.get_model(), var, groups,
                       json.dumps(generate_descriptive_stats(var, groups, data, data_columns),
                                  sort_keys=True, indent=4, separators=(',', ': ')))
    error = ''
    shape = 'pfa_json'

    print(pfa)

    # Store results
    database_connector.save_results(pfa, error, shape)


# Generate an object containing the descriptive statistics for the given variable
def generate_descriptive_stats(var, groups, data, data_columns):
    output = list()
    output.append(generate_histogram(data, data_columns, var, None))
    for group in groups:
        output.append(generate_histogram(data, data_columns, var, group))

    return output


def generate_histogram(data, data_columns, variable, group):
    var_data = [row[0] for row in data]
    group_data = [row[data_columns.index(group.lower())] for row in data] if group else []
    variable_type = database_connector.var_type(variable)['type']
    group_type = database_connector.var_type(group)['type'] if group else None
    group_categories = database_connector.var_type(group)['values'] if group else None

    category = list()
    label = "Histogram"
    if group:
        label += " - " + group

    if variable_type == "real":
        var_data = [float(d) for d in var_data]
        category, header, value = histo_real(category, var_data, group, group_categories, group_data, group_type)
    elif variable_type == "integer":
        var_data = [int(d) for d in var_data]
        category, header, value = histo_integer(category, var_data, group, group_categories, group_data, group_type)
    else:
        var_data = [str(d) for d in var_data]
        var_categories = database_connector.var_type(variable)['values']
        category, header, value = histo_nominal(category, var_data, group, group_categories, group_data, group_type,
                                                var_categories)

    return {
        "code": variable,
        "dataType": "DatasetStatistic",
        "label": label,
        "dataset": {
            "data": {
                "header": header,
                "shape": "vector",
                "value": value,
                "categories": category
            },
            "name": "Count"
        }
    }


def histo_nominal(category, data, group, group_categories, group_data, group_type, variable_categories):
    data = [str(d) for d in data]
    header = []
    # Nominal variable
    sums = {}
    for code in variable_categories:
        header.append(code)
        sums[code] = 0
    for v in data:
        sums[v.rstrip()] += 1
    value = list(map(lambda h: sums[h], header))
    if group and group_type != "real":
        # Histogram using grouping variable
        cat_header = []
        value = []
        n = len(header)  # number of possible values for this variable
        for gc in group_categories:
            cat_header += header
            category += [gc] * n
            cat_data = []  # Store only data for the current gc
            for v, g in zip(data, group_data):
                if str(gc).rstrip() == str(g).rstrip():
                    cat_data.append(v)
            hist = [0] * n
            for d in cat_data:
                hist[header.index(str(d).rstrip())] += 1
            value += hist
        header = cat_header
    return category, header, value


def histo_integer(category, data, group, group_categories, group_data, group_type):
    data = [int(d) for d in data]
    h_min = min(data)
    h_max = max(data)
    h_step = ((h_max - h_min) // bins) + 1
    histogram = numpy.histogram(data, bins=numpy.arange(h_min, h_max + (2 * h_step), h_step))
    header = histogram[1].tolist()
    value = histogram[0].tolist()
    header = [int(h) for h in header]
    if group and group_type != "real":
        # Histogram using grouping variable
        cat_header = []
        value = []
        for gc in group_categories:
            category += [gc] * len(header)
            cat_data = []  # Store only data for the current gc
            for v, g in zip(data, group_data):
                if gc == g:
                    cat_data.append(int(v))
            histogram = numpy.histogram(cat_data, bins=header)
            cat_header += histogram[1].tolist()
            value += histogram[0].tolist()
        header = cat_header
    return category, header, value


def histo_real(category, data, group, group_categories, group_data, group_type):
    data = [float(d) for d in data]
    histogram = numpy.histogram(data, bins=bins)
    header = histogram[1].tolist()
    value = histogram[0].tolist()
    if group and group_type != "real":
        # Histogram using grouping variable
        cat_header = []
        for gc in group_categories:
            category += [gc] * bins
            cat_data = []
            for v, g in zip(data, group_data):
                if gc == g:
                    cat_data.append(float(v))
            histogram = numpy.histogram(cat_data, bins=header)
            cat_header += histogram[1].tolist()
            value += histogram[0].tolist()
        header = cat_header
    return category, header, value


def generate_pfa(algo_code, algo_name, docker_image, model, variable, grps, results):
    str_grps = '","'.join(grps)
    output = ('''
{
  "code": "%s",
  "name": "%s",
  "data": {
    "cells": {
      "validations": [],
      "data": {
        "init": %s,
        "type": {
          "type": "array",
          "doc": "Histograms computation",
          "items":
            {
              "type": {
                "namespace": "%s",
                "type": "record",
                "fields": [
                  {
                    "type": "string",
                    "doc": "Shape",
                    "name": "shape"
                  },
                  {
                    "type": "array",
                    "items": "string",
                    "doc": "Categories",
                    "name": "categories"
                  },
                  {
                    "type": "array",
                    "items": "string",
                    "doc": "Header",
                    "name": "header"
                  },
                  {
                    "type": "array",
                    "items": "int",
                    "doc": "Value",
                    "name": "value"
                  }
                ]
              }
            },
          "name": "Histograms"
        }
      },
      "query": {
        "init": {
          "grouping": ["%s"],
          "variable": "%s"
        },
        "type": {
          "type": "record",
          "doc": "Definition of the inputs",
          "fields": [
            {
              "type": {
                "type": "string"
              },
              "doc": "Main histogram variable",
              "name": "variable"
            },
            {
              "type": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "doc": "Categories used for specific histograms",
              "name": "groups"
            }
          ],
          "name": "Query"
        }
      }
    },
    "name": "%s",
    "doc": "Histograms computation",
    "metadata": {
      "docker_image": "%s"
    },
    "output": {
      "type": "null"
    },
    "action": [
      null
    ],
    "input": {
      "type": "null"
    }
  }
}
    ''' % (algo_code, algo_name, results, model, str_grps, variable, algo_name, docker_image))
    return output


if __name__ == '__main__':
    main()
