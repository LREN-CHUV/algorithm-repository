#!/bin/sh

# Run this function in the data pipeline

id=$1

if [ -z "$id" ]; then
  id=001
fi

http -v PUT localhost:8087/job \
         requestId="$id" \
         dockerImage="registry.federation.mip.hbp/mip_federation/r-summary-stats:latest" \
         inputDb=local \
         outputDb=analytics \
         parameters:='{"PARAM_query":"select * from job_result_nodes where job_id='$id'", "PARAM_colnames":"tissue1_volume"}'
