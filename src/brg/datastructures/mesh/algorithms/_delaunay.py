from brg.datastructures.mesh.mesh import Mesh

from brg.geometry import centroid_points
from brg.geometry import distance_point_point
from brg.geometry import add_vectors
from brg.geometry import bounding_box

from brg.geometry.planar import is_point_in_polygon_2d
from brg.geometry.planar import is_point_in_circle_2d
from brg.geometry.planar import circle_from_points_2d


class DelaunayMesh(Mesh):
    """"""

    def insert_vertex(self, fkey, key=None, xyz=None):
        """Insert a vertex in the specified face.

        Parameters:
            fkey (str): The key of the face in which the vertex should be inserted.

        Returns:
            str: The keys of the newly created faces.

        Raises:
            VelueError: If the face does not exist.
        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(key, x=x, y=y, z=z)
        for u, v in self.face[fkey].iteritems():
            fkeys.append(self.add_face([u, v, w]))
        del self.face[fkey]
        return fkeys


# replace and import from framework once fkeys are returned
def swap_edge(mesh, u, v):
    """Replace an edge of the mesh by an edge connecting the opposite
    vertices of the adjacent faces.

    Parameters:
        u (str): The key of one of the vertices of the edge.
        v (str): The key of the other vertex of the edge.

    Returns:
        None

    Raises:
        ValueError: If `u` and `v` are not neighbours.
        TriMeshError: If one of the half-edges does not exist.
    """
    # check legality of the swap
    # swapping on the boundary is not allowed
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]
    if fkey_uv is None or fkey_vu is None:
        print "yo 1"
        return "yo 1"
    # swapping to a half-edge that already exists is not allowed
    o_uv = mesh.face[fkey_uv][v]
    o_vu = mesh.face[fkey_vu][u]
    if o_uv in mesh.halfedge[o_vu] and o_vu in mesh.halfedge[o_uv]:
        print "yo 2"
        return "yo 2"
    # swapping between non-triangles is not allowed
    # this check is only necessary to make the algorithm applicable to
    # non-triangle meshes!
    # perhaps this is not necessary
    if len(mesh.face[fkey_uv]) != 3 or len(mesh.face[fkey_vu]) != 3:
        print "yo 3"
        return "yo 3"
    # swap
    # delete the current half-edge
    del mesh.halfedge[u][v]
    del mesh.halfedge[v][u]
    # delete the adjacent faces
    del mesh.face[fkey_uv]
    del mesh.face[fkey_vu]
    # add the faces created by the swap
    fkey1 = mesh.add_face([o_uv, o_vu, v])
    fkey2 = mesh.add_face([o_vu, o_uv, u])
    return fkey1, fkey2


def super_triangle(coords):
    centpt = centroid_points(coords)
    bbpts = bounding_box(coords)
    dis = distance_point_point(bbpts[0], bbpts[2])
    dis = dis * 300
    v1 = (0 * dis, 2 * dis, 0)
    v2 = (1.73205 * dis, -1.0000000000001 * dis, 0)  # due to numerical issues
    v3 = (-1.73205 * dis, -1 * dis, 0)
    pt1 = add_vectors(centpt, v1)
    pt2 = add_vectors(centpt, v2)
    pt3 = add_vectors(centpt, v3)
    return pt1, pt2, pt3


def delaunay_from_points(points3d, outbound_keys=None, inbounds_keys=None):
    mesh = DelaunayMesh()
    points = [(point[0], point[1], 0.0) for point in points3d]

    # create super triangle
    pt1, pt2, pt3 = super_triangle(points)
    # add super triangle vertices to mesh (remember supertrikeys)
    max = len(points)
    super_keys = str(max), str(max + 1), str(max + 2)
    mesh.add_vertex(super_keys[0], {'x': pt1[0], 'y': pt1[1], 'z': pt1[2]})
    mesh.add_vertex(super_keys[1], {'x': pt2[0], 'y': pt2[1], 'z': pt2[2]})
    mesh.add_vertex(super_keys[2], {'x': pt3[0], 'y': pt3[1], 'z': pt3[2]})
    mesh.add_face(super_keys)

    # iterate over points
    for i, pt in enumerate(points):
        # if key not in superkeys:
        # insert point
        key = str(i)
        # draw_light(mesh,temp = False)
        fkeys = mesh.faces()
        # check in which triangle this point falls
        for fkey in fkeys:
            # abc = mesh.face_coordinates(fkey) #This is slower
            # This is faster:
            keya, keyb, keyc = mesh.face_vertices(fkey)
            dicta = mesh.vertex[keya]
            a = [dicta['x'], dicta['y']]
            dictb = mesh.vertex[keyb]
            b = [dictb['x'], dictb['y']]
            dictc = mesh.vertex[keyc]
            c = [dictc['x'], dictc['y']]
            pt_2d = (pt[0], pt[1])
            if is_point_in_polygon_2d(pt_2d,[a, b, c]):
                # generate 3 new triangles (faces) and delete surrounding triangle
                newtris = mesh.insert_vertex(fkey, key, xyz=pt)
                break

        while newtris:
            # print "newtris: "+ str(newtris)
            fkey = newtris.pop()
            # print "popped: "+ str(fkey)

            # get opposite_face
            keys = mesh.face_vertices(fkey)
            s = list(set(keys) - set([key]))
            u, v = s[0], s[1]
            fkey1 = mesh.halfedge[u][v]
            if fkey1 != fkey:
                fkey_op, u, v = fkey1, u, v
            else:
                fkey_op, u, v = mesh.halfedge[v][u], u, v

            if fkey_op:
                # fpts = mesh.face_coordinates(fkey_op)#This is slower
                # This is faster:
                keya, keyb, keyc = mesh.face_vertices(fkey_op)
                dicta = mesh.vertex[keya]
                a = [dicta['x'] + 0.000000001, dicta['y'] - 0.000000001]  # avoid numerical issues for points on a line
                dictb = mesh.vertex[keyb]
                b = [dictb['x'], dictb['y']]
                dictc = mesh.vertex[keyc]
                c = [dictc['x'], dictc['y']]

                circle = circle_from_points_2d(a, b, c)

                if is_point_in_circle_2d(pt,circle):
                    # mesh.swap_edge(u, v)
                    fkey, fkey_op = swap_edge(mesh, u, v)
                    # print "swaped: "+ u +" - " + v
                    newtris.append(fkey)
                    newtris.append(fkey_op)

    # Clean-up:
    # Delete faces adjacent to supertriangle
    for key in super_keys:
        # mesh.delete_vertex(key) for future implementation
        mesh.remove_vertex(key)

    # Delete faces outside of boundary
    if outbound_keys:
        poly = []
        poly.append(mesh.vertex_coordinates(outbound_keys[-1]))  # make it a closed poly
        for key in outbound_keys:
            poly.append(mesh.vertex_coordinates(key))
        for fkey in mesh.faces():
            cent = mesh.face_centroid(fkey)
            if not is_point_in_polygon_2d(poly, cent):
                mesh.delete_face(fkey)

    # Delete faces inside of inside boundaries
    if inbounds_keys:
        for inbound_keys in inbounds_keys:
            poly = []
            poly.append(mesh.vertex_coordinates(inbound_keys[-1]))  # make it a closed poly
            for key in inbound_keys:
                poly.append(mesh.vertex_coordinates(key))
            for fkey in mesh.faces():
                cent = mesh.face_centroid(fkey)
                if is_point_in_polygon_2d(poly, cent):
                    mesh.delete_face(fkey)

    return [[int(key) for key in mesh.face_vertices(fkey, True)] for fkey in mesh.faces()]

if __name__ == "__main__":
    
    import rhinoscriptsyntax as rs
    from brg.datastructures.mesh.algorithms._delaunay import delaunay
    from brg_rhino.helpers.mesh import draw_mesh
    
    objs = rs.GetObjects("Select Points",1)
    
    pts = [rs.PointCoordinates(obj) for obj in objs]
    
    faces = delaunay(pts)
    faces = [[int(face[0]),int(face[1]),int(face[2]),int(face[2])] for face in faces]
    print faces
    rs.AddMesh(pts,faces)