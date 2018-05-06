# Global constants for whole Makefile
PYTHON = python3.6
MAIN_MODULE = medtagger
SCRIPTS_DIRECTORY = scripts

# Tests configuration
COVERAGE_LIMIT = 0
MAX_CYCLOMATIC_COMPLEXITY = 5
UNIT_TESTS_MODULE = tests/unit_tests
UNIT_TEST = $(UNIT_TESTS_MODULE)
FUNCTIONAL_TESTS_MODULE = tests/functional_tests
FUNCTIONAL_TESTS_DOCKER_COMPOSE = ../.travis/backend_functional_tests_docker-compose.yml
FUNCTIONAL_TEST = $(FUNCTIONAL_TESTS_MODULE)

# Third party configuration files
PYLINT_CONFIG_FILE = .pylintrc
PYLINT_UNIT_TESTS_CONFIG_FILE = .test.pylintrc

#
# Development setup
#

venv:
	virtualenv -p $(PYTHON) venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -r requirements.dev.txt

install_packages:
	$(PYTHON) -m pip install -r requirements.txt

install_dev_packages:
	$(PYTHON) -m pip install -r requirements.dev.txt

#
# Running MedTagger
#

run_rest:
	PYTHONPATH=`pwd` $(PYTHON) medtagger/api/rest.py

run_rest_production:
	PYTHONPATH=`pwd` uwsgi --http :51000 --gevent 1000 --master --wsgi-file medtagger/api/rest.py --plugin http --http-keepalive --limit-post 10485760 --callable app --processes 4

run_websocket:
	PYTHONPATH=`pwd` $(PYTHON) medtagger/api/websocket.py

run_websocket_production:
	PYTHONPATH=`pwd` uwsgi --http :51001 --gevent 1000 --http-websockets --master --wsgi-file medtagger/api/websocket.py --callable app

run_workers:
	PYTHONPATH=`pwd` celery -A medtagger.workers worker --loglevel=info

#
# Dependencies
#

start_dependencies:
	cd .. && docker-compose up -d cassandra postgres rabbitmq
	make update_dependencies

stop_dependencies:
	cd .. && docker-compose down

clear_dependencies: stop_dependencies
	docker volume rm medtagger_postgres-data medtagger_hbase-data medtagger_rabbitmq-data

update_dependencies:
	./scripts/dev__prepare_backend.sh

#
# Testing
#

test: test_pylint test_flake8 test_mypy unit_tests

test_pylint:
	pylint $(MAIN_MODULE) $(SCRIPTS_DIRECTORY) --rcfile=$(PYLINT_CONFIG_FILE)
	pylint $(UNIT_TESTS_MODULE) $(FUNCTIONAL_TESTS_MODULE) --rcfile=$(PYLINT_UNIT_TESTS_CONFIG_FILE)

test_flake8:
	flake8 $(MAIN_MODULE) $(UNIT_TESTS_MODULE) $(FUNCTIONAL_TESTS_MODULE) $(SCRIPTS_DIRECTORY) --max-complexity=$(MAX_CYCLOMATIC_COMPLEXITY)

test_mypy:
	mypy --ignore-missing-imports $(MAIN_MODULE) $(UNIT_TESTS_MODULE) $(FUNCTIONAL_TESTS_MODULE) $(SCRIPTS_DIRECTORY)

unit_tests:
	. $(UNIT_TESTS_MODULE)/configuration.sh && pytest --cov=$(MAIN_MODULE) --cov-fail-under=$(COVERAGE_LIMIT) $(UNIT_TEST)

functional_tests:
	docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) up -d cassandra postgres rabbitmq
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && ./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && alembic upgrade head
	@if . $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && ! pytest $(FUNCTIONAL_TEST) ; then\
		docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) down;\
		echo "Functional tests failed!";\
		exit 1;\
	fi
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && alembic downgrade base
	docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) down
	echo "Functional tests passed!"

functional_tests_docker:
	./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
	alembic upgrade head
	pytest $(FUNCTIONAL_TESTS_MODULE)

#
# Utilities
#

clean:
	rm -rf venv
	find . -name '*.swp' -delete
	find . -name '*.pyc' -delete
	find . -name '*.log' -delete

.PHONY: venv install_packages run_api run_workers start_dependencies stop_dependencies update_dependencies clean test test_pylint test_flake8 test_mypy unit_tests functional_tests
