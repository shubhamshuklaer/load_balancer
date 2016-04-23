#!/usr/bin/env python

import host_data
from token_client import run_token_client

def balance():
    d=len(host_data.neighbors)
    if d == 0:
        return
    cycle_length=d+int(d*host_data.self_loop_fraction)
    #  print("cycle lenght :"+str(cycle_length))
    tmp_tkns=[]
    for i in range(d):
        tmp_tkns.append([])
    # Balance algo
    with host_data.tokens_list_lock:
        tk_len=len(host_data.tokens_list)
        index=0

        for i in range(tk_len):
            tmp=host_data.tokens_list.pop()
            index=(host_data.prev_index + 1 + i) % cycle_length
            #  print("index :"+str(index))
            if index < d:
                tmp_tkns[index].append(tmp)
            else:
                host_data.tokens_list.insert(0,tmp)

        host_data.prev_index=index


    send_tokens(tmp_tkns)

def send_tokens(tmp_tkns):
    for i in range(len(host_data.neighbors)):
        #  print("s "+str(i)+":"+str(tmp_tkns[i]))
        run_token_client(host_data.neighbors[i],tmp_tkns[i])


