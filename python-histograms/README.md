[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--histograms-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-histograms/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-histograms.svg)](https://hub.docker.com/r/hbpmip/python-histograms/tags "hbpmip/python-histograms image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-histograms.svg)](https://microbadger.com/#/images/hbpmip/python-histograms "hbpmip/python-histograms on microbadger")

# Python Histograms

Calculates histogram of nominal or real variable grouped by nominal variables in independent variables. It ignores
null values. Histogram edges are taken from `minValue` and `maxValue` property of dependent variable. If not avaiable,
then these values are calculated dynamically from dependent values (this won't work in distributed mode though).


## Usage

It has two modes

1. `compute --mode intermediate`
2. `compute --mode aggregate --job-ids 1 2 3`

Intermediate mode calculates histograms from a single node, while aggregate mode is used after intermediate to
combine histograms from multiple jobs. Intermediate mode can be also used to calculate histograms from single node.


## Build (for contributors)

Run: `./build.sh`


## Integration Test (for contributors)

Run: `captain test`


## Publish (for contributors)

Run: `./publish.sh`


## Unit tests (for contributors)

```
Run unit tests
```
find . -name \*.pyc -delete
(cd tests; docker-compose run test_suite -x --ff --capture=no)
```
