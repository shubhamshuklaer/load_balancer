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

neighbors=[]
tokens_list=[]
tokens_list_lock=Lock()
workers_hash_lock=Lock()
neighbors_lock=Lock()
prev_index=0

workers_hash=dict()
workers_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),"workers")

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
