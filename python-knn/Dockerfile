## Run unit tests

FROM hbpmip/python-base-build:0.4.5

COPY requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY knn.py /src/knn.py
COPY tests/unit/ /src/tests/

WORKDIR /src
#RUN pytest tests/ -x --ff --capture=no

## Build target image

FROM hbpmip/python-mip-sklearn:0.3.10

ENV DOCKER_IMAGE=hbpmip/python-knn:0.3.2 \
    FUNCTION=python-knn

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY knn.py /knn.py

ENTRYPOINT ["python", "/knn.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-knn" \
      org.label-schema.description="Python implementation of sgd-regression" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
