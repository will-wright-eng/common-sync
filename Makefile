#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

#* Setup
.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))
.DEFAULT_GOAL := help

help: ## list make commands
	@echo ${MAKEFILE_LIST}
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#* Commands
docker-kill: ## kill all docker containers
	@./scripts/docker-kill.sh

# https://jupyter-docker-stacks.readthedocs.io/en/latest/
run-nb: ## run jupyter notebook on port 10000
	@echo "http://<hostname>:10000/?token=<token>"
	docker run -it --rm -p 10000:8888 -v "${PWD}":/home/jovyan/work jupyter/datascience-notebook:85f615d5cafa

#* Poetry
poetry-download: ## poetry-download
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

poetry-remove: ## poetry-remove
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall

#* Installation
install: ## install
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n
	-poetry run mypy --install-types --non-interactive ./

pre-commit-install: ## pre-commit-install
	poetry run pre-commit install

#* Formatters
codestyle: ## codestyle
	poetry run pyupgrade --exit-zero-even-if-changed --py39-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
	poetry run black --config pyproject.toml ./

#* Linting
test: ## test
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=common_sync tests/
	poetry run coverage-badge -o assets/images/coverage.svg -f

check-codestyle: ## check-codestyle
	poetry run isort --diff --check-only --settings-path pyproject.toml ./
	poetry run black --diff --check --config pyproject.toml ./
	poetry run darglint --verbosity 2 common_sync tests

mypy: ## mypy
	poetry run mypy --config-file pyproject.toml ./

check-safety: ## check-safety
	poetry check
	poetry run safety check --full-report
	poetry run bandit -ll --recursive common_sync tests

update-dev-deps: ## update-dev-deps
	poetry add -D bandit@latest darglint@latest "isort[colors]@latest" mypy@latest pre-commit@latest pydocstyle@latest pylint@latest pytest@latest pyupgrade@latest safety@latest coverage@latest coverage-badge@latest pytest-html@latest pytest-cov@latest
	poetry add -D --allow-prereleases black@latest

#* Cleaning
pycache-remove: ## pycache-remove
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

dsstore-remove: ## dsstore-remove
	find . | grep -E ".DS_Store" | xargs rm -rf

mypycache-remove: ## mypycache-remove
	find . | grep -E ".mypy_cache" | xargs rm -rf

ipynbcheckpoints-remove: ## ipynbcheckpoints-remove
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

pytestcache-remove: ## pytestcache-remove
	find . | grep -E ".pytest_cache" | xargs rm -rf

build-remove: ## build-remove
	rm -rf build/

lint: test check-codestyle mypy check-safety

cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove
