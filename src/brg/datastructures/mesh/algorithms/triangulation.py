"""This module defines algorithms for generating triangulations."""

from numpy import asarray
from scipy.spatial import Delaunay

from brg.datastructures.mesh.mesh import Mesh


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


def delaunay_from_mesh(mesh):
    """Return a Delaunay triangulation from a given mesh.

    Parameters:
        mesh (brg.datastructures.mesh.Mesh) :
            The original mesh.

    Returns:
        mesh :
            ...

    >>> ...

    """
    d = Delaunay(mesh.xy)
    return Mesh.from_vertices_and_faces(mesh.xyz, d.simplices)


def delaunay_from_points(points):
    """"""
    xyz = asarray(points)
    assert 2 <= xyz.shape[1], "At least xy xoordinates required."
    d = Delaunay(xyz[:, 0:2])
    return Mesh.from_vertices_and_faces(points, d.simplices)


# @see: _scripts
def delaunay_from_boundary(boundary):
    """"""
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    dmesh = delaunay_from_mesh(mesh)

    vlabel = dict((key, key) for key in dmesh)
    flabel = dict((fkey, fkey) for fkey in dmesh.face)

    dmesh.draw(vertex_label=vlabel,
               face_label=flabel,
               vertex_size=None,
               show_vertices=True,
               show_faces=True)
