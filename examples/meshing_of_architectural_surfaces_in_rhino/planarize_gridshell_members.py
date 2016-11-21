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


from brg.geometry.arithmetic import add_vectors
from brg.geometry.arithmetic import subtract_vectors

from brg.geometry.transformations import normalize
from brg.geometry.transformations import scale
from brg.utilities.colors import i2rgb
from brg.geometry.spatial import closest_point_on_plane

import brg_rhino.utilities as rhino
from brg.datastructures.mesh.algorithms.smoothing import mesh_smooth_centerofmass
from brg.datastructures.mesh.algorithms.smoothing import mesh_smooth_angle
from brg.datastructures.mesh.algorithms.smoothing import mesh_smooth_centroid
from brg.datastructures.mesh.algorithms.smoothing import  mesh_smooth_area


from brg.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions

from brg_rhino.conduits.lines import LinesConduit

#import utility as rhutil
import Rhino
import scriptcontext





def get_faces_from_polylines(polys,points):
    faces = []
    for key in polys:
        poly_points = polys[key]['points']
        indices = []
        for point in poly_points:
            indices.append(str(rs.PointArrayClosestPoint(points,point)))
        faces.append(indices)
    return faces



def get_points_coordinates(objs):
    return [rs.PointCoordinates(obj) for obj in objs]


def get_polyline_points(polylines):
    polys = {}
    for key,id in enumerate(polylines):
        polys[key] = {}
        if not rs.IsCurveClosed(id):
            print str(id) + " is an open curve"
            rs.MessageBox(str(id) + " is an open curve")
            return None
        polys[key]['points'] = rs.PolylineVertices(id)[:-1]
        polys[key]['id'] = id
    return polys


def draw_light(mesh,temp = True):
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    xyz = mesh.xyz
    faces = []
    
    for fkey in mesh.faces_iter():
        face = mesh.face_vertices(fkey,True)
        
        
        #poly_pts = [xyz[key_index[k]] for k in face+[face[0]]]
        
        face.append(face[-1])
        faces.append([key_index[k] for k in face])
        
        
    
        #rs.AddPolyline(poly_pts)
        
    guid = rs.AddMesh(xyz, faces) 
    if temp:
        rs.EnableRedraw(True)
        rs.EnableRedraw(False)
        rs.DeleteObject(guid)
    return guid 

def draw(mesh,layer_1,layer_2):
    
    rs.EnableRedraw(False)
    


    objs = rs.ObjectsByLayer(layer_1)
    rs.DeleteObjects(objs)
    objs = rs.ObjectsByLayer(layer_2)
    rs.DeleteObjects(objs)    
    
    pts_objs = []
    for key, a in mesh.vertices_iter(True):
    
       pt = (a['x'], a['y'], a['z'])
       
       pts_objs.append(rs.AddPoint(pt))
       rs.ObjectColor(pts_objs[-1],a['color'] )
       
    rs.ObjectLayer(pts_objs,layer_1)
        
        
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    xyz = mesh.xyz    
    polylines = []
    for fkey in mesh.faces_iter():
        face = mesh.face_vertices(fkey,True)
        
        
        poly_pts = [xyz[key_index[k]] for k in face+[face[0]]]
        polylines.append(rs.AddPolyline(poly_pts))
        
    rs.ObjectLayer(polylines,layer_2)
    
        
        

    rs.EnableRedraw(True)
       





def relax_mesh_on_surface():
    
    srf = rs.ObjectsByLayer("re_01_trg_srf")[0]
    srf_id = rs.coerceguid(srf, True)
    brep = rs.coercebrep(srf_id, False)
    
    polylines = rs.ObjectsByLayer("re_02_polys")
    pts_objs = rs.ObjectsByLayer("re_03_points")
    guides = rs.ObjectsByLayer("re_04_guides")
    
    vis = 30
    kmax = 300
    dis = 0.3
    
    pts = get_points_coordinates(pts_objs)
    
    mesh = Mesh()
    
    for i,pt in enumerate(pts):
        color = rs.ObjectColor(pts_objs[i])
        type, guide_srf,guide_crv = None, None, None

        if [rs.ColorRedValue(color),rs.ColorGreenValue(color),rs.ColorBlueValue(color)] == [255,0,0]:
            type = 'fixed'
        elif [rs.ColorRedValue(color),rs.ColorGreenValue(color),rs.ColorBlueValue(color)] == [255,255,255]:
            type = 'free'
        elif [rs.ColorRedValue(color),rs.ColorGreenValue(color),rs.ColorBlueValue(color)] == [0,0,0]:
            type = 'surface'
            guide_srf = brep
        else:
            type = 'guide'
            for guide in guides:
                if rs.ObjectColor(guide) == color:
                    crv_id = rs.coerceguid(guide, True)
                    crv = rs.coercecurve(crv_id, False)
                    guide_crv = crv
                    break       
            
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2], 'color' : color, 'type' : type,'guide_srf' : guide_srf,'guide_crv' : guide_crv})
    

    
    polys = get_polyline_points(polylines)
    tris = get_faces_from_polylines(polys,pts)
    
    for tri in tris:
        mesh.add_face(tri)     


    rs.EnableRedraw(False)

    pts = []
    for key, a in mesh.vertices_iter(True):
        
        
        pt1 = (a['x'], a['y'], a['z'])
        pts.append(pt1)
        vec = mesh.vertex_normal(key) 
        vec = scale(normalize(vec),dis)
        pt2 = subtract_vectors(pt1,vec)
        
        pt2 = subtract_vectors(pt1,vec)
        a['x2'] = pt2[0]
        a['y2'] = pt2[1]
        a['z2'] = pt2[2]
        
        #rs.AddLine(pt1,pt2)
    
    
    

    
    for k in range(kmax):
        nodes_top_dict = {key: [] for key in mesh.vertices()}
        polys = []
        max_distances = []
        for u,v in mesh.edges():
            pt1 = mesh.vertex_coordinates(u)
            pt2 = mesh.vertex_coordinates(v)
            pt3 = mesh.vertex[u]['x2'],mesh.vertex[u]['y2'],mesh.vertex[u]['z2']
            pt4 = mesh.vertex[v]['x2'],mesh.vertex[v]['y2'],mesh.vertex[v]['z2']
            points = [pt1,pt2,pt3,pt4]
            plane = rs.PlaneFitFromPoints(points)
            points_planar = [rs.PlaneClosestPoint(plane, pt) for pt in points]
            
            if k%vis == 0:
                polys.append(rs.AddPolyline([pt1,pt2,pt4,pt3,pt1]))
            
            nodes_top_dict[u].append(points_planar[2])
            nodes_top_dict[v].append(points_planar[3])
               
            distances = [distance(pt1,pt2) for pt1,pt2 in zip(points,points_planar)]
            max_distances.append(max(distances))    
                    
        for key in mesh.vertices():
            cent = centroid(nodes_top_dict[key])
            mesh.vertex[key]['x2'] = cent[0]
            mesh.vertex[key]['y2'] = cent[1]
            mesh.vertex[key]['z2'] = cent[2] 
    

    
        if k%vis == 0:    
            rs.EnableRedraw(True)
            rs.EnableRedraw(False)
            print max(max_distances)
            if not k == 0 and not k == kmax-1:
                rs.DeleteObjects(polys)
        
    rs.EnableRedraw(True)
    #draw(mesh,"re_03_points","re_02_polys")
    

if __name__ == "__main__":
    
    
    relax_mesh_on_surface()