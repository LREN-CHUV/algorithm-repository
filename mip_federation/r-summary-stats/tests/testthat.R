library(testthat);
library(hbpjdbcconnect);
library(jsonlite);

# Perform the computation
source("/src/main.R");

connect2outdb();

job_id <- Sys.getenv("JOB_ID");

# Get the results
results <- RJDBC::dbGetQuery(out_conn, "select node, data from job_result where job_id = ?", job_id);

node <- results$node[[1]]
data <- results$data[[1]]

res <- fromJSON(data);

result_min    <- res$tissue1_volume[[1]];
result_q1     <- res$tissue1_volume[[2]];
result_median <- res$tissue1_volume[[3]];
result_q3     <- res$tissue1_volume[[4]];
result_max    <- res$tissue1_volume[[5]];
result_mean   <- res$tissue1_volume[[6]];
result_std    <- res$tissue1_volume[[7]];
result_sum    <- res$tissue1_volume[[8]];
result_count  <- res$tissue1_volume[[9]];

# Disconnect from the database
disconnectdbs();

expect_equal(result_min,    0.0068206, tolerance = 1e-6);
## TODO - improve this result - expect_equal(result_q1,     0.00857095, tolerance = 1e-6);
## TODO - improve this result - expect_equal(result_median, 0.00931775, tolerance = 1e-6);
## TODO - improve this result - expect_equal(result_q3,     0.009805875, tolerance = 1e-6);
expect_equal(result_max,    0.011463, tolerance = 1e-6);
expect_equal(result_mean,   0.0091911, tolerance = 1e-6);
expect_equal(result_std,    0.00087956, tolerance = 1e-5, scale=1);
expect_equal(result_sum,    0.9191096, tolerance = 1e-6);
expect_equal(result_count,  100);

expect_equal(node, "job_test");

print ("[ok] Success!");
