FROM hbpmip/python-summary-statistics

COPY requirements-dev.txt /src/
RUN pip install -r /src/requirements-dev.txt

ENTRYPOINT ["python", "-m", "pytest", "/tests/unit"]
