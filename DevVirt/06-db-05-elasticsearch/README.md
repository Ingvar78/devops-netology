# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста

```bash
iva@c8:~/Documents/ES $ cat Dockerfile
ARG OS_VERSION=7
ARG ES_VERSION=8.0.1

FROM centos:$OS_VERSION

ENV ES_VER=8.0.1
ENV ES_HOME=/opt/elasticsearch-${ES_VER}
ENV ES_JAVA_HOME=/opt/elasticsearch-${ES_VER}/jdk
ENV ES_JAVA_OPTS="-Xms128m -Xmx128m"
ENV PATH=$PATH:/opt/elasticsearch-${ES_VER}/bin

RUN yum update -y --setopt=tsflags=nodocs && \
yum install -y perl-Digest-SHA && \
yum install -y wget && \
rm -rf /var/cache/yum && \
groupadd elastic && \
useradd elastic -g elastic -p elasticsearch && \
mkdir -p /var/lib/elasticsearch/logs && \
mkdir -p /var/lib/elasticsearch/snapshots && \
mkdir -p /var/lib/elasticsearch/data

WORKDIR /opt

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VER}-linux-x86_64.tar.gz && \
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VER}-linux-x86_64.tar.gz.sha512 && \
shasum -a 512 -c elasticsearch-${ES_VER}-linux-x86_64.tar.gz.sha512 && \
tar -xzf elasticsearch-${ES_VER}-linux-x86_64.tar.gz && \
rm elasticsearch-${ES_VER}-linux-x86_64.tar.gz && \
chown -R elastic:elastic ${ES_HOME} && chown -R elastic:elastic /var/lib/elasticsearch

ADD elasticsearch.yml ${ES_HOME}/config/elasticsearch.yml

EXPOSE 9200 9300

WORKDIR ${ES_HOME}

USER elastic

CMD ["elasticsearch"]
```

[DockerFile](./src/Dockerfile)

[elasticsearch.yml](./src/elasticsearch.yml)

- ссылку на образ в репозитории dockerhub

[egerpro/elasticsearch:8.0.1](https://hub.docker.com/repository/docker/egerpro/elasticsearch)

- ответ `elasticsearch` на запрос пути `/` в json виде

```bash
iva@c8:~/Documents/ES $ curl localhost:9200
{
  "name" : "netology_test",
  "cluster_name" : "netology_test_cluster",
  "cluster_uuid" : "hKQdGfh0SU6cCINEH6E4nA",
  "version" : {
    "number" : "8.0.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "801d9ccc7c2ee0f2cb121bbe22ab5af77a902372",
    "build_date" : "2022-02-24T13:55:40.601285296Z",
    "build_snapshot" : false,
    "lucene_version" : "9.0.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

при использовании ssl:
curl -X GET "https://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s&pretty" --key certificates/elasticsearch-ca.pem  -k -u elastic

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

```bash
iva@c8:~/Documents/ES/6.5+ $ curl -k -X GET 'http://localhost:9200/_cat/indices?v'
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   ind-1 UZ-IFhpOS5C9nl36Xfjkrw   1   0          0            0       225b           225b
yellow open   ind-3 JwlnrqswSbW_p_bq0kZy-g   4   2          0            0       900b           900b
yellow open   ind-2 QcbBo_t5RgSHzyLY5WXWJQ   2   1          0            0       450b           450b
```

Получите состояние кластера `elasticsearch`, используя API.

```bash
iva@c8:~/Documents/ES/6.5+ $ curl localhost:9200/_cluster/health | python3 -m json.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   411  100   411    0     0   200k      0 --:--:-- --:--:-- --:--:--  200k
{
    "cluster_name": "netology_test_cluster",
    "status": "yellow",
    "timed_out": false,
    "number_of_nodes": 1,
    "number_of_data_nodes": 1,
    "active_primary_shards": 8,
    "active_shards": 8,
    "relocating_shards": 0,
    "initializing_shards": 0,
    "unassigned_shards": 10,
    "delayed_unassigned_shards": 0,
    "number_of_pending_tasks": 0,
    "number_of_in_flight_fetch": 0,
    "task_max_waiting_in_queue_millis": 0,
    "active_shards_percent_as_number": 44.44444444444444
}
```

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Поскольку кластер состоит из одной ноды, шарды индексов ind-2 и ind-3 не реплицированы и находятся в статусе unssigned. После добавления дополнительных нод в кластер на которые они смогут реплицироваться статус их изменится на GREEN, кластер так же сменит статус после репликации.


Удалите все индексы.

```bash
iva@c8:~/Documents/ES/6.5+ $ curl -X DELETE "localhost:9200/ind-1?pretty"
{
  "acknowledged" : true
}
iva@c8:~/Documents/ES/6.5+ $ curl -X DELETE "localhost:9200/ind-2?pretty"
{
  "acknowledged" : true
}
iva@c8:~/Documents/ES/6.5+ $ curl -X DELETE "localhost:9200/ind-3?pretty"
{
  "acknowledged" : true
}
iva@c8:~/Documents/ES/6.5+ $ curl -X GET http://localhost:9200/_cluster/health | python3 -m json.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   397  100   397    0     0   129k      0 --:--:-- --:--:-- --:--:--  129k
{
    "cluster_name": "netology_test_cluster",
    "status": "green",
    "timed_out": false,
    "number_of_nodes": 1,
    "number_of_data_nodes": 1,
    "active_primary_shards": 1,
    "active_shards": 1,
    "relocating_shards": 0,
    "initializing_shards": 0,
    "unassigned_shards": 0,
    "delayed_unassigned_shards": 0,
    "number_of_pending_tasks": 0,
    "number_of_in_flight_fetch": 0,
    "task_max_waiting_in_queue_millis": 0,
    "active_shards_percent_as_number": 100.0
}

```

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.


Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

```bash
iva@c8:~/Documents/ES/6.5+ $ curl -X PUT "localhost:9200/_snapshot/netology_backup?verify=false&pretty" -H 'Content-Type: application/json' -d'
> {
>   "type": "fs",
>   "settings": {
>     "location": "/var/lib/elasticsearch/snapshots"
>   }
> }
> '
{
  "acknowledged" : true
}
```

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

```bash
iva@c8:~/Documents/ES/6.5+ $ curl -k -X GET 'http://localhost:9200/_cat/indices?v'
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  OVHYrxi4QTus4WG9ZLPU1w   1   0          0            0       225b           225b
```

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

```bash
sh-4.2$ ls -la /var/lib/elasticsearch/snapshots/
total 32
drwxr-xr-x. 1 elastic elastic   134 Mar  5 20:56 .
drwxr-xr-x. 1 elastic elastic    47 Mar  5 17:57 ..
-rw-r--r--. 1 elastic elastic   843 Mar  5 20:56 index-0
-rw-r--r--. 1 elastic elastic     8 Mar  5 20:56 index.latest
drwxr-xr-x. 4 elastic elastic    66 Mar  5 20:56 indices
-rw-r--r--. 1 elastic elastic 17426 Mar  5 20:56 meta-04NT9A1qTQCGekpctIlgnw.dat
-rw-r--r--. 1 elastic elastic   355 Mar  5 20:56 snap-04NT9A1qTQCGekpctIlgnw.dat
```

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

```bash
iva@c8:~/Documents/ES/6.5+ $ curl -X PUT "localhost:9200/test-2?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "index": {
>       "number_of_replicas": 0,
>       "number_of_shards": 1
>     }
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}
iva@c8:~/Documents/ES/6.5+ $ curl -k -X GET 'http://localhost:9200/_cat/indices?v'
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 sqI9cnNfQ4afI38lYZx16w   1   0          0            0       225b           225b

```
[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

```bash
iva@c8:~/Documents/ES/6.5+ $ curl -X GET "http://localhost:9200/_snapshot/netology_backup/*?verbose=false&pretty"
{
  "snapshots" : [
    {
      "snapshot" : "three_snap",
      "uuid" : "04NT9A1qTQCGekpctIlgnw",
      "repository" : "netology_backup",
      "indices" : [
        ".geoip_databases",
        "test"
      ],
      "data_streams" : [ ],
      "state" : "SUCCESS"
    }
  ],
  "total" : 1,
  "remaining" : 0
}
iva@c8:~/Documents/ES/6.5+ $ curl -X POST http://localhost:9200/_snapshot/netology_backup/three_snap/_restore
{"accepted":true}
iva@c8:~/Documents/ES/6.5+ $ curl -k -X GET 'http://localhost:9200/_cat/indices?v'
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 sqI9cnNfQ4afI38lYZx16w   1   0          0            0       225b           225b
green  open   test   m5K-KOOSRZOWRhO7frhD7Q   1   0          0            0       225b           225b
```


Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

---

после изменения пути повторно пересозданы индексы и snapshot, 

iva@c8:~/Documents/ES/6.5+ $ docker exec -it busy_noether sh -c 'pwd && ls -la snapshots'
/opt/elasticsearch-8.0.1
total 32
drwxr-xr-x. 1 elastic elastic   134 Mar  5 21:59 .
drwxr-xr-x. 1 elastic elastic    49 Mar  5 21:48 ..
-rw-r--r--. 1 elastic elastic   843 Mar  5 21:59 index-0
-rw-r--r--. 1 elastic elastic     8 Mar  5 21:59 index.latest
drwxr-xr-x. 4 elastic elastic    66 Mar  5 21:59 indices
-rw-r--r--. 1 elastic elastic 17443 Mar  5 21:59 meta-9egGqFM4RZaBg8IWiO89mg.dat
-rw-r--r--. 1 elastic elastic   355 Mar  5 21:59 snap-9egGqFM4RZaBg8IWiO89mg.dat

iva@c8:~/Documents/ES/6.5+ $ curl -X GET "http://localhost:9200/_snapshot/netology_backup/*?verbose=false&pretty"
{
  "snapshots" : [
    {
      "snapshot" : "three_snap",
      "uuid" : "9egGqFM4RZaBg8IWiO89mg",
      "repository" : "netology_backup",
      "indices" : [
        ".geoip_databases",
        "test"
      ],
      "data_streams" : [ ],
      "state" : "SUCCESS"
    }
  ],
  "total" : 1,
  "remaining" : 0
}

iva@c8:~/Documents/ES/6.5+ $  curl -X POST http://localhost:9200/_snapshot/netology_backup/three_snap/_restore
{"accepted":true}
iva@c8:~/Documents/ES/6.5+ $ curl -k -X GET 'http://localhost:9200/_cat/indices?v'
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 B__JK2ejT3WXxS2l9pEkrg   1   0          0            0       225b           225b
green  open   test   V_9UzZYASz-3nayL2FZ78w   1   0          0            0       225b           225b

---

