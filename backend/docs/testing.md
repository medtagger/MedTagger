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

## Functional tests

MedTagger Backend supports functional tests. To define them we use PyTest with prepared set of
 REST & WebSocket API testing clients.

To run such tests, please make sure that all of the dependencies are running on your machine. You can use
 Docker-Compose to do so:

```bash
(venv) $ docker-compose up -d hbase postgres rabbitmq
(venv) $ make functional_tests
(venv) $ docker-compose down
```

