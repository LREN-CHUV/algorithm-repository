library(testthat)

# Perform the computation
source("/src/main.R")

conn <- dbConnect(drv, Sys.getenv("OUT_JDBC_URL"), Sys.getenv("OUT_JDBC_USER"), Sys.getenv("OUT_JDBC_PASSWORD"))
request_id <- Sys.getenv("REQUEST_ID")
result_table <- Sys.getenv("RESULT_TABLE", "results_linear_regression")
result_columns <- Sys.getenv("RESULT_COLUMNS", "request_id, node, param_y, param_a, result_betai, result_sigmai")

# Get the results
results <- dbGetQuery(conn, paste("select ", result_columns ," from ", result_table, " where request_id = ?"), request_id)

node <- results$node
param_y <- results$param_y
param_a <- results$param_a
result_betai <- results$result_betai
result_sigmai <- results$result_sigmai

# Disconnect from the database server
dbDisconnect(conn)

expect_equal(node, "Test")
expect_equal(param_y, "select tissue1_volume from test.brain_feature where feature_name='Hippocampus_L' order by tissue1_volume")
expect_equal(param_a, "select tissue1_volume from test.brain_feature where feature_name='Hippocampus_R' order by tissue1_volume")

expect_equal(result_betai, 1.001287, tolerance = 1e-6)
expect_equal(result_sigmai, 234.9487, tolerance = 1e-6)

print ("Success!")
