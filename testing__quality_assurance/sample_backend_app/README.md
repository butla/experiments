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
- why is Pylint taking so long scanning SQLAlchemy?
- make sure the use of SQLAlchemy is correct. I'm still learning it :)
- Add Github CI for the app
