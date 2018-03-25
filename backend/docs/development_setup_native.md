Running backend natively
------------------------

Native setup may be a good idea for machines that won't be able to handle heavy virtual machine. Native setup consumes
less RAM, which may be needed if your PC has eg. 4GB of RAM.

### Requirements

Here is a list of things that you need to run our backend natively:
 - Linux (recommended Ubuntu) / macOS,
 - Python 3.6,
 - Python 3.6-dev,
 - Virtualenv,
 - Make,
 - Docker with Docker-Compose.

### How to do this?

Let's start! At first, please clone this repository somewhere on your computer:

```bash
$ git clone git@github.com:jpowie01/MedTagger.git
$ cd MedTagger
```

Then, you'll be able to create a virtual environment which may be helpful to manage your dependencies locally. To do so,
please run below make's entry and activate it:

```bash
$ cd backend
$ sudo make install_system_dependencies
$ make venv
$ . ./devenv.sh
```

You can now run all dependencies like HBase, PostgreSQL and RabbitMQ with just one command:
```bash
(venv) $ make start_dependencies
```

Now, your backend is ready to be used, so let's try to run it!

Open three separate windows with activated virtual environment. In the first one we'll run Celery workers which are
responsible for adding and converting Dicoms to our HBase. To run it, please execute such command:

```bash
$ . ./devenv.sh
(venv) $ make run_workers
```

In the second window we'll open our Flask REST API server. To do so, please execute:

```bash
$ . ./devenv.sh
(venv) $ make run_rest
```

And in the third window we'll open WebSocket server:

```bash
$ . ./devenv.sh
(venv) $ make run_websocket
```

And that's all! Everything should be fine and Swagger for our REST API should be available on
`http://localhost:51000/api/v1`.

### How to update dependencies (eg. database schema)?

To make sure that your databases are up-to-date use:

```bash
(venv) $ make update_dependencies
```

