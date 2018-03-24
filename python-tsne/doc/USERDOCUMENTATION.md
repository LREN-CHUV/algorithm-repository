## python-tsne for HBP
### A–tSNE Description

The python-tsne is a wrapper for the the A-tSNE algorithm developed by N. Pezzotti [[1](#reference-material)]. The underlying algorithm is an improvement on the [Barnes-Hut tSNE](http://lvdmaaten.github.io/publications/papers/JMLR_2014.pdf) using an approximated k-nearest neighbor calculation. The precision of A-tSNE can varied by changing the parameter _theta_ (in the paper [[1](#reference-material)] this is refered to as _⍴_). A _theta_ value of 1.0 is equivalent to Barnes-Hut tSNE. In tests using 60k MNIST digits, (60k points by 784 dimensions), a _theta_ value of 0.34 was shown to give a two order of magnitude speed-up while giving results nearly-identical to the full accuracy algorithm.

Using tSNE requires some care especially in choosing the perplexity parameter that determines the effective number of neighbors. We refer the reader to the advice given by [L. van der Maaten](https://lvdmaaten.github.io/tsne/) and the article [How to use t-SNE effectively](https://distill.pub/2016/misread-tsne/) by Wattenberg, et al., 2016.

### HBP Wrapping description

##### Input data
The HBP standard wrapping uses the _dependent_ and _independent_ variables convention for input data. To map this to tSNE we perform tSNE over the all independent variables, i.e. these form the dimensions for tSNE. In addition there is the option to use the dependent variable as a label in the output embedding. This option is controlled by the _dependent_is_label_ parameter, see [Parameter description](#parameter-description) below.

tSNE requires the dimensions to be normalized before processing. An additional wrapping parameter _do_zscore_, if "True", causes the wrapper to perform an automatic z-score using the python scipy.stats.zscore function. If the parameter is set to "False" then the user should ensure that the data is normalized before passing it to the python-tsne.

### Parameter description

Parameter | Description | Default (if any)
--- | --- | ---
perplexity |  Describes the effective number of neighbors considered for each data-point. The article [How to use t-SNE effectively](https://distill.pub/2016/misread-tsne/) provides some insight into the effect of this variable. | 30
theta | The approximation parameter. 1.0 is equivalent to BH-tSNE. See [the A-tSNE description](#atsne-description) for more information.| 0.5
target_dimensions | This parameter should be left at 2 as the Highchart output is not designed to support higher numbers of dimensions | 2
iterations | The number of tSNE iterations to perform. If the clustering is not satisfactory a simple experiment is to double the default and see if that makes any difference. If not, the perplexity parameter may help. | 1000
do_zscore | If "True" the data is zscored before running tSNE. If "False" the data is assumed to be pre-normalized | "True"
dependent_is_label | If "True" the dependent data is used to color label the Highchart output. | "True"



### Reference material

__Source code__ A-tSNE is build as a command line tool part of the [High-Dimensional-Inspector](https://github.com/Nicola17/High-Dimensional-Inspector/tree/master/applications/command_line_tools) project

__DOI__ : https://doi.org/10.1109/TVCG.2016.2570755

__BibTeX for citing at-SNE__

```bibtex
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
```

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
