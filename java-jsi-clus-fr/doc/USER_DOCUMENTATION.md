[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--fr-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fr/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-fr.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fr/tags "hbpmip/java-jsi-clus-fr image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-fr.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-fr "hbpmip/java-jsi-clus-fr on microbadger")

# Feature ranking for structured outputs user reference manual

### Description:

Methods for feature ranking are used in many domains with many descriptive variables and high-dimensional problems. The obtained rankings (feature importance scores) provide an additional insight about the importance of the variables for the target and/or reduce the dimensionality of the problem. Many real-life problems have structured targets that need to be predicted. However, the task of feature ranking in the context of predicting structured target variables is more complex than the same task for simple classification or regression. Typical approaches for this task decompose the output to primitive components, perform feature ranking on these smaller problems, and then aggregate the resulting rankings into a single ranking. Such an approach ignores the dependencies between components of the structured target variable. This approach is based on ensembles of predictive clustering trees and treats structured variables directly.

### Parameters:

* Descriptive variables: A set of descriptive variables, whose rankings (importance scores) we are interested in. They can be numeric or categoric or mix of both types.

* Target variables: A set of one or more (dependent) variables in relation to which we are estimating the importance of descriptive variables. They can either be all numeric or all categoric.

* Number of decision trees in ensemble: In general, more trees in the ensemble improves the accuracy, but at the expense of a higher computational cost.

Reference: 
Petković, M., Džeroski, S., & Kocev, D. (2017, October). Feature Ranking for Multi-target Regression with Tree Ensemble Methods. In International Conference on Discovery Science (pp. 171-185). Springer, Cham. [URL](https://link.springer.com/chapter/10.1007/978-3-319-67786-6_13)