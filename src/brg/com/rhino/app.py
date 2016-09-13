# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 13:31:36
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
"""Communication with Rhino through the COM interface."""

import time

from comtypes.client import CreateObject
from comtypes.client import GetModule


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__date__       = '2016-08-29 13:31:36'


__all__ = [
    'RhinoApp'
]


class RhinoApp(object):
    """"""

    def __init__(self):
        self.app = None
        self.rsm = None
        self.rsi = None

    def create(self):
        self.app = CreateObject('Rhino5.Application')
        self.rsm = GetModule(['{75B1E1B4-8CAA-43C3-975E-373504024FDB}', 1, 0])
        print 'loading script interface...'
        attempts = 20
        while attempts:
            try:
                print 'attempt %s' % attempts
                self.rsi = self.app.GetScriptObject.QueryInterface(self.rsm.IRhinoScript)
                break
            except Exception:
                time.sleep(0.5)
            attempts -= 1
        if self.rsi is None:
            raise Exception('error loading script interface...')
        print 'script interface loaded!'

    def show(self, flag=1):
        self.app.Visible = flag

    def wait(self):
        self.rsi.GetString('Press enter to exit...', 'exit')
        self.rsi.Command('_Exit')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    rhino = RhinoApp()
    rhino.create()
    rhino.show()
    rhino.wait()
