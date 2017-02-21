__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'join_edges_network',
]


def join_edges_network(network, ab, cd):
    """Join two edges of a network.
    """
    intersection = set(ab) & set(cd)
    if not intersection:
        raise Exception('The edges are not connected.')
    a, b = ab
    c, d = cd
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
