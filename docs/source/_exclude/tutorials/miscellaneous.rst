.. _miscellaneous:

********************************************************************************
Miscellaneous
********************************************************************************

.. contents::


Subprocesses
============

Python has many packages (for example, paerts of NumPy and SciPy) that are wrappers
around highly optimised C or C++ or even Fortran libraries. Unfortunately, this
means that these packages are then not available in flavours of Python that are
not C-based, such as IronPython or Jython.

However, the built-in ``subprocess`` module provides an easy way around this
limitation.


.. code-block:: python

    # the external script
    # test.py

    # some imports that would throw an error in Rhino

    from scipy.interpolate import griddata
    from scipy.sparse import csr_matrix
    from scipy.optimize import minimize
    from scipy.spatial import distance_matrix

    import time

    for i in range(100):
        print i
        time.sleep(0.1)


.. code-block:: python

    # calling the script through an external process

    from subprocess import Popen
    from subprocess import PIPE

    args = ['pythonw', '-u', 'test.py']

    p = Popen(args, stderr=PIPE, stdout=PIPE)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        print line.strip()
        # this prints here whatever is being printed by the script

    stdout, stderr = p.communicate()

    print 'stdout:'
    print stdout
    print 'stderr:'
    print stderr


.. code-block:: python

    1
    2
    3
    
    ...

    97
    98
    99
    stdout:

    stderr:


.. seealso::

    * :mod:`compas.utilities.scripts`
    * :mod:`compas.utilities.xfunc`
    * :mod:`compas.utilities.xfuncio`
    * :mod:`compas_rhino.utilities.scripts`


Geometric maps
==============

Geometric maps are extremely useful for quickly identifying matching geometry.
For example, the constructor function ``from_lines`` of the ``Network`` class
uses a geometric map to identify matching point locations.

The idea is simple. A point location can be converted to a string with a certain
precision. This *geometric* key can be used to store the corresponding location
uniquely in a dictionary. This map can then be used efficiently to identify, for
example, the unique start and end points of a set of lines.


.. code-block:: python

    def geometric_key(xyz, precision='3f'):
        return '{0[0]:.{1}},{0[1]:.{1}},{0[2]:.{1}}'.format(xyz, precision)


    xyz = [1.61803, 2.71828, 3.14159]

    print geometric_key(xyz, '1f')
    print geometric_key(xyz, '2f')
    print geometric_key(xyz, '3f')

    # '1.6,2.7,3.1'
    # '1.62,2.72,3.14'
    # '1.618,2.718,3.142'

    p = [1.61903, 2.72328, 3.14259]

    print geometric_key(xyz, '1f') == geometric_key(p, '1f')
    print geometric_key(xyz, '2f') == geometric_key(p, '2f')
    print geometric_key(xyz, '3f') == geometric_key(p, '3f')

    # True
    # True
    # False


.. code-block:: python

    from compas.utilities import geometric_key

    class Network(object):

        ...

        @classmethod
        def from_lines(cls, lines, precision='3f', **kwargs):
            network = cls(**kwargs)
            edges   = []
            vertex  = {}
            for line in lines:
                sp = line[0]
                ep = line[1]
                a  = geometric_key(sp, precision)
                b  = geometric_key(ep, precision)
                vertex[a] = sp
                vertex[b] = ep
                edges.append((a, b))
            key_index = dict((k, i) for i, k in enumerate(iter(vertex)))
            for key, xyz in vertex.iteritems():
                i = key_index[key]
                network.add_vertex(i, x=xyz[0], y=xyz[1], z=xyz[2])
            for u, v in edges:
                i = key_index[u]
                j = key_index[v]
                network.add_edge(i, j)
            return network


.. important::
    
    Using geometric maps is not the same as comparing distances. By comparing
    distances, all points within a circle with a specific radius around a test
    point will match the test point. By using geometric maps, space is divided 
    into small boxes or cubes. All points within the box or cube map to the same
    location. The boxes or cubes are dicretely sized according to the specified
    float precision.


.. seealso::

    * :func:`compas.utilities.geometric_key`
    * :class:`compas.datastructures.network.Network`


File handling
=============

*under* *construction*


External software
=================

*under* *construction*

