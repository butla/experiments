# all variables will be exported to child processes
.EXPORT_ALL_VARIABLES:

# So we're sure what shell we're using.
SHELL:=/bin/bash

SOURCES:=sample_backend tests

# MAIN COMMANDS
# ==============

setup_development:
	poetry install

run: _start_compose db_migration

# You need to restart this command after adding new files
run_with_restarts: run
	fd --exclude .git --no-ignore '\.py$$' sample_backend | entr -c make _start_compose

check: static_checks test

format:
	@echo "=== Formatting code... ==="
	@poetry run black $(SOURCES)
	@echo "=== Sorting imports... ==="
	@poetry run isort $(SOURCES)

# UTILITY COMMANDS
# ================

rebuild_images:
	docker-compose build

wipe_data:
	docker-compose down -v

show_api_documentation:
	xdg-open http://localhost:8080/docs

shell:
	poetry run ptpython

db_shell:
	PGPASSWORD=postgres poetry run pgcli -h localhost -p 5432 -U postgres -d postgres

docker_app_shell:
	docker exec -it sample_backend_app-api-1 sh

export_requirements:
	poetry export --output=requirements.txt

# SUBCOMMANDS
# ===========
db_migration:
	@echo "=== Running DB migrations... ==="
	poetry run alembic upgrade head

_start_compose:
	@echo "=== Starting Docker Compose... ==="
	docker-compose up -d

static_checks:
	@echo === Checking import sorting... ===
	@poetry run isort -c $(SOURCES)

	@echo === Checking code formatting... ===
	@poetry run black --check $(SOURCES)

	@echo === Linting... ===
	@poetry run pylint $(SOURCES)

	@echo === Checking types... ===
	@poetry run mypy $(SOURCES)


test:
	@echo === Running tests... ===
	@poetry run pytest tests

# TODO this conflicts with run_with_restarts, as the container goes down for a moment
test_continously:
	fd --exclude .git --no-ignore '\.py$$' | entr -c make test
