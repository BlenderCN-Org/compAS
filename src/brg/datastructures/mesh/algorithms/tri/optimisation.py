from brg.datastructures.mesh.algorithms.optimisation import mesh_smooth

from brg.datastructures.mesh.algorithms.tri.split import split_edge
from brg.datastructures.mesh.algorithms.tri.collapse import collapse_edge
from brg.datastructures.mesh.algorithms.tri.swap import swap_edge

__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2015-12-04 16:10:59'


def remesh(mesh, target,
           tol=0.1, kmax=100,
           start=None, steps=None,
           verbose=False, allow_boundary=False,
           ufunc=None):
    """Remesh until all edges have a specified target length.

    This involves three operations:

        * split edges that are shorter than a minimum length,
        * collapse edges that are longer than a maximum length,
        * swap edges if this improves the valency error.

    The minimum and maximum lengths are calculated based on a desired target
    length:

    Parameters:
        target (float): The target length.
        tol (float): Length deviation tolerance. Defaults to `0.1`
        kmax (int): The number of iterations.
        verbose (bool): Print feedback messages, if True.

    Returns:
        None
    """
    def _remesh(target, kmax):
        if verbose:
            print
            print target
        lmin = (1 - tol) * (4.0 / 5.0) * target
        lmax = (1 + tol) * (4.0 / 3.0) * target
        boundary = set(mesh.vertices_on_boundary())
        count = 0
        for k in xrange(kmax):
            if verbose:
                print
                print k
            count += 1
            # split
            if count == 1:
                visited = set()
                has_split = False
                for u, v in mesh.edges():
                    # is this correct?
                    if u in visited or v in visited:
                        continue
                    l = mesh.edge_length(u, v)
                    if l <= lmax:
                        continue
                    if verbose:
                        print 'split edge: {0} - {1}'.format(u, v)
                    split_edge(mesh, u, v, allow_boundary=allow_boundary)
                    visited.add(u)
                    visited.add(v)
                    has_split = True
            # collapse
            elif count == 2:
                visited = set()
                has_collapsed = False
                for u, v in mesh.edges():
                    # is this correct?
                    if u in visited or v in visited:
                        continue
                    l = mesh.edge_length(u, v)
                    if l >= lmin:
                        continue
                    if verbose:
                        print 'collapse edge: {0} - {1}'.format(u, v)
                    collapse_edge(mesh, u, v)
                    visited.add(u)
                    visited.add(v)
                    for nbr in mesh.halfedge[u]:
                        visited.add(nbr)
                    has_collapsed = True
            # swap
            elif count == 3:
                visited = set()
                has_swapped = False
                for u, v in mesh.edges():
                    if u in visited or v in visited:
                        continue
                    f1 = mesh.halfedge[u][v]
                    f2 = mesh.halfedge[v][u]
                    if f1 is None or f2 is None:
                        continue
                    v1 = mesh.face[f1][v]
                    v2 = mesh.face[f2][u]
                    valency1 = mesh.vertex_degree(u)
                    valency2 = mesh.vertex_degree(v)
                    valency3 = mesh.vertex_degree(v1)
                    valency4 = mesh.vertex_degree(v2)
                    if u in boundary:
                        valency1 += 2
                    if v in boundary:
                        valency2 += 2
                    if v1 in boundary:
                        valency3 += 2
                    if v2 in boundary:
                        valency4 += 2
                    current_error = abs(valency1 - 6) + abs(valency2 - 6) + abs(valency3 - 6) + abs(valency4 - 6)
                    flipped_error = abs(valency1 - 7) + abs(valency2 - 7) + abs(valency3 - 5) + abs(valency4 - 5)
                    if current_error <= flipped_error:
                        continue
                    if verbose:
                        print 'swap edge: {0} - {1}'.format(u, v)
                    swap_edge(mesh, u, v)
                    visited.add(u)
                    visited.add(v)
                    has_swapped = True
            # count
            else:
                if not has_split and not has_collapsed and not has_swapped:
                    break
                count = 0
            # smoothen
            mesh_smooth(mesh, 1)
            if ufunc:
                ufunc(mesh)
    # remesh differently based on target specifications
    # if start and steps:
    #     step = (start - target) / float(steps)
    #     for i in range(steps + 1):
    #         target = start - i * step
    #         _remesh(target)
    #     smooth(mesh, 5)
    if start and steps:
        step = (start - target) / float(steps)
        kmax = max(int(kmax / float(steps)), 10)
        for i in range(steps + 1):
            target = start - i * step
            _remesh(target, kmax)
    else:
        _remesh(target, kmax)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import time

    from brg.datastructures import Mesh
    from brg.datastructures.mesh.drawing import draw_mesh

    vertices = [
        (0.0, 0.0, 0.0),
        (10.0, 0.0, 0.0),
        (10.0, 10.0, 0.0),
        (0.0, 10.0, 0.0),
        (5.0, 5.0, 0.0)
    ]

    faces = [
        ('0', '1', '4'),
        ('1', '2', '4'),
        ('2', '3', '4'),
        ('3', '0', '4')
    ]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    t0 = time.time()

    remesh(mesh, target=0.5, start=1.0, steps=10, tol=0.05, kmax=300, allow_boundary=True, verbose=False)

    t1 = time.time()

    print t1 - t0

    draw_mesh(mesh)
