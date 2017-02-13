from brg_rhino.mixins import Mixin

from brg_rhino.helpers.network import select_network_vertices
from brg_rhino.helpers.network import select_network_vertex
from brg_rhino.helpers.network import select_network_edges
from brg_rhino.helpers.network import select_network_edge
from brg_rhino.helpers.network import select_network_faces
from brg_rhino.helpers.network import select_network_face


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MeshSelect', 'NetworkSelect', ]


class MeshSelect(Mixin):
    """"""

    pass


class NetworkSelect(Mixin):
    """"""

    select_vertex   = select_network_vertex
    select_vertices = select_network_vertices
    select_edge     = select_network_edge
    select_edges    = select_network_edges
    select_face     = select_network_face
    select_faces    = select_network_faces


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
