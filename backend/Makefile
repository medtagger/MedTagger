# Global constants for whole Makefile
PYTHON = python3.6
MAIN_MODULE = medtagger
SCRIPTS_DIRECTORY = scripts
VENV_SITE_PACKAGES = venv/lib/python3.6/site-packages
PYTHON_INCLUDE_DIRECTORY = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")
PYTHON_LIBRARY_DIRECTORY = $(shell $(PYTHON) -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
PYTHON_SITE_PACKAGES = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
PYTHON_GDCM_DIRECTORY = $(shell $(PYTHON) -c 'import os, gdcm; print(os.path.split(gdcm.__file__)[0])' 2>&1 || '')
SYSTEM_NAME = $(shell uname -s)

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
# Development
#

venv:
	virtualenv -p $(PYTHON) venv
	cp -rf $(PYTHON_SITE_PACKAGES)/_gdcmswig.so $(VENV_SITE_PACKAGES) || echo "WARNING! GDCM not found" 
	cp -rf $(PYTHON_SITE_PACKAGES)/gdcm.py $(VENV_SITE_PACKAGES) || echo "WARNING! GDCM not found"
	cp -rf $(PYTHON_SITE_PACKAGES)/gdcmswig.py $(VENV_SITE_PACKAGES) || echo "WARNING! GDCM not found"
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -r requirements.dev.txt

install_system_dependencies:
	@if [ $(SYSTEM_NAME) = Darwin ]; then\
		brew install gdcm --with-python3;\
		cp -rf $(PYTHON_GDCM_DIRECTORY)/_gdcmswig.so $(PYTHON_SITE_PACKAGES);\
		cp -rf $(PYTHON_GDCM_DIRECTORY)/gdcm.py $(PYTHON_SITE_PACKAGES);\
		cp -rf $(PYTHON_GDCM_DIRECTORY)/gdcmswig.py $(PYTHON_SITE_PACKAGES);\
	else\
		apt-get update;\
		apt-get install -y cmake swig;\
		wget https://github.com/malaterre/GDCM/archive/v2.8.4.tar.gz;\
		tar xvf v2.8.4.tar.gz;\
		rm v2.8.4.tar.gz;\
		mkdir _build_gdcm;\
		cd _build_gdcm;\
		cmake -DGDCM_BUILD_SHARED_LIBS=ON -DGDCM_BUILD_APPLICATIONS=ON -DPYTHON_INCLUDE_DIR='$(PYTHON_INCLUDE_DIRECTORY)' -DPYTHON_LIBRARY='$(PYTHON_LIBRARY_DIRECTORY)' -DPYTHON_EXECUTABLE='$(PYTHON)' -DGDCM_INSTALL_PYTHONMODULE_DIR='$(PYTHON_SITE_PACKAGES)' -DGDCM_WRAP_PYTHON=ON ../GDCM-2.8.4;\
		make;\
		make install;\
		cd ..;\
		rm -rf _build_gdcm;\
	fi

install_packages:
	$(PYTHON) -m pip install -r requirements.txt

install_dev_packages:
	$(PYTHON) -m pip install -r requirements.dev.txt

run_api:
	PYTHONPATH=`pwd` $(PYTHON) medtagger/api/app.py

run_workers:
	PYTHONPATH=`pwd` celery -A medtagger.workers worker --loglevel=info

#
# Dependencies
#

start_dependencies:
	cd .. && docker-compose up -d hbase postgres rabbitmq
	make update_dependencies

stop_dependencies:
	cd .. && docker-compose down

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
	docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) up -d hbase postgres rabbitmq
	. $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && ./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
	@if . $(FUNCTIONAL_TESTS_MODULE)/configuration.sh && ! pytest $(FUNCTIONAL_TEST) ; then\
		echo "Functional tests failed!";\
		docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) down;\
		exit 1;\
	fi
	docker-compose -f $(FUNCTIONAL_TESTS_DOCKER_COMPOSE) down

functional_tests_docker:
	./$(SCRIPTS_DIRECTORY)/wait_for_dependencies.sh
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
