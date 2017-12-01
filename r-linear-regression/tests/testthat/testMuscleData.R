context("MuscleData");

library(testthat);
library(rmipadaptor);
library(jsonlite);
library(yaml);

test_that("We can perform linear regression on one variable, one covariable and one group", {

  job_id <- '002';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select strip, conc, length from muscle",
    PARAM_variables="length",
    PARAM_covariables="conc",
    PARAM_grouping="strip");

  # Perform the computation
  source("/src/main.R");

  out_conn <- connect2outdb();

  # Get the results
  results <- DBI::dbGetQuery(out_conn, paste("select node, data, shape from job_result where job_id =", DBI::dbQuoteString(out_conn, job_id)));

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

  expect_equal(node, "job_test");
  expect_equal(shape, "pfa_yaml");

  expect_equal(result_model_const, 9.005107, tolerance = 1e-6);
  expect_equal(result_model_coeff, c(4.950000, 4.790558, -2.478915, -4.012249, -2.278915, 13.947957, 3.858670, 6.771425, 8.458670, 6.921085, 13.847957, 10.447957, 6.971425, 12.371425, 5.800000, 7.125000, -0.467688, 14.932312, 9.398979, 8.532312, 4.697957), tolerance = 1e-6);
  expect_equal(result_residuals, list(min=-8.438266, q1=-1.435457, median=0.35, q3=2.113858, max=8.438266), tolerance=1e-5);

  expect_equal(result_r_squared, 0.8350627, tolerance = 1e-6);
  expect_equal(result_degrees_freedom, c(22, 38, 22));

});
