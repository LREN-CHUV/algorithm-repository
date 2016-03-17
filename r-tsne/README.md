# r-tsne

Implementation of a linear regression in R

## Development process

The goal of this project is to create a Docker image containing the full R environment capable of:

1. Read parameters from the environment and connect to a database
2. Query the database and prepare the data
3. Run the algorithm (here, a linear regression)
4. Format the results into a format that can be easily shared. We are using the [PFA format](http://dmg.org/pfa/) here in its YAML form. It will get translated to JSON automatically be the workflow application which provides web services which execute this Docker container.
5. Save the results into the result database.

The Docker image should contain a R script at /src/main.R as well as all libraries and files that this script depends on.

The following scripts are provided to help you:

### `./build.sh`

The main build script, it packages this project into a Docker image and performs the tests.
It requires [captain](https://github.com/harbur/captain) and [Docker engine](https://www.docker.com/) to run. If you cannot install captain on your platform, you may use the following commands to build the project:

```
  docker build -t hbpmip/r-tsne .
  ./tests/test.sh
```

### `./dev.sh`

This script provides a R runtime executed inside a Docker container. It also starts an input database and a result database.

To develop the main.R script, you should type the following in the R shell:
```
  library(devtools)
  devtools::install_github("LREN-CHUV/hbplregress")
  source(\"/src/main.R\")
```

### `./tests/test.sh`

This script performs the tests. It assumes that the image has been built before using ./build.sh

It executes the Docker image and starts an input database and a result database.

You can run the tests interactively using this environment with the command

```
  ./tests/test.sh --interactive
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
