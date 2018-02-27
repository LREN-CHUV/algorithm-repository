[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%r--3c-008bb8.svg)](https://hub.docker.com/r/hbpmip/r-3c) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/r-3c.svg)](https://hub.docker.com/r/hbpmip/r-3c/tags "hbpmip/r-3c image tags") [![](https://images.microbadger.com/badges/version/hbpmip/r-3c.svg)](https://microbadger.com/images/hbpmip/r-3c "Get your own version badge on microbadger.com") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/r-3c.svg)](https://microbadger.com/#/images/hbpmip/r-3c "hbpmip/r-3c on microbadger")

# 3c Docker for MIP

## Usage

```sh

  docker run --rm --env [list of environment variables] hbpmip/r-3c:latest compute

```

where the environment variables are:

* Input Parameters (for 3c):  
   - PARAM_query  : SQL query producing the dataframe to analyse  
   - PARAM_variables : The variables to pass to y1 (Disease Diagnosis)
   - PARAM_covariables1 : The variables to pass to X1 (Clinical Measures)
   - PARAM_covariables2 : The variables to pass to X2 (Potential Biomarkers)
   - PARAM_* : any other parameters to pass to the R function. See example in the docker-compose file.
* Execution context:  
   - JOB_ID : ID of the job  
   - NODE : Node used for the execution of the script  
   - IN_DBI_DRIVER   : Class name of the DBI driver for input data  
   - IN_DBI_DBNAME     : Database name for the database connection for input data  
   - IN_DBI_HOST     : Host name for the database connection for input data  
   - IN_DBI_PORT     : Port number for the database connection for input data  
   - IN_DBI_PASSWORD : Password for the database connection for input data  
   - IN_DBI_USER     : User for the database connection for input data  
   - OUT_DBI_DRIVER   : Class name of the DBI driver for output data  
   - OUT_DBI_DBNAME     : Database name for the database connection for output data  
   - OUT_DBI_HOST     : Host name for the database connection for output data  
   - OUT_DBI_PORT     : Port number for the database connection for output data  
   - OUT_DBI_USER     : User for the database connection for output data  
   - OUT_DBI_PASSWORD : Password for the database connection for output data  

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
  docker build -t hbpmip/r-3c .
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