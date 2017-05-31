FROM hbpmip/python-mip:8f296be

RUN conda install -y numpy
RUN conda update numpy

COPY histograms.py /main.py

ENV DOCKER_IMAGE=hbpmip/python-histograms
ENV MODEL histograms
ENV FUNCTION python-histograms
ENV CODE histo
ENV NAME Histograms
