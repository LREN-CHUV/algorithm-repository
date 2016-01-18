#!/bin/sh

git submodule sync
git submodule update --init
git submodule foreach git pull origin master
