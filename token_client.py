#!/usr/bin/env python
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import pickle
import config

class Token_client(Protocol):
    def connectionMade(self):
        self.transport.write(pickle.dumps(self.factory.user_tokens))

class Token_client_factory(ClientFactory):
    protocol=Token_client
    user_tokens=None
    def __init__(self,_user_tokens):
        self.user_tokens=_user_tokens

# we will send list of tokens
def run_token_client(ip,user_tokens):
    reactor.callFromThread(reactor.connectTCP,ip, config.token_serv_port, Token_client_factory(user_tokens))
