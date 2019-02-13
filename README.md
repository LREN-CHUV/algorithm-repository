[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/) [![TAU](https://img.shields.io/badge/TAU-ICTAF-AD2C32.svg)](http://ictaf.tau.ac.il/index.asp?lang=eng) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/a170b1b08f81441f85c004480ddaac0f)](https://www.codacy.com/app/hbp-mip/algorithm-repository?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=HBPMedical/algorithm-repository&amp;utm_campaign=Badge_Grade) [![CircleCI](https://circleci.com/gh/HBPMedical/algorithm-repository.svg?style=svg)](https://circleci.com/gh/HBPMedical/algorithm-repository)

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

# List of algorithms

## [hbpmip/python-anova](./python-anova/): Anova algorithm
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--anova-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-anova/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-anova.svg)](https://hub.docker.com/r/hbpmip/python-anova/tags "hbpmip/python-anova image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-anova.svg)](https://microbadger.com/#/images/hbpmip/python-anova "hbpmip/python-anova on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

This is a Python implementation of Anova.

## [hbpmip/python-correlation-heatmap](./python-correlation-heatmap/): Correlation heatmap
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--correlation--heatmap-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-correlation-heatmap/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-correlation-heatmap.svg)](https://hub.docker.com/r/hbpmip/python-correlation-heatmap/tags "hbpmip/python-correlation-heatmap image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-correlation-heatmap.svg)](https://microbadger.com/#/images/hbpmip/python-correlation-heatmap "hbpmip/python-correlation-heatmap on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

Calculate correlation heatmap, only works for real variables.
Run it on single node or in a distributed mode.
First, intermediate mode calculates covariance matrix from a single node, then aggregate mode is used after intermediate to combine statistics from multiple jobs and produce the final graph.

## [hbpmip/python-distributed-pca](./python-correlation-heatmap/): PCA - principal components analysis
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--distributed--pca-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-distributed-pca/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-distributed-pca.svg)](https://hub.docker.com/r/hbpmip/python-distributed-pca/tags "hbpmip/python-distributed-pca image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-distributed-pca.svg)](https://microbadger.com/#/images/hbpmip/python-distributed-pca "hbpmip/python-distributed-pca on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

Calculate PCA, only works for real variables.
Run it on single node or in a distributed mode.
First, intermediate mode calculates covariance matrix from a single node, then aggregate mode is used after intermediate to combine statistics from multiple jobs and produce the final graph.

Code is shared with [hbpmip/python-correlation-heatmap](./python-correlation-heatmap/)

## [hbpmip/python-distributed-kmeans](./python-distributed-kmeans/): K-means
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--distributed--kmeans-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-distributed-kmeans/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-distributed-kmeans.svg)](https://hub.docker.com/r/hbpmip/python-distributed-kmeans/tags "hbpmip/python-distributed-kmeans image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-distributed-kmeans.svg)](https://microbadger.com/#/images/hbpmip/python-distributed-kmeans "hbpmip/python-distributed-kmeans on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) 

Implementation of distributed k-means clustering (https://github.com/MRN-Code/dkmeans) in Python. It uses Single-Shot Decentralized LLoyd (https://github.com/MRN-Code/dkmeans#single-shot-decentralized-lloyd).

Intermediate mode calculates clusters on a single node, while aggregate mode is merging the clusters according to least merging error (e.g. smallest distance between centroids).

## [hbpmip/python-histograms](./python-histograms/): Histograms
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--histograms-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-histograms/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-histograms.svg)](https://hub.docker.com/r/hbpmip/python-histograms/tags "hbpmip/python-histograms image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-histograms.svg)](https://microbadger.com/#/images/hbpmip/python-histograms "hbpmip/python-histograms on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

Calculates histogram of nominal or real variable grouped by nominal variables in independent variables. Histogram edges are taken from `minValue` and `maxValue` property of dependent variable. If not available, then these values are calculated dynamically from dependent values (this won't work in distributed mode though).

## [hbpmip/python-jsi-hedwig](./python-jsi-hedwig/): Hedwig method 
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--jsi--hedwig-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hedwig/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-jsi-hedwig.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hedwig/tags "hbpmip/python-jsi-hedwig image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-jsi-hedwig.svg)](https://microbadger.com/#/images/hbpmip/python-jsi-hedwig "hbpmip/python-jsi-hedwig on microbadger") [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

Hedwig method for semantic subgroup discovery.  (https://github.com/anzev/hedwig).

## [hbpmip/python-jsi-hinmine](./python-jsi-hinmine/): HINMINE
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--jsi--hinmine-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hinmine/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-jsi-hinmine.svg)](https://hub.docker.com/r/hbpmip/python-jsi-hinmine/tags "hbpmip/python-jsi-hinmine image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-jsi-hinmine.svg)](https://microbadger.com/#/images/hbpmip/python-jsi-hinmine "hbpmip/python-jsi-hinmine on microbadger") [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

The HINMINE algorithm for network-based propositionalization is an algorithm for data analysis based on network analysis methods.

The input for the algorithm is a data set containing instances with real-valued features. The purpose of the algorithm is to construct a new set of features for further analysis by other data mining algorithms. The algorithm outputs a data set with features, generated for each data instance in the input data set. The features represent how close a given instance is to the other instances in the data set. The closeness of instances is measured using the PageRank algorithm, calculated on a network constructed from instance similarities.

## [hbpmip/python-knn](./python-knn/): k-nearest neighbors
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--knn-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-knn/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-knn.svg)](https://hub.docker.com/r/hbpmip/python-knn/tags "hbpmip/python-knn image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-knn.svg)](https://microbadger.com/#/images/hbpmip/python-knn "hbpmip/python-knn on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

Implementation of k-nearest neighbors algorithm (https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) in Python.

Run it on single node or in a distributed mode.

## [hbpmip/python-linear-regression](./python-linear-regression/): Linear and logistic regression
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--linear--regression-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-linear-regression/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-linear-regression.svg)](https://hub.docker.com/r/hbpmip/python-linear-regression/tags "hbpmip/python-linear-regression image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-linear-regression.svg)](https://microbadger.com/#/images/hbpmip/python-linear-regression "hbpmip/python-linear-regression on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

Python implementation of multivariate linear regression. It supports both continuous and categorical as independent variables. Run it on single node or in a distributed mode.
Python implementation of logistic regressions on one class versus the others. Only single-node mode is supported

## [hbpmip/python-sgd-regression](./python-sgd-regression/): SGD family of regressions
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--sgd--regression-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-sgd-regression/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-sgd-regression.svg)](https://hub.docker.com/r/hbpmip/python-sgd-regression/tags "hbpmip/python-sgd-regression image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-sgd-regression.svg)](https://microbadger.com/#/images/hbpmip/python-sgd-regression "hbpmip/python-sgd-regression on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

This is a Python implementation of scikit-learn estimators (http://scikit-learn.org/stable/modules/scaling_strategies.html) using Stochastic Gradient Descent and the `partial_fit` method for distributed learning.

Implemented methods:

* __linear_model__ - calls `SGDRegressor` or `SGDClassifier`
* __neural_network__ - calls `MLPRegressor` or `MLPClassifier`
* __naive_bayes__ - calls `MixedNB` (mix of `GaussianNB` and `MultinomialNB`), only works for classification tasks
* __gradient_boosting__ - calls `GradientBoostingRegressor` or `GradientBoostingClassifier`, does not support distributed training.

## [hbpmip/python-summary-statistics](./python-summary-statistics/): Summary statistics
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--summary--statistics-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-summary-statistics/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-summary-statistics.svg)](https://hub.docker.com/r/hbpmip/python-summary-statistics/tags "hbpmip/python-summary-statistics image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-summary-statistics.svg)](https://microbadger.com/#/images/hbpmip/python-summary-statistics "hbpmip/python-summary-statistics on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

It calculates various summary statistics for entire dataset and also for all subgroups created by combining all possible values of nominal covariates. Run it on single node or in a distributed mode.

## [hbpmip/python-tsne](./python-tsne/): t-SNE
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--tsne-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-tsne/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-tsne.svg)](https://hub.docker.com/r/hbpmip/python-tsne/tags "hbpmip/python-tsne image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-tsne.svg)](https://microbadger.com/#/images/hbpmip/python-tsne "hbpmip/python-tsne on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

The python-tsne is a wrapper for the the A-tSNE algorithm developed by N. Pezzotti. The underlying algorithm is an improvement on the Barnes-Hut tSNE (http://lvdmaaten.github.io/publications/papers/JMLR_2014.pdf) using an approximated k-nearest neighbor calculation.

## [hbpmip/java-jsi-clus-fire](./java-jsi-clus-fire/): k-nearest neighbors
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--fire-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fire/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-fire.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fire/tags "hbpmip/java-jsi-clus-fire image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-fire.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-fire "hbpmip/java-jsi-clus-fire on microbadger") [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

## [hbpmip/java-jsi-clus-fr](./java-jsi-clus-fr/): k-nearest neighbors
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--fr-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fr/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-fr.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-fr/tags "hbpmip/java-jsi-clus-fr image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-fr.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-fr "hbpmip/java-jsi-clus-fr on microbadger") [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

## [hbpmip/java-jsi-clus-pct](./java-jsi-clus-pct/): k-nearest neighbors
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--pct-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-pct.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct/tags "hbpmip/java-jsi-clus-pct image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-pct.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-pct "hbpmip/java-jsi-clus-pct on microbadger") [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

## [hbpmip/java-jsi-clus-pct-ts](./java-jsi-clus-pct-ts/): k-nearest neighbors
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--pct--ts-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct-ts/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-pct-ts.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-pct-ts/tags "hbpmip/java-jsi-clus-pct-ts image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-pct-ts.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-pct-ts "hbpmip/java-jsi-clus-pct-ts on microbadger") [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

## [hbpmip/java-jsi-clus-rm](./java-jsi-clus-rm/): k-nearest neighbors
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--rm-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-rm/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-rm.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-rm/tags "hbpmip/java-jsi-clus-rm image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-rm.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-rm "hbpmip/java-jsi-clus-rm on microbadger") [![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

## [hbpmip/java-jsi-streams-modeltree](./java-jsi-streams-modeltree/): k-nearest neighbors
[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

## [hbpmip/java-jsi-streams-regressiontree](./java-jsi--streams--regressiontree/): k-nearest neighbors
[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)

## [hbpmip/python-longitudinal](./python-longitudinal/): Longitudinal
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--longitudinal-008bb8.svg)](https://hub.docker.com/r/hbpmip/python-longitudinal/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/python-longitudinal.svg)](https://hub.docker.com/r/hbpmip/python-longitudinal/tags "hbpmip/python-longitudinal image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/python-longitudinal.svg)](https://microbadger.com/#/images/hbpmip/python-longitudinal "hbpmip/python-distributed-pca on microbadger")

## [hbpmip/r-3c](./r-3c/): 3C
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fr--3c-008bb8.svg)](https://hub.docker.com/r/hbpmip/r-3c/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/r-3c.svg)](https://hub.docker.com/r/hbpmip/r-3c/tags "hbpmip/r-3c image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/r-3c.svg)](https://microbadger.com/#/images/hbpmip/r-3c "hbpmip/python-distributed-pca on microbadger")

## [hbpmip/r-ggparci](./r-ggparci/): ggParci
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fr--ggparci-008bb8.svg)](https://hub.docker.com/r/hbpmip/r-ggparci/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/r-ggparci.svg)](https://hub.docker.com/r/hbpmip/r-ggparci/tags "hbpmip/r-ggparci image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/r-ggparci.svg)](https://microbadger.com/#/images/hbpmip/r-ggparci "hbpmip/python-distributed-pca on microbadger")

## [hbpmip/r-heatmaply](./r-heatmaply/): Heatmaply
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fr--heatmaply-008bb8.svg)](https://hub.docker.com/r/hbpmip/r-heatmaply/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/r-heatmaply.svg)](https://hub.docker.com/r/hbpmip/r-heatmaply/tags "hbpmip/r-heatmaply image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/r-heatmaply.svg)](https://microbadger.com/#/images/hbpmip/r-heatmaply "hbpmip/python-distributed-pca on microbadger")

## [hbpmip/java-rapidminer-knn](./java-rapidminer-knn]): :new_moon: k-NN k-NN
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--rapidminer--knn-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-knn/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-rapidminer-knn.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-knn/tags "hbpmip/java-rapidminer-knn image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-rapidminer-knn.svg)](https://microbadger.com/#/images/hbpmip/java-rapidminer-knn "hbpmip/python-distributed-pca on microbadger")

k-NN implemented with RapidMiner. Deprecated, replaced by [hbpmip/python-knn](./python-knn/)

## [java-rapidminer-naivebayes](./java-rapidminer-naivebayes]): :new_moon: Naive Bayes Naive Bayes
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpython--tsne-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-naivebayes/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-rapidminer-naivebayes.svg)](https://hub.docker.com/r/hbpmip/java-rapidminer-naivebayes/tags "hbpmip/java-rapidminer-naivebayes image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-rapidminer-naivebayes.svg)](https://microbadger.com/#/images/hbpmip/java-rapidminer-naivebayes "hbpmip/python-distributed-pca on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

Naive Bayes implemented with RapidMiner. Deprecated, replaced by [hbpmip/python-naivebayes](./python-naivebayes/)

## [hbpmip/r-linear-regression](./r-linear-regression/): :new_moon: Linear regression Linear regression
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fr--linear--regression-008bb8.svg)](https://hub.docker.com/r/hbpmip/r-linear-regression/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/r-linear-regression.svg)](https://hub.docker.com/r/hbpmip/r-linear-regression/tags "hbpmip/r-linear-regression image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/r-linear-regression.svg)](https://microbadger.com/#/images/hbpmip/r-linear-regression "hbpmip/python-distributed-pca on microbadger") [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)

Linear regression implemented in R, with support for federated results. Deprecated, replaced by [hbpmip/python-linear-regression](./python-linear-regression/)

# Algorithm capabilities

| Algorithm                                                          | Description           | Predictive         | Federated results         | In production      | Used for                   | Runtime engine |
|:-------------------------------------------------------------------|:----------------------|:-------------------|:--------------------------|:-------------------|:---------------------------|:--|
| [hbpmip/python-anova](./python-anova/)                             | Anova                 |                    | :heavy_check_mark: :soon: | :heavy_check_mark: | Regression                 | Woken |
| [hbpmip/python-correlation-heatmap](./python-correlation-heatmap/) | Correlation heatmap   |                    | :x:                       | :heavy_check_mark: | Visualisation              | Woken |
| [hbpmip/python-distributed-pca](./python-distributed-pca/)         | PCA                   |                    | :heavy_check_mark:        | :heavy_check_mark: | Visualisation              | Woken |
| [hbpmip/python-distributed-kmeans](./python-distributed-kmeans/)   | K-means               |                    | :heavy_check_mark:        | :heavy_check_mark: | Clustering                 | Woken |
| [hbpmip/python-histograms](./python-histograms/)                   | Histograms            |                    | :heavy_check_mark:        | :heavy_check_mark: | Visualisation              | Woken |
| [hbpmip/python-jsi-hedwig](./python-jsi-hedwig/)                   | Hedwig                |                    | :x:                       | :heavy_check_mark: |                            | Woken |
| [hbpmip/python-jsi-hinmine](./python-jsi-hinmine/)                 | HINMINE               |                    | :x:                       | :heavy_check_mark: |                            | Woken |
| [hbpmip/python-knn](./python-knn/)                                 | k-NN                  | :heavy_check_mark: | :heavy_check_mark:        | :heavy_check_mark: | Clustering                 | Woken |
| [hbpmip/python-linear-regression](./python-linear-regression/)     | Linear regression     | :heavy_check_mark: | :heavy_check_mark:        | :heavy_check_mark: | Regression                 | Woken |
| [hbpmip/python-linear-regression](./python-linear-regression/)     | Logistic regression   | :heavy_check_mark: | :x:                       | :heavy_check_mark: | Regression, Classification | Woken |
| [hbpmip/python-sgd-regression](./python-sgd-regression/)           | SGD Linear model      | :heavy_check_mark: | :heavy_check_mark:        | :heavy_check_mark: | Classification             | Woken |
| [hbpmip/python-sgd-regression](./python-sgd-regression/)           | SGD Neural Network    | :heavy_check_mark: | :x:                       | :heavy_check_mark: | Classification             | Woken |
| [hbpmip/python-sgd-regression](./python-sgd-regression/)           | SGD Naive Bayes       | :heavy_check_mark: | :x:                       | :heavy_check_mark: | Classification             | Woken |
| [hbpmip/python-sgd-regression](./python-sgd-regression/)           | SGD Gradient Boosting | :heavy_check_mark: | :x:                       | :heavy_check_mark: | Classification             | Woken |
| [hbpmip/python-summary-statistics](./python-summary-statistics/)   | Summary statistics    |                    | :heavy_check_mark:        | :heavy_check_mark: | Data exploration           | Woken |
| [hbpmip/python-tsne](./python-tsne/)                               | t-SNE                 |                    | :x:                       | :heavy_check_mark: | Visualisation              | Woken |


# Acknowledgements

This work has been funded by the European Union Seventh Framework Program (FP7/2007­2013) under grant agreement no. 604102 (HBP)

This work is part of SP8 of the Human Brain Project (SGA1).
