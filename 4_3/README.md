### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис
1. добавлена ',' в строке между элементами массива 
2. формат именования переменныз '"ip"' -добалены кавычки, так же для данного параметре формат значения приведён к строковому значению поскольку тип переменной должен по идее совпадать для элементов массива

```
{
    "info": "Sample JSON output from our service\t",
    "elements": [{
            "name": "first",
            "type": "server",
            "ip": "7175 "
        }, {
            "name": "second",
            "type": "proxy",
            "ip": "71.78.22.43"
        }
    ]
}

```


## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. 
К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. 
Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. 
Формат записи YAML по одному сервису: `- имя сервиса: его IP`. 
Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт: test4_3.py
```python
#!/usr/bin/env python3
# sudo python3 -m pip install requests
# sudo python3 -m pip install pyyaml

import os, sys, requests, socket, json, time, datetime, yaml

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
 print('file exist, work')
 with open(change_log, "a") as f:
  print(f'{datetime.datetime.now():%Y-%m-%d-%H-%M-%S} Check Sarted -------------------------------------------', file=f)
check_status=False

sitelist=("drive.google.com","mail.google.com","google.com")

cur_state = {}
last_state = {}
file_json = "services_state.json"
file_yaml = "services_state.yaml"
prefix = "http://"
request_timeout = 3

sleep_t = 10
cnt = 1

if os.path.isfile(file_json):
    with open(file_json) as json_file:
        data = json.load(json_file)
        last_state = data['Last'][0]

while True:

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
# single json 
                with open(site + ".json", 'w') as json_f:
                  json_data = json.dumps({site: ip})
                  json_f.write(json_data)
# single yaml
                with open(site + ".yaml", 'w') as yaml_f:
                 yaml_data = yaml.dump([{site: ip}])
                 yaml_f.write(yaml_data)
        else:
            print(f'[ERROR] {prefix+site} return status code: {str(rt)}')
            check_status=True
            with open(change_log, "a") as f:
              print(f'[ERROR] {prefix+site} return status code: {str(rt)}', file=f)
            ip = "error"
        last_state[site] = ip
        json_dict = {'Last': [last_state]}
# full json
        with open(file_json, "w") as outfile:
         json.dump(json_dict, outfile, indent=4, sort_keys=False)
# full yaml
        with open("services_state.yaml", 'w') as yaml_f:
                            yaml_data = yaml.dump(json_dict)
                            yaml_f.write(yaml_data)

    if check_status==True:
      with open(change_log, "a") as f:
              print(f'{datetime.datetime.now():%Y-%m-%d-%H-%M-%S} Check Finish with Fail', file=f)
    elif check_status==False:
      with open(change_log, "a") as f:
              print(f'{datetime.datetime.now():%Y-%m-%d-%H-%M-%S} Check Finish with status "Ok"', file=f)

    cnt += 1
    check_status=False
    if cnt >= 10:
      break
    time.sleep(sleep_t)

```

### Вывод скрипта при запуске при тестировании:
```bash
[iva@c8test test]$ ./test4_3.py
Not exists
drive.google.com - 108.177.14.194
[ERROR] drive.google.com IP mismatch: None 108.177.14.194
mail.google.com - 173.194.222.17
[ERROR] mail.google.com IP mismatch: None 173.194.222.17
google.com - 142.251.1.113
[ERROR] google.com IP mismatch: None 142.251.1.113
drive.google.com - 108.177.14.194
mail.google.com - 173.194.222.17
google.com - 142.251.1.113
drive.google.com - 108.177.14.194
mail.google.com - 173.194.222.17
google.com - 142.251.1.113
drive.google.com - 173.194.222.194
[ERROR] drive.google.com IP mismatch: 108.177.14.194 173.194.222.194
mail.google.com - 173.194.222.18
[ERROR] mail.google.com IP mismatch: 173.194.222.17 173.194.222.18
google.com - 64.233.165.100
[ERROR] google.com IP mismatch: 142.251.1.113 64.233.165.100
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 64.233.165.100
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 64.233.165.100
^CTraceback (most recent call last):
  File "./test4_3.py", line 98, in <module>
    time.sleep(sleep_t)
KeyboardInterrupt
[iva@c8test test]$

```

### json-файл(ы), который(е) записал ваш скрипт:
```json

[iva@c8test test]$ tail -n +1 *.json
==> drive.google.com.json <==
{"drive.google.com": "173.194.222.194"}
==> google.com.json <==
{"google.com": "64.233.165.100"}
==> mail.google.com.json <==
{"mail.google.com": "173.194.222.18"}
==> services_state.json <==
{
    "Last": [
        {
            "drive.google.com": "173.194.222.194",
            "mail.google.com": "173.194.222.18",
            "google.com": "64.233.165.100"
        }
    ]
}
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml

[iva@c8test test]$ tail -n +1 *.yaml
==> drive.google.com.yaml <==
- drive.google.com: 173.194.222.194

==> google.com.yaml <==
- google.com: 64.233.165.100

==> mail.google.com.yaml <==
- mail.google.com: 173.194.222.18

==> services_state.yaml <==
Last:
- drive.google.com: 173.194.222.194
  google.com: 64.233.165.100
  mail.google.com: 173.194.222.18
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python
???
```

### Пример работы скрипта:
???
