Sample back-end app
===================

A sample backend app used to illustrate testing and development techniques.

## Development operations

Most of the commands are in the Makefile

### Additional commands

Creating a migration: `poetry run alembic revision --autogenerate -m <message>`

## TODOs

- `make static_checks` should pass
- show that I don't normally do downgrade migrations
