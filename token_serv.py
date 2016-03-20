#!/usr/bin/env python
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import pickle
import config
import host_data
from user_token import User_token
import os

class Token_serv(Protocol):

    def dataReceived(self, data):
        tmp_tokens=pickle.loads(data)
        if len(tmp_tokens)!=0 and tmp_tokens[0].data_type==User_token.WORKER:
            for tmp_tkn in tmp_tokens:
                file_path=os.path.join(host_data.workers_dir,tmp_tkn.data["file_name"])
                with open(file_path,"w") as worker_file:
                    worker_file.write(tmp_tkn.data["content"])
                host_data.insert_worker_hash(file_path)
        elif len(tmp_tokens)!=0 and tmp_tokens[0].data_type==User_token.SOLVED:
            print(tmp_tokens)
        else:
            host_data.append_tokens(tmp_tokens)
        self.transport.loseConnection()

class Token_serv_factory(Factory):
    protocol=Token_serv

def run_token_serv(port=config.token_serv_port):
    reactor.callFromThread(reactor.listenTCP,port,Token_serv_factory())
