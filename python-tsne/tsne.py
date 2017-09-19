#!/usr/bin/env python3

import logging
import database_connector  # Library coming from the parent Docker image and used to manage input/output data
import subprocess
import os
import sys
import numpy as np
import tempfile
import scipy.stats
import pandas
import json
import re


def main():
    logging.basicConfig(level=logging.INFO)

    # Get variables names
    # Note - this implementation does not distinguish between vars and covars
    # they are all treated as tsne dimensions. All the data retrieved
    # is used to create the embedding.
    # TODO Discover if these assumptions are correct. If not it's easy to change...
    var = database_connector.get_var()  # Dependent variable
    gvars = database_connector.get_gvars()  # Independent nominal variables
    cvars = database_connector.get_covars()  # Independent continuous variables
    covs = [x for x in (gvars + cvars) if len(x) > 0]  # All independent variables

    # Check dependent variable type
    if database_connector.var_type(var)['type'] not in ["integer", "real"]:
        sys.exit("Dependent variable should be continuous !")

    # Get data
    data = database_connector.fetch_data()
    df = pandas.DataFrame(data['data'], columns=data['columns'])
    convdf = df.apply(lambda x: pandas.to_numeric(x))
    # Write the data to a temporary file
    f = tempfile.NamedTemporaryFile(delete=False)

    source_dimensions = len(data['columns'])  # source dimensions
    num_points = len(data['data'])   # number of samples/points
    input = convdf.values.astype(np.float32)

    # Get the parameters (optional)
    perplexity = 30
    theta = 0.5
    target_dimensions = 2
    iterations = 1000
    do_zscore = True
    try:
        perplexity_str = os.getenv('PARAM_MODEL_perplexity', '30')
        perplexity = int(perplexity_str)
        theta_str = os.getenv('PARAM_MODEL_theta', '0.5')
        theta = float(theta_str)
        iterations_str = os.getenv('PARAM_MODEL_iterations', '1000')
        iterations = int(iterations_str)
        target_dimensions_str = os.getenv('PARAM_MODEL_target_dimensions', '2')
        target_dimensions = int(target_dimensions_str)
        do_zscore_str = os.getenv('PARAM_MODEL_do_zscore', 'True')
        if do_zscore_str == 'True':
            do_zscore = True
        elif do_zscore_str == 'False':
            do_zscore = False
        else:
            raise ValueError
    except ValueError as e:
        logging.error("Could not convert supplied parameter to numeric value, error: ", e)
        raise
    except:
        logging.error(" Unexpected error:", sys.exec_info()[0])
        raise
    # Compute results
    if do_zscore:
        input = scipy.stats.zscore(input)

    inputFilePath = f.name
    input.tofile(inputFilePath)
    f.close()

    f = tempfile.NamedTemporaryFile(delete=False)
    outputFilePath = f.name
    f.close()
    output = a_tsne(inputFilePath, outputFilePath, num_points,
                     source_dimensions, target_dimensions, perplexity,
                     theta, iterations)

    chart = generate_scatterchart(output, perplexity, theta, iterations)

    error = ''
    shape = 'highchart_json'

    logging.info("Highchart: %s", chart)
    database_connector.save_results(chart, error, shape)

    # print("Chart is ", chart)


def testPlot(npdata):
    """
    Plot a numpy x,y array - For debug purposes only
    :param npdata:
    :return: None
    """
    import matplotlib.pyplot as plt
    x = npdata[:, 0]
    y = npdata[:, 1]
    colors = (0, 0, 0)
    plt.scatter(x, y, c=colors)
    plt.show()

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
          "output: {3}, dims: {4}x{5} ".format(str(perplexity), str(iterations),
                                               inputFilePath, outputFilePath, num_points, source_dimensions))
    sys.stdout.flush()
    status = subprocess.call(
        ['/atsne/atsne_cmd',
            '-p', str(perplexity), '-i', str(iterations),
            '-t', str(theta), '-d', str(target_dimensions),
            inputFilePath,  outputFilePath,
            str(num_points), str(source_dimensions)],
        env={"LD_LIBRARY_PATH": "/atsne"})
    print("end atsne")
    sys.stdout.flush()
    data = np.fromfile(outputFilePath, dtype=np.float32)
    data = np.reshape(data, (-1, 2))
    return data

def generate_scatterchart(data, perplexity, theta, iterations):
    """
        Generate json configuration for Highcharts to display the
        tsne plot.
    :param data: a numpy nd array shape (n,2)
    :param perplexity: the perplexity value used to generate the embedding
    :param theta: th theta value used to generate the embedding
    :param iterations: the number of iterations used in a-tSNE
    :return: JSON string representing a Highchart plot of the embedding
    """

    chart_template = {
        'chart': {
            'type': 'scatter',
            'zoomType': 'xy'
        },
        'title': {
            'text': "a-tSNE embedding for: " + ','.join([database_connector.get_var()] +  database_connector.get_covars())
        },
        'subtitle': {
            'text': 'tSNE params: perplexity {}, theta {}, iterations {}'.format(perplexity, theta, iterations)
        },
        'xAxis': {
            'title': {
                'enabled': True,
                'text': 'tsne1'
            },
            'labels': {
                'enabled': False
            }
        },
        'yAxis': {
            'title': {
                'enabled': True,
                'text': 'tsne2'
            },
            'labels': {
                'enabled': False
            }
        },
        'plotOptions': {
            'scatter': {
                'marker': {
                    'radius': 3,
                },
            }
        },
        'series': [{
            'name': 'tSNE Embedding',
            'color': 'rgba(223, 83, 83, .5)',
            'data': data.tolist()
        }]
    }

    json_str =  json.dumps(chart_template)
    # de-quote the keys - compatible with javascript
    return re.subn(r"\"(\w+)\"(:)", r"\1\2", json_str)[0]




if __name__ == '__main__':
    main()
