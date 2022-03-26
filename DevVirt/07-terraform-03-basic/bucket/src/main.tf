provider "yandex" {
  #NOTE:
  #Only one of token or service_account_key_file must be specified.
  #
  service_account_key_file = var.service_account_key_file
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = var.zone
}

data "yandex_compute_image" "centos" {
  family = "centos-8"
}

resource "yandex_vpc_network" "vpcnet" {
  name = "vpcnet"
}

resource "yandex_vpc_subnet" "vpcsubnet" {
  name           = "vpcsubnet"
  network_id     = resource.yandex_vpc_network.vpcnet.id
  v4_cidr_blocks = ["10.2.0.0/24"]
  zone           = "ru-central1-a"
}

resource "yandex_compute_instance" "vm" {
  name        = "netology-c8"
  hostname    = "netology_c8.local"
  platform_id = "standard-v1"

  resources {
    cores         = 2
    memory        = 2
    core_fraction = 100
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.centos.id
      type     = "network-hdd"
      size     = "20"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.vpcsubnet.id
    nat       = true
    ipv6      = false
  }

  metadata = {
    ssh-keys = "centos:${file("~/.ssh/id_rsa.pub")}"
  }
}