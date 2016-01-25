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
  
  res
});