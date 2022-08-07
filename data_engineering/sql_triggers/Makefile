.PHONY: run

# MAIN commands
# =========================

run:
	docker-compose up -d

migrate:
	poetry run python -m triggers.schema_setup

db_enter:
	PGPASSWORD=secret pgcli -h localhost -d postgres -p 5432 -U postgres

check: test static_checks

# SECONDARY commands
# =========================

test:
	poetry run pytest -v triggers/test_triggers.py

static_checks:
	poetry run pylint triggers
