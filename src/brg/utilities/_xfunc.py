"""This module ...

..  Copyright 2014 BLOCK Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        `http://www.apache.org/licenses/LICENSE-2.0`_

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

.. TODO: make script server about running local scripts in cpython
.. TODO: move webfunc to API class definition

"""

import os
import json

from subprocess import Popen
from subprocess import PIPE


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Mar 5, 2015'
__contact__    = '''ETH Zurich,
Institute for Technology in Architecture,
BLOCK Research Group,
Stefano-Franscini-Platz 5,
HIL H 47,
8093 Zurich, Switzerland
'''


wrapper = """
import os
import sys
import importlib

import json
import cStringIO
import cProfile
import pstats

basedir  = sys.argv[1]
funcname = sys.argv[2]
args     = sys.argv[3]
kwargs   = sys.argv[4]

args     = json.loads(args)
kwargs   = json.loads(kwargs)

profile = cProfile.Profile()
profile.enable()

sys.path.insert(0, basedir)
parts = funcname.split('.')

if len(parts) > 1:
    m = importlib.import_module('.'.join(parts[:-1]))
    f = getattr(m, parts[-1])
    r = f(*args, **kwargs)
    print
    print '## RESULT ##'
    print
    print json.dumps(r)
else:
    m = importlib.import_module(parts[0])
    f = getattr(m, parts[0])
    r = f(*args, **kwargs)
    print
    print '## RESULT ##'
    print
    print json.dumps(r)

profile.disable()

stream = cStringIO.StringIO()
stats  = pstats.Stats(profile, stream=stream)
stats.strip_dirs()
stats.sort_stats(1)
stats.print_stats(20)

print
print '## PROFILE ##'
print
print stream.getvalue()
"""


def xecute(funcname, basedir, *args, **kwargs):
    if not os.path.isdir(basedir):
        raise Exception('basedir is not a directory: %s' % basedir)
    mode = kwargs.get('mode', 0)
    try:
        del kwargs['mode']
    except KeyError:
        pass
    args_str = json.dumps(args)
    kwargs_str = json.dumps(kwargs)
    process_args = ['pythonw', '-u', '-c', wrapper, basedir, funcname, args_str, kwargs_str]
    process = Popen(process_args, stderr=PIPE, stdout=PIPE)
    lines = []
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.strip()
        lines.append(line)
        if mode:
            print line
    _, stderr = process.communicate()
    if stderr:
        raise Exception(stderr)
    return lines


class XFunc(object):
    def __init__(self, basedir, mode=0):
        self._basedir = None
        self.basedir  = basedir
        self.mode     = mode
        self.python   = 'pythonw'

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, basedir):
        if not os.path.isdir(basedir):
            raise Exception('basedir is not a directory: %s' % basedir)
        self._basedir = basedir

    def __call__(self, funcname, *args, **kwargs):
        kwargs['mode'] = self.mode
        return xecute(funcname, self.basedir, *args, **kwargs)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    here    = os.path.dirname(__file__)
    basedir = os.path.abspath(os.path.join(here, '../../'))

    xfunc = XFunc(basedir, mode=0)

    res = xfunc('brg.datastructures.geometric_key', [0.1, 0.001, 0.3])

    for r in res:
        print r
