import compas

from compas.datastructures.network import Network
from compas.datastructures.network.algorithms import network_dijkstra_path

network = Network.from_obj(compas.get_data('grid_irregular.obj'))

weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

start = 21
end = 22

path = network_dijkstra_path(network.adjacency, weight, start, end)

edges = []
for i in range(len(path) - 1):
    u = path[i]
    v = path[i + 1]
    if v not in network.edge[u]:
        u, v = v, u
    edges.append([u, v])

network.plot(
    vlabel={key: key for key in (start, end)},
    vcolor={key: (255, 0, 0) for key in (path[0], path[-1])},
    vsize=0.15,
    ecolor={(u, v): (255, 0, 0) for u, v in edges},
    ewidth={(u, v): 2.0 for u, v in edges},
    elabel={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()}
)
