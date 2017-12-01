FROM hbpmip/r-base-build:3.4.2-2 as r-build-env

RUN installGithub.r LREN-CHUV/hbplregress@f5b3ee4f4

FROM hbpmip/r-mip:0.4.0

MAINTAINER ludovic.claude54@gmail.com

COPY --from=r-build-env /usr/local/lib/R/site-library/hbplregress/ /usr/local/lib/R/site-library/hbplregress/

COPY main.R pfa.yml.whisker /src/
COPY tests/testthat.R /src/tests/
COPY tests/testthat/ /src/tests/testthat/

ENV DOCKER_IMAGE=hbpmip/r-linear-regression:0.1.0 \
    FUNCTION=r-linear-regression

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL eu.humanbrainproject.function=linear-regression \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="Lester Melie-Garcia" \
      eu.humanbrainproject.function.organisation="LREN, CHUV" \
      eu.humanbrainproject.function.date="2015-06-27" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/r-linear-regression" \
      org.label-schema.description="Linear regression in R" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="Apache2.0" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
