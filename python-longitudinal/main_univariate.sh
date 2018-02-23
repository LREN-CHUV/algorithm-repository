#!/usr/bin/env bash

cd longitudina/examples/scalar_models/univariate/sigmoid/
exec ../../../../build/Longitudina fit \
settings/model_settings.xml \
settings/algorithm_settings.xml \
settings/data_settings.xml \
settings/sampler_settings.xml \
0
echo "done"
cd output/
ls
