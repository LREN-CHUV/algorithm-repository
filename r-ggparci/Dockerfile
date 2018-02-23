FROM hbpmip/r-base-build:3.4.2-2 as r-build-env

ENV GGPARCI_VERSION=0.2.0
RUN installGithub.r HBPMedical/ggparci@0.2.0

FROM hbpmip/r-mip:0.4.1

MAINTAINER ludovic.claude54@gmail.com

COPY --from=r-build-env /usr/local/lib/R/site-library/assertthat/ /usr/local/lib/R/site-library/assertthat/    
COPY --from=r-build-env /usr/local/lib/R/site-library/BH/ /usr/local/lib/R/site-library/BH/                    
COPY --from=r-build-env /usr/local/lib/R/site-library/bindr/ /usr/local/lib/R/site-library/bindr/              
COPY --from=r-build-env /usr/local/lib/R/site-library/bindrcpp/ /usr/local/lib/R/site-library/bindrcpp/        
COPY --from=r-build-env /usr/local/lib/R/site-library/cli/ /usr/local/lib/R/site-library/cli/                  
COPY --from=r-build-env /usr/local/lib/R/site-library/colorspace/ /usr/local/lib/R/site-library/colorspace/    
COPY --from=r-build-env /usr/local/lib/R/site-library/crayon/ /usr/local/lib/R/site-library/crayon/            
COPY --from=r-build-env /usr/local/lib/R/site-library/dichromat/ /usr/local/lib/R/site-library/dichromat/      
COPY --from=r-build-env /usr/local/lib/R/site-library/digest/ /usr/local/lib/R/site-library/digest/            
COPY --from=r-build-env /usr/local/lib/R/site-library/dplyr/ /usr/local/lib/R/site-library/dplyr/              
COPY --from=r-build-env /usr/local/lib/R/site-library/ggplot2/ /usr/local/lib/R/site-library/ggplot2/          
COPY --from=r-build-env /usr/local/lib/R/site-library/glue/ /usr/local/lib/R/site-library/glue/                
COPY --from=r-build-env /usr/local/lib/R/site-library/gtable/ /usr/local/lib/R/site-library/gtable/            
COPY --from=r-build-env /usr/local/lib/R/site-library/labeling/ /usr/local/lib/R/site-library/labeling/        
COPY --from=r-build-env /usr/local/lib/R/site-library/lazyeval/ /usr/local/lib/R/site-library/lazyeval/        
COPY --from=r-build-env /usr/local/lib/R/site-library/magrittr/ /usr/local/lib/R/site-library/magrittr/        
COPY --from=r-build-env /usr/local/lib/R/site-library/munsell/ /usr/local/lib/R/site-library/munsell/          
#COPY --from=r-build-env /usr/local/lib/R/site-library/pillar/ /usr/local/lib/R/site-library/pillar/            
COPY --from=r-build-env /usr/local/lib/R/site-library/pkgconfig/ /usr/local/lib/R/site-library/pkgconfig/      
COPY --from=r-build-env /usr/local/lib/R/site-library/plogr/ /usr/local/lib/R/site-library/plogr/              
COPY --from=r-build-env /usr/local/lib/R/site-library/plyr/ /usr/local/lib/R/site-library/plyr/                
COPY --from=r-build-env /usr/local/lib/R/site-library/purrr/ /usr/local/lib/R/site-library/purrr/              
COPY --from=r-build-env /usr/local/lib/R/site-library/R6/ /usr/local/lib/R/site-library/R6/                    
COPY --from=r-build-env /usr/local/lib/R/site-library/RColorBrewer/ /usr/local/lib/R/site-library/RColorBrewer/
COPY --from=r-build-env /usr/local/lib/R/site-library/Rcpp/ /usr/local/lib/R/site-library/Rcpp/                
COPY --from=r-build-env /usr/local/lib/R/site-library/reshape2/ /usr/local/lib/R/site-library/reshape2/        
COPY --from=r-build-env /usr/local/lib/R/site-library/rlang/ /usr/local/lib/R/site-library/rlang/              
COPY --from=r-build-env /usr/local/lib/R/site-library/scales/ /usr/local/lib/R/site-library/scales/            
COPY --from=r-build-env /usr/local/lib/R/site-library/stringi/ /usr/local/lib/R/site-library/stringi/          
COPY --from=r-build-env /usr/local/lib/R/site-library/stringr/ /usr/local/lib/R/site-library/stringr/          
COPY --from=r-build-env /usr/local/lib/R/site-library/tibble/ /usr/local/lib/R/site-library/tibble/            
COPY --from=r-build-env /usr/local/lib/R/site-library/tidyr/ /usr/local/lib/R/site-library/tidyr/              
COPY --from=r-build-env /usr/local/lib/R/site-library/tidyselect/ /usr/local/lib/R/site-library/tidyselect/    
#COPY --from=r-build-env /usr/local/lib/R/site-library/utf8/ /usr/local/lib/R/site-library/utf8/                
COPY --from=r-build-env /usr/local/lib/R/site-library/svglite/ /usr/local/lib/R/site-library/svglite/  
COPY --from=r-build-env /usr/local/lib/R/site-library/gdtools/ /usr/local/lib/R/site-library/gdtools/  
COPY --from=r-build-env /usr/local/lib/R/site-library/withr/ /usr/local/lib/R/site-library/withr/  
COPY --from=r-build-env /usr/local/lib/R/site-library/ggparci/ /usr/local/lib/R/site-library/ggparci/  

COPY main.R /src/
COPY tests/testthat.R /src/tests/
COPY tests/testthat/ /src/tests/testthat/

ENV DOCKER_IMAGE=hbpmip/r-ggparci:0.1.0 \
    FUNCTION=r-ggparci

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL eu.humanbrainproject.function=ggparci \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="Shay Yaacoby, Tal Galili, Loduvic Claude" \
      eu.humanbrainproject.function.organisation="" \
      eu.humanbrainproject.function.date="" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/ggparci" \
      org.label-schema.description="Parallel coordinates Plot with confidence intervals" \
      org.label-schema.url="" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/HBPMedical/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="" \
      org.label-schema.license="Apache2.0" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
