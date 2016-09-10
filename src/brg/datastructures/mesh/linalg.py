from brg.numerical.matrices import connectivity_matrix

__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2015-12-04 08:56:24'


def mesh_connectivity_matrix(mesh, key_index=None):
    key_index = key_index or dict((key, index) for index, key in mesh.edges_enum())
    edges = [(key_index[u], key_index[v]) for u, v in mesh.edges_iter()]
    return connectivity_matrix(edges)
