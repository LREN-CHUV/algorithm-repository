FROM hbpmip/python-mip:b856e51

COPY requirements.txt /requirements.txt
COPY anova.py /main.py

RUN conda install -y --file /requirements.txt

ENV DOCKER_IMAGE=hbpmip/python-anova
ENV MODEL anova
ENV FUNCTION python-anova
ENV CODE anova
ENV NAME Anova
