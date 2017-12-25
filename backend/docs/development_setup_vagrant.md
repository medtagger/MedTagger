Running backend in Vagrant
--------------------------

### Requirements 

Please follow the documentation about setting up Vagrant [here](/docs/development_setup_vagrant.md).

### How to run backend?

Open two SSH connections (in separate windows) to your virtual machine and make sure that you're inside `/vagrant/backend`
directory. In the first one we'll run Celery workers which are responsible for adding and converting Dicoms to our
HBase. To run it, please execute such command:

```bash
$ make run_workers
```

In the second window we'll open our Flask REST API with WebSockets server. To do so, please execute:

```bash
$ make run_api
```

And that's all! Everything should be fine and Swagger for our REST API should be available on
`http://10.0.0.99:51000/api/v1`. 
