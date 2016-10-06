"""This module ...


..  Copyright 2014 BLOCK Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        `http://www.apache.org/licenses/LICENSE-2.0`_

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

from brg.datastructures.mesh.mesh import Mesh


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 10, 2014'


class QuadMesh(Mesh):
    """"""

    def add_face(self, vertices, fkey=None):
        """Add a face to the mesh.

        The number of vertices of the face should be three or four. In this
        count the last vertex is ignored if it is the same as the first.

        Parameters:
            vertices (list): The vertices of the face.

        Returns:
            str: The key of the added face.

        Raises:
            MeshError: If the number of vertices exceeds four.
        """
        if vertices[-1] == vertices[0]:
            del vertices[-1]
        if len(vertices) > 4:
            raise Exception('The face has too many vertices: {0}'.format(vertices))
        super(QuadMesh, self).add_face(vertices, fkey=fkey)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from brg.viewers.mesh import MeshViewer
    from brg.geometry.polyhedron import Polyhedron

    polyhedron = Polyhedron.generate(6)
    mesh = QuadMesh(polyhedron.vertices, polyhedron.faces)

    viewer = MeshViewer(mesh, 800, 800)
    viewer.camera.zoom = 3.
    viewer.setup()
    viewer.show()
