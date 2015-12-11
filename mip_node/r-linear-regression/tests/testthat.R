library(testthat);
library(hbpjdbcconnect);
library(jsonlite);

# Perform the computation
source("/src/main.R");

connect2outdb();

job_id <- Sys.getenv("JOB_ID");

# Get the results
results <- RJDBC::dbGetQuery(out_conn, "select node, data from job_result where job_id = ?", job_id);

node <- results$node[[1]];
data <- results$data[[1]];

res <- as.data.frame(fromJSON(data));

result_betai <- results$result_betai;
result_sigmai <- results$result_sigmai;

# Disconnect from the database
disconnectdbs();

expect_equal(node, "Test");

expect_equivalent(result_beta, c(1.51756892,-1.91151546));
expect_equivalent(result_sigma, c(NA, NA));

print ("[ok] Success!");
