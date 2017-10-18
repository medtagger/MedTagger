Development setup with Vagrant
------------------------------

Vagrant is the easiest way to prepare your dev environment. It will automatically create a VirtualBox virtual machine,
 which will have all of our dependencies inside of it.

### Requirements 

Here is a list of things that you've got to install:
- [VirtualBox](https://www.virtualbox.org),
- [Vagrant](https://www.vagrantup.com).

### How to do this?

Once you've install your VirtualBox with Vagrant, it's time to clone this repository.

```bash
$ git clone git@gitlab.com:praca-inzynierska/Backend-API.git
```

Then you will be able to open it inside PyCharm and use Vagrant plugin to boot up your machine. To do this
you can choose `Tools > Vagrant > Up` or use CLI and run `vagrant up`.   

**Important:** It may take a while, because Vagrant needs to download box with Ubuntu image and then install
all dependencies like Python and Docker with all needed containers.

Once your machine is now running, it's time to create a configuration file. Please create a new empty file and name it
`backend_api.conf`. Base on an example file (`backend_api.example.conf`) and fill your configuration with all needed
entries.

**_Tip!_** Running API inside of a Virtual Machine should be hosted on 0.0.0.0!

Your project is now ready to be run but your HBase database is still empty. Before you start your journey with backend,
please connect with your VM over SSH (use `vagrant ssh` command). Then go to `/vagrant` directory and launch script
that will create all tables in HBase.

```bash
$ python3.6 migrate_hbase.py
```

It will ask you a few questions and answer them with `y` or `yes` to create all needed entries.

**_Tip!_** This script may be useful one day to create new tables or delete a new one. Please check documentation
inside of this script for more information.

Now, your backend is ready to be used, so let's try to run it!

Open two SSH connections (in separate windows) to our virtual machine and make sure that you're inside `/vagrant`
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
