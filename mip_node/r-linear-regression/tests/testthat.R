library(testthat);
library(hbpjdbcconnect);
library(jsonlite);

# Perform the computation
source("/src/main.R");

connect2outdb();

job_id <- Sys.getenv("JOB_ID");

# Get the results
results <- RJDBC::dbGetQuery(out_conn, "select node, data from job_result where job_id = ?", job_id);

node <- results$node[[1]]
data <- results$data[[1]]

print (data)

res <- as.data.frame(fromJSON(data));

print res
param_y <- res$param_y;
param_a <- results$param_a;
result_betai <- results$result_betai;
result_sigmai <- results$result_sigmai;

# Disconnect from the database
disconnectdbs();

expect_equal(node, "Test");
expect_equal(param_y, "select tissue1_volume from test.brain_feature where feature_name='Hippocampus_L' order by tissue1_volume");
expect_equal(param_a, "select tissue1_volume from test.brain_feature where feature_name='Hippocampus_R' order by tissue1_volume");

expect_equal(result_betai, 1.001287, tolerance = 1e-6);
expect_equal(result_sigmai, 234.9487, tolerance = 1e-6);

print ("Success!");
