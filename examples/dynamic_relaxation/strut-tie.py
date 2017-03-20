"""An example of dynamic relaxation for strut and tie models."""

from compas_blender.utilities.layers import layer_clear
from compas_blender.utilities.objects import get_objects_by_layer
from compas_blender.utilities.objects import select_objects_none

from compas_blender.geometry.mesh import network_from_bmesh

from compas.utilities import geometric_key

from compas.numerical.methods.dynamic_relaxation import run

from numpy import abs
from numpy import sum

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


select_objects_none()
layer_clear(19)

# Construct Network
network = network_from_bmesh(get_objects_by_layer(0)[0])

# Make gkey_key dictionary
gkey_key = {}
for key in network.vertices():
    gkey_key[geometric_key(network.vertex_coordinates(key), '3f')] = key

# Vertex attributes
network.set_vertices_attributes(network.vertices(), {'BC': [1, 1, 1], 'P': [0, 0, 0]})

# Edge attributes
network.set_edges_attributes(network.edges(), {'E': 5 * 10**9, 'A': 0.001, 's0': 0, 'CT': 'CT'})

# Support vertices
supports = get_objects_by_layer(1)
for support in supports:
    key = gkey_key[geometric_key(list(support.location), '3f')]
    network.set_vertex_attributes(key, {'BC': [0, 0, 0]})

# Loads
loads = get_objects_by_layer(2)
for load in loads:
    key = gkey_key[geometric_key(list(load.location), '3f')]
    network.set_vertex_attributes(key, {'P': [float(i) for i in load.name.split('_')]})

# Run
X, f, l = run(network, refresh=100, bmesh=True, scale=0.2)
lp = sum(abs(f) * l)
print('Load path: {0:.3g}'.format(lp))

select_objects_none()
