# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 22:00:58
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
"""Matlab communication through the Matlab Engine.

This module defines a class for starting and interacting with the Matlab Engine.

>>> m = MatlabEngine()
>>> m.isprime(37)
True

"""


from brg import matlab_engine


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2016-08-29 22:00:58'


__all__ = [
    'MatlabEngineError',
    'MatlabEngine',
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
        self.engine = matlab_engine.start_matlab()
        print 'engine started!'

    def stop(self):
        print 'stopping engine...'
        self.engine.quit()
        print 'engine stopped!'


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    m = MatlabEngine()

    print m.isprime(37)
