#'
#' This script computes the ggplot object for parallel coordinates plot.
#' The data (input parameters: variables, covariables, grouping) are obtained from the local databases using a specific query.
#' This query will be the same for all nodes.
#'
#' #' Environment variables:
#' - Input Parameters:
#'      PARAM_query  : SQL query producing the dataframe to analyse
#'      PARAM_variables : Column separated list of variables, only the first variable will be used
#'      PARAM_covariables : Column separated list of covariables
#'      PARAM_grouping : Column separated list of groupings
#' - Execution context:
#'      JOB_ID : ID of the job
#'      NODE : Node used for the execution of the script
#'      IN_DBI_DRIVER   : Class name of the DBI driver for input data
#'      IN_DBI_DBNAME     : Database name for the database connection for input data
#'      IN_DBI_HOST     : Host name for the database connection for input data
#'      IN_DBI_PORT     : Port number for the database connection for input data
#'      IN_DBI_PASSWORD : Password for the database connection for input data
#'      IN_DBI_USER     : User for the database connection for input data
#'      OUT_DBI_DRIVER   : Class name of the DBI driver for output data
#'      OUT_DBI_DBNAME     : Database name for the database connection for output data
#'      OUT_DBI_HOST     : Host name for the database connection for output data
#'      OUT_DBI_PORT     : Port number for the database connection for output data
#'      OUT_DBI_USER     : User for the database connection for output data
#'      OUT_DBI_PASSWORD : Password for the database connection for output data

library(rmipadaptor)
library(magrittr)
library(ggplot2)
library(svglite)
library(ggparci)

# Initialisation
env_vars_names <- c("PARAM_variables",
                    "PARAM_covariables",
                    "PARAM_grouping",
                    "PARAM_query")

vars_names_r <- substring(text = env_vars_names,first = 7)

vars_list <- env_vars_names %>%
  # read the specified variables into a character
  Sys.getenv() %>%
  # split each string and output a list of character vectors
  strsplit(split = ",")

# assign in the global evviroment (or you can use attach(vars_list))
lapply(seq_along(vars_list),
       function(x) {
         assign(vars_names_r[x], vars_list[[x]], envir=.GlobalEnv)
       }
)

docker_image <- Sys.getenv("DOCKER_IMAGE", "hbpmip/r-ggparci:latest");
data   <- fetchData();
qp <- ggparci(x = data, group = variables)
blob <- stringSVG(grid::grid.draw(qp))
saveResults(results =  blob,shape = "svg")
disconnectdbs()
