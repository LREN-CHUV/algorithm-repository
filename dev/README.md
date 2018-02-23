
# Development environment

To assist the integration of new algorithms, it can be quite useful to be able to have a database containing sample data and result tables running on your desktop and open to all applications, including RStudio, Jupiter notebooks...

The db.sh script is doing exactly that: it starts a local Postgres database and installs sample data and the result table.

Usage:

```sh
  ./db.sh
```

You can connect to the database server on localhost, port 5432.

There are 2 databases available in this Postgres server:

* 'data': username: 'data', password: 'data'

It contains several sample databases. Please refer to [sample-data-db-setup](https://github.com/HBPMedical/sample-data-db-setup) project for details.

* 'woken': username: 'woken', password: 'woken'

It contains the JOB_RESULTS table used to store the results of the algorithm.
