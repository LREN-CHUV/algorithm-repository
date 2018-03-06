FROM hbpmip/r-3c

COPY testthat.R /src/tests/
COPY testthat/ /src/tests/testthat/

WORKDIR /src

ENTRYPOINT ["/usr/bin/Rscript", "/src/tests/testthat.R"]
