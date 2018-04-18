[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--linear-regression-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-linear-regression/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-linear-regression.svg)](https://hub.docker.com/r/hbpmip/python-linear-regression/tags "hbpmip/python-linear-regression image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-linear-regression.svg)](https://microbadger.com/#/images/hbpmip/python-linear-regression "hbpmip/python-linear-regression on microbadger")

# Python linear-regression

Python implementation of multivariate linear regression. It supports both nominal and categorical variables and implicitly
drop null values in data. Both single-node and distributed mode return JSON with structure such as
```
{
    'agegroup_50-59y': {
        'coef': 3.2571304466,
        'p_values': 0.7387901953,
        'std_err': 9.5993224941,
        't_values': 0.3393083677
    },
    'intercept': {
        'coef': 1042.2837545842,
        'p_values': 0.0,
        'std_err': 45.1479998776,
        't_values': 23.0859342033
    },
    ...
}
```

## Single-node mode

Regression coefficients and statistics are calculated using [statsmodels](http://www.statsmodels.org/dev/index.html) package.

### Usage

`docker run python-linear-regression compute`


## Distributed mode

Aggregation mode pools the local betas and XtX matrices, constructs normal equations from these blocks and uses them
to calculate aggregated betas (see original [R implementation](https://github.com/LREN-CHUV/hbplregress/blob/master/R/LRegress_group.R)).
Calculated betas are identical to the single-node mode, however standard errors, t-statistics
and p-values are estimated from the local standard errors and might differ from the single-node case. This is because we
do not have residuals available in the aggregation step and therefore cannot compute standard error of the residuals.
In order to do that, we would have to propagate aggregate betas back to nodes, recalculate standard error there and
perform one more aggregation step.


### Usage

It has two modes

1. `compute --mode intermediate`
2. `compute --mode aggregate --job-ids 1 2 3`

Intermediate mode returns the same output as a single-node mode and aggregate mode combines these outputs into single
estimate.


## Build (for contributors)

Run: `./build.sh`


## Test (for contributors)

Run: `./tests/test.sh`


## Publish (for contributors)

Run: `./publish.sh`
