[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

# Streaming model trees for multi-target regression for privacy-preserving analysis user reference manual

### Description:

iSOUP-Trees are decision trees that are learned incrementally and can be used for modeling of structured target variables. Decision trees in general, are hierarchical models, where each internal node contains a test on a descriptive variable (attribute) of an example and each branch leaving this node corresponds to an outcome of this test. Terminal nodes (leaves) of a tree contain models defining the values of the target (dependent) variable for all examples falling in a given leaf. Given a new example, for which the value of the target variable should be predicted, the tree is interpreted from the root. In each inner node, the prescribed test is performed, and according to the result, the corresponding sub-tree is selected. When the selected node is a leaf, the value of the target variable for the new example is predicted according to the model in this leaf. In iSOUP-Tree model trees the model in a leaf is a linear model that takes as inputs the values of the input attributes. iSOUP-Trees process the target variable as a structured object, in particular, a vector of numeric values. These trees thus predict several target variables simultaneously. The main advantage of such trees over a set of separate trees for each dependent variable is that a single tree is usually much smaller than the total size of the individual trees for all variables and therefore much easier to interpret. Once a decision tree is learned on the data we can use it for two purposes. First, we can use it for explaining the connections between the variables and determine the variables that are important for grouping (clustering) similar examples according to the dependent target variable. Second, we can use the tree for predicting the target variable of new examples.

Due to the nature of their learning procedure, iSOUP-Trees process data examples one by one and never store the examples directly. This allows us to transfer models between hospital nodes without violating privacy restrictions. Once a model is transferred to a new hospital node it is further updated using the available data. The process then repeats for the next hospital node until the model has learned from all of the available data. This allows the model to generalize over all available data.

### Parameters:

* Target variables: A set of one or more (dependent) variables for which we want to learn a predictive model that will describe their values in terms of descriptive variables. They must all be numeric.

Reference:

Osojnik, A., Panov, P., & Džeroski, S. (2017). Tree-based methods for online multi-target regression. In Journal of Intelligent Information Systems (vol. 50, issue 2, pp. 315-330). Springer, Cham. [URL](https://link.springer.com/article/10.1007/s10844-017-0462-7)
