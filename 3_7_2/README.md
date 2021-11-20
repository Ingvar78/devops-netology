# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?

В Linux доступны следующие команды: ifconfig, ip, в Windows это ipconfig. ниже список доступных интервейсов eno1 - физическая сетевая карта, lo - интерфейс обратной петли (local loopback) - позволяет компьютеру обращатся к самому себе, 
virb0 - интерфейс виртулальной сетевой карты (бридж) - для взаимодействия с виртуальными хостами.

```bash
iva@c8:~/Documents/netology/devops-netology/3_7_2  (3.7.2)$ ifconfig 
eno1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.17  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::5246:5dff:fe6f:2f14  prefixlen 64  scopeid 0x20<link>
        ether 50:46:5d:6f:2f:14  txqueuelen 1000  (Ethernet)
        RX packets 113558  bytes 96443768 (91.9 MiB)
        RX errors 0  dropped 106  overruns 0  frame 0
        TX packets 51649  bytes 17276961 (16.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 20  memory 0xf7100000-f7120000  

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 98  bytes 6114 (5.9 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 98  bytes 6114 (5.9 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

virbr0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
        ether 52:54:00:dc:4e:6d  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?

LLDP
Link Layer Discovery Protocol (LLDP) — протокол канального уровня, позволяющий сетевому оборудованию оповещать оборудование, работающее в локальной сети, о своём существовании и передавать ему свои характеристики, а также получать от него аналогичные сведения. 

так же на равне с данным протоколом используются следующи:

для IPv4 - ARP (Address Resolution Protocol) - для определения IP по MAC-адресу, IRDP (Internet Router Discovery Protocol или ICMP Router Discovery Protocol) или RDISC (от англ. Router Discovery — обнаружение маршрутизаторов) — протокол для компьютерных хостов для обнаружения присутствия и расположения маршрутизаторов в их локальной сети IPv4.

для IPv6 - NDP (Neighbor Discovery Protocol (NDP, ND)) - протокол обнаружения соседей 


3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.

4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.

6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?



 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

 8*. Установите эмулятор EVE-ng.
 
 Инструкция по установке - https://github.com/svmyasnikov/eve-ng

 Выполните задания на lldp, vlan, bonding в эмуляторе EVE-ng. 
 
 ---

