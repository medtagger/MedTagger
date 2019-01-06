provider "openstack" {}

## Network ##
resource "openstack_networking_network_v2" "network" {
  name           = "medtagger_net"
  admin_state_up = true
}

resource "openstack_networking_subnet_v2" "subnet" {
  name       = "medtagger_subnet"
  network_id = "${openstack_networking_network_v2.network.id}"
  cidr       = "192.168.0.0/24"
  ip_version = 4
}

resource "openstack_networking_router_v2" "router" {
  name                = "medtagger_router"
  external_network_id = "a8f3db7d-cd3f-4941-94d3-2aaffd0a9175"
  admin_state_up      = true
}

resource "openstack_networking_router_interface_v2" "router_interface" {
  router_id = "${openstack_networking_router_v2.router.id}"
  subnet_id = "${openstack_networking_subnet_v2.subnet.id}"
}

resource "openstack_networking_floatingip_v2" "floatip_1" {
  pool = "ext-net"
}

## Security groups ##

resource "openstack_networking_secgroup_v2" "ssh_secgroup" {
  name        = "SSH"
  description = "Allow SSH traffic to MedTagger hosts"
}

resource "openstack_networking_secgroup_rule_v2" "ssh_rule" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.ssh_secgroup.id}"
}

resource "openstack_networking_secgroup_v2" "ui_secgroup" {
  name        = "UI"
  description = "Allow access to MedTagger UI"
}

resource "openstack_networking_secgroup_rule_v2" "ui_rule" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 80
  port_range_max    = 80
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.ui_secgroup.id}"
}

resource "openstack_networking_secgroup_v2" "cassandra_secgroup" {
  name        = "CASSANDRA"
  description = "Allow access for Cassandra"
}

resource "openstack_networking_secgroup_rule_v2" "cassandra_rule" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 9042
  port_range_max    = 9042
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.cassandra_secgroup.id}"
}

## Key pairs ##

resource "openstack_compute_keypair_v2" "medtagger_keypair_app" {
  name = "app-key"
}

resource "openstack_compute_keypair_v2" "medtagger_keypair_db" {
  name = "db-key"
}

## Volumes ##
resource "openstack_blockstorage_volume_v2" "app_volume" {
  name = "App"
  size = 10
}

resource "openstack_blockstorage_volume_v2" "db_volume" {
  name = "Db"
  size = 10
}

resource "openstack_blockstorage_volume_v2" "cass_volume" {
  name = "Cassandra"
  size = 50
}

resource "openstack_blockstorage_volume_v2" "psql_volume" {
  name = "PostreSQL"
  size = 10
}

## Instances ##

## App host ##
resource "openstack_compute_instance_v2" "app" {
  name      = "AppHost"
  image_id  = "23e4701c-dbfb-49a1-bc83-96c4f30d91a6"
  flavor_id = "474e27b9-36aa-4e4e-989a-e3cc3e17d413"
  key_pair  = "${openstack_compute_keypair_v2.medtagger_keypair_app.name}"

  security_groups = [
    "default",
    "${openstack_networking_secgroup_v2.ssh_secgroup.name}",
    "${openstack_networking_secgroup_v2.ui_secgroup.name}",
  ]

  network {
    uuid = "${openstack_networking_network_v2.network.id}"
  }
}

resource "openstack_compute_floatingip_associate_v2" "fip_1" {
  floating_ip = "${openstack_networking_floatingip_v2.floatip_1.address}"
  instance_id = "${openstack_compute_instance_v2.app.id}"
}

resource "openstack_compute_volume_attach_v2" "app_volume_attach" {
  instance_id = "${openstack_compute_instance_v2.app.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.app_volume.id}"
}

## Db Host ##
resource "openstack_compute_instance_v2" "db" {
  name      = "DbHost"
  image_id  = "23e4701c-dbfb-49a1-bc83-96c4f30d91a6"
  flavor_id = "474e27b9-36aa-4e4e-989a-e3cc3e17d413"
  key_pair  = "${openstack_compute_keypair_v2.medtagger_keypair_db.name}"

  security_groups = [
    "default",
    "${openstack_networking_secgroup_v2.ssh_secgroup.name}",
    "${openstack_networking_secgroup_v2.cassandra_secgroup.name}",
  ]

  network {
    uuid = "${openstack_networking_network_v2.network.id}"
  }
}

resource "openstack_compute_volume_attach_v2" "db_volume_attach" {
  instance_id = "${openstack_compute_instance_v2.db.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.db_volume.id}"
}

resource "openstack_compute_volume_attach_v2" "cass_volume_attach" {
  instance_id = "${openstack_compute_instance_v2.db.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.cass_volume.id}"
}

resource "openstack_compute_volume_attach_v2" "psql_volume_attach" {
  instance_id = "${openstack_compute_instance_v2.db.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.psql_volume.id}"
}
