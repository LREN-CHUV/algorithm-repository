FROM hbpmip/python-histograms

COPY tests/data/ /src/tests/data/
COPY requirements-dev.txt /src/
RUN pip install -r /src/requirements-dev.txt

COPY data_tracking/ /src/data_tracking/
RUN pip install -e /src/

COPY tests/unit_test.py /src/tests/

WORKDIR /src/tests/

ENTRYPOINT ["/bin/sh", "-c", "nosetests", "unit_test.py"]
