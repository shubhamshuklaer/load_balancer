#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pickle
import config
import host_data
from user_token import User_token
import os
# https://twistedmatrix.com/documents/15.5.0/core/howto/udp.html
# http://www.math.uiuc.edu/~gfrancis/illimath/windows/aszgard_mini/pylibs/twisted/test/test_udp.py
class Token_serv(DatagramProtocol):

    def datagramReceived(self, data,addr):
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
        #  self.transport.loseConnection()
    def startProtocol(self):
        print("start")

    def stopProtocol(self):
        print("stopped")

def run_token_serv(port=config.token_serv_port):
    reactor.callFromThread(reactor.listenUDP,port,Token_serv())
