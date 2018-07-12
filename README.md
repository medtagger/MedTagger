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

[![Build Status](https://travis-ci.org/jpowie01/MedTagger.svg?branch=master)](https://travis-ci.org/jpowie01/MedTagger)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Waffle.io - Columns and their card count](https://badge.waffle.io/jpowie01/MedTagger.svg?columns=Backlog,Sprint,In%20Progress,Review%20%EF%B8%8F,Done)](https://waffle.io/jpowie01/MedTagger)

## Our technology stack

 - User Interface uses [TypeScript 2.7+](http://typescriptlang.org/) with [Angular 6](http://angular.io/) and [Material Design](http://material.angular.io/) style,
 - REST API and WebSockets for communication with Backend,
 - Backend written in [Python 3.6+](https://www.python.org),
 - [Flask](http://flask.pocoo.org/) with [Flask-RESTPlus](http://flask-restplus.readthedocs.io/) as a REST API framework,
 - [Celery](http://www.celeryproject.org/) workers using [RabbitMQ](https://www.rabbitmq.com/) for communication,
 - [PostgreSQL](https://www.postgresql.org/) as a storage for metadata,
 - [Cassandra](http://cassandra.apache.org/) as a storage for images,
 - [Docker](http://docker.com/) containers for production setup,
 - [Traefik](https://traefik.io/) as a reverse proxy and load balancer for Docker containers,
 - [Vagrant](https://www.vagrantup.com) for development environment,
 - [Travis](http://travis-ci.org/) for Continuous Integration.

## What are we doing now?

 - [ ] Labeling using multiple tools
   - [x] Rectangle
   - [x] Points
   - [x] Connected Points
   - [ ] Brush
 - [ ] Zoom for labeling small objects
 - [ ] Surveys as additional actions for provided labels
 - [ ] Validation mechanism
 - [ ] On-demand datasets generation

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
 - email: `admin@medtagger.com`,
 - password: `medtagger1`.

### Dockerized environment

MedTagger can be set up easily with Docker-Compose:

```bash
$ docker-compose up
```

More about setting up environment with Docker Compose can be found [here](/docs/setup_with_docker_compose.md).

## User Interface

Below screenshots show how MedTagger looks like:

#### Login Page
![Login Page](/docs/assets/login_page.png)

#### Main Page
![Main Page](/docs/assets/main_page.png)

#### Navigation Sidebar
![Navigation Sidebar](/docs/assets/navigation_sidebar.png)

#### Categories Page
![Categories Page](/docs/assets/categories_page.png)

#### Labeling Page
![Labeling Page](/docs/assets/labelling_page.png)

#### Upload Page
![Upload Page](docs/assets/upload_page.png)
