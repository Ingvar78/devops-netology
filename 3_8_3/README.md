# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
```
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```

```bash
User Access Verification

Username: rviews
route-views>show ip route 95.31.137.0
Routing entry for 95.30.0.0/15
  Known via "bgp 6447", distance 20, metric 0
  Tag 6939, type external
  Last update from 64.71.137.241 1w2d ago
  Routing Descriptor Blocks:
  * 64.71.137.241, from 64.71.137.241, 1w2d ago
      Route metric is 0, traffic share count is 1
      AS Hops 3
      Route tag 6939
      MPLS label: none
route-views>show ip route 95.31.137.252
Routing entry for 95.30.0.0/15
  Known via "bgp 6447", distance 20, metric 0
  Tag 6939, type external
  Last update from 64.71.137.241 1w2d ago
  Routing Descriptor Blocks:
  * 64.71.137.241, from 64.71.137.241, 1w2d ago
      Route metric is 0, traffic share count is 1
      AS Hops 3
      Route tag 6939
      MPLS label: none
route-views>


-----

route-views>show bgp 95.31.137.252
BGP routing table entry for 95.30.0.0/15, version 1365037841
Paths: (24 available, best #20, table default)
  Not advertised to any peer
  Refresh Epoch 3
  3303 3216 8402
    217.192.89.50 from 217.192.89.50 (138.187.128.158)
      Origin IGP, localpref 100, valid, external
      Community: 3216:1000 3216:1004 3216:2001 3303:1004 3303:1006 3303:1030 3303:3051 8402:900 8402:904
      path 7FE03765C7B0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7660 2516 6762 8402 8402
    203.181.248.168 from 203.181.248.168 (203.181.248.168)
      Origin IGP, localpref 100, valid, external
      Community: 2516:1030 7660:9003
      path 7FE148521F28 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3267 3356 8402 8402
    194.85.40.15 from 194.85.40.15 (185.141.126.1)
      Origin IGP, metric 0, localpref 100, valid, external
      path 7FE1536E79F0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  57866 3356 8402 8402
    37.139.139.17 from 37.139.139.17 (37.139.139.17)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 3356:2 3356:22 3356:100 3356:123 3356:501 3356:903 3356:2065 8402:900 8402:904
      path 7FE0BF55B6F0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7018 3356 8402 8402
    12.0.1.63 from 12.0.1.63 (12.0.1.63)
      Origin IGP, localpref 100, valid, external
      Community: 7018:5000 7018:37232
      path 7FE0E86B8C30 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3333 6762 8402 8402
    193.0.0.56 from 193.0.0.56 (193.0.0.56)
      Origin IGP, localpref 100, valid, external
      Community: 6762:1 6762:92 6762:14900
      path 7FE1128A5728 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  49788 12552 3216 8402
    91.218.184.60 from 91.218.184.60 (91.218.184.60)
      Origin IGP, localpref 100, valid, external
      Community: 12552:12000 12552:12100 12552:12101 12552:22000
      Extended Community: 0x43:100:1
      path 7FE11564B7F8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  20912 3257 3356 8402 8402
    212.66.96.126 from 212.66.96.126 (212.66.96.126)
      Origin IGP, localpref 100, valid, external
      Community: 3257:8070 3257:30515 3257:50001 3257:53900 3257:53902 20912:65004
      path 7FE0A121C828 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  8283 6762 8402 8402
    94.142.247.3 from 94.142.247.3 (94.142.247.3)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 6762:1 6762:92 6762:14900 8283:1 8283:101
      unknown transitive attribute: flag 0xE0 type 0x20 length 0x18
        value 0000 205B 0000 0000 0000 0001 0000 205B
              0000 0005 0000 0001 
      path 7FE04FEE76D8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3356 8402 8402
    4.68.4.46 from 4.68.4.46 (4.69.184.201)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 3356:2 3356:22 3356:100 3356:123 3356:501 3356:903 3356:2065 8402:900 8402:904
      path 7FE03789E658 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1221 4637 6762 8402 8402
    203.62.252.83 from 203.62.252.83 (203.62.252.83)
      Origin IGP, localpref 100, valid, external
      path 7FE04772FD38 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  2497 3356 8402 8402
    202.232.0.2 from 202.232.0.2 (58.138.96.254)
      Origin IGP, localpref 100, valid, external
      path 7FE133D01460 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  852 3356 8402 8402
    154.11.12.212 from 154.11.12.212 (96.1.209.43)
      Origin IGP, metric 0, localpref 100, valid, external
      path 7FE004B733B8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  20130 6939 3216 8402
    140.192.8.16 from 140.192.8.16 (140.192.8.16)
      Origin IGP, localpref 100, valid, external
      path 7FE16D0E1688 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  701 1273 8402 8402 8402
    137.39.3.55 from 137.39.3.55 (137.39.3.55)
      Origin IGP, localpref 100, valid, external
      path 7FE0517C6728 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3257 3356 8402 8402
    89.149.178.10 from 89.149.178.10 (213.200.83.26)
      Origin IGP, metric 10, localpref 100, valid, external
      Community: 3257:8794 3257:30043 3257:50001 3257:54900 3257:54901
      path 7FE07E9E8CC0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3549 3356 8402 8402
    208.51.134.254 from 208.51.134.254 (67.16.168.191)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 3356:2 3356:22 3356:100 3356:123 3356:501 3356:903 3356:2065 3549:2581 3549:30840 8402:900 8402:904
      path 7FE126F8E418 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  53767 14315 6453 6453 3356 8402 8402
    162.251.163.2 from 162.251.163.2 (162.251.162.3)
      Origin IGP, localpref 100, valid, external
      Community: 14315:5000 53767:5000
      path 7FE147AD8A70 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  101 3356 8402 8402
    209.124.176.223 from 209.124.176.223 (209.124.176.223)
      Origin IGP, localpref 100, valid, external
      Community: 101:20100 101:20110 101:22100 3356:2 3356:22 3356:100 3356:123 3356:501 3356:903 3356:2065 8402:900 8402:904
      Extended Community: RT:101:22100
      path 7FE112242EC8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  6939 3216 8402
    64.71.137.241 from 64.71.137.241 (216.218.252.164)
      Origin IGP, localpref 100, valid, external, best
      path 7FE15F782548 RPKI State not found
      rx pathid: 0, tx pathid: 0x0
  Refresh Epoch 1
  3561 3910 3356 8402 8402
    206.24.210.80 from 206.24.210.80 (206.24.210.80)
      Origin IGP, localpref 100, valid, external
      path 7FE13F2039A0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  4901 6079 3356 8402 8402
    162.250.137.254 from 162.250.137.254 (162.250.137.254)
      Origin IGP, localpref 100, valid, external
      Community: 65000:10100 65000:10300 65000:10400
      path 7FE0C3BD08C0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1351 6939 3216 8402
    132.198.255.253 from 132.198.255.253 (132.198.255.253)
      Origin IGP, localpref 100, valid, external
      path 7FE0AF916A90 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  19214 3257 3356 8402 8402
    208.74.64.40 from 208.74.64.40 (208.74.64.40)
      Origin IGP, localpref 100, valid, external
      Community: 3257:8108 3257:30048 3257:50002 3257:51200 3257:51203
      path 7FE1435AB020 RPKI State not found
      rx pathid: 0, tx pathid: 0
route-views>  


```

2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.

```bash
vagrant@u8:~$ lsmod | grep dummy
vagrant@u8:~$ sudo modprobe dummy
vagrant@u8:~$ lsmod | grep dummy
dummy                  16384  0
vagrant@u8:~$ sudo ip link add dummy0 type dummy
vagrant@u8:~$ sudo ip a add 10.10.1.101/32 dev dummy0
vagrant@u8:~$ sudo ip l set dev dummy0 up
vagrant@u8:~$ ip -c -br addr show
lo               UNKNOWN        127.0.0.1/8 ::1/128 
eth0             UP             10.0.2.15/24 fe80::a00:27ff:fe73:60cf/64 
dummy0           UNKNOWN        10.10.1.101/32 fe80::4829:c6ff:fe9d:ffd3/64 
vagrant@u8:~$ ping 10.10.1.101 
PING 10.10.1.101 (10.10.1.101) 56(84) bytes of data.
64 bytes from 10.10.1.101: icmp_seq=1 ttl=64 time=0.018 ms
64 bytes from 10.10.1.101: icmp_seq=2 ttl=64 time=0.019 ms
64 bytes from 10.10.1.101: icmp_seq=3 ttl=64 time=0.014 ms

--- 10.10.1.101 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2050ms
rtt min/avg/max/mdev = 0.014/0.017/0.019/0.002 ms
vagrant@u8:~$ ip r
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
```

перезагружаемся...

```bash
agrant@u8:~$ ip r
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
vagrant@u8:~$ ip -c -br addr show
lo               UNKNOWN        127.0.0.1/8 ::1/128 
eth0             UP             10.0.2.15/24 fe80::a00:27ff:fe73:60cf/64 
vagrant@u8:~$ 
```

```bash
vagrant@u8:~$ sudo su
root@u8:/home/vagrant# echo "dummy" >> /etc/modules
root@u8:/home/vagrant# cat /etc/modules
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with "#" are ignored.

dummy
vagrant@u8:~$ ip -c -br addr show
lo               UNKNOWN        127.0.0.1/8 ::1/128 
eth0             UP             10.0.2.15/24 fe80::a00:27ff:fe73:60cf/64 
vagrant@u8:~$ sudo su
root@u8:/home/vagrant# lsmod | grep dummy
dummy                  16384  0
root@u8:/home/vagrant# vi /etc/network/interfaces
root@u8:/home/vagrant# vi /etc/network/interfaces
root@u8:/home/vagrant# cat /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d
auto dummy0
iface dummy0 inet static
    address 10.10.1.102/32
    pre-up ip link add dummy0 type dummy
    post-down ip link del dummy0
    post-up ip route add 172.16.100.0/24 dev dummy0 src 10.10.1.102
    post-up ip route add default via 172.16.100.1 dev dummy0
root@u8:/home/vagrant# reboot
Connection to 127.0.0.1 closed by remote host.
Connection to 127.0.0.1 closed.
iva@c8:~/Vagrant $ vagrant ssh
vagrant@u8:~$ ip r
default via 172.16.100.1 dev dummy0 
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
172.16.100.0/24 dev dummy0 scope link src 10.10.1.102 
vagrant@u8:~$ ip route list
default via 172.16.100.1 dev dummy0 
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
172.16.100.0/24 dev dummy0 scope link src 10.10.1.102 
```


3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.

```bash
vagrant@u8:~$ netstat -atlpn 
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 10.0.2.15:22            10.0.2.2:45898          ESTABLISHED -                   
tcp6       0      0 :::111                  :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
vagrant@u8:~$ nc -l 5555&
[1] 1255
vagrant@u8:~$ netstat -atlpn 
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:5555            0.0.0.0:*               LISTEN      1255/nc             
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 10.0.2.15:22            10.0.2.2:45898          ESTABLISHED -                   
tcp6       0      0 :::111                  :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
vagrant@u8:~$ ss -pta
State                          Recv-Q                         Send-Q                                                 Local Address:Port                                                   Peer Address:Port                         Process                                               
LISTEN                         0                              4096                                                         0.0.0.0:sunrpc                                                      0.0.0.0:*                                                                                  
LISTEN                         0                              1                                                            0.0.0.0:5555                                                        0.0.0.0:*                             users:(("nc",pid=1255,fd=3))                         
LISTEN                         0                              4096                                                   127.0.0.53%lo:domain                                                      0.0.0.0:*                                                                                  
LISTEN                         0                              128                                                          0.0.0.0:ssh                                                         0.0.0.0:*                                                                                  
ESTAB                          0                              0                                                          10.0.2.15:ssh                                                        10.0.2.2:45898                                                                              
LISTEN                         0                              4096                                                            [::]:sunrpc                                                         [::]:*                                                                                  
LISTEN                         0                              128                                                             [::]:ssh                                                            [::]:*       
```

```bash
vagrant@u8:~$ sudo su
root@u8:/home/vagrant# netstat -atlpn  
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      1/init              
tcp        0      0 0.0.0.0:5555            0.0.0.0:*               LISTEN      1255/nc             
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      609/systemd-resolve 
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      758/sshd: /usr/sbin 
tcp        0      0 10.0.2.15:22            10.0.2.2:45898          ESTABLISHED 847/sshd: vagrant [ 
tcp6       0      0 :::111                  :::*                    LISTEN      1/init              
tcp6       0      0 :::22                   :::*                    LISTEN      758/sshd: /usr/sbin 
```

установлено ssh соединение по порту 22 ip 10.0.2.15, pid 847
22 - стандартный порт для подключения по ssh
53 - стандантный порт для DNS
5555 - эмулятор приложения на порту 5555 (nc -l 5555)

4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?

```bash
root@u8:/home/vagrant# netstat -aulpn  
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
udp        0      0 127.0.0.53:53           0.0.0.0:*                           609/systemd-resolve 
udp        0      0 10.0.2.15:68            0.0.0.0:*                           416/systemd-network 
udp        0      0 0.0.0.0:111             0.0.0.0:*                           1/init
udp6       0      0 :::111                  :::*                                1/init
root@u8:/home/vagrant# ss -uap
State         Recv-Q           Send-Q            Local Address:Port               Peer Address:Port             Process
UNCONN           0                0              127.0.0.53%lo:domain               0.0.0.0:*                  users:(("systemd-resolve",pid=609,fd=12))
UNCONN           0                0              10.0.2.15%eth0:bootpc              0.0.0.0:*                  users:(("systemd-network",pid=416,fd=19))
UNCONN           0                0              0.0.0.0:sunrpc                     0.0.0.0:*                  users:(("rpcbind",pid=608,fd=5),("systemd",pid=1,fd=36))
UNCONN           0                0              [::]:sunrpc                         [::]:*                    users:(("rpcbind",pid=608,fd=7),("systemd",pid=1,fd=38))
```

```bash

```

5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали.

![Screenshot](./img/HomeNet.png)

```
iva@c8:~/Documents/netology/devops-netology/3_8_3  (3.8.3)$ traceroute ya.ru -A
traceroute to ya.ru (87.250.250.242), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1) [*]  0.514 ms  0.596 ms  0.654 ms
 2  95.31.0.1 (95.31.0.1) [AS8402]  3.006 ms  3.008 ms  8.008 ms
 3  78.107.15.1 (78.107.15.1) [AS8402]  8.005 ms  7.994 ms  7.984 ms
 4  10.2.254.178 (10.2.254.178) [*]  7.973 ms  7.963 ms  7.959 ms
....
```

 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

6*. Установите Nginx, настройте в режиме балансировщика TCP или UDP.

7*. Установите bird2, настройте динамический протокол маршрутизации RIP.

8*. Установите Netbox, создайте несколько IP префиксов, используя curl проверьте работу API.

 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате Slack.

---

