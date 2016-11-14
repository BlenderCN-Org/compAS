__author__     = ['Matthias Rippmann <rippmann@ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 11, 2016'


import time
import rhinoscriptsyntax as rs  
import math


from delaunay import delaunay


def convert_to_uv_space(srf,pts):
    pts_uv = []
    for pt in pts:
        uv = rs.SurfaceClosestPoint(srf,pt)
        pts_uv.append((uv[0],uv[1],0))
    return pts_uv


trg_len = 1

srf = rs.GetObject("Select Srf",8)

crvs = rs.DuplicateEdgeCurves(srf) 

print crvs
if len(crvs)>1:
    joint = rs.JoinCurves(crvs)
    if joint:
        print len(joint)
        print joint
        if len(joint) > 2:
            print "hole" 
else:
    if rs.IsCurveClosed(crvs[0]):
        print "closed"#e.g. if it is a disk
    else:
        print "Surface need to be split"#e.g. if it is a sphere
     









objs = rs.GetObjects("Select Points",1)
polyline = rs.GetObject("Select boundary curve",4)


pts = [rs.PointCoordinates(obj) for obj in objs]

editpts = rs.CurveEditPoints(polyline)

outbound_keys = []
for editpt in editpts:
    for i,pt in enumerate(pts):
        if rs.PointCompare(pt,editpt):
            outbound_keys.append(str(i))

polylines = rs.GetObjects("Select hole curves",4)
inbounds_keys = []
for poly in polylines:
    editpts = rs.CurveEditPoints(poly)
    inbound_keys = []
    for editpt in editpts:
        for i,pt in enumerate(pts):
            if rs.PointCompare(pt,editpt):
                inbound_keys.append(str(i))
    inbounds_keys.append(inbound_keys)         



res = delaunay(pts,outbound_keys,inbounds_keys)

print ("hello")