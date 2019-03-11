provider "openstack" {
  version = "~> 1.13"
}

variable image_id {
  default = "bfb95819-9d93-47bf-ba97-5a60968fbdc0"
}

variable flavor_id {
  default = "474e27b9-36aa-4e4e-989a-e3cc3e17d413"
}

variable default_network {
  default = "ext-net"
}

variable dns_list {
  type = "list"
  default = ["8.8.8.8"]
}

variable ext_network_id {
    default = "a8f3db7d-cd3f-4941-94d3-2aaffd0a9175"
}

variable user {
  default = "ubuntu"
}

variable app_key_name {
  default = "app-key-dev"
}

variable db_key_name {
  default = "db-key-dev"
}
