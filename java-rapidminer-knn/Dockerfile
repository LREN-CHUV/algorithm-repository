FROM hbpmip/java-rapidminer:aee168e

MAINTAINER arnaud@ahead.solutions.ch

ENV DOCKER_IMAGE=hbpmip/java-rapidminer-knn:latest
ENV JAVA_CLASSPATH=${JAVA_CLASSPATH}:./dist/java-rapidminer-knn.jar
ENV JAVA_ARGS=eu.hbp.mip.container.rapidminer.models.Knn

COPY target/java-rapidminer-knn.jar /dist/java-rapidminer-knn.jar

ENV MODEL knn
ENV FUNCTION java-rapidminer-knn
