#!/usr/bin/env python3

import os, sys, requests, socket, json

log_path='/tmp/check-log.txt'

check_file = os.path.exists(log_path)

print(check_file)

if check_file==False:
 print('Not exists')
 log_file=open(log_path,'w')
# log_file.close()
elif os.path.isfile(log_path)==False:
 print('is a dir')
 sys.exit()
elif os.path.isfile(log_path):
 print('file exist, work')

sitelist=("drive.google.com","mail.google.com","google.com")

for site in sitelist:
 print(f'{site}')
