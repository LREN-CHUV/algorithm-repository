#
# This script computes the linear regression.
# The data (input parameters: y, A) are obtained from the local databases using a specific query.
# These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_query  : SQL query producing the dataframe to analyse
#      PARAM_varname : Name of the variable
#      PARAM_covarnames : Column separated list of covariables
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

# Initialisation
varname <- Sys.getenv("PARAM_varname");
covarnames <- strsplit(Sys.getenv("PARAM_covarnames"), ",");

# Fetch the data
data <- fetchData();

# Convert all strings to factors
data[sapply(data, is.character)] <- lapply(data[sapply(data, is.character)], 
                                       as.factor)

# Perform the computation
res <- LRegress_Node(data, varname, covarnames);

res <- list(beta = res[[1]], sigma = res[[2]]);

# Store results in the database
saveResults(res);
