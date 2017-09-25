FROM hbpmip/java-base-build:3.5.0-jdk-8-7 as build-java-env

COPY pom.xml /project/pom.xml
COPY src/ /project/src

# Repeating the file copy works better. I dunno why.
RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn package site

FROM hbpmip/java-rapidminer:0.7.6

MAINTAINER arnaud@ahead-solutions.ch

ENV DOCKER_IMAGE=hbpmip/java-rapidminer-knn:0.1.0
ENV JAVA_CLASSPATH=${JAVA_CLASSPATH}:/usr/share/jars/java-rapidminer-knn.jar
ENV JAVA_ARGS=/eu/humanbrainproject/mip/algorithms/rapidminer/models/knn/settings.properties
ENV MODEL knn
ENV FUNCTION java-rapidminer-knn

COPY --from=build-java-env /project/target/java-rapidminer-knn.jar /usr/share/jars/java-rapidminer-knn.jar
COPY --from=build-java-env /project/target/site/ /var/www/html/
COPY src/ /src/

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/java-rapidminer-knn" \
      org.label-schema.description="KNN algorithm" \
      org.label-schema.url="https://github.com/LREN-CHUV/functions-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/functions-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="AGPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
