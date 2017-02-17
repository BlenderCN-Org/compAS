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


.. code-block:: python

    3 0
    0 1
    1 2
    2 3


.. code-block:: python

    # edges of the face

    # facedict

    start = u = facedict.iterkeys().next()

    while True:
        v = facedict[u]
        print u, v
        if v == start:
            break
        u = v


.. code-block:: python

    0 1
    1 2
    2 3
    3 0


.. code-block:: python
  
    # descendant of a vertex

    # facelist

    u = random.choice(facelist)
    i = facelist.index(u) + 1
    v = facelist[i]

    # what if u == 3?

    u = 3
    n = len(facelist)
    i = facelist.index(u) + 1
    v = facelist[i % n]


.. code-block:: python
  
    # descendant of a vertex

    # facedict

    u = random.choice(facedict)
    v = facedict[u]


.. code-block:: python

    # ancestor of a vertex

    # facelist

    v = random.choice(facelist)
    i = facelist.index(v) - 1
    u = facelist[i]


.. code-block:: python

    # ancestor of a vertex

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


.. code-block:: python

    # path from one vertex to another

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


.. code-block:: python

    import random
    import timeit

    def filter_list():
        items = random.sample(xrange(1000000), 10000)
        exclude = random.sample(xrange(1000000), 10000)
        result = [item for item in items if item not in exclude]

    def filter_set():
        items = random.sample(xrange(1000000), 10000)
        exclude = random.sample(xrange(1000000), 10000)
        exclude = set(exclude)
        result = [item for item in items if item not in exclude]


    if __name__ == "__main__":

        t0 = timeit.timeit("filter_list()", "from __main__ import filter_list", number=100)
        t1 = timeit.timeit("filter_set()", "from __main__ import filter_set", number=100)

        print t0
        print t1

::

    138
    0.8


Sorting
=======

.. code-block:: python
  
    import random

    items = random.sample(xrange(20), 20)

    print sorted(items)


::

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


.. code-block:: python

    items = [str(item) for item in items]

    print sorted(items)
    print sorted(items, key=int)


::

    ['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '3', '4', '5', '6', '7', '8', '9']
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']


.. code-block:: python

    keys = random.sample(xrange(20), 10)
    values = random.sample(xrange(20, 40), 10)

    d = dict(zip(keys, values))

    print d
    print sorted(d)


::

    {0: 33, 1: 31, 2: 30, 3: 38, 8: 39, 10: 25, 11: 36, 12: 20, 16: 35, 17: 23}
    [0, 1, 2, 3, 8, 10, 11, 12, 16, 17]


.. code-block:: python

    result = sorted(d.items(), key=lambda item: item[1])

    print result
    print zip(*result)


::

    [(12, 20), (17, 23), (10, 25), (2, 30), (1, 31), (0, 33), (16, 35), (11, 36), (3, 38), (8, 39)]
    [(12, 17, 10, 2, 1, 0, 16, 11, 3, 8), (20, 23, 25, 30, 31, 33, 35, 36, 38, 39)]


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

    * :mod:`brg.geometry.elements`
    * :class:`brg.datastructures.mesh.Mesh`
    * :class:`brg.datastructures.network.Network`
    * :class:`brg.datastructures.volmesh.VolMesh`


Profiling
=========

Although this is typically not really necessary, we all like ourt code to be fast,
and therefore spend many hours optimising it as much as possible. Unfortunately,
our alforithms are often slowed down the most by unexpected procedures and functions.
According to some, premature optimisation is the source of all evil.
Whether this is true or not, it is a good idea to profile before you optimise;
and Pyhton's standard library provides a few modules that make this very simple.


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


.. code-block:: python

    @print_profile
    def silly():
        for i in range(10):
            print i

    silly()


::

    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
             3 function calls in 0.000 seconds

       Ordered by: internal time

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 test.py:22(silly)
            1    0.000    0.000    0.000    0.000 {range}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



.. seealso::

    * :mod:`brg.utilities.profiling`
    * :mod:`brg.utilities.scripts`
    * :mod:`brg.utilities.xfunc`
    * :mod:`brg.utilities.xfuncio`


Classmethods
============

Class methods can be used to create alternative constructor functions.
These provide an explicit equivalent of the constructor overloading functionality
found in other languages.

.. add factory classmethods
.. => objects of the base type, but with different da

.. code-block:: python
    
    class Network(object):

        def __init__(self):
            # the default "constructor"
            pass

        @classmethod
        def from_obj(cls, filepath):
            # alternative constructor 1
            network = cls()
            # do stuff to initialise the network
            return network

        @classmethod
        def from_lines(cls, lines):
            # alternative constructor 2
            network = cls()
            # do stuff to initialise the network
            return network


.. code-block:: python

    def network_from_obj(cls, filepath):
        # alternative constructor 1
        network = cls()
        # do stuff to initialise the network
        return network

    class Network(object):

        def __init__(self):
            # the default "constructor"
            pass

    Network.from_obj = classmethod(network_from_obj)


Magic methods
=============

Magic methods (*dunder* methods, i.e. methods with double underscores at the beginning
and end), allow you to modify the default behaviour of an object.

.. code-block:: python

    class Network(object):

        ...

        def __contains__(self, key):
            # if key in network: ...
            return key in self.vertex

        def __len__(self):
            # len(network)
            return len(self.vertex)

        def __iter__(self):
            # for key in network: ...
            return iter(self.vertex)

        def __getitem__(self, key):
            # network[key]
            return self.vertex[key]

        def __str__(self):
            # print network
            return "Hello, i am a network :)"

