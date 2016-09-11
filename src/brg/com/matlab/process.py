# -*- coding: utf-8 -*-
# @Date    : 2016-08-29 23:34:28
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
"""Matlab (sub)process.


Examples:

    >>> m = MatlabProcess()
    >>> m.start()
    >>> m.write_value('a', 37)
    >>> m.run_command('tf = isprime(a);')
    >>> m.read_workspace()
    >>> m.stop()
    >>> print m.ws_data

"""


from subprocess import Popen
from subprocess import PIPE

from scipy.io import savemat
from scipy.io import loadmat


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2016-08-29 23:34:28'


__all__ = [
    'MatlabProcessError',
    'MatlabProcess',
]


class MatlabProcessError(Exception):
    def __init__(self, message=None):
        if not message:
            message = """"""
        super(MatlabProcessError, self).__init__(message)


class MatlabProcess(object):
    """"""

    def __init__(self, matlab_exec=None, ws_dir=None, ws_data=None, ws_filename=None):
        self.ws_filename = './workspace.mat'
        self.ws_data = {}
        self.process = None
        self.matlab_exec = matlab_exec or 'matlab'
        self.matlab_options = ['-nosplash']

    def start(self, options=None):
        print 'create workspace file.'
        with open(self.ws_filename, 'wb'):
            pass
        print 'starting Matlab process...'
        pargs = [self.matlab_exec]
        pargs.extend(self.matlab_options)
        self.process = Popen(pargs, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        self._wait_until('__READY__')
        print '================================================================='

    def _wait_until(self, str_to_wait_for):
        self.process.stdin.write("'{0}'\n".format(str_to_wait_for))
        while True:
            line = self.process.stdout.readline()
            if line.strip() == str_to_wait_for:
                return

    def stop(self):
        print '================================================================='
        print 'stopping Matlab process...'
        self.process.stdin.write("exit;\n")
        self.process.terminate()
        print 'closing streams...'
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()

    def run_command(self, command):
        print 'run Matlab command: {0}'.format(command)
        command = command.strip() + '\n'
        self.process.stdin.write(command)
        self._wait_until('__COMPLETED__')

    def write_value(self, name, value):
        print 'write Matlab value: {0} => {1}'.format(name, value)
        self.process.stdin.write("{0}={1};\n".format(name, value))

    def read_value(self, name, default=None):
        print 'read Matlab value: {0}'.format(name)
        self.process.stdin.write("save('{0}', '{1}');\n".format(self.ws_filename, name))
        self._wait_until('__SAVED__')
        loadmat(self.ws_filename, mdict=self.ws_data)
        value = self.ws_data.get(name)
        if value:
            return value[0][0]
        return default

    def write_workspace(self):
        if not self.ws_data:
            return
        print 'write Matlab workspace.'
        savemat(self.ws_filename, self.ws_data)
        self.process.stdin.write("load({0});\n".format(self.ws_filename))
        self._wait_until('__LOADED__')

    def read_workspace(self):
        print 'read Matlab workspace.'
        self.process.stdin.write("save('{0}');\n".format(self.ws_filename))
        self._wait_until('__SAVED__')
        loadmat(self.ws_filename, mdict=self.ws_data)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    m = MatlabProcess()

    m.start()

    m.write_value('a', 37)
    m.run_command('tf = isprime(a);')

    m.read_workspace()

    m.stop()

    print m.ws_data
