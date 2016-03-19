#!/usr/bin/env python
from token_client import run_token_client
from user_token import User_token
import getopt
import sys
import os
from twisted.internet import reactor

num_tokens=10
ip=None
file_path=None

def usage():
    print("TODO")

def get_test_token_list():
    ret_val=[]
    for i in range(num_tokens):
        ret_val.append(User_token(i))
    return ret_val

def get_file():
    print(file_path)
    print(os.path.splitext(file_path))
    if not (os.path.exists(file_path) and os.path.splitext(file_path)[1]==".py"):
        print("File does not exist or is not a python script")
        exit(2)

    data=dict()
    data["file_name"]=os.path.basename(file_path)
    with open(file_path,"r") as script:
        data["content"]=script.read()
    return [User_token(data,User_token.WORKER)]


try:
    opts,args=getopt.getopt(sys.argv[1:],"hn:",["ip=","file="])
except getopt.GetoptError:
    usage()
    exit(2)

for opt,arg in opts:
    if opt=="-h":
        usage()
        exit(0)
    elif opt=="-n":
        num_tokens=int(arg)
    elif opt=="--ip":
        ip=arg
    elif opt=="--file":
        file_path=os.path.expanduser(arg)

if ip != None:
    if file_path is not None:
        run_token_client(ip,get_file())
    else:
        run_token_client(ip,get_test_token_list())
    if not reactor.running:
        reactor.run()

