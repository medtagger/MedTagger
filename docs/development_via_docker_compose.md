Development with Docker Compose
-------------------------------

Docker Compose is great to set up all depended services. It can setup things like Hadoop, HBase and RabbitMQ just
 with one command! But... it's not a good idea to develop the project inside of it. Instead, consider using Vagrant
 or setup the project natively.

### Requirements
 - [Docker Engine](https://www.docker.com),
 - [Docker Compose](https://docs.docker.com/compose/).
 
**Watch out:** It's highly possible that Docker Compose was included as part of a Docker Engine (on macOS/Windows)!
 More information can be found [here](https://docs.docker.com/compose/install/#prerequisites).

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

