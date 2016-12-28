"""The datastructures.

The BRG framework currently provides three types of datastructures:

- the mesh, implemented as a half-edge datastructure;
- the network, implemented as a graph; and
- the volumetric mesh, implemented as a half-plane datastructure.

"""

from brg.datastructures.mesh.mesh import Mesh
from brg.datastructures.network.network import Network
from brg.datastructures.volmesh.volmesh import VolMesh


docs = [
    {'mesh': []},
    {'network': []},
    {'volmesh': []},
]
