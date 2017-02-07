.. _python:

********************************************************************************
Python
********************************************************************************

.. contents::

.. magic methods


Lists and Dicts
===============

.. code-block:: python

    import random

    facelist = [0, 1, 2, 3]
    facedict = {0: 1, 1: 2, 2: 3, 3: 0}


.. code-block:: python

    # edges of the face

    # facelist

    for i in range(-1, len(facelist) - 1):
        u = facelist[i]
        v = facelist[i + 1]
        print u, v

    # facedict

    start = u = facedict.iterkeys().next()

    while True:
        v = facedict[u]
        print u, v
        if v == start:
            break
        u = v


.. code-block:: python
  
    # descendant of a vertex

    # facelist

    u = random.choice(facelist)
    i = facelist.index(u) + 1
    v = facelist[i]

    # what if u == 3?

    n = len(facelist)
    i = facelist.index(u) + 1
    v = facelist[i % n]

    # facedict

    u = random.choice(facedict)
    v = facedict[u]


.. code-block:: python

    # ancestor of a vertex

    # facelist

    v = random.choice(facelist)
    i = facelist.index(v) - 1
    u = facelist[i]

    # facedict

    rfacedict = {v: u for u, v in facedict.iteritems()}

    v = random.choice(facedict)
    u = rfacedict[v]


.. code-block:: python

    # path from one vertex to another

    # facelist

    u = random.choice(facelist)
    v = random.choice(facelist)

    i = face.index(u)
    j = face.index(v)

    if j > i:
        path = face[i:j + 1]
    else:
        path = face[i:] + face[:j + 1]

    # facedict

    u = random.choice(facedict)
    v = random.choice(facedict)

    path = [u]

    while True:
        u = facedict[u]
        path.append(u)
        if u == v:
            break


Sets
====

.. code-block:: python

    import random

    items = random.sample(xrange(1000000), 10000)
    exclude = random.sample(xrange(1000000), 10000)

    result = [item for item in items if item not in exclude]


.. code-block:: python

    exclude = set(exclude)

    result = [item for item in items if item not in exclude]


.. code-block:: python
  
    items = set(items)
    exclude = set(exclude)

    result = list(items - exclude)


Sorting
=======

.. code-block:: python
  
    import random

    items = random.sample(xrange(20), 20)

    print sorted(items)

    items = [str(item) for item in items]

    print sorted(items)
    print sorted(items, key=int)


.. code-block:: python

    keys = random.sample(xrange(20), 20)
    values = random.sample(xrange(20, 40), 20)

    d = dict(zip(keys, values))

    print d
    print sorted(d)

    result = sorted(d.items(), key=lambda item: item[1])

    print result
    print zip(*result)


Defaults
========

.. code-block:: python

    def func(a, b, c=1):
        pass


.. code-block:: python

    def func(a, b, c=None):
        if not c:
            c = 1


.. code-block:: python

    def func(a, b, c=None):
        c = c or 1


.. code-block:: python

    def func(a, b, **kwargs):
        c = kwargs.get('c', 1)
        print c

    func(a, b)
    func(a, b, c=None)


.. code-block:: python

    def func(a, b, **kwargs):
        c = kwargs.get('c') or 1
        print c

    func(a, b, c=None)


Descriptors
===========

.. seealso::

    :class:`brg.datastructures.mesh.Mesh`
    :class:`brg.datastructures.network.Network`
    :class:`brg.datastructures.volmesh.VolMesh`


Decorators
==========

.. seealso::

    :func:`brg.utilities.profiling.print_profile`


Profiling
=========

