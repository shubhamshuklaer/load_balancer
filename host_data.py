#!/usr/bin/env python
from threading import Lock

neighbors=[]
tokens_list=[]
tokens_list_lock=Lock()

def append_tokens(user_tokens):
    with tokens_list_lock:
        tokens_list.extend(user_tokens)

def print_tokens():
    for tkn in tokens_list:
        print(tkn)
