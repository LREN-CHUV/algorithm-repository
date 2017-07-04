#!/usr/bin/env bash

docker run \
-e "JOB_ID=$(uuidgen)" \
-e "NODE=federation" \
-e "PARAM_variables=lefthippocampus" \
-e "PARAM_covariables=" \
-e "PARAM_grouping=alzheimerbroadcategory" \
-e "PARAM_meta={\"lefthippocampus\":{\"description\":\"\",\"methodology\":\"lren-nmm-volumes\",\"label\":\"Left Hippocampus\",\"code\":\"lefthippocampus\",\"units\":\"cm3\",\"length\":20,\"type\":\"real\"},\"alzheimerbroadcategory\":{\"enumerations\":[{\"code\":\"AD\",\"label\":\"Alzheimer's disease\"},{\"code\":\"CN\",\"label\":\"Cognitively Normal\"},{\"code\":\"Other\",\"label\":\"Other\"}],\"description\":\"There will be two broad categories taken into account. Alzheimer's disease (AD) in which the diagnostic is 100% certain and \\\"Other\\\" comprising the rest of Alzheimer's related categories. The \\\"Other\\\" category refers to Alzheime's related diagnosis which origin can be traced to other pathology eg. vascular. In this category MCI diagnosis can also be found. In summary, all Alzheimer's related diagnosis that are not pure.\",\"methodology\":\"mip-cde\",\"label\":\"Alzheimer Broad Category\",\"code\":\"alzheimerbroadcategory\",\"type\":\"polynominal\"}}" \
-e "PARAM_query=select lefthippocampus,alzheimerbroadcategory from merged_data where lefthippocampus is not null and alzheimerbroadcategory is not null and alzheimerbroadcategory != 'Other'" \
-e "IN_JDBC_URL=jdbc:postgresql://172.18.0.1:5432/features" \
-e "IN_JDBC_USER=features" \
-e "IN_JDBC_PASSWORD=featurespwd" \
-e "OUT_JDBC_URL=jdbc:postgresql://172.18.0.1:5432/woken" \
-e "OUT_JDBC_USER=woken" \
-e "OUT_JDBC_PASSWORD=wokenpwd" \
hbpmip/python-histograms compute
