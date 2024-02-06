quality-check: isort black flake8 mypy

poetry:
	pip install poetry
	poetry install

pre-commit:
	pre-commit install
	pre-commit autoupdate

isort:
	isort . --profile black

black:
	black .

mypy:
	mypy .

flake8:
	flake8 .

build-bot-docker:
	docker compose down
	docker compose up --build --force-recreate bot
