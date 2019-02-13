[![JSI](https://img.shields.io/badge/JSI-KT-AF4C64.svg)](http://kt.ijs.si/)
[![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fjava--jsi--clus--rm-008bb8.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-rm/)
[![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/java-jsi-clus-rm.svg)](https://hub.docker.com/r/hbpmip/java-jsi-clus-rm/tags "hbpmip/java-jsi-clus-rm image tags")
[![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/java-jsi-clus-rm.svg)](https://microbadger.com/#/images/hbpmip/java-jsi-clus-rm "hbpmip/java-jsi-clus-rm on microbadger")

# Redescription mining with Predictive Clustering Trees (CLUS-RM) - user reference manual

### Description:

Redescription mining (RM) is a descriptive data mining task aimed at finding re-descriptions (multiple descriptions) of different subsets of entities contained in the data. Redescription is a tuple of logical formulas (called queries) where each formula contains attributes from one data view. Queries can contain conjunction, disjunction and negation logical operators. Currently, redescription mining uses at most two different views to re-describe entities contained in the data. Redescription mining offers unique insight into the data by finding groups that are similar with respect to both views and at the same times provide concise and understandable descriptions. Redescription mining is especially useful to discover different (potentially non-linear) associations between different subsets of attributes. CLUS-RM is a redescription mining algorithm based on Predictive Clustering Trees (PCTs). It is also equipped with a redescription set optimization procedure which allows users to control the number of returned redescriptions. The algorithm has been extended to allow adding attribute constraints to the redescription mining process. These constraints are added as a predefined sets of attributes that should occur in redescription queries. There are three types of attribute constraints and corresponding redescription set construction types available when using attribute constraints: a) "suggested", b) "soft" and c) "hard". In suggested constraint-based redescription mining, redescriptions satisfying user-defined constraints are given higher score, thus are more likely  to occur in the output redescription set. Soft constraint-based redescription mining takes into account only redescriptions that satisfy at least part of one predefined attribute constraint set. Hard constraint-based redescription mining takes into account only redescriptions fully satisfying at least one pre-defined constraint set.  

### Parameters:

* View 1 (W1): Index of a start and end attribute contained in the first data view (attributes must have consecutive indices).
* View 2 (W2): Index of a start and end attribute contained in the second data view (attributes must have consecutive indices).
* Minimal Jaccard index: Specify minimal redescription accuracy (measured with Jaccard index) required to return it to the user. Parameter values are contained in [0,1].
* Maximal p-value: Specify maximal redescription p-value required to return it to the user. Parameter values are contained in [0,1].
* Minimal redescription support: Specify minimal redescription support required to return it to the user. Parameter values are contained in [1,|E|], where |E| denotes number of entities in the dataset.
* Maximal redescription support: Specify maximal redescription support allowed. Parameter values are contained in [1,|E|], where |E| denotes number of entities in the dataset.
* Number of random restarts (initializations): Specify the number of random initialization steps performed by the CLUS-RM .
* Number of iteration: Specify the number of iterations (also called alternations) performed by the CLUS-RM.
* Number of redescriptions: Specify the number of redescriptions to be returned by the CLUS-RM.
* Attribute importance for attributes from view 1: Specify the attribute importance used in constraint-based redescription mining for attributes contained in the first view. Possible values are: "none" - allow redescriptions with any attributes from view1, "suggested" - allow defining combinations of attributes that increase redescription score (redescriptions containing specified attributes are preferred), "soft" - only return redescriptions satisfying at least part of specified constraints to the user (redescriptions satisfying larger portion of constraint set are preferred), "hard" - only return redescriptions satisfying all constraints defined in one constraint set.
* Attribute importance for attributes from view 2: Specify the attribute importance used in constraint-based redescription mining for attributes contained in the second view. Possible values are: "none" - allow redescriptions with any attributes from view2, "suggested" - allow defining combinations of attributes that increase redescription score (redescriptions containing specified attributes are preferred), "soft" - only return redescriptions satisfying at least part of specified constraints to the user (redescriptions satisfying larger portion of constraint set are preferred), "hard" - only return redescriptions satisfying all constraints defined in one constraint set.
* Important attributes from view 1: defines constraint sets, for attributes contained in view 1, to be used in constraint-based redescription mining. Constraints are specified in the format "{a;b;c},{a;d}", where a,b,c,d are some attributes contained in the first view (view1) of the data.
* Important attributes from view 2: defines constraint sets, for attributes contained in view 2, to be used in constraint-based redescription mining. Constraints are specified in the format "{e;f;g},{h;i}", where e,f,g,h,i are some attributes contained in the second view (view2) of the data.

Reference:

Mihelčić M, Džeroski S, Lavrač N, Šmuc T. (2016) Redescription Mining with Multi-target Predictive Clustering Trees. In Postproceedings of the New Frontiers in Mining Complex Patterns workshop.

Mihelčić M, Šimić G, Babić Leko M, Lavrač N, Džeroski S, et al. (2017) Using redescription mining to relate clinical and biological characteristics of cognitively impaired and Alzheimer’s disease patients. PLOS ONE 12(10): e0187364. https://doi.org/10.1371/journal.pone.0187364
