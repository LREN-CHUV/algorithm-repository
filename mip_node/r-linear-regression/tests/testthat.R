library(testthat);
library(hbpjdbcconnect);
library(jsonlite);

# Perform the computation
source("/src/main.R");

connect2outdb();

job_id <- Sys.getenv("JOB_ID");

# Get the results
results <- RJDBC::dbGetQuery(out_conn, "select node, data, shape from job_result where job_id = ?", job_id);

node <- results$node[[1]];
data <- results$data[[1]];
shape <- results$shape[[1]];

res <- fromJSON(data);

result_coefficients <- res$coefficients;
result_residuals <- res$residuals;

# Disconnect from the database
disconnectdbs();

expect_equal(node, "Test");
expect_equal(shape, "r_other_intermediate");

expect_equal(result_coefficients[[1]], 1.51756892,  tolerance = 1e-6);
expect_equal(result_coefficients[[2]], -1.91151546, tolerance = 1e-6);
expect_equal(ncol(result_residuals), 0);

print ("[ok] Success!");
