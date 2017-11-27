FROM hbpmip/python-mip:0.2.3

MAINTAINER mirco.nasuti@chuv.ch

ENV DOCKER_IMAGE=hbpmip/python-histograms:0.3.4 \
    FUNCTION=python-histograms

COPY requirements.txt /requirements.txt
COPY histograms.py /histograms.py

RUN pip install -r /requirements.txt

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
