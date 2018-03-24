[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--fire-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fire/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-fire.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fire/tags "hbpmip/java-jsi-clus-fire image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-fire.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-fire "hbpmip/java-jsi-clus-fire on microbadger")

# Fitted rule ensembles for multi-target regression user reference manual

### Description:

Methods for learning decision rules are being successfully applied to many problem domains, especially where understanding and interpretation of the learned model is necessary. Although decision trees are regarded as easily interpretable models, in many cases, decision rules are even simpler to understand. The rule ensembles for multi-target regression employ the rule ensembles approach, which transcribes an ensemble of decision trees (in this case an ensemble of predictive clustering trees) into a large collection of rules. An optimization procedure is then used for selecting the best (and much smaller) subset of these rules, and to determine their weights. The accuracy of multi-target regression rule ensembles tend to be better than the accuracy of multi-target regression trees, but somewhat worse than the accuracy of multi-target random forests. The rules are significantly more concise than random forests, and it is also possible to create very small rule sets that are still comparable in accuracy to single regression trees.

### Parameters:

* Descriptive variables: A set of descriptive variables, which are used within tests inside the decision tree that describe how the similar examples are clustered together. They can be numeric or categoric or mix of both types.

* Target variables: A set of one or more (dependent) variables for which we want to learn a predictive model that will describe their values in terms of descriptive variables. They must be numeric.

* Number of decision trees in the initial ensemble: Rule ensembles start by generating an ensemble of (predictive clustering) trees - this is the size of the ensemble. Increasing the number increases the variance of the candidate rules, but also increases the computational complexity (run time).

* Maximum number of trees: The maximum number of trees the method returns. The parameter can be used to prevent overly long run times on hard to model or noisy data.


Reference:
Aho, T., Ženko, B., Džeroski, S., & Elomaa, T. (2012). Multi-target regression with rule ensembles. Journal of Machine Learning Research, 13(Aug), 2367-2407. [PDF](http://www.jmlr.org/papers/volume13/aho12a/aho12a.pdf)
