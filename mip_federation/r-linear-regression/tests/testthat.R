library(testthat)

# Perform the computation
source("/src/main.R")

conn <- dbConnect(drv, Sys.getenv("OUT_JDBC_URL"), Sys.getenv("OUT_JDBC_USER"), Sys.getenv("OUT_JDBC_PASSWORD"))
request_id <- Sys.getenv("REQUEST_ID")
result_table <- Sys.getenv("RESULT_TABLE", "federation_results_linear_regression")
result_columns <- Sys.getenv("RESULT_COLUMNS", "request_id, param_beta, param_sigma, result_betaf, result_sigmaf")

# Get the results
results <- dbGetQuery(conn, paste("select ", result_columns ," from ", result_table, " where request_id = ?"), request_id)

param_beta <- results$param_beta
param_sigma <- results$param_sigma
result_betaf <- results$result_betaf
result_sigmaf <- results$result_sigmaf

# Disconnect from the database server
dbDisconnect(conn)

expect_equal(param_beta, "{0.9960748,1.005173}")
expect_equal(param_sigma, "{550.1556,410.0745}")

expect_equal(result_betaf, 1.001287, tolerance = 1e-6)
expect_equal(result_sigmaf, 234.9487, tolerance = 1e-6)

print ("Success!")
