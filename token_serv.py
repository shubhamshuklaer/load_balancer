#!/usr/bin/python2
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import pickle

class Token_serv(Protocol):

    def dataReceived(self, data):
        tmp_token=pickle.loads(data)
        print(tmp_token.data)
        self.transport.loseConnection()

class Token_serv_factory(Factory):
    protocol=Token_serv
    #  def buildProtocol(self,addr):
        #  return Token_serv()

# 8007 is the port you want to run under. Choose something >1024
endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(Token_serv_factory())
reactor.run()
