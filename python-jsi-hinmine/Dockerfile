FROM hbpmip/python-mip:0.2.4

MAINTAINER jan.kralj@ijs.si

ENV DOCKER_IMAGE=hbpmip/python-jsi-hinmine:0.1.0 \
    FUNCTION=python-jsi-hinmine

# Install system packages
RUN apt-get update \
  && apt-get install -y git gcc python3-dev \
  && python -m pip install --upgrade pip

# Install hinmine and its requirements
COPY netSDM/ /project/netSDM
COPY mip_hinmine.py /project/mip_hinmine.py
COPY requirements_mip.txt /project/requirements_mip.txt

WORKDIR /project/netSDM

RUN python3.6 setup.py install

WORKDIR /project

RUN pip install -r /project/netSDM/requirements.txt \
  && pip install -r /project/requirements_mip.txt \
  && rm -rf /project/netSDM

ENTRYPOINT ["python3.6", "/project/mip_hinmine.py"]

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
