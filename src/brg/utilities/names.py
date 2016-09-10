import random
import string


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Jun 19, 2015'


def rname(n=17):
    return ''.join(random.choice(string.lowercase) for _ in range(n))
