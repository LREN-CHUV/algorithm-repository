FROM hbpmip/r-job:1ed44df

MAINTAINER ludovic.claude54@gmail.com

RUN installGithub.r LREN-CHUV/hbpsummarystats@33e64db1

LABEL eu.humanbrainproject.function=summary-stats \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="Lester Melie-Garcia" \
      eu.humanbrainproject.function.organisation="LREN, CHUV" \
      eu.humanbrainproject.function.date="2015-06-27"

COPY main.R pfa.yml /src/
COPY tests/testthat.R /src/tests/
COPY tests/testthat/ /src/tests/testthat/

ENV FUNCTION r-summary-stats
