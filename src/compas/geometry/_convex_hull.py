from __future__ import print_function

from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import dot_vectors


__author__     = ['Matthias Rippmann <rippmann@ethz.ch>']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<rippmannt@ethz.ch>'


def normal_face(points, face):
    u = subtract_vectors(points[face[1]], points[face[0]])
    v = subtract_vectors(points[face[-1]], points[face[0]])
    return cross_vectors(u, v)

def seen(points, face, p):
    normal = normal_face(points, face)
    vec = subtract_vectors(points[p], points[face[0]])
    return (dot_vectors(normal, vec) >= 0)

def bdry(faces):
    bdry_fw = set([(face[i - 1], face[i]) for face in faces for i in range(0,len(face))])
    bdry_bk = set([(face[i], face[i - 1]) for face in faces for i in range(0,len(face))])
    return bdry_fw - bdry_bk

def add_point(points, hull, p):
    seen_faces = [face for face in hull if seen(points, face, p)]
    if len(seen_faces)==len(hull): #if can see all faces, unsee ones looking "down"
        normal = normal_face(points, seen_faces[0]) 
        seen_faces = [face for face in seen_faces if dot_vectors(normal_face(points, face), normal) > 0]
    for face in seen_faces:
        hull.remove(face)
    for edge in bdry(seen_faces):
        hull.append([edge[0], edge[1], p])
      
def convex_hull(points):
    """Construct convex hull for a set of points.

    Parameters:
        points (sequence): A sequence of XYZ coordinates.

    Returns:
        faces (sequence of sequences of integers): the triangular faces of the convex hull

    References:
        https://gist.github.com/anonymous/5184ba0bcab21d3dd19781efd3aae543

    Note:
        The algorithm is not optimized and relatively slow on large sets of points.
        See here for a more optimized version of this algorithm:
        http://thomasdiewald.com/blog/?p=1888 
        
    Examples:

        .. code-block:: python

            import math
            import random
            
            from compas.geometry import distance_point_point
            from compas_rhino.helpers.mesh import draw_mesh
            from compas.datastructures.mesh import Mesh
            
            
            
            radius = 5
            origin = (0., 0., 0.)
            count = 0
            points = []
            while count < 1000:
                x = (random.random() - 0.5) * radius * 2
                y = (random.random() - 0.5) * radius * 2
                z = (random.random() - 0.5) * radius * 2
                pt = x, y, z
                if distance_point_point(origin, pt) <= radius:
                    points.append(pt)
                    count += 1
            
            faces =  convex_hull(points)    
            
            mesh = Mesh.from_vertices_and_faces(points, faces)
            
            draw_mesh(mesh,
                        show_faces = True,
                        show_vertices = False,
                        show_edges = False)

    """   
     
    hull = [[0,1,2],[0,2,1]]
    for i in range(3,len(points)):
        add_point(points, hull, i)        
    return hull

if __name__ == "__main__":

    import math
    import random
    
    from compas.geometry import distance_point_point
    from compas_rhino.helpers.mesh import draw_mesh
    from compas.datastructures.mesh import Mesh
    
    
    
    radius = 5
    origin = (0., 0., 0.)
    count = 0
    points = []
    while count < 1000:
        x = (random.random() - 0.5) * radius * 2
        y = (random.random() - 0.5) * radius * 2
        z = (random.random() - 0.5) * radius * 2
        pt = x, y, z
        if distance_point_point(origin, pt) <= radius:
            points.append(pt)
            count += 1
    
    faces =  convex_hull(points)    
    
    mesh = Mesh.from_vertices_and_faces(points, faces)
    
    draw_mesh(mesh,
                show_faces = True,
                show_vertices = False,
                show_edges = False)