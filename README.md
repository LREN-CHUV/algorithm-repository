[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/a170b1b08f81441f85c004480ddaac0f)](https://www.codacy.com/app/hbp-mip/algorithm-repository?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=HBPMedical/algorithm-repository&amp;utm_campaign=Badge_Grade) [![CircleCI](https://circleci.com/gh/HBPMedical/algorithm-repository.svg?style=svg)](https://circleci.com/gh/HBPMedical/algorithm-repository)

# Algorithm repository

This is the repository of algorithms for the [MIP](https://mip.humanbrainproject.eu).

Algorithms, written in their native language (R, Matlab, Python, Java...) are encapsulated in a Docker container that provides them with the runtime environment necessary to execute this function.

The environment variables provided to the Docker container are used as parameters to the function or algorithm to execute.

Currently, we expect the Docker containers to be autonomous:

* they should connect to a database and retrieve the dataset to process
* they should process the data, taking into account the parameters given as environment variables to the Docker container
* they should store the results into the results database.

The format of the results should be easily shared.

* For algorithms providing statistical analysis or machine learning, we require the results to be in [PFA format](http://dmg.org/pfa/) in its YAML or JSON form.
* For algorithms providing visualisations, we support different formats, including Highcharts, Vis.js, PNG and SVG.
* For algorithms providing tabular data, we expect a JSON output in this format: [Tabular Data Resource](https://github.com/frictionlessdata/specs/blob/master/specs/tabular-data-resource.md)

# Acknowledgements

This work has been funded by the European Union Seventh Framework Program (FP7/2007­2013) under grant agreement no. 604102 (HBP)

This work is part of SP8 of the Human Brain Project (SGA1).
