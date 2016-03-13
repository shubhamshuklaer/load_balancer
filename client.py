#!/usr/bin/env python
from token_client import run_token_client
from user_token import User_token
import getopt
import sys

def usage():
    print("TODO")

def get_test_token_list():
    ret_val=[]
    for i in range(10):
        ret_val.append(User_token(i))
    return ret_val

try:
    opts,args=getopt.getopt(sys.argv[1:],"h",["ip="])
except getopt.GetoptError:
    usage()
    exit(2)

for opt,arg in opts:
    if opt=="-h":
        usage()
        exit(0)
    elif opt=="--ip":
        run_token_client(ip,get_test_token_list())

