"""brg.datastructures.mesh.algorithms.orientation: Algorithms related to mesh orientation and orientability."""


from brg.datastructures.traversal import bfs
from brg.utilities.profiling import print_profile


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


@print_profile
def mesh_unify_cycle_directions(mesh, root=None):
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters:
        root (str): The key of the root face. Defaults to None.

    Returns:
        None

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
    bfs(mesh.face_adjacency(), root, unify)
    mesh.halfedge = dict((key, {}) for key in mesh.vertices_iter())
    for fkey, face in mesh.face.iteritems():
        for u, v in face.iteritems():
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


@print_profile
def mesh_flip_cycle_directions(mesh):
    """Flip the cycle directions of all faces.

    This function does not care about the directions being unified or not. It
    just reverses whatever direction it finds.

    Returns:
        None
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

    import brg
    from brg.datastructures.mesh.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces_big.obj'))

    # for flip in mesh.face:
    #     mesh.face[flip] = dict((v, u) for u, v in mesh.face[flip].items())
    #     break

    mesh_unify_cycle_directions(mesh)

    print mesh

    # print flip

    # for u, v in mesh.face[flip].items():
    #     if v in mesh.halfedge and u in mesh.halfedge[v]:
    #         fkey = mesh.halfedge[v][u]
    #         if fkey != flip:
    #             print 'not flipped', fkey
    #         else:
    #             print 'flipped', fkey
    #     elif u in mesh.halfedge and v in mesh.halfedge[u]:
    #         fkey = mesh.halfedge[u][v]
    #         if fkey != flip:
    #             print 'flipped', fkey
    #         else:
    #             print 'not flipped', fkey
    #     else:
    #         pass

    # vertex_label = dict((key, key) for key in mesh)
    # face_label = dict((fkey, fkey) for fkey in mesh.face)

    # mesh.plot(
    #     # show_vertices=True,
    #     # face_label=face_label
    # )
