FROM registry.federation.mip.hbp/mip_base/r-job:latest

MAINTAINER ludovic.claude54@gmail.com

LABEL eu.humanbrainproject.function=box-stats \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="Lester Melie-Garcia" \
      eu.humanbrainproject.function.organisation="LREN, CHUV" \
      eu.humanbrainproject.function.date="2015-06-27"

COPY downloads/hbpsummarystats_0.0.0.9000_R_x86_64-pc-linux-gnu.tar.gz /tmp/hbpsummarystats.tar.gz
COPY main.R /src/

RUN R CMD INSTALL /tmp/hbpsummarystats.tar.gz
