#!/bin/bash -e

get_script_dir () {
     SOURCE="${BASH_SOURCE[0]}"

     while [ -h "$SOURCE" ]; do
          DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
          SOURCE="$( readlink "$SOURCE" )"
          [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
     done
     cd -P "$( dirname "$SOURCE" )"
     pwd
}

ROOT_DIR="$(get_script_dir)/../.."

OPTS=""
OPERATION="test"

if [ "$1" = "--interactive" ]; then
  OPTS="-i -t"
  OPERATION="R"
fi

echo "Starting the results database..."
$ROOT_DIR/tests/analytics-db/start-db.sh
echo
echo "Starting the local database..."
$ROOT_DIR/tests/dummy-ldsm/start-db.sh
echo

function _cleanup() {
  local error_code="$?"
  echo "Stopping the databases..."
  $ROOT_DIR/tests/analytics-db/stop-db.sh
  $ROOT_DIR/tests/dummy-ldsm/stop-db.sh
  exit $error_code
}
trap _cleanup EXIT INT TERM

sleep 2

if groups $USER | grep &>/dev/null '\bdocker\b'; then
  DOCKER="docker"
else
  DOCKER="sudo docker"
fi

$DOCKER run --rm $OPTS \
  --link dummyldsm:indb \
  --link analyticsdb:outdb \
  -e NODE=job_test \
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
