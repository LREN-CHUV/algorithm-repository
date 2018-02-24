[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--pct--ts-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct-ts/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-pct-ts.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct-ts/tags "hbpmip/java-jsi-clus-pct-ts image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-pct-ts.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-pct-ts "hbpmip/java-jsi-clus-pct-ts on microbadger")

# hbpmip/java-jsi-clus-pct-ts: Predictive Clustering Trees (PCTs) for time-series prediction from JSI

Implementation of the Predictive Clustering Trees capable of time-series prediction. http://kt.ijs.si

## Usage

```sh
  docker run --rm --env [list of environment variables] hbpmip/java-jsi-clus-pct-ts compute
```

where the environment variables are:

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
* PARAM_variables: List of target variables
* PARAM_covariables: List of input variables
* PARAM_query: Query selecting the data to feed into the algorithm for training
* PARAM_MODEL_pruned: PCTs can be pruned or not. Use PARAM_MODEL_pruned=yes to prune and PARAM_MODEL_pruned=no otherwise (default is PARAM_MODEL_pruned=yes)
* PARAM_MODEL_minobj: Specify minimal number of examples in leaf nodes of the PCT (default is PARAM_MODEL_minobj=2)
