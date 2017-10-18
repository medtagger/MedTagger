Native setup
------------

Native setup may be a good idea for machines that won't be able to handle heavy virtual machine. Native setup consumes
less RAM, which may be needed if your PC has eg. 4GB of RAM.

### Requirements

Here is a list of things that you need to run our backend natively:
 - Linux (recommended Ubuntu) / macOS,
 - Python 3.6,
 - Virtualenv,
 - Make,
 - RabbitMQ, Hadoop and HBase (can be set up using Docker Compose).

### How to do this?

**Important:** Before following below steps, please make sure that you've got access to the Rabbit, HBase and other
dependencies. To do so, please follow steps from the docs [here](dependencies_via_docker_compose.md)!

Let's start! At first, please clone this repository somewhere on your computer:

```bash
$ git clone git@gitlab.com:praca-inzynierska/Backend-API.git
```

Then, you'll be able to create a virtual environment which may be helpful to manage your dependencies locally. To do so,
please run below make's entry and activate it:

```bash
$ make venv
$ . vevn/bin/activate
```

It's time to create a configuration file. Please create a new empty file and name it `backend_api.conf`. Base on
an example file (`backend_api.example.conf`) and fill your configuration with all needed entries.

Your project is now ready to be run but your HBase database is still empty. Before you start your journey with backend,
launch script that will create all tables in HBase.

```bash
(venv) $ python3.6 migrate_hbase.py
```

It will ask you a few questions and answer them with `y` or `yes` to create all needed entries.

**_Tip!_** This script may be useful one day to create new tables or delete a new one. Please check documentation
inside of this script for more information.

Now, your backend is ready to be used, so let's try to run it!

Open two separate windows with activated virtual environment. In the first one we'll run Celery workers which are
responsible for adding and converting Dicoms to our HBase. To run it, please execute such command:

```bash
$ make run_workers
```

In the second window we'll open our Flask REST API with WebSockets server. To do so, please execute:

```bash
$ make run_api
```

And that's all! Everything should be fine and Swagger for our REST API should be available on
`http://localhost:51000/api/v1`.
