.. _python:

********************************************************************************
Python intro
********************************************************************************

.. contents::

* lists and dicts
* sets
* comprehensions, reduction, mapping
* sorting (using key functions)
* default values
* flow control
* decorators, descriptors
* profiling, timing

.. give examples of where these things are used in the framework

Lists and Dicts
===============

Differences related to definition and processing of faces?


.. code-block:: python

	face = [0, 1, 2, 3]

	# edges of the face

	for i in range(-1, len(face) - 1):
		u = face[i]
		v = face[i + 1]
		print u, v

	# descendant of a vertex

	from random import randint

	u = randint(0, 3)  # what if u = 3?
	v = face[face.index(u) + 1]

	# ancestor of a vertex

	v = randint(0, 3)
	u = face[face.index(v) - 1]


.. code-block:: python

	face = {0: 1, 1: 2, 2: 3, 3: 0}

	# edges of the face

	start = u = 0

	while True:
		v = face[u]
		print u, v
		if v == start:
			break
		u = v

	# descendant of a vertex

	from random import randint

	u = randint(0, 3)
	v = face[u]

	# ancestor of a vertex

	rface = dict((v, u) for u, v in face.iteritems())

	v = randint(0, 3)
	u = rface[v]


Sets
====

Member checking, unique elements, intersections, ...


.. code-block:: python

	from random import randint

	items = [randint(0, 3) for i in range(10)]

