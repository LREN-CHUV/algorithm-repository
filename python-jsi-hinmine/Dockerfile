FROM hbpmip/python-mip:0.5.6

MAINTAINER jan.kralj@ijs.si

ENV DOCKER_IMAGE=hbpmip/python-jsi-hinmine:0.2.3 \
    FUNCTION=python-jsi-hinmine

# Install system packages
RUN apt-get update \
  && apt-get install -y git gcc python3-dev \
  && python -m pip install --upgrade pip

# Install hinmine and its requirements
COPY netSDM/ /src/netSDM
COPY mip_hinmine.py /src/mip_hinmine.py
COPY requirements.txt /src/requirements.txt
COPY doc/ /src/doc/

WORKDIR /src/netSDM

RUN python3.6 setup.py install

WORKDIR /src

RUN pip install -r /src/netSDM/requirements.txt \
  && pip install -r /src/requirements.txt \
  && rm -rf /src/netSDM

ENTRYPOINT ["python3.6", "/src/mip_hinmine.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-jsi-hinmine" \
      org.label-schema.description="HINMine algorithm for network propositionalization" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="JSI KT" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
