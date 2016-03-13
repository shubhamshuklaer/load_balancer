#!/usr/bin/env python
class User_token:
    data=None
    _id=None
    def __init__(self,_data=None):
        self.data=_data

    # called by built-in str() and print() function.
    def __str__(self):
        return str(self.data)

    # http://stackoverflow.com/questions/875074/how-to-print-a-list-dict-or-collection-of-objects-in-python
    # Called by built-in repr() function. When we print list of user_tokens the
    # str function is called on list and then the list calls repr function on
    # all the objects hence we need both. If we print user_token directly then
    # str would have been called
    def __repr__(self):
        return str(self.data)

