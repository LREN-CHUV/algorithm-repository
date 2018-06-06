#!/usr/bin/env bash

set -o pipefail  # trace ERR through pipes
set -o errtrace  # trace ERR through 'time command' and other functions
set -o errexit   ## set -e : exit the script if any statement returns a non-true return value

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

cd "$(get_script_dir)"

cleanup=1
for param in "$@"
do
  if [ "--no-cleanup" == "$param" ]; then
    cleanup=0
    echo "INFO: --no-cleanup option detected !"
  fi
done

if [[ $NO_SUDO || -n "$CIRCLECI" ]]; then
  DOCKER_COMPOSE="docker-compose"
elif groups $USER | grep &>/dev/null '\bdocker\b'; then
  DOCKER_COMPOSE="docker-compose"
else
  DOCKER_COMPOSE="sudo docker-compose"
fi

function _cleanup() {
  local error_code="$?"
  echo "Stopping the containers..."
  $DOCKER_COMPOSE stop | true
  $DOCKER_COMPOSE down | true
  $DOCKER_COMPOSE rm -f > /dev/null 2> /dev/null | true
  exit $error_code
}

if [[ "$cleanup" == 1 ]]; then
trap _cleanup EXIT INT TERM
fi

echo "Starting the databases..."
$DOCKER_COMPOSE up -d --remove-orphans db
$DOCKER_COMPOSE run wait_dbs
$DOCKER_COMPOSE run create_dbs

echo
echo "Initialise the databases..."
$DOCKER_COMPOSE run sample_data_db_setup
$DOCKER_COMPOSE run woken_db_setup

echo
echo "Run the CLUS PCT algorithm for single-target classification..."
$DOCKER_COMPOSE run clus_pct_classification_st compute
echo "Run the CLUS PCT algorithm for single-target regression..."
$DOCKER_COMPOSE run clus_pct_regression_st compute
# echo "Run the CLUS PCT algorithm for multi-target classification..."
# $DOCKER_COMPOSE run clus_pct_classification_mt compute
# echo "Run the CLUS PCT algorithm for multi-target regression..."
# $DOCKER_COMPOSE run clus_pct_regression_mt compute

echo
echo "Running PFA validation..."
$DOCKER_COMPOSE run pfa_validator_classification_st
$DOCKER_COMPOSE run pfa_validator_regression_st
# $DOCKER_COMPOSE run pfa_validator_classification_mt
# $DOCKER_COMPOSE run pfa_validator_regression_mt

echo
# Cleanup
if [[ "$cleanup" == 1 ]]; then
_cleanup
fi
