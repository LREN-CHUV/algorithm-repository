#
# This script computes the linear regression.
# The data (input parameters: y, A) are obtained from the local databases using a specific query.
# These queries will be the same for all nodes.
# 
# Environment variables:
# 
# - Input Parameters:
#      PARAM_y  : SQL query producing the y parameter of L_Regress_Node
#      PARAM_A : SQL query producing the A parameter of L_Regress_Node
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

library(hbplregress)
library(hbpjdbcconnect);

# Initialisation
yQuery <- Sys.getenv("PARAM_y")
A_Query <- Sys.getenv("PARAM_A")

# Fetch the data
y <- unlist(fetchData(yQuery));
A <- unlist(fetchData(A_Query));

if (length(A) %% length(y) != 0) stop(paste('Length of A is not a multiple of y, found length(A)=', length(A), " and length(y)=", length(y)))

# Perform the computation

A <- matrix(data = A, nrow = length(y), ncol = length(A) / length(y))
res <- LRegress_Node(y, A)

res <- as.data.frame(res);

# Store results in the database
saveResults(res);
