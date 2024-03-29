Sample back-end app
===================

A sample back-end app used to illustrate testing and development techniques.

## Development operations

The commands are in the Makefile. Please review it.

## Demonstrated techniques

- integrated and external (functional / end-to-end) tests with Docker Compose
- reloading app container on code changes (`make run_reloading`)
- running tests on code changes (`make test_reloading`)
- injectable locally bound container ports - accommodating self-hosted CI runners
- autogenerated SQL migrations
- migrations without the downgrade option. Downgrades create a risk of data loss in a real system.
  If there are issues with the migrations the solution is to provide fixes in new migrations.
- ...others...


## TODOs

- make `mypy` pass
- switch out pylint, black, and isort for ruff
- pytest: stop trying to interpret TestsConfig as a test class
  - https://docs.pytest.org/en/7.1.x/example/pythoncollection.html
- show coverage measurements from docker in external tests
- `make check` should also verify that requirements.txt is up to date with poetry dependencies
- Add Github CI for the app that removes docker-compose.override.yml to fully check the app image
- app versioning
