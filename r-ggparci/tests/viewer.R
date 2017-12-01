library(rmipadaptor);

conn <- connect2outdb();

# Get the results
results <- DBI::dbGetQuery(out_conn, paste("select * from job_result where job_id =", DBI::dbQuoteString(out_conn, job_id)));

data <- results$data[[1]];

file.save(data, file="data/out/result.svg", ascii=TRUE)
