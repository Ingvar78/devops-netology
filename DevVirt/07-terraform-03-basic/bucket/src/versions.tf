terraform {
  required_providers {
    yandex = {
      source = "terraform-registry.storage.yandexcloud.net/yandex-cloud/yandex"
    }
  }

  backend "s3" {
    endpoint = "storage.yandexcloud.net"
    bucket   = "neto-ingvar78"
    region   = "us-east-1"
    key      = "terraform.tfstate"

    #access_key = ""
    #secret_key = ""
    #AWS_ACCESS_KEY_ID: Идентификатор ключа доступа
    #AWS_SECRET_ACCESS_KEY: Секретный ключ доступа

    skip_region_validation      = true
    skip_credentials_validation = true
  }

  required_version = ">= 1.1"
}
