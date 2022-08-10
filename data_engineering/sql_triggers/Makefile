.PHONY: run

# MAIN commands
# =========================

run: _run migrate

check: test static_checks

db_enter:
	PGPASSWORD=secret pgcli -h localhost -d postgres -p 5432 -U postgres

# SECONDARY commands
# =========================

test:
	poetry run pytest -v triggers/test_triggers.py

static_checks:
	poetry run pylint triggers

migrate:
	poetry run python -m triggers.schema_setup

_run:
	docker-compose up -d
