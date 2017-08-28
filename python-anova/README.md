# Python Anova


## What is it ?

This is a Python script that generates anova.


## How to build a Docker image

Run: `./build.sh`


## How to try it when developing

Run: `./dev.sh`


## Method specific parameters

Use the `PARAM_MODEL_design` environment variable to choose an Anova multi-factors design.
The possible values are:
* factorial: a factorial design (all interactions are taken)
* additive: an additive design (no interaction is taken)
