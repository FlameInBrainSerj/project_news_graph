.PHONY: run-pipeline quality-check poetry isort black mypy flake8 run-scrapers run-preprocessing run-model-train run-model-inference

run-pipeline: run-scrapers run-preprocessing run-model-train run-model-inference

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
	docker compose up -d
	python .\scrapers\scrapers_main.py
	docker compose down

run-preprocessing:
	python .\preprocessing\preprocessing_main.py

run-model-train:
	python .\model\train.py

run-model-inference:
	python .\model\infer.py
