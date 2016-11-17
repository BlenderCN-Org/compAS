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
from brg.geometry.functions import centroid
from brg.geometry.functions import distance
from brg.geometry.functions import midpoint

import brg_rhino.utilities as rhino
#import utility as rhutil
import Rhino
import scriptcontext


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

def create_quad_mesh(srf,u_div,v_div):
    
  
    
    u_domain = rs.SurfaceDomain(srf, 0)
    v_domain = rs.SurfaceDomain(srf, 1)
    u = (u_domain[1] - u_domain[0]) / (u_div - 1)
    v = (v_domain[1] - v_domain[0]) / (v_div - 1)
    
    #pts =  [[None for i in range(v_div)] for j in range(u_div)]
    mesh_pts = []
    for i in xrange(u_div):
        for j in xrange(v_div):
            #pts[i][j] = rs.EvaluateSurface (srf, u_domain[0] + u * i, v_domain[0] + v * j)
            mesh_pts.append(rs.EvaluateSurface (srf, u_domain[0] + u * i, v_domain[0] + v * j))
            
    faces = []        
    for i in xrange(u_div-1):
         for j in xrange(v_div-1):       
             faces.append(((i*v_div)+j,((i+1)*v_div)+j,((i+1)*v_div)+j+1,(i*v_div)+j+1))

    mesh = Mesh()
    
    for i,pt in enumerate(mesh_pts):
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2]})
    
    for face in faces:
        mesh.add_face(face)  
    
    return mesh        

if __name__ == "__main__":
    
    srf = rs.GetObject("Select Surface",8)
    rs.EnableRedraw(False)
    u_div = 40
    v_div = 15
    
    mesh = create_quad_mesh(srf,u_div,v_div)

    draw_light(mesh,temp = False)  
    
    
    kmax = 1500
    diagonal_fac = .1
    edge_fac = .1
    vis = 20

    
    boundary = mesh.vertices_on_boundary()
    boundary = []
    
    
    diagonal = {}
    for fkey in mesh.faces_iter():
        keys = mesh.face_vertices(fkey, ordered=True)
        if len(keys) == 4:
            dis1 = distance(mesh.vertex_coordinates(keys[0]),mesh.vertex_coordinates(keys[2]))
            dis1_min, dis1_max = dis1*(1-diagonal_fac),dis1*(1+diagonal_fac)
            dis2 = distance(mesh.vertex_coordinates(keys[1]),mesh.vertex_coordinates(keys[3]))
            dis2_min, dis2_max = dis2*(1-diagonal_fac),dis2*(1+diagonal_fac)
            diagonal[fkey] = dis1_min,dis1_max,dis2_min,dis2_max
            
    edges_dis = {}
    for uv in mesh.edges():
        dis = mesh.edge_length(uv[0], uv[1])
        dis_min, dis_max = dis*(1-edge_fac),dis*(1+edge_fac)
        edges_dis[uv] = dis_min, dis_max
    
    for k in range(kmax):
        rs.Prompt("Iteration {0} of {1}".format(k+1,kmax+1))
        nodes_dict = {key: [] for key in mesh.vertices()}
        dots = []
        for fkey in mesh.faces_iter():
            
            keys = mesh.face_vertices(fkey,ordered=True)
            points = [mesh.vertex_coordinates(key) for key in keys]
            plane = rs.PlaneFitFromPoints(points)
            
            if k%vis==0:
                if not rs.PointsAreCoplanar(points,.01):
                    dots.append(rs.AddTextDot("x",centroid(points)))
            
            points = [rs.PlaneClosestPoint(plane, pt) for pt in points]
            
            

            
            
            dis1_min, dis1_max,dis2_min,dis2_max= diagonal[fkey] 
            
            dis1_step = distance(points[0],points[2])
            dis2_step = distance(points[1],points[3])
            
            if dis1_step < dis1_min:
                trg_dis = dis1_min
            elif dis1_step > dis1_max:
                trg_dis = dis1_max
            else:
                trg_dis = None
            if trg_dis:
                mid_pt = midpoint(points[0],points[2])
                vec = rs.VectorCreate(points[0],mid_pt)
                vec = rs.VectorUnitize(vec)
                vec = rs.VectorScale(vec,trg_dis*0.5)
                points[0] = rs.PointAdd(mid_pt,vec)
                points[2] = rs.PointAdd(mid_pt,rs.VectorScale(vec,-1))
                #rs.AddLine(points[0],points[2])
                
                
            if dis2_step < dis2_min:
                trg_dis = dis2_min
            elif dis2_step > dis2_max:
                trg_dis = dis2_max
            else:
                trg_dis = None
            if trg_dis:
                mid_pt = midpoint(points[1],points[3])
                vec = rs.VectorCreate(points[1],mid_pt)
                vec = rs.VectorUnitize(vec)
                vec = rs.VectorScale(vec,trg_dis*0.5)
                points[1] = rs.PointAdd(mid_pt,vec)
                points[3] = rs.PointAdd(mid_pt,rs.VectorScale(vec,-1))
                #rs.AddLine(points[1],points[3])            
            
            for i,key in enumerate(keys):
                nodes_dict[key].append(points[i])
        
        
        
                
        for key in mesh.vertices():
            if key in boundary:
                continue
            cent = centroid(nodes_dict[key])
            mesh.vertex[key]['x'] = cent[0]
            mesh.vertex[key]['y'] = cent[1]
            mesh.vertex[key]['z'] = cent[2]   
            
            
        nodes_dict = {key: [] for key in mesh.vertices()}    
        for uv in mesh.edges():
            dis_step = mesh.edge_length(uv[0], uv[1])
            dis_min, dis_max = edges_dis[uv] 
            
            if dis_step < dis_min:
                trg_dis = dis_min
            elif dis_step > dis_max:
                trg_dis = dis_max
            else:
                trg_dis = None
            if trg_dis:
                pt1 = mesh.vertex_coordinates(uv[0])
                pt2 = mesh.vertex_coordinates(uv[1])
                
                mid_pt = midpoint(pt1,pt2)
                vec = rs.VectorCreate(pt1,mid_pt)
                vec = rs.VectorUnitize(vec)
                vec = rs.VectorScale(vec,trg_dis*0.5)
                pt1 = rs.PointAdd(mid_pt,vec)
                pt2 = rs.PointAdd(mid_pt,rs.VectorScale(vec,-1))
                
                nodes_dict[uv[0]].append(pt1)
                nodes_dict[uv[1]].append(pt2)
                
                #rs.AddLine(pt1,pt2) 
        
        for key in nodes_dict:
            if key in boundary:
                continue
            cent = centroid(nodes_dict[key])
            if cent:
                mesh.vertex[key]['x'] = cent[0]
                mesh.vertex[key]['y'] = cent[1]
                mesh.vertex[key]['z'] = cent[2] 
        #rs.AddPoints(points)
          
          
        if k%vis==0:    
            draw_light(mesh,temp = True)  
            if dots: rs.DeleteObjects(dots)
    
    draw_light(mesh,temp = False)  


