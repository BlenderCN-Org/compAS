.. _cablenet:

********************************************************************************
Equilibrium of a Cablenet in Rhino
********************************************************************************

.. contents::


As a script
===========

.. code-block:: python

    import brg
    from brg.datastructures.network import Network
    from brg.utilities import XFuncIO

    import brg_rhino as rhino


    class Cablenet(Network):

        def __init__(self):
            super(Cablenet, self).__init__()
            self.dva.update({
                'px': 0.0,
                'py': 0.0,
                'pz': 0.0,
                'rx': 0.0,
                'ry': 0.0,
                'rz': 0.0,
                'is_fixed': False,
            })
            self.dea.update({'q': 1.0, 'f': 0.0, 'l': 0.0})

        def draw(self):
            rhino.draw_network(
                self,
                vertexcolor={key: (255, 0, 0) for key, attr in self.vertices_iter(True) if attr['is_fixed']},
                clear_layer=True
            )

        def draw_forces(self):
            rhino.display_network_axial_forces(self, True)

        def draw_reaction_forces(self):
            rhino.display_network_reaction_forces(self, True)


    xrun = XFuncIO()

    cablenet = Cablenet.from_obj(brg.get_data('lines.obj'))

    leaves = set(cablenet.leaves())

    for key, attr in cablenet.vertices_iter(True):
        attr['is_fixed'] = key in leaves

    cablenet.draw()

    while True:
        keys = rhino.select_network_vertices(cablenet)
        if not keys:
            break
        if not rhino.update_network_vertex_attributes(cablenet, keys):
            break
        cablenet.draw()

    while True:
        keys = rhino.select_network_edges(cablenet)
        if not keys:
            break
        if not rhino.update_network_edge_attributes(cablenet, keys):
            break
        cablenet.draw()

    key_index = dict((key, index) for index, key in cablenet.vertices_enum())

    xyz   = [cablenet.vertex_coordinates(key) for key in cablenet]
    edges = [(key_index[u], key_index[v]) for u, v in cablenet.edges()]
    fixed = [key_index[key] for key, attr in cablenet.vertices_iter(True) if attr['is_fixed']]
    q     = cablenet.get_edges_attribute('q', 1.0)
    loads = cablenet.get_vertices_attributes(('px', 'py', 'pz'))

    fname = 'brg.numerical.methods.force_density.fd'
    fargs = [xyz, edges, fixed, q, loads]

    xrun(fname, *fargs, rtype='dict')

    if xrun.error:
        print rhino.display_text(xrun.error)
    else:
        xyz = xrun.data['xyz']
        res = xrun.data['r']
        for key, attr in cablenet.vertices_iter(True):
            index = key_index[key]
            attr['x'] = xyz[index][0]
            attr['y'] = xyz[index][1]
            attr['z'] = xyz[index][2]
            attr['rx'] = res[index][0]
            attr['ry'] = res[index][1]
            attr['rz'] = res[index][2]
        f = xrun.data['f']
        for index, u, v, attr in cablenet.edges_enum(True):
            attr['f'] = f[index]
        cablenet.draw()
        cablenet.draw_forces()
        cablenet.draw_reaction_forces()


