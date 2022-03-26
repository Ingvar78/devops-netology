variable "cloud_id" {
  description = "Cloud"
}
variable "folder_id" {
  description = "Folder"
}
variable "zone" {
  description = "Zone"
  # Значение по умолчанию
  default = "ru-central1-a"
}
variable "public_key_path" {
  # Описание переменной
  description = "Path to the public key used for ssh access"
}
variable "service_account_key_file" {
  description = "key .json"
}
variable "private_key_path" {
  description = "Path to Private Key File"
}
variable "vCores_count" {
  description = "vCores count"
  default     = 2
}
variable "memory_size" {
  description = "Memory RAM in GB"
  default     = 2
}
variable "sa_id" {
  description = "SERVICE ACCOUNT ID"
}
