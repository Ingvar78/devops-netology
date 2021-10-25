# devops-netology 

### Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

1. Какой системный вызов делает команда cd? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой, это shell builtin, поэтому запустить strace непосредственно на cd не получится. 
    Тем не менее, вы можете запустить strace на /bin/bash -c 'cd /tmp'. В этом случае вы увидите полный список системных вызовов, которые делает сам bash при старте. 
    Вам нужно найти тот единственный, который относится именно к cd. Обратите внимание, что strace выдаёт результат своей работы в поток stderr, а не в stdout.

2. Попробуйте использовать команду file на объекты разных типов на файловой системе. Например:

```
Last login: Mon Oct 25 20:03:26 2021 from 10.0.2.2
vagrant@u8:~$ file /dev/tty
/dev/tty: character special (5/0)
vagrant@u8:~$ file /dev/sda
/dev/sda: block special (8/0)
vagrant@u8:~$ file /bin/bash
/bin/bash: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=a6cb40078351e05121d46daa768e271846d5cc54, for GNU/Linux 3.2.0, stripped

```

Используя strace выясните, где находится база данных file на основании которой она делает свои догадки.

```
vagrant@u8:~$ rm strace2.txt 
vagrant@u8:~$ strace -o strace2.txt   file /bin/bash
```

Ищем в стэктрэйсе какие файлы открывались:


```
vagrant@u8:~$ grep openat strace2.txt 
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libmagic.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/liblzma.so.5", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libbz2.so.1.0", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
openat(AT_FDCWD, "/bin/bash", O_RDONLY|O_NONBLOCK) = 3
```

исключаем библиотеки и кэш из поиска интересующих нас файла и сам bash

остаются три файла, один из которых отсутсвует.

```
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory) - не существует
openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3 - конфигурационный файл для добавления магических чисел
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3 - основной файл содержащий магические числа для определения типа файла.
```

интересующий нас файл:

```
vagrant@u8:~$ ls -la /usr/share/misc/magic.mgc
lrwxrwxrwx 1 root root 24 Jul 28 17:46 /usr/share/misc/magic.mgc -> ../../lib/file/magic.mgc
```

3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. 
    Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

3.1 Создаём поток записи в файл:

```
vagrant@u8:~$ tty
/dev/pts/1
vagrant@u8:~$ htop | tee -a logfile
```

3.2 Проверяем в другой сессии

```
vagrant@u8:~$ tty
/dev/pts/0
vagrant@u8:~$ ls -la | grep logfile 
-rw-rw-r-- 1 vagrant vagrant  73774 Oct 25 22:34 logfile
vagrant@u8:~$ ls -la | grep logfile 
-rw-rw-r-- 1 vagrant vagrant  73774 Oct 25 22:34 logfile
vagrant@u8:~$ ls -la | grep logfile 
-rw-rw-r-- 1 vagrant vagrant  73923 Oct 25 22:34 logfile
vagrant@u8:~$ ls -la | grep logfile 
-rw-rw-r-- 1 vagrant vagrant  73923 Oct 25 22:34 logfile
vagrant@u8:~$ ls -la | grep logfile 
-rw-rw-r-- 1 vagrant vagrant  74020 Oct 25 22:34 logfile
```

3.3 ищем наш процесс который пишет в логфайл и информацию о нём

```
vagrant@u8:~$ ps aux | grep logfile
vagrant     2221  0.0  0.0   8088   592 pts/1    S+   22:39   0:00 tee -a logfile

vagrant@u8:~$ ps aux | grep tee
vagrant     2221  0.0  0.0   8088   592 pts/1    S+   22:39   0:00 tee -a logfile
```

vagrant@u8:~$ lsof -p 2221 | grep logfile
tee     2221 vagrant    3w   REG  253,0   119535  131092 /home/vagrant/logfile

3.4 Удаляем файл.

```
vagrant@u8:~$ rm logfile
vagrant@u8:~$ file logfile
logfile: cannot open `logfile' (No such file or directory)
vagrant@u8:~$ cat logfile
cat: logfile: No such file or directory

```

```
agrant@u8:/home$ lsof -p 2221 | grep logfile
tee     2221 vagrant    3w   REG  253,0   194997  131092 /home/vagrant/logfile (deleted)
```

```
vagrant@u8:~$ cat /proc/2221/fd/3
vagrant@u8:~$  !!#!!
  1  [                          0.0%]   Tasks: 29, 22 thr; 1 running
  2  [                          0.0%]   Load average: 0.00 0.00 0.00 
  3  [                          0.0%]   Uptime: 03:01:12
  4  [|                         0.7%]
  Mem[||||||||            110M/2.92G]
  Swp[                       0K/980M]

    PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command
   2220 vagrant    20   0 10492  3892  3296 R  0.7  0.1  0:01.63 htop
    574 root       RT   0  273M 17992  8200 S  0.0  0.6  0:00.68 /sbin/multipath
   2106 vagrant    20   0 13960  6416  4844 S  0.0  0.2  0:00.15 sshd: vagrant@p
    840 root       20   0  288M  2824  2456 S  0.0  0.1  0:01.03 /usr/sbin/VBoxS
    632 root       20   0 81828  3724  3424 S  0.0  0.1  0:00.21 /usr/sbin/irqba
    424 root       20   0 21568  5620  3904 S  0.0  0.2  0:00.62 /lib/systemd/sy
    394 root       19  -1 59668 24160 23144 S  0.0  0.8  0:00.15 /lib/systemd/sy
   2310 root       20   0 13796  9076  7632 S  0.0  0.3  0:00.01 sshd: vagrant [
    845 root       20   0  288M  2824  2456 S  0.0  0.1  0:00.78 /usr/sbin/VBoxS
   2221 vagrant    20   0  8088   592   528 S  0.0  0.0  0:00.09 tee -a logfile
    624 messagebu  20   0  7604  4652  3992 S  0.0  0.2  0:00.40 /usr/bin/dbus-d
    579 root       RT   0  273M 17992  8200 S  0.0  0.6  0:00.41 /sbin/multipath
    623 root       20   0  232M  7324  6496 S  0.0  0.2  0:00.17 /usr/lib/accoun
    659 root       20   0  232M  7324  6496 S  0.0  0.2  0:00.14 /usr/lib/accoun
F1Help  F2Setup F3SearchF4FilterF5Tree  F6SortByF7Nice -F8Nice +F9Kill  F10Quit

```

Очищаем файл.

```
vagrant@u8:~$ cat /dev/null> /proc/2221/fd/3
```

Очистка файла позволяет освободить место, но т.к. процесс всё ещё работает, файл продолжит наполняться забивая место, что бы этого избежать можно вызвать принудительное завершение процесса, дескриптор удалитсся.


4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

    Зомби-процессы не занимают памяти, но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом.
    При достижении лимита записей все процессы пользователя, от имени которого выполняется создающий зомби родительский процесс, не будут способны создавать новые дочерние процессы.
    Всякий процесс при завершении и до считывания статуса завершения предком пребывает в состоянии зомби, это совершенно нормально и короткоживущие зомби-процессы не представляют проблемы в системе. 
    При этом ряд ошибок программирования может приводить к возникновению и накоплению в системе необрабатываемых процессов-зомби (т. е. уже завершившихся процессов, родитель которых не считывает их статус).

5. В iovisor BCC есть утилита opensnoop:

```
root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
/usr/sbin/opensnoop-bpfcc
```

На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04. Дополнительные сведения по установке.

6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.

7. Чем отличается последовательность команд через ; и через && в bash? Например:

```
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#
```

Есть ли смысл использовать в bash &&, если применить set -e?

8. Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?

9. Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

