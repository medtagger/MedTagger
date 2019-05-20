## Network ##

resource "openstack_networking_network_v2" "network" {
  name = "medtagger_net"
  admin_state_up = true
}

resource "openstack_networking_subnet_v2" "subnet" {
  name = "medtagger_subnet"
  network_id = "${openstack_networking_network_v2.network.id}"
  cidr = "192.168.0.0/24"
  dns_nameservers = "${var.dns_list}"
}

resource "openstack_networking_router_v2" "router" {
  name = "medtagger_router"
  external_network_id = "${var.ext_network_id}"
  admin_state_up = true
}

resource "openstack_networking_router_interface_v2" "router_interface" {
  router_id = "${openstack_networking_router_v2.router.id}"
  subnet_id = "${openstack_networking_subnet_v2.subnet.id}"
}

resource "openstack_networking_floatingip_v2" "floatip_1" {
  pool = "${var.default_network}"
}

## Security groups ##

resource "openstack_networking_secgroup_v2" "app_sec_group" {
  name = "app"
  description = "Security group for app hosts for MedTagger"
}

resource "openstack_networking_secgroup_rule_v2" "ssh_app" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 22
  port_range_max = 22
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.app_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "ui" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 80
  port_range_max = 80
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.app_sec_group.id}"
}


resource "openstack_networking_secgroup_v2" "db_sec_group" {
  name = "db"
  description = "Security group for Db hosts for MedTagger"
}

resource "openstack_networking_secgroup_rule_v2" "ssh_db" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 22
  port_range_max = 22
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.db_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "cassandra_sec_group" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 9042
  port_range_max = 9042
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.db_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "postgres_sec_group" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 5432
  port_range_max = 5432
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.db_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "rabbit_sec_group_1" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 5672
  port_range_max = 5672
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.db_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "rabbit_sec_group_2" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 15672
  port_range_max = 15672
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.db_sec_group.id}"
}

resource "openstack_networking_secgroup_v2" "docker_swarm_sec_group" {
  name = "docker-swarm"
  description = "Security group for docker-swarm configuration for MedTagger"
}

resource "openstack_networking_secgroup_rule_v2" "docker_1" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 2377
  port_range_max = 2377
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.docker_swarm_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "docker_2" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "tcp"
  port_range_min = 7946
  port_range_max = 7946
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.docker_swarm_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "docker_3" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "udp"
  port_range_min = 7946
  port_range_max = 7946
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.docker_swarm_sec_group.id}"
}

resource "openstack_networking_secgroup_rule_v2" "docker_4" {
  direction = "ingress"
  ethertype = "IPv4"
  protocol = "udp"
  port_range_min = 4789
  port_range_max = 4789
  remote_ip_prefix = "0.0.0.0/0"
  security_group_id = "${openstack_networking_secgroup_v2.docker_swarm_sec_group.id}"
}
