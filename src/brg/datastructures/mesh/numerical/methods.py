"""High-level interfaces to numerical methods for meshes."""


from brg.numerical.methods.fd import fd


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


def mesh_fd(mesh):
    k_i   = dict((k, i) for i, k in mesh.vertices_enum())
    xyz   = mesh.get_vertices_attributes(('x', 'y', 'z'))
    loads = mesh.get_vertices_attributes(('px', 'py', 'pz'), 0.0)
    fixed = [k_i[key] for key in mesh if mesh.vertex[key]['is_anchor']]
    edges = [(k_i[u], k_i[v]) for u, v in mesh.edges_iter()]
    q     = mesh.get_edges_attribute('q')
    res   = fd(xyz, edges, fixed, q, loads)

    for key in mesh:
        index = k_i[key]
        mesh.vertex[key]['x'] = res.xyz[index][0]
        mesh.vertex[key]['y'] = res.xyz[index][1]
        mesh.vertex[key]['z'] = res.xyz[index][2]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg

    from brg.datastructures.mesh.mesh import Mesh
    from brg.datastructures.mesh.viewer import MeshViewer

    mesh = Mesh.from_obj(brg.find_resource('faces.obj'))

    mesh.set_dva({'is_anchor': False})
    mesh.set_dea({'q': 1.0})

    for key in mesh:
        mesh.vertex[key]['is_anchor'] = mesh.vertex_degree(key) == 2

    mesh_fd(mesh)

    viewer = MeshViewer(mesh, 800, 600)
    viewer.grid_on = False
    viewer.camera.zoom = 10
    viewer.setup()
    viewer.show()
