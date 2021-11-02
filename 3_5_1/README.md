# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.

1. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

C точки зрения системы все жесткие ссылки эквивалентны объекту на который ссылаются и иимеют те же атрибуты и права доступа.



1. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

    ```bash
    vagrant@u8:~$ lsblk
    NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    sda                    8:0    0   64G  0 disk 
    ├─sda1                 8:1    0  512M  0 part /boot/efi
    ├─sda2                 8:2    0    1K  0 part 
    └─sda5                 8:5    0 63.5G  0 part 
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
    sdb                    8:16   0  2.5G  0 disk 
    sdc                    8:32   0  2.5G  0 disk 
    ```

1. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

    ```bash
    vagrant@u8:~$ sudo -i
    root@u8:~# fdisk /dev/sdb

    Welcome to fdisk (util-linux 2.34).
    Changes will remain in memory only, until you decide to write them.
    Be careful before using the write command.
    
    Device does not contain a recognized partition table.
    Created a new DOS disklabel with disk identifier 0x79ef6416.
    
    Command (m for help): g
    Created a new GPT disklabel (GUID: 92C28C09-9002-174B-801E-6C7DB07B366A).
    
    Command (m for help): n
    Partition number (1-128, default 1): 
    First sector (2048-5242846, default 2048):
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242846, default 5242846): +2G

    Created a new partition 1 of type 'Linux filesystem' and of size 2 GiB.
    
    Command (m for help): n
    Partition number (2-128, default 2): 
    First sector (4196352-5242846, default 4196352): 
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242846, default 5242846): 

    Created a new partition 2 of type 'Linux filesystem' and of size 511 MiB.

    Command (m for help): p
    Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK   
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 92C28C09-9002-174B-801E-6C7DB07B366A

    Device       Start     End Sectors  Size Type
    /dev/sdb1     2048 4196351 4194304    2G Linux filesystem
    /dev/sdb2  4196352 5242846 1046495  511M Linux filesystem
    
    Command (m for help): wq
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.
    
    ```

1. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

    ```bash
    root@u8:~# sfdisk -d /dev/sdb | sfdisk /dev/sdc
    Checking that no-one is using this disk right now ... OK

    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK   
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes

    >>> Script header accepted.
    >>> Created a new GPT disklabel (GUID: 92C28C09-9002-174B-801E-6C7DB07B366A).
    /dev/sdc1: Created a new partition 1 of type 'Linux filesystem' and of size 2 GiB.
    /dev/sdc2: Created a new partition 2 of type 'Linux filesystem' and of size 511 MiB.
    /dev/sdc3: Done.
    
    New situation:
    Disklabel type: gpt
    Disk identifier: 92C28C09-9002-174B-801E-6C7DB07B366A
    
    Device       Start     End Sectors  Size Type
    /dev/sdc1     2048 4196351 4194304    2G Linux filesystem
    /dev/sdc2  4196352 5242846 1046495  511M Linux filesystem

    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.
    root@u8:~# 
    
    ```

1. Соберите `mdadm` RAID1 на паре разделов 2 Гб.

    ```bash
    root@u8:~# mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
    mdadm: Note: this array has metadata at the start and
        may not be suitable as a boot device.  If you plan to
        store '/boot' on this device please ensure that
        your boot-loader understands md/v1.x metadata, or use
        --metadata=0.90
    mdadm: size set to 2094080K
    Continue creating array? y
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md0 started.
    
    ```

1. Соберите `mdadm` RAID0 на второй паре маленьких разделов.

    ```bash
    root@u8:~# mdadm -C -v /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
    mdadm: chunk size defaults to 512K
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md1 started.
    ```

1. Создайте 2 независимых PV на получившихся md-устройствах.

    ```bash
    root@u8:~# pvcreate /dev/md0
      Physical volume "/dev/md0" successfully created.
    root@u8:~# pvcreate /dev/md1
      Physical volume "/dev/md1" successfully created.
    ```

1. Создайте общую volume-group на этих двух PV.

    ```bash
    root@u8:~# vgcreate vg_shared /dev/md0 /dev/md1
      Volume group "vg_shared" successfully created
    ```

1. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

    ```bash
    root@u8:~# lvcreate -n lv_100m -L100M vg_shared /dev/md1
      Logical volume "lv_100m" created.
    root@u8:~# lvdisplay
    ....

    --- Logical volume ---
      LV Path                /dev/vg_shared/lv_100m
      LV Name                lv_100m
      VG Name                vg_shared
      LV UUID                vTvR3t-H4GW-NYoG-azdP-t04v-iSxY-X0XP2B
      LV Write Access        read/write
      LV Creation host, time u8, 2021-11-02 22:36:47 +0000
      LV Status              available
      # open                 0
      LV Size                100.00 MiB
      Current LE             25
      Segments               1
      Allocation             inherit
      Read ahead sectors     auto
      - currently set to     4096
      Block device           253:2
    ```

1. Создайте `mkfs.ext4` ФС на получившемся LV.

/dev/vg_shared/lv_100m

    ```bash
    root@u8:~# mkfs.ext4 /dev/vg_shared/lv_100m
    mke2fs 1.45.5 (07-Jan-2020)
    Creating filesystem with 25600 4k blocks and 25600 inodes
    
    Allocating group tables: done                            
    Writing inode tables: done                            
    Creating journal (1024 blocks): done
    Writing superblocks and filesystem accounting information: done
    ```

1. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

    ```bash
    root@u8:~# mkdir /tmp/new
    root@u8:~# mount /dev/vg_shared/lv_100m /tmp/new/
    ```

1. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

    ```bash
    root@u8:~# wget -q https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
    root@u8:~# df -h
    Filesystem                     Size  Used Avail Use% Mounted on
    udev                           447M     0  447M   0% /dev
    tmpfs                           99M  704K   98M   1% /run
    /dev/mapper/vgvagrant-root      62G  1.5G   57G   3% /
    tmpfs                          491M     0  491M   0% /dev/shm
    tmpfs                          5.0M     0  5.0M   0% /run/lock
    tmpfs                          491M     0  491M   0% /sys/fs/cgroup
    /dev/sda1                      511M  4.0K  511M   1% /boot/efi
    vagrant                         22G  3.4G   19G  16% /vagrant
    tmpfs                           99M     0   99M   0% /run/user/1000
    /dev/mapper/vg_shared-lv_100m   93M   22M   65M  25% /tmp/new
    root@u8:~# ls -lah /tmp/new/
    total 22M
    drwxr-xr-x  3 root root 4.0K Nov  2 22:43 .
    drwxrwxrwt 10 root root 4.0K Nov  2 22:41 ..
    drwx------  2 root root  16K Nov  2 22:40 lost+found
    -rw-r--r--  1 root root  22M Nov  2 14:24 test.gz
    ```

1. Прикрепите вывод `lsblk`.

    ```bash
    root@u8:~# lsblk
    NAME                    MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    sda                       8:0    0   64G  0 disk  
    ├─sda1                    8:1    0  512M  0 part  /boot/efi
    ├─sda2                    8:2    0    1K  0 part  
    └─sda5                    8:5    0 63.5G  0 part  
      ├─vgvagrant-root      253:0    0 62.6G  0 lvm   /
      └─vgvagrant-swap_1    253:1    0  980M  0 lvm   [SWAP]
    sdb                       8:16   0  2.5G  0 disk  
    ├─sdb1                    8:17   0    2G  0 part  
    │ └─md0                   9:0    0    2G  0 raid1 
    └─sdb2                    8:18   0  511M  0 part  
      └─md1                   9:1    0 1017M  0 raid0 
        └─vg_shared-lv_100m 253:2    0  100M  0 lvm   /tmp/new
    sdc                       8:32   0  2.5G  0 disk  
    ├─sdc1                    8:33   0    2G  0 part  
    │ └─md0                   9:0    0    2G  0 raid1 
    └─sdc2                    8:34   0  511M  0 part  
      └─md1                   9:1    0 1017M  0 raid0 
        └─vg_shared-lv_100m 253:2    0  100M  0 lvm   /tmp/new

    ```

1. Протестируйте целостность файла:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```

    ```bash
    root@u8:~# gzip -t /tmp/new/test.gz
    root@u8:~# echo $?
    0
    ```


1. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

    ```bash
    root@u8:~# pvmove /dev/md1 /dev/md0
      /dev/md1: Moved: 8.00%
      /dev/md1: Moved: 100.00%
    ```

1. Сделайте `--fail` на устройство в вашем RAID1 md.

    ```bash
    root@u8:~# mdadm /dev/md0 --fail /dev/sdb1
    mdadm: set /dev/sdb1 faulty in /dev/md0

    ```

1. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

    ```bash
    root@u8:~# dmesg | grep md0
    [  912.963144] md/raid1:md0: not clean -- starting background reconstruction
    [  912.963145] md/raid1:md0: active with 2 out of 2 mirrors
    [  912.963156] md0: detected capacity change from 0 to 2144337920
    [  912.964622] md: resync of RAID array md0
    [  923.511589] md: md0: resync done.
    [ 3507.605460] md/raid1:md0: Disk failure on sdb1, disabling device. - говорит что ошибка на sda1, диск выключен
               md/raid1:md0: Operation continuing on 1 devices. - продолжает работать на одном диске

    ```

1. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```

    ```bash
    root@u8:~# gzip -t /tmp/new/test.gz
    root@u8:~# echo $?
    0
    ```


1. Погасите тестовый хост, `vagrant destroy`.
 
 ---

