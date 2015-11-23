library(testthat);
library(jsonlite);

# Perform the computation
source("/src/main.R");

connect2outdb();

job_id <- Sys.getenv("JOB_ID");

# Get the results
results <- RJDBC::dbGetQuery(out_conn, "select node, data from job_result where job_id = ?", job_id);

node <- results$node[[1]]
data <- results$data[[1]]

res <- as.data.frame(fromJSON(data));

result_min <- res["min","tissue1_volume"];
result_q1 <- res["q1","tissue1_volume"];
result_median <- res["median","tissue1_volume"];
result_q3 <- res["q3","tissue1_volume"];
result_max <- res["max","tissue1_volume"];
result_mean <- res["mean","tissue1_volume"];
result_std <- res["std","tissue1_volume"];
result_sum <- res["sum","tissue1_volume"];
result_count <- res["count","tissue1_volume"];

# Disconnect from the database
disconnectdbs();

expect_equal(node, "job_test");

expect_equal(result_min,    0.0068206, tolerance = 1e-6);
expect_equal(result_q1,     0.00857095, tolerance = 1e-6);
expect_equal(result_median, 0.00931775, tolerance = 1e-6);
expect_equal(result_q3,     0.009805875, tolerance = 1e-6);
expect_equal(result_max,    0.011463, tolerance = 1e-6);
expect_equal(result_mean,   0.0091911, tolerance = 1e-6);
expect_equal(result_std,    0.00087956, tolerance = 1e-6);
expect_equal(result_sum,    0.9191096, tolerance = 1e-6);
expect_equal(result_count,  100);

print ("Success!");
