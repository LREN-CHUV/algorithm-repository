FROM hbpmip/java-base-build:3.5.0-jdk-8-8 as build-java-env

COPY pom.xml /project/pom.xml
COPY src/ /project/src

# Repeating the file copy works better. I dunno why.
RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn package site

FROM hbpmip/java-rapidminer:0.9.0

MAINTAINER arnaud@ahead-solutions.ch

ENV DOCKER_IMAGE=hbpmip/java-rapidminer-naivebayes:0.2.0 \
    JAVA_CLASSPATH=${JAVA_CLASSPATH}:/usr/share/jars/java-rapidminer-naivebayes.jar \
    JAVA_ARGS=/eu/humanbrainproject/mip/algorithms/rapidminer/naivebayes/settings.properties \
    MODEL="Naive Bayes" \
    FUNCTION=java-rapidminer-naivebayes

COPY --from=build-java-env /project/target/naivebayes.jar /usr/share/jars/java-rapidminer-naivebayes.jar
COPY --from=build-java-env /project/target/site/ /var/www/html/
COPY src/ /src/

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/java-rapidminer-naivebayes" \
      org.label-schema.description="Naive Bayes algorithm" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
