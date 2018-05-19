FROM hbpmip/r-base-build:3.4.2-2 as r-build-env

ENV heatmaply_VERSION=master
# TODO - use version like HBPMedical/heatmaply@0.1.0
# RUN installGithub.r HBPMedical/heatmaply    -->> I use the CRAN version instead, it is more stable.
RUN install.r heatmaply
RUN install.r svglite

FROM hbpmip/r-mip:0.5.1

MAINTAINER ludovic.claude54@gmail.com

# install pandoc for writing the html output file as standalone
RUN wget https://github.com/jgm/pandoc/releases/download/2.1.1/pandoc-2.1.1-1-amd64.deb
RUN dpkg -i pandoc-2.1.1-1-amd64.deb

# copy heatmaply and svglite and their dependencies
COPY --from=r-build-env /usr/local/lib/R/site-library/assertthat/ /usr/local/lib/R/site-library/assertthat
COPY --from=r-build-env /usr/local/lib/R/site-library/base64enc/ /usr/local/lib/R/site-library/base64enc
COPY --from=r-build-env /usr/local/lib/R/site-library/BH/ /usr/local/lib/R/site-library/BH
COPY --from=r-build-env /usr/local/lib/R/site-library/bindr/ /usr/local/lib/R/site-library/bindr
COPY --from=r-build-env /usr/local/lib/R/site-library/bindrcpp/ /usr/local/lib/R/site-library/bindrcpp
COPY --from=r-build-env /usr/local/lib/R/site-library/bitops/ /usr/local/lib/R/site-library/bitops
COPY --from=r-build-env /usr/local/lib/R/site-library/caTools/ /usr/local/lib/R/site-library/caTools
COPY --from=r-build-env /usr/local/lib/R/site-library/cli/ /usr/local/lib/R/site-library/cli
COPY --from=r-build-env /usr/local/lib/R/site-library/colorspace/ /usr/local/lib/R/site-library/colorspace
COPY --from=r-build-env /usr/local/lib/R/site-library/crayon/ /usr/local/lib/R/site-library/crayon
COPY --from=r-build-env /usr/local/lib/R/site-library/crosstalk/ /usr/local/lib/R/site-library/crosstalk
COPY --from=r-build-env /usr/local/lib/R/site-library/curl/ /usr/local/lib/R/site-library/curl
COPY --from=r-build-env /usr/local/lib/R/site-library/data.table/ /usr/local/lib/R/site-library/data.table
# COPY --from=r-build-env /usr/local/lib/R/site-library/debugme/ /usr/local/lib/R/site-library/debugme
COPY --from=r-build-env /usr/local/lib/R/site-library/dendextend/ /usr/local/lib/R/site-library/dendextend
COPY --from=r-build-env /usr/local/lib/R/site-library/DEoptimR/ /usr/local/lib/R/site-library/DEoptimR
COPY --from=r-build-env /usr/local/lib/R/site-library/dichromat/ /usr/local/lib/R/site-library/dichromat
COPY --from=r-build-env /usr/local/lib/R/site-library/digest/ /usr/local/lib/R/site-library/digest
COPY --from=r-build-env /usr/local/lib/R/site-library/diptest/ /usr/local/lib/R/site-library/diptest
COPY --from=r-build-env /usr/local/lib/R/site-library/dplyr/ /usr/local/lib/R/site-library/dplyr
COPY --from=r-build-env /usr/local/lib/R/site-library/flexmix/ /usr/local/lib/R/site-library/flexmix
COPY --from=r-build-env /usr/local/lib/R/site-library/foreach/ /usr/local/lib/R/site-library/foreach
COPY --from=r-build-env /usr/local/lib/R/site-library/fpc/ /usr/local/lib/R/site-library/fpc
COPY --from=r-build-env /usr/local/lib/R/site-library/gclus/ /usr/local/lib/R/site-library/gclus
COPY --from=r-build-env /usr/local/lib/R/site-library/gdata/ /usr/local/lib/R/site-library/gdata
COPY --from=r-build-env /usr/local/lib/R/site-library/gdtools/ /usr/local/lib/R/site-library/gdtools
COPY --from=r-build-env /usr/local/lib/R/site-library/ggplot2/ /usr/local/lib/R/site-library/ggplot2
COPY --from=r-build-env /usr/local/lib/R/site-library/glue/ /usr/local/lib/R/site-library/glue
COPY --from=r-build-env /usr/local/lib/R/site-library/gplots/ /usr/local/lib/R/site-library/gplots
COPY --from=r-build-env /usr/local/lib/R/site-library/gridExtra/ /usr/local/lib/R/site-library/gridExtra
COPY --from=r-build-env /usr/local/lib/R/site-library/gtable/ /usr/local/lib/R/site-library/gtable
COPY --from=r-build-env /usr/local/lib/R/site-library/gtools/ /usr/local/lib/R/site-library/gtools
COPY --from=r-build-env /usr/local/lib/R/site-library/heatmaply/ /usr/local/lib/R/site-library/heatmaply
COPY --from=r-build-env /usr/local/lib/R/site-library/hexbin/ /usr/local/lib/R/site-library/hexbin
COPY --from=r-build-env /usr/local/lib/R/site-library/htmltools/ /usr/local/lib/R/site-library/htmltools
COPY --from=r-build-env /usr/local/lib/R/site-library/htmlwidgets/ /usr/local/lib/R/site-library/htmlwidgets
COPY --from=r-build-env /usr/local/lib/R/site-library/httpuv/ /usr/local/lib/R/site-library/httpuv
COPY --from=r-build-env /usr/local/lib/R/site-library/httr/ /usr/local/lib/R/site-library/httr
COPY --from=r-build-env /usr/local/lib/R/site-library/iterators/ /usr/local/lib/R/site-library/iterators
COPY --from=r-build-env /usr/local/lib/R/site-library/jsonlite/ /usr/local/lib/R/site-library/jsonlite
COPY --from=r-build-env /usr/local/lib/R/site-library/kernlab/ /usr/local/lib/R/site-library/kernlab
COPY --from=r-build-env /usr/local/lib/R/site-library/labeling/ /usr/local/lib/R/site-library/labeling
COPY --from=r-build-env /usr/local/lib/R/site-library/lazyeval/ /usr/local/lib/R/site-library/lazyeval
COPY --from=r-build-env /usr/local/lib/R/site-library/magrittr/ /usr/local/lib/R/site-library/magrittr
COPY --from=r-build-env /usr/local/lib/R/site-library/mclust/ /usr/local/lib/R/site-library/mclust
COPY --from=r-build-env /usr/local/lib/R/site-library/mime/ /usr/local/lib/R/site-library/mime
COPY --from=r-build-env /usr/local/lib/R/site-library/modeltools/ /usr/local/lib/R/site-library/modeltools
COPY --from=r-build-env /usr/local/lib/R/site-library/munsell/ /usr/local/lib/R/site-library/munsell
COPY --from=r-build-env /usr/local/lib/R/site-library/mvtnorm/ /usr/local/lib/R/site-library/mvtnorm
COPY --from=r-build-env /usr/local/lib/R/site-library/openssl/ /usr/local/lib/R/site-library/openssl
# COPY --from=r-build-env /usr/local/lib/R/site-library/pillar/ /usr/local/lib/R/site-library/pillar
COPY --from=r-build-env /usr/local/lib/R/site-library/pkgconfig/ /usr/local/lib/R/site-library/pkgconfig
COPY --from=r-build-env /usr/local/lib/R/site-library/plogr/ /usr/local/lib/R/site-library/plogr
COPY --from=r-build-env /usr/local/lib/R/site-library/plotly/ /usr/local/lib/R/site-library/plotly
COPY --from=r-build-env /usr/local/lib/R/site-library/plyr/ /usr/local/lib/R/site-library/plyr
COPY --from=r-build-env /usr/local/lib/R/site-library/prabclus/ /usr/local/lib/R/site-library/prabclus
COPY --from=r-build-env /usr/local/lib/R/site-library/processx/ /usr/local/lib/R/site-library/processx
COPY --from=r-build-env /usr/local/lib/R/site-library/purrr/ /usr/local/lib/R/site-library/purrr
COPY --from=r-build-env /usr/local/lib/R/site-library/qap/ /usr/local/lib/R/site-library/qap
COPY --from=r-build-env /usr/local/lib/R/site-library/R6/ /usr/local/lib/R/site-library/R6
COPY --from=r-build-env /usr/local/lib/R/site-library/RColorBrewer/ /usr/local/lib/R/site-library/RColorBrewer
COPY --from=r-build-env /usr/local/lib/R/site-library/Rcpp/ /usr/local/lib/R/site-library/Rcpp
COPY --from=r-build-env /usr/local/lib/R/site-library/registry/ /usr/local/lib/R/site-library/registry
COPY --from=r-build-env /usr/local/lib/R/site-library/reshape2/ /usr/local/lib/R/site-library/reshape2
COPY --from=r-build-env /usr/local/lib/R/site-library/rlang/ /usr/local/lib/R/site-library/rlang
COPY --from=r-build-env /usr/local/lib/R/site-library/robustbase/ /usr/local/lib/R/site-library/robustbase
COPY --from=r-build-env /usr/local/lib/R/site-library/scales/ /usr/local/lib/R/site-library/scales
COPY --from=r-build-env /usr/local/lib/R/site-library/seriation/ /usr/local/lib/R/site-library/seriation
COPY --from=r-build-env /usr/local/lib/R/site-library/shiny/ /usr/local/lib/R/site-library/shiny
COPY --from=r-build-env /usr/local/lib/R/site-library/sourcetools/ /usr/local/lib/R/site-library/sourcetools
COPY --from=r-build-env /usr/local/lib/R/site-library/stringi/ /usr/local/lib/R/site-library/stringi
COPY --from=r-build-env /usr/local/lib/R/site-library/stringr/ /usr/local/lib/R/site-library/stringr
COPY --from=r-build-env /usr/local/lib/R/site-library/svglite/ /usr/local/lib/R/site-library/svglite
COPY --from=r-build-env /usr/local/lib/R/site-library/tibble/ /usr/local/lib/R/site-library/tibble
COPY --from=r-build-env /usr/local/lib/R/site-library/tidyr/ /usr/local/lib/R/site-library/tidyr
COPY --from=r-build-env /usr/local/lib/R/site-library/tidyselect/ /usr/local/lib/R/site-library/tidyselect
COPY --from=r-build-env /usr/local/lib/R/site-library/trimcluster/ /usr/local/lib/R/site-library/trimcluster
COPY --from=r-build-env /usr/local/lib/R/site-library/TSP/ /usr/local/lib/R/site-library/TSP
# COPY --from=r-build-env /usr/local/lib/R/site-library/utf8/ /usr/local/lib/R/site-library/utf8
COPY --from=r-build-env /usr/local/lib/R/site-library/viridis/ /usr/local/lib/R/site-library/viridis
COPY --from=r-build-env /usr/local/lib/R/site-library/viridisLite/ /usr/local/lib/R/site-library/viridisLite
COPY --from=r-build-env /usr/local/lib/R/site-library/webshot/ /usr/local/lib/R/site-library/webshot
COPY --from=r-build-env /usr/local/lib/R/site-library/whisker/ /usr/local/lib/R/site-library/whisker
COPY --from=r-build-env /usr/local/lib/R/site-library/withr/ /usr/local/lib/R/site-library/withr
COPY --from=r-build-env /usr/local/lib/R/site-library/xtable/ /usr/local/lib/R/site-library/xtable
COPY --from=r-build-env /usr/local/lib/R/site-library/yaml/ /usr/local/lib/R/site-library/yaml
COPY --from=r-build-env /usr/local/lib/R/site-library/later/ /usr/local/lib/R/site-library/later
COPY --from=r-build-env /usr/local/lib/R/site-library/promises/ /usr/local/lib/R/site-library/promises


COPY main.R /src/
COPY tests/testthat.R /src/tests/
COPY tests/testthat/ /src/tests/testthat/

ENV DOCKER_IMAGE=hbpmip/r-heatmaply:0.2.0 \
    FUNCTION=r-heatmaply

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL eu.humanbrainproject.function=heatmaply \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="Shay Yaacoby, Tal Galili, Ludovic Claude" \
      eu.humanbrainproject.function.organisation="" \
      eu.humanbrainproject.function.date="" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/heatmaply" \
      org.label-schema.description="Interactive Heatmap Plot" \
      org.label-schema.url="" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/HBPMedical/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="" \
      org.label-schema.license="Apache2.0" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
