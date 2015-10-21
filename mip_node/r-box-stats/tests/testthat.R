library(testthat)

# Perform the computation
source("/src/main.R")

connect2outdb()

request_id <- Sys.getenv("REQUEST_ID")
result_table <- Sys.getenv("RESULT_TABLE", "result_box_stats")
result_columns <- "request_id, node, id, min, q1, median, q3, max"

# Get the results
results <- RJDBC::dbGetQuery(out_conn, paste("select ", result_columns ," from ", result_table, " where request_id = ?"), request_id)

node <- results$node[[1]]
result_min <- results$min
result_q1 <- results$q1
result_median <- results$median
result_q3 <- results$q3
result_max <- results$max

# Disconnect from the database
disconnectdbs()

expect_equal(node, "Test")

print (results)
expect_equal(result_min, 0.0068206, tolerance = 1e-6)
expect_equal(result_q1, 0.00857095, tolerance = 1e-6)
expect_equal(result_median, 0.00931775, tolerance = 1e-6)
expect_equal(result_q3, 0.009805875, tolerance = 1e-6)
expect_equal(result_max, 0.011463, tolerance = 1e-6)

print ("Success!")
