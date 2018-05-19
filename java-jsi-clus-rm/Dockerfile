FROM hbpmip/java-base-build:3.5.2-jdk-8-0 as build-java-env

COPY pom.xml /project/pom.xml
COPY src/ /project/src
COPY deps/ /project/deps

RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn dependency:go-offline

# Repeating copy of the settings works better. I dunno why.
RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn package site

FROM hbpmip/java-mip:0.5.7

MAINTAINER martin.breskvar@ijs.si

ENV DOCKER_IMAGE=java-jsi-clus-rm \
	FUNCTION=java-jsi-clus-rm \
    JAVA_CLASSPATH=${JAVA_CLASSPATH}:/opt/weka/props/:/usr/share/jars/jsi-clus-rm-deps.jar:/usr/share/jars/lib/*:/usr/share/jars/Redescription_mining_MW_ConstrainedGen1.jar:/usr/share/jars/CLUSNHMC.jar \
    JAVA_MAINCLASS=eu.humanbrainproject.mip.algorithms.jsi.clus.rm.Entrypoint \
    WEKA_HOME=/opt/weka

COPY docker/databases-props/ /opt/weka/databases-props/
COPY --from=build-java-env /project/deps/ /usr/share/jars/
COPY --from=build-java-env /project/target/jsi-clus-rm-deps.jar /usr/share/jars/jsi-clus-rm-deps.jar
COPY --from=build-java-env /project/target/site/ /var/www/html/
COPY src/ /src/
COPY doc/ /src/doc/

RUN mkdir -p /opt/weka/props/weka/experiment \
    && chown -R compute:compute /mip/ /opt/weka/ /usr/share/jars/

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/

WORKDIR /usr/share/jars

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/java-jsi-clus-rm" \
      org.label-schema.description="PCT-based algorithm for Redescription Mining" \
      org.label-schema.url="https://github.com/LREN-CHUV/algorithm-repository" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/algorithm-repository.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="JSI KT and IRB ZEL" \
      org.label-schema.license="GPLv3" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
