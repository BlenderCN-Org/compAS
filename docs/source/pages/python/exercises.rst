.. _python-exercises:

********************************************************************************
Exercises
********************************************************************************

.. highlight:: python


Questions
=========

1.  Construct a list of odd numbers below 20 and then reverse the list in place.
    
    * Don't use *reverse* or *reversed*.


2.  Given two lists of 3D points (xyz coordinates), find the locations in the
    second list that also exist in the first.
    
    * Use a tolerance of ``1e-3``.


3.  Define a function that takes:
    
    * two positional arguments,
    * one optional argument with default value ``None``, and
    * an unknown number of additional keyword arguments.


4.  Demonstrate the principle of a cyclic list. Given a list of length ``n``,
    allow for indexing by ``m >= n`` and ``m <= -n``.

5.  Construct a list ``c`` with all elements in ``b`` that are not in ``a``.

    .. code-block:: python

        a = ...
        b = ...


6.  Construct a list ``c`` with all elements in ``b`` that are not in ``a``,
    while preserving the order of elements in ``b``.

    .. code-block:: python

        a = ...
        b = ...


7.  Construct a list of 1000 random integers between 1 and 1000000. Find the index
    of the item with the highest value.

8.  Define a class with a method that behaves as if it is abstract.

9.  Define a class with alternative constructors that can be called explicitly.

    .. code-block:: python

        o = MyClass()
        o = MyClass.from_xxx()
        o = MyClass.from_yyy()


10. Define a vector class that supports the following operations.

    .. code-block:: python
        
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2, 3)
        v3 = v1 + v2
        v3 * 2


11. Write a function that does a counter-clockwise check of 3 points A, B, C.

    * A, B, C are in the xy-plane (i.e. z=0)
    * the function should return True if the rotation from vector AB onto AC is counter-clockwise.


12. Write a (memoized) recursive fibonacci function.

13. Write a function that does a breadth-first seach of a given network
    starting at a given root element.

    * The network is given as a dictionary of adjacencies: nbrs = adjacency[node].
    * Return a list of nodes in breadth-first order.


14. Write a simple bubble sort function.


Answers
=======

::

    a = range(1, 20, 2)
    a[:] = a[::-1]

::

    points = []
    lookup = dict(('{0[0]:.3f},{0[1]:.3f},{0[2]:.3f}'.format(xyz), i) for i, xyz in enumerate(points))

::

    def f(arg1, arg2, arg3=None, **kwargs):
        pass

::

    a = [0, 1, 2]
    item = a[5 % len(a)]

::

    a = [1, 4, 7, 9, 12, 19, 13, 3, 2]
    b = range(20)
    c = list(set(b) - set(a))


::

    a = set(a)
    c = [x for x in b if x not in a]

::

    from random import randint

    a = dict((randint(1, 1000000), i) for i in range(1000))
    k, v = sorted(a.items(), key=lambda x: x[1])[-1]

::

    class MyAbstractClass(object):
        def method(self):
            raise NotImplementedError

::

    class MyClass(object):
        def __init__(self):
            pass

        @classmethod
        def from_xxx(cls):
            return cls()

        @classmethod
        def from_yyy(cls):
            return cls()


::

    class Vector(object):

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        def __add__(self, other):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
            return Vector(x, y, z)

        def __mul__(self, n):
            self.x *= n
            self.y *= n
            self.z *= n

::

    def ccw_(A, B, C):
        return (B[0] - A[0]) * (C[1] - A[1]) > (B[1] - A[1]) * (C[0] - A[0])

::

    def rfib(n, memo={}):
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n not in memo:
            memo[n] = rfib(n - 2) + rfib(n - 1)
        return memo[n]

