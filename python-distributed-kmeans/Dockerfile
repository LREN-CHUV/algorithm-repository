FROM hbpmip/python-mip-sklearn:0.3.7

COPY requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY distributed_kmeans.py /src/distributed_kmeans.py
COPY tests/unit /src/tests/

WORKDIR /src
RUN pytest tests/ -x --ff --capture=no


FROM hbpmip/python-mip-sklearn:0.3.7

MAINTAINER mirco.nasuti@chuv.ch

ENV DOCKER_IMAGE=hbpmip/python-distributed-kmeans:0.0.2 \
    FUNCTION=python-distributed-kmeans

RUN apt-get update
RUN apt-get install -y git

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY distributed_kmeans.py /distributed_kmeans.py

ENTRYPOINT ["python", "/distributed_kmeans.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-distributed-kmeans" \
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
