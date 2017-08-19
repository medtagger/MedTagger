PYTHON=python3.6
MAIN_MODULE=data_labeling
UNIT_TESTS_MODULE=tests

#
# Development
#

venv:
	virtualenv -p $(PYTHON) venv
	venv/bin/pip install -r requirements.txt

install_packages:
	$(PYTHON) -m pip install -r requirements.txt

#
# Testing
#

test: pylint flake8 mypy pytest

pylint:
	pylint $(MAIN_MODULE)

flake8:
	flake8 $(MAIN_MODULE)

mypy:
	mypy $(MAIN_MODULE)

pytest:
	pytest --cov=$(MAIN_MODULE) --cov-fail-under=80 $(UNIT_TESTS_MODULE)

#
# Utilities
#

clean:
	rm -rf venv

.PHONY: venv clean test pylint flake8 pytest
