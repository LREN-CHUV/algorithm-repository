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
#'      PARAM_dims: integer; Output dimensionality (default: 2)
#'      PARAM_initial_dims: integer; the number of dimensions that should be retained
#'          in the initial PCA step (default: 50)
#'      PARAM_perplexity: numeric; Perplexity parameter (default: 1)
#'      PARAM_theta: numeric; Speed/accuracy trade-off (increase for less
#'          accuracy), set to 0.0 for exact TSNE (default: 0.5)
#'      PARAM_pca: logical; Whether an initial PCA step should be performed (default: TRUE)
#'      PARAM_max_iter: integer; Maximum number of iterations (default: 1000)
#'      PARAM_scale: logical; Whether to scale the covariables to  a mean of 0 and a standard deviation of 1 (default: FALSE)
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
variables    <- strsplit(Sys.getenv("PARAM_variables"), ",");
variables    <- variables[lapply(variables,length)>0];
covariables  <- strsplit(Sys.getenv("PARAM_covariables"), ",");
covariables  <- covariables[lapply(covariables,length)>0];
groupingstr  <- Sys.getenv("PARAM_grouping", "");
grouping     <- if (groupingstr == "") list() else strsplit(groupingstr, ",");
docker_image <- Sys.getenv("DOCKER_IMAGE", "hbpmip/r-tsne:latest");

dims         <- as.integer(Sys.getenv("PARAM_dims", 2));
initial_dims <- as.integer(Sys.getenv("PARAM_initial_dims", 50));
perplexity   <- as.numeric(Sys.getenv("PARAM_perplexity", 1));
theta        <- as.numeric(Sys.getenv("PARAM_theta", 0.5));
pca          <- as.logical(Sys.getenv("PARAM_pca", T));
max_iter     <- as.integer(Sys.getenv("PARAM_max_iter", 1000));
scale        <- as.logical(Sys.getenv("PARAM_scale", F));

parameters   <- list(dims = dims, initial_dims = initial_dims, perplexity = perplexity,
                                theta = theta, pca = tolower(pca), max_iter = max_iter);

# Fetch the data
data <- fetchData();
# Remove duplicates
data <- unique(data);

# Split data: covariables are used by tSNE, the other columns will be merged with the result
tsne_data <- as.data.frame(data[ , names(data) %in% unlist(covariables)]);

other_data <- as.data.frame(data[ , names(data) %in% c(unlist(variables), unlist(grouping))]);

if (scale) {
  tsne_data <- scale(tsne_data);
}

# Perform the computation
res <- Rtsne(tsne_data, dims = dims, initial_dims = initial_dims, perplexity = perplexity,
       theta = theta, pca = pca, max_iter = max_iter,
       check_duplicates = TRUE, verbose = FALSE, is_distance = FALSE, Y_init = NULL);

# Build the response

reduced_data <- as.data.frame(cbind(res$Y, other_data));

reduced_types <- sapply(reduced_data, class);
reduced_types_df <- data.frame(name=names(reduced_types), type=reduced_types, doc="");
reduced_defs <- apply(reduced_types_df[c('name','type','doc')], 1, function(y) {
  doc <- paste('Variable', y['name']);
  if (grepl("\\d+", y['name'])) {
    doc <- paste('Reduced dimension', y['name']);
  }
  switch(y['type'],
    character={
      if (length(data[,y['name']]) < 100) {
        toJSON(list(name=y['name'], type=list(type="enum", name=paste("Enum", y['name'], sep=''), symbols=levels(factor(data[,y['name']]))), doc=doc), auto_unbox=T)
      } else {
        toJSON(list(name=y['name'], type="string", doc=doc), auto_unbox=T)
      }
    },
    numeric=toJSON(list(name=y['name'], type="double", doc=doc), auto_unbox=T)
)});
reduced_defs <- as.list(reduced_defs);
names(reduced_defs) <- NULL;

reduced_values <- unname(rowSplit(reduced_data));
reduced_values <- sapply(reduced_values, function(row) {toJSON(as.list(row), auto_unbox=TRUE, digits=8, Date = "ISO8601")});

# Ensure that we use only supported types: list, string
store <- list(variables = toJSON(unlist(variables)),
              covariables = toJSON(unlist(covariables)),
              grouping = toJSON(unlist(grouping)),
              parameters = parameters,
              sql = Sys.getenv("PARAM_query", ""),
              data_count = nrow(data),
              docker_image = docker_image,
              reduced_defs = reduced_defs,
              reduced_values = reduced_values,
              summary_number_of_objects = res$N,
              summary_original_dimensionality = res$origD,
              summary_perplexity = res$perplexity,
              summary_theta = res$theta,
              summary_costs = toJSON(res$costs),
              summary_iter_costs = toJSON(res$itercosts)
              );

template <- readLines("/src/pfa.yml.whisker");

# Store results in the database
saveResults(whisker.render(template, store), shape = 'pfa_yaml');
