# Global constants for whole Makefile
PYTHON = python3.7
MAIN_MODULE = medtagger
SCRIPTS_DIRECTORY = scripts

# Tests configuration
ifdef TESTS
	TESTS_TO_RUN = -k $(TESTS)
else
	TESTS_TO_RUN =
endif
COVERAGE_LIMIT = 0
MAX_CYCLOMATIC_COMPLEXITY = 5
UNIT_TESTS_MODULE = tests/unit_tests
FUNCTIONAL_TESTS_MODULE = tests/functional_tests
FUNCTIONAL_TESTS_DOCKER_COMPOSE = ../.travis/backend_functional_tests_docker-compose.yml
PYTEST_SLOWEST_TESTS=30

# Third party configuration files
PYLINT_CONFIG_FILE = .pylintrc
PYLINT_UNIT_TESTS_CONFIG_FILE = .test.pylintrc

#
# Development setup
#

venv:
	# Disable Cassandra Driver tweaks - not needed in development setup
	export CASS_DRIVER_NO_CYTHON=1
	export CASS_DRIVER_NO_EXTENSIONS=1
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

run_database_migrations:
	PYTHONPATH=`pwd` alembic upgrade head

#
# Dependencies
#

start_dependencies:
	cd .. && docker-compose up -d cassandra postgres rabbitmq
	make update_dependencies

stop_dependencies:
	cd .. && docker-compose down

clear_dependencies: stop_dependencies
	docker volume rm medtagger_postgres-data medtagger_cassandra-data medtagger_rabbitmq-data

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
	. $(UNIT_TESTS_MODULE)/configuration.sh && pytest --cov=$(MAIN_MODULE) --cov-fail-under=$(COVERAGE_LIMIT) --durations=$(PYTEST_SLOWEST_TESTS) $(UNIT_TESTS_MODULE) $(TESTS_TO_RUN)

functional_tests:
	make functional_tests__prepare_environment
	@if ! make functional_tests__run; then\
		make functional_tests__clear_dependencies;\
		echo "Functional tests failed!";\
		exit 1;\
	fi
	echo "Functional tests passed!"
	make functional_tests__delete_environment

functional_tests__prepare_environment:
	docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) up -d cassandra postgres rabbitmq
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && ./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && alembic upgrade head

functional_tests__run:
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && pytest --durations=$(PYTEST_SLOWEST_TESTS) $(FUNCTIONAL_TESTS_MODULE) $(TESTS_TO_RUN)
	
functional_tests__delete_environment:
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && alembic downgrade base
	make functional_tests__clear_dependencies

functional_tests__clear_dependencies:
	docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) down

functional_tests_docker:
	./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
	alembic upgrade head
	pytest --durations=$(PYTEST_SLOWEST_TESTS) $(FUNCTIONAL_TESTS_MODULE)
	alembic downgrade base

#
# Utilities
#

clean:
	rm -rf venv
	find . -name '*.swp' -delete
	find . -name '*.pyc' -delete
	find . -name '*.log' -delete

.PHONY: venv install_packages run_api run_workers start_dependencies stop_dependencies update_dependencies clean test test_pylint test_flake8 test_mypy unit_tests functional_tests
