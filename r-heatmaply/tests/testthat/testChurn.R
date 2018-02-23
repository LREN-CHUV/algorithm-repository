Sys.setenv(
  IN_DBI_DRIVER = "PostgreSQL",
  IN_DB_DBNAME = "data",
  IN_DB_HOST   = "localhost",
  IN_DB_PORT   = 5432,
  IN_DB_USER   = "data",
  IN_DB_PASSWORD = "data",
  OUT_DBI_DRIVER = "PostgreSQL",
  OUT_DB_DBNAME = "woken",
  OUT_DB_HOST   = "localhost",
  OUT_DB_PORT   = 5432,
  OUT_DB_USER   = "woken",
  OUT_DB_PASSWORD = "woken")

Sys.setenv(
  PARAM_query       = "SELECT * FROM churn LIMIT 20")

source("main.R")

print("Success!")
