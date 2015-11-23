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

data <- fromJSON(data);
res <- sapply(data, fromJSON);
tv <- res[,"tissue1_volume"];

result_min <- tv$min;
result_q1 <- tv$q1;
result_median <- tv$median;
result_q3 <- tv$q3;
result_max <- tv$max;
result_mean <- tv$mean;
result_std <- tv$std;
result_sum <- tv$sum;
result_count <- tv$count;

# Disconnect from the database
disconnectdbs();

expect_equal(node, "job_test");

expect_equal(tv$min,    0.0068206, tolerance = 1e-6);
expect_equal(tv$q1,     0.00857095, tolerance = 1e-6);
expect_equal(tv$median, 0.00931775, tolerance = 1e-6);
expect_equal(tv$q3,     0.009805875, tolerance = 1e-6);
expect_equal(tv$max,    0.011463, tolerance = 1e-6);
expect_equal(tv$mean,   0.0091911, tolerance = 1e-6);
expect_equal(tv$std,    0.00087956, tolerance = 1e-6);
expect_equal(tv$sum,    0.9191096, tolerance = 1e-6);
expect_equal(tv$count,  100);

print ("Success!");
