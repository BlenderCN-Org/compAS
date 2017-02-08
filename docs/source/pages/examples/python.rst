.. _python:

********************************************************************************
Python
********************************************************************************

.. contents::

.. magic methods
.. integrate andrew's comments


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


Descriptors
===========

.. code-block:: python

    class Vector(object):

        def __init__(self, x, y):
            self.x = x
            self.y = y

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = float(value)

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, value):
            self._y = float(value)


.. code-block:: python

    class Vector(object):

        def __init__(self, x, y):
            self._x = float(x)
            self._y = float(y)

        @property
        def x(self):
            return self._x

        @property
        def y(self):
            return self._y


.. code-block:: python

    class Vector(object):

        ...

        @property
        def xy(self):
            return self.x, self.y

        @property
        def length(self):
            return (self.x ** 2 + self.y ** 2) ** 0.5


.. code-block:: python

    vector = Vector(0, 2)

    print vector.xy
    # 0.0 2.0

    print vector.length
    # 2.0    


.. seealso::

    https://docs.python.org/2/reference/datamodel.html#descriptors

    * :mod:`brg.geometry.elements`

    * :class:`brg.datastructures.mesh.Mesh`
    * :class:`brg.datastructures.network.Network`
    * :class:`brg.datastructures.volmesh.VolMesh`


Profiling
=========

.. code-block:: python

    import cProfile
    import pstats

    profile = cProfile.Profile()
    profile.enable()

    for i in range(10):
        print i

    profile.disable()

    stats  = pstats.Stats(profile)
    stats.strip_dirs()
    stats.sort_stats(1)
    stats.print_stats(20)


Decorators
==========

.. rename profiling to code(analysis)

.. code-block:: python

    import cProfile
    import pstats

    from functools import wraps

    def print_profile(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profile = cProfile.Profile()
            profile.enable()
            #
            res = func(*args, **kwargs)
            #
            profile.disable()
            stats = pstats.Stats(profile)
            stats.strip_dirs()
            stats.sort_stats(1)
            stats.print_stats(20)
            return res
        return wrapper

    @print_profile
    def silly():
        for i in range(10):
            print i

    silly()


.. seealso::

    :func:`brg.utilities.profiling.print_profile`

