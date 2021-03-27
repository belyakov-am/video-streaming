output "service-internal-ip" {
  value = yandex_compute_instance.service.network_interface[0].ip_address
}

resource "yandex_compute_instance" "service" {
  name = "service"
  hostname = "service"
  platform_id = "standard-v2"
  folder_id = var.folder_id

  resources {
    cores = 2
    memory = 1
    core_fraction = 5
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.container-optimized-image.id
      size = 13
      type = "network-hdd"
    }
  }

  scheduling_policy {
    preemptible = true
  }

  service_account_id = yandex_iam_service_account.sa.id

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat = false
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}
