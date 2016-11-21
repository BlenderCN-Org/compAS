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
from brg.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions


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







def wrapper(vis):
    
   
    tolerance = rs.UnitAbsoluteTolerance()
    
    def user_function(mesh,i):
    
     #dict((k, i) for i, k in self.vertices_enum())
     
        for key, a in mesh.vertices_iter(True):
        
           pt = (a['x'], a['y'], a['z'])
           
           if a['type'] == 'fixed' or a['type'] == 'free':
               continue
           if a['type'] == 'guide':
               point = rs.coerce3dpoint(pt)
               rc, t = a['guide_crv'].ClosestPoint(point)
               pt = a['guide_crv'].PointAt(t)
           elif a['type'] == 'surface':
               point = rs.coerce3dpoint(pt)
               pt = a['guide_srf'].ClosestPoint(point)
            
           mesh.vertex[key]['x'] = pt[0]
           mesh.vertex[key]['y'] = pt[1]
           mesh.vertex[key]['z'] = pt[2]    
        
        
        if vis:
            if i%vis==0:
                rs.Prompt(str(i))
                draw_light(mesh,temp = True) 
                Rhino.RhinoApp.Wait()
  
    return user_function


def relax_mesh_on_surface():
    
    srf = rs.ObjectsByLayer("re_01_trg_srf")[0]
    srf_id = rs.coerceguid(srf, True)
    brep = rs.coercebrep(srf_id, False)
    
    polylines = rs.ObjectsByLayer("re_02_polys")
    pts_objs = rs.ObjectsByLayer("re_03_points")
    guides = rs.ObjectsByLayer("re_04_guides")
    
    vis = 1
    
    
    pts = get_points_coordinates(pts_objs)
    
    mesh = Mesh()
    
    for i,pt in enumerate(pts):
        color = rs.ObjectColor(pts_objs[i])

        type = None
        guide_srf = None
        guide_crv = None

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
        
    user_function = wrapper(vis)    
    mesh_smooth_centerofmass(mesh, fixed=None, kmax=10, d=1.0, ufunc=user_function)
    
    draw_light(mesh,temp = True)
    

if __name__ == "__main__":
    
    
    relax_mesh_on_surface()