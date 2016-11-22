# -*- coding: utf-8 -*-

from math import cos
from math import pi
from brg.datastructures.mesh.operations.split import split_edge

__author__ = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, BRG - ETH Zurich'
__license__ = 'MIT'
__email__ = 'vanmelet@ethz.ch'


def loop_subdivision(mesh, k=1, fixed=None):
    if not fixed:
        fixed = []

    fixed = set(fixed)
    subd = mesh.copy()

    for _ in range(k):
        key_xyz       = dict((key, subd.vertex_coordinates(key)) for key in subd)
        fkey_vertices = dict((fkey, subd.face_vertices(fkey, ordered=True)) for fkey in subd.face)
        uv_w          = dict(((u, v), subd.face[subd.halfedge[u][v]][v]) for u in subd.halfedge for v in subd.halfedge[u])
        edgepoints    = dict()

        for key in subd:
            nbrs = subd.vertex_neighbours(key)
            n = len(nbrs)
            if n == 3:
                a = 3. / 16.
            else:
                a = (5. / 8. - (3. / 8. + 0.25 * cos(2 * pi / n)) ** 2) / n
            nbrs = [key_xyz[nbr] for nbr in nbrs]
            nbrs = [sum(axis) for axis in zip(*nbrs)]
            xyz = key_xyz[key]
            xyz = [(1. - n * a) * xyz[i] + a * nbrs[i] for i in range(3)]
            subd.vertex[key]['x'] = xyz[0]
            subd.vertex[key]['y'] = xyz[1]
            subd.vertex[key]['z'] = xyz[2]

        for u, v in subd.edges():
            w = split_edge(subd, u, v)
            edgepoints[(u, v)] = w
            edgepoints[(v, u)] = w
            v1 = key_xyz[u]
            v2 = key_xyz[v]
            vl = key_xyz[uv_w[(u, v)]]
            vr = key_xyz[uv_w[(v, u)]]
            xyz = [3. * (v1[i] + v2[i]) / 8. + (vl[i] + vr[i]) / 8. for i in range(3)]
            subd.vertex[w]['x'] = xyz[0]
            subd.vertex[w]['y'] = xyz[1]
            subd.vertex[w]['z'] = xyz[2]

        for fkey, vertices in fkey_vertices.items():
            u, v, w = vertices
            uv = edgepoints[(u, v)]
            vw = edgepoints[(v, w)]
            wu = edgepoints[(w, u)]
            subd.add_face([wu, u, uv])
            subd.add_face([uv, v, vw])
            subd.add_face([vw, w, wu])
            subd.add_face([uv, vw, wu])
            del subd.face[fkey]

    return subd


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from brg.datastructures.mesh.tri import Mesh
    from brg.geometry.polyhedron import Polyhedron
    from brg.datastructures.mesh.viewer import SubdMeshViewer

    tet = Polyhedron.generate(4)

    mesh = Mesh.from_vertices_and_faces(tet.vertices, tet.faces)

    viewer = SubdMeshViewer(mesh, subdfunc=loop_subdivision)

    viewer.axes.x_color = (0.1, 0.1, 0.1)
    viewer.axes.y_color = (0.1, 0.1, 0.1)
    viewer.axes.z_color = (0.1, 0.1, 0.1)

    viewer.setup()
    viewer.show()
