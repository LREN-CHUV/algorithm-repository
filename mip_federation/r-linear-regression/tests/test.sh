#!/bin/sh -e

docker run --rm --link test-postgres:postgres \
  -e REQUEST_ID=001 \
  -e IN_JDBC_DRIVER=org.postgresql.Driver \
  -e IN_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.3-1103.jdbc41.jar \
  -e IN_JDBC_URL=jdbc:postgresql://postgres:5432/postgres \
  -e IN_JDBC_USER=postgres \
  -e IN_JDBC_PASSWORD=test \
  -e OUT_JDBC_DRIVER=org.postgresql.Driver \
  -e OUT_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.3-1103.jdbc41.jar \
  -e OUT_JDBC_URL=jdbc:postgresql://postgres:5432/postgres \
  -e OUT_JDBC_USER=postgres \
  -e OUT_JDBC_PASSWORD=test \
  -e INPUT_TABLE=test.results_linear_regression \
  -e RESULT_TABLE=test.federation_results_linear_regression \
  registry.federation.mip.hbp/mip_federation/r-linear-regression-test test
