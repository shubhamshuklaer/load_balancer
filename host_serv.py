#!/usr/bin/python2
from token_serv import run_token_serv
from token_client import run_token_client
from user_token import User_token
import threading

token_serv_thread=threading.Thread(target=run_token_serv)
token_serv_thread.start()

run_token_client("localhost",User_token([1,2,3]))
