#!/usr/bin/python2
from token_serv import run_token_serv
from token_client import run_token_client
from user_token import User_token
import threading
import host_data
from twisted.internet import reactor
import time

# http://twistedmatrix.com/trac/wiki/FrequentlyAskedQuestions#Igetexceptions.ValueError:signalonlyworksinmainthreadwhenItrytorunmyTwistedprogramWhatswrong
# The default reactor, by default, will install signal handlers to catch events
# like Ctrl-C, SIGTERM, and so on. However, you can't install signal handlers
# from non-main threads in Python, which means that reactor.run() will cause an
# error. Pass the installSignalHandlers=0 keyword argument to reactor.run to
# work around this.
threading.Thread(target=reactor.run,kwargs={'installSignalHandlers':0}).start()

token_serv_thread=threading.Thread(target=run_token_serv)
token_serv_thread.start()

# Testing
run_token_client("localhost",[User_token([1,2,3]),User_token([4,5,6])])
time.sleep(1)
host_data.print_tokens()

# Note that we have to pass a callable in callFromThread. reactor.stop() is not
# callable but reactor.stop is
reactor.callFromThread(reactor.stop)
