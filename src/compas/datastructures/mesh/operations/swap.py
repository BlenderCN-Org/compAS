__author__    = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


def swap_edge_trimesh(mesh, u, v):
    """Replace an edge of the mesh by an edge connecting the opposite
    vertices of the adjacent faces.

    Parameters:
        u (str): The key of one of the vertices of the edge.
        v (str): The key of the other vertex of the edge.

    Returns:
        None

    Raises:
        ValueError: If `u` and `v` are not neighbours.
        TriMeshError: If one of the half-edges does not exist.
    """
    # check legality of the swap
    # swapping on the boundary is not allowed
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]
    if fkey_uv is None or fkey_vu is None:
        return
    # swapping to a half-edge that already exists is not allowed
    o_uv = mesh.face[fkey_uv][v]
    o_vu = mesh.face[fkey_vu][u]
    if o_uv in mesh.halfedge[o_vu] and o_vu in mesh.halfedge[o_uv]:
        return
    # swap
    # delete the current half-edge
    del mesh.halfedge[u][v]
    del mesh.halfedge[v][u]
    # delete the adjacent faces
    del mesh.face[fkey_uv]
    del mesh.face[fkey_vu]
    # add the faces created by the swap
    a = mesh.add_face([o_uv, o_vu, v])
    b = mesh.add_face([o_vu, o_uv, u])
    return a, b


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
