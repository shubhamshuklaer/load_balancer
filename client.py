#!/usr/bin/env python
from token_client import run_token_client
from token_serv import run_token_serv
from user_token import User_token
import getopt
import sys
import os
from twisted.internet import reactor
import host_data
import config
import pickle

num_tokens=10
ip=None
file_path=None
send_tokens=False

def usage():
    print("TODO")

def get_test_token_list():
    ret_val=[]
    for i in range(num_tokens):
        ret_val.append(User_token(i,User_token.NORMAL,host_data.calc_file_hash(file_path)))
    #  with open("/tmp/sent.txt","wb") as log_file:
        #  pickle.dump(ret_val,log_file)
    return ret_val

def get_file():
    data=dict()
    data["file_name"]=os.path.basename(file_path)
    with open(file_path,"r") as script:
        data["content"]=script.read()
    return [User_token(data,User_token.WORKER)]


try:
    opts,args=getopt.getopt(sys.argv[1:],"hn:s",["ip=","file="])
except getopt.GetoptError:
    usage()
    exit(2)

for opt,arg in opts:
    if opt=="-h":
        usage()
        exit(0)
    elif opt=="-n":
        send_tokens=True
        num_tokens=int(arg)
    elif opt=="--ip":
        ip=arg
    elif opt=="--file":
        file_path=os.path.expanduser(arg)

if file_path == None:
    exit(2)

if not (os.path.exists(file_path) and os.path.splitext(file_path)[1]==".py"):
    print("File does not exist or is not a python script")
    exit(2)

if ip != None:
    if send_tokens == True:
        run_token_client(ip,get_test_token_list())
        run_token_serv(config.solved_token_serv_port)
    else:
        run_token_client(ip,get_file())

    if not reactor.running:
        reactor.run()

