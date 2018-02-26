Sys.setenv(
  PARAM_query   = "SELECT * FROM iris",
  IN_DBI_DRIVER = "PostgreSQL",
  IN_DBI_DBNAME = "data",
  IN_DBI_HOST   = "localhost",
  IN_DBI_PORT   = 5432,
  IN_DBI_USER   = "data",
  IN_DBI_PASSWORD = "data",
  OUT_DBI_DRIVER = "PostgreSQL",
  OUT_DBI_DBNAME = "woken",
  OUT_DBI_HOST   = "localhost",
  OUT_DBI_PORT   = 5432,
  OUT_DBI_USER   = "woken",
  OUT_DBI_PASSWORD = "woken")

Sys.setenv(
  PARAM_variables   = "sepal_length",
  PARAM_covariables = "petal_width, petal_length",
  PARAM_grouping = "Species", # TODO: fix to match the name in the database
  PARAM_query       = "SELECT * FROM iris")

source("../../R/main.R")
