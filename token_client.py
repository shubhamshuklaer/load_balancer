#!/usr/bin/env python
import pickle
import config
import socket
# http://grokbase.com/t/python/python-list/0369kdpe56/scanning-for-local-servers-getting-a-broadcast-address
# http://www.tutorialspoint.com/python/python_networking.htm
# we will send list of tokens
def run_token_client(ip,user_tokens,port=config.token_serv_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    if ip == "<broadcast>":
        sock.setsockopt (socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(pickle.dumps(user_tokens), (ip, port))
    #  reactor.callFromThread(reactor.listenUDP,0,Token_client(ip, port, user_tokens))
