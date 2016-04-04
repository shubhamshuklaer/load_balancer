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
        try:
            tmp_tokens=pickle.loads(data)
            if len(tmp_tokens) != 0:
                tmp_tkn=tmp_tokens[0]
                # Only for normal tokens will I send multiple tokens at once
                if tmp_tkn.data_type==User_token.WORKER:
                    if host_data.insert_worker(tmp_tkn.data["file_name"],tmp_tkn.data["content"]):
                        host_data.send_worker_to_all(tmp_tkn)
                elif tmp_tkn.data_type==User_token.SOLVED:
                    print(tmp_tkn)
                elif tmp_tkn.data_type==User_token.SERVICE_BROADCAST:
                    if host_data.is_hypercube:
                        if host_data.is_hypercube_neighbor(tmp_tkn.ip):
                            host_data.insert_neighbor(tmp_tkn.ip)
                    else:
                        host_data.insert_neighbor(tmp_tkn.ip)
                elif tmp_tkn.data_type==User_token.LOG_SERVICE_BROADCAST:
                    host_data.insert_log_server(tmp_tkn.ip)
                elif tmp_tkn.data_type==User_token.LOG:
                    print(tmp_tkn.ip+" : "+str(tmp_tkn.data["num_tokens"]))
                else:
                    host_data.append_tokens(tmp_tokens)
            #  self.transport.loseConnection()
        except EOFError:
            with open("/tmp/got.txt","wb") as log_file:
                log_file.write(data)
            print(str(addr)+" : "+str(data))

    #  def startProtocol(self):
        #  print("start")

    #  def stopProtocol(self):
        #  print("stopped")

def run_token_serv(port=config.token_serv_port):
    reactor.callFromThread(reactor.listenUDP,port,Token_serv())
