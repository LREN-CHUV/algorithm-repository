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

import matplotlib
matplotlib.use("Agg")

from mip_helper import io_helper, utils, errors, shapes

import logging
import numpy as np
import io
import argparse
import shap
import matplotlib.pyplot as plt
from titus.genpy import PFAEngine


DEFAULT_DOCKER_IMAGE = "python-feature-importance"

# Configure logging
logging.basicConfig(level=logging.INFO)


@utils.catch_user_error
def main(job_id):
    # Read inputs
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    X = io_helper.fetch_dataframe(variables=indep_vars)

    if utils.is_nominal(dep_var):
        raise errors.UserError('SHAP does not work for classification yet.')

    # Load PFA
    results = io_helper.load_intermediate_json_results([job_id])
    if not results:
        raise errors.UserError('Job {} does not exist.'.format(job_id))
    engine, = PFAEngine.fromJson(results[0])

    # Prediction function
    columns = X.columns
    int_columns = list(X.columns[X.dtypes == int])

    def _predict(X):
        pred = []
        for row in X:
            d = dict(zip(columns, row))
            for c in int_columns:
                d[c] = int(d[c])

            pred.append(engine.action(d))

        return np.array(pred)

    # use Kernel SHAP to explain test set predictions
    explainer = shap.KernelExplainer(_predict, X)
    shap_values = explainer.shap_values(X, nsamples=100)

    shap.summary_plot(shap_values, X, show=False)
    f = io.StringIO()
    plt.savefig(f, format="svg", bbox_inches='tight', dpi=None)
    f.seek(0)
    svg = f.read().strip()

    # Store results
    io_helper.save_results(svg, shapes.Shapes.SVG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('compute', choices=['compute'])
    parser.add_argument('--mode', choices=['single'], default='single')
    parser.add_argument('--job-id', type=str, required=True)

    args = parser.parse_args()

    # > compute --job-id 42
    if args.mode == 'single':
        main(args.job_id)
