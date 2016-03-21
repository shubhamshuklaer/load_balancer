#!/usr/bin/env python
import pickle
import config
import socket

# we will send list of tokens
def run_token_client(ip,user_tokens,port=config.token_serv_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(pickle.dumps(user_tokens), (ip, port))
    #  reactor.callFromThread(reactor.listenUDP,0,Token_client(ip, port, user_tokens))
