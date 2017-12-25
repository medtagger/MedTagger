Backend API
-----------

Repository contains code for backend written in Python.

### Development setup

There are two ways to setup your environment:
 - virtual machine using Vagrant ([more information](backend/docs/development_setup_vagrant.md)),
 - or natively on your host ([more information](backend/docs/development_setup_native.md)).

### Good to know about development

Here you can find good practices and tips for development:
 - [Changing database models](backend/docs/changing_database_models.md).

### Testing your code
Use `make test` to test your code. It will run PyLint, Flake8, MyPy and PyTest with all of our unit tests.
 The same thing happens in GitLab CI, so make sure that your code is properly linted and tested!

You can also run `make functional_tests`. This will run the tests on real dependencies running inside of
 the Docker containers that you can [setup with Docker Compose](docs/development_via_docker_compose.md).

