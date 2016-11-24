#!/usr/bin/env python3

import json
import re
import numpy

import database_connector


# Settings and global variables
bins = 50  # Number of bins


def main():

    # Get inputs
    data = database_connector.fetch_data()['data']
    metadata = database_connector.fetch_data()['headers']
    colnames = [col.name for col in metadata]
    var = colnames[0]
    groups = colnames[1:]

    # Compute results
    pfa = generate_pfa(database_connector.get_code(), database_connector.get_name(),
                       database_connector.get_docker_image(), database_connector.get_model(), var, groups,
                       json.dumps(generate_descriptive_stats(var, groups, data, metadata),
                                  sort_keys=True, indent=4, separators=(',', ': ')))
    error = ''
    shape = 'pfa_json'

    # Store results
    database_connector.save_results(pfa, error, shape)


# Generate an object containing the descriptive statistics for the given variable
def generate_descriptive_stats(var, groups, data, metadata):
    var_data = [row[0] for row in data]
    var_type = get_var_type(metadata[0].type_code)

    output = list()
    output.append(generate_histogram(var_data, var, var_type, None))
    for group in groups:
        output.append(generate_histogram(var_data, var, var_type, group))

    return output


def get_var_type(value):
    # ==> Temporary : Should use meta-db
    return {
        1042: "string",
        1082: "float",
        1700: "date"
    }[value]
    # < ==


def generate_histogram(data, variable, variable_type, group):
    label = "Histogram"
    header = []
    category = []

    # ==> Temporary : Should use meta-db
    variable_type = "real"
    group_data = ""
    group_type = "polynomial"
    group_categories = ["AD, MCI", "CN"]
    # < ==

    if group:
        label += " - " + group

    if variable_type == "real":
        data = [float(d) for d in data]  # Temporary
        histogram = numpy.histogram(data, bins=bins)
        header = histogram[1].tolist()
        value = histogram[0].tolist()

        if group and group_type != "real":
            # Histogram using grouping variable
            cat_header = []
            for gc in group_categories:
                category += [gc]*bins
                cat_data = []
                for v, g in zip(data, group_data):
                    if gc['code'] == str(g, encoding='utf-8').rstrip():
                        cat_data.append(float(v))
                histogram = numpy.histogram(cat_data, bins=header)
                cat_header += histogram[1].tolist()
                value += histogram[0].tolist()
            header = cat_header

    elif variable_type == "integer":
        h_min = data.min()
        h_max = data.max()
        h_step = ((h_max - h_min)//bins)+1
        histogram = numpy.histogram(data, bins=numpy.arange(h_min, h_max + (2 * h_step), h_step))
        header = histogram[1].tolist()
        value = histogram[0].tolist()

        header = [int(h) for h in header]

        if group and group_type != "real":
            # Histogram using grouping variable
            cat_header = []
            value = []
            for gc in group_categories:
                category += [gc["code"]]*len(header)
                cat_data = []  # Store only data for the current gc
                for v, g in zip(data, group_data):
                    if gc['code'] == str(g, encoding='utf-8').rstrip():
                        cat_data.append(int(v))
                histogram = numpy.histogram(cat_data, bins=header)
                cat_header += histogram[1].tolist()
                value += histogram[0].tolist()
            header = cat_header

    else:
        variable_categories = list(set(data))
        # Nominal variable
        sums = {}
        for c1 in variable_categories:
            code = c1["code"]
            header.append(code)
            sums[code] = 0

        for v in group_data:
            sums[str(v, encoding='utf-8').rstrip()] += 1

        value = list(map(lambda h: sums[h], header))

        if group and group_type != "real":
            # Histogram using grouping variable
            cat_header = []
            value = []
            n = len(header)  # number of possible values for this variable
            for gc in group_categories:
                cat_header += header
                category += [gc["code"]] * n
                cat_data = []  # Store only data for the current gc
                for v, g in zip(data, group_data):
                    if gc['code'] == str(g, encoding='utf-8').rstrip():
                        cat_data.append(str(v, encoding='utf-8').rstrip())
                hist = [0] * n
                for d in cat_data:
                    hist[header.index(d)] += 1
                value += hist
            header = cat_header

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
