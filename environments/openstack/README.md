# Provisioning with Openstack

## How to run it ?

Download [`Openstack RC file`](https://docs.openstack.org/zh_CN/user-guide/common/cli-set-environment-variables-using-openstack-rc.html) from your Openstack instance. It holds all needed environmental variables.

Source the file:
```bash
$ source meddtager-project.sh
```

Finally:
```bash
$ make deploy
```

**Tip:** You can use `terraform plan` to see what changes would be done, without actually apllying them.
