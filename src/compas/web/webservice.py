import os
import json

import cProfile
import cStringIO
import pstats
import traceback
import inspect


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'Dispatcher',
    'list_methods_wrapper',
    'method_help_wrapper',
    'method_signature_wrapper',
    'test_connection'
]


class Dispatcher(object):
    """"""

    def _dispatch(self, name, args):
        try:
            method = getattr(self, name)
        except AttributeError:
            return 'The requested method is not part of the API: {0}.'.format(name)
        try:
            idict = json.loads(args[0])
        except (IndexError, TypeError):
            return """
API methods require a single JSON encoded dictionary as input.
For example: input = json.dumps({'param_1': 1, 'param_2': [2, 3]})
"""
        odict = self._call_wrapped(method, idict)
        return json.dumps(odict)

    def _call_wrapped(self, method, idict):
        odict = {}
        try:
            profile = cProfile.Profile()
            profile.enable()
            # profiler enabled
            data, iterations = method(idict)
            # profiler disabled
            profile.disable()
            stream = cStringIO.StringIO()
            stats = pstats.Stats(profile, stream=stream)
            stats.strip_dirs()
            stats.sort_stats(1)
            stats.print_stats(20)
            odict['data']       = data
            odict['error']      = None
            odict['iterations'] = iterations
            odict['profile']    = stream.getvalue()
        except:
            odict['data']       = None
            odict['error']      = traceback.format_exc()
            odict['iterations'] = None
            odict['profile']    = None
        return odict


def test_connection():
    """Return a message containing the client's IP address."""
    return 'You have reached our server from IP {0}'.format(os.environ['REMOTE_ADDR'])


def list_methods_wrapper(dispatcher):
    def list_methods():
        def is_public_method(member):
            return inspect.ismethod(member) and not member.__name__.startswith('_')
        members = inspect.getmembers(dispatcher, is_public_method)
        return [member[0] for member in members]
    return list_methods


def method_help_wrapper(dispatcher):
    def method_help(name):
        if not hasattr(dispatcher, name):
            return 'Not a registered API method: {0}'.format(name)
        method = getattr(dispatcher, name)
        return inspect.getdoc(method)
    return method_help


def method_signature_wrapper(dispatcher):
    def method_signature(name):
        if not hasattr(dispatcher, name):
            return 'Not a registered API method: {0}'.format(name)
        method = getattr(dispatcher, name)
        spec = inspect.getargspec(method)
        args = spec.args
        defaults = spec.defaults
        return args[1:], defaults
    return method_signature


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
