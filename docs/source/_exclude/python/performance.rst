.. _python-performance:

********************************************************************************
Performance
********************************************************************************

.. warning::
    
    This page is still under construction. We intend to add information about the
    following topics:

    * profiling
    * line profiling
    * numba
    * gpu => pycuda, pyopencl
    * numpy & scipy
    * cython
    * pybind11
    * weave


.. contents::


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

