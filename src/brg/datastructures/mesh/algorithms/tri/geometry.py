"""brg.datastructures.mesh.algorithms.geometry: Compute geometric properties of a mesh."""


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


# @see: __temp/scripts/compute_isolines.py
# contours := isolines of heightfield
def mesh_compute_contours(mesh, n=10):
    raise NotImplementedError


# @see: __temp/scripts/compute_isolines.py
def mesh_compute_isolines(mesh, n=10):
    raise NotImplementedError


# @see: __temp/scripts/compute_gradient.py
def mesh_compute_gradient(mesh):
    raise NotImplementedError


def mesh_compute_curvature(mesh):
    raise NotImplementedError


def mesh_planarize(mesh):
    raise NotImplementedError


def mesh_circularize(mesh):
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
