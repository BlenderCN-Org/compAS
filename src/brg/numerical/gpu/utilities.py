"""brg.numerical.gpu.utilities : Miscellaneous GPU functions."""

try:
    import pycuda
    import pycuda.autoinit
except ImportError as e:
    pass


__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__author__     = ['Andrew Liew <liew@arch.ethz.ch>']


def device():
    """ Displays the GPU CUDA device details.

    Parameters:
        None

    Returns:
        None

    Examples:
        >>> device()
        Device: GeForce GTX 980
        Compute Capability: 5.2
        Total Memory: 4194 MB
        CLOCK_RATE: 1266000
        ...
        MAX_BLOCK_DIM_X: 1024
        MAX_BLOCK_DIM_Y: 1024
        MAX_BLOCK_DIM_Z: 64
        ...etc
     """
    pycuda.driver.init()
    dev = pycuda.driver.Device(0)
    print('Device: ' + dev.name())
    print('Compute Capability: %d.%d' % dev.compute_capability())
    print('Total Memory: %s MB' % (dev.total_memory()//(1024000)))
    atts = [(str(att), value) for att, value in dev.get_attributes().items()]
    atts.sort()
    for att, value in atts:
        print('%s: %s' % (att, value))
