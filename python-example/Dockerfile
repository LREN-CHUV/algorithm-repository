FROM hbpmip/python-mip:0.1.3

COPY requirements.txt /requirements.txt
COPY algo.py /main.py

RUN conda install -y --file /requirements.txt

ENV DOCKER_IMAGE=hbpmip/python-example
ENV MODEL example
ENV FUNCTION python-example
ENV CODE example
ENV NAME example
