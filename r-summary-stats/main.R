#'
#' Computes the summary statistics.
#' The data are obtained from the local databases using a specific query.
#' This query will be the same for all nodes.
#'
#' Environment variables:
#'
#' - Input Parameters:
#'      PARAM_query  : SQL query producing the dataframe to analyse
#'      PARAM_variables : Column separated list of variables
#'      PARAM_covariables : Column separated list of covariables
#'      PARAM_grouping : Column separated list of groupings
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
library(hbpsummarystats);

# Initialisation
variables <- strsplit(Sys.getenv("PARAM_variables"), ",");
variables <- variables[lapply(variables,length)>0];
covariables <- strsplit(Sys.getenv("PARAM_covariables"), ",");
covariables <- covariables[lapply(covariables,length)>0];
groupingstr <- Sys.getenv("PARAM_grouping", "");
grouping <- if (groupingstr == "") list() else strsplit(groupingstr, ",");
docker_image <- Sys.getenv("DOCKER_IMAGE", "hbpmip/r-summary-stats:latest");

columns <- unique(c(variables, covariables, grouping));

# Fetch the data
data <- fetchData();

# Perform the computation
results <- as.data.frame(tablesummarystats(data, columns));

res <- as.data.frame(t(results));
res <- as.data.frame(cbind(name=rownames(res), res));

# Extract type = integer
intRows <- res[res$type == 'integer', ];
rownames(intRows) <- NULL;
if (nrow(intRows) == 0) {
	intRows <- c();
	intRowHeader <- c();
	intRowTail <- c();
} else {
	intRowHeader <- unname(rowSplit(intRows[1,]));
	intRowTail <- unname(rowSplit(intRows[-1,]));
	intRows <- unname(rowSplit(intRows));
}

# Extract type = numeric
numRows <- res[res$type == 'numeric', ];
rownames(numRows) <- NULL;
if (nrow(numRows) == 0) {
	numRows <- c();
	numRowHeader <- c();
	numRowTail <- c();
} else {
	numRowHeader <- unname(rowSplit(numRows[1,]));
	numRowTail <- unname(rowSplit(numRows[-1,]));
	numRows <- unname(rowSplit(numRows));
}

# Extract type = character with empty factors
charRows <- res[res$type == 'character', ];
strRows <- charRows[is.na(charRows$factors), ];
rownames(strRows) <- NULL;
if (nrow(strRows) == 0) {
	strRows <- c();
	strRowHeader <- c();
	strRowTail <- c();
} else {
	strRowHeader <- unname(rowSplit(strRows[1,]));
	strRowTail <- unname(rowSplit(strRows[-1,]));
	strRows <- unname(rowSplit(strRows));
}

# Extract type = character with factors
factorRows <- charRows[!is.na(charRows$factors), ];
rownames(factorRows) <- NULL;
if (nrow(factorRows) == 0) {
	factorRows <- c();
	factorRowHeader <- c();
	factorRowTail <- c();
} else {
	factorRows$factors <- sapply(factorRows$factors, toJSON);
	factorRowHeader <- unname(rowSplit(factorRows[1,]));
	factorRowTail <- unname(rowSplit(factorRows[-1,]));
	factorRows <- unname(rowSplit(factorRows));
}

# Ensure that we use only supported types: list, string
store <- list(
              variables = toJSON(variables, auto_unbox=T),
              covariables = toJSON(covariables, auto_unbox=T),
              grouping = toJSON(c(paste(grouping, sep=":"))),
              sql = Sys.getenv("PARAM_query", ""),
              data_count = nrow(data),
              docker_image = docker_image,
              intRowHeader = intRowHeader,
              intRowTail = intRowTail,
              intRows = intRows,
              numRowHeader = numRowHeader,
              numRowTail = numRowTail,
              numRows = numRows,
              strRowHeader = strRowHeader,
              strRowTail = strRowTail,
              strRows = strRows,
              factorRowHeader = factorRowHeader,
              factorRowTail = factorRowTail,
              factorRows = factorRows
    );

template <- readLines("/src/pfa.yml");

# Store results in the database
saveResults(whisker.render(template, store), fn = 'r-summary-stats', shape = 'pfa_yaml');
