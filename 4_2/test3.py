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
