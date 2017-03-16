.. _python-basics-2:

********************************************************************************
Basics 2
********************************************************************************

.. warning::
    
    This page is still under construction.


.. contents::


Functions
=========

Definitions
-----------

http://stackoverflow.com/questions/9872824/calling-a-python-function-with-args-kwargs-and-optional-default-arguments

.. code-block:: python

    def f():
        pass

    def f(a):
        pass

    def f(a1, a2):
        pass

    def f(a1, a2=None):
        pass

    def f(a1=None, a2):
        pass

    def f(*args):
        pass

    def f(**kwargs):
        pass

    def f(a1, a2, *args):
        pass

    def f(a1, a2, *args, **kwargs):
        pass


Variable Scope
--------------

.. code-block:: python

    globals()
    locals()


Default values
--------------

.. code-block:: python

    def f(a, b, c=[]):
        pass

    def f(a, b, c=None):
        if c is None:
            c = []

    def f(a, b, c=None):
        if not c:
            c = []

    def f(a, b, c=None):
        c = c or []


Decorators
==========


Classes
=======


.. code-block:: python

    class Vector():

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z


    class Vector():

        def __init__(self, x, y=0, z=0):
            try:
                len(x)
            except:
                x = [x, y, z]
            if len(x) == 1:
                x = [x[0], y, z]
            elif len(x) == 2:
                x = [x[0], x[1], z]
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]


    class Vector():

        def __init__(self, end, start=None):
            if not start:
                start = [0, 0, 0]
            x = end[0] - start[0]
            y = end[1] - start[1]
            z = end[2] - start[2]
            self.x = x
            self.y = y
            self.z = z


.. code-block:: python

    class Vector():
        ...

        def add(self, other):
            self.x += other.x
            self.y += other.y
            self.z += other.z


.. code-block:: python

    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)

    v1.add(v2)


.. code-block:: python

    v3 = [0, 0, 1]

    v1.add(v3)


Magic methods
-------------

.. code-block:: python

    class Vector(object):
        ...

        def __getitem__(self, key):
            i = key % 3
            if i == 0:
                return self.x
            if i == 1:
                return self.y
            if i == 2:
                return self.z
            raise KeyError

        def __setitem__(self, key, value):
            i = key % 3
            if i == 0:
                self.x = value
                return
            if i == 1:
                self.y = value
                return
            if i == 2:
                self.z = value
                return
            raise KeyError

        def __iter__(self):
            return iter([self.x, self.y, self.z])

        def add(self, other):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]


    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    v3 = [0, 0, 1]

    v1.add(v2)
    v1.add(v3)


.. code-block:: python

    class Vector(object):
        ...

        def __add__(self, other):
            return Vector([self.x + other[0], self.y + other[1], self.z + other[2]])

        def __sub__(self, other):
            return Vector([self.x - other[0], self.y - other[1], self.z - other[2]])

        def __mul__(self, n):
            return Vector([self.x * n, self.y * n, self.z * n])

        def __pow__(self, n):
            return Vector([self.x ** n, self.y ** n, self.z ** n])


    v = v1 + v2
    v = v1 + v3
    v = v1 * 2
    v = v1 ** 2


Descriptors
-----------

`Descriptor HowTo Guide <https://docs.python.org/2/howto/descriptor.html>`_


.. code-block:: python

    class Vector(object):

        def __init__(self, end, start=None):
            self._x = None
            self._y = None
            self._z = None
            if not start:
                start = [0, 0, 0]
            x = end[0] - start[0]
            y = end[1] - start[1]
            z = end[2] - start[2]
            self.x = x
            self.y = y
            self.z = z

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, x):
            self._x = float(x)

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, y):
            self._y = float(y)

        @property
        def z(self):
            return self._z

        @z.setter
        def z(self, z):
            self._z = float(z)


.. code-block:: python

    class Vector(object):
        ...

        @property
        def length(self):
            return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5


Classmethods
------------

.. code-block:: python

    class Vector(object):

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        @classmethod
        def from_points(cls, start, end):
            x = end[0] - start[0]
            y = end[1] - start[1]
            z = end[2] - start[2]
            return cls(x, y, z)


    v = Vector.from_points([1, 0, 0], [2, 0, 0])


Meta Classes
------------


Abstract Base Classes
---------------------

.. code-block:: python

    from abc import ABCMeta
    from abc import abstractmethod


    class Vector(object):

        __metaclass__ = ABCMeta

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        ...

        @abstractmethod
        def add(self, other):
            # raise NotImplementedError
            pass


    class Vector2(Vector):

        def add(self, other):
            ...


    class Vector3(Vector):

        def add(self, other):
            ...


Exceptions
==========


Duck Typing
===========


Miscellaneous
=============

