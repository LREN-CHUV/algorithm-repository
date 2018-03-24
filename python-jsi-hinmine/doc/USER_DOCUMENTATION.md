[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--jsi--hinmine-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hinmine/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-jsi-hinmine.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hinmine/tags "hbpmip/python-jsi-hinmine image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-jsi-hinmine.svg)](https://microbadger.com/images/hbpmip/python-jsi-hinmine "Get your own image badge on microbadger.com")

# HINMine user reference manual

### Description:

The HinMine algorithm is an algorithm designed to construct networ-analysis-based feature vectors for data instances that can be either nodes in a network or standard data instances with a fixed set of numeric features. In this implementation, the input for the algorithm is a set of data instances, and the output of the algorithm is a new data set with the same instances, but new features constructed out of them.

The algorithm works in two steps. In the first step, a network is constructed out of the input data, where the nodes of the network correspond to the data instances and the strength of the connection between two instances exponentially depends on the square of the Euclidean distance between the two instances. In the second step, network propositionalization is performed on the resulting network. Network propositionalization is a method for constructing feature vectors for each target node in the network using the personalized PageRank (P-PR) algorithm. The personalized PageRank of node *v* in a network is defined as the stationary distribution of the position of a random walker who starts the walk in node $v$ and then at each node either selects one of the outgoing connections or jumps back to node *v*. The probability (denoted *p*) of continuing the walk is a parameter of the personalized PageRank algorithm and is by default set to *0.85*. Once calculated, the resulting PageRank vectors are normalized according to the Euclidean norm. The resulting vector contains information about the proximity of node *v* to each of the remaining nodes of the network. We consider the P-PR vectors of a node as a propositionalized feature vector of the node. Because two nodes with similar P-PR vectors will be in proximity of similar nodes a classifier should consider them as similar instances. The constructed feature vectors can be then used to analyze the nodes from which they were calculated, and therefore, the original data instances.

### Parameters:

* damping: The variable *p* used in the construction of the P-PR vectors during propositionalization. The value of this variable can be any real number between *0* and *1*. Smaller values of the damping factor ensure faster calculation of the feature vectors, however larger values of *p* mean that the algorithm is capable of performing longer walks, exploring more of the structure of the data.

* normalize (True/False): This variable determines whether the feature values of the input data instances should be normalized or not. If True, then the values of each feature are normalized to be between 0 and 1. This allows the algorithm to fairly compare two features measured with incomparable units. The value of this variable should be False if the difference in the size of the features carries inherent meaning.

Reference:
Kralj, J., Robnik-Šikonja, M., & Lavrač, N. (2018). HINMINE: heterogeneous information network mining with information retrieval heuristics. Journal of Intelligent Information Systems, 50(1), 29-61. [URL](https://link.springer.com/article/10.1007/s10844-017-0444-9)
