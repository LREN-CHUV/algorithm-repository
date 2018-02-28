import os
from fabric.api import run, env, cd, lcd, local, settings, task


algo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


@task
def start_db():
    """Start sample database for testing. See algorithm-repository/dev/README.md"""
    with lcd(algo_dir):
        local('./dev/db.sh')


@task
def psql_woken():
    local('PGPASSWORD=woken psql -h localhost -U woken')


@task
def psql_sample_data():
    local('PGPASSWORD=data psql -h localhost -U data')
