.PHONY: run

run:
	cd tests; bash -c "docker-compose up --build; docker-compose down -v"

test:
	pipenv run pytest -v tests/
