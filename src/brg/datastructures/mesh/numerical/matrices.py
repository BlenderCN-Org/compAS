""""""

__author__ = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, BRG - ETH Zurich',
__license__ = 'MIT'
__email__ = 'vanmelet@ethz.ch'


def connectivity_matrix(mesh):
    raise NotImplementedError


# see __snippets/algos/heat for cotangent weights
# ony for tri meshes though
def laplacian_matrix(mesh):
    raise NotImplementedError


def adjacency_matrix(mesh):
    raise NotImplementedError
