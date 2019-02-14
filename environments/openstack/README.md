# Deployment on Openstack

### Preparing ssh keys

Proceed to Openstack Instance - Computations - Security - Create new key-pair
remember to name it as the same as in main.tf

Download the private keys, place them in Ansible dir.

### Machines provisioning

In this setup we will create two separate virtual machines on Openstack:
- Application host,
- Database host.

To do se we firstly need download 
the [`Openstack RC file`](https://docs.openstack.org/zh_CN/user-guide/common/cli-set-environment-variables-using-openstack-rc.html) 
from your Openstack instance. Follow the first step from the instruction to learn 
how to download this file and how to use it.

This file hold all needed variables needed for successful authorization
to the Openstack during provisioning.

Source the file (if you haven't already):
```bash
$ source meddtager-project.sh
```

Then run:
```bash
$ make deploy
```

**Tip:** You can use `terraform plan` to see what changes would be done, 
without actually allying them.

### Ansible deployment

In this setup we have three separate roles:
- **Common**: Installing Docker, docker-compose and all needed dependencies,
- **App**: Setting up application host services with docker-compose,
- **Db**: Setting up database host services with docker-compose.

**Important note**: To be able to run the ansible you first need to run the terraform
provisioning to generate an **inventory** file. 
Otherwise you would need to create inventory manually. Head to terraform folder
and look at the `inventory.tpl` file to learn how does the structure
looks like.

This step have 1 manual

To install all dependencies and start the docker containers simply run: 
```bash
$ ansible-playbook site.yml -i inventory
```