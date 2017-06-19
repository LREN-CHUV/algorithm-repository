FROM hbpmip/java-rapidminer:ab6aa23

MAINTAINER arnaud@ahead.solutions.ch

ENV DOCKER_IMAGE=hbpmip/java-rapidminer-knn:latest
ENV JAVA_CLASSPATH=${JAVA_CLASSPATH}:./dist/java-rapidminer-knn.jar
ENV JAVA_ARGS=ch.lren.hbpmip.rapidminer.models.Knn

COPY target/java-rapidminer-knn.jar /dist/java-rapidminer-knn.jar

ENV MODEL knn
ENV FUNCTION java-rapidminer-knn
