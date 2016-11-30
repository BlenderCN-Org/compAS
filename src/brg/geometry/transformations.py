from brg.geometry.functions import length


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 3, 2014'


def translate():
    raise NotImplementedError


def rotate():
    raise NotImplementedError


def normalize(vector):
    """normalizes a vector

    Parameters:
        v1 (tuple, list, Vector): The vector.

    Returns:
        Tuple: normalized vector
    """
    l = float(length(vector))
    if l <= 0:
        l = 1e-9
    return vector[0] / l, vector[1] / l, vector[2] / l


def scale(vector, f):
    """Scales vector by factor

    Parameters:
        vector (tuple, list, Vector): The vector
        f (float): scale factor

    Returns:
        Tuple: Scaled vector
    """
    return vector[0] * f, vector[1] * f, vector[2] * f


def mirror():
    pass


def project():
    pass


def skew():
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
