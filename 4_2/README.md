### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-02-py/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | в данном случае не будет присвоено значение, т.к. будет получено исключение при попытке выполнения операций сложения строковой и целочисленной переменной - TypeError: unsupported operand type(s) for +: 'int' and 'str'  |
| Как получить для переменной `c` значение 12?  | необходимо переменную а объявить как string, т.е. a = '1' либо привести к строке c = str(a) + b  |
| Как получить для переменной `c` значение 3?  | необходимо переменную b объявить int, b =2 или привести к значению int в процессе сложения c = int(a) + int(b) |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```
### Cкрипт:
```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/test/devops-netology/4_2/", "git status"]
abs_path = os.path.abspath(os.path.expanduser(os.path.expandvars(bash_command[0].replace('cd ', ''))))
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(abs_path+'/'+prepare_result)
    if result.find('renamed') != -1:
        prepare_result = result.replace('\trenamed:    ', '')
        print(abs_path+'/'+prepare_result)
    if result.find('new file') != -1:
        prepare_result = result.replace('\tnew file:   ', '')
        print(abs_path+'/'+prepare_result)
    if result.find('     ') != -1:
        prepare_result = result.replace('\t     ', '')
        print(abs_path+'/'+prepare_result)
```

### Вывод скрипта при запуске при тестировании:
```bash
[iva@c8test test]$ ./test_change.py
/home/iva/test/devops-netology/4_2/new file.txt
/home/iva/test/devops-netology/4_2/test.py -> test1.py
/home/iva/test/devops-netology/4_2/test_change.py
[iva@c8test test]$ cd devops-netology/
[iva@c8test devops-netology]$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   4_2/new file.txt
        renamed:    4_2/test.py -> 4_2/test1.py
        modified:   4_2/test_change.py

```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os, sys, getopt
def main(argv):
  path_git = ''
  try:
   opts, args = getopt.getopt(argv,"hp:","path=")
  except getopt.GetoptError:
   print ('test.py -p <path>')
   sys.exit(2)
  for opt, arg in opts:
   if opt == '-h':
     print ('for find changes: ./test.py -p <path> ')
     sys.exit()
   elif opt in ("-p", "--path"):
     path_git = arg
     print ('Path for check: ', path_git)
     check_path = os.path.expanduser(path_git)
   if not path_git or os.path.isdir(check_path) != 1:
    print("git repo not accesible or the specified directory does not exist:" + path_git)
    sys.exit()
   path = os.path.abspath(path_git)
   print (f'debug path: { path}')
   modified = ('modified', 'renamed', 'new file')
   not_a_git = ('not a git', 'not a git repo')
   bash_command = ["cd " + path, "git status"]
   result_os = os.popen(' && '.join(bash_command)).read()
   is_change = False
   for result in result_os.split('\n'):
    for check_t in not_a_git:
        if result.find(check_t) != -1:
          print(path + ": this directory is not a git repository.")
          is_change = True
    for check_t in modified:
        if result.find(check_t) != -1:
            result = result.replace(f'\t{check_t}:','')
            result = result.replace(' ','')
            print(path + "/" + result)
            is_change = True
   if is_change != 1:
        print(path + ": there are no changes in this git repository. working tree clean")


if __name__ == "__main__":
       main(sys.argv[1:])
```

### Вывод скрипта при запуске при тестировании:
```bash
[iva@c8test test]$ ./test3.py -p ./devops-netology/
Path for check:  ./devops-netology/
debug path: /home/iva/test/devops-netology
/home/iva/test/devops-netology/4_2/newfile.txt
/home/iva/test/devops-netology/4_2/test.py->4_2/test1.py
/home/iva/test/devops-netology/4_2/test_change.py
...
[iva@c8test test]$ ./test3.py -p ./netology-devops/
Path for check:  ./netology-devops/
debug path: /home/iva/test/netology-devops
/home/iva/test/netology-devops: there are no changes in this git repository. working tree clean
...
[iva@c8test test]$ ./test3.py -p /home/iva/test/devops-netology/
Path for check:  /home/iva/test/devops-netology/
debug path: /home/iva/test/devops-netology
/home/iva/test/devops-netology/4_2/newfile.txt
/home/iva/test/devops-netology/4_2/test.py->4_2/test1.py
/home/iva/test/devops-netology/4_2/test_change.py
...
[iva@c8test test]$ ./test3.py -p /home/iva/test/devops
Path for check:  /home/iva/test/devops
git repo not accesible or the specified directory does not exist:/home/iva/test/devops
[iva@c8test test]$ mkdir devops_null
[iva@c8test test]$ ./test3.py -p /home/iva/test/devops_null/
Path for check:  /home/iva/test/devops_null/
debug path: /home/iva/test/devops_null
fatal: not a git repository (or any of the parent directories): .git
/home/iva/test/devops_null: there are no changes in this git repository. working tree clean
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3
# sudo python3 -m pip install requests

import os, sys, requests, socket, json, time, datetime

from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError
from contextlib import suppress

change_log='check-log.txt'

check_file = os.path.exists(change_log)

if check_file==False:
 print('Not exists')
 log_file=open(change_log,'w')
 log_file.close()
elif os.path.isfile(change_log)==False:
 print('is a dir')
 sys.exit()
elif os.path.isfile(change_log):
 print('log file exist, work')
 with open(change_log, "a") as f:
  print(f'{datetime.datetime.now():%Y-%m-%d-%H-%M-%S} Check Sarted -------------------------------------------', file=f)
check_status=False

sitelist=("drive.google.com","mail.google.com","google.com","eger.pro")

#for site in sitelist:
# print(f'{site}')

cur_state = {}
last_state = {}
file_json = "services_state.json"
prefix = "http://"
request_timeout = 3
if os.path.isfile(file_json):
    with open(file_json) as json_file:
        data = json.load(json_file)
        last_state = data['Last'][0]
for site in sitelist:
    rt = 0
    with suppress(ConnectTimeout):
        with suppress(ConnectionError):
            r = requests.get(prefix+site, verify=True, timeout=request_timeout)
            rt = r.status_code
    if rt == 200:
        ip = socket.gethostbyname(site)
        ip_prev = ip
        print(site+' - '+ip)
        ip_last_st = last_state.get(site)
        if ip != ip_last_st:
            print('[ERROR] '+site+' IP mismatch: '+str(ip_last_st)+' '+ip)
            check_status=True
            with open(change_log, "a") as f:
             print(f'{datetime.datetime.now():%Y-%m-%d-%H-%M-%S} {site} IP mismatch: {str(ip_last_st)} -> {ip}', file=f)
    else:
        print(f'[ERROR] {prefix+site} return status code: {str(rt)}')
        check_status=True
        with open(change_log, "a") as f:
          print(f'[ERROR] {prefix+site} return status code: {str(rt)}', file=f)
        ip = "error"
    last_state[site] = ip
    json_dict = {'Last': [last_state]}
    with open(file_json, "w") as outfile:
     json.dump(json_dict, outfile, indent=4, sort_keys=False)

if check_status==True:
  with open(change_log, "a") as f:
          print(f'{datetime.datetime.now():%Y-%m-%d-%H-%M-%S} Check Finish with Fail', file=f)
elif check_status==False:
  with open(change_log, "a") as f:
          print(f'{datetime.datetime.now():%Y-%m-%d-%H-%M-%S} Check Finish with status "Ok"', file=f)
```


### Вывод скрипта при запуске при тестировании:



```bash
[iva@c8test test]$ ./test4.py
log file exist, work
drive.google.com - 108.177.14.194
mail.google.com - 173.194.73.18
google.com - 64.233.161.138
[ERROR] http://eger.pro return status code: 403
...
[iva@c8test test]$ ./test4.py
log file exist, work
drive.google.com - 64.233.163.194
[ERROR] drive.google.com IP mismatch: 108.177.14.194 64.233.163.194
mail.google.com - 216.58.209.197
[ERROR] mail.google.com IP mismatch: 173.194.73.18 216.58.209.197
google.com - 74.125.205.138
[ERROR] google.com IP mismatch: 64.233.161.138 74.125.205.138
[ERROR] http://eger.pro return status code: 403

```
#Вывод сохранённой информации в лог изменений и json-файл

```bash
[iva@c8test test]$ cat services_state.json
{
    "Last": [
        {
            "drive.google.com": "64.233.163.194",
            "mail.google.com": "216.58.209.197",
            "google.com": "74.125.205.138",
            "eger.pro": "error"
        }
    ]
}[iva@c8test test]$ cat check-log.txt
2021-12-21-01-33-00 Check Sarted -------------------------------------------
2021-12-21-01-34-18 Check Sarted -------------------------------------------
2021-12-21-01-36-10 Check Sarted -------------------------------------------
2021-12-21-01-36-10 drive.google.com IP mismatch: 108.177.14.194 -> 173.194.222.194
2021-12-21-01-36-10 mail.google.com IP mismatch: 142.251.1.83 -> 64.233.161.17
2021-12-21-01-36-10 google.com IP mismatch: 74.125.205.101 -> 216.58.210.142
2021-12-21-01-38-14 Check Sarted -------------------------------------------
2021-12-21-01-38-16 Check Sarted -------------------------------------------
2021-12-21-01-38-18 Check Sarted -------------------------------------------
2021-12-21-01-38-21 Check Sarted -------------------------------------------
2021-12-21-01-38-23 Check Sarted -------------------------------------------
2021-12-21-01-39-20 Check Sarted -------------------------------------------
2021-12-21-01-39-21 Check Finish with status False
2021-12-21-01-43-33 Check Sarted -------------------------------------------
2021-12-21-01-43-34 drive.google.com IP mismatch: 173.194.222.194 -> 173.194.221.194
2021-12-21-01-43-34 mail.google.com IP mismatch: 64.233.161.17 -> 216.58.209.197
2021-12-21-01-43-34 google.com IP mismatch: 216.58.210.142 -> 64.233.161.102
2021-12-21-01-43-34 Check Finish with Fail
2021-12-21-01-43-58 Check Sarted -------------------------------------------
2021-12-21-01-43-59 Check Finish with status "Ok"
2021-12-21-01-45-15 Check Sarted -------------------------------------------
2021-12-21-01-45-15 drive.google.com IP mismatch: 173.194.221.194 -> 108.177.14.194
2021-12-21-01-45-16 mail.google.com IP mismatch: 216.58.209.197 -> 173.194.73.18
2021-12-21-01-45-16 google.com IP mismatch: 64.233.161.102 -> 64.233.161.138
2021-12-21-01-46-33 Check Sarted -------------------------------------------
[ERROR] http://eger.pro return status code: 403
2021-12-21-01-46-35 Check Finish with Fail
2021-12-21-01-48-55 Check Sarted -------------------------------------------
[ERROR] http://eger.pro return status code: 403
2021-12-21-01-48-57 Check Finish with Fail
2021-12-21-01-49-29 Check Sarted -------------------------------------------
[ERROR] http://eger.pro return status code: 403
2021-12-21-01-49-31 Check Finish with Fail
2021-12-21-01-49-33 Check Sarted -------------------------------------------
[ERROR] http://eger.pro return status code: 403
2021-12-21-01-49-34 Check Finish with Fail
2021-12-21-01-49-40 Check Sarted -------------------------------------------
[ERROR] http://eger.pro return status code: 403
2021-12-21-01-49-42 Check Finish with Fail
2021-12-21-01-49-50 Check Sarted -------------------------------------------
[ERROR] http://eger.pro return status code: 403
2021-12-21-01-49-52 Check Finish with Fail
2021-12-21-01-50-32 Check Sarted -------------------------------------------
2021-12-21-01-50-33 drive.google.com IP mismatch: 108.177.14.194 -> 64.233.163.194
2021-12-21-01-50-33 mail.google.com IP mismatch: 173.194.73.18 -> 216.58.209.197
2021-12-21-01-50-34 google.com IP mismatch: 64.233.161.138 -> 74.125.205.138
[ERROR] http://eger.pro return status code: 403
2021-12-21-01-50-34 Check Finish with Fail
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
```
