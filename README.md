# genifest

Genifest generates Manifest Files for the Green Software Impact Framework by combining usage data from a server with a template file

## Installation

```bash
cd genifest

# Create a virtual environemt.
python3.9 -m venv venv
source venv/bin/activate

# Install package as editable including development requirements.
make develop

# After the repository is prepared commit this as your initial commit
git add .
git commit -m "Initial commit"
```

## Development

A lot of commong task during development are available using the `make` command.
Here is a list of available commands:

```bash
clean                Remove all Python artifacts.
clean-pyc            Remove Python file artifacts.
clean-dist           Clean build artifacts.
test                 Run tests quickly with the default Python.
docs:                Build docs.
docs-serve:          Build docs and serve on a local webserver.
coverage             Run coverage.
format               Format code following configured styleguide.
install              Install the package to the active Python site-packages.
develop              Install the package for local development.
bumbversion          Bump version based on conventional commits.
changelog            Generate CHANGELOG.md based on conventional commits.
check-version        Check versions of installed packages.
dist                 Build package.
docker-build         Build container for this application.
docker-publish       Publish docker container on docker.io.
docker-run-develop   Run bash in container for development.
docker-run           Run docker container.
```

This repository makes use of [pre-commit hooks](https://pre-commit.com)
to automatically do some cleanup and enforce code style before something is
actually commited.

## Credit

This template was generated from the [Cookiecutter mypyproject](https://gitlab.com/irlaender/cookiecutter-mypyproject) template.
