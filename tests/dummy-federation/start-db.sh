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

if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER=docker
else
    DOCKER=sudo docker
fi

$DOCKER rm --force dummyfederation 2> /dev/null | true
$DOCKER run --name dummyfederation \
    -v $(get_script_dir):/tests \
    -e POSTGRES_PASSWORD=test -d postgres:9.4.5

$DOCKER exec dummyfederation \
    /bin/bash -c 'while ! pg_isready -U postgres ; do sleep 1; done && exec psql -U postgres -f /tests/create.sql'
