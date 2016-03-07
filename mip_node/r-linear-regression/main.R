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

model_const <- res$coefficients[[1]];
model_coeff <- as.data.frame(cbind(coeff_names[-1], res$coefficients[-1]));
colnames(model_coeff) <- c("coeff_name", "coefficient");
model_names <- coeff_names[-1];

if (length(res$anova) == 1 && is.na(res$anova)) {
    anova <- matrix(nrow=0,ncol=0);
    if_anova <- FALSE;
} else {
    if_anova <- TRUE;
    anova_residuals <- res$anova[nrow(res$anova),];
    colnames(anova_residuals) <- c("degree_freedom", "sum_sq", "mean_sq", "f_value", "p_value");
    anova_coefficients <- res$anova[-nrow(res$anova),];
    anova_coefficients <- as.data.frame(cbind(rownames(anova_coefficients), anova_coefficients));
    colnames(anova_coefficients) <- c("coeff_name", "degree_freedom", "sum_sq", "mean_sq", "f_value", "p_value");
    anova_coeffs <- as.list(rownames(anova_coefficients));
    anova_coeff_header <- anova_coeffs[[1]];
    anova_coeff_tail <- anova_coeffs[-1];
}

summary_coefficients <- as.data.frame(cbind(coeff_names, res$summary$coefficients));
colnames(summary_coefficients) <- c("coeff_name", "estimate", "std_error", "t_value", "p_value");
summary_coefficient_names <- rownames(summary_coefficients);
summary_coefficient_names <- summary_coefficient_names[-1];

summary_aliased <- as.data.frame(cbind(coeff_names, sapply(res$summary$aliased, function(x) {tolower(as.character(x))} )));
colnames(summary_aliased) <- c("coeff_name", "aliased");
summary_aliased_names <- rownames(summary_aliased);
summary_aliased_names <- summary_aliased_names[-1];

summary_degrees_freedom <- as.vector(res$summary$df);

summary_cov_unscaled <- as.matrix(res$summary$cov.unscaled);

summary_residual_values  <- res$summary$residuals;
summary_residual_quantile <- quantile(summary_residual_values);
summary_residuals <- list(
  min = min(summary_residual_values),
  q1 = summary_residual_quantile[[2]],
  median = median(summary_residual_values),
  q3 = summary_residual_quantile[[4]],
  max = max(summary_residual_values));

# Ensure that we use only supported types: list, string
store <- list(variable = varname,
              covariables = toJSON(covarnames, auto_unbox=T),
              groups = toJSON(c(paste(groups, sep=":"))),
              model_names = model_names,
              model_const = model_const,
              model_coeff = unname(rowSplit(model_coeff)),
              if_anova = if_anova,
              anova_coeff_header = anova_coeff_header,
              anova_coeff_tail = anova_coeff_tail,
              anova_coefficients = anova_coefficients,
              anova_residuals = anova_residuals,
              summary_coefficients = unname(rowSplit(summary_coefficients)),
              summary_coefficient_names = summary_coefficient_names,
              summary_residuals = summary_residuals,
              summary_aliased = unname(rowSplit(summary_aliased)),
              summary_aliased_names = summary_aliased_names,
              summary_sigma = res$summary$sigma,
              summary_degrees_freedom = toJSON(summary_degrees_freedom),
              summary_r_squared = res$summary$r.squared,
              summary_adj_r_squared = res$summary$adj.r.squared,
              summary_cov_unscaled = toJSON(summary_cov_unscaled));

template <- readLines("/src/pfa.yml");

# Store results in the database
saveResults(whisker.render(template, store), fn = 'r-linear-regression', shape = 'pfa_yaml');
