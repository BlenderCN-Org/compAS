"""This module defines the trimesh class."""

from brg.geometry import dot
from brg.geometry import length
from brg.geometry import cross

from brg.datastructures.mesh.mesh import Mesh


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


class TriMesh(Mesh):
    """Data structure for mesh with triangular faces."""

    def add_face(self, vertices, fkey=None):
        """Add a face to the mesh.

        The number of vertices of the face should be exactly three. In this
        count the last vertex is ignored if it is the same as the first.

        Parameters:
            vertices (list): The vertices of the face.

        Returns:
            str: The key of the added face.

        Raises:
            MeshError: If the number of vertices is not exactly three.
        """
        if vertices[-1] == vertices[0]:
            del vertices[-1]
        if len(vertices) != 3:
            raise Exception('The face has too many vertices: {0}'.format(vertices))
        return super(TriMesh, self).add_face(vertices, fkey=fkey)

    def is_extraordinary(self, key):
        return len(self.vertex_neighbours(key)) != 6

    def edge_cotangent(self, u, v):
        fkey = self.halfedge[u][v]
        cotangent = 0.0
        if fkey is not None:
            w = self.face[fkey][v]  # self.vertex_descendent(v, fkey)
            wu = self.edge_vector(w, u)
            wv = self.edge_vector(w, v)
            cotangent = dot(wu, wv) / length(cross(wu, wv))
        return cotangent

    def edge_cotangents(self, u, v):
        a = self.edge_cotangent(u, v)
        b = self.edge_cotangent(v, u)
        return a, b


class PowerDiagram():
    pass


class DelaunayTriangulation():
    pass


class VoronoiDiagram():
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from brg.datastructures.mesh.viewer import MeshViewer
    from brg.geometry.polyhedron import Polyhedron

    polyhedron = Polyhedron.generate(4)
    mesh = TriMesh.from_vertices_and_faces(polyhedron.vertices, polyhedron.faces)

    viewer = MeshViewer(mesh, 800, 800)
    viewer.camera.zoom = 3.
    viewer.setup()
    viewer.show()
