FROM hbpmip/java-mip:latest

MAINTAINER arnaud@ahead-solutions.ch

# Install the dependencies
COPY pom.xml /dist/pom.xml
RUN chown -R compute:compute /dist
RUN exec gosu compute /usr/bin/mvn -f /dist dependency:resolve

COPY src /dist/src
COPY tests/java /dist/tests
RUN chown -R compute:compute /dist/src
RUN chown -R compute:compute /dist/tests
RUN exec gosu compute /usr/bin/mvn -f /dist compile

ENV FUNCTION rapidminer
