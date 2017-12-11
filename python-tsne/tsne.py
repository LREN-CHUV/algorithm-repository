#!/usr/bin/env python3

import logging
from io_helper import io_helper # Library coming from the parent Docker image and used to manage input/output data
import subprocess
import sys
import numpy as np
import tempfile
import scipy.stats
import pandas as pd
import json
import re
import colorsys


def main():
    logging.basicConfig(level=logging.INFO)

    inputs = io_helper.fetch_data()

    # Dependent variable for tsne this might be the labels - this is optional
    labels = None
    dependent = inputs["data"].get("dependent", [])
    indep_vars = inputs["data"]["independent"]  # For tsne the data dimensions



    if not data_types_in_allowed(indep_vars, ["integer", "real"]):
        logging.warning("Independent variables should be continuous !")
        return None
    #
    data = format_independent_data(inputs["data"])
    df = pd.DataFrame.from_dict(data)
    source_dimensions = df.shape[1] # number of columns
    num_points = df.shape[0]   # number of samples/points

    convdf = df.apply(lambda x: pd.to_numeric(x))
    # Write the data to a temporary file
    f = tempfile.NamedTemporaryFile(delete=False)
    input = convdf.values.astype(np.float32)
    logging.debug('input {}'.format(input))

    # Get the parameters (optional)
    perplexity = 30
    theta = 0.5
    target_dimensions = 2
    iterations = 1000
    do_zscore = True
    dependent_is_label = True

    try:
        perplexity = get_parameter(inputs['parameters'], 'perplexity', perplexity)
        theta = get_parameter(inputs['parameters'], 'theta', theta)
        target_dimensions = get_parameter(inputs['parameters'], 'target_dimensions', target_dimensions)
        iterations = get_parameter(inputs['parameters'], 'iterations', iterations)
        do_zscore_str = get_parameter(inputs['parameters'], 'do_zscore', str(do_zscore))
        if do_zscore_str == 'True':
            do_zscore = True
        elif do_zscore_str == 'False':
            do_zscore = False
        else:
            raise ValueError
        dependent_is_label_str = get_parameter(inputs['parameters'], 'dependent_is_label', str(dependent_is_label))
        if dependent_is_label_str == 'True':
            dependent_is_label = True
        elif dependent_is_label_str == 'False':
            dependent_is_label = False
        else:
            raise ValueError

    except ValueError as e:
        logging.error("Could not convert supplied parameter to value, error: ", e)
        raise
    except:
        logging.error(" Unexpected error:", sys.exec_info()[0])
        raise
    # Compute results

    if do_zscore:
        input = scipy.stats.zscore(input)

    if len(dependent) > 0 and dependent_is_label:
        dep_var = dependent[0]
        labels = dep_var["series"]

    inputFilePath = f.name
    input.tofile(inputFilePath)
    f.close()

    f = tempfile.NamedTemporaryFile(delete=False)
    outputFilePath = f.name
    f.close()
    output = a_tsne(inputFilePath, outputFilePath, num_points,
                     source_dimensions, target_dimensions, perplexity,
                     theta, iterations)

    logging.debug('output shape {}'.format(output.shape))
    logging.debug('output {}'.format(output))
    chart = generate_scatterchart(output, indep_vars, labels, perplexity, theta, iterations)

    error = ''
    shape = 'application/highcharts+json'

    logging.debug("Highchart: %s", chart)
    io_helper.save_results(chart, error, shape)
    logging.info("Highchart output saved to database.")

    # print("Chart is ", chart)

def format_data(input_data):
    all_vars = input_data["dependent"] + input_data["independent"]
    data = {v["name"]: v["series"] for v in all_vars}
    return data

def format_independent_data(input_data):
    data = {v["name"]: v["series"] for v in input_data["independent"]}
    return data

def data_types_in_allowed(data, allowed_types):
    for var_info in data:
        if var_info["type"]["name"] not in allowed_types:
            logging.warning("Variable should be one of  !")
            return False
    return True

def get_parameter(params_list, param_name, default_value):
    """
    Params are a list where each list item is a dict containing
    the keys 'name' and 'value'
    :param params_list: the params list
    :param param_name: the 'name' to extract
    :param default_value: a default value if 'name' is not present
    :return:
    """
    for p in params_list:
        if p["name"] == param_name:
            return p["value"]
    return default_value



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
            str(num_points), str(source_dimensions)])
    print("end atsne")
    sys.stdout.flush()
    data = np.fromfile(outputFilePath, dtype=np.float32)
    data = np.reshape(data, (-1, 2))
    return data

def generate_scatterchart(data, indep_vars, labels, perplexity, theta, iterations):
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
            'text': "a-tSNE embedding for: " + ', '.join([x['name'] for x in indep_vars])

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
                'enabled': labels is not None
            }
        },
        'plotOptions': {
            'scatter': {
                'marker': {
                    'radius': 3,
                },
            }
        },
        'series': get_chart_series(data, labels)
    }

    return json.dumps(chart_template)
    # de-quote the keys - compatible with javascript
    # return re.subn(r"\"(\w+)\"(:)", r"\1\2", json_str)[0]


def get_chart_series(data, labels):
    logging.debug('data shape {}'.format(data.shape))
    logging.debug('data {}'.format(data))
    # pydevd.settrace('localhost', port=41022, stdoutToServer=True, stderrToServer=True)  # port=41022, stdoutToServer=True, stderrToServer=True)
    # no labels to differentiate the data everything in one big group
    if labels is None :
        return [{
            'name': 'tSNE Embedding',
            'color': 'rgba(223, 83, 83, .5)',
            'data': data.tolist()
        }]
    # otherwise group the data per label
    series_list = []
    unique_labels = list(set(labels))
    n_labels = len(unique_labels)
    hsv_colors = [(x*1.0/n_labels, 0.5, 0.5) for x in range(n_labels)]
    rgb_colors = [colorsys.hsv_to_rgb(*x) for x in hsv_colors]
    label_array = np.array(labels).reshape(-1,1)
    for idx, label in enumerate(unique_labels):
        mask = label_array == label
        sub_data = data[mask[:, 0], :]
        series = {
            'name': label,
            'color': 'rgba({}, {}, {}, .5)'.format(int(rgb_colors[idx][0]*255), int(rgb_colors[idx][1]*255), int(rgb_colors[idx][2]*255)),
            'data': sub_data.tolist()
        }
        series_list.append(series)
    return series_list



if __name__ == '__main__':
    main()
