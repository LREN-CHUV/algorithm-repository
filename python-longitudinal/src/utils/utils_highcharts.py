#!/usr/bin/env python3

import logging
import os
import sys
import math
import csv
import numpy as np

def generate_data_univar(p0, v0, t0):
    """
    Creates the values for a curve for a single patient (combination of p0, v0, t0), to plot the curve
    :param p0:
    :param v0:
    :param t0:
    :return: The succession of curves
    """
    loc_series = []
    for t in range(40, 110):
        loc_series.append({'x': t, 'y': 1. / (1. + (1./ p0 - 1) * math.exp(-v0*(t-t0)))})
    return loc_series


def generate_data_multivar(g, delta, w, v0, t0):
    """
    Multivariate function
    Args:
        g (float)
        delta (float):
        w (float): weight
        v0 (float): acceleration of the slope
        t0 (float): initial start of the slope for the specific individual
    """
    loc_series = []
    for t in range(40, 110):
        G = g * math.exp(-delta) + 1.
        parallel_curve = - w * (1./G + 1) * (G + 1) - delta - v0 * (t - t0)
        parallel_curve = 1 + g * math.exp(parallel_curve)
        parallel_curve = 1. / parallel_curve
        loc_series.append({'x': t, 'y': parallel_curve})
    return loc_series


def generate_all_data_univar(pop_param, indiv_param):
    loc_series = []
    # Generate population curves: mean
    p0 = pop_param['p0']
    v0 = pop_param['v0']
    t0 = pop_param['t0']
    loc_series.append({'data': generate_data_univar(p0, v0, t0), 'name': 'Mean'})

    # Generate individual curves
    #for id_patient in indiv_param.keys():
    #    t0 = indiv_param[id_patient]['tau'][0]
    #    v0 = math.exp(float(indiv_param[id_patient]['ksi'][0]))
    #    id = indiv_param[id_patient]['id'][0]
    #    indiv_results = generate_data_univar(p0, v0, t0)
    #    loc_series.append({'data': indiv_results, 'name': 'Patient ' + id})
    return loc_series


def generate_all_data_multivar(pop_param, indiv_param):
    loc_series = []
    # Generate population curves: mean
    g = pop_param['g']
    deltas = pop_param['deltas']
    v0 = pop_param['v0']
    t0 = pop_param['t0']
    for delta in deltas:
        loc_series.append({'data': generate_data_multivar(g, delta, 0, v0, t0), 'name': 'Mean_' + str(delta)})

    # Generate individual curves
    # To edit if needed
    #for id_patient in indiv_param.keys():
    #    print(indiv_param[id_patient])
    #    t0 = indiv_param[id_patient]['tau'][0]
    #    v0 = math.exp(float(indiv_param[id_patient]['ksi'][0]))
    #    w = math.exp(float(indiv_param[id_patient]['w'][0]))
    #    id = indiv_param[id_patient]['id'][0]
    #    indiv_results = generate_data_multivar(t, g, delta, w, v0, t0)
    #    for delta in deltas:
    #       loc_series.append({'data': indiv_results, 'name': 'Patient ' + id} + "_" + delta)
    return loc_series


def read_population_parameters(path_to_file):
    """
    Reads the population parameters file
    Args:
        path_to_file: the path to the population file Longitudina outputted

    Returns:
        dict: a dictionnary with the name of the parameters as keys and their values as values
    """
    reader = csv.reader(open(path_to_file, 'r'))
    params = {}
    params_delta = {}
    params_delta_tilde = {}
    nb_delta = 0
    for row in reader:
        name = row[0].lower()
        if name[0:6] == "delta#":
            params_delta[name] = float(row[1])
            nb_delta += 1
        elif name[0:6] == "delta_":
            params_delta_tilde[name] = float(row[1])
        else:
            params[name] = float(row[1])

    params["deltas"] = [params_delta["delta#"+str(i)] for i in range(len(params_delta))]
    #params["deltas_tilde"] = [params_delta_tilde["delta_tilde#"+str(i)] for i in range(len(params_delta))]

    return params


def read_multiple_individual_parameters(file_name):
    reader = csv.reader(open(file_name, 'r'))
    parameters = {}
    s_parameters_mean = {}
    s_parameters_last = {}

    for row in reader:
        id_ = row[0].strip()
        parameter = row[1].strip().lower()
        last_value = float(row[2].strip())
        mean_value = float(row[3].strip())

        if id_ not in parameters:
            parameters[id_] = {}
            s_parameters_last[id_] = {}
            s_parameters_mean[id_] = {}

        ### Handle the sources
        if parameter[0:2] != "s#":
            parameters[id_]['last_'+parameter] = last_value
            parameters[id_]['mean_'+parameter] = mean_value
        else:
            s_parameters_last[id_][parameter] = last_value
            s_parameters_mean[id_][parameter] = mean_value

    for k, v in s_parameters_last.items():
        values = [v["s#"+str(i)] for i in range(len(v))]
        parameters[k]["last_s"] = values

    for k, v in s_parameters_mean.items():
        values = [v["s#"+str(i)] for i in range(len(v))]
        parameters[k]["mean_s"] = values

    return parameters

def compute_individual_parameters(list_elements, number_of_params):
    """ Reads the individual parameters file
    Args:
        list_elements: the list of the lines extracted from the files
        number_of_params: the number of parameters per trajectory

    Returns:
        dict: dictionnary of individual parameters
    """
    individual_parameters = {}
    idx_start = 0

    for tpl in number_of_params:
        idx_end = idx_start + tpl[1]
        if tpl[0] == "id":
            individual_parameters[tpl[0].rstrip()] = [(list_elements[i].rstrip()) for i in range(idx_start, idx_end)]
        else:
            individual_parameters[tpl[0].rstrip()] = [float(list_elements[i].rstrip()) for i in range(idx_start, idx_end)]
        idx_start = idx_end

    return individual_parameters



def write_univar_output_to_highchart():
    """
    Computes the highchart for the univariate model, and writes it to a string
    :return: string: The highchart representation of the curves
    """
    pop_param = read_population_parameters("longitudina/examples/scalar_models/univariate/sigmoid/output/population_parameters.csv")
    indiv_param = read_multiple_individual_parameters("longitudina/examples/scalar_models/univariate/sigmoid/output/individual_parameters.csv")
    series = generate_all_data_univar(pop_param, indiv_param)
    result_string = "{title: {text: 'Evolution of scores in time'},yAxis: {title: {text: 'Scores'}}, xAxis: {title: " \
                    "{text: 'Age'}}, legend: {layout: 'vertical',align: 'right',verticalAlign: 'middle',borderWidth: 0}, " \
                    "series: " + str(series) + "}"

    return result_string


def write_multivar_output_to_highchart():
    """
    Computes the highchart for the multivariate model, and writes it to a string
    :return: string: The highchart representation of the curves
    """
    pop_param = read_population_parameters("longitudina/examples/scalar_models/multivariate/output/population_parameters.csv")
    indiv_param = read_individual_parameters("longitudina/examples/scalar_models/multivariate/output/individual_parameters.csv")
    series = generate_all_data_multivar(pop_param, indiv_param)
    result_string = "{title: {text: 'Evolution of scores in time'},yAxis: {title: {text: 'Scores'}}, xAxis: {title: " \
                    "{text: 'Age'}}, legend: {layout: 'vertical',align: 'right',verticalAlign: 'middle',borderWidth: 0}, " \
                    "series: " + str(series) + "}"

    return result_string