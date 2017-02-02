__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'planarize_mesh',
    'circularize_mesh',
    'mesh_contours',
    'mesh_isolines',
    'mesh_gradient',
    'mesh_curvature',
]


def planarize_mesh(mesh):
    raise NotImplementedError


def circularize_mesh(mesh):
    raise NotImplementedError


# @see: __temp/scripts/compute_isolines.py
# contours := isolines of heightfield
def mesh_contours(mesh, n=10):
    raise NotImplementedError


# @see: __temp/scripts/compute_isolines.py
def mesh_isolines(mesh, n=10):
    raise NotImplementedError


# @see: __temp/scripts/compute_gradient.py
def mesh_gradient(mesh):
    raise NotImplementedError


def mesh_curvature(mesh):
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
