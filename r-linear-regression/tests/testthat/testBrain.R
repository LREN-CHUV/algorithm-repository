context("Brain");

library(testthat);
library(hbpjdbcconnect);
library(yaml);

test_that("We can perform linear regression on one variable and one covariable", {

  job_id <- '003';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select age, prov, left_amygdala from brain",
    PARAM_variables="left_amygdala",
    PARAM_covariables="age",
    PARAM_grouping="prov");

  # Perform the computation
  source("/src/main.R");

  out_conn <- connect2outdb();

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

  expect_equal(node, "job_test");
  expect_equal(shape, "pfa_yaml");


  expect_equal(result_model_const, 0.3270614,     tolerance = 1e-6, scale = 1);
  expect_equal(result_model_coeff[1], 0.18680482, tolerance = 1e-6, scale = 1);
  expect_equal(result_model_coeff[2], 0.00537280, tolerance = 1e-6, scale = 1);

  expect_equal(result_r_squared, 0.96454576, tolerance = 1e-6);
  expect_equal(result_degrees_freedom, c(3,6,3));

});

test_that("We can perform linear regression on one variable and two covariables", {

  job_id <- '003b';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select left_splsupparlob, right_poparoper, right_pogpostcgyr from brain",
    PARAM_variables="left_splsupparlob",
    PARAM_covariables="right_poparoper,right_pogpostcgyr",
    PARAM_grouping="");

  # Perform the computation
  source("/src/main.R");

  out_conn <- connect2outdb();

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

  expect_equal(node, "job_test");
  expect_equal(shape, "pfa_yaml");


  expect_equal(result_model_const, -0.03204289,  tolerance = 1e-6, scale = 1);
  expect_equal(result_model_coeff[1], 0.4448689, tolerance = 1e-6, scale = 1);
  expect_equal(result_model_coeff[2], 0.1286247, tolerance = 1e-6, scale = 1);

  expect_equal(result_r_squared, 0.6961309, tolerance = 1e-6);
  expect_equal(result_degrees_freedom, c(3,6,3));

});
