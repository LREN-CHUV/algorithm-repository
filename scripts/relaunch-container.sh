#!/bin/sh

container_id=$1

env=$(docker inspect $container_id | jq --raw-output '.. | .Env? | .[]? | (" -e \"" + . + "\"")')

image=$(docker inspect $container_id | jq --raw-output '[.. | .Config? | .Image?] | map(select(. != null))[0]')

docker run -it --rm $env $image

