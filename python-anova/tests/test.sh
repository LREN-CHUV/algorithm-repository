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
trap _cleanup EXIT INT TERM

echo "Starting the databases..."
$DOCKER_COMPOSE up -d --remove-orphans db
$DOCKER_COMPOSE run wait_dbs
$DOCKER_COMPOSE run create_dbs

echo
echo "Initialise the databases..."
$DOCKER_COMPOSE run sample_data_db_setup
$DOCKER_COMPOSE run woken_db_setup

# single-node mode
echo
echo "Run the Anova algorithm..."
$DOCKER_COMPOSE run anova-single compute

# distributed mode - 1st phase
echo "Run the anova-a-1..."
$DOCKER_COMPOSE run anova-a-1 compute --mode intermediate-models
echo "Run the anova-b-1..."
$DOCKER_COMPOSE run anova-b-1 compute --mode intermediate-models
echo "Run the anova-agg-1..."
$DOCKER_COMPOSE run anova-agg-1 compute --mode aggregate-models --job-ids 1 2

# distributed mode - 2nd phase
echo "Run the anova-a-2..."
$DOCKER_COMPOSE run anova-a-2 compute --mode intermediate-anova --job-ids 3
echo "Run the anova-b-2..."
$DOCKER_COMPOSE run anova-b-2 compute --mode intermediate-anova --job-ids 3
echo "Run the anova-agg-2..."
$DOCKER_COMPOSE run anova-agg-2 compute --mode aggregate-anova --job-ids 4 5

echo
# Cleanup
_cleanup
