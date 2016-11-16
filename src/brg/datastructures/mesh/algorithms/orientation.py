from brg.datastructures.traversal import bfs

__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


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
                    mesh.face[nbr] = dict((v, u) for u, v in mesh.face[nbr].iteritems())
                    return
    if root is None:
        root = mesh.face.iterkeys().next()
    bfs(mesh.face_adjacency(), root, unify)
    mesh.halfedge = dict((key, {}) for key in mesh.vertices_iter())
    for fkey, face in mesh.face.iteritems():
        for u, v in face.iteritems():
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


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

    import cStringIO
    import cProfile
    import pstats

    import brg
    from brg.datastructures.mesh.mesh import Mesh

    profile = cProfile.Profile()
    profile.enable()

    mesh = Mesh.from_obj(brg.get_data('faces_big.obj'))
    mesh_unify_cycle_directions(mesh)

    profile.disable()

    stream = cStringIO.StringIO()
    stats  = pstats.Stats(profile, stream=stream)
    stats.strip_dirs()
    stats.sort_stats(1)
    stats.print_stats(20)

    print stream.getvalue()
