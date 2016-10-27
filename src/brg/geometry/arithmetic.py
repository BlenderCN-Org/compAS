__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 3, 2014'


docs = [
    'add_vectorlist',
    'add_vectors',
    'subtract_vectors',
]


def add_vectorlist(vectors):
    """Adds multiple 3d vectors

    Parameters:
       vectors (list): set of vectors.

    Returns:
       Tuple: Resulting vector
    """
    x = sum([x[0] for x in vectors])
    y = sum([y[1] for y in vectors])
    z = sum([z[2] for z in vectors])
    return (x, y, z)


def add_vectors(v1, v2):
    """Adds two 3d vectors

    Parameters:
        v1 (tuple, list, Vector): The first vector.
        v2 (tuple, list, Vector): The second vector.

    Returns:
        Tuple: Resulting vector
    """
    return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]


def subtract_vectors(v1, v2):
    """Subtracts the second vector from the first.

    Parameters:
        v1 (tuple, list, Vector): The first vector.
        v2 (tuple, list, Vector): The second vector.

    Returns:
        Tuple: Resulting vector
    """
    return v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
