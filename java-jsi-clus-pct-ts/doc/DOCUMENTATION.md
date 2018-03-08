[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--pct--ts-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct-ts/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-pct-ts.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct-ts/tags "hbpmip/java-jsi-clus-pct-ts image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-pct-ts.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-pct-ts "hbpmip/java-jsi-clus-pct-ts on microbadger")

# Predictive Clustering Trees (PCTs) for time-series prediction user reference manual

### Description:

Predictive Clustering Trees (PCTs) are decision trees that can be used for modeling of structured target variables. Decision trees in general, are hierarchical models, where each internal node contains a test on a descriptive variable (attribute) of an example and each branch leaving this node corresponds to an outcome of this test. Terminal nodes (leaves) of a tree contain models defining the values of the target (dependent) variable for all examples falling in a given leaf. Given a new example, for which the value of the target variable should be predicted, the tree is interpreted from the root. In each inner node, the prescribed test is performed, and according to the result, the corresponding sub-tree is selected. When the selected node is a leaf, the value of the target variable for the new example is predicted according to the model in this leaf. If the target variable is numeric, the models in the leaves are typically constant values (regression tree), if the target variable is categorical, the models are categorical values (classification tree). PCTs make it possible for the target variable to be a structured object such as a vector or a time-series. In the latter case, the tree predicts the whole time-series simultaneously. Once a decision tree is learned on the data we can use it for two purposes. First, we can use it for explaining the connections between the descriptive variables and time changes in the target variable, and determine the variables that are important for grouping (clustering) examples with similar time patterns. Second, we can use the tree for predicting the time patterns of the target variable.

### Parameters:

* Descriptive variables: A set of descriptive variables, which are used within tests inside the decision tree that describe how the similar examples are clustered together. They can be numeric or categoric or mix of both types.

* Target variables representing a time-series: A set of more than one measurements of the same target variable (measured at predefined time points) for which we want to learn a predictive model that will describe the time-series pattern in terms of descriptive variables. The variables representing the time-series must be numeric.

* Minimum number of examples in a decision tree leaf: This parameter influences the size of the learned tree (post-pruning parameter), the larger the number, the smaller the learned tree.

* Pruning (Yes/No): The parameter defines whether a post-pruning procedure is applied after the initial decision tree learning. Pruning reduces the size of the tree and such a tree tends to overfit data less.
