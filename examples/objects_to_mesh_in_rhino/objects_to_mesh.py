__author__     = ['Matthias Rippmann <rippmann@ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 11, 2016'


import time
import rhinoscriptsyntax as rs  
import math
import copy
import Rhino
from brg.datastructures.mesh.mesh import Mesh
from brg.datastructures.mesh.algorithms.smoothing import mesh_smooth

import brg_rhino.utilities as rhino
#import utility as rhutil
import Rhino
import scriptcontext

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
    if crvs: rs.DeleteObjects(crvs)
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
    return guid                  

def convert_to_uv_space(srf,all_pts):
    
    uv_pts = []
    for pt in all_pts:
        u,v = rs.SurfaceClosestPoint(srf,pt) 
        uv_pts.append((u,v,0))
    return uv_pts

def wrapper(brep,tolerance,fixed):
    def user_func(mesh,i):
        
        
        key_index = mesh.key_index()
        
        #dict((k, i) for i, k in self.vertices_enum())
        
        pts = []
        key_index = {}
        count = 0
        for k, a in mesh.vertices_iter(True):
            if k in fixed:
                continue
            pts.append((a['x'], a['y'], a['z'])) 
            key_index[k] = count
            count += 1
        if pts:
            points = rs.coerce3dpointlist(pts, True)      
            points = brep.Faces[0].PullPointsToFace(points, tolerance)
            if len(pts) == len(points):
                #print "Yes"
                for key in key_index:
                    index = key_index[key]
                    mesh.vertex[key]['x'] = points[index][0]
                    mesh.vertex[key]['y'] = points[index][1]
                    mesh.vertex[key]['z'] = points[index][2]
            else:
                print "No"
                pass
            
        
        
        
        
        if i%10==0:
            rs.Prompt(str(i))
            draw_light(mesh,temp = True) 
            Rhino.RhinoApp.Wait()
            

        
        
        
            
    return user_func
        
    #count += 1

def nurbs_to_mesh(srf,trg_len):
    
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
    crvs  = [x for (_,x) in sorted(zip(crvs_len,joint))]
    
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
     

    rs.DeleteObjects(crvs)        

           
     
    all_pts_uv = convert_to_uv_space(srf,all_pts) 
    tris = delaunay(all_pts_uv,outbound_keys,inbounds_keys)
    
    mesh = Mesh()
    
    for i,pt in enumerate(all_pts):
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2]})
    
    for tri in tris:
        mesh.add_face(tri)  
    
    
    edge_lengths = []
    for u, v in mesh.edges():
        edge_lengths.append(mesh.edge_length(u, v))
    
    print "Max"
    target_start = max(edge_lengths)/2
    print target_start
    
    rs.EnableRedraw(False)
    
    
    srf_id = rs.coerceguid(srf, True)
    brep = rs.coercebrep(srf_id, False)   
    tolerance = rs.UnitAbsoluteTolerance()
    
    fixed = outbound_keys+[item for sublist in inbounds_keys for item in sublist]
    print fixed
    user_func = wrapper(brep,tolerance,fixed)
    
    if 1==1:
        remesh(mesh,trg_len,
           tol=0.1, divergence=0.01, kmax=300,
           target_start=target_start, kmax_approach=150,
           verbose=False, allow_boundary=False,
           ufunc=user_func)
 
    for k in xrange(10):
        mesh_smooth(mesh,1)
        user_func(mesh,k)
    
    return draw_light(mesh,temp = False) 
    
    
    
if __name__ == '__main__':
    
    poly_srf = rs.GetObjects("Select Object",8+16+32)
    if poly_srf:
        srfs_explo = rs.ExplodePolysurfaces(poly_srf) 
    
    if srfs_explo:
        srfs = srfs_explo
    else:
        srfs = poly_srf
       
        
    trg_len = rs.GetReal("Target Edges Length")
    rhino_meshes = []
    for srf in srfs:
        rs.EnableRedraw(False)
        rs.HideObject(srf)
        rhino_meshes.append(nurbs_to_mesh(srf,trg_len))
        if srfs_explo:
            rs.DeleteObject(srf)
        else:
            rs.ShowObject(srf)
    rs.JoinMeshes(rhino_meshes, True)

    