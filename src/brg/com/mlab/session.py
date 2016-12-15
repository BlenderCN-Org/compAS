# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 22:00:58
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
"""Matlab communication through the Matlab Engine.

This module defines a class for interacting with an existing (shared) Matlab Session.

>>> m = MatlabSession()
>>> m.isprime(37)
True

"""

__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = '2016-08-29 22:00:58'


class MatlabSessionError(Exception):
    def __init__(self, message=None):
        if not message:
            message = '''There is no active Matlab session, or could not connect to one...
Don't forget to run "matlab.engine.shareEngine" in Matlab!
Note that the Matlab engine for Python is only available since R2014b.
For older versions of Matlab, use *MatlabProcess* instead.
On Windows, *MatlabClient* is also available.
'''
        super(MatlabSessionError, self).__init__(message)


class MatlabSession(object):
    """Connect to an existing, shared Matlab session.

    Note that the Matlab engine for Python is only available since R2014b.
    """

    def __init__(self):
        self.matlab = None
        self.engine = None
        self.session = None
        self.connect()

    def __getattr__(self, name):
        if self.engine:
            method = getattr(self.engine, name)
            def wrapper(*args, **kwargs):
                return method(*args, **kwargs)
            return wrapper

    def find(self):
        session = self.matlab.engine.find_matlab()
        if not session or not len(session):
            raise MatlabSessionError()
        self.session = session[0]
        print self.session

    def connect(self):
        import matlab
        self.matlab = matlab
        self.find()
        self.engine = matlab.engine.connect_matlab(self.session)

    def disconnect(self):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    m = MatlabSession()

    print m.isprime(37)
