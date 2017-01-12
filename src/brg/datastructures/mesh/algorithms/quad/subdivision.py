""""""

from brg.exceptions import MeshAlgorithmError


__author__    = 'Tom Van Mele, '
__copyright__ = 'Copyright 2016, BRG - ETH Zurich'
__license__   = 'MIT'
__email__     = 'vanmelet@ethz.ch'


# this was used as a basis for the implementation of doo-sabin
# and the update of catmull-clark
# don't use this for anything other then an example...
# this implementation assumes the mesh is closed
# when extraordinary vertices exist in the control mesh, any subd mesh has gas faces with more than 4 vertices
def quad_subdivision(mesh, k=1):
    c1 = 3. / 16.
    c2 = 9. / 16.
    c3 = 3. / 16.
    c4 = 1. / 16.
    cls = type(mesh)
    for _ in range(k):
        old_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        fkey_old_new = dict((fkey, {}) for fkey in mesh.face)
        subd = cls()
        for fkey in mesh.face:
            vertices = mesh.face_vertices(fkey, ordered=True)
            if len(vertices) != 4:
                raise MeshAlgorithmError
            o1 = old_xyz[vertices[0]]
            o2 = old_xyz[vertices[1]]
            o3 = old_xyz[vertices[2]]
            o4 = old_xyz[vertices[3]]
            n1 = [c1 * o4[i] + c2 * o1[i] + c3 * o2[i] + c4 * o3[i] for i in range(3)]
            n2 = [c1 * o1[i] + c2 * o2[i] + c3 * o3[i] + c4 * o4[i] for i in range(3)]
            n3 = [c1 * o2[i] + c2 * o3[i] + c3 * o4[i] + c4 * o1[i] for i in range(3)]
            n4 = [c1 * o3[i] + c2 * o4[i] + c3 * o1[i] + c4 * o2[i] for i in range(3)]
            a = subd.add_vertex(x=n1[0], y=n1[1], z=n1[2])
            b = subd.add_vertex(x=n2[0], y=n2[1], z=n2[2])
            c = subd.add_vertex(x=n3[0], y=n3[1], z=n3[2])
            d = subd.add_vertex(x=n4[0], y=n4[1], z=n4[2])
            fkey_old_new[fkey][vertices[0]] = a
            fkey_old_new[fkey][vertices[1]] = b
            fkey_old_new[fkey][vertices[2]] = c
            fkey_old_new[fkey][vertices[3]] = d
        for fkey in mesh.face:
            if len(vertices) != 4:
                raise MeshAlgorithmError
            vertices = mesh.face_vertices(fkey, ordered=True)
            old_new = fkey_old_new[fkey]
            subd.add_face([old_new[old] for old in vertices])
        for key in mesh.vertex:
            if mesh.is_vertex_on_boundary(key):
                continue
            face = []
            for nbr in mesh.vertex_neighbours(key, ordered=True):
                fkey = mesh.halfedge[key][nbr]
                if fkey is not None:
                    face.append(fkey_old_new[fkey][key])
            if len(face) > 2:
                subd.add_face(face[::-1])
        edges = set()
        for u in mesh.halfedge:
            for v in mesh.halfedge[u]:
                if (u, v) in edges:
                    continue
                edges.add((u, v))
                edges.add((v, u))
                uv_fkey = mesh.halfedge[u][v]
                vu_fkey = mesh.halfedge[v][u]
                if uv_fkey is None or vu_fkey is None:
                    continue
                face = []
                face.append(fkey_old_new[uv_fkey][u])
                face.append(fkey_old_new[vu_fkey][u])
                face.append(fkey_old_new[vu_fkey][v])
                face.append(fkey_old_new[uv_fkey][v])
                subd.add_face(face)
        mesh = subd
    return mesh


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from brg.datastructures.mesh.quad import QuadMesh
    from brg.geometry.polyhedron import Polyhedron

    cube = Polyhedron.generate(6)

    quad = QuadMesh.from_vertices_and_faces(cube.vertices, cube.faces)
    quad = quad_subdivision(quad)

    quad.draw()
