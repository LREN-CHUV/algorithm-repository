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

# Fetch the data
y <- fetchData();

listStats <- lapply(y[,'data'], fromJSON)
listStats <- lapply(listStats, as.data.frame)

# Perform the computation
results <- unlist(dbGetQuery(conn, paste("select ", input_result_columns, "from ", input_table, " where request_id = ?"), request_id))
names(results) <- c('beta1','beta2','Sigma1','Sigma2')

res <- do.call(LRegress_Federation, as.list(results))
n <- length(results)

betas <- results[seq(1, n / 2)]
sigmas <- results[seq(n / 2 + 1, n)]

betas_arr <- paste('{', paste(betas, collapse=','), '}', sep='')
sigmas_arr <- paste('{', paste(sigmas, collapse=','), '}', sep='')

# Store results in the database
saveResults(as.data.frame(globalStats));
