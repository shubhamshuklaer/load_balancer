#!/usr/bin/env python

import host_data
from token_client import run_token_client

def balance():
    d=len(host_data.neighbors)
    tmp_tkns=[]
    for i in range(d):
        tmp_tkns.append([])
    # Balance algo
    with host_data.tokens_list_lock:
        tk_len=len(host_data.tokens_list)

        for i in range(tk_len):
            tmp=host_data.tokens_list.pop()
            index=i % (2*d)
            print("index :"+str(index))
            if index < d:
                tmp_tkns[index].append(tmp)
            else:
                host_data.tokens_list.insert(0,tmp)


    send_tokens(tmp_tkns)

def send_tokens(tmp_tkns):
    for i in range(len(host_data.neighbors)):
        print("s "+str(i)+":"+str(tmp_tkns[i]))
        run_token_client(host_data.neighbors[i],tmp_tkns[i])


