from numpy import set_printoptions


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


__all__ = [
    'set_array_print_precision',
    'unset_array_print_precision',
]


OLD_SETTINGS = None
FLOAT_PRECISION = '2f'


# http://stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
# float_formatter = lambda x: '%.2f' % x
def float_formatter(x):
    return '{0:+.{1}}'.format(x, FLOAT_PRECISION)


# http://stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
# set_printoptions(formatter={'float_kind': float_formatter})
def set_array_print_precision(precision='2f'):
    global FLOAT_PRECISION
    FLOAT_PRECISION = precision
    set_printoptions(formatter={'float_kind': float_formatter})


def unset_array_print_precision():
    set_printoptions(formatter=None)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
