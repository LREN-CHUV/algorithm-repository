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

res <- fromJSON(data);

# Disconnect from the database
disconnectdbs();

expect_equal(param_beta, "{0.9960748,1.005173}")
expect_equal(param_sigma, "{550.1556,410.0745}")

expect_equal(result_betaf, 1.001287, tolerance = 1e-6)
expect_equal(result_sigmaf, 234.9487, tolerance = 1e-6)

print ("[ok] Success!");
