# All variables will be exported to child processes. Can be useful later.
.EXPORT_ALL_VARIABLES:

# So we're sure what shell we're using.
SHELL:=/bin/bash

SOURCES:=sample_backend tests

# MAIN COMMANDS
# ==============

setup_development:
	poetry install

run: _start_compose db_migration

check: static_checks test

format:
	@echo "=== Formatting code... ==="
	@poetry run black $(SOURCES)
	@echo "=== Sorting imports... ==="
	@poetry run isort $(SOURCES)

# UTILITY COMMANDS
# ================

build_docker: export_requirements
	docker compose build

destroy:
	docker compose down -v

show_api_documentation:
	xdg-open http://localhost:8080/docs

shell:
	poetry run ptpython

db_shell:
	PGPASSWORD=postgres poetry run pgcli -h localhost -p 5432 -U postgres -d postgres

docker_app_shell:
	docker exec -it sample_backend_app-api-1 sh

# SUBCOMMANDS
# ===========
db_migration:
	@echo "=== Running DB migrations... ==="
	poetry run alembic upgrade head

# Usage make make_migration MESSAGE="<a message>"
make_migration:
	@echo "=== Autogenerating DB migrations... ==="
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"


export_requirements:
	poetry export --output=requirements.txt

_start_compose:
	@echo "=== Starting Docker Compose... ==="
	docker compose up -d

test:
	@echo === Running tests... ===
	@poetry run pytest tests

test_reloading:
	fd --exclude .git --no-ignore '\.py$$' | entr -c make test

static_checks: _check_isort _check_format _check_linter _check_types

_check_isort:
	@echo === Checking import sorting... ===
	@poetry run isort -c $(SOURCES)

_check_format:
	@echo === Checking code formatting... ===
	@poetry run black --check $(SOURCES)

_check_linter:
	@echo === Linting... ===
	@poetry run pylint $(SOURCES)

_check_types:
	@echo === Checking types... ===
	@poetry run mypy $(SOURCES)
