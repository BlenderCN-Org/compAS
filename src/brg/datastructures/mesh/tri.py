
from brg.datastructures.mesh.mesh import Mesh


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 10, 2014'


class TriMeshError(Exception):
    pass


class TriMesh(Mesh):
    """Data structure for mesh with triangular faces.
    """

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
