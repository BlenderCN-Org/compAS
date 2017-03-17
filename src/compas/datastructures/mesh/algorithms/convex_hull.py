# to be checked out and implemented using compas
# works well as is
# https://gist.github.com/anonymous/5184ba0bcab21d3dd19781efd3aae543
# check also http://thomasdiewald.com/blog/?p=1888 

# import math
# 
# 
# from compas_rhino.helpers.mesh import mesh_from_guid
# from compas_rhino.helpers.mesh import draw_mesh
# from compas.datastructures.mesh import Mesh
# 
# from compas.datastructures.mesh.algorithms.subdivision import subdivide_mesh_catmullclark
# 
# import rhinoscriptsyntax as rs
# 
# 
def vect(points, start, end):
    return [y - x for x, y  in zip(points[start], points[end])]
     
def cross(u, v):
    return [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]]
    
def dot(u, v):
    return sum([x*y for x, y in zip(u,v)])
 
def normal(points, face):
    u = vect(points, face[0], face[1])
    v = vect(points, face[0], face[-1])
    return cross(u, v)
 
def seen(points, face, p):
    N = normal(points, face)
    P = vect(points, face[0], p)
    return (dot(N, P) >= 0)
 
def bdry(faces):
    bdry_fw = set( [(F[i-1], F[i]) for F in faces for i in range(0,len(F)) ] )
    bdry_bk = set( [(F[i], F[i-1]) for F in faces for i in range(0,len(F)) ] )
    return bdry_fw - bdry_bk
 
def addPoint(points, hull, p):
    seenF = [F for F in hull if seen(points, F, p)]
    if len(seenF)==len(hull): #if can see all faces, unsee ones looking "down"
        N = normal(points, seenF[0]) 
        seenF = [F for F in seenF if dot(normal(points, F), N) > 0]
    for F in seenF:
        hull.remove(F)
    for E in bdry(seenF):
        hull.append([E[0], E[1], p])
       
def convexHull(points):
    hull = [[0,1,2],[0,2,1]]
    for i in range(3,len(points)):
        addPoint(points, hull, i)        
    return hull
 
def coords(points, hull):
    return [[points[p] for p in F] for F in hull]
 
objs = rs.GetObjects("Select Points",1)
pts = [rs.PointCoordinates(obj) for obj in objs]
 
faces =  convexHull(pts)    
#print coords(points, convexHull(points))  
 
mesh = Mesh.from_vertices_and_faces(pts, faces)