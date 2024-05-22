.PHONY: clean help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-pyc clean-dist ## Remove all Python artifacts.

clean-pyc: ## Remove file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.coverage' -exec rm -fr {} +
	find . -name 'coverage.xml' -exec rm -fr {} +

clean-dist: ## Clean build artifacts.
	rm -rf build
	rm -rf dist

test: ## Run tests quickly with the default Python.
	pytest

docs: ## Build docs
	mkdocs docs

docs-serve: ## Build docs and serve on a local webserver.
	mkdocs serve

coverage: ## Run tests quickly with the default Python.
	pytest --cov-report xml --cov-report term-missing --cov=genifest tests --cov-fail-under=100

format: ## Format code following configured styleguide.
	pre-commit run --all

install: clean ## Install the package to the active Python's site-packages.
	pip install -e .

develop: clean ## Install the package for local development.
	[ ! -d .git ] && git init || echo "Git repository already exists"
	pip install --upgrade pip
	pip install -e ".[development]"
	pip freeze | grep -v git+ssh > docker/requirements.txt
	pre-commit install
	pre-commit autoupdate
	cz init

check-version: ## Check versions of installed packages.
	pip-licenses --from=mixed --order=license

bumpversion: ## Bump version based on conventional commits.
	cz bump

changelog: ## Generate CHANGELOG.md based on conventional commits.
	cz changelog

dist: clean-dist ## Build package.
	python3 setup.py sdist bdist_wheel

docker-build: dist ## Build container for this application.
	docker build -t toirl/genifest -f docker/Dockerfile .
docker-build-develop: ## Build container for development in PyCharm
	docker build --target develop -t toirl/genifest-develop -f docker/Dockerfile .

docker-publish: docker-build ## Publish docker container on docker.io.
	# Stable "latest" tag
	docker tag toirl/genifest toirl/genifest:latest
	docker push toirl/genifest:latest
	# Stable major tag
	docker tag toirl/genifest toirl/genifest:$$(python docker/buildtags.py major)
	docker push toirl/genifest:$$(python docker/buildtags.py major)
	# Stable minor tag
	docker tag toirl/genifest toirl/genifest:$$(python docker/buildtags.py minor)
	docker push toirl/genifest:$$(python docker/buildtags.py minor)
	# Unique rev tag
	docker tag toirl/genifest toirl/genifest:$$(python docker/buildtags.py commit)
	docker push toirl/genifest:$$(python docker/buildtags.py commit)

docker-run-develop: ## Run bash in container for development.
	docker run --rm -it -v $$(pwd):/app --entrypoint /bin/bash toirl/genifest-develop

docker-run: ## Run docker container.
	docker run --rm -it toirl/genifest
