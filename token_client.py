#!/usr/bin/python2
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from user_token import User_token
import pickle

class Token_client(Protocol):
    def connectionMade(self):
        self.transport.write(pickle.dumps(User_token([1,2,3])))

class Token_client_factory(ClientFactory):
    protocol=Token_client


reactor.connectTCP('localhost', 8007, Token_client_factory())
reactor.run()
