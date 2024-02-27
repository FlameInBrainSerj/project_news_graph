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

run-scrapers:
	python .\scrapers\scrapers_main.py

run-preprocessing:
	python .\preprocessing\preprocessing_main.py
