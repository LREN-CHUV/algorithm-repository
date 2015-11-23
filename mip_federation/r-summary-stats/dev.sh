#!/bin/bash -e

if [[ "$USER" == "vagrant" ]]; then

  docker run -i -t --rm \
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
    -e RESULT_TABLE=result_summary_stats \
    registry.federation.mip.hbp/mip_federation/r-summary-stats-test R

else

  ../../tests/analytics-db/start-db.sh
  ../../tests/dummy-federation/start-db.sh
  
  sleep 2
  
  if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER="docker"
  else
    DOCKER="sudo docker"
  fi

  $DOCKER run -i -t --rm \
    --link dummyfederation:indb \
    --link analyticsdb:outdb \
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
    registry.federation.mip.hbp/mip_federation/r-summary-stats-test shell

  ../../tests/analytics-db/stop-db.sh
  ../../tests/dummy-federation/stop-db.sh

fi
