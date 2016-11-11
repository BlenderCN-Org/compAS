__author__     = ['Matthias Rippmann <rippmann@ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 11, 2016'


import time
import rhinoscriptsyntax as rs  
import math


from delaunay import delaunay


objs = rs.GetObjects("Select Points",1)
pts = [rs.PointCoordinates(obj) for obj in objs]

res = delaunay(pts)
print res
print ("hello")