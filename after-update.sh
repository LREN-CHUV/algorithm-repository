#!/bin/sh

git submodule sync
git submodule update --init
if [ "$IN_SUBMODULE" = "true" ]; then
  git clean -f -d
fi
