Docker Compose for dependencies
-------------------------------

Docker Compose is great to set up all depended services. It can setup things like Hadoop, HBase and RabbitMQ just
with one command!

### Requirements
 - [Docker Engine](https://www.docker.com),
 - [Docker Compose](https://docs.docker.com/compose/).
 
**Watch out:** It's highly possible that Docker Compose was included as part of a Docker Engine (on Mac/Windows)!
More information can be found [here](https://docs.docker.com/compose/install/#prerequisites).

### How to use it?

It's really easy to start all needed external dependencies:

```bash
$ docker-compose up
```

_**TIP!**_ Add `-d` (detach) option to run everything in the background.

You can also specify which dependency should be run alone by:

```bash
$ docker up rabbitmq
```

For more information about usage please read the [documentation](https://docs.docker.com/compose/).
