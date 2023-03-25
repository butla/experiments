.EXPORT_ALL_VARIABLES:

# So we're sure what shell we're using.
SHELL:=/bin/bash

SOURCES:=app tests

run:
	poetry run uvicorn --port 8080 app.main:app

# TODO uvicorn with reload eats up CPU
run_continuously:
	fd --exclude .git --no-ignore '\.py$$' app | entr -rc make run

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

	@echo =================
	@echo Checking types...
	@echo =================
	@poetry run mypy $(SOURCES)

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
