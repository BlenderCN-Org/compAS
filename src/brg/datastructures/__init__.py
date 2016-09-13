"""The datastructures.

The BRG framework currently provides three types of datastructures:

- the mesh, implemented as a half-edge datastructure;
- the network, implemented as a graph; and
- the volumetric mesh, implemented as a half-plane datastructure.

"""

import mesh
import network
import volmesh

from mesh.mesh import Mesh
from mesh.tri.mesh import TriMesh
from mesh.quad.mesh import QuadMesh

from network.network import Network

from volmesh.volmesh import VolMesh


__all__ = [
    'mesh',
    'network',
    'volmesh',
]
