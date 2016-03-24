#!/usr/bin/env python
from token_serv import Token_serv
from twisted.internet import reactor
from user_token import User_token
import threading
from token_serv import run_token_serv
from token_client import run_token_client
import config
import time

stop_it=False

if not reactor.running:
    threading.Thread(target=reactor.run,kwargs={'installSignalHandlers':0}).start()
    stop_it=True

token_serv_thread=threading.Thread(target=run_token_serv,args=[config.log_serv_port]).start()

count=0
try:
    while True:
        if count % 10 == 0:
            run_token_client("<broadcast>",[User_token("",User_token.LOG_SERVICE_BROADCAST)])
        time.sleep(1)
except KeyboardInterrupt:
    pass

if stop_it:
    reactor.callFromThread(reactor.stop)
