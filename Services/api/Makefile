.PHONY: quality-check poetry isort black mypy flake8 api-tests api-tests-cov api-tests-cov-report

quality-check: isort black flake8 mypy

poetry:
	pip install poetry
	poetry install

isort:
	isort .

black:
	black .

mypy:
	mypy .

flake8:
	flake8 .

# Tests
api-tests:
	python -m pytest --disable-warnings tests
api-tests-cov:
	coverage run -m pytest --disable-warnings tests
api-tests-cov-report:
	python -m pytest --cov --cov-report=html:coverage_report --disable-warnings tests
