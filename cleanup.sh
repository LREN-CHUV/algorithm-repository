#!/bin/bash

echo "Remove old Docker images created for MIP"

tag=$@

if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER="docker"
else
    DOCKER="sudo docker"
fi

if [[ "$tag" == "" ]]; then
    echo "Usage: ./cleanup.sh <tag>"
    echo "where tag can be one of:"
    $DOCKER images | grep "hbpmip/" | awk '{print $2}' | sort | uniq
    exit 1
fi

# Remove exited containers
$DOCKER ps -q -f status=exited | xargs --no-run-if-empty $DOCKER rm

# Remove tagged images
for t in $tag; do
  $DOCKER images | grep "hbpmip/" | grep $t | cut -d' ' -f1 | sed -e "s/$/:$t/" | xargs --no-run-if-empty docker rmi
done

# Remove anomymous images
$DOCKER images -f "dangling=true" -q | xargs --no-run-if-empty $DOCKER rmi
