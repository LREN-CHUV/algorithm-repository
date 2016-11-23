#!/usr/bin/env bash

docker run \
-e "META_DB_HOST=172.17.0.1" \
-e "META_DB_PORT=65433" \
-e "META_DB_NAME=meta" \
-e "META_DB_USER=meta" \
-e "META_DB_PASSWORD=metapass" \
-e "SCIENCE_DB_HOST=172.17.0.1" \
-e "SCIENCE_DB_PORT=65432" \
-e "SCIENCE_DB_NAME=science" \
-e "SCIENCE_DB_USER=science" \
-e "SCIENCE_DB_PASSWORD=sciencepass" \
-e "ANALYTICS_DB_HOST=172.17.0.1" \
-e "ANALYTICS_DB_PORT=65431" \
-e "ANALYTICS_DB_NAME=postgres" \
-e "ANALYTICS_DB_USER=postgres" \
-e "ANALYTICS_DB_PASSWORD=test" \
-e "VARIABLE=DX" \
-e "GROUPS=PTGENDER,DX,APOE4,AgeGroup" \
-e "JOB_ID=$(uuidgen)" \
-e "NODE=federation" \
hbpmip/python-histograms python histograms.py
