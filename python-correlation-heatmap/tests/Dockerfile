# TODO: this should be extending `Dockerfile` in the parent directory, not image in production. Use multi-stage
# build for that
FROM hbpmip/python-correlation-heatmap

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY requirements-dev.txt /src/
RUN pip install -r /src/requirements-dev.txt

ENTRYPOINT ["python", "-m", "pytest", "/tests/unit"]
