context("BrainData");

library(testthat);
library(hbpjdbcconnect);
library(yaml);

test_that("We can perform linear regression on one variable and one covariable", {

  job_id <- '001';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select feature_name, tissue1_volume from brain_feature order by tissue1_volume",
    PARAM_variable="tissue1_volume",
    PARAM_covariables="feature_name");

  # Perform the computation
  source("/src/main.R");

  connect2outdb();

  # Get the results
  results <- RJDBC::dbGetQuery(out_conn, "select node, data, shape from job_result where job_id = ?", job_id);
  
  node <- results$node[[1]];
  data <- results$data[[1]];
  shape <- results$shape[[1]];
  
  res <- yaml.load(data);
  
  result_model_const <- res$cells$model$init$const;
  result_model_coeff <- res$cells$model$init$coeff;
  result_residuals <- res$residuals;
  result_r_squared <- res$cells$summary$init$r_squared;
  result_degrees_freedom <- res$cells$summary$init$degrees_freedom;
  
  # Disconnect from the database
  disconnectdbs();
  
  expect_equal(node, "Test");
  expect_equal(shape, "pfa_yaml");
  
  expected_result_residuals = "[{\"(Intercept)\":1.563e-08,\"feature_nameHippocampus_R\":-1.563e-08,\"_row\":\"(Intercept)\"},{\"(Intercept)\":-1.563e-08,\"feature_nameHippocampus_R\":3.126e-08,\"_row\":\"feature_nameHippocampus_R\"}]"
  
  expect_equal(result_model_const, 0.009194024, tolerance = 1e-6);
  expect_equal(result_model_coeff[1], -0.000005856, tolerance = 1e-6);
  # expect_equal(result_residuals, fromJSON(expected_result_residuals), tolerance=1e-5);
  
  expect_equal(result_r_squared, 1.119383e-05, tolerance = 1e-6);
  expect_equal(result_degrees_freedom, c(2, 98, 2));
  
  print ("[ok] Success!");

});
