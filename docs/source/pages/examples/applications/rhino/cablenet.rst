.. _cablenet:

********************************************************************************
Equilibrium of a Cablenet
********************************************************************************

.. contents::


Using a script
==============

.. code-block:: python

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


Using a custom class
====================


.. code-block:: python

    import brg
    from cablenet import Cablenet


    cablenet = Cablenet.from_obj(brg.get_data('lines.obj'))

    cablenet.set_fixed_vertices(cablenet.leaves())

    cablenet.draw()

    cablenet.update_vertex_attributes()
    cablenet.update_edge_attributes()
    cablenet.update_equilibrium()

    cablenet.draw_forces()
    cablenet.draw_reaction_forces()


.. code-block:: python

    # cablenet.py

    from brg.datastructures.network import Network
    from brg.utilities.xfuncio import XFuncIO

    import brg_rhino as rhino


    xrun = XFuncIO()


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

        @property
        def xyz(self):
            return self.get_vertices_attributes(('x', 'y', 'z'))

        @property
        def q(self):
            return self.get_edges_attribute('q')

        @property
        def loads(self):
            return self.get_vertices_attributes(('px', 'py', 'pz'))

        @property
        def ij(self):
            k_i = dict((k, i) for i, k in self.vertices_enum())
            return [(k_i[u], k_i[v]) for u, v in self.edges_iter()]

        @property
        def fixed(self):
            k_i = dict((k, i) for i, k in self.vertices_enum())
            return [k_i[k] for k, attr in cablenet.vertices_iter(True) if attr['is_fixed']]         

        def update_vertex_attributes(self):
            while True:
                keys = rhino.select_network_vertices(self)
                if not keys:
                    break
                if not rhino.update_network_vertex_attributes(self, keys):
                    break
                self.draw()

        def update_edge_attributes(self):
            while True:
                keys = rhino.select_network_edges(self)
                if not keys:
                    break
                if not rhino.update_network_edge_attributes(self, keys):
                    break
                self.draw()

        def set_fixed_vertices(self, keys):
            keys = set(keys)
            for key, attr in self.vertices_iter(True):
                attr['is_fixed'] = key in keys

        def update_equilibrium(self):
            k_i   = dict((k, i) for i, k in self.vertices_enum())
            fname = 'brg.numerical.methods.force_density.fd'
            fargs = [self.xyz, self.ij, self.fixed, self.q, self.loads]

            xrun(fname, *fargs, rtype='dict')

            if xrun.error:
                print rhino.display_text(xrun.error)
            else:
                xyz = xrun.data['xyz']
                res = xrun.data['r']
                for key, attr in self.vertices_iter(True):
                    index = k_i[key]
                    attr['x'] = xyz[index][0]
                    attr['y'] = xyz[index][1]
                    attr['z'] = xyz[index][2]
                    attr['rx'] = res[index][0]
                    attr['ry'] = res[index][1]
                    attr['rz'] = res[index][2]
                f = xrun.data['f']
                for index, u, v, attr in self.edges_enum(True):
                    attr['f'] = f[index]
                self.draw()

        def draw(self):
            rhino.draw_network(
                self,
                vertexcolor={key: (255, 0, 0) for key, attr in self.vertices_iter(True) if attr['is_fixed']},
                clear_layer=True
            )

        def draw_forces(self):
            rhino.display_network_axial_forces(self, True, scale=0.1)

        def draw_reaction_forces(self):
            rhino.display_network_reaction_forces(self, True)


Using geometric input
=====================

.. code-block:: python
    
    import ast

    from brg.utilities import geometric_key as gkey
    from cablenet import Cablenet

    import brg_rhino as rhino

    guids = rhino.select_lines()
    lines = rhino.get_line_coordinates(guids)
    names = rhino.get_object_names(guids)

    cablenet = Cablenet.from_lines(lines)

    xyz_key = dict((gkey(cablenet.vertex_coordinates(key)), key) for key in cablenet)

    for i, guid in enumerate(guids):
        name = names[i]

        try:
            attr = ast.literal_eval(name)
        except:
            continue

        sp, ep = lines[i]

        u = xyz_key[gkey(sp)]
        v = xyz_key[gkey(ep)]

        if v in self.edge[u]:
            cablenet.edge[u][v].update(attr)
        else:
            cablenet.edge[v][u].update(attr)

    cablenet.draw()


Using a toolbar
===============

*under* *construction*

