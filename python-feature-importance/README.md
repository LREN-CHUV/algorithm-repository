[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--feature-importance-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-feature-importance/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-feature-importance.svg)](https://hub.docker.com/r/hbpmip/python-feature-importance/tags "hbpmip/python-feature-importance image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-feature-importance.svg)](https://microbadger.com/#/images/hbpmip/python-feature-importance "hbpmip/python-feature-importance on microbadger")

# Python feature-importance

## Single-node mode

Calculate feature importance for arbitrary model using [SHAP](https://github.com/slundberg/shap).

### Usage

`docker run python-feature-importance compute`


## Distributed mode

Not implemented yet.


## Build (for contributors)

Run: `./build.sh`


## Test (for contributors)

Run: `./tests/test.sh`


## Publish (for contributors)

Run: `./publish.sh`
