# Global constants for whole Makefile
PYTHON = python3.6
MAIN_MODULE = data_labeling
UNIT_TESTS_MODULE = tests
COVERAGE_LIMIT = 0

# Third party configuration files
PYLINT_CONFIG_FILE = .pylintrc
PYLINT_UNIT_TESTS_CONFIG_FILE = .test.pylintrc

# Our application configuration files
UNIT_TESTS_CONFIG_FILE = backend_api.test.conf

#
# Development
#

venv:
	virtualenv -p $(PYTHON) venv
	venv/bin/pip install -r requirements.txt

install_packages:
	$(PYTHON) -m pip install -r requirements.txt

run_api:
	PYTHONPATH=`pwd` $(PYTHON) data_labeling/api/app.py

run_worker:
 	PYTHONPATH=`pwd` celery -A data_labeling.workers worker --loglevel=info

#
# Testing
#

test: test_pylint test_flake8 test_mypy test_pytest

test_pylint:
	pylint $(MAIN_MODULE) --rcfile=$(PYLINT_CONFIG_FILE)
	pylint $(UNIT_TESTS_MODULE) --rcfile=$(PYLINT_UNIT_TESTS_CONFIG_FILE)

test_flake8:
	flake8 $(MAIN_MODULE) $(UNIT_TESTS_MODULE)

test_mypy:
	mypy --ignore-missing-imports $(MAIN_MODULE) $(UNIT_TESTS_MODULE)

test_pytest:
	CONFIG_FILE=$(UNIT_TESTS_CONFIG_FILE) pytest --cov=$(MAIN_MODULE) --cov-fail-under=$(COVERAGE_LIMIT) $(UNIT_TESTS_MODULE)

#
# Utilities
#

clean:
	rm -rf venv
	find . -name '*.pyc' -delete

.PHONY: venv install_packages run_api run_workers clean test test_pylint test_flake8 test_mypy test_pytest
