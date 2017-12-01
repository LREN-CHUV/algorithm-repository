FROM hbpmip/r-base-build:3.4.2-2 as r-build-env

RUN install.r gpsasi

FROM hbpmip/r-mip:0.4.0

MAINTAINER ludovic.claude54@gmail.com

COPY --from=r-build-env /usr/local/lib/R/site-library/hbplregress/ /usr/local/lib/R/site-library/hbplregress/

COPY main.R /src/
COPY tests/testthat.R /src/tests/
COPY tests/testthat/ /src/tests/testthat/

ENV DOCKER_IMAGE=hbpmip/r-ggparci:0.1.0 \
    FUNCTION=ggparci

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL eu.humanbrainproject.function=ggparci \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="ADD" \
      eu.humanbrainproject.function.organisation="ADD" \
      eu.humanbrainproject.function.date="ADD" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/ggparci" \
      org.label-schema.description="Parallel coordinates with confidence intervals" \
      org.label-schema.url="ADD" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="ADD" \
      org.label-schema.license="Apache2.0" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
