library(rmipadaptor);

job_id <- Sys.getenv("JOB_ID");
conn <- connect2outdb();

# Get the results
results <- DBI::dbGetQuery(out_conn, paste("select * from job_result where job_id =", DBI::dbQuoteString(out_conn, job_id)));

data <- results$data[[1]];

write(data, file="/data/out/result.txt")
