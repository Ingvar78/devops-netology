# Домашнее задание к занятию "6.2. SQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

```bash
iva@c8:~/Documents/pg $ cat docker-compose.yml 
version: "3.15"
services:
  postgres:
    image: postgres:12.10-alpine3.15
    environment:
      POSTGRES_PASSWORD: "pgpwd4test"
      PGDATA: "/var/lib/postgresql/data/pgdata"
    volumes:
      - ./:/var/lib/postgresql/data
      - ./backup:/var/lib/postgresql/backup
    ports:
      - "5432:5432"
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 4G
```

```bash
iva@c8:~/Documents/pg $ docker-compose build && docker-compose up -d
postgres uses an image, skipping
Creating network "pg_default" with the default driver
Creating pg_postgres_1 ... done
iva@c8:~/Documents/pg $ docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED         STATUS         PORTS                                       NAMES
35fcae85d34c   postgres:12.10-alpine3.15   "docker-entrypoint.s…"   9 seconds ago   Up 7 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   pg_postgres_1
iva@c8:~/Documents/pg $ docker exec -it pg_postgres_1 sh
/ # ls -la /var/lib/postgresql/
total 0
drwxr-xr-x    1 postgres postgres        20 Feb 20 16:52 .
drwxr-xr-x    1 root     root            24 Feb 12 00:49 ..
drwxr-xr-x    2 root     root             6 Feb 20 16:52 backup
drwxrwxr-x    5 1000     1000           128 Feb 20 16:52 data
/ # 

```

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db

```bash
/ # su - postgres
35fcae85d34c:~$ psql
psql (12.10)
Type "help" for help.

postgres=# CREATE USER "test-admin-user" WITH PASSWORD 'pgadm4test';
CREATE ROLE
postgres=# CREATE DATABASE test_db;
CREATE DATABASE
postgres=# \c test_db
You are now connected to database "test_db" as user "postgres".
test_db=# 
```

- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)

```bash
test_db=# CREATE TABLE orders (id SERIAL PRIMARY KEY, наименование TEXT,  цена INT);
CREATE TABLE
test_db=# CREATE TABLE clients(id SERIAL PRIMARY KEY, фамилия TEXT, страна_проживания TEXT, заказ INT, CONSTRAINT fk_orders FOREIGN KEY (заказ) REFERENCES orders (id));
CREATE TABLE
test_db=# CREATE INDEX страна_проживания_idx ON clients(страна_проживания);
CREATE INDEX
```

- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db

```bash
test_db=# GRANT ALL PRIVILEGES ON DATABASE test_db TO "test-admin-user";
GRANT
test_db=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "test-admin-user";
GRANT
test_db=# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "test-admin-user";
GRANT
```
- создайте пользователя test-simple-user

```bash
test_db=# CREATE USER "test-simple-user" WITH PASSWORD 'pgsimpl4test';
CREATE ROLE
```
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

```bash
test_db=# GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "test-simple-user";
GRANT
```

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,

```bash
test_db=# \list
                                     List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |       Access privileges        
-----------+----------+----------+------------+------------+--------------------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres                  +
           |          |          |            |            | postgres=CTc/postgres         +
           |          |          |            |            | "test-admin-user"=CTc/postgres
(4 rows)

```
- описание таблиц (describe)

```bash
test_db=# \d orders
                               Table "public.orders"
    Column    |  Type   | Collation | Nullable |              Default               
--------------+---------+-----------+----------+------------------------------------
 id           | integer |           | not null | nextval('orders_id_seq'::regclass)
 наименование | text    |           |          | 
 цена         | integer |           |          | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)

test_db=# \d clients
                                  Table "public.clients"
      Column       |  Type   | Collation | Nullable |               Default               
-------------------+---------+-----------+----------+-------------------------------------
 id                | integer |           | not null | nextval('clients_id_seq'::regclass)
 фамилия           | text    |           |          | 
 страна_проживания | text    |           |          | 
 заказ             | integer |           |          | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "страна_проживания_idx" btree ("страна_проживания")
Foreign-key constraints:
    "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)

```

- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db

SELECT * from information_schema.table_privileges WHERE table_catalog ILIKE 'test_db%' and table_schema ILIKE 'public';

ограничено схемой public - т.к. в ней расположены основные таблицы, в случае если необходимо получить список всех объектов БД данный фильтр можно убрать.

- список пользователей с правами над таблицами test_db

```bash
test_db=# SELECT * from information_schema.table_privileges WHERE table_catalog ILIKE 'test_db%' and table_schema ILIKE 'public';
 grantor  |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy 
----------+------------------+---------------+--------------+------------+----------------+--------------+----------------
 postgres | postgres         | test_db       | public       | orders     | INSERT         | YES          | NO
 postgres | postgres         | test_db       | public       | orders     | SELECT         | YES          | YES
 postgres | postgres         | test_db       | public       | orders     | UPDATE         | YES          | NO
 postgres | postgres         | test_db       | public       | orders     | DELETE         | YES          | NO
 postgres | postgres         | test_db       | public       | orders     | TRUNCATE       | YES          | NO
 postgres | postgres         | test_db       | public       | orders     | REFERENCES     | YES          | NO
 postgres | postgres         | test_db       | public       | orders     | TRIGGER        | YES          | NO
 postgres | test-admin-user  | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test-admin-user  | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | TRUNCATE       | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | REFERENCES     | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | TRIGGER        | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test-simple-user | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | DELETE         | NO           | NO
 postgres | postgres         | test_db       | public       | clients    | INSERT         | YES          | NO
 postgres | postgres         | test_db       | public       | clients    | SELECT         | YES          | YES
 postgres | postgres         | test_db       | public       | clients    | UPDATE         | YES          | NO
 postgres | postgres         | test_db       | public       | clients    | DELETE         | YES          | NO
 postgres | postgres         | test_db       | public       | clients    | TRUNCATE       | YES          | NO
 postgres | postgres         | test_db       | public       | clients    | REFERENCES     | YES          | NO
 postgres | postgres         | test_db       | public       | clients    | TRIGGER        | YES          | NO
 postgres | test-admin-user  | test_db       | public       | clients    | INSERT         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | SELECT         | NO           | YES
 postgres | test-admin-user  | test_db       | public       | clients    | UPDATE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | TRUNCATE       | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | REFERENCES     | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | TRIGGER        | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | INSERT         | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | SELECT         | NO           | YES
 postgres | test-simple-user | test_db       | public       | clients    | UPDATE         | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | DELETE         | NO           | NO
(36 rows)

test_db=# \dp
                                           Access privileges
 Schema |      Name      |   Type   |         Access privileges          | Column privileges | Policies 
--------+----------------+----------+------------------------------------+-------------------+----------
 public | clients        | table    | postgres=arwdDxt/postgres         +|                   | 
        |                |          | "test-admin-user"=arwdDxt/postgres+|                   | 
        |                |          | "test-simple-user"=arwd/postgres   |                   | 
 public | clients_id_seq | sequence | postgres=rwU/postgres             +|                   | 
        |                |          | "test-admin-user"=rwU/postgres     |                   | 
 public | orders         | table    | postgres=arwdDxt/postgres         +|                   | 
        |                |          | "test-admin-user"=arwdDxt/postgres+|                   | 
        |                |          | "test-simple-user"=arwd/postgres   |                   | 
 public | orders_id_seq  | sequence | postgres=rwU/postgres             +|                   | 
        |                |          | "test-admin-user"=rwU/postgres     |                   | 
(4 rows)
```

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

```bash
test_db=# INSERT INTO public.orders (наименование, цена) VALUES('Шоколад', 10),('Принтер', 3000),('Книга', 500),('Монитор', 7000),('Гитара', 4000);
INSERT 0 5
```
Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

```bash
test_db=# INSERT INTO public.clients (фамилия, страна_проживания, заказ) VALUES('Иванов Иван Иванович', 'USA'),('Петров Петр Петрович', 'Canada'),('Иоганн Себастьян Бах', 'Japan'),('Ронни Джеймс Дио', 'Russia'),('Ritchie Blackmore', 'Russia');
ERROR:  INSERT has more target columns than expressions
LINE 1: ... INTO public.clients (фамилия, страна_проживания, заказ) VAL...
                                                             ^ поскольку поле заказ является fk то при вставке можно получить ошибку если значение не указано


test_db=# INSERT INTO public.clients (фамилия, страна_проживания) VALUES('Иванов Иван Иванович', 'USA'),('Петров Петр Петрович', 'Canada'),('Иоганн Себастьян Бах', 'Japan'),('Ронни Джеймс Дио', 'Russia'),('Ritchie Blackmore', 'Russia');
INSERT 0 5

```
Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 

```bash
test_db=# select count(*) from orders;
 count 
-------
     5
(1 row)

test_db=# select count(*) from clients;
 count 
-------
     5
(1 row)

```
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

```bash
test_db=# select * from orders;
 id | наименование | цена 
----+--------------+------
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000
(5 rows)

test_db=# select * from clients;
 id |       фамилия        | страна_проживания | заказ 
----+----------------------+-------------------+-------
  1 | Иванов Иван Иванович | USA               |      
  2 | Петров Петр Петрович | Canada            |      
  3 | Иоганн Себастьян Бах | Japan             |      
  4 | Ронни Джеймс Дио     | Russia            |      
  5 | Ritchie Blackmore    | Russia            |      
(5 rows)

```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

```bash
test_db=# update clients set заказ =(select id from orders o where наименование='Книга') where фамилия ='Иванов Иван Иванович';
UPDATE 1
test_db=# update clients set заказ =(select id from orders o where наименование='Монитор') where фамилия ='Петров Петр Петрович';
UPDATE 1
test_db=# update clients set заказ =(select id from orders o where наименование='Гитара') where фамилия ='Иоганн Себастьян Бах';
UPDATE 1
test_db=# select * from clients;
 id |       фамилия        | страна_проживания | заказ 
----+----------------------+-------------------+-------
  4 | Ронни Джеймс Дио     | Russia            |      
  5 | Ritchie Blackmore    | Russia            |      
  1 | Иванов Иван Иванович | USA               |     3
  2 | Петров Петр Петрович | Canada            |     4
  3 | Иоганн Себастьян Бах | Japan             |     5

```

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.

```bash
test_db=# select * from clients c join orders o on c.заказ =o.id and c.заказ IS NOT NULL order by c.id;
 id |       фамилия        | страна_проживания | заказ | id | наименование | цена 
----+----------------------+-------------------+-------+----+--------------+------
  1 | Иванов Иван Иванович | USA               |     3 |  3 | Книга        |  500
  2 | Петров Петр Петрович | Canada            |     4 |  4 | Монитор      | 7000
  3 | Иоганн Себастьян Бах | Japan             |     5 |  5 | Гитара       | 4000
(3 rows)

или

test_db=# select * from clients where заказ is not null;
 id |       фамилия        | страна_проживания | заказ 
----+----------------------+-------------------+-------
  1 | Иванов Иван Иванович | USA               |     3
  2 | Петров Петр Петрович | Canada            |     4
  3 | Иоганн Себастьян Бах | Japan             |     5
(3 rows)


```

Подсказк - используйте директиву `UPDATE`.

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

```bash
test_db=# explain select * from clients where заказ is not null;
                        QUERY PLAN                         
-----------------------------------------------------------
 Seq Scan on clients  (cost=0.00..18.10 rows=806 width=72)
   Filter: ("заказ" IS NOT NULL)
(2 rows)

test_db=# explain select * from clients c join orders o on c.заказ =o.id and c.заказ IS NOT NULL order by c.id;
                                  QUERY PLAN                                   
-------------------------------------------------------------------------------
 Sort  (cost=96.14..98.15 rows=806 width=116)
   Sort Key: c.id
   ->  Hash Join  (cost=37.00..57.23 rows=806 width=116)
         Hash Cond: (c."заказ" = o.id)
         ->  Seq Scan on clients c  (cost=0.00..18.10 rows=806 width=72)
               Filter: ("заказ" IS NOT NULL)
         ->  Hash  (cost=22.00..22.00 rows=1200 width=40)
               ->  Seq Scan on orders o  (cost=0.00..22.00 rows=1200 width=40)
(8 rows)

```
Приведите получившийся результат и объясните что значат полученные значения.

в первом варианте при запросе по таблице clients планировщик выбрал план простого последовательного сканирования. 

Числа, перечисленные в скобках (слева направо), имеют следующий смысл:
Стоимость запуска (0.00) - время, которое проходит, прежде чем начнётся этап вывода данных, например для сортирующего узла это время сортировки.
Вторая цифра - общая стоимость (18.10) - вычисляется в предположении что данная часть плана выполняется до конца, то есть возвращает все доступные строки.
Ожидаемое количество строк (806), которое должен вывести этот узел плана при выполнении до конца узла плана.
Ожидаемый средний размер строк (72), выводимых этим узлом плана (в байтах).

Второй план запроса включает стоимость выполненич сортировки результата и сканирования таблицы orders

так же возможно получение представления плана запроса в формате JSON 

```
explain (FORMAT JSON) select * from clients c join orders o on c.заказ =o.id and c.заказ IS NOT NULL order by c.id;

[
  {
    "Plan": {
      "Node Type": "Sort",
      "Parallel Aware": false,
      "Startup Cost": 96.14,
      "Total Cost": 98.15,
      "Plan Rows": 806,
      "Plan Width": 116,
      "Sort Key": ["c.id"],
      "Plans": [
        {
          "Node Type": "Hash Join",
          "Parent Relationship": "Outer",
          "Parallel Aware": false,
          "Join Type": "Inner",
          "Startup Cost": 37.00,
          "Total Cost": 57.23,
          "Plan Rows": 806,
          "Plan Width": 116,
          "Inner Unique": true,
          "Hash Cond": "(c.\"заказ\" = o.id)",
          "Plans": [
            {
              "Node Type": "Seq Scan",
              "Parent Relationship": "Outer",
              "Parallel Aware": false,
              "Relation Name": "clients",
              "Alias": "c",
              "Startup Cost": 0.00,
              "Total Cost": 18.10,
              "Plan Rows": 806,
              "Plan Width": 72,
              "Filter": "(\"заказ\" IS NOT NULL)"
            },
            {
              "Node Type": "Hash",
              "Parent Relationship": "Inner",
              "Parallel Aware": false,
              "Startup Cost": 22.00,
              "Total Cost": 22.00,
              "Plan Rows": 1200,
              "Plan Width": 40,
              "Plans": [
                {
                  "Node Type": "Seq Scan",
                  "Parent Relationship": "Outer",
                  "Parallel Aware": false,
                  "Relation Name": "orders",
                  "Alias": "o",
                  "Startup Cost": 0.00,
                  "Total Cost": 22.00,
                  "Plan Rows": 1200,
                  "Plan Width": 40
                }
              ]
            }
          ]
        }
      ]
    }
  }
]
```



## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

```bash
35fcae85d34c:~$ exit
/ # chown -R postgres:postgres /var/lib/postgresql/backup/
/ # ls -la /var/lib/postgresql/backup/
total 0
drwxr-xr-x    2 postgres postgres         6 Feb 20 16:52 .
drwxr-xr-x    1 postgres postgres        61 Feb 20 18:13 ..
/ # ls -la /var/lib/postgresql/
total 12
drwxr-xr-x    1 postgres postgres        61 Feb 20 18:13 .
drwxr-xr-x    1 root     root            24 Feb 12 00:49 ..
-rw-------    1 postgres postgres        99 Feb 20 18:15 .ash_history
-rw-------    1 postgres postgres      6102 Feb 20 18:13 .psql_history
drwxr-xr-x    2 postgres postgres         6 Feb 20 16:52 backup
drwxrwxr-x    5 1000     1000           128 Feb 20 16:52 data
/ # su - postgres
35fcae85d34c:~/backup$ cd /var/lib/postgresql/backup/
35fcae85d34c:~/backup$ pg_dumpall --database=test_db -c -U postgres | gzip > dump_test_db.gz
35fcae85d34c:~/backup$ pg_dump -Fd test_db -f dump_2022_02_20
35fcae85d34c:~/backup$ ls -la
total 4
drwxr-xr-x    3 postgres postgres        52 Feb 20 18:48 .
drwxr-xr-x    1 postgres postgres        61 Feb 20 18:47 ..
drwx------    2 postgres postgres        59 Feb 20 18:48 dump_2022_02_20
-rw-r--r--    1 postgres postgres      1967 Feb 20 18:48 dump_test_db.gz
35fcae85d34c:~/backup$ exit 
/ # exit
iva@c8:~/Documents/pg $ docker-compose down
Stopping pg_postgres_1 ... done
Removing pg_postgres_1 ... done
Removing network pg_default
```

Поднимите новый пустой контейнер с PostgreSQL.

```bash
iva@c8:~/Documents/pg $ docker run --name pg-12.10 -p 5432:5432 -e POSTGRES_PASSWORD=pgpwd4test -e PGDATA=/var/lib/postgresql/data/pgdata -d -v "$(pwd)/newdata":/var/lib/postgresql/data -v "/home/iva/Documents/pg/backup":/var/lib/postgresql/backup:rw postgres:12.10
a3bc52374743593a584cc39466e9fcf6d0374e080663cb4f886f24f23c55a9c3
iva@c8:~/Documents/pg $ ls -la
итого 12
drwxrwxr-x.  5 iva   iva     75 фев 20 22:37 .
drwxr-xr-x. 11 iva   iva   4096 фев 20 22:04 ..
drwxr-xr-x.  3 avahi avahi   52 фев 20 21:48 backup
-rw-rw-r--.  1 iva   iva    391 фев 20 18:51 docker-compose.yml
drwxr-xr-x.  3 root  root    20 фев 20 22:35 newdata
drwx------. 19 avahi root  4096 фев 20 21:49 pgdata
iva@c8:~/Documents/pg $ docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS                                       NAMES
a3bc52374743   postgres:12.10   "docker-entrypoint.s…"   56 seconds ago   Up 55 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   pg-12.10
```

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

```bash
iva@c8:~/Documents/pg $ docker exec -it pg-12.10 sh
# su - postgres
postgres@a3bc52374743:~$ ls -la
total 4
drwxr-xr-x. 1 postgres postgres 41 Feb 20 19:39 .
drwxr-xr-x. 1 root     root     24 Feb 14 22:09 ..
-rw-------. 1 postgres postgres 26 Feb 20 19:39 .bash_history
drwxr-xr-x. 3       70       70 52 Feb 20 18:48 backup
drwxr-xr-x. 3 root     root     20 Feb 20 19:35 data
postgres@a3bc52374743:~$ 
..
postgres@a3bc52374743:~/backup$ psql -U postgres -W test_db < dump_test_db
Password: 
...

postgres=# \c test_db;
You are now connected to database "test_db" as user "postgres".
test_db=# \d
               List of relations
 Schema |      Name      |   Type   |  Owner   
--------+----------------+----------+----------
 public | clients        | table    | postgres
 public | clients_id_seq | sequence | postgres
 public | orders         | table    | postgres
 public | orders_id_seq  | sequence | postgres
(4 rows)

test_db=# \d orders
                                     Table "public.orders"
          Column          |  Type   | Collation | Nullable |              Default               
--------------------------+---------+-----------+----------+------------------------------------
 id                       | integer |           | not null | nextval('orders_id_seq'::regclass)
 наименование | text    |           |          | 
 цена                 | integer |           |          | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)

test_db=# \d clients
                                          Table "public.clients"
              Column               |  Type   | Collation | Nullable |               Default               
-----------------------------------+---------+-----------+----------+-------------------------------------
 id                                | integer |           | not null | nextval('clients_id_seq'::regclass)
 фамилия                    | text    |           |          | 
 страна_проживания | text    |           |          | 
 заказ                        | integer |           |          | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "страна_проживания_idx" btree ("страна_проживания")
Foreign-key constraints:
    "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)



```

---

Полезные ссылки по теме:

[postgres on dockerhub](https://hub.docker.com/_/postgres)

[Запускаем PostgreSQL в Docker: от простого к сложному](https://habr.com/ru/post/578744/)
