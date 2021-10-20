# devops-netology 

### Домашнее задание к занятию "3.1. Работа в терминале, лекция 1"

1. Установлено средство виртуализации Oracle VirtualBox (v6.1 on Linux).

2. Установлено средство автоматизации Hashicorp Vagrant.

```
[iva@c8 devops-netology]$ vagrant -v
Vagrant 2.2.18
```

3. Подготовлено окружение 

```
[iva@c8 devops-netology]$ uname -a
Linux c8.localdomain 4.18.0-305.19.1.el8_4.x86_64 #1 SMP Wed Sep 15 15:39:39 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

4. С помощью базового файла конфигурации запустите Ubuntu 20.04 в VirtualBox посредством Vagrant:

4.1 Создали директорию, в которой будут храниться конфигурационные файлы Vagrant. Выполнили vagrant init. 
    Изменили содержимое Vagrantfile по умолчанию:
```
[iva@c8 Vagrant]$ cat Vagrantfile 
Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-20.04"
 end
```
    выполнили комманду vagrant up , что привело к созданию виртуального хоста со следующими параметрами:

5. Аппаратные ресурсы по умолчанию: RAM 1024МБ, CPU 2, VideoRAM  4МБ, HDD 64ГБ, cеть Intel PRO/1000 MT Desctop (NAT).

6. Ознакомившись с документацией изменили конфигурацию, RAM 3Gb, CPU 4, изменили имя хоста.

```
[iva@c8 Vagrant]$ cat Vagrantfile 
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.hostname = 'u8.local'

  config.vm.provider :virtualbox do |v|
    v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    v.memory = 1024 * 3
    v.cpus = 2 * 2
  end
end
```

7. Подключились к виртуальному хосту с использзованием комманды vagrant ssh

```
vagrant@u8:~$ uname -a
Linux u8 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
vagrant@u8:~$ df -h
Filesystem                  Size  Used Avail Use% Mounted on
udev                        1.5G     0  1.5G   0% /dev
tmpfs                       300M  656K  299M   1% /run
/dev/mapper/vgvagrant-root   62G  1.5G   57G   3% /
tmpfs                       1.5G     0  1.5G   0% /dev/shm
tmpfs                       5.0M     0  5.0M   0% /run/lock
tmpfs                       1.5G     0  1.5G   0% /sys/fs/cgroup
/dev/sda1                   511M  4.0K  511M   1% /boot/efi
vagrant                      22G  3.0G   19G  14% /vagrant
tmpfs                       300M     0  300M   0% /run/user/1000
vagrant@u8:~$ 
```

8. man bash | grep -RHn HISTSIZE

```
vagrant@u8:~/manbash$ man bash | grep -n HISTFILESIZE
1006:       HISTFILESIZE
3536:       FILESIZE.  If HISTFILESIZE is unset, or set to null, a non-numeric value, or a numeric
3549:       history, the history file is truncated to contain no more than HISTFILESIZE lines.  If
3550:       HISTFILESIZE is unset, or set to null, a non-numeric value, or a  numeric  value  less
vagrant@u8:~/manbash$ man bash | grep -n ignoreboth
994:              ignoreboth  is  shorthand for ignorespace and ignoredups.  A value of erasedups
```

Переменная HISTSIZE задаёт длинну истории - количество строк в журнале history, Строка 1006 в man bash.

ignoreboth = ignorespace + ignoredups. Не записывает в журнал строки начинающиеся с пробела и повторяющиеся комманды. Строка 994 в man bash

9. {} -  используется в сценариях требующих генерации значений из набора, для примера {1..10}  сгенерирует последовательность от 1 до 10.

10. 

```
touch {1..100000}  - сгенерирует 100 000 файлов, 
touch {1..300000} - не сможет сгенерировать 300 000 файлов, т.к. есть ограничения на размер аргумента передаваемого в виде массива значений.
```

```
vagrant@u8:~/manbash$ touch {1..300000}
-bash: /usr/bin/touch: Argument list too long
```

11. В man bash поищите по /\[\[. Что делает конструкция [[ -d /tmp ]] - проверяет существование директориеи, возвращает (True/False)

CONDITIONAL EXPRESSIONS
       Conditional expressions are used by the [[ compound command and the test and [ builtin commands to test file attributes and perform 

       -d FILE – True if the FILE exists and is a directory.
12.

```
vagrant@u8:~$ type -a bash
bash is /usr/bin/bash
bash is /bin/bash
vagrant@u8:~$ mkdir /tmp/new_path_directory
vagrant@u8:~$ 
vagrant@u8:~$ cp /bin/bash /tmp/new_path_directory/
vagrant@u8:~$ 
vagrant@u8:~$ PATH=/tmp/new_path_directory:$PATH
vagrant@u8:~$ 
vagrant@u8:~$ type -a bash
bash is /tmp/new_path_directory/bash
bash is /usr/bin/bash
bash is /bin/bash
vagrant@u8:~$ 
```



13. at, batch 

```
 at      executes commands at a specified time.

 batch   executes commands when system load levels permit; in  other  words,  when  the load average drops below 1.5, or the value specified in the invocation of atd.
```
другими словами, at -выполнение в указанное время, batch - в период наименьшей загрузки системы.

14. 