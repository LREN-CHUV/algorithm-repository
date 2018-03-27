[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--sgd-regression-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-sgd-regression/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-sgd-regression.svg)](https://hub.docker.com/r/hbpmip/python-sgd-regression/tags "hbpmip/python-sgd-regression image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-sgd-regression.svg)](https://microbadger.com/#/images/hbpmip/python-sgd-regression "hbpmip/python-sgd-regression on microbadger")

# Python sgd-regression

This is a Python implementation of [scikit-learn estimators](http://scikit-learn.org/stable/modules/scaling_strategies.html) that use `partial_fit` method for distributed learning.

Implemented methods:
- `linear_model` - calls `SGDRegressor` or `SGDClassifier`
- `neural_network` - calls `MLPRegressor` or `MLPClassifier`
- `naive_bayes` - calls `MixedNB` (mix of `GaussianNB` and `MultinomialNB`), only works for classification tasks


## Usage

It has two modes

```sh
docker run --rm --env [list of environment variables] hbpmip/python-sgd-regression:VERSION compute --mode partial --job-id 12
```

which calls `partial_fit` of scikit-learn estimator and saves intermediate results into `job_results` table. If
`--job-id` is specified, it will first load the estimator and continue its training. If not, it will start from scratch.

```sh
docker run --rm --env [list of environment variables] hbpmip/python-sgd-regression:VERSION compute --mode final --job-id 13
```

this mode in addition converts estimator into PFA. If you have only one node, calling `naive_bayes` with `compute final`
will be equivalent to running Naive Bayes in a non-distributed way.

Environment variables are:

* NODE: name of the node (machine) used for execution
* JOB_ID: ID of the job.
* IN_JDBC_DRIVER: org.postgresql.Driver
* IN_JDBC_URL: URL to the input database, e.g. jdbc:postgresql://db:5432/features
* IN_JDBC_USER: User for the input database
* IN_JDBC_PASSWORD: Password for the input database
* OUT_JDBC_DRIVER: org.postgresql.Driver
* OUT_JDBC_URL: URL to the output database, jdbc:postgresql://db:5432/woken
* OUT_JDBC_USER: User for the output database
* OUT_JDBC_PASSWORD: Password for the output database
* PARAM_variables: Name of the target variable (only one variable is supported for KNN)
* PARAM_covariables: List of covariables
* PARAM_query: Query selecting the variables and covariables to feed into the algorithm for training.
* MODEL_PARAM_type: Type of model to use, could be `linear_model`, `neural_network` or `naive_bayes`

Use additional `MODEL_PARAM_[sklearn_parameter]` envs to specify scikit-learn model parameters (e.g. `MODEL_PARAM_alpha`
  for Naive Bayes).


## Build (for contributors)

Run: `./build.sh`


## Integration Test (for contributors)

Run: `captain test`


## Publish (for contributors)

Run: `./publish.sh`


## Unit tests (for contributors)

Run: `./build.sh`

WARNING: unit tests can fail nondeterministically on `AttributeError: can't set attribute` because of some error
in Titus port to Python 3

Run integration tests:

```
  cd tests
  ./test.sh
```
