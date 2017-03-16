from importlib import import_module

modules = [
    'compas',
    'compas.com',
    'compas.datastructures',
    'compas.datastructures.mesh',
    'compas.datastructures.network',
    'compas.datastructures.volmesh',
    'compas.files',
    'compas.geometry',
    'compas.numerical',
    'compas.numerical.euler',
    'compas.numerical.gpu',
    'compas.numerical.methods',
    'compas.numerical.solvers',
    'compas.physics',
    'compas.plotters',
    'compas.utilities',
    'compas.viewers',
    'compas.web',
    'compas.xlibs',

    'compas_blender',
    'compas_grasshopper',

    'compas_rhino',
    'compas_rhino.conduits',
    'compas_rhino.forms',
    'compas_rhino.geometry',
    'compas_rhino.helpers',
    'compas_rhino.numerical',
    'compas_rhino.ui',
    'compas_rhino.utilities',
]


for name in modules:
    obj = import_module(name)

    print obj

    with open('source/pages/core/{0}.rst'.format(name), 'wb+') as fp:
        fp.write(obj.__doc__)
