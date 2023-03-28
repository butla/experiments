# all variables will be exported to child processes
.EXPORT_ALL_VARIABLES:

# So we're sure what shell we're using.
SHELL:=/bin/bash

SOURCES:=app tests

setup_development:
	poetry install

run: db_migration
	docker-compose up -d

db_migration:
	poetry run alembic upgrade head

check: static_checks test

format:
	@echo ==================
	@echo Formatting code...
	@echo ==================
	@poetry run black $(SOURCES)

	@echo ==================
	@echo Sorting imports...
	@echo ==================
	@poetry run isort $(SOURCES)

shell:
	poetry run ptpython

static_checks:
	@echo ==========================
	@echo Checking import sorting...
	@echo ==========================
	@poetry run isort -c $(SOURCES)

	@echo ===========================
	@echo Checking code formatting...
	@echo ===========================
	@poetry run black --check $(SOURCES)

	# TODO
	# @echo =================
	# @echo Checking types...
	# @echo =================
	# @poetry run mypy $(SOURCES)

	@echo ==========
	@echo Linting...
	@echo ==========
	@poetry run pylint $(SOURCES)

test:
	@echo ================
	@echo Running tests...
	@echo ================
	@poetry run pytest tests

test_continously:
	fd --exclude .git --no-ignore '\.py$$' | entr -c make test

export_requirements:
	poetry export --output=requirements.txt

