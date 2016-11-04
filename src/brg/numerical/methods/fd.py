"""brg.numerical.methods.fd : The force-density method."""

from numpy import array

from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from brg.numerical.matrices import connectivity_matrix
from brg.numerical.linalg import normrow

from result import Result


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


def fd(vertices, edges, fixed, q, loads):
    """Force-density numerical method.

    Parameters:
        vertices (list): Vertices' x, y and z co-ordinates.
        edges (list): Connectivity information of edges
        fixed (list): Indices of vertices fixed from spatial translations.
        q (list): Force densities of edges.
        loads (list): Point loads (px, py, pz) applied to vertices.

    Returns:
        obj: Result class of output data.
    """
    num_v     = len(vertices)
    free      = list(set(range(num_v)) - set(fixed))
    xyz       = array(vertices, dtype=float).reshape((-1, 3))
    q         = array(q, dtype=float).reshape((-1, 1))
    p         = array(loads, dtype=float).reshape((-1, 3))
    C         = connectivity_matrix(edges, 'csr')
    Ci        = C[:, free]
    Cf        = C[:, fixed]
    Ct        = C.transpose()
    Cit       = Ci.transpose()
    Q         = diags([q.flatten()], [0])
    A         = Cit.dot(Q).dot(Ci)
    b         = p[free] - Cit.dot(Q).dot(Cf).dot(xyz[fixed])
    xyz[free] = spsolve(A, b)
    l         = normrow(C.dot(xyz))
    f         = q * l
    r         = p - Ct.dot(Q).dot(C).dot(xyz)
    return Result(xyz, q, f, l, r)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg

    # from brg.datastructures.network.network import Network

    # network = Network.from_obj(brg.get_data('lines.obj'))

    # network.set_dva({'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
    # network.set_dea({'q': 1.0})

    # for key in network:
    #     network.vertex[key]['is_anchor'] = network.is_vertex_leaf(key)

    # for index, u, v, attr in network.edges_enum(True):
    #     network.edge[u][v]['q'] = float(index)

    # k_i   = dict((k, i) for i, k in network.vertices_enum())
    # xyz   = network.get_vertices_attributes(('x', 'y', 'z'))
    # loads = network.get_vertices_attributes(('px', 'py', 'pz'))
    # fixed = [k_i[key] for key in network if network.vertex[key]['is_anchor']]
    # edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]
    # q     = network.get_edges_attribute('q')
    # res   = fd(xyz, edges, fixed, q, loads)

    # for key in network:
    #     index = k_i[key]
    #     network.vertex[key]['x'] = res.xyz[index][0]
    #     network.vertex[key]['y'] = res.xyz[index][1]
    #     network.vertex[key]['z'] = res.xyz[index][2]

    # network.draw(vcolor=dict((key, '#ff0000') for key in network if network.vertex[key]['is_anchor']))

    from brg.datastructures.mesh.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    mesh.set_dva({'is_anchor': False})
    mesh.set_dea({'q': 1.0})

    for key in mesh:
        mesh.vertex[key]['is_anchor'] = mesh.vertex_degree(key) == 2

    # for index, (u, v, attr) in mesh.edges_enum(True):
    #     mesh.edge[u][v]['q'] = float(index)

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

    mesh.draw(vertex_color=dict((key, '#ff0000') for key in mesh if mesh.vertex[key]['is_anchor']))
