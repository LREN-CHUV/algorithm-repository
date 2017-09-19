#!/usr/bin/env bash

docker run \
-e "JOB_ID=$(uuidgen)" \
-e "NODE=federation" \
-e "PARAM_variables=iq" \
-e "PARAM_covariables=college_math,score_math_course1,score_math_course2" \
-e "PARAM_grouping=" \
-e "PARAM_meta={\"iq\":{\"code\":\"iq\",\"type\":\"real\"},\"college_math\":{\"code\":\"college_math\",\"type\":\"real\"},\"score_math_course1\":{\"code\":\"score_math_course1\",\"type\":\"real\"},\"score_math_course2\":{\"code\":\"score_math_course2\",\"type\":\"real\"}}" \
-e "PARAM_query=select iq,college_math,score_math_course1,score_math_course2 from sample_data where iq is not null and college_math is not null and score_math_course1 is not null and score_math_course2 is not null" \
-e "IN_JDBC_URL=jdbc:postgresql://172.18.0.1:5432/features" \
-e "IN_JDBC_USER=postgres" \
-e "IN_JDBC_PASSWORD=test" \
-e "OUT_JDBC_URL=jdbc:postgresql://172.18.0.1:5432/woken" \
-e "OUT_JDBC_USER=woken" \
-e "OUT_JDBC_PASSWORD=wokenpwd" \
-e "PARAM_MODEL_perplexity=30" \
-e "PARAM_MODEL_theta=0.5" \
-e "PARAM_MODEL_iterations=1000" \
-e "PARAM_MODEL_target_dimensions=2" \
-e "PARAM_MODEL_do_zscore=True"
hbpmip/python-tsne compute
