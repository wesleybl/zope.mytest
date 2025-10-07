# Makefile for zope.mytest package
VENV_NAME = venv
PYTHON = python3
VENV_PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip

.PHONY: help venv install install-dev test clean lint format check-format

help:  ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

venv:  ## Create Python virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Virtual environment created in $(VENV_NAME)/"

install: venv  ## Install package dependencies
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install zope.interface

install-dev: install  ## Install package in development mode
	@echo "Installing package in development mode..."
	$(PIP) install -e .
	@echo "Package installed in development mode"

test: install-dev  ## Run tests
	@echo "Running tests..."
	$(VENV_PYTHON) tests.py

lint: install-dev  ## Run linting (requires pylint)
	@echo "Installing pylint..."
	$(PIP) install pylint
	@echo "Running linting..."
	$(VENV_PYTHON) -m pylint src/zope/mytest/

format: install-dev  ## Format code with black (requires black)
	@echo "Installing black..."
	$(PIP) install black
	@echo "Formatting code..."
	$(VENV_PYTHON) -m black src/ tests.py

check-format: install-dev  ## Check code formatting (requires black)
	@echo "Installing black..."
	$(PIP) install black
	@echo "Checking code formatting..."
	$(VENV_PYTHON) -m black --check src/ tests.py

example: install-dev  ## Run usage example
	@echo "Running usage example..."
	$(VENV_PYTHON) -c "from zope.mytest import usage_example; usage_example()"

clean:  ## Remove virtual environment and build artifacts
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete"

build: install-dev  ## Build package for distribution
	@echo "Building package..."
	$(VENV_PYTHON) setup.py sdist bdist_wheel

activate:  ## Show command to activate virtual environment
	@echo "To activate the virtual environment, run:"
	@echo "  source $(VENV_NAME)/bin/activate"

check-deps:  ## Check if dependencies are installed
	@echo "Checking dependencies..."
	$(VENV_PYTHON) -c "import zope.interface; print('zope.interface is installed')"

verify-pylance-issue: install-dev  ## Verify that code works despite Pylance errors
	@echo "Running Pylance issue verification..."
	$(VENV_PYTHON) verify_pylance_issue.py