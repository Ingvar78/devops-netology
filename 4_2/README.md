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
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
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
