FROM hbpmip/java-rapidminer:latest

MAINTAINER arnaud@ahead.solutions.ch

ENV DOCKER_IMAGE=hbpmip/java-rapidminer-naivebayes:latest
ENV JAVA_CLASSPATH=${JAVA_CLASSPATH}:./dist/java-rapidminer-naivebayes.jar
ENV JAVA_ARGS=ch.lren.hbpmip.rapidminer.models.NaiveBayes

COPY java-rapidminer-naivebayes.jar /dist/java-rapidminer-naivebayes.jar

ENV MODEL Naive Bayes
ENV FUNCTION java-rapidminer-naivebayes
