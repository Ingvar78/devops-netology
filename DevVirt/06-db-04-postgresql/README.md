# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

```bash
iva@c8:~/Documents/pg $ docker-compose build && docker-compose up -d
postgres uses an image, skipping
Creating network "pg_default" with the default driver
Pulling postgres (postgres:13.6-alpine3.15)...
13.6-alpine3.15: Pulling from library/postgres
59bf1c3509f3: Pull complete
c50e01d57241: Pull complete
a0646b0f1ead: Pull complete
d61c3269c761: Pull complete
a98aa553905b: Pull complete
863a0e4b7c1c: Pull complete
11bfb8ea649e: Pull complete
4d752d0ff5ff: Pull complete
Digest: sha256:a003a8ef4aed3ec511525efe9230da56d5368f53f6033cb241154dd6781ffd23
Status: Downloaded newer image for postgres:13.6-alpine3.15
Creating pg_postgres_1 ... done
iva@c8:~/Documents/pg $ docker ps
CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                                       NAMES
74141704c281   postgres:13.6-alpine3.15   "docker-entrypoint.s…"   27 seconds ago   Up 15 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   pg_postgres_1
iva@c8:~/Documents/pg $ docker exec -it pg_postgres_1 sh
...
```

Подключитесь к БД PostgreSQL используя `psql`.

psql postgresql://[user[:password]@][host][:port][,...][/dbname][?param1=value1&...]

```bash
~ $ psql postgresql://postgres:pgpwd4test@localhost:5432
psql (13.6)
Type "help" for help.

postgres=# \?
...
```

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД

```bash
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
```

- подключения к БД

```bash
Connection
  \c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo}
                         connect to new database (currently "postgres")
                         
postgres=# \c postgres
You are now connected to database "postgres" as user "postgres".

```
- вывода списка таблиц

для просмотра доступны только системные таблицы, поскольку в БД ещё не создавались пользовательские базы/таблицы, соответсвенно на текущем этапе возомжен просмотр только системных таблиц, комманды дополняются ключём S.

```bash
 (options: S = show system objects, + = additional detail)
...
  \dt[S+] [PATTERN]      list tables
...
postgres=# \dt[S+]
                                        List of relations
   Schema   |          Name           | Type  |  Owner   | Persistence |    Size    | Description 
------------+-------------------------+-------+----------+-------------+------------+-------------
 pg_catalog | pg_aggregate            | table | postgres | permanent   | 56 kB      | 
...

```
- вывода описания содержимого таблиц

```bash
 \d[S+]                 list tables, views, and sequences
 \d[S+]  NAME           describe table, view, sequence, or index
 \d[+] table_name
 
postgres=# \dS+ pg_db_role_setting
                             Table "pg_catalog.pg_db_role_setting"
   Column    |  Type  | Collation | Nullable | Default | Storage  | Stats target | Description 
-------------+--------+-----------+----------+---------+----------+--------------+-------------
 setdatabase | oid    |           | not null |         | plain    |              | 
 setrole     | oid    |           | not null |         | plain    |              | 
 setconfig   | text[] | C         |          |         | extended |              | 
Indexes:
    "pg_db_role_setting_databaseid_rol_index" UNIQUE, btree (setdatabase, setrole), tablespace "pg_global"
Tablespace: "pg_global"
Access method: heap
...

```

- выхода из psql

```bash
  \q                     quit psql

```

## Задача 2

Используя `psql` создайте БД `test_database`.

```bash
postgres=# CREATE DATABASE test_database;
CREATE DATABASE
```

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).


Восстановите бэкап БД в `test_database`.


```bash
postgres=# \q
/ # psql -U postgres -f /var/lib/postgresql/backup/test_dump.sql test_database
SET
SET
SET
SET
SET
 set_config 
------------
 
(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval 
--------
      8
(1 row)

ALTER TABLE

~ $ psql postgresql://postgres:pgpwd4test@localhost:5432
psql (13.6)
Type "help" for help.
postgres=# \l
                                   List of databases
     Name      |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
---------------+----------+----------+------------+------------+-----------------------
 postgres      | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 template1     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 test_database | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

```


Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

```bash
postgres=# \c test_database 
You are now connected to database "test_database" as user "postgres".
test_database=# \dt+
                              List of relations
 Schema |  Name  | Type  |  Owner   | Persistence |    Size    | Description 
--------+--------+-------+----------+-------------+------------+-------------
 public | orders | table | postgres | permanent   | 8192 bytes | 
(1 row)

test_database=# ANALYZE VERBOSE public.orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 8 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE

```

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

```
avg_width	integer	 	Средний размер элементов в столбце, в байтах
```
**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

```bash
test_database=# select avg_width, attname from pg_stats where tablename='orders' order by avg_width desc;
 avg_width | attname 
-----------+---------
        16 | title
         4 | id
         4 | price
(3 rows)

```

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

[Секционирование таблиц](https://postgrespro.ru/docs/postgresql/13/ddl-partitioning)

Предложите SQL-транзакцию для проведения данной операции.

По условиям граница orders_1 начинается со значения большего чем 499 по этой причине начальное value from будет 500
для секции orders_2 значения должны быть меньше или раывно 499 по этой причине последнее значение бужет равно 500,
верхние и нижние границы 

```bash
test_database=# create table orders (id integer not null,title character varying(80) not null,price integer default 0) partition by range (price); 
CREATE TABLE
test_database=# create table orders_2 partition of orders for values from (0) to (500);
CREATE TABLE
test_database=# create table orders_1 partition of orders for values from (500) to (1000);
CREATE TABLE
test_database=# insert into orders (id, title, price) select * from orders_old;
INSERT 0 8
test_database=# select * from orders_1;
 id |       title        | price 
----+--------------------+-------
  2 | My little database |   500
  6 | WAL never lies     |   900
  8 | Dbiezdmin          |   501
(3 rows)
test_database=# select * from orders_2;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(5 rows)
test_database=# select * from orders;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
  2 | My little database   |   500
  6 | WAL never lies       |   900
  8 | Dbiezdmin            |   501
(8 rows)
test_database=# select * from orders_old ;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  2 | My little database   |   500
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  6 | WAL never lies       |   900
  7 | Me and my bash-pet   |   499
  8 | Dbiezdmin            |   501
(8 rows)

```

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

Ответ: "ручного" разбиения можно было избежать при проектировании таблицы путём введения секционирования до внесения данных в таблицу.

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

что бы добавить уникальность значений в секционированнных таблицах необходимо добавить после создания секции соответсвующие констрэйт:

```
alter table orders_1 add constraint orders_1_title_unique unique (title);

alter table orders_2 add constraint orders_2_title_unique unique (title);
```

---
