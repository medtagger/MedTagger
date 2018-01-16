Setup with Docker Compose
-------------------------

Docker Compose is great to set up all environment with one command. It is also great
 for setting up all depended services. Docker Compose can setup things like Hadoop,
 HBase and RabbitMQ easily!

**But...** it's not a good idea to develop the project inside of it. Changes in the
 code will require rebuilding whole Docker images. Instead, consider using Vagrant
 or setup the project natively on Linux/macOS.

### Requirements

 - [Docker CE](https://www.docker.com/community-edition),
 - [Docker Compose](https://docs.docker.com/compose/install/).

_**TIP!**_ Check your host machine with these commands:

```bash
$ docker --version
Docker version 17.09.1-ce, build 19e2cf6
$ docker-compose --version
docker-compose version 1.17.1, build 6d101fb
```

### How to setup whole MedTagger?

To run whole MedTagger using Docker Compose, you can just execute `up` command like this:

```bash
$ docker-compose up
```

### How to setup dependencies?

It's really easy to start all needed external dependencies:

```bash
$ docker-compose up hbase postgres rabbitmq
```

_**TIP!**_ Add `-d` (detach) option to run everything in the background!

For more information about usage please read the [documentation](https://docs.docker.com/compose/).

