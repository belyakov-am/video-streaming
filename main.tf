variable "token" {
}

variable "cloud_id" {
}

variable "folder_id" {
}

variable "zone" {
}

provider "yandex" {
  token     = var.token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

terraform {
    required_providers {
        yandex = {
            source = "yandex-cloud/yandex"
        }
    }
}

resource "yandex_compute_instance" "app" {
  name = "app"

  resources {
    cores  = 2
    memory = 1
    core_fraction = 5
    gpus = 0  
  }

  boot_disk {
    initialize_params {
      image_id = "fd8vmcue7aajpmeo39kk"
      type     = "network-hdd"
      size     = "13"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "yandex_vpc_network" "network-1" {
  name = "network1"
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = "new-network"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

output "in_ip_app" {
  value = yandex_compute_instance.app.network_interface.0.ip_address
}

output "ex_ip_app" {
  value = yandex_compute_instance.app.network_interface.0.nat_ip_address
}
