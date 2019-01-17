#!/usr/bin/env python3
# Copyright (C) 2017  LREN CHUV for Human Brain Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from mip_helper import io_helper, errors, utils, parameters
from mip_helper.shapes import Shapes

import logging
import json

from pandas import DataFrame
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

DESIGN_PARAM = "design"
DEFAULT_DESIGN = "factorial"
MAX_FACTORIAL_COVARIABLES = 8
ANOVA_TYPE_PARAM = "type"
ANOVA_TYPE_DEFAULT = "III"

DEFAULT_DOCKER_IMAGE = "python-anova"


@utils.catch_user_error
def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    inped_vars = inputs["data"]["independent"]
    design = parameters.get_parameter(DESIGN_PARAM, str, DEFAULT_DESIGN)
    anova_type = parameters.get_parameter(ANOVA_TYPE_PARAM, str, ANOVA_TYPE_DEFAULT)

    # Check dependent variable type (should be continuous)
    if dep_var["type"]["name"] not in ["integer", "real"]:
        raise errors.UserError('Dependent variable should be continuous!')

    # Extract data and parameters from inputs
    data = format_data(inputs["data"])

    # Compute anova and generate PFA output
    anova_results = format_output(compute_anova(dep_var, inped_vars, data, design, anova_type).to_dict())
    
    #logging.info(anova_results)  
    # Store results
    io_helper.save_results(anova_results, Shapes.JSON)


def format_data(input_data):
    all_vars = input_data["dependent"] + input_data["independent"]
    data = {v["name"]: v["series"] for v in all_vars}
    return data


def format_output(statsmodels_dict):
    return json.dumps(DataFrame.from_dict(statsmodels_dict).transpose().fillna("NaN").to_dict())


def compute_anova(dep_var, indep_vars, data, design=DEFAULT_DESIGN, anova_type=ANOVA_TYPE_DEFAULT):
    formula = generate_formula(dep_var, indep_vars, design)
    logging.info("Formula: %s" % formula)
    data = DataFrame(data)

    if data.empty:
        raise errors.UserError('SQL returned no data, check your dataset and null values.')

    lm = ols(data=data, formula=formula).fit()
#    logging.info(lm.summary())

    if lm.df_resid == 0:
        raise errors.UserError(
            'Too many factors ({}) for too little data ({}). Use less covariables or different design.'.format(
                len(lm.params), len(data)
            )
        )

    return anova_lm(lm, type = anova_type)


def generate_formula(dep_var, indep_vars, design):
    if design == 'additive':
        op = " + "
    elif design == 'factorial':
        op = " * "
    else:
        raise errors.UserError("Invalid design parameter : %s" % design)

    if design == 'factorial' and len(indep_vars) >= MAX_FACTORIAL_COVARIABLES:
        raise errors.UserError(
            'You can use at most {} covariables with factorial design ({} was used)'.format(
                MAX_FACTORIAL_COVARIABLES, len(indep_vars)
            )
        )

    dep_var = dep_var["name"]
    indep_vars = [
        v["name"] if v["type"]["name"] in ["integer", "real"] else str.format("C(%s)" % v["name"]) for v in indep_vars
    ]
    indep_vars = op.join(indep_vars)
    indep_vars = indep_vars.strip(op)
    return str.format("%s ~ %s" % (dep_var, indep_vars))


if __name__ == '__main__':
    main()
