context("Brain");

library(testthat);
library(hbpjdbcconnect);
library(yaml);

test_that("We can perform tSNE on several covariables and one grouping", {

  job_id <- '003';
  Sys.setenv(JOB_ID=job_id,
    PARAM_query="select * from brain",
    PARAM_variables="age",
    PARAM_covariables="left_amygdala,left_splsupparlob,right_poparoper,right_pogpostcgyr",
    PARAM_grouping="prov",
    PARAM_perplexity=1,
    PARAM_theta=0.0);

  set.seed(100);

  # Perform the computation
  source("/src/main.R");

  out_conn <- connect2outdb();

  # Get the results
  results <- RJDBC::dbGetQuery(out_conn, "select node, data, shape from job_result where job_id = ?", job_id);
  
  node <- results$node[[1]];
  data <- results$data[[1]];
  shape <- results$shape[[1]];

  # Disconnect from the database
  disconnectdbs();
  
  expect_equal(node, "job_test");
  expect_equal(shape, "pfa_yaml");
  
  res <- yaml.load(data);

  reduced_data <- as.data.frame(do.call(rbind.data.frame, res$cells$reduced_data$init), stringsAsFactors = T);
  names(reduced_data) <- c('X1', 'X2', 'prov', 'age');
  row.names(reduced_data) <- NULL;

  expected_df <- data.frame(
    X1 = c(-53.5168,86.4786,-49.1458,-42.6087,103.1089,96.5247,-60.0566,-43.5824,-37.202),
    X2 = c(311.0639,-395.9667,316.3409,324.2359,-395.4002,-395.625,303.1716,-33.9247,-33.8958),
    prov = c("AD1", "AD1", "AD1", "AD1", "AD1", "AD1", "AD1", "AD2", "AD2"),
    age = c(81.2, 81.2, 81.2, 73.6, 73.6, 73.6, 73.6, 70.1, 70.1)
  );
  row.names(expected_df) <- NULL;

  # Use a wide tolerance because tSNE is non deterministic
  expect_equal(reduced_data, expected_df, tolerance = 20, scale = 1);
  
});
