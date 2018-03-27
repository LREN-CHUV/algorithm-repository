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

# single-node case
# echo
# echo "Run the distributed-knn-single..."
# $DOCKER_COMPOSE run distributed-knn-single compute

echo
echo "Run the distributed-knn-a..."
$DOCKER_COMPOSE run distributed-knn-a compute --mode intermediate
echo "Run the distributed-knn-b..."
$DOCKER_COMPOSE run distributed-knn-b compute --mode intermediate
echo "Run the distributed-knn-agg..."
$DOCKER_COMPOSE run distributed-knn-agg compute --mode aggregate --job-ids 1 2

echo
echo "Run PFA validator (skipped)..."
# $DOCKER_COMPOSE run pfa_validator

echo
# Cleanup
if [[ "$cleanup" == 1 ]]; then
  _cleanup
fi
