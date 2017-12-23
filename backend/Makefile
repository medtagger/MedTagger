# Global constants for whole Makefile
PYTHON = python3.6
MAIN_MODULE = medtagger
UNIT_TESTS_MODULE = tests/unit_tests
FUNCTIONAL_TESTS_MODULE = tests/functional_tests
DOCKER_COMPOSE_FILE = docker-compose.yml
SCRIPTS_DIRECTORY = scripts
COVERAGE_LIMIT = 0

# Third party configuration files
PYLINT_CONFIG_FILE = .pylintrc
PYLINT_UNIT_TESTS_CONFIG_FILE = .test.pylintrc

#
# Development
#

venv:
	virtualenv -p $(PYTHON) venv
	venv/bin/pip install -r requirements.txt

install_packages:
	$(PYTHON) -m pip install -r requirements.txt

run_api:
	PYTHONPATH=`pwd` $(PYTHON) medtagger/api/app.py

run_workers:
	PYTHONPATH=`pwd` celery -A medtagger.workers worker --loglevel=info

#
# Testing
#

test: test_pylint test_flake8 test_mypy unit_tests

test_pylint:
	pylint $(MAIN_MODULE) $(SCRIPTS_DIRECTORY) --rcfile=$(PYLINT_CONFIG_FILE)
	pylint $(UNIT_TESTS_MODULE) --rcfile=$(PYLINT_UNIT_TESTS_CONFIG_FILE)
	pylint $(FUNCTIONAL_TESTS_MODULE) --rcfile=$(PYLINT_UNIT_TESTS_CONFIG_FILE)

test_flake8:
	flake8 $(MAIN_MODULE) $(UNIT_TESTS_MODULE) $(FUNCTIONAL_TESTS_MODULE) $(SCRIPTS_DIRECTORY)

test_mypy:
	mypy --ignore-missing-imports $(MAIN_MODULE) $(UNIT_TESTS_MODULE) $(FUNCTIONAL_TESTS_MODULE) $(SCRIPTS_DIRECTORY)

unit_tests:
	. $(UNIT_TESTS_MODULE)/configuration.sh && pytest --cov=$(MAIN_MODULE) --cov-fail-under=$(COVERAGE_LIMIT) $(UNIT_TESTS_MODULE)

functional_tests:
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && ./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && pytest $(FUNCTIONAL_TESTS_MODULE)

functional_tests_docker:
	./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
	pytest $(FUNCTIONAL_TESTS_MODULE)

#
# Utilities
#

clean:
	rm -rf venv
	find . -name '*.pyc' -delete

.PHONY: venv install_packages run_api run_workers clean test test_pylint test_flake8 test_mypy unit_tests functional_tests
