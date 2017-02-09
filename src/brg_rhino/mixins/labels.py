from brg_rhino.mixins import Mixin

from brg_rhino.helpers.network import display_network_vertex_labels
from brg_rhino.helpers.network import display_network_edge_labels
from brg_rhino.helpers.network import display_network_face_labels


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['DisplayMeshLabels', 'DisplayNetworkLabels', ]


class DisplayMeshLabels(Mixin):
    """"""

    pass


class DisplayNetworkLabels(Mixin):
    """"""

    display_vertex_labels = display_network_vertex_labels
    display_edge_labels = display_network_edge_labels
    display_face_labels = display_network_face_labels


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
