[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--rapidminer--naivebayes-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-naivebayes/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-rapidminer-knn.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-knn/tags "hbpmip/java-rapidminer-knn image tags") [![](https://images.microbadger.com/badges/version/hbpmip/java-rapidminer-naivebayes.svg)](https://microbadger.com/images/hbpmip/java-rapidminer-naivebayes "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/hbpmip/java-rapidminer-naivebayes.svg)](https://microbadger.com/images/hbpmip/java-rapidminer-naivebayes "Get your own image badge on microbadger.com")

# java-rapidminer-naivebayes

Implementation of the [Naive Bayes classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) algorithm using RapidMiner

## Usage

```sh

  docker run --rm --env [list of environment variables] hbpmip/java-rapidminer-naivebayes:0.2.1 compute

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
* PARAM_variables: Name of the target variable (only one variable is supported for KNN)
* PARAM_covariables: List of covariables
* PARAM_query: Query selecting the variables and covariables to feed into the algorithm for training.

## Development process

The goal of this project is to create a Docker image containing the full R environment capable of:

1. Read parameters from the environment and connect to a database
2. Query the database and prepare the data
3. Run the algorithm (here, Naive Bayes)
4. Format the results into a format that can be easily shared. We are using the [PFA format](http://dmg.org/pfa/) here in its JSON form.
5. Save the results into the result database.

The Docker image should contain the binaries and resources that this algorithm depends on.

The following scripts are provided to help you:

### `./build.sh`

The main build script, it packages this project into a Docker image and performs the tests.
It requires [captain](https://github.com/harbur/captain) and [Docker engine](https://www.docker.com/) to run. If you cannot install captain on your platform, you may use the following commands to build the project:

```
  captain build
  # or
  docker build -t hbpmip/java-rapidminer-naivebayes .
```

### `./tests/test.sh`

This script performs the tests. It assumes that the image has been built before using ./build.sh

It executes the Docker image, starts an input database and a result database, then executes the algorithm using sample data for training.

You can run the tests with the command:

```
  ./tests/test.sh
```

## Validation of the PFA output

Install Titus from [OpenDatagroup Hadrian](https://github.com/opendatagroup/hadrian/wiki/Installation#case-4-you-want-to-install-titus-in-python)

Titus provides a tool called [pfainspector](https://github.com/opendatagroup/hadrian/wiki/Titus-pfainspector)

Check the validity of the PFA output of this algorithm with the following procedure:

* Read the yaml document from the database ('data' column)
* Convert the document from YAML to JSON, for example using [yamltojson.com](http://yamltojson.com)
* Start pfainspector
* Load the json
```
  load lreg_output.json as lreg_output
```
* Validate the json
```
  pfa validate lreg_output
```
