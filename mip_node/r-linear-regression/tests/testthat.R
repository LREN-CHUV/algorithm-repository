library(testthat);
library(hbpjdbcconnect);
library(jsonlite);
library(yaml);

# Perform the computation
source("/src/main.R");

connect2outdb();

job_id <- Sys.getenv("JOB_ID");

# Get the results
results <- RJDBC::dbGetQuery(out_conn, "select node, data, shape from job_result where job_id = ?", job_id);

node <- results$node[[1]];
data <- results$data[[1]];
shape <- results$shape[[1]];

res <- yaml.load(data);

result_coefficients <- res$cells$coefficients$init;
result_residuals <- res$residuals;
result_r_square <- res$cells$summary$init$r_squared;
result_degrees_freedom <- res$cells$summary$init$degrees_freedom;

# Disconnect from the database
disconnectdbs();

expect_equal(node, "Test");
expect_equal(shape, "pfa_yaml");

expected_result_residuals = "[{\"(Intercept)\":1.563e-08,\"feature_nameHippocampus_R\":-1.563e-08,\"_row\":\"(Intercept)\"},{\"(Intercept)\":-1.563e-08,\"feature_nameHippocampus_R\":3.126e-08,\"_row\":\"feature_nameHippocampus_R\"}]"

expect_equal(result_coefficients$'_intercept_', 0.009194024, tolerance = 1e-6);
expect_equal(result_coefficients$feature_nameHippocampus_R, -0.000005856, tolerance = 1e-6);
# expect_equal(result_residuals, fromJSON(expected_result_residuals), tolerance=1e-5);

expect_equal(result_r_square, 1.119383e-05, tolerance = 1e-6);
expect_equal(result_degrees_freedom, c(2, 98, 2));

print ("[ok] Success!");
