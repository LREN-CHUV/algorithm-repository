FROM hbpmip/python-mip-sklearn:latest

MAINTAINER mirco.nasuti@chuv.ch

ENV DOCKER_IMAGE=hbpmip/python-knn:0.0.1 \
    FUNCTION=python-knn

RUN apt-get update
RUN apt-get install -y git

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY knn.py /knn.py

# TODO: put these dependencies out of /python-knn
COPY sklearn_to_pfa /sklearn_to_pfa

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
