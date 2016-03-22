#!/usr/bin/env python
import pickle
import config
import socket
from user_token import User_token
# http://grokbase.com/t/python/python-list/0369kdpe56/scanning-for-local-servers-getting-a-broadcast-address
# http://www.tutorialspoint.com/python/python_networking.htm
# we will send list of tokens
def run_token_client(ip,user_tokens,port=config.token_serv_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    if ip == "<broadcast>":
        sock.setsockopt (socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while len(user_tokens)!=0:
        tmp_tkns=[]
        while len(pickle.dumps(tmp_tkns)) < config.udp_max_data_size and len(user_tokens)!=0:
            tmp_tkns.append(user_tokens.pop())
        # The last element would have crossed the limit
        if len(pickle.dumps(tmp_tkns)) > config.udp_max_data_size:
            user_tokens.append(tmp_tkns.pop())
        sock.sendto(pickle.dumps(tmp_tkns), (ip, port))
