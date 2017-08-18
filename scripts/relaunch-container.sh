#!/bin/sh

container_id=$1

env_file="$(mktemp)"
docker inspect $container_id | jq --raw-output '.. | .Env? | .[]?' > "$env_file"

image=$(docker inspect $container_id | jq --raw-output '[.. | .Config? | .Image?] | map(select(. != null))[0]')

docker run -it --rm --env-file "$env_file" "$image"

rm "$env_file"

