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

import argparse
import logging
import json

from pandas import DataFrame
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

DESIGN_PARAM = "design"
DEFAULT_DESIGN = "factorial"
MAX_FACTORIAL_COVARIABLES = 8

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

    # Check dependent variable type (should be continuous)
    if utils.is_nominal(dep_var):
        raise errors.UserError('Dependent variable should be continuous!')

    # Extract data and parameters from inputs
    data = format_data(inputs["data"])

    # Compute anova
    anova_results = format_output(compute_anova(dep_var, inped_vars, data, design).to_dict())

    # Store results
    io_helper.save_results(anova_results, Shapes.JSON)


def format_data(input_data):
    all_vars = input_data["dependent"] + input_data["independent"]
    data = {v["name"]: v["series"] for v in all_vars}
    return data


def format_output(statsmodels_dict):
    return json.dumps(DataFrame.from_dict(statsmodels_dict).transpose().fillna("NaN").to_dict())


def compute_anova(dep_var, indep_vars, data, design='factorial'):
    formula = generate_formula(dep_var, indep_vars, design)
    logging.info("Formula: %s" % formula)
    data = DataFrame(data)

    if data.empty:
        raise errors.UserError('SQL returned no data, check your dataset and null values.')

    lm = ols(data=data, formula=formula).fit()
    logging.info(lm.summary())

    if lm.df_resid == 0:
        raise errors.UserError(
            'Too many factors ({}) for too little data ({}). Use less covariables or different design.'.format(
                len(lm.params), len(data)
            )
        )

    return anova_lm(lm)


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

    terms = []
    for var in indep_vars:
        if utils.is_nominal(var):
            terms.append("C({}, levels={})".format(var["name"], var['type']['enumeration']))
        else:
            terms.append(var['name'])

    return "{} ~ {}".format(dep_var["name"], op.join(terms))


if __name__ == '__main__':
    import distributed_anova

    parser = argparse.ArgumentParser()
    parser.add_argument('compute', choices=['compute'])
    parser.add_argument(
        '--mode',
        choices=['single', 'intermediate-models', 'aggregate-models', 'intermediate-anova', 'aggregate-anova'],
        default='single'
    )
    parser.add_argument('--job-ids', type=str, nargs="*", default=[])

    args = parser.parse_args()

    # > compute
    if args.mode == 'single':
        main()
    # > compute --mode intermediate-models
    elif args.mode == 'intermediate-models':
        distributed_anova.intermediate_models()
    # > compute --mode aggregate-models --job-ids 1 2 3
    elif args.mode == 'aggregate-models':
        distributed_anova.aggregate_models(args.job_ids)
    # > compute --mode intermediate-anova --job-ids 4
    elif args.mode == 'intermediate-anova':
        distributed_anova.intermediate_anova(args.job_ids)
    # > compute --mode aggregate-anova --job-ids 5 6 7
    elif args.mode == 'aggregate-anova':
        distributed_anova.aggregate_anova(args.job_ids)
