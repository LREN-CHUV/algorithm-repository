#'
#' This script generates  ...
#' The data are obtained from the local databases using a specific query.
#' This query will be the same for all nodes.
#'
#' The environment variables are:
#'
#' * Input Parameters (for 3c):
#'   - PARAM_query  : SQL query producing the dataframe to analyse
#'   - PARAM_variables : The variables to pass to y1 (Disease Diagnosis)
#'   - PARAM_covariables1 : The variables to pass to X1 (Clinical Measures)
#'   - PARAM_covariables2 : The variables to pass to X2 (Potential Biomarkers)
#'   - PARAM_* : any other parameters to pass to the R function. See example in the docker-compose file.
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

pdf(NULL) # do not plot
library(rmipadaptor)
library(CCC)
library(aurelius)

## for debugging only (5 lines):
# Sys.setenv(PARAM_variables = "churn")
# Sys.setenv(PARAM_covariables1 = "day_mins,day_calls,day_charge,eve_mins,eve_calls,eve_charge,night_mins,night_calls,night_charge")
# Sys.setenv(PARAM_covariables2 = "intl_mins,intl_calls,intl_charge,custserv_calls")
# Sys.setenv(PARAM_n_clusters = 3)
# data <- read.csv("../sample-data-db-setup/sql/churn.csv")[1:500,]

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

## remap variables to fit CCC functions
columns1 <- if (var_list$covariables1 == "") stop("missing PARAM_covariables1") else unlist(strsplit(var_list$covariables1, split = ","))
columns2 <- if (var_list$covariables2 == "") stop("missing PARAM_covariables2") else unlist(strsplit(var_list$covariables2, split = ","))
y <- var_list$variables
## convert to numeric the following input variables:
numeric_inputs <- c()
for (i in seq_along(var_list))
  if (names(var_list[i]) %in% numeric_inputs) var_list[i] <- as.numeric(var_list[i])

## run the main script
C2_results <- C2(data[,columns1], data[,y],
                 feature_selection_method="RF",
                 num_clusters_method="Manhattan",
                 clustering_method="Manhattan",
                 plot.num.clus=FALSE, plot.clustering=FALSE,
                 k=as.numeric(var_list$n_clusters))

new_y <- C2_results[[3]]

C3_results <- C3(PBx = data[,columns2], newy = new_y,
                 feature_selection_method = "RF",
                 classification_method="RF")

# table(new_y, C3_results[[2]])

model_as_pfa <- pfa(model)
write_pfa(model_as_pfa,file = "/tmp/model.pfa")
model_string <- paste0(readLines(con = "/tmp/model.pfa"),collapse = "\n")
saveResults(results = model_string,shape = "pfa")
disconnectdbs()
