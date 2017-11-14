#!/usr/bin/env bash

docker run \
-e "JOB_ID=$(uuidgen)" \
-e "NODE=federation" \
-e "PARAM_variables=Name" \
-e "PARAM_covariables=SepalLength,SepalWidth,PetalLength,PetalWidth" \
-e "PARAM_query=select Name,SepalLength,SepalWidth,PetalLength,PetalWidth from sample_data where Name is not null and SepalLength is not null and SepalWidth is not null and PetalLength is not null and PetalWidth is not null" \
-e "PARAM_meta={\"Name\":{\"code\":\"Name\",\"type\":\"string\"},\"SepalLength\":{\"code\":\"SepalLength\",\"type\":\"real\"},\"SepalWidth\":{\"code\":\"SepalWidth\",\"type\":\"real\"},\"PetalLength\":{\"code\":\"PetalLength\",\"type\":\"real\"}, \"PetalWidth\":{\"code\":\"PetalWidth\",\"type\":\"real\"}}" \
-e "IN_JDBC_URL=jdbc:postgresql://172.18.0.1:5432/features" \
-e "IN_JDBC_USER=features" \
-e "IN_JDBC_PASSWORD=featurespwd" \
-e "OUT_JDBC_URL=jdbc:postgresql://172.18.0.1:5432/woken" \
-e "OUT_JDBC_USER=woken" \
-e "OUT_JDBC_PASSWORD=wokenpwd" \
-e "PARAM_MODEL_perplexity=30" \
-e "PARAM_MODEL_theta=0.5" \
-e "PARAM_MODEL_iterations=1000" \
-e "PARAM_MODEL_target_dimensions=2" \
-e "PARAM_MODEL_do_zscore=True" \
hbpmip/python-tsne compute
