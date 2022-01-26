
# Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами"

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов

Паттерны — это способ построения (структуризации) программного кода специальным образом. На практике они используются программистами для того, чтобы решить какую-нибудь проблему, устранить определенную «боль» разработчика. 
В этом случае предполагается, что существует некоторый перечень общих формализованных проблем (а это так и есть), причем данные проблемы встречаются относительно часто. 
И вот здесь-то на сцену и выходят паттерны, которые как раз таки и предоставляют способы решения этих проблем.

Преимущество применения паттернов IaaС на практике это возможность единожды описав инфраструктуру многократно её воспроизводить, производить развёртывние идентичных сервера/сред для тестирования/разработки, масштабирование при необходимости. 
Следующим преимуществом является автоматизация рутинных действий что приводит к снижению трудозатрат на их выполнение - как следствие повышается скорость разработки, выявления и устранения дефектов за счёт более раннего их обнаружения и тестирования на этапе сборки.
Автоматизация поставки - позволяет сократить время от этапа разработки до внедрения.
Паттерны IaaC позволяют стандартизировать развёртывание инфраструктуры, что снижает вероятность появления ошибок или отклонений связанных с человеческим фактором.

Применение на практике IaaC паттернов позволяет ускорить процесс разработки, снизить трудозатраты на поиск и устранение дефектов, организовать непрерывную поставку продукта

- Какой из принципов IaaC является основополагающим?

Идемпотентность операций - свойство сценария/операции позволяющее многократно получать/воспроизводить одно и то же состояние объекта (среды) что и при первом применении, т.е. не зависимо от того сколько раз будет проигран сценарий, результат всегда будет идентичен результату полученному в первый раз.


## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?

Не требует установки агентов на клиентах, использует SSH или WinRM соединение.
Низкий порог входа, поддержка декларативного и императивного подхода, описание конфигурации - «плейбуки» вформате YAML
Поддерживает широкий набор модулей позволяющих управлять конфигурацией как ОС, так и различным ПО и сетевым оборудованием.
Ansible Galaxy - публичный репозиторий, в котором размещается огромное количество готовых ролей Ansible.

- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

На мой взгляд более надёжный push - позволяет определить когда, кдуа и какую конфигурацию отправить, так же позволяет проконтролировать результат применения.

## Задача 3

Установить на личный компьютер:

- VirtualBox

```bash
iva@c8:~/Documents/netology/devops-netology/DevVirt/05-virt-02-iaac  (05-virt-02-iaac *)$ virtualbox --help
Oracle VM VirtualBox VM Selector v6.1.32
(C) 2005-2022 Oracle Corporation
All rights reserved.

No special options.

If you are looking for --startvm and related options, you need to use VirtualBoxVM.
```

- Vagrant

```bash
iva@c8:~/Documents/netology/devops-netology/DevVirt/05-virt-02-iaac  (05-virt-02-iaac *)$ vagrant --version
Vagrant 2.2.19

```

- Ansible

```bash
iva@c8:~/Documents/netology/devops-netology/DevVirt/05-virt-02-iaac  (05-virt-02-iaac *)$ ansible --version
[DEPRECATION WARNING]: Ansible will require Python 3.8 or newer on the controller starting with Ansible 2.12. Current version: 3.6.8 (default, Sep 10 2021, 09:13:53) [GCC 8.5.0 20210514 (Red Hat 8.5.0-3)]. This feature will be removed from ansible-core in version 2.12. Deprecation
 warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ansible [core 2.11.7] 
  config file = None
  configured module search path = ['/home/iva/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/iva/.local/lib/python3.6/site-packages/ansible
  ansible collection location = /home/iva/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/iva/.local/bin/ansible
  python version = 3.6.8 (default, Sep 10 2021, 09:13:53) [GCC 8.5.0 20210514 (Red Hat 8.5.0-3)]
  jinja version = 3.0.3
  libyaml = True
```

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

- Создать виртуальную машину.

```bash
iva@c8:~/Documents/netology/devops-netology/DevVirt/05-virt-02-iaac/src/vagrant  (05-virt-02-iaac *)$ vagrant up
Bringing machine 'server1.netology' up with 'virtualbox' provider...
==> server1.netology: Checking if box 'bento/ubuntu-20.04' version '202107.28.0' is up to date...
==> server1.netology: Clearing any previously set network interfaces...
==> server1.netology: Found default DHCP server from initial VirtualBox install. Cleaning it up...
==> server1.netology: Preparing network interfaces based on configuration...
    server1.netology: Adapter 1: nat
    server1.netology: Adapter 2: hostonly
==> server1.netology: Forwarding ports...
    server1.netology: 22 (guest) => 20011 (host) (adapter 1)
    server1.netology: 22 (guest) => 2222 (host) (adapter 1)
==> server1.netology: Running 'pre-boot' VM customizations...
==> server1.netology: Booting VM...
==> server1.netology: Waiting for machine to boot. This may take a few minutes...
    server1.netology: SSH address: 127.0.0.1:2222
    server1.netology: SSH username: vagrant
    server1.netology: SSH auth method: private key
    server1.netology: Warning: Connection reset. Retrying...
    server1.netology: Warning: Remote connection disconnect. Retrying...
    server1.netology: Warning: Remote connection disconnect. Retrying...
    server1.netology: Warning: Connection reset. Retrying...
    server1.netology: 
    server1.netology: Vagrant insecure key detected. Vagrant will automatically replace
    server1.netology: this with a newly generated keypair for better security.
    server1.netology: 
    server1.netology: Inserting generated public key within guest...
    server1.netology: Removing insecure key from the guest if it's present...
    server1.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
==> server1.netology: Machine booted and ready!
==> server1.netology: Checking for guest additions in VM...
==> server1.netology: Setting hostname...
==> server1.netology: Configuring and enabling network interfaces...
==> server1.netology: Mounting shared folders...
    server1.netology: /vagrant => /home/iva/Documents/netology/devops-netology/DevVirt/05-virt-02-iaac/src/vagrant
==> server1.netology: Running provisioner: ansible...
    server1.netology: Running ansible-playbook...

PLAY [nodes] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *******************************************
changed: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] ****************************
changed: [server1.netology]

TASK [Checking DNS] ************************************************************
changed: [server1.netology]

TASK [Installing tools] ********************************************************
ok: [server1.netology] => (item=git)
ok: [server1.netology] => (item=curl)

TASK [Installing docker] *******************************************************
changed: [server1.netology]

TASK [Add the current user to docker group] ************************************
changed: [server1.netology]

PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

- Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды

```bash
iva@c8:~/Documents/netology/devops-netology/DevVirt/05-virt-02-iaac/src/vagrant  (05-virt-02-iaac *)$ vagrant ssh
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue 25 Jan 2022 11:52:32 PM UTC

  System load:  0.15              Users logged in:          0
  Usage of /:   3.2% of 61.31GB   IPv4 address for docker0: 172.17.0.1
  Memory usage: 20%               IPv4 address for eth0:    10.0.2.15
  Swap usage:   0%                IPv4 address for eth1:    192.168.56.3
  Processes:    107


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Tue Jan 25 23:50:07 2022 from 10.0.2.2
```
для развёртывания VM потребовалось изменить способ назначения IP адреса на dhcp

```
docker ps
```

```bash
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
vagrant@server1:~$ groups 
vagrant adm cdrom sudo dip plugdev lxd lpadmin sambashare docker
vagrant@server1:~$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete 
Digest: sha256:975f4b14f326b05db86e16de00144f9c12257553bba9484fed41f9b6f2257800
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```
