#!/usr/bin/env python

import host_data
from token_client import run_token_client

def balance():
    d=len(host_data.neighbors)
    tmp_tkns=[]*d
    # Balance algo
    with host_data.tokens_list_lock:
        for i in range(len(host_data.tokens_list)):
            tmp=host_data.tokens_list.pop()
            index=i % 2*d
            if index < d:
                tmp_tkns[index].append(tmp)
            else:
                host_data.tokens_list.insert(0,tmp)


    send_tokens(tmp_tkns)

def send_tokens(tmp_tkns):
    for i in range(len(host_data.neighbors)):
        run_token_client(host_data.neighbors[i],tmp_tkns[i])


