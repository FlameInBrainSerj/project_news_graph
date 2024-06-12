.PHONY: quality-check poetry pre-commit isort black mypy flake8 bot-tests bot-tests-cov bot-tests-cov-report alembic-init alembic-upgrade-head

poetry:
	pip install poetry
	poetry install
pre-commit:
	pre-commit install
	pre-commit autoupdate

# Code quality
quality-check: isort black flake8 mypy
isort:
	isort .
black:
	black .
mypy:
	mypy . --explicit-package-bases
flake8:
	flake8 .

# Tests
bot-tests:
	python -m pytest tests
bot-tests-cov:
	coverage run -m pytest tests
bot-tests-cov-report:
	pytest --cov --cov-report=html:coverage_report


# Alembic
alembic-init:
	alembic revision --autogenerate -m 'initial'
alembic-upgrade-head:
	alembic upgrade head
