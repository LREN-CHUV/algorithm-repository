FROM hbpmip/r-job:33e64db1

MAINTAINER ludovic.claude54@gmail.com

RUN installGithub.r HBPSP8Repo/Rtsne@f72a26d

LABEL eu.humanbrainproject.function=tsne \
      eu.humanbrainproject.function.location=node \
      eu.humanbrainproject.function.version=0.1 \
      eu.humanbrainproject.function.author="Ludovic Claude" \
      eu.humanbrainproject.function.organisation="LREN, CHUV" \
      eu.humanbrainproject.function.date="2016-03-17"

COPY main.R pfa.yml /src/
COPY tests/testthat.R /src/tests/
COPY tests/testthat/ /src/tests/testthat/

ENV FUNCTION r-tsne
