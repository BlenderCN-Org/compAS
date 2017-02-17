from importlib import import_module

modules = [
    'brg',
    'brg.com',
    'brg.datastructures',
    'brg.datastructures.mesh',
    'brg.datastructures.network',
    'brg.datastructures.tree',
    'brg.datastructures.volmesh',
    'brg.files',
    'brg.geometry',
    'brg.numerical',
    'brg.numerical.euler',
    'brg.numerical.gpu',
    'brg.numerical.methods',
    'brg.numerical.solvers',
    'brg.physics',
    'brg.plotters',
    'brg.utilities',
    'brg.viewers',
    'brg.web',
    'brg.xlibs',

    'brg_blender',
    'brg_grasshopper',

    'brg_rhino',
    'brg_rhino.conduits',
    'brg_rhino.forms',
    'brg_rhino.geometry',
    'brg_rhino.helpers',
    'brg_rhino.numerical',
    'brg_rhino.ui',
    'brg_rhino.utilities',
]


for name in modules:
    obj = import_module(name)

    print obj

    with open('source/pages/reference/{0}.rst'.format(name), 'wb+') as fp:
        fp.write(obj.__doc__)
