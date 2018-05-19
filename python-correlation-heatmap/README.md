[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--summary--statistics-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-correlation-heatmap/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-correlation-heatmap.svg)](https://hub.docker.com/r/hbpmip/python-correlation-heatmap/tags "hbpmip/python-correlation-heatmap image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-correlation-heatmap.svg)](https://microbadger.com/#/images/hbpmip/python-correlation-heatmap "hbpmip/python-correlation-heatmap on microbadger")

# Python Correlation Heatmap

Calculate correlation heatmap, only works for **real variables**.

You can run it on single node with `compute` and env variable `MODEL_PARAM_graph=correlation_heatmap`.

1. `compute`

Or in a distributed mode with

1. `compute --mode intermediate`
2. `compute --mode aggregate --job-ids 1 2 3`

Intermediate mode calculates covariance matrix from a single node, while aggregate mode is used after intermediate to
combine statistics from multiple jobs and produce the final graph.


# Python Distributed PCA

Calculate PCA and return biplot visualization and screeplot. It only works for **real variables**.

You can run it on single node with `compute` and env variable `MODEL_PARAM_graph=pca`.

1. `compute`

Or in a distributed mode with

1. `compute --mode intermediate`
2. `compute --mode aggregate --job-ids 1 2 3`

<!--
Proposal for distributed mode with PCA scores graph included. See https://trello.com/c/jfLav9K6/58-distributed-pca for
discussion
1. `compute --mode intermediate` (calculate covariance matrices on nodes)
2. `compute --mode aggregate --job-ids 1 2 3` (calculate aggregated correlation matrix)
3. `compute --mode intermediate --agg-job-id 4` (calculate covariance matrices and also sample scores for PCA)
4. `compute --mode aggregate --job-ids 5 6 7 --graph pca` (produce plotly visualization) -->


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
