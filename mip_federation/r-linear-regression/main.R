#
# This script computes the linear regression.
# The data (input parameters: y, A) are obtained from the local databases using a specific query.
# These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Execution context:
#      REQUEST_ID : ID of the incoming request
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
#      INPUT_TABLE: name of the input table, defaults to 'results_linear_regression'
#      INPUT_RESULT_COLUMNS: list of result columns in the input table, defaults to "result_betai, result_sigmai"
#      RESULT_TABLE: name of the result table, defaults to 'federation_results_linear_regression'
#      RESULT_COLUMNS: list of columns for the result table, default to "request_id, param_beta, param_sigma, result_betaf, result_sigmaf"
#

library(hbplregress)
library(RJDBC)

# Initialisation
drv <- JDBC(Sys.getenv("IN_JDBC_DRIVER"),
           Sys.getenv("IN_JDBC_JAR_PATH"),
           identifier.quote="`")
conn <- dbConnect(drv, Sys.getenv("IN_JDBC_URL"), Sys.getenv("IN_JDBC_USER"), Sys.getenv("IN_JDBC_PASSWORD"))
request_id <- Sys.getenv("REQUEST_ID")
input_table <- Sys.getenv("INPUT_TABLE", "results_linear_regression")
input_result_columns <- Sys.getenv("INPUT_RESULT_COLUMNS", "result_betai, result_sigmai")

# Perform the computation
results <- unlist(dbGetQuery(conn, paste("select ", input_result_columns, "from ", input_table, " where request_id = ?"), request_id))
names(results) <- c('beta1','beta2','Sigma1','Sigma2')

res <- do.call(LRegress_Federation, as.list(results))
n <- length(results)

betas <- results[seq(1, n / 2)]
sigmas <- results[seq(n / 2 + 1, n)]

betas_arr <- paste('{', paste(betas, collapse=','), '}', sep='')
sigmas_arr <- paste('{', paste(sigmas, collapse=','), '}', sep='')

result_table <- Sys.getenv("RESULT_TABLE", "federation_results_linear_regression")
result_columns <- Sys.getenv("RESULT_COLUMNS", "request_id, param_beta, param_sigma, result_betaf, result_sigmaf")

if (Sys.getenv("IN_JDBC_DRIVER") != Sys.getenv("OUT_JDBC_DRIVER") ||
	Sys.getenv("IN_JDBC_JAR_PATH") != Sys.getenv("OUT_JDBC_JAR_PATH")) {

	outDrv <- JDBC(Sys.getenv("OUT_JDBC_DRIVER"),
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
dbSendUpdate(outConn, paste( "INSERT INTO ", result_table, "(", result_columns, ") VALUES (?, ?, ?, ?, ?)"),
	request_id, betas_arr, sigmas_arr, res[[1]], res[[2]])

# Disconnect from the database server
if (Sys.getenv("IN_JDBC_URL") != Sys.getenv("OUT_JDBC_URL")) dbDisconnect(outConn)
dbDisconnect(conn)
