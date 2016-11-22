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
from brg.datastructures.mesh.algorithms.smoothing import mesh_smooth
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
        face.append(face[-1])
        faces.append([key_index[k] for k in face])
    guid = rs.AddMesh(xyz, faces) 
    if temp:
        rs.EnableRedraw(True)
        rs.EnableRedraw(False)
        rs.DeleteObject(guid)
    return guid 



def relax_mesh_on_surface():
    
    srf = rs.ObjectsByLayer("re_01_trg_srf")[0]
    polylines = rs.ObjectsByLayer("re_02_polys")
    pts_objs = rs.ObjectsByLayer("re_03_points")
    guides = rs.ObjectsByLayer("re_04_guides")
    
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
            guide_srf = srf
        else:
            type = 'guide'
            for guide in guides:
                if rs.ObjectColor(guide) == color:
                    guide_crv = guide
                    break       
            
        mesh.add_vertex(str(i),{'x' : pt[0], 'y' : pt[1], 'z' : pt[2], 'color' : color, 'type' : type,'guide_srf' : guide_srf,'guide_crv' : guide_crv})
    

    
    polys = get_polyline_points(polylines)
    tris = get_faces_from_polylines(polys,pts)
    
    for tri in tris:
        print tri
        mesh.add_face(tri)     
        
    mesh_unify_cycle_directions(mesh)
    
    draw_light(mesh,temp = False)
    

if __name__ == "__main__":
    
    
    relax_mesh_on_surface()