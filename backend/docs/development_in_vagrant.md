Running MedTagger Backend in Vagrant
------------------------------------

Here you can find more information about running MedTagger Backend in Vagrant.

### Requirements 

Please follow the documentation about setting up Vagrant [here](/docs/development_setup_vagrant.md).

### How to run backend?

Open two SSH connections (in separate windows) to your virtual machine and make sure that you're inside `/vagrant/backend`
 directory. Then run command below to prepare your development environment:
 
 ```bash
 $ . devenv.sh
```
 
 In the first window we'll run Celery workers which are responsible for handling difficult tasks (eg. adding and
 converting Dicoms to our HBase DB). To run Celery workers, please execute such command:

```bash
$ make run_workers
```

In the second window we'll open our REST & WebSockets API server. To do so, please execute:

```bash
$ make run_api
```

And that's all! Everything should be fine and Swagger for our REST API should be available on
 `http://10.0.0.99:51000/api/v1`. 
