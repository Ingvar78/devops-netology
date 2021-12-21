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
