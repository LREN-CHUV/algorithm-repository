[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--rapidminer--knn-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-knn/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-rapidminer-knn.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-knn/tags "hbpmip/java-rapidminer-knn image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-rapidminer-knn.svg)](https://microbadger.com/#/images/hbpmip/java-rapidminer-knn "hbpmip/java-rapidminer-knn on microbadger")

# java-rapidminer-knn

Implementation of the KNN algorithm using RapidMiner

## Usage

```
  docker run --rm hbpmip/java-rapidminer-knn:0.0.1 compute

```

## Development process

The goal of this project is to create a Docker image containing the full R environment capable of:

1. Read parameters from the environment and connect to a database
2. Query the database and prepare the data
3. Run the algorithm
4. Format the results into a format that can be easily shared. We are using the [PFA format](http://dmg.org/pfa/) here in its YAML form. It will get translated to JSON automatically be the workflow application which provides web services which execute this Docker container.
5. Save the results into the result database.

The Docker image should contain the binaries for the algorithm as well as all libraries and files that the algorithm depends on.

The following scripts are provided to help you:

### `./build.sh`

The main build script, it packages this project into a Docker image and performs the tests.
It requires [captain](https://github.com/harbur/captain) and [Docker engine](https://www.docker.com/) to run. If you cannot install captain on your platform, you may use the following commands to build the project:

```
  docker build -t hbpmip/java-rapidminer-knn .
  ./tests/test.sh
```

### `./tests/test.sh`

This script performs the tests. It assumes that the image has been built before using ./build.sh

It executes the Docker image and starts an input database and a result database.

Command to launch the tests:

```
  ./tests/test.sh
```

### `./publish.sh`

Publish a new version of the algorithm packaged in a Docker image to Docker hub

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
