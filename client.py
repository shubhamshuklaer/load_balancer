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
import threading
import time
import imp

ip=None
worker_path=None
client_path=None
send_tokens=False
wait_for_neighbors=20

def usage():
    print("TODO")

subcmd_index=len(sys.argv)
if "--" in sys.argv:
    subcmd_index=sys.argv.index("--")

def generate_token_list():
    mod = imp.load_source("tmp_client",client_path)
    host_data.accept_data_func=mod.accept_data
    data_list = mod.generate_data_list(sys.argv[subcmd_index+1:])
    ret_val=[]
    hash_val=host_data.calc_file_hash(worker_path)
    for data in data_list:
        ret_val.append(User_token(data,User_token.NORMAL,hash_val))
    #  with open("/tmp/sent.txt","wb") as log_file:
        #  pickle.dump(ret_val,log_file)
    return ret_val

def check_file(file_path):
    if file_path == None:
        print("path cannot be None")
        exit(2)

    if not (os.path.exists(file_path) and os.path.splitext(file_path)[1]==".py"):
        print(file_path+" does not exist or is not a python script")
        exit(2)


def get_file():
    data=dict()
    data["file_name"]=os.path.basename(worker_path)
    with open(worker_path,"r") as script:
        data["content"]=script.read()
    return [User_token(data,User_token.WORKER)]



try:
    opts,args=getopt.getopt(sys.argv[1:subcmd_index],"hsw:c:",["ip="])
except getopt.GetoptError:
    usage()
    exit(2)

for opt,arg in opts:
    if opt=="-h":
        usage()
        exit(0)
    elif opt=="-s":
        send_tokens=True
    elif opt=="--ip":
        ip=arg
    elif opt=="-w":
        worker_path=os.path.expanduser(arg)
    elif opt=="-c":
        client_path=os.path.expanduser(arg)


check_file(worker_path)
if send_tokens:
    check_file(client_path)

def run_with_fastest_ping(func):
    fast_ip=None
    while fast_ip == None:
        print("Waiting for fastest ping")
        time.sleep(wait_for_neighbors)
        fast_ip=host_data.get_fastest_neighbor()
        if fast_ip!=None:
            print("Ip choosen: "+fast_ip)
            run_token_client(fast_ip,func())


if ip == None:
    if send_tokens == True:
        _args=[generate_token_list]
    else:
        _args=[get_file]
    threading.Thread(target=run_with_fastest_ping,args=_args).start()
    run_token_serv(config.solved_token_serv_port)
else:
    if send_tokens == True:
        run_token_client(ip,generate_token_list())
        run_token_serv(config.solved_token_serv_port)
    else:
        run_token_client(ip,get_file())

if not reactor.running:
    reactor.run()
