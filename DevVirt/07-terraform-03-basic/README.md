# Домашнее задание к занятию "7.3. Основы и принцип работы Терраформ"

## Задача 1. Создадим бэкэнд в S3 (необязательно, но крайне желательно).

Если в рамках предыдущего задания у вас уже есть аккаунт AWS, то давайте продолжим знакомство со взаимодействием
терраформа и aws. 

1. Создайте s3 бакет, iam роль и пользователя от которого будет работать терраформ. Можно создать отдельного пользователя,
а можно использовать созданного в рамках предыдущего задания, просто добавьте ему необходимы права, как описано 
[здесь](https://www.terraform.io/docs/backends/types/s3.html).
1. Зарегистрируйте бэкэнд в терраформ проекте как описано по ссылке выше. 

Ввиду имеющихся текущих ограничений на aws, работы проводились на yandex.cloud.

```bash

iva@c9:~/Documents/YC $ yc iam access-key create --service-account-name neto-robot
access_key:
  id: ajee50ng7jcav6p2c6oq
  service_account_id: ajegb4hm7vmc8mtflcdq
  created_at: "2022-03-25T23:39:13.295548648Z"
  key_id: YCAJE********************
secret: YCOX5m-V59h*****************************

Узнайте идентификатор сервисного аккаунта по его имени:

iva@c9:~/Documents/YC $ yc iam service-account get neto-robot
id: ajegb4hm7vmc8mtflcdq
folder_id: b1gm6im3mcuc36r6kn8s
created_at: "2022-03-25T22:28:10Z"
name: neto-robot
description: Service account for Netology

или

iva@c9:~/Documents/YC $ yc iam service-account list
+----------------------+------------+
|          ID          |    NAME    |
+----------------------+------------+
| ajegb4hm7vmc8mtflcdq | neto-robot |
+----------------------+------------+

Назначьте роль сервисному аккаунту neto-robot, используя его идентификатор:

yc resource-manager folder add-access-binding netology \
    --role editor \
    --subject serviceAccount:ajegb4hm7vmc8mtflcdq

export AWS_ACCESS_KEY_ID='YCAJE********************'
export AWS_SECRET_ACCESS_KEY='YCOX5m-V59h*****************************'

iva@c9:~/Documents/tf $ terraform init

Initializing the backend...

Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Finding latest version of terraform-registry.storage.yandexcloud.net/yandex-cloud/yandex...
- Installing terraform-registry.storage.yandexcloud.net/yandex-cloud/yandex v0.72.0...
- Installed terraform-registry.storage.yandexcloud.net/yandex-cloud/yandex v0.72.0 (self-signed, key ID E40F590B50BB8E40)

Partner and community providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://www.terraform.io/docs/cli/plugins/signing.html

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

iva@c9:~/Documents/tf $ terraform workspace list
* default

iva@c9:~/Documents/tf $ terraform workspace new stage
Created and switched to workspace "stage"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.

iva@c9:~/Documents/tf $ terraform workspace new prod
Created and switched to workspace "prod"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.

iva@c9:~/Documents/tf $ terraform workspace select prod

iva@c9:~/Documents/tf $ terraform workspace list
  default
* prod
  stage

```

После инициализации s3 и создания workspace - в Object storage создается переменная с соответсвующими путями neto-ingvar78/env:stage и neto-ingvar78/env:prod. В зависимости от текущего workspace данные state сохранятся в одноимённой директории 

[Промежуточный результат Terraform с бакетом](./bucket/src/)

## Задача 2. Инициализируем проект и создаем воркспейсы. 

1. Выполните `terraform init`:
    * если был создан бэкэнд в S3, то терраформ создат файл стейтов в S3 и запись в таблице 
dynamodb.
    * иначе будет создан локальный файл со стейтами.  
1. Создайте два воркспейса `stage` и `prod`.
1. В уже созданный `aws_instance` добавьте зависимость типа инстанса от вокспейса, что бы в разных ворскспейсах 
использовались разные `instance_type`.
1. Добавим `count`. Для `stage` должен создаться один экземпляр `ec2`, а для `prod` два. 
1. Создайте рядом еще один `aws_instance`, но теперь определите их количество при помощи `for_each`, а не `count`.
1. Что бы при изменении типа инстанса не возникло ситуации, когда не будет ни одного инстанса добавьте параметр
жизненного цикла `create_before_destroy = true` в один из рессурсов `aws_instance`.
1. При желании поэкспериментируйте с другими параметрами и рессурсами.

В виде результата работы пришлите:
* Вывод команды `terraform workspace list`.

```bash
iva@c9:~/Documents/tf $ terraform workspace list
  default
* prod
  stage

```

* Вывод команды `terraform plan` для воркспейса `prod`.  

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
