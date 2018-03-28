[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--summary--statistics-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-correlation-heatmap/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-correlation-heatmap.svg)](https://hub.docker.com/r/hbpmip/python-correlation-heatmap/tags "hbpmip/python-correlation-heatmap image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-correlation-heatmap.svg)](https://microbadger.com/#/images/hbpmip/python-correlation-heatmap "hbpmip/python-correlation-heatmap on microbadger")

# Python Correlation Heatmap

Calculate correlation heatmap, only works for **real variables**.

You can run it on single node with `compute` or in a distributed way with

1. `compute --mode intermediate`
2. `compute --mode aggregate --job-ids 1 2 3`

Intermediate mode calculates covariance matrix from a single node, while aggregate mode is used after intermediate to
combine statistics from multiple jobs.


## Build (for contributors)

Run: `./build.sh`


## Integration Test (for contributors)

Run: `captain test`


## Publish (for contributors)

Run: `./publish.sh`


## Unit tests (for contributors)

Run unit tests
```
find . -name \*.pyc -delete
(cd tests; docker-compose run test_suite -x --ff --capture=no)
```
