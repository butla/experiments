.PHONY: run

# MAIN commands
# =========================

run:
	docker-compose up -d

migrate:
	poetry run python -m triggers.migrations

db_enter:
	PGPASSWORD=secret pgcli -h localhost -d postgres -p 5432 -U postgres

check: test

# SECONDARY commands
# =========================

test:
	poetry run pytest -v triggers/test_triggers.py
