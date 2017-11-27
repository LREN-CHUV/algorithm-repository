FROM hbpmip/python-mip:0.2.3

MAINTAINER mirco.nasuti@chuv.ch

ENV DOCKER_IMAGE=hbpmip/python-linear-regression:0.0.5 \
    FUNCTION=python-linear-regression

COPY requirements.txt /requirements.txt
COPY linear_regression.py /linear_regression.py

RUN pip install -r /requirements.txt

ENTRYPOINT ["python", "/linear_regression.py"]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/python-linear-regression" \
      org.label-schema.description="Python implementation of linear-regression" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
