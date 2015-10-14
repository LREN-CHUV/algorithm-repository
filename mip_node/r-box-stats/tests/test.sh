#!/bin/sh -e

docker run --rm --link test-postgres:postgres \
  -e REQUEST_ID=001 \
  -e NODE=Test \
  -e PARAM_query="select tissue1_volume from brain_feature order by tissue1_volume" \
  -e PARAM_colnames="tissue1_volume" \
  -e IN_JDBC_DRIVER=org.postgresql.Driver \
  -e IN_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
  -e IN_JDBC_URL="jdbc:postgresql://postgres:5432/test?currentSchema=public" \
  -e IN_JDBC_USER=test \
  -e IN_JDBC_PASSWORD=test \
  -e IN_SCHEMA=public \
  -e OUT_JDBC_DRIVER=org.postgresql.Driver \
  -e OUT_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
  -e OUT_JDBC_URL="jdbc:postgresql://postgres:5432/test?currentSchema=public" \
  -e OUT_JDBC_USER=test \
  -e OUT_JDBC_PASSWORD=test \
  -e OUT_SCHEMA=public \
  -e RESULT_TABLE=result_box_stats \
  registry.federation.mip.hbp/mip_node/r-box-stats-test test
