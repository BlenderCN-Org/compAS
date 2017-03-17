.. _python-exercises:

********************************************************************************
Exercises
********************************************************************************

.. note::

    More exercises will be added in the future.


Construct a list of odd numbers below 20 and then reverse the list in place,
without using *reverse* or *reversed*.

.. code-block:: python

    odd = range(1, 20, 2)
    # odd = [i for i in range(20) if i % 2]

    odd[:] = odd[::-1]


-----


Given a list of 3D points (xyz coordinates),
construct a lookup table that links 3D locations to items in the list.

Use a tolerance of ``.3f``

For example, if the list contains point ``(1.2345, 2.4325, 1.3456)`` at index 5, 
the lookup should return 5 for point ``(1.2346, 2.4328, 1.3457)``

.. code-block:: python

    import random

    points = [(random.randint(10000, 99000) / 10000., 
               random.randint(10000, 99000) / 10000., 
               random.randint(10000, 99000) / 10000.) for i in range(10)]

    points[5] = (1.2345, 2.4325, 1.3456)

    lookup = dict(('{0[0]:.3f},{0[1]:.3f},{0[2]:.3f}'.format(xyz), index) for index, xyz in enumerate(points))

    key = '{0[0]:.3f},{0[1]:.3f},{0[2]:.3f}'.format(points[5])
    print lookup[key]


-----


Define a (dummy) function that takes:

* 2 positional arguments
* 1 optional argument with default value ``None``
* an unknown number of additional keyword arguments

.. code-block:: python

    def f(a, b, c=None, **d):
        pass


-----


Demonstrate the principle of a cyclic list.

* given a list of length n
* allow for indexing by ``m >= n`` and ``m <= -n``
* n = 6
* items[6]
* items[600]
* items[-9]
* items[-3000]

.. code-block:: python

    a = range(10)

    print a[12 % len(a)]

    class CyclicList(object):
        def __init__(self, items):
            self.items = items

        def __getitem__(self, key):
            return self.items[key % len(self.items)]

    c = CyclicList(range(10))
    print c[20]


-----


Construct a list *c* with all element in *b* that are not in *a*.

.. code-block:: python

    a = range(1, 100, 2)
    b = range(1, 100)

    c = set(b) - set(a)


-----


Construct a list *c* with all element in *b* that are not in *a*,
but while preserving the order of the elements in *b*.

.. code-block:: python

    a = range(1, 100, 2)
    b = range(1, 100)
    a = set(a)
    c = [x for x in b if x not in a]


-----


Construct a list of 1000 random integers between 1 and 10000000.
Then find the index of the item with the highest value.

.. code-block:: python

    import random

    items = [random.randint(1, 10000000) for i in range(1000)]
    k, v  = sorted(enumerate(items), key=lambda x: x[1])[-1]

    items = dict((index, randint(1, 1000000)) for index in range(1000))
    k, v  = sorted(items.items(), key=lambda x: x[1])[-1]


-----


Write a function that returns ``True`` if the rotation from AB onto AC is CCW.
A, B, C are points in the xy-plane...

.. code-block:: python

    def is_ccw(A, B, C):
        return (B[0] - A[0]) * (C[1] - A[1]) > (B[1] - A[1]) * (C[0] - A[0])


-----


Write a function that returns the nth number in the fibonacci series.

.. code-block:: python

    def fib(n):
        # if n == 1: return 1
        # if n == 2: return 1
        a, b = 1, 1
        for i in range(n - 1):
            a, b = b, a + b
        return a


-----


Write a recursive version of the fibonacci function.

.. code-block:: python

    def rfib(n):
        if n == 1: return 1
        if n == 2: return 1
        return rfib(n-2) + rfib(n-1)


-----


Write a memoized version of the recursive fibonacci function.

.. code-block:: python

    def mrfib(n, memo={}):
        if n == 1: return 1
        if n == 2: return 1
        if n not in memo:
            memo[n] = mrfib(n-2, memo) + mrfib(n-1, memo)
        return memo[n]


