############## VARIABLES ##############

variable "token" {}
variable "folder_id" {}
variable "cloud_id" {}
variable "zone" {
  default = "ru-central1-a"
}

############## PROVIDER ##############

terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
      version = "0.49.0"
    }
  }
}

provider "yandex" {
  token = var.token
  cloud_id = var.cloud_id
  folder_id = var.folder_id
  zone = var.zone
}

############## ACCOUNT ##############

resource "yandex_iam_service_account" "sa" {
  name = "hw"
}

resource "yandex_resourcemanager_folder_iam_binding" "b" {
  folder_id = var.folder_id
  role = "container-registry.images.puller"
  members = [
    "serviceAccount:${yandex_iam_service_account.sa.id}",
  ]
}

############## IMAGE ##############

data "yandex_compute_image" "container-optimized-image" {
  family = "container-optimized-image"
}

data "yandex_compute_image" "nat-instance" {
  family = "nat-instance-ubuntu"
}
