from __future__ import print_function

from compas.datastructures.network.algorithms import network_bfs


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'unify_cycles_mesh',
    'flip_cycles_mesh',
]


def unify_cycles_mesh(mesh, root=None):
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters:
        root (str): The key of the root face. Defaults to None.

    Raises:
        ValueError: If `direction` is not one of (None, `ccw`, `cw`)
    """
    def unify(node, nbr):
        for u, v in mesh.face[nbr].iteritems():
            if u in mesh.face[node]:
                if v == mesh.face[node][u]:
                    # if the traversal of a neighbouring halfedge
                    # is in the same direction
                    # flip the neighbour
                    mesh.face[nbr] = dict((v, u) for u, v in mesh.face[nbr].iteritems())
                    return
    if root is None:
        root = mesh.face.iterkeys().next()
    # pass unify as callback function
    # what about the return value?
    network_bfs(mesh.face_adjacency(), root, unify)
    mesh.halfedge = dict((key, {}) for key in mesh.vertices_iter())
    for fkey, face in mesh.face.iteritems():
        for u, v in face.iteritems():
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


def flip_cycles_mesh(mesh):
    """Flip the cycle directions of all faces.

    This function does not care about the directions being unified or not. It
    just reverses whatever direction it finds.

    """
    mesh.halfedge = dict((key, {}) for key in mesh.vertices_iter())
    for fkey, face in mesh.face.iteritems():
        mesh.face[fkey] = dict((nbr, key) for key, nbr in face.items())
        for u, v in face.iteritems():
            mesh.halfedge[v][u] = fkey
            if v not in mesh.halfedge[u]:
                mesh.halfedge[u][v] = None


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get_data('faces_big.obj'))

    unify_cycles_mesh(mesh)

    # run_profile(unify_mesh_cycles)(mesh)
    # profiled(unify_mesh_cycles)(mesh)

    print(mesh)
