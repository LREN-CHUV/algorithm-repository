(these are just my personal notes, will be removed when PR is no longer WIP)

# How it all works:
1. User specifices algorithm, variables & covariables in MIP frontend (creates JSON request in the background)
2. POST request to `/mining/job` with body
```
{
    "user": {"code": "user1"},
    "variables": [{"code": "var1"}],
    "covariables": [{"code": "var2"},{"code": "var3"}],
    "grouping": [{"code": "var4"}],
    "filters": [],
    "algorithm": "python-sgd-regression",
    "datasets": [{"code": "dataset1"},{"code": "dataset2"}],
    "targetTable": "cde_features_A",
}
```
3. `woken` converts request body to ENV variables and runs `docker-compose run python-sgd-regression compute`
4. script in a container loads data from sample / production database tables `cde_features_A, cde_features_B and cde_features_C` and writes intermediate result to DB on each partial update (everything in that single script)
5. last job result will be saved into a database as a PFA model


# Notes:
- don't forget to stop your local PG database, otherwise `psql -h localhost -U data -d data` won't work and would try to connect to your local one and not the one running on Docker
