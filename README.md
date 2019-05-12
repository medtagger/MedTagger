# MedTagger

**MedTagger** is a collaborative framework for annotating **medical datasets**.

Main goal of this project was to design and develop software environment,
which helps in **aggregation and labeling** huge datasets of medical scans,
powered by idea of **crowdsourcing**. Platform also provides mechanism for
label **validation**, thus making produced datasets of labels more reliable
for the future use.

MedTagger is still **under heavy development**, so please keep in mind that
many things may change or new versions may not be fully backward compatible.
Contact with us directly in case you want to use our work :)

Documentation for the MedTagger can be found [here](/docs).

[![Build Status](https://travis-ci.com/medtagger/MedTagger.svg?branch=master)](https://travis-ci.com/medtagger/MedTagger)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Our technology stack

 - User Interface uses [TypeScript 2.7+](http://typescriptlang.org/) with [Angular 6](http://angular.io/) and [Material Design](http://material.angular.io/) style,
 - REST API and WebSockets for communication with Backend,
 - Backend written in [Python 3.7](https://www.python.org),
 - [Flask](http://flask.pocoo.org/) with [Flask-RESTPlus](http://flask-restplus.readthedocs.io/) as a REST API framework,
 - [Celery](http://www.celeryproject.org/) workers using [RabbitMQ](https://www.rabbitmq.com/) for communication,
 - [PostgreSQL](https://www.postgresql.org/) as a storage for metadata,
 - [Cassandra](http://cassandra.apache.org/) as a storage for images,
 - [Docker](http://docker.com/) containers for production setup,
 - [Traefik](https://traefik.io/) as a reverse proxy and load balancer for Docker containers,
 - [Vagrant](https://www.vagrantup.com) for development environment,
 - [Travis](http://travis-ci.org/) for Continuous Integration.

## MedTagger setup

MedTagger consists of two main parts:
 - `frontend` - User Interface application written in TypeScript & Angular ([more](/frontend)),
 - `backend` - system's architecture and API written in Python ([more](/backend)).

### Development

To set up MedTagger locally you can use Vagrant virtual machine:

```bash
$ vagrant up
```

Then follow up with our [documentation](/docs). Default development account is:
 - email: `admin@medtagger`,
 - password: `medtagger`.

### Docker environment

MedTagger can be set up easily with Docker-Compose:

```bash
$ docker-compose up
```

More about setting up environment with Docker-Compose can be found [here](/docs/setup_with_docker_compose.md).

### Data Analysis with Jupyter Notebook

Together with Docker-Compose setup, you can use Jupyter Notebook server to easily analyse collected annotations.
 [Here](/examples/data_analysis) you can find some examples that shows how to do so.

More information about setting up local Jupyter Notebook session can be found [here](/docs/jupyter_notebook.md).

## User Interface

Below screenshots show how MedTagger looks like:

#### Login Page
![Login Page](/docs/assets/login-page.png)

#### Home Page
![Home Page](/docs/assets/home-page.png)

#### Labeling Page
![Labeling Page](/docs/assets/labeling-page-1.png)
![Labeling Page](/docs/assets/labeling-page-2.png)
![Labeling Page](/docs/assets/labeling-page-3.png)
