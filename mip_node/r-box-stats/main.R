#
# XXX This script computes the linear regression.
# XXX The data (input parameters: y, A) are obtained from the local databases using a specific query.
# XXX These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_query  : SQL query producing the dataframe to analyse
#      PARAM_colnames : Column separated list of columns to include in the stats
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
#      RESULT_TABLE: name of the result table, defaults to 'result_box_stats'
#

library(hbpboxstats)
library(hbpjdbcconnect)

# Initialisation
connect2indb()
request_id <- Sys.getenv("REQUEST_ID")
node <- Sys.getenv("NODE")
query <- Sys.getenv("PARAM_query")
columns <- Sys.getenv("PARAM_colnames")

# Fetch the data
y <- RJDBC::dbGetQuery(in_conn, query)

# Perform the computation
res <- tableboxstats(y, strsplit(columns, ","))

result_table <- Sys.getenv("RESULT_TABLE", "result_box_stats")

connect2outdb()

# Store results in the database
n <- ncol(res)
results <- data.frame(request_id = rep(request_id, n), node = rep(node, n), id = 1:n,
	               min = res['min',], q1 = res['q1',], median = res['median',], q3 = res['q3',], max = res['max',])

RJDBC::dbWriteTable(out_conn, result_table, results, overwrite=FALSE, append=TRUE, row.names = FALSE)

# Disconnect from the databases
disconnectdbs()
