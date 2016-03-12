#!/usr/bin/env python
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import pickle
import config
import host_data

class Token_serv(Protocol):

    def dataReceived(self, data):
        tmp_tokens=pickle.loads(data)
        host_data.append_tokens(tmp_tokens)
        self.transport.loseConnection()

class Token_serv_factory(Factory):
    protocol=Token_serv

def run_token_serv():
    reactor.callFromThread(reactor.listenTCP,config.token_serv_port,Token_serv_factory())
