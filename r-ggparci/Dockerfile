FROM hbpmip/r-base-build:3.4.2-2 as r-build-env

RUN installGithub.r HBPMedical/ggparci

FROM hbpmip/r-mip:0.4.1

MAINTAINER ludovic.claude54@gmail.com

COPY --from=r-build-env /usr/local/lib/R/site-library/hbplregress/ /usr/local/lib/R/site-library/hbplregress/

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
