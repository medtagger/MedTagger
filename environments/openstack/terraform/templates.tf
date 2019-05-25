## Inventory ##

data "template_file" "inventory" {
  template = "${file("inventory.tpl")}"

  vars {
    app_host_ip = "${openstack_networking_floatingip_v2.floatip_1.address}"
    db_host_ip = "${openstack_compute_instance_v2.db.access_ip_v4}"
    app_key_name = "${var.app_key_name}.pem"
    db_key_name = "${var.db_key_name}.pem"
    default_user = "${var.user}"
  }
}

resource "null_resource" "update_inventory" {

  triggers {
    template = "${data.template_file.inventory.rendered}"
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.inventory.rendered}' > ../ansible/inventory"
  }
}

## Backend.env ##

data "template_file" "env" {
  template = "${file("backend.env.tpl")}"

  vars {
    db_host_ip = "${openstack_compute_instance_v2.db.access_ip_v4}"
  }
}

resource "null_resource" "update_env_file" {

  triggers {
    template = "${data.template_file.env.rendered}"
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.env.rendered}' > ../backend.env"
  }
}