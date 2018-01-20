MedTagger Architecture
----------------------

MedTagger's architecture was designed to be as much scalable as possible. It means
 that each of the system's component should allow to increase its performance easily.

## Diagram

![MedTagger Architecture](/docs/assets/architecture.png)

## Components

Above diagram consists of several components. Each of them has its own responsibilities:

 - **GUI** - Graphics User Interface written in TypeScript. It's using Angular 4, SCSS and many
   other frontend technologies, libraries and tools. It works on user's web browser. This
   project is stored in `/frontend` directory.

 - **Application** - main backend application written in Python 3.6+. It's using Flask as a
   framework for REST API and many extentions that enable WebSocket support, easy
   input validation and output marshaling. It also use SQLAlchemy as SQL ORM engine and
   Alembic for SQL database management. It contains clients for HBase data manipulation
   that uses HappyBase as a framework. It's part of a project in `/backend` directory.

 - **Celery Workers** - part of a backend application for long running and performance
   impacting tasks. It uses RabbitMQ as a broker that passes tasks for running. Workers
   may be running on multiple other nodes. Tasks are defined in the `/backend/workers`
   directory.

 - **RabbitMQ** - message broker used for communication between main application instance
   and Celery Workers' nodes.

 - **HBase** - NoSQL database storage used for aggregation of all Scans and its Slices. It
   stores data using high-scalable tables and key-value access.

 - **PostgreSQL** - SQL database that stores all of our business models and metadata related
   to medical data.

