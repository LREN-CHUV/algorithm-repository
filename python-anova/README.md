[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--anova-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-anova/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-anova.svg)](https://hub.docker.com/r/hbpmip/python-anova/tags "hbpmip/python-anova image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-anova.svg)](https://microbadger.com/#/images/hbpmip/python-anova "hbpmip/python-anova on microbadger")

# Python Anova

This is a Python implementation of Anova (Type I).


## Single-node mode

ANOVA is calculated using [statsmodels](http://www.statsmodels.org/dev/index.html) package.

### Usage

`docker run python-anova compute`


## Distributed mode

First we generate formula for ANOVA and pool XtX and Xty matrices from all nodes. Aggregation mode then calculates betas from aggregated XtX and Xty matrices for all submodels (intercept -> one feature -> ... -> full model). These betas are then distributed back to nodes to calculate [decomposition of sum of squares](https://en.wikipedia.org/wiki/Partition_of_sums_of_squares) for all submodels.

Finally, calculated sum of squares for all models from all nodes are aggregated again and ANOVA table is constructed.


### Usage

First calculate XtX and Xty for normal equations on all nodes with
```
compute --mode intermediate-models
```
then aggregate and create nested models on a single node
```
compute --mode aggregate-models --job-ids 1 2 3
```
and send it back to all nodes to make predictions
```
compute --mode intermediate-anova --job-id 4
```
finally aggregate again to produce final table
```
compute --mode aggregate-anova --job-ids 5 6 7
```


## Build (for contributors)

Run: `./build.sh`


## Test (for contributors)

Run: `./tests/test.sh`


## Publish (for contributors)

Run: `./publish.sh`
