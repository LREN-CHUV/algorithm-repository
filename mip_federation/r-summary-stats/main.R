#
# XXX This script computes the linear regression.
# XXX The data (input parameters: y, A) are obtained from the local databases using a specific query.
# XXX These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_query  : SQL query producing the dataframe to analyse
# - Execution context:
#      REQUEST_ID : ID of the incoming request
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

# Fetch the data
y <- fetchData();


# Perform the computation
res <- tablesummarystats_group(y);

result_table <- Sys.getenv("RESULT_TABLE", "result_summary_stats");

# Store results in the database
saveResults(res);
