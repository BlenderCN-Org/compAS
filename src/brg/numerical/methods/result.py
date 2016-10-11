__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Jul 8, 2015'


class Result():
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
