#!/usr/bin/env python
class User_token:
    data=None
    _id=None
    def __init__(self,_data=None):
        self.data=_data

    def __str__(self):
        return str(self.data)


