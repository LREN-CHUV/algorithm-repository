#!/usr/bin/env bash

docker run \
-e "JOB_ID=$(uuidgen)" \
-e "NODE=federation" \
-e "PARAM_variables=rightorifgorbitalpartoftheinferiorfrontalgyrus" \
-e "PARAM_grouping=DX" \
-e "PARAM_query=select * from ADNI_MERGE" \
-e "IN_JDBC_URL=jdbc:postgresql://192.168.0.1:65432/science" \
-e "IN_JDBC_USER=science" \
-e "IN_JDBC_PASSWORD=sciencepass" \
-e "OUT_JDBC_URL=jdbc:postgresql://192.168.0.1:65431/postgres" \
-e "OUT_JDBC_USER=postgres" \
-e "OUT_JDBC_PASSWORD=test" \
hbpmip/python-histograms python histograms.py
