#!/usr/bin/env python3

import math

try:
    import utils_read_inputs
except:
    from utils import utils_read_inputs

def generate_data_univar(p0, v0, t0):
    """
    Creates the values for a curve for a single patient (combination of p0, v0, t0), to plot the curve
    :param p0:
    :param v0:
    :param t0:
    :return: The succession of curves
    """
    loc_series = []
    for t in range(0, 110):
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
    for t in range(0, 110):
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

    # Generate individual curves: this will be needed in SGA2, but is not needed in SGA1

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

    # Generate individual curves: this will be needed in SGA2, but is not needed in SGA1
    #for id_patient in indiv_param.keys():
    #    print(indiv_param[id_patient])
    #    t0 = indiv_param[id_patient]['tau'][0]
    #    v0 = math.exp(float(indiv_param[id_patient]['ksi'][0]))
    #    w = math.exp(float(indiv_param[id_patient]['w'][0]))
    #    id = indiv_param[id_patient]['id'][0]
    #    indiv_results = generate_data_multivar(g, delta, w, v0, t0)
    #    for delta in deltas:
    #       loc_series.append({'data': indiv_results, 'name': 'Patient ' + id} + "_" + delta)
    return loc_series



def write_univar_output_to_highchart():
    """
    Computes the highchart for the univariate model, and writes it to a string
    :return: string: The highchart representation of the curves
    """
    pop_param = utils_read_inputs.read_population_parameters("longitudina/examples/scalar_models/univariate/output/population_parameters.csv")
    indiv_param = utils_read_inputs.read_multiple_individual_parameters("longitudina/examples/scalar_models/univariate/output/individual_parameters.csv")
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
    pop_param = utils_read_inputs.read_population_parameters("longitudina/examples/scalar_models/multivariate/output/population_parameters.csv")
    indiv_param = utils_read_inputs.read_individual_parameters("longitudina/examples/scalar_models/multivariate/output/individual_parameters.csv")
    series = generate_all_data_multivar(pop_param, indiv_param)
    result_string = "{title: {text: 'Evolution of scores in time'},yAxis: {title: {text: 'Scores'}}, xAxis: {title: " \
                    "{text: 'Age'}}, legend: {layout: 'vertical',align: 'right',verticalAlign: 'middle',borderWidth: 0}, " \
                    "series: " + str(series) + "}"

    return result_string