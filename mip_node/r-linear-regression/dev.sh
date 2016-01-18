#!/bin/bash -e

function cheat_sheet() {

  echo "Cheat sheet - run the following commands:"
  echo
  echo "library(devtools)"
  echo
  echo "devtools::install_github(\"LREN-CHUV/hbplregress\")"
  echo "  Load the library"
  echo
  echo "source(\"/src/main.R\")"
  echo "  Perform the computation"
  echo
  echo "lintr::lint(\"/src/main.R\")"
  echo "  Checks the style of the source code"
  echo
  echo "-----------------------------------------"

}

echo "Starting the results database..."
../../tests/analytics-db/start-db.sh
echo "Starting the local database..."
../../tests/dummy-ldsm/start-db.sh

sleep 2
  
if groups $USER | grep &>/dev/null '\bdocker\b'; then
  DOCKER="docker"
else
  DOCKER="sudo docker"
fi

cheat_sheet

$DOCKER run -i -t --rm \
  --link dummyldsm:indb \
  --link analyticsdb:outdb \
  -v $(pwd)/:/src/ \
  -v $(pwd)/tests:/src/tests/ \
  -e JOB_ID=002 \
  -e NODE=dev \
  -e PARAM_query="select feature_name, tissue1_volume from brain_feature order by tissue1_volume" \
  -e PARAM_varname="feature_name" \
  -e PARAM_covarnames="tissue1_volume" \
  -e IN_JDBC_DRIVER=org.postgresql.Driver \
  -e IN_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
  -e IN_JDBC_URL="jdbc:postgresql://indb:5432/postgres" \
  -e IN_JDBC_USER=postgres \
  -e IN_JDBC_PASSWORD=test \
  -e OUT_JDBC_DRIVER=org.postgresql.Driver \
  -e OUT_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
  -e OUT_JDBC_URL="jdbc:postgresql://outdb:5432/postgres" \
  -e OUT_JDBC_USER=postgres \
  -e OUT_JDBC_PASSWORD=test \
  registry.federation.mip.hbp/mip_tools/r-interactive R

../../tests/analytics-db/stop-db.sh
../../tests/dummy-ldsm/stop-db.sh
