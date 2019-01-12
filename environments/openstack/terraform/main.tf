provider "openstack" {
  version = "~> 1.13"
}

variable image_id {
  default = "23e4701c-dbfb-49a1-bc83-96c4f30d91a6"
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

variable app_key_path {
  default = "../ansible/app.key"
}

variable db_key_path {
  default = "../ansible/db.key"
}
