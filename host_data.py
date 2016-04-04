#!/usr/bin/env python
from threading import Lock
import os
import hashlib
import sys
import threading
import imp
import config
from token_client import run_token_client
from user_token import User_token,get_ip_address
import ipaddress

neighbors=[]
tokens_list=[]
log_servers=[]
log_servers_lock=Lock()
tokens_list_lock=Lock()
workers_hash_lock=Lock()
neighbors_lock=Lock()
prev_index=0
is_hypercube=False
own_ip=get_ip_address()

workers_hash=dict()
workers_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),"workers")

def is_hypercube_neighbor(ip):
    own_ip_bin=bin(int(ipaddress.IPv4Address(own_ip)))
    ip_bin=bin(int(ipaddress.IPv4Address(ip)))
    num_diff=0
    for i in range(len(own_ip_bin)):
        if own_ip_bin[i] != ip_bin[i]:
            num_diff=num_diff+1
    if num_diff == 1:
        return True
    else:
        return False

def insert_log_server(ip):
    with log_servers_lock:
        if ip not in log_servers:
            log_servers.append(ip)

def send_log():
    data=dict()
    data["num_tokens"]=len(tokens_list)
    tkn=User_token(data,User_token.LOG)
    with log_servers_lock:
        for ip in log_servers:
            run_token_client(ip,[tkn],config.log_serv_port)


def insert_neighbor(ip):
    if ip != get_ip_address():
        with neighbors_lock:
            if ip not in neighbors:
                neighbors.append(ip)


def broadcast_service():
    tkn=User_token("",User_token.SERVICE_BROADCAST)
    run_token_client("<broadcast>",[tkn])


def calc_file_hash(file_path):
    file_path=os.path.expanduser(file_path)
    if not os.path.exists(file_path):
        return None
    else:
        # http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file/3431835#3431835
        # I think block size is only so that we don't have to store the entire huge file in a string.
        # I don't think it has anythin to do with the library
        # https://docs.python.org/3/library/hashlib.html
        # Its written that Repeated calls are equivalent to a single call with
        # the concatenation of all the arguments: m.update(a); m.update(b) is
        # equivalent to m.update(a+b).
        blocksize=65536
        hasher=hashlib.sha256()
        with open(file_path,"r") as f:
            buf = f.read(blocksize)
            while len(buf) > 0:
                #  http://stackoverflow.com/questions/7585307/typeerror-unicode-objects-must-be-encoded-before-hashing
                hasher.update(buf.encode("utf-8"))
                buf = f.read(blocksize)
        return hasher.digest()

def insert_worker_hash(file_path):
    hash_val=calc_file_hash(file_path)
    with workers_hash_lock:
        workers_hash[hash_val]=file_path

def insert_worker(file_name,content):
    file_path=os.path.join(workers_dir,file_name)
    hasher=hashlib.sha256()
    hasher.update(content.encode("utf-8"))
    hash_val=hasher.digest()
    if hash_val in workers_hash:
        #  print("worker exists")
        return False

    with open(file_path,"w") as worker_file:
        worker_file.write(content)
    host_data.insert_worker_hash(file_path)
    return True

def send_worker_to_all(tkn):
    with neighbors_lock:
        for ip in neighbors:
            run_token_client(ip,[tkn])



def append_tokens(user_tokens):
    with tokens_list_lock:
        tokens_list.extend(user_tokens)

def print_tokens():
    with tokens_list_lock:
        print(str(len(tokens_list))+" : "+str(tokens_list))


def gen_all_hash():
    for file_name in os.listdir(workers_dir):
        split=os.path.splitext(file_name)
        # possiblility of generation of pyc
        if len(split)==2 and split[1] == ".py":
            file_path=os.path.join(workers_dir,file_name)
            workers_hash[calc_file_hash(file_path)]=file_path

def solve_data(tkn,worker_path):
    mod = imp.load_source("tmp_worker",worker_path)
    run_token_client(tkn.ip,[User_token(mod.solve(tkn.data),User_token.SOLVED)],config.solved_token_serv_port)

def solve_one_token():
    tmp_tkn=None
    with tokens_list_lock:
        if len(tokens_list) != 0:
            tmp_tkn=tokens_list.pop()
    if tmp_tkn != None:
        if tmp_tkn.worker_hash in workers_hash:
            # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            threading.Thread(target=solve_data,args=[tmp_tkn,workers_hash[tmp_tkn.worker_hash]]).start()
        else:
            with tokens_list_lock:
                tokens_list.append(tmp_tkn)
