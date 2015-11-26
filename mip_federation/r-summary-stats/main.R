#
# Computes the summary statistics at the federation level.
# Data comes from the intermediate statistics gathered on each local nodes.
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

library(hbpsummarystats);
library(hbpjdbcconnect);
library(jsonlite);

# Fetch the data
y <- fetchData();

listStats <- lapply(y[,'data'], fromJSON)
listStats <- lapply(listStats, as.data.frame)

# Perform the computation
globalStats <- tablesummarystats_group(listStats);

# Store results in the database
saveResults(as.data.frame(globalStats));
