Sample back-end app
===================

A sample backend app used to illustrate testing and development techniques.

## Development operations

Most of the commands are in the Makefile

### Additional commands

Creating a migration: `poetry run alembic revision --autogenerate -m <message>`

## TODOs

- make `mypy` pass
- show coverage measurements from docker in external tests
- show that I don't normally do downgrade migrations
- external tests should wait for the API to become available to enable testing with reloads
- `make check` should also verify that requirements.txt is up to date with poetry dependencies
- why is Pylint taking so long scanning SQLAlchemy?
- make sure the use of SQLAlchemy is correct. I'm still learning it :)
- Add Github CI for the app
