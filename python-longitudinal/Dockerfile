FROM hbpmip/python-mip:latest as python-longitudinal-base

MAINTAINER clementine.fourrier@icm-institute.org

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="icm-base-docker" \
      org.label-schema.description="Base docker" \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="ICM" \
      org.label-schema.schema-version="1.0"

RUN echo "deb http://deb.debian.org/debian stretch main" >> /etc/apt/sources.list
RUN echo "deb-src http://deb.debian.org/debian stretch main" >> /etc/apt/sources.list

# Installing the basics (gcc, g++, ...)
#RUN rm var/lib/apt/lists/httpredir.debian.org_debian_dists_jessie_main_binary-amd64_Packages.gz
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y \
build-essential \
cmake \
git

# Installing armadillo
RUN apt-get install -y libopenblas-dev
RUN apt-get install -y liblapack-dev #libopenlapack to check and use instead
RUN apt-get install -y libarmadillo-dev

# Installing python
RUN apt-get install -y python-dev
RUN apt-get install -y python-pandas


FROM python-longitudinal-base

MAINTAINER clementine.fourrier@icm-institute.org

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/icm-algorithm" \
      org.label-schema.description="Executes the ICM algorithm" \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="ICM" \
      org.label-schema.schema-version="1.0"

# Installing Longitudina
RUN git clone https://oauth2:Qgqe3QnzXYAM7YsQTwd_@gitlab.icm-institute.org/aramislab/longitudina -b HBP longitudina
RUN cd longitudina/ && rm -rf build && \
git submodule init && git submodule update && \
cmake . && make

COPY src/utils/utils.py utils/utils.py
COPY src/utils/utils_highcharts.py utils/utils_highcharts.py
COPY src/utils/utils_inputs.py utils/utils_inputs.py
COPY src/utils/utils_PFA.py utils/utils_PFA.py
COPY main.py /main.py
COPY main_univariate.sh /main_univariate.sh
COPY main_multivariate.sh /main_multivariate.sh
#CMD ["./main.py"]