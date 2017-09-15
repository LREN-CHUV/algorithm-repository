FROM hbpmip/python-mip:6fb0698

# This COPY may be replaced by a build step when the atsne is open sourced (BvL 19/09/2017)
COPY atsne/ /atsne/
COPY requirements.txt /requirements.txt
COPY algo.py /main.py

RUN conda install -y --file /requirements.txt

ENV DOCKER_IMAGE=hbpmip/python-tsne
ENV MODEL example
ENV FUNCTION python-tsne
ENV CODE tsne
ENV NAME tsne
