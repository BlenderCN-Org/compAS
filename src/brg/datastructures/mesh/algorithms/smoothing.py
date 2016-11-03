__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


# to add:
# - laplacian area smoothing
# - laplacian cotangent smoothing
def mesh_smooth(mesh, k=1, d=0.5):
    """Smoothen the input mesh by moving each vertex to the centroid of its
    neighbours.

    Note:
        This is a node-per-node version of Laplacian smoothing with umbrella weights.

    Parameters:
        k (int): The number of smoothing iterations.
            Defaults to `1`.
        d (float): Scale factor for (i.e. damping of) the displacement vector.
            Defaults to `0.5`.

    Returns:
        None
    """
    def centroid(points):
        p = len(points)
        return [coord / p for coord in map(sum, zip(*points))]
    boundary = set(mesh.vertices_on_boundary())
    for _ in range(k):
        key_xyz = dict((key, (attr['x'], attr['y'], attr['z'])) for key, attr in mesh.vertices_iter(True))
        for key in key_xyz:
            if key in boundary:
                continue
            nbrs       = mesh.vertex_neighbours(key)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = centroid(points)
            x, y, z    = key_xyz[key]
            tx, ty, tz = d * (cx - x), d * (cy - y), d * (cz - z)
            mesh.vertex[key]['x'] += tx
            mesh.vertex[key]['y'] += ty
            mesh.vertex[key]['z'] += tz


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
