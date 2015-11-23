#
# Computes the summary statistics.
# The data are obtained from the local databases using a specific query.
# This query will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_query  : SQL query producing the dataframe to analyse
#      PARAM_colnames : Column separated list of columns to include in the stats
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
#      RESULT_TABLE: name of the result table, defaults to 'result_summary_stats'
#

library(hbpsummarystats);
library(hbpjdbcconnect);
library(jsonlite);

# Initialisation
columns <- Sys.getenv("PARAM_colnames");

# Fetch the data
y <- fetchData();

# Perform the computation
res <- tablesummarystats(y, strsplit(columns, ","));

res <- as.data.frame(res);
ijson <- sapply(res, function(x) toJSON(x, auto_unbox=TRUE, digits=8));
df <- as.data.frame(ijson);
names(df) <- columns;

# Store results in the database
saveResults(toJSON(df));
