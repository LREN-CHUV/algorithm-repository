#
# This script computes the linear regression.
# The data (input parameters: y, A) are obtained from the local databases using a specific query.
# These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_query  : SQL query producing the list of intermediate results to analyse
# - Execution context:
#      JOB_ID : ID of the job
#      NODE : Node used for the execution of the script
#      IN_JDBC_DRIVER : class name of the JDBC driver for input data
#      IN_JDBC_JAR_PATH : path to the JDBC driver jar for input data
#      IN_JDBC_URL : JDBC connection URL for input data
#      IN_JDBC_USER : User for the database connection for input data
#      IN_JDBC_PASSWORD : Password for the database connection for input data
#      OUT_JDBC_DRIVER : class name of the JDBC driver for output results
#      OUT_JDBC_JAR_PATH : path to the JDBC driver jar for output results
#      OUT_JDBC_URL : JDBC connection URL for output results
#      OUT_JDBC_USER : User for the database connection for output results
#      OUT_JDBC_PASSWORD : Password for the database connection for output results
#

library(hbplregress);
library(hbpjdbcconnect);
library(jsonlite);

Ndegree <- as.numeric(Sys.getenv("PARAM_ndegree", 99));

# Fetch the data
y <- fetchData();

data <- lapply(y[,'data'], fromJSON);
betas <- lapply(data, function (x) {x$beta});
sigmas <- lapply(data, function (x) {x$sigma});

# Perform the computation
res <- LRegress_Federation(betas, sigmas, Ndegree);

# Store results in the database
saveResults(res);
