#'
#' This script computes the t-Distributed Stochastic Neighbor Embedding.
#' The data (input parameters: variables, covariables, grouping) are obtained from the local databases using a specific query.
#' This query will be the same for all nodes.
#'
#' Environment variables:
#'
#' - Input Parameters:
#'      PARAM_query  : SQL query producing the dataframe to analyse
#'      PARAM_variables : Column separated list of variables
#'      PARAM_covariables : Column separated list of covariables
#'      PARAM_grouping : Column separated list of groupings
    dims: integer; Output dimensionality (default: 2)

initial_dims: integer; the number of dimensions that should be retained
          in the initial PCA step (default: 50)

perplexity: numeric; Perplexity parameter

   theta: numeric; Speed/accuracy trade-off (increase for less
          accuracy), set to 0.0 for exact TSNE (default: 0.5)

check_duplicates: logical; Checks whether duplicates are present. It is
          best to make sure there are no duplicates present and set
          this option to FALSE, especially for large datasets (default:
          TRUE)

     pca: logical; Whether an initial PCA step should be performed
          (default: TRUE)
max_iter: integer; Maximum number of iterations (default: 1000)

 verbose: logical; Whether progress updates should be printed (default:
          FALSE)

is_distance: logical; Indicate whether X is a distance matrix
          (experimental, default: FALSE)

  Y_init: matrix; Initial locations of the objects. If NULL, random
          initialization will be used (default: NULL). Note that when
          using this, the initial stage with false perplexity values
          and a larger momentum term will be skipped.

#' - Execution context:
#'      JOB_ID : ID of the job
#'      NODE : Node used for the execution of the script
#'      IN_JDBC_DRIVER : class name of the JDBC driver for input data
#'      IN_JDBC_JAR_PATH : path to the JDBC driver jar for input data
#'      IN_JDBC_URL : JDBC connection URL for input data
#'      IN_JDBC_USER : User for the database connection for input data
#'      IN_JDBC_PASSWORD : Password for the database connection for input data
#'      OUT_JDBC_DRIVER : class name of the JDBC driver for output results
#'      OUT_JDBC_JAR_PATH : path to the JDBC driver jar for output results
#'      OUT_JDBC_URL : JDBC connection URL for output results
#'      OUT_JDBC_USER : User for the database connection for output results
#'      OUT_JDBC_PASSWORD : Password for the database connection for output results
#'

suppressMessages(library(hbpjdbcconnect));
library(jsonlite);
library(whisker);
library(Rtsne);

# Initialisation
variables <- strsplit(Sys.getenv("PARAM_variables"), ",");
variables <- variables[lapply(variables,length)>0];
covariables <- strsplit(Sys.getenv("PARAM_covariables"), ",");
covariables <- covariables[lapply(covariables,length)>0];
groupingstr <- Sys.getenv("PARAM_grouping", "");
grouping <- if (groupingstr == "") list() else strsplit(groupingstr, ",");
docker_image <- Sys.getenv("DOCKER_IMAGE", "hbpmip/r-tsne:latest");

# Fetch the data
data <- fetchData();


# Perform the computation
res <- Rtsne(data, dims = 2, initial_dims = 50, perplexity = 30,
       theta = 0.5, check_duplicates = TRUE, pca = TRUE, max_iter = 1000,
       verbose = FALSE, is_distance = FALSE, Y_init = NULL);

# Build the response
coeff_names <- names(res$coefficients);
coeff_names[1] <- "_intercept_";

model_const <- res$coefficients[[1]];
model_coeff <- as.vector(res$coefficients[-1]);

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
store <- list(variables = toJSON(variables, auto_unbox=T),
              covariables = toJSON(covariables, auto_unbox=T),
              grouping = toJSON(c(paste(grouping, sep=":"))),
              sql = Sys.getenv("PARAM_query", ""),
              data_count = nrow(data),
              docker_image = docker_image,
              model_const = model_const,
              model_coeff = toJSON(model_coeff, digits = 8),
              if_anova = if_anova,
              anova_coeff_header = anova_coeff_header,
              anova_coeff_tail = anova_coeff_tail,
              anova_coefficients = unname(rowSplit(anova_coefficients)),
              anova_residuals = unname(rowSplit(anova_residuals)),
              summary_coefficients = unname(rowSplit(summary_coefficients)),
              summary_coefficient_names = summary_coefficient_names,
              summary_residuals = summary_residuals,
              summary_aliased = unname(rowSplit(summary_aliased)),
              summary_aliased_names = summary_aliased_names,
              summary_sigma = res$summary$sigma,
              summary_degrees_freedom = toJSON(summary_degrees_freedom),
              summary_r_squared = res$summary$r.squared,
              summary_adj_r_squared = res$summary$adj.r.squared,
              summary_cov_unscaled = toJSON(summary_cov_unscaled, digits = 8));

template <- readLines("/src/pfa.yml");

# Store results in the database
saveResults(whisker.render(template, store), shape = 'pfa_yaml');
