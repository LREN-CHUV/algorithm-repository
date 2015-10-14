#
# This script computes the linear regression.
# The data (input parameters: y, A) are obtained from the local databases using a specific query.
# These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_y  : SQL query producing the y parameter of L_Regress_Node
#      PARAM_A : SQL query producing the A parameter of L_Regress_Node
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
#      RESULT_TABLE: name of the result table, defaults to 'results_linear_regression'
#      RESULT_COLUMNS: list of columns for the result table, default to "request_id, node, param_y, param_a, result_betai, result_sigmai"
#

library(hbplregress)
library(RJDBC)

# Initialisation
drv <- JDBC(Sys.getenv("IN_JDBC_DRIVER"),
           Sys.getenv("IN_JDBC_JAR_PATH"),
           identifier.quote="`")
conn <- dbConnect(drv, Sys.getenv("IN_JDBC_URL"), Sys.getenv("IN_JDBC_USER"), Sys.getenv("IN_JDBC_PASSWORD"))
request_id <- Sys.getenv("REQUEST_ID")
node <- Sys.getenv("NODE")
yQuery <- Sys.getenv("PARAM_y")
A_Query <- Sys.getenv("PARAM_A")

# Perform the computation
y <- unlist(dbGetQuery(conn, yQuery))
A <- unlist(dbGetQuery(conn, A_Query))

if (length(A) %% length(y) != 0) stop(paste('Length of A is not a multiple of y, found length(A)=', length(A), " and length(y)=", length(y)))

A <- matrix(data = A, nrow = length(y), ncol = length(A) / length(y))
res <- LRegress_Node(y, A)

result_table <- Sys.getenv("RESULT_TABLE", "results_linear_regression")
result_columns <- Sys.getenv("RESULT_COLUMNS", "request_id, node, param_y, param_a, result_betai, result_sigmai")

if (Sys.getenv("IN_JDBC_DRIVER") != Sys.getenv("OUT_JDBC_DRIVER") ||
	Sys.getenv("IN_JDBC_JAR_PATH") != Sys.getenv("OUT_JDBC_JAR_PATH")) {

	outDrv <- JDBC(Sys.getenv("OUTJDBC_DRIVER"),
           Sys.getenv("OUT_JDBC_JAR_PATH"),
           identifier.quote="`")
} else {
	outDrv <- drv
}

if (Sys.getenv("IN_JDBC_URL") != Sys.getenv("OUT_JDBC_URL") ||
	Sys.getenv("IN_JDBC_USER") != Sys.getenv("OUT_JDBC_USER") ||
	Sys.getenv("IN_JDBC_PASSWORD") != Sys.getenv("OUT_JDBC_PASSWORD")) {

    outConn <- dbConnect(drv, Sys.getenv("OUT_JDBC_URL"), Sys.getenv("OUT_JDBC_USER"), Sys.getenv("OUT_JDBC_PASSWORD"))
} else {
	outConn <- conn
}

# Store results in the database
dbSendUpdate(outConn, paste( "INSERT INTO ", result_table, "(", result_columns, ") VALUES (?, ?, ?, ?, ?, ?)"),
	request_id, node, yQuery, A_Query, res[[1]], res[[2]])

# Disconnect from the database server
if (Sys.getenv("IN_JDBC_URL") != Sys.getenv("OUT_JDBC_URL")) dbDisconnect(outConn)
dbDisconnect(conn)
