[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--fr-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fr/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-fr.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fr/tags "hbpmip/java-jsi-clus-fr image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-fr.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-fr "hbpmip/java-jsi-clus-fr on microbadger")

# hbpmip/java-jsi-clus-fr: Feature ranking for structured outputs

Implementation of the feature ranking from CLUS software. http://kt.ijs.si

## Usage

```sh
docker run --rm --env [list of environment variables] hbpmip/java-jsi-clus-fr compute
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
* PARAM_MODEL_size: How many models should the ensemble contain. (default is MODEL_PARAM_size=100)