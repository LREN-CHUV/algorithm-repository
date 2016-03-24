context("BrainData");

library(testthat);
library(hbpjdbcconnect);
library(yaml);

test_that("We can perform summary statistics on one variable", {

  job_id <- '001';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select tissue1_volume from brain_feature",
    PARAM_variables="tissue1_volume",
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

  tv1_min <- res$cells$summary$init$tissue1_volume$min;
  tv1_q1 <- res$cells$summary$init$tissue1_volume$q1;
  tv1_median <- res$cells$summary$init$tissue1_volume$median;
  tv1_q3 <- res$cells$summary$init$tissue1_volume$q3;
  tv1_max <- res$cells$summary$init$tissue1_volume$max;
  tv1_mean <- res$cells$summary$init$tissue1_volume$mean;
  tv1_std <- res$cells$summary$init$tissue1_volume$std;
  tv1_sum <- res$cells$summary$init$tissue1_volume$sum;
  tv1_count <- res$cells$summary$init$tissue1_volume$count;

  # Disconnect from the database
  disconnectdbs();

  expect_equal(node, "job_test");
  expect_equal(shape, "pfa_yaml");

  expect_equal(tv1_min,    0.0068206,   tolerance = 1e-6, scale = 1);
  expect_equal(tv1_q1,     0.00857095,  tolerance = 1e-6, scale = 1);
  expect_equal(tv1_median, 0.00931775,  tolerance = 1e-6, scale = 1);
  expect_equal(tv1_q3,     0.009805875, tolerance = 1e-6, scale = 1);
  expect_equal(tv1_max,    0.011463,    tolerance = 1e-6, scale = 1);
  expect_equal(tv1_mean,   0.0091911,   tolerance = 1e-6, scale = 1);
  expect_equal(tv1_std,    0.00087956,  tolerance = 1e-6, scale = 1);
  expect_equal(tv1_sum,    0.9191096,   tolerance = 1e-6, scale = 1);
  expect_equal(tv1_count,  100);

});

test_that("We can perform summary statistics on 2 variables, one is a factor", {

  job_id <- '001b';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select feature_name, tissue1_volume from brain_feature",
    PARAM_variables="tissue1_volume",
    PARAM_covariables="feature_name",
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

  tv1_min <- res$cells$summary$init$tissue1_volume$min;
  tv1_q1 <- res$cells$summary$init$tissue1_volume$q1;
  tv1_median <- res$cells$summary$init$tissue1_volume$median;
  tv1_q3 <- res$cells$summary$init$tissue1_volume$q3;
  tv1_max <- res$cells$summary$init$tissue1_volume$max;
  tv1_mean <- res$cells$summary$init$tissue1_volume$mean;
  tv1_std <- res$cells$summary$init$tissue1_volume$std;
  tv1_sum <- res$cells$summary$init$tissue1_volume$sum;
  tv1_count <- res$cells$summary$init$tissue1_volume$count;
  fn_count <- res$cells$summary$init$feature_name$count;
  fn_factors <- res$cells$summary$init$feature_name$factors;

  # Disconnect from the database
  disconnectdbs();

  expect_equal(node, "job_test");
  expect_equal(shape, "pfa_yaml");

  expect_equal(tv1_min,    0.0068206,   tolerance = 1e-6, scale = 1);
  expect_equal(tv1_q1,     0.00857095,  tolerance = 1e-6, scale = 1);
  expect_equal(tv1_median, 0.00931775,  tolerance = 1e-6, scale = 1);
  expect_equal(tv1_q3,     0.009805875, tolerance = 1e-6, scale = 1);
  expect_equal(tv1_max,    0.011463,    tolerance = 1e-6, scale = 1);
  expect_equal(tv1_mean,   0.0091911,   tolerance = 1e-6, scale = 1);
  expect_equal(tv1_std,    0.00087956,  tolerance = 1e-6, scale = 1);
  expect_equal(tv1_sum,    0.9191096,   tolerance = 1e-6, scale = 1);
  expect_equal(tv1_count,  100);
  expect_equal(fn_count,   100);
  expect_equal(fn_factors, c("Hippocampus_L", "Hippocampus_R"));

});
