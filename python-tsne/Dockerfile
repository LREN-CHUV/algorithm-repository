FROM hbpmip/python-mip:0.2.5

MAINTAINER b.van_lew@lumc.nl

ENV DOCKER_IMAGE=hbpmip/python-tsne:0.3.3 \
    FUNCTION=python-tsne

# This COPY may be replaced by a build step when the atsne is open sourced (BvL 19/09/2017)
COPY atsne/ /atsne/
COPY requirements.txt /requirements.txt
COPY tsne.py /tsne.py

RUN pip install -r /requirements.txt
RUN apt-get update -y -qq && \
    apt-get install -y qt5-default && \
    apt-get install -y libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# For dev purposes (i.e. docker exec) use the following noop daemon
# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["python", "/tsne.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-tsne" \
      org.label-schema.description="Python wrapper for approximated tSNE" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LKEB LUMC" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
