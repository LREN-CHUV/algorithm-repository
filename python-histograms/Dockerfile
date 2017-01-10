FROM hbpmip/python-mip:b1570ef

RUN conda install -y numpy
RUN conda update numpy

COPY histograms.py /main.py

ENV DOCKER_IMAGE=hbpmip/python-histograms
ENV MODEL histograms
ENV FUNCTION python-histograms
ENV CODE histo
ENV NAME Histograms
