#! /bin/sh -e

docker stop test-postgres > /dev/null
docker rm test-postgres > /dev/null
