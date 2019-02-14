.PHONY: run

# be sure to be in an activated virtualenv
run: migrate
	python manage.py runserver

test:
	# TODO add pylint
	coverage run --source=django_sample/,polls/ -m pytest 
	coverage report -m

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

shell:
	python manage.py shell_plus
