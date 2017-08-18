#!/usr/bin/env python3

import logging
import json

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

import database_connector


def main():
    logging.basicConfig(level=logging.INFO)

    # Get variables names
    var = database_connector.get_var()  # Dependent variable
    gvars = database_connector.get_gvars()  # Independent nominal variables
    cvars = database_connector.get_covars()  # Independent continuous variables
    covs = [x for x in (gvars + cvars) if len(x) > 0]  # All independent variables

    # Check dependent variable type
    if database_connector.var_type(var)['type'] not in ["integer", "real"]:
        logging.warning("Dependent variable should be continuous !")
        return None

    # Get data
    fetched_data = database_connector.fetch_data()
    data = format_data(fetched_data)

    # Compute results
    pfa = generate_pfa(database_connector.get_code(), database_connector.get_name(),
                       database_connector.get_docker_image(), database_connector.get_model(), var, covs,
                       compute_anova(var, gvars, cvars, data).to_json())
    error = ''
    shape = 'pfa_json'

    logging.info("PFA: %s", pfa)

    # Store results
    database_connector.save_results(pfa, error, shape)


# Compute Anova
def compute_anova(var, gvars, cvars, data):
    formula = generate_formula(var, gvars, cvars)
    logging.info("Formula: %s" % formula)
    lm = ols(data=data, formula=formula).fit()
    logging.info(lm.summary())
    return anova_lm(lm, typ=2)


# Generate formula for Anova
def generate_formula(var, gvars, cvars):
    gvars = [str.format("C(%s)" % g) for g in gvars]
    gvars = ' + '.join(gvars)
    cvars = ' + '.join(cvars)
    cov = ' + '.join([gvars, cvars])
    cov = cov.strip(' + ')
    return str.format("%s ~ %s" % (var, cov))


# Format data for Anova
def format_data(fetched_data):
    data = dict()
    i = 0
    for c in fetched_data['columns']:
        data[c] = list()
        for v in fetched_data['data']:
            try:
                value = float(v[i])
            except ValueError:
                value = str(v[i])
            data[c].append(value)
        i += 1
    return data


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
        "type": "array",
        "doc": "Anova computation",
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
        "name": "Anova"
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
            "doc": "Main anova variable",
            "name": "variable"
          },
          {
            "type": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "doc": "Categories used for specific anova",
            "name": "groups"
          }
        ],
        "name": "Query"
      }
    }
  },
  "doc": "Anova computation",
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
