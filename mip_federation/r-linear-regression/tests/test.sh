#!/bin/sh -e

../../tests/analytics-db/start-db.sh
../../tests/dummy-federation/start-db.sh

sleep 2

docker run --rm \
  --link dummyfederation:indb \
  --link analyticsdb:outdb \
  -e JOB_ID=001 \
  -e NODE=job_test \
  -e PARAM_query="select * from job_result_nodes where job_id='001'" \
  -e PARAM_colnames="tissue1_volume" \
  -e IN_JDBC_DRIVER=org.postgresql.Driver \
  -e IN_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
  -e IN_JDBC_URL=jdbc:postgresql://indb:5432/postgres \
  -e IN_JDBC_USER=postgres \
  -e IN_JDBC_PASSWORD=test \
  -e OUT_JDBC_DRIVER=org.postgresql.Driver \
  -e OUT_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
  -e OUT_JDBC_URL=jdbc:postgresql://outdb:5432/postgres \
  -e OUT_JDBC_USER=postgres \
  -e OUT_JDBC_PASSWORD=test \
  registry.federation.mip.hbp/mip_federation/r-linear-regression-test test

../../tests/analytics-db/stop-db.sh
../../tests/dummy-federation/stop-db.sh

