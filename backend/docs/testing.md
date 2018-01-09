Testing MedTagger Backend
-------------------------

Backend tests always run on each Pull Request that you will send to our repository. To check your code
 locally follow the instructions below.

## Linters & Unit tests

MedTagger Backend uses many linters and checkers to make sure that our codebase follows Python standards.
 We use PyLint, Flake8 with many plugins and MyPy for type checking. We also use PyTest for definition of
 all unit tests.

To run such linters and tests please execute:

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

MedTagger Backend supports also functional tests. To define them we use PyTest with prepared set of
 REST & WebSocket API testing clients.

To run such tests, please make sure that all of the dependencies are running on your machine. Use
 Docker-Compose to do so:

```bash
(venv) $ docker-compose up -d hbase postgres rabbitmq
(venv) $ make functional_tests
(venv) $ docker-compose down
```

