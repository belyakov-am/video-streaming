resource "yandex_vpc_network" "network" {
  name      = "tf-network"
  folder_id = var.folder_id
}

# ------------------------------------------------------------------------------

resource "yandex_vpc_subnet" "subnet" {
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["192.168.0.0/16"]
  zone           = var.zone
  route_table_id = yandex_vpc_route_table.nat.id
}

resource "yandex_vpc_subnet" "nat-public-subnet" {
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.100.0.0/24"]
  zone           = var.zone
}

# ------------------------------------------------------------------------------

resource "yandex_vpc_route_table" "nat" {
  network_id = yandex_vpc_network.network.id

  static_route {
    destination_prefix = "0.0.0.0/0"
    next_hop_address   = yandex_compute_instance.nat.network_interface.0.ip_address
  }
}
