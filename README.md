
# Functions repository

This is the repository of functions for the [MIP](https://mip.humanbrainproject.eu).

Functions, written in their native language (R, Matlab, Python, Java...) are encapsulated in a Docker container that provides them with the runtime environment necessary to execute this function.

The environment variables provided to the Docker container are used as parameters to the function or algorithm to execute.

Currently, we expect the Docker containers to be autonomous:

* they should connect to a database and retrieve the dataset to process
* they should process the data, taking into account the parameters given as environment variables to the Docker container
* they should store the results into the results database.

The format of the results should be easily shared. We are using the [PFA format](http://dmg.org/pfa/) here in its YAML form. It will get translated to JSON automatically be the workflow application which provides web services which execute this Docker container.
