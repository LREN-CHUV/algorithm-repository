[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--summary--statistics-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-summary-statistics/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-summary-statistics.svg)](https://hub.docker.com/r/hbpmip/python-summary-statistics/tags "hbpmip/python-summary-statistics image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-summary-statistics.svg)](https://microbadger.com/#/images/hbpmip/python-summary-statistics "hbpmip/python-summary-statistics on microbadger")

# Python Statistics

This is a Python implementation of Statistics. It calculates various summary statistics for entire dataset and
also for all subgroups created by combining all possible values of nominal covariates.

It has two modes

1. `compute --mode intermediate`
2. `compute --mode aggregate --job-ids 1 2 3`

Intermediate mode calculates statistics from a single node, while aggregate mode is used after intermediate to
combine statistics from multiple jobs. Intermediate mode can be also used to calculate statistics from single node.


## Build (for contributors)

Run: `./build.sh`


## Integration Test (for contributors)

Run: `captain test`


## Publish (for contributors)

Run: `./publish.sh`


## Unit tests (for contributors)

Create symlink from `python-summary-statistics` to `mip_helper` module from `python-mip`
```
ln -s ~/projects/python-base-docker-images/python-mip/mip_helper/mip_helper mip_helper
```
Run unit tests
```
find . -name \*.pyc -delete
(cd tests; docker-compose run test_suite -x --ff --capture=no)
```
