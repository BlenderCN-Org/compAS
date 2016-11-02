""" An example of Dynamic Relaxation, using a Rhino model and subprocess."""

from brg.datastructures.network.network import Network

from brg.datastructures.utilities import geometric_key
from brg.datastructures.utilities import gkeys_from_network

from brg_rhino.datastructures.mesh import RhinoMesh

from brg_rhino.utilities.drawing import xdraw_cylinders
from brg_rhino.utilities.objects import get_point_coordinates
from brg_rhino.utilities import wait

from subprocess import Popen
from subprocess import PIPE

import json
import rhinoscriptsyntax as rs


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


# Mesh from loft
left_curve = rs.ObjectsByLayer('left_curve')
right_curve = rs.ObjectsByLayer('right_curve')
top_curve = rs.ObjectsByLayer('top_curve')
bot_curve = rs.ObjectsByLayer('bot_curve')
surface = rs.AddSweep2([left_curve, right_curve], [top_curve, bot_curve])
mesh = RhinoMesh.from_surface(surface, density=(20, 20))
rs.DeleteObject(surface)

# Make Network
edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)]
         for u, v in mesh.edges()]
network = Network.from_lines(edges)
network.set_dva(attr_dict={'bcx': 1, 'bcy': 1, 'bcz': 1,
                           'px': 0, 'py': 0, 'pz': -1})
network.set_dea(attr_dict={'s0': 0.0*10**6, 'E': 1*10**9,
                           'A': 0.25*3.142*0.002**2})
vkeys, ekeys = gkeys_from_network(network)

# Lines
rs.CurrentLayer('lines')
rs.DeleteObjects(rs.ObjectsByLayer('lines'))
rs.EnableRedraw(False)
for u, v in mesh.edges():
    if  len(mesh.vertex_neighbours(u) + mesh.vertex_neighbours(v)) <= 6:
        sp = mesh.vertex_coordinates(u)
        ep = mesh.vertex_coordinates(v)
        rs.AddLine(sp, ep)
rs.EnableRedraw(True)

# Fixed
xyz = [rs.CurveStartPoint(left_curve), rs.CurveEndPoint(left_curve),
       rs.CurveStartPoint(right_curve), rs.CurveEndPoint(right_curve)]
indices = [vkeys[geometric_key(i, '3f')] for i in xyz]
for index in indices:
    network.set_vertex_attribute(index, 'bcx', 0)
    network.set_vertex_attribute(index, 'bcy', 0)
    network.set_vertex_attribute(index, 'bcz', 0)

# Edge ties
mps = [rs.CurveMidPoint(line) for line in rs.ObjectsByLayer('lines')]
uv = [ekeys[geometric_key(i, '3f')] for i in mps]
for u, v in uv:
    network.set_edge_attribute(u, v, 's0', 0*10**6)

# Settings
settings = {'tol': 1,
            'steps': 50000,
            'rtype': 'magnitude_1',
            'factor': 1,
            'ct': 't'}

# Subprocess
sub = 'D:/py/dr_subprocess.py'
ipath = 'D:/idata.json'
opath = 'D:/odata.json'
spath = 'D:/sdata.json'
network.to_json(ipath)
with open(spath, 'w+') as fp:
    json.dump(settings, fp)
p = Popen(['pythonw', '-u', sub, ipath, opath, spath],
          stdout=PIPE, stderr=PIPE)
while True:
    line = p.stdout.readline()
    if not line:
        break
    line = line.strip()
    print line
    wait()
stdout, stderr = p.communicate()
network_ = Network.from_json(opath)

# Plot lines
rs.CurrentLayer('plot')
rs.DeleteObjects(rs.ObjectsByLayer('plot'))
sc = 0.2
rmin = 0.01
fmax = max([abs(fi) for fi in network_.get_edges_attribute('f')])
lines = []
for u, v in network_.edges():
    if  network_.edge[u][v]['f'] > 0:
        col = [0, 0, 255]
    else:
        col = [255, 0, 0]
    r = abs(sc * network_.edge[u][v]['f'] / fmax)
    lines.append({'start': network_.vertex_coordinates(u),
                  'end': network_.vertex_coordinates(v),
                  'name': 'edge_' + u + '-' + v,
                  'color': col,
                  'radius': r + rmin})
xdraw_cylinders(lines)

print('Script finished')
