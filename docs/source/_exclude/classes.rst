.. _python-classes:

********************************************************************************
Classes
********************************************************************************


.. contents::


Class definition
================

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
===========

Descriptors provide a way to control how the attributes of an object are accessed.
For example, they can be used to create read-only attributes, or to make sure that
the value of an attribute is always of a specific type.


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
=============

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
============

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


Meta Classes
============

*Under construction*


