"""This module ...


..  Copyright 2014 Block Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        `http://www.apache.org/licenses/LICENSE-2.0`_

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import json

from xmlrpclib import ServerProxy


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Jul 10, 2015'
__contact__    = '''ETH Zurich,
Institute for Technology in Architecture,
Block Research Group,
Stefano-Franscini-Platz 5,
HIL H 47,
8093 Zurich, Switzerland
'''


class WebAPIError(Exception):
    pass


class WebAPI(object):

    def __init__(self, url=None):
        self._url = None
        self._server = None
        self._funcname = None
        self._func = None
        self.url = url
        self.error = None
        self.profile = None
        self.data = None
        self.iterations = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        if url:
            self._server = ServerProxy(url)

    def reset(self):
        self.error = None
        self.profile = None
        self.data = None
        self.iterations = None

    def test(self):
        self.reset()
        return self._server.test()

    def info(self):
        self.reset()
        return self._server.info()

    def list_methods(self):
        self.reset()
        return self._server.list_methods()

    def method_help(self, name):
        self.reset()
        return self._server.method_help(name)

    def method_signature(self, name):
        self.reset()
        return self._server.method_signature(name)

    def __getattr__(self, funcname):
        self.reset()
        self._funcname = funcname
        if self._server is None:
            if not self._url:
                self.error = 'There is no server address.'
            else:
                self.error = 'The server is not available.'
            raise WebAPIError(self.error)
        try:
            self._func = getattr(self._server, self._funcname)
        except:
            self.error = 'The function does not exist on the web server.'
            raise WebAPIError(self.error)
        return self.func

    def func(self, idict=None, **kwargs):
        if not idict:
            idict = {}
        idict.update(kwargs)
        idump = json.dumps(idict)
        result = None
        attempts = 10
        while attempts:
            attempts -= 1
            try:
                string = self._func(idump)
            except IOError as e:
                if not attempts:
                    print e
            else:
                result = json.loads(string)
                break
        if result is None:
            self.error = 'No output was generated.'
            raise WebAPIError(self.error)
        self.error = result.get('error', None)
        if self.error:
            raise WebAPIError(self.error)
        self.data = result.get('data', None)
        self.profile = result.get('profile', '')
        self.iterations = result.get('iterations', [])
        return self.data

    def print_error(self):
        print '=' * 80
        print 'Error'
        print '-' * 80
        print self.error
        print

    def print_profile(self):
        print '=' * 80
        print 'Profile'
        print '-' * 80
        print self.profile
        print

    def print_data(self):
        print '=' * 80
        print 'Data'
        print '-' * 80
        print self.data
        print

    def print_iterations(self):
        print '=' * 80
        print 'Iterations'
        print '-' * 80
        print self.iterations
        print

    def print_output(self, title=None):
        if title:
            print '#' * 80
            print title
            print
        self.print_error()
        self.print_data()
        self.print_iterations()
        self.print_profile()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    api = WebAPI()
    api.url = 'http://block.arch.ethz.ch/api/brg_private/tna.py'

    print api.test()
    print api.info()
    print

    for method in api.list_methods():
        print method
        sig = api.method_signature(method)
        print 'args:', sig[0]
        print 'kwargs:', sig[1]
        print
        print api.method_help(method)
        print
