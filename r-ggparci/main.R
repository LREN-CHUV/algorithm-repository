#'
#' This script generates the parallel coordinates vislualization and save it as svg file.
#' The data are obtained from the local databases using a specific query.
#' This query will be the same for all nodes.
#'
#' The environment variables are:
#'
#' * Input Parameters (for ggparci):
#'    - PARAM_query  : SQL query producing the dataframe to analyse
#'    - PARAM_variables : the grouping variable
#'    - PARAM_covariables : The variables to be ploted in the parallel coordinates plot.
#'    - PARAM_* : to pass any option to the R function. See example in the docker-compose.yml file.
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
library(ggplot2)
library(svglite)
library(ggparci)

## for debugging only (4 lines):
# Sys.setenv(PARAM_variables   = "Species")
# Sys.setenv(PARAM_covariables = "Sepal.Length,Sepal.Width,Petal.Length")
# Sys.setenv(PARAM_flip_coords = "T")
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

## add data argument to the arguments list and remap other arguments to fit ggparci

var_list$data <- data
var_list$columns <- if (var_list$covariables == "") 1:ncol(data) else unlist(strsplit(var_list$covariables, split = ","))
var_list$groups_column <- var_list$variables

## run the main function

plot_object <- do.call(what = ggparci,args = var_list,quote = F)
height <- if (is.null(var_list$height)) 4 else as.numeric(var_list$height)
width  <- if (is.null(var_list$width))  5 else as.numeric(var_list$width)

svg_str <- stringSVG(grid::grid.draw(plot_object), height = height, width = width) # use htmlSVG to debug

saveResults(results =  svg_str, shape = "svg")
disconnectdbs()
