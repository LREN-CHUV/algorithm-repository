

## python-tsne for HBP
### A-tSNE Description

The python-tsne is a wrapper for the the A-tSNE algorithm developed by N. Pezzotti [[1](#reference-material)]. The underlying algorithm is an improvement on the [Barnes-Hut tSNE](http://lvdmaaten.github.io/publications/papers/JMLR_2014.pdf) using and approximated k-nearest neighbor calculation. The precision of A-tSNE can varied by changing the parameter _theta_ (in the paper this is refered to as _⍴_). A theta value of 1.0 is equivalent to Barnes-Hut tSNE, in the [paper](#reference-material) a theta value of 0.34 is shown to give a two order of magnitude speed-up while giving results nearly-identical to the full accuracy algorithm.

Using tSNE requires some care especially in choosing the perplexity parameter that determines the number of nearest neighbours. We refer the reader to the advice given by [L. van der Maaten](https://lvdmaaten.github.io/tsne/) and the article [How to use t-SNE effectively](https://distill.pub/2016/misread-tsne/) by Wattenberg, et al., 2016.

### Wrapping description

For HBP 

The output of the
### Parameters
perplexity = 30
theta = 0.5
target_dimensions = 2
iterations = 1000
do_zscore = True
dependent_is_label = True

Parameter | Description | Default (if any)
--- | --- | ---
perplexity |  Describes the effective number of neighbors considered for each data-point | 30
theta |



### Reference material
__DOI__ : https://doi.org/10.1109/TVCG.2016.2570755

__BibTeX for citing at-SNE__


@article{pezzotti_approximated_2017,
	title = {Approximated and {User} {Steerable} {tSNE} for {Progressive} {Visual} {Analytics}},
	volume = {23},
	issn = {1077-2626},
	doi = {10.1109/TVCG.2016.2570755},
	abstract = {Progressive Visual Analytics aims at improving the interactivity in existing analytics techniques by means of visualization as well as interaction with intermediate results. One key method for data analysis is dimensionality reduction, for example, to produce 2D embeddings that can be visualized and analyzed efficiently. t-Distributed Stochastic Neighbor Embedding (tSNE) is a well-suited technique for the visualization of high-dimensional data. tSNE can create meaningful intermediate results but suffers from a slow initialization that constrains its application in Progressive Visual Analytics. We introduce a controllable tSNE approximation (A-tSNE), which trades off speed and accuracy, to enable interactive data exploration. We offer real-time visualization techniques, including a density-based solution and a Magic Lens to inspect the degree of approximation. With this feedback, the user can decide on local refinements and steer the approximation level during the analysis. We demonstrate our technique with several datasets, in a real-world research scenario and for the real-time analysis of high-dimensional streams to illustrate its effectiveness for interactive data analysis.},
	number = {7},
	journal = {IEEE Transactions on Visualization and Computer Graphics},
	author = {Pezzotti, N. and Lelieveldt, B. P. F. and Maaten, L. v d and Höllt, T. and Eisemann, E. and Vilanova, A.},
	month = jul,
	year = {2017},
	keywords = {Algorithm design and analysis, approximate computation, Approximation algorithms, approximation level, Computational complexity, controllable tSNE approximation, Data analysis, data visualisation, Data visualization, density-based solution, dimensionality reduction, High dimensional data, high-dimensional data visualization, interactive data analysis, magic lens, progressive visual analytics, Real-time systems, t-distributed stochastic neighbor embedding, user steerable tSNE, Visual analytics, visualization techniques},
	pages = {1739--1752}
}
