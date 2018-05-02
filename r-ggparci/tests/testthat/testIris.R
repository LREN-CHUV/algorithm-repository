print("[Iris test] Starting...")

if (is.null(Sys.getenv("NODE"))) {
  Sys.setenv(
    IN_DBI_DRIVER = "PostgreSQL",
    IN_DATABASE   = "data",
    IN_HOST       = "localhost",
    IN_PORT       = 5432,
    IN_USER       = "data",
    IN_PASSWORD   = "data",
    OUT_DBI_DRIVER = "PostgreSQL",
    OUT_DATABASE   = "woken",
    OUT_HOST       = "localhost",
    OUT_PORT       = 5432,
    OUT_USER       = "woken",
    OUT_PASSWORD   = "woken")
}

Sys.setenv(
  JOB_ID            = "20",
  PARAM_variables   = "name",
  PARAM_covariables = "",
  PARAM_query       = "SELECT * FROM iris")

source("/src/main.R")

print("[Iris test] Success!")
