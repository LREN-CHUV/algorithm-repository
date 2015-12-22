#!/bin/bash -e

function cheat_sheet() {

  echo "Cheat sheet - run the following commands:"
  echo
  echo "library(devtools)"
  echo
  echo "devtools::install_github(\"LREN-CHUV/hbpsummarystats\")"
  echo "  Load the library"
  echo
  echo "source(\"/src/main.R\")"
  echo "  Perform the computation"
  echo
  echo "lintr::lint_package()"
  echo "  Checks the style of the source code"
  echo
  echo "devtools::load_all()"
  echo "  Load the code in the current project"
  echo
  echo "devtools::document()"
  echo "  Generates the documentation"
  echo
  echo "devtools::use_testthat()"
  echo "  Setup the package to use testthat"
  echo
  echo "-----------------------------------------"

}

if [[ "$USER" == "vagrant" ]]; then

  cheat_sheet

  docker run -i -t --rm \
    -v $(pwd):/src/ \
    -v $(pwd)/tests:/src/tests/ \
    -e JOB_ID=001 \
    -e NODE=Test \
    -e PARAM_query="select * from job_result_nodes where job_id='001'" \
    -e PARAM_colnames="tissue1_volume" \
    -e IN_JDBC_DRIVER=org.postgresql.Driver \
    -e IN_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
    -e IN_JDBC_URL="jdbc:postgresql://172.17.42.1:31432/postgres" \
    -e IN_JDBC_USER=postgres \
    -e IN_JDBC_PASSWORD=vagrantadmin \
    -e OUT_JDBC_DRIVER=org.postgresql.Driver \
    -e OUT_JDBC_JAR_PATH=/usr/lib/R/libraries/postgresql-9.4-1201.jdbc41.jar \
    -e OUT_JDBC_URL="jdbc:postgresql://172.17.42.1:31432/analytics" \
    -e OUT_JDBC_USER=analytics \
    -e OUT_JDBC_PASSWORD=neuroinfo \
    registry.federation.mip.hbp/mip_tools/r-interactive R

else

  ../../tests/analytics-db/start-db.sh
  ../../tests/dummy-federation/start-db.sh
  
  sleep 2
  
  if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER="docker"
  else
    DOCKER="sudo docker"
  fi

  cheat_sheet

  $DOCKER run -i -t --rm \
    --link dummyfederation:indb \
    --link analyticsdb:outdb \
    -v $(pwd)/:/src/ \
    -v $(pwd)/tests:/src/tests/ \
    -e JOB_ID=001 \
    -e NODE=dev \
    -e PARAM_query="select * from job_result_nodes where job_id='001'" \
    -e PARAM_colnames="tissue1_volume" \
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
  ../../tests/dummy-federation/stop-db.sh

fi
