Testing MedTagger Backend
-------------------------

Backend tests run on each Pull Request that you will send to our repository. To check your code locally
 follow instructions below.

## Linters & Unit tests

MedTagger Backend uses many linters and checkers to make sure that our codebase follows Python standards.
 We use PyLint, Flake8 with many plugins and MyPy for type checking. We also use PyTest for definition of
 our unit tests.

To run linters and unit tests please execute:

```bash
$ . ./devenv.sh
(venv) $ make test
```

_**TIP!**_ You can also run specific tool by:

 - `make test_pylint`,
 - `make test_flake8`,
 - `make test_mypy`,
 - `make unit_tests`.

_**TIP!**_ You can also specify which unit test should be executed by:

```bash
(venv) $ make unit_tests UNIT_TEST=tests/unit_tests/api/core/test_business.py
```

## Functional tests

MedTagger Backend supports functional tests. To define them we use PyTest with prepared set of
 REST & WebSocket API testing clients.

To run such tests please execute:

```bash
(venv) $ make functional_tests
```

_**TIP!**_ You can also specify which functional test should be executed by:

```bash
(venv) $ make functional_tests FUNCTIONAL_TEST=tests/functional_tests/test_basic_flow.py 
```

