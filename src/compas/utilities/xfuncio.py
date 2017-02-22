import os
import json

from subprocess import Popen
from subprocess import PIPE

from functools import wraps


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['xecuteio', 'XFuncIO']


WRAPPER = """
import sys
import importlib

import json
import cStringIO
import cProfile
import pstats
import traceback
from json import encoder


basedir  = sys.argv[1]
funcname = sys.argv[2]
ipath    = sys.argv[3]
opath    = sys.argv[4]

with open(ipath, 'rb') as fp:
    idict = json.load(fp)

try:
    args   = idict['args']
    kwargs = idict['kwargs']

    profile = cProfile.Profile()
    profile.enable()

    # sys.path.insert(0, basedir)
    parts = funcname.split('.')

    if len(parts) > 1:
        mname = '.'.join(parts[:-1])
        fname = parts[-1]
        m = importlib.import_module(mname)
        f = getattr(m, fname)
    else:
        m = importlib.import_module(parts[0])
        f = getattr(m, parts[0])

    r = f(*args, **kwargs)

    profile.disable()

    stream = cStringIO.StringIO()
    stats  = pstats.Stats(profile, stream=stream)
    stats.strip_dirs()
    stats.sort_stats(1)
    stats.print_stats(20)

except:
    odict = {}
    odict['error']      = traceback.format_exc()
    odict['data']       = None
    odict['iterations'] = None
    odict['profile']    = None

else:
    odict = {}
    odict['error']      = None
    odict['data']       = r
    odict['iterations'] = None
    odict['profile']    = stream.getvalue()

e_frepr = encoder.FLOAT_REPR
encoder.FLOAT_REPR = lambda o: format(o, '.16g')

with open(opath, 'wb+') as fp:
    json.dump(odict, fp)

encoder.FLOAT_REPR = e_frepr
"""


def run_as_xfunc(basedir, tmpdir):
    def decorator(func):
        @wraps
        def wrapper(*args, **kwargs):
            # stuff before
            res = func()
            # stuff after
            return res
        return wrapper
    return decorator


def xecuteio(funcname, basedir, tmpdir, *args, **kwargs):
    # if not os.path.isdir(basedir):
    #     raise Exception('basedir is not a directory: %s' % basedir)
    if not os.path.isdir(tmpdir):
        raise Exception('tmpdir is not a directory: %s' % tmpdir)
    if not os.access(tmpdir, os.W_OK):
        raise Exception('you do not have write access to tmpdir')

    mode = kwargs.get('mode', 0)

    try:
        del kwargs['mode']
    except KeyError:
        pass

    ipath = os.path.join(tmpdir, '%s.in' % funcname)
    opath = os.path.join(tmpdir, '%s.out' % funcname)

    idict = {'args': args, 'kwargs': kwargs}

    # e_frepr = encoder.FLOAT_REPR
    # encoder.FLOAT_REPR = lambda o: format(o, '.16g')

    with open(ipath, 'wb+') as fh:
        json.dump(idict, fh)

    with open(opath, 'wb+') as fh:
        fh.write('')

    # encoder.FLOAT_REPR = e_frepr

    process_args = ['pythonw', '-u', '-c', WRAPPER, basedir, funcname, ipath, opath]
    process = Popen(process_args, stderr=PIPE, stdout=PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.strip()
        if mode:
            print(line)
    _, stderr = process.communicate()

    if stderr:
        odict = {'error'     : stderr,
                 'data'      : None,
                 'iterations': None,
                 'profile'   : None}
    else:
        with open(opath, 'rb') as fh:
            odict = json.load(fh)

    return odict


class XFuncIO(object):
    def __init__(self, basedir='.', tmpdir='.', mode=0):
        self._basedir   = None
        self._tmpdir    = None
        self.basedir    = basedir
        self.tmpdir     = tmpdir
        self.mode       = mode
        self.python     = 'pythonw'
        self.data       = None
        self.iterations = None
        self.profile    = None
        self.error      = None

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, basedir):
        # if not os.path.isdir(basedir):
        #     raise Exception('basedir is not a directory: %s' % basedir)
        self._basedir = basedir

    @property
    def tmpdir(self):
        return self._tmpdir

    @tmpdir.setter
    def tmpdir(self, tmpdir):
        if not os.path.isdir(tmpdir):
            raise Exception('tmpdir is not a directory: %s' % tmpdir)
        if not os.access(tmpdir, os.W_OK):
            raise Exception('you do not have write access to tmpdir')
        self._tmpdir = tmpdir

    def __call__(self, funcname, *args, **kwargs):
        kwargs['mode'] = self.mode
        odict = xecuteio(funcname, self.basedir, self.tmpdir, *args, **kwargs)
        self.data       = odict['data']
        self.profile    = odict['profile']
        self.iterations = odict['iterations']
        self.error      = odict['error']


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    xfunc = XFuncIO(mode=1)

    xfname = 'compas.utilities.animation.test'

    xfunc(xfname)

    print(xfunc.data)
    print(xfunc.error)
    print(xfunc.profile)
