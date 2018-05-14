## Run unit tests

FROM hbpmip/python-base-build:0.4.5

COPY requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY correlation_heatmap.py /src/correlation_heatmap.py
COPY tests/unit/ /src/tests/

WORKDIR /src
RUN pytest tests/ -x --ff --capture=no

## Build target image

FROM hbpmip/python-mip:0.6.1

MAINTAINER mirco.nasuti@chuv.ch

ENV DOCKER_IMAGE=hbpmip/python-correlation-heatmap:0.3.1 \
    FUNCTION=python-correlation-heatmap

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY correlation_heatmap.py /src/correlation_heatmap.py

ENTRYPOINT ["python", "/src/correlation_heatmap.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-correlation-heatmap" \
      org.label-schema.description="Python implementation of Statistics" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
