[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--jsi--hedwig-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hedwig/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-jsi-hedwig.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hedwig/tags "hbpmip/python-jsi-hedwig image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-jsi-hedwig.svg)](https://microbadger.com/images/hbpmip/python-jsi-hedwig "Get your own image badge on microbadger.com")

# Hedwig user reference manual

### Description:

The Hedwig algorithm for subgroup discovery is a data mining algorithm designed for exploratory data analysis of a data set. It receieves as input a data set of instances that can have either numeric or categoric features describing them. The input instances must be labeled, meaning that each instance belongs to a given class. By default, the first column of the data set is presumed to be the label of the data instances. As output, the algorithm produces a file containing interesting patterns (in the form of rules) of the data instances, along with some quality measures of the presented patterns.

The algorithm works by first discretizing the data set. Each numeric feature is discretized into 10 approximately equally sized bins - because the goal of the algorithm is to produce human readable *descriptions* of the data set, 10 is a sensible number of bins at which interesting rules can be discovered while not making the output difficult to understand. Once the data set has been discretized, the algorithm searches for rules, describing the data set. The goal of Hedwig is to discover not simply single properties of interesting subsets of a data set, but more complex rules in the form of *conjuncts* of properties. For example, in the *iris* data set, we can discover the rule *if 3.95<=petal_length<5.425 **and** 1.3<=petal_width<1.9, **then** Iris-versicolor*. Complex rules like this are discovered using beam search, where the beam contains the best *N* rules found so far. It starts with the default rule which covers all the input examples. In every search iteration, each rule from the beam is specialized via one of the four operations: (1) replace the predicate of a rule  with a predicate that is a sub-class of the previous one, (2) negate predicate of a rule, (3) append a new unary predicate to the rule, or (4) append a new binary predicate, introducing a new existentially quantified variable, where the new variable has to be `consumed' by a literal, which has to be added as a conjunction to this clause in the next step of rule refinement.

### Parameters:

* beam: The size of the beam to be used in the search. Larger values of this variable cause the search of the algorithm to take longer and return more high quality rules.

* support: The minimum relative support of the rules, discovered by Hedwig. The value of this parameter must be between 0 and 1 as the parameter represents the ration of the covered examples in the entire data set.

Reference:
Vavpetič, A., Novak, P. K., Grčar, M., Mozetič, I., & Lavrač, N. (2013, October). Semantic data mining of financial news articles. In International Conference on Discovery Science (pp. 294-307). Springer, Berlin, Heidelberg. [URL](https://link.springer.com/chapter/10.1007/978-3-642-40897-7_20)
