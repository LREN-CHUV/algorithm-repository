context("MuscleData");

library(testthat);
library(hbpjdbcconnect);
library(jsonlite);
library(yaml);

test_that("We can perform linear regression on one variable, one covariable and one group", {

  job_id <- '002';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select strip, conc, length from muscle",
    PARAM_varname="length",
    PARAM_covarnames="conc",
    PARAM_groups="strip");

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
  result_residuals <- res$cells$summary$init$residuals;
  result_r_squared <- res$cells$summary$init$r_squared;
  result_degrees_freedom <- res$cells$summary$init$degrees_freedom;
  
  # Disconnect from the database
  disconnectdbs();
  
  expect_equal(node, "Test");
  expect_equal(shape, "pfa_yaml");
  
  expect_equal(result_model_const, 9.005107, tolerance = 1e-6);
  expect_equal(result_model_coeff, c(4.9500, 4.7906, -2.4789, -4.0122, -2.2789, 13.9480, 3.8587, 6.7714, 8.4587, 6.9211, 13.8480, 10.4480, 6.9714, 12.3714, 5.8000, 7.1250, -0.4677, 14.9323, 9.3990, 8.5323, 4.6980), tolerance = 1e-6);
  expect_equal(result_residuals, list(min=-8.438266, q1=-1.435457, median=0.35, q3=2.113858, max=8.438266), tolerance=1e-5);

  expect_equal(result_r_squared, 0.8350627, tolerance = 1e-6);
  expect_equal(result_degrees_freedom, c(22, 38, 22));
  
  print ("[ok] Success!");

});
