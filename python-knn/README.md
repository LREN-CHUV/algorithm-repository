[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--sgd-regression-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-knn/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-knn.svg)](https://hub.docker.com/r/hbpmip/python-knn/tags "hbpmip/python-knn image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-knn.svg)](https://microbadger.com/#/images/hbpmip/python-knn "hbpmip/python-knn on microbadger")

# Python distributed k-means clustering

Implementation of [distributed k-means clustering](https://github.com/MRN-Code/dkmeans) in Python. It uses
[Single-Shot Decentralized LLoyd](https://github.com/MRN-Code/dkmeans#single-shot-decentralized-lloyd).

Clustering is parametrized using env `MODEL_PARAM_n_clusters`, but the final number of clusters is also influenced
by the number of nodes - total number of output clusters is `floor(n_clusters * n_nodes / 2)`.


## Usage

It has two modes

1. `compute --mode intermediate`
2. `compute --mode aggregate --job-ids 1 2 3`

Intermediate mode calculates clusters on a single node, while aggregate mode is merging the clusters according
to least merging error (e.g. smallest distance between centroids).


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
