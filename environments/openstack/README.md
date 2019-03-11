# Deployment on OpenStack

In this tutorial you will learn how to set up MedTagger on OpenStack
using Terraform and Ansible. 

### Creating main.tf file

As you can see from the `.example.main.tf` there are several variables that are 
used in this deployment. To be able to deploy MedTagger onto your Openstack instance,
you would have to:

1. Rename the file to `main.tf`,
2. Fill it with your own variables.

### Creating custom configuration

MedTagger instance can be configurable depending on you needs regarding
the tasks, tags and tools. Head to the `.example.medtagger.yml` to see
the configuration. Make any changes that are needed and then rename the file
to `.medtagger.yml`.  


### Generating SSH keys

Proceed to your OpenStack Instance and go to **Computations - Access and Security - Key pairs** tab.

Click on **Create Key Pair** button and create 2 sets of key pairs.

**Important**: By default our configurations scripts assume that the keys are named `app-key`
and `db-key`. If you want to use different names, please change them in `main.tf` and 
`group_vars/all.yml` files.

The download of the private keys should start automatically after creating them. If not,
download private keys manually and place then in **environments/openstack/ansible** directory.

Remember to change file mode:

```bash
$ chmod 0600 db-key.pem
```

### Machines provisioning

After this step you will have:
- 2 (Ubuntu 18) instances (AppHost and DbHost) available on OpenStack,
- AppHost will have externally available IP address,
- Network connectivity between your App and Db host,
- 4 volumes set up (App Host, DB Host, PostgreSQL and Storage),
- Security Groups enabling certain ports for different services.

To start with the provisioning we firstly need to download 
the [`Openstack RC file`](https://docs.openstack.org/zh_CN/user-guide/common/cli-set-environment-variables-using-openstack-rc.html) 
from your Openstack instance. To do so proceed to the **Computations - Access and Security - API access** tab and
click on **Download OpenStack RC File v3**.

This file hold all needed variables needed for successful authorization
to the Openstack during provisioning.

To apply those variables source the file (you will be prompted for password
to your OpenStack instance):
```bash
$ source meddtager-project.sh
```

Now you are all set and you can start provisioning, to do so simply run:

```bash
$ make deploy
```

**Tip:** You can use `terraform plan` to see what changes would be done, 
without actually applying them.

### Ansible deployment

**Note**: It is assumed that:
- you have already completed the Terraform part of this deployment.
If not, you will have to create the `inventory` and `backend.env` files manually. 
Head to terraform folder and look at the `inventory.tpl` and `backend.env.tpl` files to 
learn how does their look like,
- the 2 private keys are placed in the `environments/openstack/ansible` folder,
- .medtagger.yml is placed in the `environments/openstack/ansible` folder.

After this step you will have running MedTagger with the chosen configuration (as 
defined by .medtagger.yaml) on the Docker Swarm.

Before we run this script head to the `group_vars/all.yml` file to 
make sure that the variables are set properly!

To install all dependencies and start the docker containers run (from the `environments/openstack/ansible` directory): 
```bash
$ ansible-playbook site.yml -i inventory
```

**Tip**: You will be prompted to accept the ssh key. You can disable it by 
adding `ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook ...`

### Configuration for Docker Swarm

Since we are setting up MedTagger using Docker Swarm, there were few changes that were needed
in our default docker-compose.yml.

1. Placement of the services.

    As you can see in the file, all of the services now how their placement
    directly specified with the following configuration:
    
    ```    
    deploy:
          placement:
            constraints:
              - node.hostname == apphost
    ```

2. Set new restart policy for database_migrations.

    Docker Swarm wants to make sure that all services replicas are set to 1,
    since we did not set any restart policy for database_migrations, docker swarm
    tried to restart the service over and over again. Since this is not needed and 
    database migration should run only once we need to change policy.
    ```
    image: medtagger_backend/database_migrations
    deploy:
      placement:
        constraints:
          - node.hostname == apphost
      restart_policy:
        condition: on-failure
    ```
 