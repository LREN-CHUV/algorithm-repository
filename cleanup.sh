#!/bin/bash

echo "Remove old Docker images created for MIP"

tag=$1

if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER="docker"
else
    DOCKER="sudo docker"
fi

if [[ "$tag" == "" ]]; then
    echo "Usage: ./cleanup.sh <tag>"
    echo "where tag can be one of:"
    $DOCKER images | grep "registry.federation.mip.hbp/" | awk '{print $2}' | sort | uniq
    exit 1
fi

# Remove exited containers
$DOCKER ps -q -f status=exited | xargs --no-run-if-empty $DOCKER rm

# Remove tagged images
$DOCKER images | grep "registry.federation.mip.hbp/" | grep $tag | cut -d' ' -f1 | sed -e "s/$/:$tag/" | xargs --no-run-if-empty docker rmi

# Remove anomymous images
$DOCKER images -f "dangling=true" -q | xargs --no-run-if-empty $DOCKER rmi
