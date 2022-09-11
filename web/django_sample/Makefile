.PHONY: run

# be sure to be in an activated virtualenv
run: migrate
	# We don't have tests that run against the live server yet, but you can call the server and
	# see what code is being touched with this.
	COVERAGE_PROCESS_START=.coveragerc poetry run python manage.py runserver

test:
	# TODO add pylint
	# TODO add YAPF?
	poetry run coverage erase
	poetry run coverage run -m pytest
	poetry run coverage combine
	poetry run coverage report -m

migrate:
	poetry run python manage.py migrate

make_migrations:
	poetry run python manage.py makemigrations

shell:
	poetry run python manage.py shell_plus
