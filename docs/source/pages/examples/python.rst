.. _python:

********************************************************************************
Python
********************************************************************************


:download:`py-exercises.py </_downloads/py-exercises.py>`


.. contents::


Lists
=====

.. code-block:: python

    polygon = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 0 1
    # 1 2
    # 2 3
    # 3 4
    # 4 5
    # 5 6
    # 6 7
    # 7 8
    # 8 9
    # 9 0


.. code-block:: python

    # edges

    for i in range(-1, len(polygon) - 1):
        u = face[i]
        v = face[i + 1]
        print u, v


.. code-block:: python

    # descendants

    import random
  
    u = random.choice(polygon)
    i = polygon.index(u)
    j = i + 1
    v = polygon[i]


.. code-block:: python

    # ancestors

    v = random.choice(polygon)
    j = polygon.index(v)
    i = j - 1
    u = polygon[i]


.. code-block:: python

    # paths

    u = random.choice(polygon)
    v = random.choice(polygon)

    i = polygon.index(u)
    j = polygon.index(v)

    if j > i:
        path = face[i:j + 1]
    else:
        path = face[i:] + face[:j + 1]


.. rubric:: Exercise

What happens when we are looking for the vertex of the polygon that comes after ``9``?


.. code-block:: python

    u = 9
    i = polygon.index(u)
    j = i + 1
    v = polygon[j]


.. code-block:: python
    
    n = len(polygon)
    u = 9
    i = polygon.index(u)
    j = (i + 1) % n
    v = polygon[j]


Dicts
=====

.. what
.. unique keys
.. key types
.. hashable
.. what for


.. warning::

    This section is still under construction.


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


Classes
=======

.. warning::

    This section is still under construction.


.. code-block:: python

    class Vector(object):

        def __init__(self, x, y):
            self.x = x
            self.y = y


.. code-block:: python

    u = Vector(0, 1)

    print u.x
    print u.y


Descriptors
-----------

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


Magic methods
-------------

Magic methods (*dunder* methods, i.e. methods with double underscores at the beginning
and end), allow you to modify the default behaviour of an object.

.. code-block:: python
    :emphasize-lines: 3,23,26,31,34,39,42,47,50

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

        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)

        def __iadd__(self, other):
            self.x += other.x
            self.y += other.y
            return self

        def __sub__(self, other):
            return Vector(self.x - other.x, self.y - other.y)

        def __isub__(self, other):
            self.x -= other.x
            self.y -= other.y
            return self

        def __mul__(self, n):
            return Vector(self.x * n, self.y * n)

        def __imul__(self, n):
            self.x *= n
            self.y *= n
            return self

        def __pow__(self, n):
            return Vector(self.x ** n, self.y ** n)

        def __ipow__(self, n):
            self.x **= n
            self.y **= n
            return self


.. code-block:: python
    :emphasize-lines: 23-39

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

        def __getitem__(self, key):
            i = key % 2
            if i == 0:
                return self.x
            if i == 1:
                return self.y
            raise KeyError

        def __setitem__(self, key, value):
            i = key % 2
            if i == 0:
                self.x = value
                return
            if i == 1:
                self.y = value
                return
            raise KeyError

        def __iter__(self):
            return iter([self.x, self.y])

        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)

        def __iadd__(self, other):
            self.x += other.x
            self.y += other.y
            return self

        def __sub__(self, other):
            return Vector(self.x - other.x, self.y - other.y)

        def __isub__(self, other):
            self.x -= other.x
            self.y -= other.y
            return self

        def __mul__(self, n):
            return Vector(self.x * n, self.y * n)

        def __imul__(self, n):
            self.x *= n
            self.y *= n
            return self

        def __pow__(self, n):
            return Vector(self.x ** n, self.y ** n)

        def __ipow__(self, n):
            self.x **= n
            self.y **= n
            return self


.. code-block:: python
    :emphasize-lines: 44-58

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

        def __getitem__(self, key):
            i = key % 2
            if i == 0:
                return self.x
            if i == 1:
                return self.y
            raise KeyError

        def __setitem__(self, key, value):
            i = key % 2
            if i == 0:
                self.x = value
                return
            if i == 1:
                self.y = value
                return
            raise KeyError

        def __iter__(self):
            return iter([self.x, self.y])

        def __add__(self, other):
            return Vector(self.x + other[0], self.y + other[1])

        def __iadd__(self, other):
            self.x += other[0]
            self.y += other[1]
            return self

        def __sub__(self, other):
            return Vector(self.x - other[0], self.y - other[1])

        def __isub__(self, other):
            self.x -= other[0]
            self.y -= other[1]
            return self

        def __mul__(self, n):
            return Vector(self.x * n, self.y * n)

        def __imul__(self, n):
            self.x *= n
            self.y *= n
            return self

        def __pow__(self, n):
            return Vector(self.x ** n, self.y ** n)

        def __ipow__(self, n):
            self.x **= n
            self.y **= n
            return self


Classmethods
------------

Class methods can be used to create alternative constructor functions.
These provide an explicit equivalent of the constructor overloading functionality
found in other languages.


.. code-block:: python
    
    class Vector(object):

        ...

        @classmethod
        def from_points(cls, a, b):
            dx = b[0] - a[0]
            dy = b[1] - a[1]
            return cls(dx, dy)

