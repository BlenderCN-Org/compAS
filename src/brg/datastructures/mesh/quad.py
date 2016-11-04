"""This module defines the quadmesh class."""

from brg.datastructures.mesh.mesh import Mesh


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


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
        return super(QuadMesh, self).add_face(vertices, fkey=fkey)

    def is_extraordinary(self, key):
        return len(self.vertex_neighbours(key)) != 4


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from brg.datastructures.mesh.viewer import MeshViewer
    from brg.geometry.polyhedron import Polyhedron

    polyhedron = Polyhedron.generate(6)
    mesh = QuadMesh.from_vertices_and_faces(polyhedron.vertices, polyhedron.faces)

    viewer = MeshViewer(mesh, 800, 800)
    viewer.camera.zoom = 3.
    viewer.setup()
    viewer.show()
