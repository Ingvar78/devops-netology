# devops-netology 

# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). 
    В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, 
    где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно 
    простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

    * поместите его в автозагрузку,
    * предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
    * удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.

История настройки:

Создаем пользователя для node_exporter. Загружаем последнюю версию из репозитория, распаковываем. Создаем новый юнит, добавляем в него ссылку на внешний файл с настройками.

```
vagrant@u8:~$ history 
    1  sudo useradd node_exporter -s /sbin/nologin
    2  wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz
    3  tar xvfz node_exporter-1.2.2.linux-amd64.tar.gz
    4  cd node_exporter-1.2.2.linux-amd64
    5  sudo cp node_exporter /usr/sbin/
    6  sudo touch /etc/systemd/system/node_exporter.service
    7  sudo vi /etc/systemd/system/node_exporter.service
    8  cat /etc/systemd/system/node_exporter.service

[Unit]
Description=Prometheus exporter for hardware and OS.
After=network.target

[Service]
Type=simple
EnvironmentFile=/etc/sysconfig/node_exporter # внешний файл с настройками.
ExecStart=/usr/sbin/node_exporter $NEX_OPTS
KillMode=process
KillSignal=SIGINT
Restart=always
RestartSec=10
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

    Создаем файл с настройками, отключаем значения по умолчанию и добавляем необходимые.

```
    9  sudo mkdir -p /etc/sysconfig
   10  sudo touch /etc/sysconfig/node_exporter
   11  sudo vi /etc/sysconfig/node_exporter
   12  sudo cat /etc/sysconfig/node_exporter


NEX_OPTS="--collector.disable-defaults --collector.zoneinfo --collector.cpu --collector.processes  --collector.netdev --collector.netstat --collector.loadavg --collector.meminfo"

```

    Запускаем, проверяем работу.


```
   13  sudo systemctl daemon-reload
   14  sudo systemctl enable node_exporter

Created symlink /etc/systemd/system/multi-user.target.wants/node_exporter.service → /etc/systemd/system/node_exporter.service.

   15  sudo systemctl start node_exporter
   16  sudo systemctl status node_exporter


● node_exporter.service - Prometheus exporter for hardware and OS.
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2021-10-30 19:03:49 UTC; 5s ago
   Main PID: 12969 (node_exporter)
      Tasks: 6 (limit: 3484)
     Memory: 2.3M
     CGroup: /system.slice/node_exporter.service
             └─12969 /usr/sbin/node_exporter --collector.disable-defaults --collector.zoneinfo --collector.cpu --collector.processes --collector.netdev --collector.loadavg --collector.meminfo

   17  curl http://localhost:9100/metrics 

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0node_scrape_collector_duration_seconds{collector="zoneinfo"} 0.000370783
node_scrape_collector_success{collector="zoneinfo"} 1


   18  sudo shutdown -r now
   19  curl http://localhost:9100/metrics
   20  sudo systemctl status node_exporter

● node_exporter.service - Prometheus exporter for hardware and OS.
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2021-10-30 19:07:02 UTC; 4min 57s ago
   Main PID: 674 (node_exporter)
      Tasks: 6 (limit: 3484)
     Memory: 16.7M
     CGroup: /system.slice/node_exporter.service
             └─674 /usr/sbin/node_exporter --collector.disable-defaults --collector.zoneinfo --collector.cpu --collector.processes --collector.netdev --collector.loadavg --collector.meminfo

   21  history 

```

2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового 
    мониторинга хоста по CPU, памяти, диску и сети.

    Доступные опции можно посмотреть вызвав с параметром --help

```
vagrant@u8:~$ node_exporter --help

```

    Базовые:
    --collector.disable-defaults используется для выключения, поскольку все метрики по-умолчанию включены
    --collector.cpu - мониторинг cpu
    --collector.meminfo - памяти
    --collector.filesystem - файловой системы
    --collector.netstat  - сетевого трафика
    и/или
    --collector.netdev - сетевых интерфейсов


3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). 
    Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:

    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,

```
vagrant@u8:~$ cat /etc/netdata/netdata.conf
# NetData Configuration

# The current full configuration can be retrieved from the running
# server at the URL
#
#   http://localhost:19999/netdata.conf
#
# for example:
#
#   wget -O /etc/netdata/netdata.conf http://localhost:19999/netdata.conf
#

[global]
    run as user = netdata
    web files owner = root
    web files group = root
    # Netdata is not designed to be exposed to potentially hostile
    # networks. See https://github.com/netdata/netdata/issues/164
    #bind socket to IP = 127.0.0.1
    bind to = 0.0.0.0
```

    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

    config.vm.network "forwarded_port", guest: 19999, host: 19999


```
iva@c8:~/Vagrant $ cat Vagrantfile 
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.hostname = 'u8.local'
  config.vm.network "forwarded_port", guest: 19999, host: 19999
  config.vm.provider :virtualbox do |v|
    v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    v.memory = 1024 * 3
    v.cpus = 2 * 2
  end
end
```

    После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. 
    Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.

    ![Screenshot](./IMG/netdata.png)


4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. 
    Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?

6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; 
    покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). 
    Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.

7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 
    (**это важно, поведение в других ОС не проверялось**). 
    Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. 
    Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. 
    Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

