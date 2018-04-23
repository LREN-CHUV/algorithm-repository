FROM hbpmip/python-distributed-kmeans

COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt

COPY requirements-dev.txt /src/
RUN pip install -r /src/requirements-dev.txt

ENTRYPOINT ["python", "-m", "pytest", "/tests/unit"]
