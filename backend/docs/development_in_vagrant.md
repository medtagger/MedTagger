Running MedTagger Backend in Vagrant
------------------------------------

Here you can find more information about running MedTagger Backend in Vagrant.

### Requirements 

Please follow the documentation about setting up Vagrant [here](/docs/development_setup_vagrant.md).

### How to run backend?

Open three SSH connections (in separate windows) to your virtual machine using `vagrant ssh` and make sure that you're
 inside `/vagrant/backend` directory. Then run below commands in three separate windows.
 
In the first window we'll run Celery workers which are responsible for handling difficult tasks (eg. adding and
 converting DICOMs to our Storage). To run Celery workers, please execute such command:

```bash
$ . devenv.sh
$ make run_workers
```

In the second window we'll open our REST API server. To do so, please execute:

```bash
$ . devenv.sh
$ make run_rest
```

In the third window we'll open our WebSocket API server:

```bash
$ . devenv.sh
$ make run_websocket
```

And that's all! Everything should be fine and Swagger for our REST API should be available on
 `http://10.0.0.99:51000/api/v1`. 
