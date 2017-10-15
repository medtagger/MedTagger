Backend API
-----------

Repository contains code for backend API written in Python.

### How to setup dev instance?
There are two ways to setup your environment:
 - virtual machine using Vagrant,
 - or natively on your host.

You can also setup all services like Hadoop, HBase, etc. with Docker Compose.

#### Vagrant
Vagrant is the easiest way to prepare your dev environment. At first, please make sure that you've properly
 installed it on your OS with instructions from their
 [documentation](https://www.vagrantup.com/intro/getting-started/install.html).

Then follow these steps:
 1. Clone this repository.
 2. Use PyCharm's Vagrant plugin or CLI command `vagrant up` to start our Virtual Machine,
 3. Prepare your configuration file and name it `backend_api.conf`. Check `backend_api.example.conf` - it contains
    all entries that you need to provide.
 4. Setup your PyCharm's interpreter - make sure that it points to Vagrant's VM and it's python binaries.
    Use `data_labeling/api/app.py` as entry point and make sure that `/vagrant/` is your working directory.
 5. In parallel you can also run `make run_worker` (via `vagrant ssh`) which will set up your Celery worker
    used for data processing (not needed if you don't want to add any new data to the storage).

Then - everything should be fine and application should be available on `http://10.0.0.99:51000/api/v1`.

_**TIP!**_ You can always use `vagrant ssh` to enter VM's bash. It will be useful during local testing.

#### Native setup
Requirements:
 - Linux (recommended Ubuntu) / macOS
 - Python 3.6
 - Virtualenv
 - Make
 - RabbitMQ, Hadoop and HBase (eg. in Docker containers)

On Linux it's really easy to setup your environment:
 1. Clone this repository.
 2. Use `make venv` to setup your virtual environment.
 3. Activate your environment with `. venv/bin/activate`.
 4. Prepare your configuration file and name it `backend_api.conf`. Check `backend_api.example.conf` - it contains
    all entries that you need to provide.
 5. Run our application with `python data_labeling/api/app.py` or `make run_api`.
 6. In another window/terminal run `make run_worker` to start Celery worker.

That's all! Now you can go to `http://localhost:51000/api/v1` and develop this application!

##### Docker Compose for all dependencies
Requirements:
 - Docker Engine,
 - Docker Compose - it is highly possible that it was part of Docker Engine. If needed, install it with
   [this](https://docs.docker.com/compose/install/#install-compose) instruction.

It's really easy to start all needed external dependencies:
```bash
$ docker-compose up
```

_**TIP!**_ Add `-d` (detach) option to run everything in the background.

### Testing your code
Use `make test` to test your code. It will run PyLint, Flake8, MyPy and PyTest with all of our unit tests.
 The same thing happen in GitLab CI, so make sure that your code is properly linted and tested!
