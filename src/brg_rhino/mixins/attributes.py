from brg_rhino.mixins import Mixin

from brg_rhino.helpers.network import update_network_attributes
from brg_rhino.helpers.network import update_network_vertex_attributes
from brg_rhino.helpers.network import update_network_edge_attributes
from brg_rhino.helpers.network import update_network_face_attributes


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['UpdateMeshAttributes', 'UpdateNetworkAttributes', ]


class UpdateMeshAttributes(Mixin):
    """"""

    pass


class UpdateNetworkAttributes(Mixin):
    """"""

    update_attributes = update_network_attributes
    update_vertex_attributes = update_network_vertex_attributes
    update_edge_attributes = update_network_edge_attributes
    update_face_attributes = update_network_face_attributes


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    mixin = UpdateNetworkAttributes()

    print mixin.update_vertex_attributes.im_self
    print mixin.update_vertex_attributes.im_class
