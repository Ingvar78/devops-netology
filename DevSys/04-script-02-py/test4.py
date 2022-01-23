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
 print('file exist, work')
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