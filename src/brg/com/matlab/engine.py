# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 22:00:58
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
"""Matlab communication through the Matlab Engine.

This module defines classes for starting and interacting with the Matlab Engine,
and for interacting with an existing (shared) Matlab Session.

>>> m = MatlabEngine()
>>> m.isprime(37)
True

"""


import matlab.engine


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2016-08-29 22:00:58'


__all__ = [
    'MatlabEngineError',
    'MatlabSessionError',
    'MatlabEngine',
    'MatlabSession',
]


class MatlabEngineError(Exception):
    def __init__(self, message=None):
        if not message:
            message = '''Could not start the Matlab engine.
Note that the Matlab engine for Python is only available since R2014b.
For older versions of Matlab, use *MatlabProcess* instead.
On Windows, *MatlabClient* is also available.
'''
        super(MatlabEngineError, self).__init__(message)


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


class MatlabEngine(object):
    """"""

    def __init__(self, delay_start=False):
        self.engine = None
        if not delay_start:
            self.start()

    def __getattr__(self, name):
        if self.engine:
            method = getattr(self.engine, name)
            def wrapper(*args, **kwargs):
                return method(*args, **kwargs)
            return wrapper
        else:
            raise MatlabEngineError()

    def start(self):
        print 'starting engine. this may take a few seconds...'
        self.engine = matlab.engine.start_matlab()
        print 'engine started!'

    def stop(self):
        print 'stopping engine...'
        self.engine.quit()
        print 'engine stopped!'


class MatlabSession(object):
    """Connect to an existing, shared Matlab session.

    Note that the Matlab engine for Python is only available since R2014b.
    """

    def __init__(self):
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
        session = matlab.engine.find_matlab()
        if not session or not len(session):
            raise MatlabSessionError()
        self.session = session[0]
        print self.session

    def connect(self):
        self.find()
        self.engine = matlab.engine.connect_matlab(self.session)

    def disconnect(self):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    # m1 = MatlabEngine()
    m2 = MatlabSession()

    print m2.isprime(37)
