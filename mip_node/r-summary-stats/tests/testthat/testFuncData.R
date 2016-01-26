context("FuncData");

library(testthat);
library(hbpjdbcconnect);

test_that("We can perform summary statistics on 2 variables", {

  job_id <- '002';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select efc,fber from func",
    PARAM_colnames="efc,fber");

  # Perform the computation
  source("/src/main.R");
  
  connect2outdb();
  
  # Get the results
  results <- RJDBC::dbGetQuery(out_conn, "select node, data from job_result where job_id = ?", job_id);
  
  node <- results$node[[1]]
  data <- results$data[[1]]
  
  res <- as.data.frame(fromJSON(data));
  
  # Disconnect from the database
  disconnectdbs();
  
  expect_equal(res["min", "efc"],    0.8895676, tolerance = 1e-6);
  expect_equal(res["q1", "efc"],     0.8909397, tolerance = 1e-6);
  expect_equal(res["median", "efc"], 0.8917949, tolerance = 1e-6);
  expect_equal(res["q3", "efc"],     0.8928247, tolerance = 1e-6);
  expect_equal(res["max", "efc"],    0.8944770, tolerance = 1e-6);
  expect_equal(res["mean", "efc"],   0.8919107, tolerance = 1e-6);
  expect_equal(res["std", "efc"],    0.0013269, tolerance = 1e-6);
  expect_equal(res["sum", "efc"],    27.6492333, tolerance = 1e-6);
  expect_equal(res["count", "efc"],  31,         tolerance = 1e-6);
  expect_equal(res["min", "fber"],    71.814765, tolerance = 1e-6);
  expect_equal(res["q1", "fber"],     79.475678, tolerance = 1e-6);
  expect_equal(res["median", "fber"], 85.462336, tolerance = 1e-6);
  expect_equal(res["q3", "fber"],     92.732653, tolerance = 1e-6);
  expect_equal(res["max", "fber"],    101.224571, tolerance = 1e-6);
  expect_equal(res["mean", "fber"],   85.995691, tolerance = 1e-6);
  expect_equal(res["std", "fber"],    7.806265, tolerance = 1e-6);
  expect_equal(res["sum", "fber"],    2665.866435, tolerance = 1e-6);
  expect_equal(res["count", "fber"],  31,         tolerance = 1e-6);
  
  expect_equal(node, "job_test");

});