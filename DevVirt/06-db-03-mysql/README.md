# Домашнее задание к занятию "6.3. MySQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

```bash
iva@c8:~/Documents/mySQL $ cat docker-compose.yml 
version: "3.9"
services:
  mysqldb:
    image: mysql/mysql-server:8.0
    restart: always
    environment:
      MYSQL_USER: 'mysql_adm'
      MYSQL_PASSWORD: 'pwd4test'
      MYSQL_DATABASE: 'test_db'
      MYSQL_ROOT_PASSWORD: 'pwd4root'
    volumes:
      - ./data:/var/lib/mysql
      - ./backup:/var/lib/mysql-backup
      - ./restore:/var/lib/mysql-restore
    ports:
      - "3306:3306"
iva@c8:~/Documents/mySQL $ docker-compose build && docker-compose up -d
mysqldb uses an image, skipping
Creating network "mysql_default" with the default driver
Creating mysql_mysqldb_1 ... done
```

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
восстановитесь из него.
Перейдите в управляющую консоль `mysql` внутри контейнера.

```bash
iva@c8:~/Documents/mySQL $ docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS                             PORTS                                                        NAMES
434b533ecdd2   mysql/mysql-server:8.0   "/entrypoint.sh mysq…"   27 seconds ago   Up 24 seconds (health: starting)   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060-33061/tcp   mysql_mysqldb_1
iva@c8:~/Documents/mySQL $ docker exec -it mysql_mysqldb_1 sh
sh-4.4# mysql -u mysql_adm -p test_db < /var/lib/mysql-restore/test_data/test_dump.sql
Enter password: 
sh-4.4# mysql -u mysql_adm -p test_db 
Enter password: 
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.28 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

Используя команду `\h` получите список управляющих команд.

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.

```bash
mysql> \s
--------------
mysql  Ver 8.0.28 for Linux on x86_64 (MySQL Community Server - GPL)

Connection id:		10
Current database:	test_db
Current user:		mysql_adm@localhost
SSL:			Not in use
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		8.0.28 MySQL Community Server - GPL
Protocol version:	10
Connection:		Localhost via UNIX socket
Server characterset:	utf8mb4
Db     characterset:	utf8mb4
Client characterset:	latin1
Conn.  characterset:	latin1
UNIX socket:		/var/lib/mysql/mysql.sock
Binary data as:		Hexadecimal
Uptime:			4 min 4 sec

Threads: 2  Questions: 54  Slow queries: 0  Opens: 160  Flush tables: 3  Open tables: 78  Queries per second avg: 0.221
--------------

mysql> 
```

Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.

```bash
mysql> \u test_db 
Database changed
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| test_db            |
+--------------------+
2 rows in set (0.00 sec)

mysql> SHOW TABLES;
+-------------------+
| Tables_in_test_db |
+-------------------+
| orders            |
+-------------------+
1 row in set (0.00 sec)

mysql> select * from orders where price >300;
+----+----------------+-------+
| id | title          | price |
+----+----------------+-------+
|  2 | My little pony |   500 |
+----+----------------+-------+
1 row in set (0.00 sec)

mysql> \q
Bye
```

В следующих заданиях мы будем продолжать работу с данным контейнером.

## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"

Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.

```bash
sh-4.4# mysql -u root -p test_db 
Enter password: 
mysql> CREATE USER
    -> 'test'@'localhost' IDENTIFIED WITH mysql_native_password by 'test-pass'
    -> PASSWORD EXPIRE INTERVAL 180 DAY
    -> FAILED_LOGIN_ATTEMPTS 3
    -> PASSWORD HISTORY 100
    -> ATTRIBUTE '{"fname": "James","lname": "Pretty"}';
Query OK, 0 rows affected (0.06 sec)

mysql> GRANT SELECT ON test_db.* to 'test'@'localhost';
Query OK, 0 rows affected, 1 warning (0.05 sec)
...

```
    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.

```bash
mysql> select * from information_schema.user_attributes where user like '%test%';
+------+-----------+---------------------------------------+
| USER | HOST      | ATTRIBUTE                             |
+------+-----------+---------------------------------------+
| test | localhost | {"fname": "James", "lname": "Pretty"} |
+------+-----------+---------------------------------------+
1 row in set (0.00 sec)
```

## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

```bash
mysql> SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> show profiles;
mysql> show profiles;
+----------+------------+---------------------------------------+
| Query_ID | Duration   | Query                                 |
+----------+------------+---------------------------------------+
|        1 | 0.00016150 | SET profiling = 1                     |
|        2 | 0.00030900 | SELECT * FROM orders                  |
|        3 | 0.00030250 | SELECT * FROM orders where price >300 |
+----------+------------+---------------------------------------+
3 rows in set, 1 warning (0.00 sec)

mysql> 

```

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.

```bash
mysql> SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'test_db';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | InnoDB |
+------------+--------+
1 row in set (0.00 sec)
```

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`

```bash
mysql> ALTER TABLE orders ENGINE = MyIsam;
Query OK, 5 rows affected (0.37 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'test_db';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | MyISAM |
+------------+--------+
1 row in set (0.00 sec)

```
- на `InnoDB`

```bash
mysql> ALTER TABLE orders ENGINE = InnoDB;
Query OK, 5 rows affected (0.41 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'test_db';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | InnoDB |
+------------+--------+
1 row in set (0.00 sec)

mysql> SHOW PROFILES;
+----------+------------+-----------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                   |
+----------+------------+-----------------------------------------------------------------------------------------+
|        1 | 0.00016150 | SET profiling = 1                                                                       |
|        2 | 0.00030900 | SELECT * FROM orders                                                                    |
|        3 | 0.00030250 | SELECT * FROM orders where price >300                                                   |
|        4 | 0.00103125 | SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'test_db' |
|        5 | 0.37493400 | ALTER TABLE orders ENGINE = MyIsam                                                      |
|        6 | 0.00093650 | SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'test_db' |
|        7 | 0.41138125 | ALTER TABLE orders ENGINE = InnoDB                                                      |
|        8 | 0.00088450 | SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'test_db' |
+----------+------------+-----------------------------------------------------------------------------------------+
8 rows in set, 1 warning (0.00 sec)

mysql> SHOW PROFILE FOR QUERY 3;
+--------------------------------+----------+
| Status                         | Duration |
+--------------------------------+----------+
| starting                       | 0.000082 |
| Executing hook on transaction  | 0.000007 |
| starting                       | 0.000008 |
| checking permissions           | 0.000007 |
| Opening tables                 | 0.000060 |
| init                           | 0.000008 |
| System lock                    | 0.000010 |
| optimizing                     | 0.000010 |
| statistics                     | 0.000019 |
| preparing                      | 0.000020 |
| executing                      | 0.000044 |
| end                            | 0.000005 |
| query end                      | 0.000004 |
| waiting for handler commit     | 0.000008 |
| closing tables                 | 0.000008 |
| freeing items                  | 0.000016 |
| cleaning up                    | 0.000010 |
+--------------------------------+----------+
17 rows in set, 1 warning (0.00 sec)


```

## Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

- в используемой сборке 8.0.28 файл конфигурации находится по пути /etc/my.cnf

```bash
sh-4.4# cat /etc/my.cnf
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/8.0/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M

# Remove leading # to revert to previous value for default_authentication_plugin,
# this will increase compatibility with older clients. For background, see:
# https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_default_authentication_plugin
# default-authentication-plugin=mysql_native_password
skip-host-cache
skip-name-resolve
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
secure-file-priv=/var/lib/mysql-files
user=mysql

pid-file=/var/run/mysqld/mysqld.pid
sh-4.4# 

mysql> SELECT * FROM performance_schema.global_variables WHERE 
    -> Variable_name LIKE 'innodb_buffer_pool_size' OR
    -> Variable_name LIKE 'innodb_log_file_size' OR
    -> Variable_name LIKE 'innodb_log_buffer_size' OR
    -> Variable_name LIKE 'innodb_file_per_table' OR
    -> Variable_name LIKE 'innodb_io_capacity' OR
    -> Variable_name LIKE 'innodb_flush_log_at_trx_commit';
+--------------------------------+----------------+
| VARIABLE_NAME                  | VARIABLE_VALUE |
+--------------------------------+----------------+
| innodb_buffer_pool_size        | 134217728      |
| innodb_file_per_table          | ON             |
| innodb_flush_log_at_trx_commit | 1              |
| innodb_io_capacity             | 200            |
| innodb_log_buffer_size         | 16777216       |
| innodb_log_file_size           | 50331648       |
+--------------------------------+----------------+
6 rows in set (0.00 sec)

```

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб

Приведите в ответе измененный файл `my.cnf`.

```bash
sh-4.4# cat /etc/my.cnf
[mysqld]
general_log = 1
general_log_file = /var/lib/mysql/general.log

default_authentication_plugin = mysql_native_password

innodb_flush_method = O_DSYNC
innodb_log_file_size = 100M
innodb_file_per_table = 1
innodb_log_buffer_size = 1M
innodb_buffer_pool_size = 10M
sh-4.4# mysql -u root -p test_db 
Enter password: 
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.28 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SELECT * FROM performance_schema.global_variables WHERE 
    -> Variable_name LIKE 'innodb_buffer_pool_size' OR
    -> Variable_name LIKE 'innodb_log_file_size' OR
    -> Variable_name LIKE 'innodb_log_buffer_size' OR
    -> Variable_name LIKE 'innodb_file_per_table' OR
    -> Variable_name LIKE 'innodb_io_capacity' OR
    -> Variable_name LIKE 'innodb_flush_log_at_trx_commit';
+--------------------------------+----------------+
| VARIABLE_NAME                  | VARIABLE_VALUE |
+--------------------------------+----------------+
| innodb_buffer_pool_size        | 10485760       |
| innodb_file_per_table          | ON             |
| innodb_flush_log_at_trx_commit | 1              |
| innodb_io_capacity             | 200            |
| innodb_log_buffer_size         | 1048576        |
| innodb_log_file_size           | 104857600      |
+--------------------------------+----------------+
6 rows in set (0.00 sec)

mysql> 
```

---



[InnoDB Startup Options and System Variables](https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html)

```bash
iva@c8:~/Documents/mySQL $ cat docker-compose.yml ./config/my.cnf 
version: "3.9"
services:
  mysqldb:
    image: mysql/mysql-server:8.0
    restart: always
    environment:
      MYSQL_USER: 'mysql_adm'
      MYSQL_PASSWORD: 'pwd4test'
      MYSQL_DATABASE: 'test_db'
      MYSQL_ROOT_PASSWORD: 'pwd4root'
    volumes:
      - ./data:/var/lib/mysql
      - ./backup:/var/lib/mysql-backup
      - ./restore:/var/lib/mysql-restore
      - ./config/my.cnf:/etc/my.cnf
    ports:
      - "3306:3306"
[mysqld]
general_log = 1
general_log_file = /var/lib/mysql/general.log

default_authentication_plugin = mysql_native_password

innodb_flush_method = O_DSYNC
innodb_log_file_size = 100M
innodb_file_per_table = 1
innodb_log_buffer_size = 1M
innodb_io_capacity = 200

innodb-buffer-pool-size=20M 
innodb-buffer-pool-instances=4
innodb-buffer-pool-chunk-size=1M;

```
