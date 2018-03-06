FROM hbpmip/r-base-build:3.4.2-2 as r-build-env

RUN install.r randomForest leaps car MASS cluster clusterCrit magrittr
RUN install.r svglite
RUN install.r aurelius

ENV CCC_VERSION=master
RUN installGithub.r HBPMedical/CCC

FROM hbpmip/r-mip:0.4.1

MAINTAINER ludovic.claude54@gmail.com

# packages dependencies for CCC
COPY --from=r-build-env /usr/local/lib/R/site-library/car/ /usr/local/lib/R/site-library/car                  
COPY --from=r-build-env /usr/local/lib/R/site-library/clusterCrit/ /usr/local/lib/R/site-library/clusterCrit  
COPY --from=r-build-env /usr/local/lib/R/site-library/leaps/ /usr/local/lib/R/site-library/leaps              
COPY --from=r-build-env /usr/local/lib/R/site-library/lme4/ /usr/local/lib/R/site-library/lme4                
COPY --from=r-build-env /usr/local/lib/R/site-library/magrittr/ /usr/local/lib/R/site-library/magrittr        
COPY --from=r-build-env /usr/local/lib/R/site-library/MatrixModels/ /usr/local/lib/R/site-library/MatrixModels
COPY --from=r-build-env /usr/local/lib/R/site-library/minqa/ /usr/local/lib/R/site-library/minqa              
COPY --from=r-build-env /usr/local/lib/R/site-library/nloptr/ /usr/local/lib/R/site-library/nloptr            
COPY --from=r-build-env /usr/local/lib/R/site-library/pbkrtest/ /usr/local/lib/R/site-library/pbkrtest        
COPY --from=r-build-env /usr/local/lib/R/site-library/quantreg/ /usr/local/lib/R/site-library/quantreg        
COPY --from=r-build-env /usr/local/lib/R/site-library/randomForest/ /usr/local/lib/R/site-library/randomForest
COPY --from=r-build-env /usr/local/lib/R/site-library/Rcpp/ /usr/local/lib/R/site-library/Rcpp                
COPY --from=r-build-env /usr/local/lib/R/site-library/RcppEigen/ /usr/local/lib/R/site-library/RcppEigen      
COPY --from=r-build-env /usr/local/lib/R/site-library/SparseM/ /usr/local/lib/R/site-library/SparseM 
#COPY --from=r-build-env /usr/local/lib/R/site-library/MASS/ /usr/local/lib/R/site-library/MASS
#COPY --from=r-build-env /usr/local/lib/R/site-library/cluster/ /usr/local/lib/R/site-library/cluster
COPY --from=r-build-env /usr/local/lib/R/site-library/CCC/ /usr/local/lib/R/site-library/CCC   

# packages dependencies for aurelius
COPY --from=r-build-env /usr/local/lib/R/site-library/aurelius/ /usr/local/lib/R/site-library/aurelius  
COPY --from=r-build-env /usr/local/lib/R/site-library/foreach/ /usr/local/lib/R/site-library/foreach    
COPY --from=r-build-env /usr/local/lib/R/site-library/gbm/ /usr/local/lib/R/site-library/gbm            
COPY --from=r-build-env /usr/local/lib/R/site-library/glmnet/ /usr/local/lib/R/site-library/glmnet      
COPY --from=r-build-env /usr/local/lib/R/site-library/iterators/ /usr/local/lib/R/site-library/iterators
COPY --from=r-build-env /usr/local/lib/R/site-library/jsonlite/ /usr/local/lib/R/site-library/jsonlite  

# packages dependencies for svglite
COPY --from=r-build-env /usr/local/lib/R/site-library/BH/ /usr/local/lib/R/site-library/BH          
COPY --from=r-build-env /usr/local/lib/R/site-library/gdtools/ /usr/local/lib/R/site-library/gdtools
COPY --from=r-build-env /usr/local/lib/R/site-library/svglite/ /usr/local/lib/R/site-library/svglite
COPY --from=r-build-env /usr/local/lib/R/site-library/withr/ /usr/local/lib/R/site-library/withr   





COPY main.R /src/
COPY tests/testthat.R /src/tests/
COPY tests/testthat/ /src/tests/testthat/

ENV DOCKER_IMAGE=hbpmip/r-3c:0.1.0 \
    FUNCTION=r-3c

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL eu.humanbrainproject.function=r-3c \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="Shay Yaacoby, Loduvic Claude" \
      eu.humanbrainproject.function.organisation="" \
      eu.humanbrainproject.function.date="" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/r-3c" \
      org.label-schema.description="3C-strategy implementation" \
      org.label-schema.url="" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/HBPMedical/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="" \
      org.label-schema.license="Apache2.0" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
