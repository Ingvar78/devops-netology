Создание сети

$ yc vpc network create \
--name net \
--labels my-label=netology \
--description "network for netology"

$ yc vpc network list
+----------------------+------+
|          ID          | NAME |
+----------------------+------+
| enp9knlmbqf7k3q180io | net  |
+----------------------+------+

$ yc vpc subnet create \
--name subnet-n \
--zone ru-central1-a \
--range 10.1.2.0/24 \
--network-name net \
--description "subnet for netology"

+----------------------+----------+----------------------+----------------+---------------+---------------+
|          ID          |   NAME   |      NETWORK ID      | ROUTE TABLE ID |     ZONE      |     RANGE     |
+----------------------+----------+----------------------+----------------+---------------+---------------+
| e9b950s9e720269srcg3 | subnet-n | enp9knlmbqf7k3q180io |                | ru-central1-a | [10.1.2.0/24] |
+----------------------+----------+----------------------+----------------+---------------+---------------+

Правим 
cd packer
centos-7-base.json 

$ yc config list
token: AQAEA7*********************************
cloud-id: b1gos10ashr7cgusvgg9
folder-id: b1ggj86e8kjsmu987amu
compute-default-zone: ru-central1-a

$ yc vpc subnets list | grep -E 'ID|subnet-n'
|          ID          |   NAME   |      NETWORK ID      | ROUTE TABLE ID |     ZONE      |     RANGE     |
| e9b950s9e720269srcg3 | subnet-n | enp9knlmbqf7k3q180io |                | ru-central1-a | [10.1.2.0/24] |


$ grep -E 'folder_id|subnet_id|token' centos-7-base.json
      "folder_id": "b1gg****************",
      "subnet_id": "e9b9****************",
      "token": "AQAEA7*********************************",

$ packer validate centos-7-base.json


$ packer build centos-7-base.json
yandex: output will be in this color.

==> yandex: Creating temporary RSA SSH key for instance...
==> yandex: Using as source image: fd8gdnd09d0iqdu7ll2a (name: "centos-7-v20220207", family: "centos-7")
==> yandex: Use provided subnet id e9b950s9e720269srcg3
==> yandex: Creating disk...
==> yandex: Creating instance...
.....
==> yandex: Creating image: centos-7-base
==> yandex: Waiting for image to complete...
==> yandex: Success image create...
==> yandex: Destroying boot disk...
    yandex: Disk has been deleted!
Build 'yandex' finished after 3 minutes 11 seconds.

==> Wait completed after 3 minutes 11 seconds

==> Builds finished. The artifacts of successful builds are:
--> yandex: A disk image was created: centos-7-base (id: fd8pj96cusik2f6mjbet) with family name centos

$ yc compute image list
+----------------------+---------------+--------+----------------------+--------+
|          ID          |     NAME      | FAMILY |     PRODUCT IDS      | STATUS |
+----------------------+---------------+--------+----------------------+--------+
| fd8pj96cusik2f6mjbet | centos-7-base | centos | f2e40ohi7d1hori8m71b | READY  |
+----------------------+---------------+--------+----------------------+--------+

Удаляем ранее созданные подсети после сборки образа
$ yc vpc subnets delete --name subnet-n && yc vpc network delete --name net

# создаём сервисный аккаунт, предоставляем роль editor

$ yc iam service-account create --name deployer-sa --description "service account for netology"
id: ajef2o19q2h1q0mbvopa
folder_id: b1ggj86e8kjsmu987amu
created_at: "2022-02-09T22:04:56.949247043Z"
name: deployer-sa
description: service account for netology


$ yc iam service-account list
+----------------------+-------------+
|          ID          |    NAME     |
+----------------------+-------------+
| ajef2o19q2h1q0mbvopa | deployer-sa |
+----------------------+-------------+

yc resource-manager folder add-access-binding netology \
    --role editor \
    --subject serviceAccount:ajef2o19q2h1q0mbvopa


перехоим в terraform и правим `provider.tf`

$ cd ../terraform

создадим файл секретов сервисного аккаунта

$ yc iam key create --service-account-name deployer-sa --output key.json
id: ajehrrrsh6mj485tcgnk
service_account_id: ajef2o19q2h1q0mbvopa
created_at: "2022-02-09T22:15:35.150560934Z"
key_algorithm: RSA_2048

далее правим variables.tf
данные для заполнения - облака и каталога берём из вывода
$ yc config list
образа 
$ yc compute image list

$ yc config list
token: AQAEA7*********************************
cloud-id: b1gos10ashr7cgusvgg9
folder-id: b1ggj86e8kjsmu987amu
compute-default-zone: ru-central1-a
$ yc compute image list
+----------------------+---------------+--------+----------------------+--------+
|          ID          |     NAME      | FAMILY |     PRODUCT IDS      | STATUS |
+----------------------+---------------+--------+----------------------+--------+
| fd8pj96cusik2f6mjbet | centos-7-base | centos | f2e40ohi7d1hori8m71b | READY  |
+----------------------+---------------+--------+----------------------+--------+


Инициализация конфигурации

$ terraform init
....
Terraform has been successfully initialized!
...
$ terraform validate
Success! The configuration is valid.

$ terraform plan
...

Plan: 13 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + external_ip_address_node01 = (known after apply)
  + external_ip_address_node02 = (known after apply)
  + external_ip_address_node03 = (known after apply)
  + external_ip_address_node04 = (known after apply)
  + external_ip_address_node05 = (known after apply)
  + external_ip_address_node06 = (known after apply)
  + internal_ip_address_node01 = "192.168.101.11"
  + internal_ip_address_node02 = "192.168.101.12"
  + internal_ip_address_node03 = "192.168.101.13"
  + internal_ip_address_node04 = "192.168.101.14"
  + internal_ip_address_node05 = "192.168.101.15"
  + internal_ip_address_node06 = "192.168.101.16"
...

Применяем план
$ terraform apply -auto-approve

null_resource.monitoring (local-exec): PLAY RECAP *********************************************************************
null_resource.monitoring (local-exec): node01.netology.yc         : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
null_resource.monitoring (local-exec): node02.netology.yc         : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
null_resource.monitoring (local-exec): node03.netology.yc         : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

null_resource.monitoring: Creation complete after 45s [id=8008179333453857403]

Apply complete! Resources: 13 added, 0 changed, 0 destroyed.

Outputs:

external_ip_address_node01 = "51.250.2.51"
external_ip_address_node02 = "51.250.5.235"
external_ip_address_node03 = "51.250.0.52"
external_ip_address_node04 = "51.250.15.76"
external_ip_address_node05 = "51.250.6.11"
external_ip_address_node06 = "51.250.15.246"
internal_ip_address_node01 = "192.168.101.11"
internal_ip_address_node02 = "192.168.101.12"
internal_ip_address_node03 = "192.168.101.13"
internal_ip_address_node04 = "192.168.101.14"
internal_ip_address_node05 = "192.168.101.15"
internal_ip_address_node06 = "192.168.101.16"



Проверка статуса нод в кластере:
```bash
iva@c8:~/Documents/netology/5.5/terraform $ ssh centos@51.250.2.51
[centos@node01 ~]$ sudo -i
[root@node01 ~]# docker node ls
ID                            HOSTNAME             STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
70onbixmxu8n6y4o4als66ieo *   node01.netology.yc   Ready     Active         Leader           20.10.12
njd8w1x9ywuqzpd9e3fyej32x     node02.netology.yc   Ready     Active         Reachable        20.10.12
gr0jet9q7exsdppv6arcmm0ga     node03.netology.yc   Ready     Active         Reachable        20.10.12
xfq5ri61qakxuw7wvcf3w6ndy     node04.netology.yc   Ready     Active                          20.10.12
y439ja0d8odji2slpdiqjhxh2     node05.netology.yc   Ready     Active                          20.10.12
8lorrvchrg9wexu0s6nqk017z     node06.netology.yc   Ready     Active                          20.10.12
root@node01 ~]# sudo docker stack ls
NAME               SERVICES   ORCHESTRATOR
swarm_monitoring   8          Swarm
```

```bash
root@node03 ~]# docker node ls
ID                            HOSTNAME             STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
70onbixmxu8n6y4o4als66ieo     node01.netology.yc   Down      Active         Unreachable      20.10.12
njd8w1x9ywuqzpd9e3fyej32x     node02.netology.yc   Ready     Active         Reachable        20.10.12
gr0jet9q7exsdppv6arcmm0ga *   node03.netology.yc   Ready     Active         Leader           20.10.12
xfq5ri61qakxuw7wvcf3w6ndy     node04.netology.yc   Ready     Active                          20.10.12
y439ja0d8odji2slpdiqjhxh2     node05.netology.yc   Ready     Active                          20.10.12
8lorrvchrg9wexu0s6nqk017z     node06.netology.yc   Ready     Active                          20.10.12
[root@node03 ~]# docker node ls
ID                            HOSTNAME             STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
70onbixmxu8n6y4o4als66ieo     node01.netology.yc   Ready     Active         Reachable        20.10.12
njd8w1x9ywuqzpd9e3fyej32x     node02.netology.yc   Ready     Active         Reachable        20.10.12
gr0jet9q7exsdppv6arcmm0ga *   node03.netology.yc   Ready     Active         Leader           20.10.12
xfq5ri61qakxuw7wvcf3w6ndy     node04.netology.yc   Ready     Active                          20.10.12
y439ja0d8odji2slpdiqjhxh2     node05.netology.yc   Ready     Active                          20.10.12
8lorrvchrg9wexu0s6nqk017z     node06.netology.yc   Ready     Active                          20.10.12
```

```bash
[root@node01 ~]# sudo docker stack ps swarm_monitoring
ID             NAME                                                              IMAGE                                          NODE                 DESIRED STATE   CURRENT STATE            ERROR     PORTS
kpq8fgri7n13   swarm_monitoring_alertmanager.1                                   stefanprodan/swarmprom-alertmanager:v0.14.0    node03.netology.yc   Running         Running 9 minutes ago              
romftc9gz3b2   swarm_monitoring_caddy.1                                          stefanprodan/caddy:latest                      node01.netology.yc   Running         Running 8 minutes ago              
vrz9rhrc0cm9    \_ swarm_monitoring_caddy.1                                      stefanprodan/caddy:latest                      node02.netology.yc   Shutdown        Complete 8 minutes ago             
eh5iqqhqzt3b    \_ swarm_monitoring_caddy.1                                      stefanprodan/caddy:latest                      node01.netology.yc   Shutdown        Shutdown 9 minutes ago             
rzhue67nqoo0   swarm_monitoring_cadvisor.8lorrvchrg9wexu0s6nqk017z               google/cadvisor:latest                         node06.netology.yc   Running         Running 9 minutes ago              
t77ihzkgf4th   swarm_monitoring_cadvisor.70onbixmxu8n6y4o4als66ieo               google/cadvisor:latest                         node01.netology.yc   Running         Running 8 minutes ago              
vcod2qpn6qqy    \_ swarm_monitoring_cadvisor.70onbixmxu8n6y4o4als66ieo           google/cadvisor:latest                         node01.netology.yc   Shutdown        Shutdown 9 minutes ago             
0qqam0s9xxy2   swarm_monitoring_cadvisor.gr0jet9q7exsdppv6arcmm0ga               google/cadvisor:latest                         node03.netology.yc   Running         Running 9 minutes ago              
my9johi63ka4   swarm_monitoring_cadvisor.njd8w1x9ywuqzpd9e3fyej32x               google/cadvisor:latest                         node02.netology.yc   Running         Running 9 minutes ago              
6w75hn540vzu   swarm_monitoring_cadvisor.xfq5ri61qakxuw7wvcf3w6ndy               google/cadvisor:latest                         node04.netology.yc   Running         Running 9 minutes ago              
rvpwbdp5j088   swarm_monitoring_cadvisor.y439ja0d8odji2slpdiqjhxh2               google/cadvisor:latest                         node05.netology.yc   Running         Running 9 minutes ago              
3yegk9yxuazv   swarm_monitoring_dockerd-exporter.8lorrvchrg9wexu0s6nqk017z       stefanprodan/caddy:latest                      node06.netology.yc   Running         Running 9 minutes ago              
snct7jimcx0a   swarm_monitoring_dockerd-exporter.70onbixmxu8n6y4o4als66ieo       stefanprodan/caddy:latest                      node01.netology.yc   Running         Running 8 minutes ago              
ysoajdv3xvch    \_ swarm_monitoring_dockerd-exporter.70onbixmxu8n6y4o4als66ieo   stefanprodan/caddy:latest                      node01.netology.yc   Shutdown        Shutdown 9 minutes ago             
tm4n5waajza0   swarm_monitoring_dockerd-exporter.gr0jet9q7exsdppv6arcmm0ga       stefanprodan/caddy:latest                      node03.netology.yc   Running         Running 9 minutes ago              
1bqejc2fi9cx   swarm_monitoring_dockerd-exporter.njd8w1x9ywuqzpd9e3fyej32x       stefanprodan/caddy:latest                      node02.netology.yc   Running         Running 9 minutes ago              
vrnpsyfxxxhw   swarm_monitoring_dockerd-exporter.xfq5ri61qakxuw7wvcf3w6ndy       stefanprodan/caddy:latest                      node04.netology.yc   Running         Running 9 minutes ago              
jnsviczup0en   swarm_monitoring_dockerd-exporter.y439ja0d8odji2slpdiqjhxh2       stefanprodan/caddy:latest                      node05.netology.yc   Running         Running 9 minutes ago              
4147al54gk0h   swarm_monitoring_grafana.1                                        stefanprodan/swarmprom-grafana:5.3.4           node03.netology.yc   Running         Running 8 minutes ago              
glkds7wdz7wi    \_ swarm_monitoring_grafana.1                                    stefanprodan/swarmprom-grafana:5.3.4           node01.netology.yc   Shutdown        Shutdown 9 minutes ago             
w1nbr09pmxel   swarm_monitoring_node-exporter.8lorrvchrg9wexu0s6nqk017z          stefanprodan/swarmprom-node-exporter:v0.16.0   node06.netology.yc   Running         Running 9 minutes ago              
jnf9ul4521i5   swarm_monitoring_node-exporter.70onbixmxu8n6y4o4als66ieo          stefanprodan/swarmprom-node-exporter:v0.16.0   node01.netology.yc   Running         Running 8 minutes ago              
l10moilmxcnu    \_ swarm_monitoring_node-exporter.70onbixmxu8n6y4o4als66ieo      stefanprodan/swarmprom-node-exporter:v0.16.0   node01.netology.yc   Shutdown        Shutdown 9 minutes ago             
dqnl1yabp3n6   swarm_monitoring_node-exporter.gr0jet9q7exsdppv6arcmm0ga          stefanprodan/swarmprom-node-exporter:v0.16.0   node03.netology.yc   Running         Running 9 minutes ago              
u6a3021fxg0o   swarm_monitoring_node-exporter.njd8w1x9ywuqzpd9e3fyej32x          stefanprodan/swarmprom-node-exporter:v0.16.0   node02.netology.yc   Running         Running 9 minutes ago              
ql58e7t96ss9   swarm_monitoring_node-exporter.xfq5ri61qakxuw7wvcf3w6ndy          stefanprodan/swarmprom-node-exporter:v0.16.0   node04.netology.yc   Running         Running 9 minutes ago              
v6qqrvvxzn9p   swarm_monitoring_node-exporter.y439ja0d8odji2slpdiqjhxh2          stefanprodan/swarmprom-node-exporter:v0.16.0   node05.netology.yc   Running         Running 9 minutes ago              
mx70xe4jj2pa   swarm_monitoring_prometheus.1                                     stefanprodan/swarmprom-prometheus:v2.5.0       node02.netology.yc   Running         Running 9 minutes ago              
g7d8uo85gsy6   swarm_monitoring_unsee.1                                          cloudflare/unsee:v0.8.0                        node04.netology.yc   Running         Running 9 minutes ago 
```


```bash
[root@node01 ~]# docker swarm update --autolock=true
Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-WGSRRm8BPuB5x7n+XGeOU5SpISItgS3DYnIiK+aHCSQ

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

```bash
$ terraform destroy

$ yc compute image delete --id 'fd8pj96cusik2f6mjbet'
