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

DIR="$(get_script_dir)"

docker run --name test-postgres -e POSTGRES_PASSWORD=test -d postgres:9.3.9

docker run --rm --link test-postgres:postgres \
    -v $DIR:/tests \
    -e PGPASSWORD=test postgres:9.3.9 \
    /bin/bash -c 'while ! pg_isready -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres ; do sleep 1; done && exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres -f /tests/create.sql'
