"""brg.numerical.methods.result : A Class to store numerical method results."""

__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__author__     = ['Tom Van Mele vanmelet@ethz.ch']


class Result(object):
    """Creates a Results class to store numerical methods output.

    Parameters:
        xyz (array): Spatial co-ordinates of the nodes (n x 3).
        q (array): Force densities of the edges (m x 1) or (m, ).
        f (array): Forces in the edges (m x 1) or (m, ).
        l (array): Edge lengths (m x 1) or (m, ).
        r (array): Residual forces at the nodes (n x 3).

    Returns:
        obj: Results class with data as lists.

    """
    def __init__(self, xyz, q, f, l, r=None):
        self.xyz = xyz.tolist()
        self.q   = q.flatten().tolist()
        self.f   = f.flatten().tolist()
        self.l   = l.flatten().tolist()
        if r is not None:
            self.r = r.tolist()
        else:
            self.r = None


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
