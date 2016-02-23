#!/bin/bash -e

if groups $USER | grep &>/dev/null '\bdocker\b'; then
    DOCKER="docker"
else
    DOCKER="sudo docker"
fi

$DOCKER stop dummyldsm > /dev/null
$DOCKER rm dummyldsm > /dev/null
