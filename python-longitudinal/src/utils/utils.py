#!/usr/bin/env python3

try:
    import utils_highcharts
except:
    from utils import utils_highcharts
try:
    import utils_PFA
except:
    from utils import utils_PFA

def write_output_to_highchart(model_type):
    if model_type == "univariate":
        return utils_highcharts.write_univar_output_to_highchart()
    if model_type == "multivariate":
        return utils_highcharts.write_multivar_output_to_highchart()

def write_output_to_pfa(model_type):
    return utils_PFA.write_output_to_pfa(model_type)
