# devops-netology 

### Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

1. Какой системный вызов делает команда cd? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой, это shell builtin, поэтому запустить strace непосредственно на cd не получится. 
    Тем не менее, вы можете запустить strace на /bin/bash -c 'cd /tmp'. В этом случае вы увидите полный список системных вызовов, которые делает сам bash при старте. 
    Вам нужно найти тот единственный, который относится именно к cd. Обратите внимание, что strace выдаёт результат своей работы в поток stderr, а не в stdout.

```
vagrant@u8:~$ strace -e trace=stat,chdir /bin/bash -c "cd /tmp"
stat("/home/vagrant", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat(".", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat("/home", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat("/home/vagrant", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
stat("/tmp", {st_mode=S_IFDIR|S_ISVTX|0777, st_size=4096, ...}) = 0
chdir("/tmp")                           = 0 - смена директории.
+++ exited with 0 +++
```

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

```
vagrant@u8:~$ sudo /usr/sbin/opensnoop-bpfcc

PID    COMM               FD ERR PATH
628    irqbalance          6   0 /proc/interrupts
628    irqbalance          6   0 /proc/stat
628    irqbalance          6   0 /proc/irq/20/smp_affinity
628    irqbalance          6   0 /proc/irq/0/smp_affinity
628    irqbalance          6   0 /proc/irq/1/smp_affinity
628    irqbalance          6   0 /proc/irq/8/smp_affinity
628    irqbalance          6   0 /proc/irq/12/smp_affinity
628    irqbalance          6   0 /proc/irq/14/smp_affinity
628    irqbalance          6   0 /proc/irq/15/smp_affinity
809    vminfo              4   0 /var/run/utmp
623    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
623    dbus-daemon        18   0 /usr/share/dbus-1/system-services
623    dbus-daemon        -1   2 /lib/dbus-1/system-services
623    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
809    vminfo              4   0 /var/run/utmp
623    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
623    dbus-daemon        18   0 /usr/share/dbus-1/system-services
623    dbus-daemon        -1   2 /lib/dbus-1/system-services
623    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
628    irqbalance          6   0 /proc/interrupts
628    irqbalance          6   0 /proc/stat
628    irqbalance          6   0 /proc/irq/20/smp_affinity
628    irqbalance          6   0 /proc/irq/0/smp_affinity
628    irqbalance          6   0 /proc/irq/1/smp_affinity
628    irqbalance          6   0 /proc/irq/8/smp_affinity
628    irqbalance          6   0 /proc/irq/12/smp_affinity
628    irqbalance          6   0 /proc/irq/14/smp_affinity
628    irqbalance          6   0 /proc/irq/15/smp_affinity
809    vminfo              4   0 /var/run/utmp
623    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
623    dbus-daemon        18   0 /usr/share/dbus-1/system-services
623    dbus-daemon        -1   2 /lib/dbus-1/system-services
623    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
```


6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.


не удалось найти данную информацию в Uuntu 20.04, ввиду отсутсвия в базовом образе раздела 2 man.

```
iva@c8:~ $ man 2 uname
<cut>
 uname()  returns system information in the structure pointed to by buf.
       The utsname struct is defined in <sys/utsname.h>:

 Part of the utsname information is also accessible  via  /proc/sys/ker‐
       nel/{ostype, hostname, osrelease, version, domainname}
</cut>
```

uname обращается к системному вызову uname(2) который возвращает структуру определенную в <sys/utsname.h>, так же часть информации utsname доступна через /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}


7. Чем отличается последовательность команд через ; и через && в bash? Например:

Выполнится в любом случае

```
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
```

Команда echo выполнится только в том случае, если директория /tmp/some_dir существует

```
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#
```

Отличие последовательности ';' и '&&' в том что с помощью ';' задаётся последовательное выполнение команд которые надо выполнить (слева на право), а с использование '&&' - логического операнда AND.

В первом случае при использовании ';' вся последовательность выполнится в любом случае вне зависимости от результата выполнения каждой из команд или проверок, 
при использовании '&&' последовательность будет прервана, если хотя бы одна команда или проверка не вернет code 0 или True.

Есть ли смысл использовать в bash &&, если применить set -e?

-e  Exit immediately if a command exits with a non-zero status.

смысл в '&&' пропадает с применением set -e, так как будет осуществлён выход если хотя бы одна команда не вернет code 0, программы/команды могут возвращать не только статус 0.
    дальнейшее выполнение при этом прекратится.

8. Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?

set -euxo

    -e  Exit immediately if a command exits with a non-zero status.
    -u  Treat unset variables as an error when substituting.
    -x  Print commands and their arguments as they are executed.
    -o option-name

	pipefail     the return value of a pipeline is the status of
                           the last command to exit with a non-zero status,
                           or zero if no command exited with a non-zero status

    -e Если одна из команд скрипта завершается неуспешно, то весь скрипт немедленно завершается. 
    -u Если работа с переменными завершается неуспешно, то весь скрирт немедленно завершается. 
    -x Выполняемые команды отображаются на консоли 
    -o pipefail - если одна из команд в pipe завершилась неуспешно, то весь pipe завершается с кодом ошибки этой команды.

    Результат работы скрипта будет более предсказуем, возможно обрабатывать ошибки.

9. Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. 
    В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. 
    Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

    D    uninterruptible sleep (usually IO)
    I    Idle kernel thread
    R    running or runnable (on run queue)
    S    interruptible sleep (waiting for an event to complete)
    T    stopped by job control signal
    t    stopped by debugger during the tracing
    W    paging (not valid since the 2.6.xx kernel)
    X    dead (should never be seen)
    Z    defunct ("zombie") process, terminated but not reaped by its parent

```
vagrant@u8:~$ ps -o stat
STAT
Ss
R+
```

    Наиболее часто встречающийся статус это S - прерываемый сон, процесс ожидает события завершения другого процесса, 
    так же часто встречаются процессы со статусом R - процесс запущен или в очереди на запуск
    I - неактивный поток ядра, 
    при операциях ввода/вывода могут встречаться процессы со статусом D - неприрываемый сон, процесс ждет завершения чтения/записи. 

    Так же у процессов могут встречаться дополнительные ключи, такие как < - высокоприоритетный процесс, N - низкоприоритетный процесс

```
          <    high-priority (not nice to other users)
           N    low-priority (nice to other users)
           L    has pages locked into memory (for real-time and custom IO)
           s    is a session leader
           l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads
                do)
           +    is in the foreground process group
```

увидеть дополнительные параметры процессов можно выполнив $ps aux