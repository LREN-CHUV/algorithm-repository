[![TAU](https://img.shields.io/badge/TAU-ICTAF-AD2C32.svg)](http://ictaf.tau.ac.il/index.asp?lang=eng) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%r--ggparci-008bb8.svg)](https://hub.docker.com/r/hbpmip/r-ggparci) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/r-ggparci.svg)](https://hub.docker.com/r/hbpmip/r-ggparci/tags "hbpmip/r-ggparci image tags") [![](https://images.microbadger.com/badges/version/hbpmip/r-ggparci.svg)](https://microbadger.com/images/hbpmip/r-ggparci "Get your own version badge on microbadger.com") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/r-ggparci.svg)](https://microbadger.com/#/images/hbpmip/r-ggparci "hbpmip/r-ggparci on microbadger")

# ggparci Docker for MIP

## Usage

```sh

  docker run --rm --env [list of environment variables] hbpmip/r-ggparci:0.2.2 compute

```

where the environment variables are:

* Input Parameters (for ggparci):
   - PARAM_query  : SQL query producing the dataframe to analyse
   - PARAM_variables : the grouping variable
   - PARAM_covariables : The variables to be ploted in the parallel coordinates plot.
* Execution context:
   - JOB_ID : ID of the job
   - NODE : Node used for the execution of the script
   - IN_DBI_DRIVER   : Class name of the DBI driver for input data
   - IN_DATABASE     : Database name for the database connection for input data
   - IN_HOST         : Host name for the database connection for input data
   - IN_PORT         : Port number for the database connection for input data
   - IN_PASSWORD     : Password for the database connection for input data
   - IN_USER         : User for the database connection for input data
   - OUT_DBI_DRIVER  : Class name of the DBI driver for output data
   - OUT_DATABASE    : Database name for the database connection for output data
   - OUT_HOST        : Host name for the database connection for output data
   - OUT_PORT        : Port number for the database connection for output data
   - OUT_USER        : User for the database connection for output data
   - OUT_PASSWORD    : Password for the database connection for output data

## Development process

The goal of this project is to create a Docker image containing the full R environment capable of:

1. Read parameters from the environment and connect to a database
2. Query the database and prepare the data
3. Run the algorithm
4. Format the results into a format that can be easily shared. Here, svg or html.
5. Save the results into the result database.

The Docker image contains an R script at `/src/main.R` as well as all libraries and files that this script depends on.

The following scripts are provided to help you:

### `./build.sh`

The main build script, it packages this project into a Docker image and performs the tests.
It requires [captain](https://github.com/harbur/captain) and [Docker engine](https://www.docker.com/) to run. If you cannot install captain on your platform, you may use the following commands to build the project:

```
  captain build
  # or
  docker build -t hbpmip/r-ggparci .
```

### `./dev.sh`

This script provides R runtime executed inside a Docker container. It also starts an input database and a result database.

<!-- To develop the main.R script, you should type the following in the R shell:
```
  library(devtools)
  devtools::install_github("LREN-CHUV/hbplregress")
  source(\"/src/main.R\")
```
 -->
### `./tests/test.sh`

This script performs the tests. It assumes that the image has been built before using ./build.sh

It executes the Docker image, starts an input database and a result database, then executes the algorithm using sample data for training.

You can run the tests with the command:

```
  ./tests/test.sh
```
