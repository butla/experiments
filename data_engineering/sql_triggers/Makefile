.PHONY: run

# MAIN commands
# =========================

run: _run migrate

check: test static_checks

db_cli:
	PGPASSWORD=secret pgcli -h localhost -d postgres -p 5432 -U postgres

clean:
	fd --hidden --follow --exclude .git --no-ignore __pycache__ --exec rm -rf

# SECONDARY commands
# =========================

test:
	poetry run pytest -v tests

static_checks:
	poetry run pylint triggers

migrate:
	poetry run python -m triggers.schema_setup

_run:
	docker-compose up -d
