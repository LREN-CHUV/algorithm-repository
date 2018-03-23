[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--sgd-regression-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-knn/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-knn.svg)](https://hub.docker.com/r/hbpmip/python-knn/tags "hbpmip/python-knn image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-knn.svg)](https://microbadger.com/#/images/hbpmip/python-knn "hbpmip/python-knn on microbadger")

# Python k-nearest neighbors

Implementation of [k-nearest neighbors algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) in Python.

Number of neighbors is parametrized using env `MODEL_PARAM_n_neighbors`.


## Usage

Works only on single node yet.

`compute`


## Build (for contributors)

Run: `./build.sh`


## Integration Test (for contributors)

Run: `captain test`


## Publish (for contributors)

Run: `./publish.sh`


## Unit tests (for contributors)

WARNING: unit tests can fail nondeterministically on `AttributeError: can't set attribute` because of some error
in Titus port to Python 3

Create symlink from `python-knn` to `mip_helper` module from `python-mip`
```
ln -s ~/projects/python-base-docker-images/python-mip/mip_helper/mip_helper mip_helper
```
Run unit tests
```
find . -name \*.pyc -delete
(cd tests; docker-compose run test_suite -x --ff --capture=no)
```
