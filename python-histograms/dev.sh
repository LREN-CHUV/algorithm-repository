#!/usr/bin/env bash

docker run \
-e "JOB_ID=$(uuidgen)" \
-e "NODE=federation" \
-e "PARAM_variables=lefthippocampus" \
-e "PARAM_covariables=" \
-e "PARAM_grouping=DX" \
-e "PARAM_meta={\"righthippocampus\":{\"type\": \"real\"},\"leftventraldc\":{\"type\": \"real\"},\"rightventraldc\":{\"type\": \"real\"}}" \
-e "PARAM_query=select lefthippocampus, dx from ADNI_MERGE where lefthippocampus is not null and dx is not null" \
-e "IN_JDBC_URL=jdbc:postgresql://192.168.0.1:65432/postgres" \
-e "IN_JDBC_USER=postgres" \
-e "IN_JDBC_PASSWORD=test" \
-e "OUT_JDBC_URL=jdbc:postgresql://192.168.0.1:5432/postgres" \
-e "OUT_JDBC_USER=postgres" \
-e "OUT_JDBC_PASSWORD=test" \
hbpmip/python-histograms python histograms.py
