# run unit-tests with `docker-compose build test_suite; docker-compose run test_suite`
# TODO: we have to rebuild Docker image on every change - how can we use `volumes` mapping instead?

FROM hbpmip/python-sgd-regression

COPY tests/unit/ /tests/unit
COPY requirements-dev.txt /src/
RUN pip install -r /src/requirements-dev.txt

ENTRYPOINT ["python", "-m", "pytest", "/tests/unit"]
