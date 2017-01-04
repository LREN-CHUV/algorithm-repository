FROM hbpmip/python-mip:222f8eb

RUN conda install -y numpy
RUN conda update numpy

ADD histograms.py .

ENV DOCKER_IMAGE=hbpmip/python-histograms
ENV MODEL histograms
ENV FUNCTION python-histograms
ENV CODE histo
ENV NAME Histograms
