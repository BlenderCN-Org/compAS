.. _python-basics-1:

********************************************************************************
Basics 1
********************************************************************************


.. note::
    
    The topics and code snippets on this page have little accompanying explanations,
    for now. We hope to change this in the future. Until then, Try to make the
    most of what is already there... Your patience and understanding is much
    appreciated! 


.. contents::


Implementations
===============

https://wiki.python.org/moin/PythonImplementations


CPython
-------

`The Official Python Documentation <https://docs.python.org/2/index.html>`_

.. code-block:: python

    # many packages are wrappers around powerful C/C++ libraries

    import sys
    import os

    import ctypes
    import cProfile
    import scipy
    import numpy
    import shapely


IronPython
----------

`IronPython .NET integration <http://ironpython.net/documentation/dotnet/>`_

.. code-block:: python

    # packages that are wrappers for C/C++ code are not available
    # access to Windows ecosystem

    import sys
    import os

    import System
    import System.Windows.Forms
    import System.Drawing.Image
    import System.Environment.NewLine


Jython
------

`The Definitive Guide to Jython <http://www.jython.org/jythonbook/en/1.0/index.html>`_

.. code-block:: python

    # packages that are wrappers for C/C++ code are not available
    # access to Java ecosystem

    import sys
    import os

    from java.lang import System
    from java.util import Vector
    from java.io import FileOuputStream


Interactive Console
===================

Windows
-------


Mac
---


Built-in functions
==================

.. code-block:: python

    # dir

    import sys

    for name in dir(sys):
        print name


.. code-block:: python
    
    # enumerate

    abc = ['a', 'b', 'c']

    i = 0
    for letter in abc:
        print i, letter
        i += 1

    for i in range(len(abc)):
        letter = abc[i]
        print i, letter

    for i, letter in enumerate(abc):
        print i, letter


.. code-block:: python

    # format

    # https://docs.python.org/2/library/string.html#formatspec
    # http://stackoverflow.com/questions/16683518/why-does-python-have-a-format-function-as-well-as-a-format-method

    format(3.14159, 'f')
    format(3.14159, 'g')
    format(3.14159, 'n')
    format(3.14159, 'e')
    format(3.14159, '')

    '{0:f}'.format(3.14159)
    '{0:.3f}'.format(3.14159)
    '{0:.0f}'.format(3.14159)

    xyz = (1, 2, 3)

    '{0[0]},{0[1]},{0[2]}'.format(xyz)
    '{0},{1},{2}'.format(*xyz)

    xyz = {'x': 1, 'y': 2, 'z': 3}

    '{x},{y},{z}'.format(xyz)


.. code-block:: python

    # map

    # see also: list comprehensions

    pi = 3.14159

    map(str, [1, 2, 3])
    map(round, [pi, pi, pi], [1, 2, 3])
    map(pow, [1, 2, 3], [3, 3, 3])


.. code-block:: python

    # range

    numbers = range(10)
    numbers = range(1, 10)
    numbers = range(0, 10, 2)
    numbers = range(1, 10, 2)

    # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


.. code-block:: python

    # sorted

    from random import shuffle

    numbers = range(0, 100)
    shuffle(numbers)

    print numbers
    print sorted(numbers)

    numbers = map(str, numbers)

    print sorted(numbers)
    print sorted(numbers, key=int)
    print sorted(numbers, key=lambda x: int(x))


.. code-block:: python

    # zip

    rows = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    cols = zip(*rows)


Built-in types
==============

`Built-in Types <https://docs.python.org/2/library/stdtypes.html>`_

`Time Complexity <https://wiki.python.org/moin/TimeComplexity>`_


List
----

* Ordered collection of items.
* List items can be of any type.
* One list can contain many different types.
* Lists are mutable.
* Behaves like a stack (LIFO)


.. code-block:: python

    # lists

    items = [1, 2, 3, 4]

    for item in items:
        print item

    items.append(5)
    items.insert(0, 6)
    items = items + [7, 8, 9]
    items.extend([11, 12, 13])

    # 6, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13

    # http://stackoverflow.com/questions/11520492/difference-between-del-remove-and-pop-on-lists

    items.remove(8)
    del items[1]
    print items.pop(3)

    print items[::2]
    print items[1::2]
    print items[::-1]
    print items
    print items[:]
    print items[0:]
    print items[:-1]


.. code-block:: python
    
    # list of defaults

    items = [0] * 4
    items = [None] * 4

    items[0] = 1

    items = [[0]] * 4

    items[0][0] = 1


Tuple
-----

* Ordered collection of items.
* Tuple items can be of any type.
* One tuple can contain multiple types.
* Tuples are immutable.


.. code-block:: python

    # tuples

    items = (1, 2, 3, 4)
    items = 1, 2, 3, 4

    for item in items:
        print item

    print items[0]
    print items[-2]

    a = 1
    b = 2

    a, b = 1, 2
    b, a = a, b

    a, b, c, d = items


Dictionary
----------

* Unordered collection of key-value pairs
* Values can be of any type.
* Keys have to be hashable (immutable): string, integer, float, tuple, frozenset
* Using strings as keys is the preferred standard


.. code-block:: python

    # dicts

    items = {}

    items['1'] = 1 
    items['2'] = 2 
    items['3'] = 3
    items['4'] = 4 

    items = {'1': 1, '2': 2, '3': 3, '4': 4}

    # items = dict((str(key), value) for key, value in enumerate([1, 2, 3, 4]))
    # items = {str(key): value for key, value in enumerate([1, 2, 3, 4])}

    for key in items:
        value = items[key]
        print key, value

    for item in items.items():
        key = item[0]
        value = item[1]
        print key, value

    for item in items.items():
        key, value = item
        print key, value

    for key, value in items.items():
        print key, value

    for key, value in items.iteritems():
        print key, value

    keys = items.keys()
    key = keys[0]

    values = items.values()
    value = values[0]

    print key, value

    del items[key]

    # pop
    # popitem
    # setdefault
    # get

    # sort dictionary based on values


Set
---

* Unordered collection of unique items
* Mutable
* Use frozenset for immutable
* Support for set operations


.. code-block:: python

    # sets

    items = set()

    items.add(1)
    items.add(2)
    items.add(1)

    items = set([1, 1, 2, 3, 4, 4])


.. code-block:: python

    # set operations

    numbers = range(100)
    odd     = range(1, 100, 2)

    even = set(numbers) - set(odd)
    even = list(even)  

    even = list(set(numbers) - set(odd))


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


List comprehensions
===================

Generate lists with an expression in brackets.


.. code-block:: python

    # odd  = range(1, 10, 2)
    # even = range(0, 10, 2) 

    numbers = [i for i in range(10)]
    odd     = [number for number in numbers if number % 2]
    even    = [number for number in numbers if number % 2 == 0]
    even    = [number for number in numbers if number not in odd]


.. code-block:: python

    # normalize a vector

    vec  = [2, 0, 0]
    l    = (sum(axis ** 2 for axis in vec)) ** 0.5
    uvec = [vec[i] / l for i in range(3)]


.. code-block:: python

    # centroid (average)

    vertices = [[x, y, z], ...]
    centroid = [sum(axis) / len(vertices) for axis in zip(* vertices)]


Dict comprehensions
===================

.. note about json (integer keys are convertex to strings => use yaml instead)

.. code-block:: python

    # items = {1: 1, 2: 2, 3: 3, 4: 4}

    items = {index: value for index, value in enumerate(range(10))}


Iterators, Generators, Generator Expressions
============================================

`StackOverflow: Difference between generators and iterators <http://stackoverflow.com/questions/2776829/difference-between-pythons-generators-and-iterators>`_


.. code-block:: python

    # iterator

    items = iter(range(10))

    print items.next()
    print next(items, 11)

    while True:
        try:
            print items.next()
        except StopIteration:
            break


.. code-block:: python

    # generator (function) to construct iterator

    def squares(start, stop):
        for i in xrange(start, stop):
            yield i ** 2

    items = squares(1, 5)
    items = list(items)

    # generator (expression) to construct iterator

    items = (i ** 2 for i in range(1, 5))


.. code-block:: python

    # generator expressions inside function calls
    # sum of squares

    sum(axis ** 2 for axis in vec)


Script, Module, Package
=======================

.. code-block:: python

    # simple script

    a = 1
    b = 2
    c = a + b

    print c


.. code-block:: python

    # script vs. module
    # http://stackoverflow.com/questions/419163/what-does-if-name-main-do

    def f1():
        ...

    def f2():
        ...

    if __name__ == '__main__':
        # this part is only executed when the module is run as a script
        # this part does not get executed when the module is imported
        # all other code will get executed when the module is imported!

        f1()
        f2()


.. code-block:: python

    # module a.py

    def b():
        print 'b'


    # script main.py

    from a import b

    b()


.. code-block:: python

    # packages
    #
    # - a
    #     __init__.py
    #     - b.py
    #         def b1():
    #             ...
    #         def b2():
    #             ...
    #     - c
    #         __init__.py
    #         d.py
    #             def d1():
    #                 ...
    #             def d2():
    #                 ...

    from a.b import b1
    import a.c.d
    from a.c.d import d2

    b1()

    a.c.d.d1()

    d2()


.. code-block:: python

    # a.__init__.py

    from b import b1
    from b import b2
    from c.d import d1
    from c.d import d2

    # main.py

    import a
    from a import b1

    a.d1()

    b1()


Core packages
=============

`The Python Standard Library <https://docs.python.org/2/library/>`_

* abc
* collections
* colorsys
* copy
* csv
* ctypes
* itertools
* json
* math
* multiprocessing
* operators
* os
* random
* subprocess
* sys
* time
* urllib2
* xmlrpclib


User packages
=============

* cairo: library for drawing vector graphics
* cvxopt: convex optimisation
* cvxpy: convex optimisation
* cython: optimising static compiler
* joblib: parallel for loops using multiprocessing
* matplotlib: (mainly) 2D plotting library
* meshpy: triangular and tetrahedral mesh generation
* networkx: creation, manipulation, and study of the structure, dynamics, and functions of complex networks
* numba: just-in-time compiler
* numpy: fundamental package for scientific computing
* pandas: data structures and data analysis tools
* pycuda: binding of Nvidia's CUDA parallel computation API
* PyOpenGL: cross platform binding to OpenGL
* pyopt: nonlinear constrained optimization problems
* PySide: binding of the cross-platform GUI toolkit Qt
* scipy: scientific computing
* shapely: manipulation and analysis of planar geometric objects
* sphinx: documentation
* sympy: symbolic mathematics


Install Modules and Packages
============================

.. include explanation about using pip

* `Python Packaging User Guide <http://python-packaging-user-guide.readthedocs.org/en/latest/installing/>`_
* `StackOverflow: Why use pip over easy_install? <http://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install>`_
* `Unofficial Windows Binaries for Python Extension Packages <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_
* `Anaconda Python distribution <http://docs.continuum.io/anaconda/index>`_
* `MacPorts <https://www.macports.org/>`_

