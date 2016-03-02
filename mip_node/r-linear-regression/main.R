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

# Build the response
coeff_names <- names(res$coefficients);
coeff_names[1] <- "_intercept_";

coefficients <- as.data.frame(cbind(coeff_names, res$coefficients));
colnames(coefficients) <- c("coeff_name", "coefficient");

if (is.na(res$anova)) {
    anova <- matrix(nrow=0,ncol=0);
    if_anova <- FALSE;
} else {
    anova <- as.matrix(res$anova);
    if_anova <- TRUE;
}

summary_coefficients <- as.data.frame(cbind(coeff_names, res$summary$coefficients));
colnames(summary_coefficients) <- c("coeff_name", "estimate", "std_error", "t_value", "p_value");

summary_aliased <- as.data.frame(cbind(coeff_names, res$summary$aliased));
colnames(summary_aliased) <- c("coeff_name", "aliased");

summary_degrees_freedom <- as.vector(res$summary$df);

summary_cov_unscaled <- as.matrix(res$summary$cov.unscaled);

# Ensure that we use only supported types: list, data.frame
store <- list(names = coeff_names,
              coefficients = unname(rowSplit(coefficients)),
              if_anova = if_anova,
              anova = toJSON(anova),
              summary_coefficients = unname(rowSplit(summary_coefficients)),
              summary_aliased = unname(rowSplit(summary_aliased)),
              summary_sigma = res$summary$sigma,
              summary_degrees_freedom = toJSON(summary_degrees_freedom),
              summary_r_squared = res$summary$r.squared,
              summary_adj_r_squared = res$summary$adj.r.squared,
              summary_cov_unscaled = toJSON(summary_cov_unscaled));
#                summary_residuals = res$summary$residuals,

template <- readLines("/src/pfa.yml");

# Store results in the database
saveResults(whisker.render(template, store), fn = 'r-linear-regression', shape = 'pfa_yaml');
