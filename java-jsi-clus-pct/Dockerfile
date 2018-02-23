FROM hbpmip/java-base-build:3.5.0-jdk-8-9 as build-java-env

COPY pom.xml /project/pom.xml
RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn dependency:resolve

COPY src/ /project/src

# Repeating copy of the settings works better. I dunno why.
RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn -Dmaven.test.skip=true package site

FROM hbpmip/java-jsi-clus:latest

MAINTAINER martin.breskvar@ijs.si

ENV DOCKER_IMAGE=java-jsi-clus-pct \
	FUNCTION=java-jsi-clus-pct \
    JAVA_CLASSPATH=${JAVA_CLASSPATH}:/usr/share/jars/jsi-clus-pct.jar \
    JAVA_MAINCLASS=eu.humanbrainproject.mip.algorithms.jsi.clus.pct.Entrypoint

COPY --from=build-java-env /project/target/jsi-clus-pct.jar /usr/share/jars/jsi-clus-pct.jar
COPY --from=build-java-env /project/target/site/ /var/www/html/
COPY src/ /src/
COPY doc/ /src/doc/

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/java-jsi-clus-pct" \
      org.label-schema.description="PCT algorithm for multi-target prediction" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="JSI KT" \
      org.label-schema.license="GPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
