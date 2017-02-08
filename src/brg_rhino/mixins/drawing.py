from brg_rhino.mixins import Mixin

from brg_rhino.helpers.mesh import draw_mesh


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['MeshDrawing', 'NetworkDrawing', ]


class MeshDrawing(Mixin):
    """"""

    draw = draw_mesh


class NetworkDrawing(Mixin):
    """"""

    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
