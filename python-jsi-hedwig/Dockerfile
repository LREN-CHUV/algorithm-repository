FROM hbpmip/python-mip:0.5.6

MAINTAINER anze.vavpetic@ijs.si

ENV DOCKER_IMAGE=hbpmip/python-jsi-hedwig:1.0.5 \
    FUNCTION=python-jsi-hedwig

COPY requirements.txt /src/requirements.txt

# Install system packages
RUN apt-get update \
    && apt-get install -y git gcc python3-dev \
    && python -m pip install --upgrade pip \
    && pip install -r /src/requirements.txt

COPY hedwig/ /src/hedwig
COPY doc/ /src/doc/

WORKDIR /src/hedwig
RUN pip install -r requirements.txt

COPY preprocess.py /src/hedwig/
COPY mip_hedwig.py /src/hedwig/
RUN python setup.py install

ENTRYPOINT ["python", "/src/hedwig/mip_hedwig.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-jsi-hedwig" \
      org.label-schema.description="Hedwig method for semantic subgroup discovery" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="JSI KT" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
