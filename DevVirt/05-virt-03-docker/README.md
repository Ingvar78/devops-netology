
# Домашнее задание к занятию "5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Любые вопросы по решению задач задавайте в чате учебной группы.

---

## Задача 1

Сценарий выполения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

Полное описание процесса:

<details>
     <summary>Решение Задачи 1</summary>
    <br>

Регистрируемся [hub.docker.com](https://hub.docker.com/)
Образ буду использовать nginx:stable-alpine - 1.20.2 на момент выполнения.


```bash
iva@c8:~/Documents/docker $ docker pull nginx:stable-alpine
iva@c8:~/Documents/docker $ docker images
REPOSITORY   TAG             IMAGE ID       CREATED        SIZE
nginx        stable          d6c9558ba445   2 days ago     141MB
nginx        1.21.6-alpine   bef258acf10d   3 days ago     23.4MB
nginx        1.21.5-alpine   cc44224bfe20   4 weeks ago    23.5MB
nginx        stable-alpine   373f8d4d4c60   2 months ago   23.2MB

iva@c8:~/Documents/docker $ docker build -t egerpro/nginx-nl:1.20.2 .
Sending build context to Docker daemon   5.12kB
Step 1/2 : FROM nginx:1.20.2-alpine
 ---> 373f8d4d4c60
Step 2/2 : COPY index.html /usr/share/nginx/html/
 ---> 1cbb7153fe19
Successfully built 1cbb7153fe19
Successfully tagged egerpro/nginx-nl:1.20.2
iva@c8:~/Documents/docker $ docker images
REPOSITORY         TAG             IMAGE ID       CREATED          SIZE
egerpro/nginx-nl   1.20.2          1cbb7153fe19   14 seconds ago   23.2MB
egerpro/nginx-nl   stable-alpine   0178cd9e55c1   8 minutes ago    23.2MB
nginx              stable          d6c9558ba445   2 days ago       141MB
nginx              1.21.6-alpine   bef258acf10d   3 days ago       23.4MB
nginx              1.21.5-alpine   cc44224bfe20   4 weeks ago      23.5MB
nginx              1.20.2-alpine   373f8d4d4c60   2 months ago     23.2MB
nginx              stable-alpine   373f8d4d4c60   2 months ago     23.2MB
```

Запускаем контейнер, тестируем
```bash
iva@c8:~/Documents/docker $ docker run --name test-page -p 80:80 -d egerpro/nginx-nl:1.20.2 
b42c9de835840b2916fbfaf68d0004ded071e921cb5dd6c0e00d0ce01a3f1362
iva@c8:~/Documents/docker $ curl localhost
<html>
    <head>Hey, Netology</head>
    <body>
    <h1>I’m DevOps Engineer!</h1>
    </body>
</html>
```
ещё пару проверок:
```bash
iva@c8:~/Documents/docker $ docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS          PORTS                               NAMES
b42c9de83584   egerpro/nginx-nl:1.20.2   "/docker-entrypoint.…"   52 seconds ago   Up 50 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp   test-page
iva@c8:~/Documents/docker $ docker stop $(docker ps -a -q)
b42c9de83584
iva@c8:~/Documents/docker $ docker rm $(docker ps -a -q)
b42c9de83584
iva@c8:~/Documents/docker $ docker exec -it for_test_nginx sh
/ # 
/ # cat /usr/share/nginx/html/index.html 
<html>
    <head>Hey, Netology</head>
    <body>
    <h1>I’m DevOps Engineer!</h1>
    </body>
</html>
/ # 
```

Push-им и чистим локальное ранее загруженные/созданные образы
```bash
va@c8:~/Documents/docker $ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: egerpro
Password: 
WARNING! Your password will be stored unencrypted in /home/iva/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

iva@c8:~/Documents/docker $ docker push egerpro/nginx-nl:1.20.2
The push refers to repository [docker.io/egerpro/nginx-nl]
fb7dd72084b1: Pushed 
6f44c5b5d074: Mounted from library/nginx 
002fcf848e67: Mounted from library/nginx 
e419fa208fe1: Mounted from library/nginx 
112ee9c2903a: Mounted from library/nginx 
68e5252d0d33: Mounted from library/nginx 
1a058d5342cc: Mounted from library/nginx 
1.20.2: digest: sha256:9f4de94ec42951ec4ee27468ca63f9c8a4c67d6b5ac58fb7556db5b83b3a2b91 size: 1775

iva@c8:~/Documents/docker $ docker rmi -f $(docker images -aq)
Untagged: egerpro/nginx-nl:1.20.2
...

iva@c8:~/Documents/docker $ docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
```

загружаем заново

```bash
iva@c8:~/Documents/docker $ docker pull egerpro/nginx-nl:1.20.2
1.20.2: Pulling from egerpro/nginx-nl
97518928ae5f: Pull complete 
a15dfa83ed30: Pull complete 
acae0b19bbc1: Pull complete 
fd4282442678: Pull complete 
b521ea0d9e3f: Pull complete 
b3282d03aa58: Pull complete 
a0be8eca73e4: Pull complete 
Digest: sha256:9f4de94ec42951ec4ee27468ca63f9c8a4c67d6b5ac58fb7556db5b83b3a2b91
Status: Downloaded newer image for egerpro/nginx-nl:1.20.2
docker.io/egerpro/nginx-nl:1.20.2
iva@c8:~/Documents/docker $ docker images
REPOSITORY         TAG       IMAGE ID       CREATED          SIZE
egerpro/nginx-nl   1.20.2    1cbb7153fe19   26 minutes ago   23.2MB
```

ссылка на docker-репозиторий: https://hub.docker.com/repository/docker/egerpro/nginx-nl

</details>

[содержимое докер файла](./src/build/docker/)

```bash
iva@c8:~/Documents/docker $ docker pull egerpro/nginx-nl:1.20.2
1.20.2: Pulling from egerpro/nginx-nl
97518928ae5f: Pull complete 
a15dfa83ed30: Pull complete 
acae0b19bbc1: Pull complete 
fd4282442678: Pull complete 
b521ea0d9e3f: Pull complete 
b3282d03aa58: Pull complete 
a0be8eca73e4: Pull complete 
Digest: sha256:9f4de94ec42951ec4ee27468ca63f9c8a4c67d6b5ac58fb7556db5b83b3a2b91
Status: Downloaded newer image for egerpro/nginx-nl:1.20.2
docker.io/egerpro/nginx-nl:1.20.2
iva@c8:~/Documents/docker $ docker images
REPOSITORY         TAG       IMAGE ID       CREATED          SIZE
egerpro/nginx-nl   1.20.2    1cbb7153fe19   26 minutes ago   23.2MB
```

https://hub.docker.com/repository/docker/egerpro/nginx-nl


## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;
- Nodejs веб-приложение;
- Мобильное приложение c версиями для Android и iOS;
- Шина данных на базе Apache Kafka;
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
- Мониторинг-стек на базе Prometheus и Grafana;
- MongoDB, как основное хранилище данных для java-приложения;
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.


---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
