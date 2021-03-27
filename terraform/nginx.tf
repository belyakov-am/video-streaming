resource "yandex_compute_instance" "service-nginx" {
  name = "service-nginx"
  hostname = "service-nginx"
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
    nat = true
  }

  metadata = {
    docker-container-declaration = file("${path.module}/declarations/nginx.yaml")
    ssh-keys = "artem:${file("~/.ssh/id_rsa.pub")}"
  }
}
