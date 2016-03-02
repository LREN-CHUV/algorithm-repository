#
# This script computes the linear regression.
# The data (input parameters: y, A) are obtained from the local databases using a specific query.
# These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_query  : SQL query producing the dataframe to analyse
#      PARAM_varname : Name of the variable
#      PARAM_covarnames : Column separated list of covariables
#      PARAM_groups : Column separated list of groups
# - Execution context:
#      JOB_ID : ID of the job
#      NODE : Node used for the execution of the script
#      IN_JDBC_DRIVER : class name of the JDBC driver for input data
#      IN_JDBC_JAR_PATH : path to the JDBC driver jar for input data
#      IN_JDBC_URL : JDBC connection URL for input data
#      IN_JDBC_USER : User for the database connection for input data
#      IN_JDBC_PASSWORD : Password for the database connection for input data
#      OUT_JDBC_DRIVER : class name of the JDBC driver for output results
#      OUT_JDBC_JAR_PATH : path to the JDBC driver jar for output results
#      OUT_JDBC_URL : JDBC connection URL for output results
#      OUT_JDBC_USER : User for the database connection for output results
#      OUT_JDBC_PASSWORD : Password for the database connection for output results
#

suppressMessages(library(hbpjdbcconnect));
library(whisker);
library(hbplregress);

# Initialisation
varname <- Sys.getenv("PARAM_varname");
covarnames <- strsplit(Sys.getenv("PARAM_covarnames"), ",");
groupstr <- Sys.getenv("PARAM_groups", "");
if (groupstr == "") {
	groups <- c();
} else {
    groups <- strsplit(Sys.getenv("PARAM_groups", ""), ",");
}

# Fetch the data
data <- fetchData();

# Perform the computation
res <- LRegress_Node(data, varname, covarnames, groups);
coefficients <- as.data.frame(res$summary$coefficients);

summary <- list(names = colnames(coefficients),
	            coefficients = coefficients,
	            aliased = res$summary$aliased,
	            sigma = res$summary$sigma,
	            df = res$summary$df,
	            r_squared = res$summary$r.squared,
	            adj_r_squared = res$summary$adj.r.squared,
	            cov_unscaled = as.data.frame(res$summary$cov.unscaled)
	           );

#	            summary_residuals = res$summary$residuals,

template <- readLines("/src/pfa.yml");

# Ensure that we use only supported types: list, data.frame
store <- list(coefficients = res$coefficients, residuals = as.data.frame(res$residuals), anova = as.data.frame(res$anova), summary = summary);

# Store results in the database
saveResults(store, fn = 'r-linear-regression');
