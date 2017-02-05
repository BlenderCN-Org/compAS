from brg_rhino.mixins import Mixin

from brg_rhino.helpers.mesh import mesh_from_guid
from brg_rhino.helpers.mesh import mesh_from_surface
from brg_rhino.helpers.mesh import mesh_from_surface_uv
from brg_rhino.helpers.mesh import mesh_from_surface_heightfield


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['MeshConstructors', 'NetworkConstructors', ]


class MeshConstructors(Mixin):
    """"""

    from_guid = mesh_from_guid
    from_surface = mesh_from_surface
    from_surface_uv = mesh_from_surface_uv
    from_surface_heightfield = mesh_from_surface_heightfield


class NetworkConstructors(Mixin):
    """"""

    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
