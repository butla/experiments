.PHONY: run

# be sure to be in an activated virtualenv
run: migrate
	# We don't have tests that run against the live server yet, but you can call the server and
	# see what code is being touched with this.
	COVERAGE_PROCESS_START=.coveragerc python manage.py runserver

test:
	# TODO add pylint
	# TODO add YAPF?
	coverage erase
	coverage run -m pytest
	coverage combine
	coverage report -m

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

shell:
	python manage.py shell_plus
