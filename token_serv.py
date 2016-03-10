#!/usr/bin/python2
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import pickle
import config
import host_data

class Token_serv(Protocol):

    def dataReceived(self, data):
        tmp_token=pickle.loads(data)
        host_data.tokens_list.append(tmp_token)
        print(tmp_token.data)
        self.transport.loseConnection()

class Token_serv_factory(Factory):
    protocol=Token_serv

def run_token_serv():
    reactor.callFromThread(reactor.listenTCP,config.token_serv_port,Token_serv_factory())
    #  if not reactor.running:
        #  reactor.run()
