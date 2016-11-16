__author__     = ['Matthias Rippmann <rippmann@ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 11, 2016'


import time
import rhinoscriptsyntax as rs  
import math
import copy
from brg.datastructures.mesh.mesh import Mesh

from brg.datastructures.mesh.algorithms.tri.topology import remesh

from delaunay import delaunay


def convert_to_uv_space(srf,pts):
    pts_uv = []
    for pt in pts:
        uv = rs.SurfaceClosestPoint(srf,pt)
        pts_uv.append((uv[0],uv[1],0))
    return pts_uv


def get_boundary_points(crvs_bound,trg_len):
    crvs = rs.ExplodeCurves(crvs_bound,True)
    if not crvs:  crvs = [crvs_bound]
    div_pts = []
    for crv in crvs:
        div = round(rs.CurveLength(crv)/trg_len,0)
        if div < 1: div = 1
        pts = rs.DivideCurve(crv,div)
        div_pts += pts
        
    div_pts = rs.CullDuplicatePoints(div_pts)

    return div_pts    
        
def get_boundary_indecies(bound_pts,all_pts): 
    keys = []
    for bound_pt in bound_pts:
        for i,pt in enumerate(all_pts):
            if rs.PointCompare(pt,bound_pt):
                keys.append(str(i))
    return keys   

def draw_light(mesh,temp = True):
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    xyz = mesh.xyz
    faces = []
    for fkey in mesh.faces_iter():
        face = mesh.face_vertices(fkey,True)
        face.append(face[-1])
        faces.append([key_index[k] for k in face])
    guid = rs.AddMesh(xyz, faces) 
    if temp:
        rs.EnableRedraw(True)
        rs.EnableRedraw(False)
        rs.DeleteObject(guid)                  

def convert_to_uv_space(srf,all_pts):
    
    uv_pts = []
    for pt in all_pts:
        u,v = rs.SurfaceClosestPoint(srf,pt) 
        uv_pts.append((u,v,0))
    return uv_pts

def nurbs_to_mesh():
    trg_len = 1
    
    srf = rs.GetObject("Select Srf",8)
    
    crvs = rs.DuplicateEdgeCurves(srf) 
    
    print crvs
    if len(crvs)>1:
        joint = rs.JoinCurves(crvs,True)
        if joint:
            print len(joint)
            print joint
            if len(joint) > 2:
                print "hole" 
    else:
        if rs.IsCurveClosed(crvs[0]):
            joint = [crvs[0]]
            print "closed"#e.g. if it is a disk
        else:
            print "Surface need to be split"#e.g. if it is a sphere
            return None
         
    
    #sort curves (this is cheating: the longer curve is not necessarily the outer boundary!) 
    #todo: an inside outside comparison in uv space
    crvs_len = [rs.CurveLength(crv) for crv in joint] 
    crvs = [x for (_,x) in sorted(zip(crvs_len,joint))]
    
    outer_crv =  crvs[-1]
    inner_crvs = crvs[:-1]
    
    outer_bound_pts = get_boundary_points(outer_crv,trg_len)
    if inner_crvs: inner_bounds_pts = [get_boundary_points(crvs,trg_len) for crvs in inner_crvs]
    
    all_pts = copy.copy(outer_bound_pts)
    if inner_crvs: 
        for pts in inner_bounds_pts:
            all_pts += pts
    
    outbound_keys = get_boundary_indecies(outer_bound_pts,all_pts)

    inbounds_keys = []
    if inner_crvs:
        for inner_bound_pts in inner_bounds_pts:
            inbounds_keys.append(get_boundary_indecies(inner_bound_pts,all_pts))      
     
    all_pts_uv = convert_to_uv_space(srf,all_pts) 
    tris = delaunay(all_pts_uv,outbound_keys,inbounds_keys)
    
    mesh = Mesh()
    
    for i,pt in enumerate(all_pts):
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2]})
    
    for tri in tris:
        mesh.add_face(tri)  
    
    
    remesh(mesh,trg_len,
           tol=0.1, kmax=150,
           start=None, steps=None,
           verbose=False, allow_boundary=False,
           ufunc=None)
    
    draw_light(mesh,temp = False) 
    
    
    
    print ("hello")
    
    
    
if __name__ == '__main__':
    
    nurbs_to_mesh()
    