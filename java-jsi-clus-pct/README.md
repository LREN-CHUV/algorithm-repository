[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--pct-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-pct.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct/tags "hbpmip/java-jsi-clus-pct image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-pct.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-pct "hbpmip/java-jsi-clus-pct on microbadger")

# hbpmip/java-jsi-clus-pct: Predictive Clustering Trees (PCTs) for multi-target prediction

Implementation of the Predictive Clustering Trees from CLUS software. http://kt.ijs.si

## Usage

```sh
docker run --rm --env [list of environment variables] hbpmip/java-jsi-clus-pct compute
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
* MODEL_PARAM_pruned: PCTs can be pruned or not. Use MODEL_PARAM_pruned=yes to prune and MODEL_PARAM_pruned=no otherwise (default is MODEL_PARAM_pruned=yes)
* MODEL_PARAM_minobj: Specify minimal number of examples in leaf nodes of the PCT (default is MODEL_PARAM_minobj=2)
