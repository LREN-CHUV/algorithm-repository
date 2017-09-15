#!/usr/bin/env python3

import logging
import database_connector  # Library coming from the parent Docker image and used to manage input/output data
import subprocess
import os
import sys
import numpy as np
import tempfile


def main():
    logging.basicConfig(level=logging.INFO)

    # Get variables names
    var = database_connector.get_var()  # Dependent variable
    gvars = database_connector.get_gvars()  # Independent nominal variables
    cvars = database_connector.get_covars()  # Independent continuous variables
    covs = [x for x in (gvars + cvars) if len(x) > 0]  # All independent variables

    # Check dependent variable type
    if database_connector.var_type(var)['type'] not in ["integer", "real"]:
        sys.exit("Dependent variable should be continuous !")

    # Get data
    data = database_connector.fetch_data()

    # Write the data to a temporary file
    f = tempfile.NamedTemporaryFile(delete=False)
    # TODO Get sizes from database data
    source_dimensions = 50
    num_points = 10000
    input = np.empty([source_dimensions, num_points], dtype=np.float32)
    # TODO Populate input file from database data
    inputFilePath = f.name
    input.tofile(inputFilePath, delete=False)
    f.close()

    f = tempfile.NamedTemporaryFile(delete=False)
    outputFilePath = f.name
    f.close()

    # Get the parameters (optional)
    perplexity = 30
    theta = 0.5
    target_dimensions = 2
    iterations = 1000
    try:
        perplexity_str = os.getenv('PARAM_MODEL_perplexity', '30')
        perplexity = int(perplexity_str)
        theta_str = os.getenv('PARAM_MODEL_theta', '0.5')
        theta = float(theta_str)
        iterations_str = os.getenv('PARAM_MODEL_iterations', '1000')
        iterations = int(iterations_str)
        target_dimensions_str = os.getenv('PARAM_MODEL_target_dimensions', '2')
        target_dimensions = int(target_dimensions_str)
    except ValueError as e:
        print "Could not convert supplied parameter to numeric value"
        raise
    except:
        print " Unexpected error:", sys.exec_info()[0]
        raise
    # Compute results
    embedding = a_tsne(inputFilePath, outputFilePath, num_points,
                     source_dimensions, target_dimensions, perplexity,
                     theta, iterations)

    # TODO write embedding as HighChart output
    #pfa = generate_pfa(database_connector.get_code(), database_connector.get_name(),
                       database_connector.get_docker_image(), database_connector.get_model(), var, covs, results)
    #error = ''  # You should store any error message in this variable
    #shape = 'pfa_json'

    #logging.info("PFA: %s", pfa)

    # Store results
    #database_connector.save_results(pfa, error, shape)


# atsne
def a_tsne(inputFilePath, outputFilePath, num_points,
           source_dimensions, target_dimensions, perplexity,
           theta, iterations):
    """

    :param inputFilePath: full path to the input file contain float data
    :param outputFilePath: path to write the embedding output
    :param num_points: number of points in input
    :param source_dimensions: dimensionality of input
    :param target_dimensions: dimensionality of output
    :param perplexity: tsne neighbourhood factor
    :param theta: approximation level
    :param iterations: number of iterations of gradient descent
    :return:
    """
    #pydevd.settrace('localhost', port=41022, stdoutToServer=True, stderrToServer=True)  # port=41022, stdoutToServer=True, stderrToServer=True)
    print("atsne: perplexity: {0}, "
          "iters: {1}, input: {2}, "
          "output: {3}, dims: {4}x{5} ".format(str(perplexity), str(iterations), inputFilePath, outputFilePath, str(header['sizes'][0]), str(header['sizes'][1]) ))
    sys.stdout.flush()
    status = subprocess.call(
        ['/atsne_cmd',
            '-p', str(perplexity), '-i', str(iterations),
            '-t', str(theta), '-d', str(target_dimensions),
            inputFilePath,  outputFilePath,
            str(num_points), str(source_dimensions)],
        env={"LD_LIBRARY_PATH": "/atsne"})
    print("end atsne")
    sys.stdout.flush()
    data = np.fromfile(outputFile, dtype=np.float32)
    data = np.reshape(data, (-1, 2))
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
