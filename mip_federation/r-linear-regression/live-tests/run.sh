#!/bin/sh

request_id=$(grep -E "request_id=.*" -o run.ini | cut -d'=' -f2)
http -v DELETE localhost:4400/scheduler/job/r-federation-linear-regression-$request_id

j2 run.json.j2 run.ini > run.json
http -v --json POST localhost:4400/scheduler/iso8601 < run.json

rm run.json
