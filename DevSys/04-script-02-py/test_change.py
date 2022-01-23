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
