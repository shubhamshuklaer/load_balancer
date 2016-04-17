#!/usr/bin/env python
from token_serv import run_token_serv
from token_client import run_token_client
from user_token import User_token,get_ip_address
import threading
from multiprocessing import Process
import host_data
from twisted.internet import reactor
import time
from balancer import balance
import getopt
import sys
import json
import config

host_server=True
stop_it=False

def usage():
    print("TODO")

try:
    opts,args=getopt.getopt(sys.argv[1:],"h",["neighbors=","log_server","hypercube"])
except getopt.GetoptError:
    usage()
    exit(2)

for opt,arg in opts:
    if opt=="-h":
        usage()
        exit(0)
    elif opt=="--neighbors":
        print(arg)
        host_data.neighbors=json.loads(arg)
    elif opt=="--log_server":
        host_server=False
    elif opt=="--hypercube":
        host_data.is_hypercube=True

if not reactor.running:
    # http://twistedmatrix.com/trac/wiki/FrequentlyAskedQuestions#Igetexceptions.ValueError:signalonlyworksinmainthreadwhenItrytorunmyTwistedprogramWhatswrong
    # The default reactor, by default, will install signal handlers to catch events
    # like Ctrl-C, SIGTERM, and so on. However, you can't install signal handlers
    # from non-main threads in Python, which means that reactor.run() will cause an
    # error. Pass the installSignalHandlers=0 keyword argument to reactor.run to
    # work around this.
    threading.Thread(target=reactor.run,kwargs={'installSignalHandlers':0}).start()
    stop_it=True

print(get_ip_address())

if host_server:
    host_data.gen_all_hash()
    threading.Thread(target=run_token_serv).start()
else:
    threading.Thread(target=run_token_serv,args=[config.log_serv_port]).start()
    # Blocking call
    host_data.init_log()


count=0

try:
    while True:
        if host_server:
            #  host_data.print_tokens()
            balance()
            host_data.solve_one_token()
            host_data.print_tokens()
            host_data.send_log()
            if count % 10 == 0:
                host_data.broadcast_service()
                print(host_data.neighbors)

            time.sleep(1)
            count=count+1
        else:
            break;
except KeyboardInterrupt:
    pass


if stop_it:
    # Note that we have to pass a callable in callFromThread. reactor.stop() is not
    # callable but reactor.stop is
    reactor.callFromThread(reactor.stop)
