#!/usr/bin/env python

# http://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python/30990617#30990617
# if you want to get the ip of which ever interface is used to connect to the network
# You do not have to have a route to 8.8.8.8 to use this. All it is doing is opening a socket, but not connecting.
import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class User_token:
    WORKER="worker"
    NORMAL="normal"
    SOLVED="solved"
    data=None
    data_type=None
    worker_hash=None
    ip=None
    _id=None
    def __init__(self,_data=None,_data_type=None,_worker_hash=None,__id=None):
        self.data=_data
        self.data_type=_data_type
        self.worker_hash=_worker_hash
        self.ip=get_ip_address()

    # called by built-in str() and print() function.
    def __str__(self):
        return self.__repr__(self)

    # http://stackoverflow.com/questions/875074/how-to-print-a-list-dict-or-collection-of-objects-in-python
    # Called by built-in repr() function. When we print list of user_tokens the
    # str function is called on list and then the list calls repr function on
    # all the objects hence we need both. If we print user_token directly then
    # str would have been called
    def __repr__(self):
        if self.data_type == User_token.WORKER:
            return self.data["file_name"]
        else:
            return str(self.data)

