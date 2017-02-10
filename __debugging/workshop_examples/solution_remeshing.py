import brg
from brg.datastructures.network import Network
from brg.utilities import XFuncIO

import brg_rhino as rhino


xrun = XFuncIO()

network = Network.from_obj(brg.get_data('lines.obj'))

network.set_dva({
    'px': 0.0,
    'py': 0.0,
    'pz': 0.0,
    'rx': 0.0,
    'ry': 0.0,
    'rz': 0.0,
    'is_fixed': False,
})

network.set_dea({
    'q': 1.0, 'f': 0.0, 'l': 0.0
})

leaves = set(network.leaves())

for key, attr in network.vertices_iter(True):
    attr['is_fixed'] = key in leaves

rhino.draw_network(
    network,
    vertexcolor={key: (255, 0, 0) for key, attr in network.vertices_iter(True) if attr['is_fixed']},
    clear_layer=True
)

while True:
    keys = rhino.select_network_vertices(network)
    if not keys:
        break
    if not rhino.update_network_vertex_attributes(network, keys):
        break
    rhino.draw_network(
        network,
        vertexcolor={key: (255, 0, 0) for key, attr in network.vertices_iter(True) if attr['is_fixed']},
        clear_layer=True
    )

while True:
    keys = rhino.select_network_edges(network)
    if not keys:
        break
    if not rhino.update_network_edge_attributes(network, keys):
        break
    rhino.draw_network(
        network,
        vertexcolor={key: (255, 0, 0) for key, attr in network.vertices_iter(True) if attr['is_fixed']},
        clear_layer=True
    )

key_index = dict((key, index) for index, key in network.vertices_enum())

xyz   = network.get_vertices_attributes(('x', 'y', 'z'))
q     = network.get_edges_attribute('q', 1.0)
loads = network.get_vertices_attributes(('px', 'py', 'pz'))

edges = [(key_index[u], key_index[v]) for u, v in network.edges()]
fixed = [key_index[key] for key, attr in network.vertices_iter(True) if attr['is_fixed']]

fname = 'brg.numerical.methods.force_density.fd'
fargs = [xyz, edges, fixed, q, loads]

xrun(fname, *fargs, rtype='dict')

if xrun.error:
    print rhino.display_text(xrun.error)
else:
    xyz = xrun.data['xyz']
    res = xrun.data['r']
    for key, attr in network.vertices_iter(True):
        index = key_index[key]
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]
        attr['rx'] = res[index][0]
        attr['ry'] = res[index][1]
        attr['rz'] = res[index][2]
    f = xrun.data['f']
    for index, u, v, attr in network.edges_enum(True):
        attr['f'] = f[index]
    rhino.draw_network(
        network,
        vertexcolor={key: (255, 0, 0) for key, attr in network.vertices_iter(True) if attr['is_fixed']},
        clear_layer=True
    )
    rhino.display_network_axial_forces(network)
    rhino.display_network_reaction_forces(network)