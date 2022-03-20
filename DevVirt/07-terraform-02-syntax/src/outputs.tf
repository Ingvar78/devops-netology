output "yandex_zone" {
  value       = yandex_compute_instance.vm.zone
  description = "Регион Яндекса, в котором создан инстанс"
}

output "yandex_ip_private" {
  value       = yandex_compute_instance.vm.network_interface.0.ip_address
  description = "Приватный IP на Яндексе"
}

output "yandex_ip_nat" {
  value       = yandex_compute_instance.vm.network_interface.0.nat_ip_address
  description = "Публичный IP адрес"
}

output "yandex_vpc_subnet" {
  value       = resource.yandex_vpc_subnet.vpcsubnet.id
  description = "Идентификатор подсети в которой создан инстанс"
}

