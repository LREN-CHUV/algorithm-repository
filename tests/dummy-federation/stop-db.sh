#!/bin/bash -e

if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER="docker"
else
    DOCKER="sudo docker"
fi

$DOCKER stop dummyfederation > /dev/null
$DOCKER rm dummyfederation > /dev/null
