#!/bin/bash -e
# ./start-db.sh -p port

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

DOCKER_PORT_OPTS=""
while getopts ":p:" opt; do
  case ${opt} in 
    p )
      DOCKER_PORT_OPTS="-p $OPTARG:5432"
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      ;;
  esac
done

shift $((OPTIND -1))
if pgrep -lf sshuttle > /dev/null ; then
  echo "sshuttle detected. Please close this program as it messes with networking and prevents Docker links to work"
  exit 1
fi

if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER="docker"
else
    DOCKER="sudo docker"
fi

$DOCKER rm --force dummyfederation 2> /dev/null | true
$DOCKER run --name dummyfederation $DOCKER_PORT_OPTS \
    -v $(get_script_dir)/sql:/docker-entrypoint-initdb.d/ \
    -e POSTGRES_PASSWORD=test -d postgres:9.6.3-alpine

$DOCKER exec dummyfederation \
    /bin/bash -c 'while ! pg_isready -U postgres ; do sleep 1; done'
