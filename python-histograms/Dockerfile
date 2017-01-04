FROM hbpmip/python-mip:53c6b8c

RUN conda install -y numpy
RUN conda update numpy

ADD histograms.py .

ENV DOCKER_IMAGE=hbpmip/python-histograms
ENV MODEL histograms
ENV FUNCTION python-histograms
ENV CODE histo
ENV NAME Histograms
