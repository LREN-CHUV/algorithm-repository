#!/bin/bash

tag=$1

if [[ "$tag" == "" ]]; then
	echo "Usage: ./cleanup.sh <tag>"
	exit 1
fi

docker images | grep "registry.federation.mip.hbp/" | grep $tag | cut -d' ' -f1 | sed -e "s/$/:$tag/" | xargs docker rmi
