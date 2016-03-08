#'
#' Computes the summary statistics.
#' The data are obtained from the local databases using a specific query.
#' This query will be the same for all nodes.
#'
#' Environment variables:
#'
#' - Input Parameters:
#'      PARAM_query  : SQL query producing the dataframe to analyse
#'      PARAM_varnames : Column separated list of variables
#'      PARAM_covarnames : Column separated list of covariables
#'      PARAM_groups : Column separated list of groups
#' - Execution context:
#'      JOB_ID : ID of the job
#'      NODE : Node used for the execution of the script
#'      IN_JDBC_DRIVER : class name of the JDBC driver for input data
#'      IN_JDBC_JAR_PATH : path to the JDBC driver jar for input data
#'      IN_JDBC_URL : JDBC connection URL for input data
#'      IN_JDBC_USER : User for the database connection for input data
#'      IN_JDBC_PASSWORD : Password for the database connection for input data
#'      OUT_JDBC_DRIVER : class name of the JDBC driver for output results
#'      OUT_JDBC_JAR_PATH : path to the JDBC driver jar for output results
#'      OUT_JDBC_URL : JDBC connection URL for output results
#'      OUT_JDBC_USER : User for the database connection for output results
#'      OUT_JDBC_PASSWORD : Password for the database connection for output results
#'

suppressMessages(library(hbpjdbcconnect));
library(jsonlite);
library(whisker);
library(hbpsummarystats);

# Initialisation
varnames <- strsplit(Sys.getenv("PARAM_varnames"), ",");
covarnames <- strsplit(Sys.getenv("PARAM_covarnames"), ",");
groupstr <- Sys.getenv("PARAM_groups", "");
if (groupstr == "") {
    groups <- c();
} else {
    groups <- strsplit(Sys.getenv("PARAM_groups", ""), ",");
}
docker_image <- Sys.getenv("DOCKER_IMAGE", "hbpmip/r-summary-stats:latest");

columns <- c(varnames, covarnames, groups);

# Fetch the data
data <- fetchData();

# Perform the computation
res <- tablesummarystats(data, columns);

# Ensure that we use only supported types: list, string
store <- list();

template <- readLines("/src/pfa.yml");

# Store results in the database
saveResults(whisker.render(template, store), fn = 'r-summary-stats', shape = 'pfa_yaml');
