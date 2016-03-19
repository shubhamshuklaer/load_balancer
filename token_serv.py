#!/usr/bin/env python
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import pickle
import config
import host_data
import os

class Token_serv(Protocol):

    def dataReceived(self, data):
        tmp_tokens=pickle.loads(data)
        if len(tmp_tokens)!=0 and tmp_tokens[0].data_type=="worker":
            for tmp_tkn in tmp_tokens:
                workers_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),"workers")
                with open(os.path.join(workers_dir,tmp_tkn.data["file_name"]),"w") as worker_file:
                    worker_file.write(tmp_tkn.data["content"])
        else:
            host_data.append_tokens(tmp_tokens)
        self.transport.loseConnection()

class Token_serv_factory(Factory):
    protocol=Token_serv

def run_token_serv():
    reactor.callFromThread(reactor.listenTCP,config.token_serv_port,Token_serv_factory())
