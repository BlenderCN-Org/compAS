from numpy import array

from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from brg.numerical.matrices import connectivity_matrix
from brg.numerical.linalg import normrow


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


def fd(vertices, edges, fixed, q, loads):
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
    return xyz, q, f, l, r


def fd_xfunc(vertices, edges, fixed, q, loads):
    xyz, q, f, l, r = fd(vertices, edges, fixed, q, loads)
    return {
        'xyz': xyz.tolist(),
        'q'  : q.ravel().tolist(),
        'f'  : f.ravel().tolist(),
        'l'  : l.ravel().tolist(),
        'r'  : r.tolist()
    }


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg

    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('saddle.obj'))

    network.set_dva({'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
    network.set_dea({'q': 1.0})

    for key in network:
        network.vertex[key]['is_anchor'] = network.is_vertex_leaf(key)

    k_i   = network.key_index()
    xyz   = network.get_vertices_attributes(('x', 'y', 'z'))
    loads = network.get_vertices_attributes(('px', 'py', 'pz'))
    q     = network.get_edges_attribute('q')

    fixed = [k_i[k] for k in network if network.vertex[k]['is_anchor']]
    edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]

    xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads)

    for key in network:
        index = k_i[key]
        network.vertex[key]['x'] = xyz[index][0]
        network.vertex[key]['y'] = xyz[index][1]
        network.vertex[key]['z'] = xyz[index][2]

    # from brg.datastructures.mesh.mesh import Mesh

    # mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    # mesh.set_dva({'is_anchor': False})
    # mesh.set_dea({'q': 1.0})

    # for key in mesh:
    #     mesh.vertex[key]['is_anchor'] = mesh.vertex_degree(key) == 2

    # # for index, (u, v, attr) in mesh.edges_enum(True):
    # #     mesh.edge[u][v]['q'] = float(index)

    # k_i   = dict((k, i) for i, k in mesh.vertices_enum())
    # xyz   = mesh.get_vertices_attributes(('x', 'y', 'z'))
    # loads = mesh.get_vertices_attributes(('px', 'py', 'pz'), 0.0)
    # fixed = [k_i[key] for key in mesh if mesh.vertex[key]['is_anchor']]
    # edges = [(k_i[u], k_i[v]) for u, v in mesh.edges_iter()]
    # q     = mesh.get_edges_attribute('q')
    # xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads)

    # for key in mesh:
    #     index = k_i[key]
    #     mesh.vertex[key]['x'] = xyz[index][0]
    #     mesh.vertex[key]['y'] = xyz[index][1]
    #     mesh.vertex[key]['z'] = xyz[index][2]

    # mesh.plot(
    #     vcolor={key: '#ff0000' for key in mesh if mesh.vertex[key]['is_anchor']}
    # )
