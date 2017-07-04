FROM hbpmip/python-mip:d2c0f87

COPY requirements.txt /requirements.txt
COPY histograms.py /main.py

RUN conda install -y --file /requirements.txt

ENV DOCKER_IMAGE=hbpmip/python-histograms
ENV MODEL histograms
ENV FUNCTION python-histograms
ENV CODE histo
ENV NAME Histograms
