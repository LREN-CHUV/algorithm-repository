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

from mip_helper import io_helper, shapes
from sklearn_to_pfa.sklearn_to_pfa import sklearn_to_pfa
from sklearn_to_pfa.featurizer import Featurizer, Standardize, OneHotEncoding
from sklearn_to_pfa.mixed_nb import MixedNB

import logging
import json
import argparse

import pandas as pd
from sklearn.linear_model import SGDRegressor, SGDClassifier
from sklearn.neural_network import MLPRegressor, MLPClassifier
import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
jsonpickle_numpy.register_handlers()


# Configure logging
logging.basicConfig(level=logging.INFO)


DEFAULT_DOCKER_IMAGE = "python-sgd-regression"


def main(job_id, generate_pfa):
    inputs = io_helper.fetch_data()
    dep_var = inputs["data"]["dependent"][0]
    indep_vars = inputs["data"]["independent"]

    if dep_var['type']['name'] in ('polynominal', 'binominal'):
        job_type = 'classification'
    else:
        job_type = 'regression'

    # Get existing results with partial model if they exist
    if job_id:
        job_result = io_helper.get_results(job_id=str(job_id))

        logging.info('Loading existing estimator')
        estimator = deserialize_sklearn_estimator(job_result.data)
    else:
        logging.info('Creating new estimator')
        estimator = _create_estimator(job_type)

    # featurization
    transforms = []
    for var in indep_vars:
        if var['type']['name'] in ('integer', 'real'):
            transforms.append(Standardize(var['name'], var['mean'], var['std']))
        elif var["type"]["name"] in ['polynominal', 'binominal']:
            transforms.append(OneHotEncoding(var['name'], var['type']['enumeration']))

    # for NaiveBayes, continuous variables must go before nominal ones
    if isinstance(estimator, MixedNB):
        transforms = sorted(transforms, key=lambda x: not isinstance(x, Standardize))
        is_nominal = []
        for tf in transforms:
            if isinstance(tf, Standardize):
                is_nominal.append(False)
            elif isinstance(tf, OneHotEncoding):
                is_nominal += [True] * len(tf.enumerations)
        estimator.is_nominal = is_nominal

    featurizer = Featurizer(transforms)

    # convert variables into dataframe
    X, y = get_Xy(dep_var, indep_vars)
    X = featurizer.transform(X)

    # Drop NaN values
    # TODO: how should we treat NaNs?
    is_null = (pd.isnull(X).any(1) | pd.isnull(y)).values
    X = X[~is_null, :]
    y = y[~is_null]

    if len(X) == 0:
        logging.warning("All data are NULL, cannot fit model")
    else:
        # Train single step
        if job_type == 'classification':
            estimator.partial_fit(X, y, classes=dep_var['type']['enumeration'])
        else:
            estimator.partial_fit(X, y)

    serialized_estimator = serialize_sklearn_estimator(estimator)

    if generate_pfa:
        # Create PFA from the estimator
        types = [(var['name'], var['type']['name']) for var in indep_vars]
        pfa = sklearn_to_pfa(estimator, types, featurizer.generate_pretty_pfa())

        # Add serialized model as metadata
        pfa['metadata'] = {
            'estimator': serialized_estimator
        }

        # Save or update job_result
        logging.info('Saving PFA to job_results table')
        pfa = json.dumps(pfa)
        io_helper.save_results(pfa, '', shapes.Shapes.PFA)
    else:
        # Save or update job_result
        logging.info('Saving serialized estimator into job_results table')
        io_helper.save_results(serialized_estimator, '', shapes.Shapes.JSON)


def serialize_sklearn_estimator(estimator):
    """Serialize model to JSON, see https://cmry.github.io/notes/serialize for inspiration."""
    return jsonpickle.encode(estimator)


def deserialize_sklearn_estimator(js):
    """Deserialize model from JSON."""
    return jsonpickle.decode(js)


def _create_estimator(job_type):
    model_parameters = {x['name']: x['value']for x in io_helper._get_parameters()}
    model_type = model_parameters.pop('type', 'linear_model')

    if job_type == 'regression':
        if model_type == 'linear_model':
            estimator = SGDRegressor(**model_parameters)
        elif model_type == 'neural_network':
            estimator = MLPRegressor(**model_parameters)
        else:
            raise ValueError('Unknown model type {} for regression'.format(model_type))

    elif job_type == 'classification':
        if model_type == 'linear_model':
            estimator = SGDClassifier(**model_parameters)
        elif model_type == 'neural_network':
            estimator = MLPClassifier(**model_parameters)
        elif model_type == 'naive_bayes':
            estimator = MixedNB(**model_parameters)
        else:
            raise ValueError('Unknown model type {} for classification'.format(model_type))

    return estimator


def get_Xy(dep_var, indep_vars):
    """Create dataframe from input data.
    :param dep_var:
    :param indep_vars:
    :return: dataframe with data from all variables
    """
    df = {}
    for var in [dep_var] + indep_vars:
        # categorical variable - we need to add all categories to make one-hot encoding work right
        if 'enumeration' in var['type']:
            df[var['name']] = pd.Categorical(var['series'], categories=var['type']['enumeration'])
        else:
            # infer type automatically
            df[var['name']] = var['series']
    X = pd.DataFrame(df)
    y = X[dep_var['name']]
    del X[dep_var['name']]
    return X, y


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('compute', choices=['compute'])
    parser.add_argument('mode', choices=['partial', 'final'])
    parser.add_argument('--job-id', type=int)

    args = parser.parse_args()

    # > compute partial --job-id 12
    if args.mode == 'partial':
        main(args.job_id, generate_pfa=False)
    # > compute final --job-id 13
    elif args.mode == 'final':
        main(args.job_id, generate_pfa=True)
