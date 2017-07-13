FROM hbpmip/java-rapidminer:7eeec79

MAINTAINER arnaud@ahead.solutions.ch

ENV DOCKER_IMAGE=hbpmip/java-rapidminer-naivebayes:latest
ENV JAVA_CLASSPATH=${JAVA_CLASSPATH}:./dist/java-rapidminer-naivebayes.jar
ENV JAVA_ARGS=eu.hbp.mip.container.rapidminer.models.NaiveBayes

COPY target/java-rapidminer-naivebayes.jar /dist/java-rapidminer-naivebayes.jar

ENV MODEL Naive Bayes
ENV FUNCTION java-rapidminer-naivebayes
