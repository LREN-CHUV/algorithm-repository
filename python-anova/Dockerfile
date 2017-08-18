FROM hbpmip/python-mip:435075d

COPY requirements.txt /requirements.txt
COPY anova.py /main.py

RUN conda install -y --file /requirements.txt

ENV DOCKER_IMAGE=hbpmip/python-anova
ENV MODEL anova
ENV FUNCTION python-anova
ENV CODE anova
ENV NAME Anova
