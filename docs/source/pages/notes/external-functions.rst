.. _notes_external-functions:

********************************************************************************
External functions
********************************************************************************

.. contents::


Python has many packages (for example, paerts of NumPy and SciPy) that are wrappers
around highly optimised C or C++ or even Fortran libraries. Unfortunately, this
means that these packages are then not available in flavours of Python that are
not C-based, such as IronPython or Jython.

However, the built-in ``subprocess`` module provides an easy way around this
limitation.


.. code-block:: python

    # the external script
    # test.py

    # some imports that would throw an error in Rhino

    from scipy.interpolate import griddata
    from scipy.sparse import csr_matrix
    from scipy.optimize import minimize
    from scipy.spatial import distance_matrix

    import time

    for i in range(100):
        print i
        time.sleep(0.1)


.. code-block:: python

    # calling the script through an external process

    from subprocess import Popen
    from subprocess import PIPE

    args = ['pythonw', '-u', 'test.py']

    p = Popen(args, stderr=PIPE, stdout=PIPE)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        print line.strip()
        # this prints here whatever is being printed by the script

    stdout, stderr = p.communicate()

    print 'stdout:'
    print stdout
    print 'stderr:'
    print stderr


.. code-block:: python

    1
    2
    3
    
    ...

    97
    98
    99
    stdout:

    stderr:


.. seealso::

    * :mod:`compas.utilities.xfunc`
    * :mod:`compas_rhino.utilities.xfunc`
