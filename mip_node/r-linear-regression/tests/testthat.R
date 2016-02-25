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

expected_result_residuals = "[{\"(Intercept)\":1.563e-08,\"feature_nameHippocampus_R\":-1.563e-08,\"_row\":\"(Intercept)\"},{\"(Intercept)\":-1.563e-08,\"feature_nameHippocampus_R\":3.126e-08,\"_row\":\"feature_nameHippocampus_R\"}]"

expect_equal(result_coefficients[[1]], 0.009194024,  tolerance = 1e-6);
expect_equal(result_coefficients[[2]], -0.000005856, tolerance = 1e-6);
expect_equal(result_residuals, fromJSON(expected_result_residuals), tolerance=1e-5);

print ("[ok] Success!");
