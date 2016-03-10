#!/usr/bin/python2
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import pickle
import config

class Token_client(Protocol):
    def connectionMade(self):
        self.transport.write(pickle.dumps(self.factory.user_token))
    def connectionLost(self,reason):
        reactor.stop()
        # reactor.callFromThread(reactor.stop())

class Token_client_factory(ClientFactory):
    protocol=Token_client
    user_token=None
    def __init__(self,_user_token):
        self.user_token=_user_token

def run_token_client(ip,user_token):
    reactor.connectTCP(ip, config.token_serv_port, Token_client_factory(user_token))
    if not reactor.running:
        reactor.run()
