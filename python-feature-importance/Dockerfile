## Run unit tests

FROM hbpmip/python-mip-sklearn:0.3.10

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /tmp/* /var/tmp/* /var/cache/* /var/lib/apt/lists/*

COPY requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY feature_importance.py /src/feature_importance.py
COPY tests/unit/ /src/tests/

WORKDIR /src
RUN pytest tests/ -x --ff --capture=no

## Build target image

FROM hbpmip/python-mip-sklearn:0.3.10

MAINTAINER mirco.nasuti@chuv.ch

ENV DOCKER_IMAGE=hbpmip/python-feature-importance:0.3.1 \
    FUNCTION=python-feature-importance

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /tmp/* /var/tmp/* /var/cache/* /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY feature_importance.py /src/feature_importance.py

ENTRYPOINT ["python", "/src/feature_importance.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-feature-importance" \
      org.label-schema.description="Python implementation of linear regression" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
