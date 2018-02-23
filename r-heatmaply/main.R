#'
#' This script generates an interactive heatmap visualization and save it as html.
#' The data are obtained from the local databases using a specific query.
#' This query will be the same for all nodes.
#'
#' The environment variables are:
#'
#' * Input Parameters (for heatmaply):
#'    - PARAM_query  : SQL query producing the dataframe to plot
#'    - PARAM_variables : Ignored.
#'    - PARAM_covariables : Ignored.
#'    - PARAM_* : any other parameters to pass to the R function. See example in the docker-compose file.
#' * Execution context:
#'    - JOB_ID : ID of the job
#'    - NODE : Node used for the execution of the script
#'    - IN_DBI_DRIVER   : Class name of the DBI driver for input data
#'    - IN_DBI_DBNAME     : Database name for the database connection for input data
#'    - IN_DBI_HOST     : Host name for the database connection for input data
#'    - IN_DBI_PORT     : Port number for the database connection for input data
#'    - IN_DBI_PASSWORD : Password for the database connection for input data
#'    - IN_DBI_USER     : User for the database connection for input data
#'    - OUT_DBI_DRIVER   : Class name of the DBI driver for output data
#'    - OUT_DBI_DBNAME     : Database name for the database connection for output data
#'    - OUT_DBI_HOST     : Host name for the database connection for output data
#'    - OUT_DBI_PORT     : Port number for the database connection for output data
#'    - OUT_DBI_USER     : User for the database connection for output data
#'    - OUT_DBI_PASSWORD : Password for the database connection for output data

library(rmipadaptor)
library(heatmaply)
library(svglite)

## for debugging only (4 lines):
# Sys.setenv(PARAM_covariables = "Sepal.Length,Sepal.Width,Petal.Length")
# Sys.setenv(PARAM_k_row = 3)
# Sys.setenv(PARAM_k_col = 2)
# data <- iris

data   <- fetchData()

## the following function definition should be moved to r-mip-adaptor, as it is general for all R images
get_PARAM_env_vars_into_R_list <- function()
{
  all_env_vars <- Sys.getenv()
  env_vars_starting_with_PARAM <- as.list(all_env_vars[ grep(pattern = "^PARAM_.*", x = names(all_env_vars)) ])
  truncated_names <- substring(text = names(env_vars_starting_with_PARAM),first = 7)
  var_list <- env_vars_starting_with_PARAM
  names(var_list) <- truncated_names
  return(var_list)
}

# get the enviroment variables starting with PARAM into an R list:
var_list <- get_PARAM_env_vars_into_R_list()

## add data argument to the arguments list and remap other arguments to fit heatmaply
columns <- if (var_list$covariables == "") 1:ncol(data) else unlist(strsplit(var_list$covariables, split = ","))
var_list$x <- data[columns]
numeric_inputs <- c("row_text_angle", "column_text_angle", "k_row", "k_col")
for (i in seq_along(var_list))
  if (names(var_list[i]) %in% numeric_inputs) var_list[i] <- as.numeric(var_list[i])

## run the main function and save to "plot.html"
var_list$file <- NULL
p <- do.call(what = heatmaply, args = var_list)
htmlwidgets::saveWidget(as_widget(p), "plot.html")
html_str <- paste0(readLines(con = "plot.html"),collapse = "\n")
saveResults(results =  html_str, shape = "html")
disconnectdbs()
