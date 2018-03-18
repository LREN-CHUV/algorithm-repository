FROM hbpmip/python-base-build:0.4.3

COPY requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY histograms.py /src/histograms.py
COPY tests/unit /src/tests/

WORKDIR /src
RUN pytest tests/

FROM hbpmip/python-mip:0.3.2

MAINTAINER mirco.nasuti@chuv.ch

ENV DOCKER_IMAGE=hbpmip/python-histograms:0.3.7 \
    FUNCTION=python-histograms

RUN apt-get update
RUN apt-get install -y git

COPY requirements.txt /requirements.txt

COPY histograms.py /histograms.py

ENTRYPOINT ["python", "/histograms.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-histograms" \
      org.label-schema.description="Python implementation of Histograms" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
