# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1. Работа c HTTP через телнет.
- Подключитесь утилитой телнет к сайту stackoverflow.com
`telnet stackoverflow.com 80`
- отправьте HTTP запрос
```bash
GET /questions HTTP/1.0
HOST: stackoverflow.com
[press enter]
[press enter]
```
- В ответе укажите полученный HTTP код, что он означает?

```bash
iva@c8:~ $ telnet stackoverflow.com 80
Trying 151.101.193.69...
Connected to stackoverflow.com.
Escape character is '^]'.
GET /questions HTTP/1.0
HOST: stackoverflow.com

HTTP/1.1 301 Moved Permanently
cache-control: no-cache, no-store, must-revalidate
location: https://stackoverflow.com/questions
x-request-guid: 7b4e22b9-d2f1-4804-b88c-19286a966ec2
feature-policy: microphone 'none'; speaker 'none'
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
Accept-Ranges: bytes
Date: Wed, 17 Nov 2021 18:48:22 GMT
Via: 1.1 varnish
Connection: close
X-Served-By: cache-bma1676-BMA
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1637174903.626468,VS0,VE101
Vary: Fastly-SSL
X-DNS-Prefetch-Control: off
Set-Cookie: prov=42bf99d4-b665-abd5-a49f-80fbd4c9c66d; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly

Connection closed by foreign host.

```

В случае обращения к сайту с использованием telnet возвращается 301 редирект на https ниже скриншот запроса.

![Screenshot](./img/stof3.png)


2. Повторите задание 1 в браузере, используя консоль разработчика F12.
- откройте вкладку `Network`
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку `Headers` - скрин ниже, для задания 1 и 2.
- укажите в ответе полученный HTTP код. 
307 - редирект на https с указанием целевой страницы
- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего? -
Дольше всего обрабатывался запрос на загрузку страницы, т.е. запрос вызываемый при переходе на целевую страницу.
- приложите скриншот консоли браузера в ответ.

![Screenshot](./img/stof1.png)
![Screenshot](./img/stof2.png)

3. Какой IP адрес у вас в интернете?

95.31.137.252

4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой `whois` 

```bash
route:          95.31.137.0/24
descr:          RU-CORBINA-BROADBAND-POOL2
origin:         AS8402
mnt-by:         RU-CORBINA-MNT
created:        2011-09-16T23:52:14Z
last-modified:  2011-09-16T23:52:14Z
source:         RIPE # Filtered
```

5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`

проходит через две AS - Биллайн(Corbina) AS8402  и Google (AS15169)

```bash
iva@c8:~/Documents/netology/devops-netology/3_6_1  (3.6.1 *)$ traceroute 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1)  0.672 ms  0.735 ms  0.861 ms
 2  95.31.0.1 (95.31.0.1)  2.764 ms  7.762 ms  7.746 ms
 3  78.107.15.1 (78.107.15.1)  7.735 ms  7.724 ms  7.712 ms
 4  10.2.254.178 (10.2.254.178)  7.784 ms  7.788 ms  7.777 ms
 5  m9-crs-be3.corbina.net (195.14.54.141)  7.774 ms  7.763 ms  7.761 ms
 6  * 213.234.224.137 (213.234.224.137)  5.069 ms *
 7  213.234.224.132 (213.234.224.132)  4.413 ms * 72.14.198.182 (72.14.198.182)  9.253 ms

 8  85.21.224.191 (85.21.224.191)  4.270 ms *  4.256 ms
 9  * * 108.170.250.99 (108.170.250.99)  9.206 ms
10  108.170.250.130 (108.170.250.130)  9.146 ms 108.170.250.129 (108.170.250.129)  9.179 ms 108.170.250.83 (108.170.250.83)  39.379 ms
11  142.251.49.24 (142.251.49.24)  19.272 ms 209.85.255.136 (209.85.255.136)  20.846 ms 172.253.65.82 (172.253.65.82)  15.821 ms
12  216.239.42.23 (216.239.42.23)  25.850 ms 172.253.64.55 (172.253.64.55)  22.355 ms 72.14.235.69 (72.14.235.69)  22.334 ms
13  * * 108.170.232.251 (108.170.232.251)  25.462 ms
14  * * 142.250.56.13 (142.250.56.13)  20.317 ms
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  dns.google (8.8.8.8)  18.016 ms * *
```

6. Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?
7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`
8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`

