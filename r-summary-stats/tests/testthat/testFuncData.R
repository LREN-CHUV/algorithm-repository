context("FuncData");

library(testthat);
library(hbpjdbcconnect);
library(yaml);

test_that("We can perform summary statistics on 2 variables", {

  job_id <- '002';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select efc,fber from func",
    PARAM_variables="efc,fber",
    PARAM_covariables="",
    PARAM_grouping="");

  # Perform the computation
  source("/src/main.R");

  out_conn <- connect2outdb();

  # Get the results
  results <- RJDBC::dbGetQuery(out_conn, "select node, data, shape from job_result where job_id = ?", job_id);

  node <- results$node[[1]]
  data <- results$data[[1]]
  shape <- results$shape[[1]];

  res <- yaml.load(data);

  efcs <- res$cells$summary$init$efc;
  fbers <- res$cells$summary$init$fber;

  # Disconnect from the database
  disconnectdbs();

  expect_equal(node, "job_test");
  expect_equal(shape, "pfa_yaml");

  expect_equal(efcs$min,    0.8895676,  tolerance = 1e-6);
  expect_equal(efcs$q1,     0.8909397,  tolerance = 1e-6);
  expect_equal(efcs$median, 0.8917949,  tolerance = 1e-6);
  expect_equal(efcs$q3,     0.8928247,  tolerance = 1e-6);
  expect_equal(efcs$max,    0.8944770,  tolerance = 1e-6);
  expect_equal(efcs$mean,   0.8919107,  tolerance = 1e-6);
  expect_equal(efcs$std,    0.0013269,  tolerance = 1e-6);
  expect_equal(efcs$sum,    27.649233,  tolerance = 1e-6);
  expect_equal(efcs$count,  31,         tolerance = 1e-6);
  expect_equal(fbers$min,   71.814765,  tolerance = 1e-6);
  expect_equal(fbers$q1,    79.475678,  tolerance = 1e-6);
  expect_equal(fbers$median,85.462336,  tolerance = 1e-6);
  expect_equal(fbers$q3,    92.732653,  tolerance = 1e-6);
  expect_equal(fbers$max,   101.224571, tolerance = 1e-6);
  expect_equal(fbers$mean,  85.995691,  tolerance = 1e-6);
  expect_equal(fbers$std,   7.806265,   tolerance = 1e-6);
  expect_equal(fbers$sum,   2665.866435,tolerance = 1e-6);
  expect_equal(fbers$count, 31,         tolerance = 1e-6);

});