#!/usr/bin/env python3

import logging
import sys

import pandas
import database_connector  # Library coming from the parent Docker image and used to manage input/output data


def main():
    logging.basicConfig(level=logging.INFO)

    # Get variables names
    var = database_connector.get_var()  # Dependent variable
    gvars = database_connector.get_gvars()  # Independent nominal variables
    cvars = database_connector.get_covars()  # Independent continuous variables
    covs = [x for x in (gvars + cvars) if len(x) > 0]  # All independent variables

    error = ''  # You should store any error message in this variable
    shape = 'pfa_json'

    # Check dependent variable type
    if database_connector.var_type(var)['type'] not in ["integer", "real"]:
        error = 'Dependent variable should be continuous !'
        database_connector.save_results('', error, shape)
        sys.exit(error)
    else:

        # Get data
        data = database_connector.fetch_data()

        # Compute results
        results = compute_example(var, data)
        pfa = generate_pfa(database_connector.get_code(), database_connector.get_name(),
                           database_connector.get_docker_image(), database_connector.get_model(), var, covs, results)

        logging.info("PFA: %s", pfa)

        # Store results
        database_connector.save_results(pfa, error, shape)


# Compute example
def compute_example(var, data):
    data = pandas.DataFrame(data['data'], columns=data['columns'])
    return data[[var]].mean().to_json()


def generate_pfa(algo_code, algo_name, docker_image, model, variable, grps, results):
    str_grps = '","'.join(grps)
    output = ('''
{
  "code": "%s",
  "name": "%s",
  "cells": {
    "validations": [],
    "data": {
      "init": %s,
      "type": {
        "name": "example",
        "doc": "example computation",
        "namespace": "%s",
        "type": "record",
        "fields": [
          {
            "type": "map",
            "values": "double",
            "doc": "mean",
            "name": "mean"
          }
        ]
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
            "doc": "Main example variable",
            "name": "variable"
          },
          {
            "type": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "doc": "Categories used for specific example",
            "name": "groups"
          }
        ],
        "name": "Query"
      }
    }
  },
  "doc": "example computation",
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
    ''' % (algo_code, algo_name, results, model, str_grps, variable, docker_image))
    return output


if __name__ == '__main__':
    main()
