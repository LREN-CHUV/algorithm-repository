#!/usr/bin/env python3

from io_helper import io_helper

import logging
import json

from pandas import DataFrame
from statsmodels.formula.api import ols

DEFAULT_DOCKER_IMAGE = "python-linear-regression"


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    inped_vars = inputs["data"]["independent"]

    # Check dependent variable type (should be continuous)
    if dep_var["type"]["name"] not in ["integer", "real"]:
        logging.warning("Dependent variable should be continuous !")
        return None

    # Extract data and parameters from inputs
    data = format_data(inputs["data"])

    # Compute linear-regression and generate PFA output
    linear_regression_results = format_output(compute_linear_regression(dep_var, inped_vars, data))

    # Store results
    io_helper.save_results(linear_regression_results, '', 'application/json')


def format_data(input_data):
    all_vars = input_data["dependent"] + input_data["independent"]
    data = {v["name"]: v["series"] for v in all_vars}
    return data


def format_output(statsmodels_dict):
    return json.dumps(DataFrame.from_dict(statsmodels_dict).transpose().fillna("NaN").to_dict())


def compute_linear_regression(dep_var, indep_vars, data):
    formula = generate_formula(dep_var, indep_vars)
    logging.info("Formula: %s" % formula)
    lm = ols(data=data, formula=formula).fit()
    logging.info(lm.summary())
    return {
        "coef": dict(lm.params),
        "std_err": dict(lm.bse),
        "t_values": dict(lm.tvalues),
        "p_values": dict(lm.pvalues)
    }


def generate_formula(dep_var, indep_vars):
    op = " + "
    dep_var = dep_var["name"]
    indep_vars = [v["name"] if v["type"]["name"] in ["integer", "real"]
                  else str.format("C(%s)" % v["name"]) for v in indep_vars]
    indep_vars = op.join(indep_vars)
    indep_vars = indep_vars.strip(op)
    return str.format("%s ~ %s" % (dep_var, indep_vars))


if __name__ == '__main__':
    main()
