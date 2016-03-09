#!/bin/bash -e

OPTS=""
OPERATION="test"

if [ "$1" = "--interactive" ]; then
  OPTS="-i -t"
  OPERATION="R"
fi

echo "Starting the results database..."
../../tests/analytics-db/start-db.sh
echo
echo "Starting the local database..."
../../tests/dummy-ldsm/start-db.sh
echo

sleep 2

if groups $USER | grep &>/dev/null '\bdocker\b'; then
  DOCKER="docker"
else
  DOCKER="sudo docker"
fi

$DOCKER run --rm $OPTS \
  --link dummyldsm:indb \
  --link analyticsdb:outdb \
  -e JOB_ID=001 \
  -e NODE=job_test \
  -e PARAM_query="select tissue1_volume from brain_feature order by tissue1_volume" \
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
  -e OUT_FORMAT=INTERMEDIATE_RESULTS \
  hbpmip/r-summary-stats $OPERATION

../../tests/analytics-db/stop-db.sh
../../tests/dummy-ldsm/stop-db.sh
