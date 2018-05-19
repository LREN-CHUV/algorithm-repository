[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--rm-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-rm/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-rm.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-rm/tags "hbpmip/java-jsi-clus-rm image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-rm.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-rm "hbpmip/java-jsi-clus-rm on microbadger")

# hbpmip/java-jsi-clus-rm: Redescription Mining using Predictive Clustering from JSI and IRB

Implementation of the Redescription mining algorithm based on Predictive Clustering Trees. 
For more details see https://github.com/matmih/CLUS-RM-library.

## Usage

```sh
  docker run --rm --env [list of environment variables] hbpmip/java-jsi-clus-rm compute
```

where the environment variables are:

* NODE: name of the node (machine) used for execution
* JOB_ID: ID of the job.
* IN_JDBC_DRIVER: org.postgresql.Driver
* IN_JDBC_URL: URL to the input database, e.g. jdbc:postgresql://db:5432/features
* IN_JDBC_USER: User for the input database
* IN_JDBC_PASSWORD: Password for the input database
* OUT_JDBC_DRIVER: org.postgresql.Driver
* OUT_JDBC_URL: URL to the output database, jdbc:postgresql://db:5432/woken
* OUT_JDBC_USER: User for the output database
* OUT_JDBC_PASSWORD: Password for the output database
* PARAM_covariables: Attributes contained in the first data view.
* PARAM_variables: Attributes contained in the second data view.
* PARAM_query: Query selecting the data to feed into the algorithm for training
* MODEL_PARAM_minJS: Specify minimal redescription accuracy (measured with Jaccard index) required to return it to the user. Parameter values are contained in [0,1]. (default is MODEL_PARAM_minJS=0.5)
* MODEL_PARAM_maxPval: Specify maximal redescription p-value required to return it to the user. Parameter values are contained in [0,1]. (default is MODEL_PARAM_maxPval=0.01)		
* MODEL_PARAM_MinSupport: Specify minimal redescription support required to return it to the user. Parameter values are contained in [1,|E|], where |E| denotes number of entities in the dataset. (This parameter MUST be defined by the user and is domain and data dependent).
* MODEL_PARAM_MaxSupport: Specify maximal redescription support allowed. Parameter values are contained in [1,|E|], where |E| denotes number of entities in the dataset. (default is MODEL_PARAM_MaxSupport = |E|).
* MODEL_PARAM_numRandomRestarts: Specify the number of random initialization steps performed by the CLUS-RM (the default is MODEL_PARAM_numRandomRestarts = 1).
* MODEL_PARAM_numIterations: Specify the number of iterations (also called alternations) performed by the CLUS-RM (the default is MODEL_PARAM_numIterations = 10).
* MODEL_PARAM_numRetRed: Specify the number of redescriptions to be returned by the CLUS-RM (the default is MODEL_PARAM_numRetRed = 50).
* MODEL_PARAM_attributeImportanceW1: Specify the attribute importance, for attributes contained in view 1, used in constraint-based redescription mining (the default is MODEL_PARAM_attributeImportanceW1 = "none"). Possible values are: "none" - allow redescriptions with any attributes from view1, "suggested" - allow defining combinations of attributes that increase redescription score (redescriptions containing specified attributes are preferred), "soft" - only return redescriptions satisfying at least part of specified constraints to the user (redescriptions satisfying larger portion of constraint set are preferred), "hard" - only return redescriptions satisfying all constraints defined in one constraint set. 
* MODEL_PARAM_attributeImportanceW2: Specify the attribute importance, for attributes contained in view 2, used in constraint-based redescription mining (the default is MODEL_PARAM_attributeImportanceW1 = "none"). Possible values are: "none" - allow redescriptions with any attributes from view2, "suggested" - allow defining combinations of attributes that increase redescription score (redescriptions containing specified attributes are preferred), "soft" - only return redescriptions satisfying at least part of specified constraints to the user (redescriptions satisfying larger portion of constraint set are preferred), "hard" - only return redescriptions satisfying all constraints defined in one constraint set. 
* MODEL_PARAM_importantAttributesW1: defines constraint sets, for attributes contained in view 1, to be used in constraint-based redescription mining (default is MODEL_PARAM_importantAttributesW1=""). Constraints are specified in the format "{a;b;c},{a;d}", where a,b,c,d are some attributes contained in the first view (view1) of the data.
* MODEL_PARAM_importantAttributesW2: defines constraint sets, for attributes contained in view 2, to be used in constraint-based redescription mining (default is MODEL_PARAM_importantAttributesW1=""). Constraints are specified in the format "{e;f;g},{h;i}", where e,f,g,h,i are some attributes contained in the second view (view2) of the data.
