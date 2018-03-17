FROM hbpmip/python-histograms

COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt

COPY requirements-dev.txt /src/
RUN pip install -r /src/requirements-dev.txt

COPY tests/unit_test.py /src/tests/
WORKDIR /src/tests/

ENTRYPOINT ["python", "-m", "pytest", "/tests/unit"]
