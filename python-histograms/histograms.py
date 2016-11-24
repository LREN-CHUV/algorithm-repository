#!/usr/bin/env python3

import json
import re
import numpy

import database_connector

# Settings and global variables
var = database_connector.get_var()
groups = re.split(', |,', str(database_connector.get_gvars()))
bins = 50  # Number of bins
variables = {}
columns = []
data = []


def main():

    # Link global variables
    global var
    global groups
    global variables
    global columns
    global data

    # Read input data
    metadata = database_connector.get_vars_metadata()
    columns = database_connector.get_vars_names()
    data = database_connector.get_vars_data()

    # Parse meta-data schema
    parse_variables(metadata)

    # Add Python type to variables
    dtype = numpy.dtype([(c, type_to_python(variables[c]["type"])) for c in columns])
    data = numpy.asarray(data, dtype=dtype)

    # Compute results
    pfa = generate_pfa(database_connector.get_code(), database_connector.get_name(),
                       database_connector.get_docker_image(), database_connector.get_model(), var, groups,
                       json.dumps(generate_descriptive_stats(var),
                                  sort_keys=True, indent=4, separators=(',', ': ')))
    error = ''
    shape = 'pfa_json'

    # Store results
    database_connector.save_results(pfa, error, shape)


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


def parse_variables(schema):
    if "variables" in schema:
        for v in schema["variables"]:
            code = v["code"]
            variables[code] = v
            for i, col in enumerate(columns):
                if col == code.lower():
                    columns[i] = code  # Avoid case-sensitivity problems

    if "groups" in schema:
        for g in schema["groups"]:
            parse_variables(g)


def type_to_python(input_type):
    return {
        'real': numpy.float,
        'integer': numpy.float,
        'binominal': "|S128",
        'polynominal': "|S128",
        'text': "|S128",
        'date': "|S128",
    }[input_type]


def generate_histogram(subdata, variable, group_variable):
    data_type = variables[variable]["type"]
    label = "Histogram"
    header = []
    category = []

    if group_variable:
        label += " - " + group_variable

    if data_type == "real":
        histogram = numpy.histogram(subdata[variable], bins=bins)
        header = histogram[1].tolist()
        value = histogram[0].tolist()

        if group_variable and variables[group_variable]["type"] != "real":
            # Histogram using grouping variable
            cat_header = []
            for gc in variables[group_variable]["enumerations"]:
                category += [gc['code']]*bins
                cat_data = []
                for v, g in zip(subdata[variable], subdata[group_variable]):
                    if gc['code'] == str(g, encoding='utf-8').rstrip():
                        cat_data.append(float(v))
                histogram = numpy.histogram(cat_data, bins=header)
                cat_header += histogram[1].tolist()
                value += histogram[0].tolist()
            header = cat_header

    elif data_type == "integer":
        h_min = subdata[variable].min()
        h_max = subdata[variable].max()
        h_step = ((h_max - h_min)//bins)+1
        histogram = numpy.histogram(subdata[variable], bins=numpy.arange(h_min, h_max + (2 * h_step), h_step))
        header = histogram[1].tolist()
        value = histogram[0].tolist()

        header = [int(h) for h in header]

        if group_variable and variables[group_variable]["type"] != "real":
            # Histogram using grouping variable
            cat_header = []
            value = []
            for gc in variables[group_variable]["enumerations"]:
                category += [gc["code"]]*len(header)
                cat_data = []  # Store only data for the current gc
                for v, g in zip(subdata[variable], subdata[group_variable]):
                    if gc['code'] == str(g, encoding='utf-8').rstrip():
                        cat_data.append(int(v))
                histogram = numpy.histogram(cat_data, bins=header)
                cat_header += histogram[1].tolist()
                value += histogram[0].tolist()
            header = cat_header

    else:
        # Nominal variable
        sums = {}
        for c1 in variables[variable]["enumerations"]:
            code = c1["code"]
            header.append(code)
            sums[code] = 0

        for v in subdata[variable]:
            sums[str(v, encoding='utf-8').rstrip()] += 1

        value = list(map(lambda h: sums[h], header))

        if group_variable and variables[group_variable]["type"] != "real":
            # Histogram using grouping variable
            cat_header = []
            value = []
            n = len(header)  # number of possible values for this variable
            for gc in variables[group_variable]["enumerations"]:
                cat_header += header
                category += [gc["code"]] * n
                cat_data = []  # Store only data for the current gc
                for v, g in zip(subdata[variable], subdata[group_variable]):
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


# Generate an object containing the descriptive statistics for the given variable
def generate_descriptive_stats(var):
    output = []
    data_type = variables[var]["type"]

    if data_type in ["integer", "real"]:
        subdata = data[~numpy.isnan(data[var])]
        output.append(generate_histogram(subdata, var, None))
        for group in groups:
            output.append(generate_histogram(subdata, var, group))

    elif variables[var]["type"] in ["binominal", "polynominal"]:  # Binominal/polynominal variables
        subdata = data[(data[var]) != b'']
        subdata = subdata[(data[var]) != b'None']
        output.append(generate_histogram(subdata, var, None))
        for group in groups:
            output.append(generate_histogram(subdata, var, group))

    return output


if __name__ == '__main__':
    main()
