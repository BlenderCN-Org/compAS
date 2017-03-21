.. _python-numerical:

********************************************************************************
Numerical
********************************************************************************

.. contents::


Vectorisation
=============

Example 1
---------

.. plot::
    :include-source:
    
    # 1D - Example 1
    #
    # Compute z = cos(x/10)*sin(y) for x and y the integers in [0, n).
    #

    import math
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    n = 5*10**6
    ir = range(n)
    x = list(ir)
    y = list(ir)

    # For loop (appended list)
    tic = time.time()
    z1 = []
    for i in ir:
        z1.append(math.cos(x[i]/10)*math.sin(y[i]))
    print('\n\nFor loop and appended list: %.5f' % (time.time()-tic) + 's')

    # For loop (pre-allocated list)
    tic = time.time()
    z2 = [0]*n
    for i in ir:
        z2[i] = math.cos(x[i]/10)*math.sin(y[i])
    print('For loop and pre-allocated list: %.5f' % (time.time()-tic) + 's')

    # List comprehension
    tic = time.time()
    z3 = [math.cos(i/10)*math.sin(j) for i, j in zip(x, y)]
    toc = time.time() - tic
    print('List comprehension: %.5f' % (time.time()-tic) + 's')

    # NumPy array
    tic = time.time()
    xm = np.array(x)
    ym = np.array(y)
    z4 = np.cos(xm/10)*np.sin(ym)
    print('NumPy array: %.5f' % (time.time()-tic) + 's')

    # Check
    print(str(np.allclose(z4, np.array(z2))) + '\n\n')

    # Plot
    plt.figure(facecolor='white')
    plt.plot(np.array(ir)[:300], z4[:300])
    plt.xlabel('$i$')
    plt.ylabel('$z$')
    plt.minorticks_on()
    plt.show()


Example 2
---------

.. plot::
    :include-source:

    # Tiling - Example 2
    #
    # Tile arrays for x and y in [0, n) for plotting z = cos(x)sin(y).
    #

    import matplotlib.pyplot as plt
    import numpy as np

    # Domain
    n = 50
    xa = np.array(range(n))
    ya = np.array(range(n))

    # Tiling methods
    xm, ym = np.meshgrid(xa, ya)
    zt = np.cos(xm)*np.sin(ym)

    # Alternative
    xt = np.tile(xa[np.newaxis, :], (n, 1))
    yt = np.tile(ya[:, np.newaxis], (1, n))

    # Plot
    plt.figure(facecolor='white')

    plt.subplot(1, 3, 1)
    cs = plt.contourf(xt, 50)
    cbar = plt.colorbar(cs)
    cbar.ax.set_ylabel('$x$')
    plt.axis('equal')

    plt.subplot(1, 3, 2)
    cs = plt.contourf(yt, 50)
    cbar = plt.colorbar(cs)
    cbar.ax.set_ylabel('$y$')
    plt.axis('equal')

    plt.subplot(1, 3, 3)
    cs = plt.contourf(zt, 50)
    cbar = plt.colorbar(cs)
    cbar.ax.set_ylabel('$z$')
    plt.axis('equal')

    plt.show()


Example 3
---------

.. plot::
    :include-source:

    # 2D  - Example 3
    #
    # Compare cos(x/20)sin(y/20) for x and y in domain [0, n), calculated by for
    # looping, list comprehension and NumPy arrays.
    #

    import math
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    # Domain
    n = 2500
    ir = range(n)
    x = list(ir)
    y = list(ir)

    # For loop list
    tic = time.time()
    z1 = []
    for i in ir:
        r = []
        for j in ir:
            r.append(math.cos(x[i]/20)*math.sin(y[j]/20))
        z1.append(r)
    print('\n\nFor loop and appended list: %.5f' % (time.time()-tic) + 's')

    # List comprehension
    tic = time.time()
    z2 = [[math.cos(i/20)*math.sin(j/20) for j in y] for i in x]
    print('List comprehension: %.5f' % (time.time()-tic) + 's')

    # NumPy array
    tic = time.time()
    ym, xm = np.meshgrid(np.array(x), np.array(y))
    z3 = np.cos(xm/20)*np.sin(ym/20)
    print('NumPy array: %.5f' % (time.time()-tic) + 's')

    # Check
    print(str(np.allclose(z3, np.array(z2))) + '\n\n')

    # Plot
    w = 300
    plt.figure(facecolor='white')
    cs = plt.contourf(xm[:w, :w], ym[:w, :w], z3[:w, :w], 30)
    cbar = plt.colorbar(cs)
    cbar.ax.set_ylabel('$z$')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.axis('equal')
    plt.show()


Example 4
---------

.. plot::
    :include-source:

    # 3D - Example 4
    #
    # Plot 1/(x^2 + y^2 + z^2 + 1) for x, y and z in domain [-n, n), comparing for
    # loop, list comprehension and NumPy array methods.
    #

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    # Domain
    n = 50
    ir = range(-n, n)
    x = list(ir)
    y = list(ir)
    z = list(ir)

    # For loop list
    tic = time.time()
    u1 = []
    for i in x:
        r = []
        for j in y:
            s = []
            for k in z:
                s.append(1/(i**2 + j**2 + k**2 + 1))
            r.append(s)
        u1.append(r)
    print('\n\nFor loop and appended list: %.5f' % (time.time()-tic) + 's')

    # List comprehension
    tic = time.time()
    u2 = [[[1/(i**2 + j**2 + k**2 + 1) for k in z] for j in y] for i in x]
    print('List comprehension: %.5f' % (time.time()-tic) + 's')

    # NumPy array
    tic = time.time()
    ym, xm, zm = np.meshgrid(np.array(y), np.array(x), np.array(z))
    u3 = 1/(xm**2 + ym**2 + zm**2 + 1)
    print('NumPy array: %.5f' % (time.time()-tic) + 's')

    # Check
    print(str(np.allclose(u3, np.array(u1))) + '\n\n')

    # Plot
    d = 2
    un = u3*1000
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xm[::d, ::d, ::d], ym[::d, ::d, ::d], zs=zm[::d, ::d, ::d],
               s=un[::d, ::d, ::d], c='b', alpha=0.1)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')
    ax.axis('equal')
    plt.show()


Example 5
---------

.. code-block:: python

    # Element versus matrix operations - Example 5
    #
    # Appreciate the differences between matrix and element based operations.
    #

    import numpy as np
    import time

    # Various operations
    A = np.array([[1, 2], [3, 4]])
    B = A*A
    C = np.dot(A, A)
    D = A**2
    E = np.matrix(A)**2
    F = np.vdot(A, A)
    G = np.matmul(A, A)

    # Setup arrays
    n = 10**6
    A = np.random.rand(n, 3)
    B = np.random.rand(n, 3)
    C = np.zeros(n)

    # For loop
    tic = time.time()
    C1 = np.copy(C)
    for i in range(n):
        C1[i] = np.sum(A[i, :]*B[i, :])
    print('\n\nFor loop: %.5f' % (time.time()-tic) + 's')

    # Vectored
    tic = time.time()
    C2 = np.sum(A*B, axis=1)
    print('Vectored: %.5f' % (time.time()-tic) + 's')

    # Check
    print(str(np.allclose(C1, C2)) + '\n\n')


Example 6
---------

.. code-block:: python

    # Slicing - Example 6
    #
    # Demonstrate a variety of ways to slice an array.
    #

    import matplotlib.pyplot as plt
    import numpy as np

    # Grid size
    n = 100


.. code-block:: python

    # Diagonals
    z = np.zeros((n, n))
    ind = list(range(n))
    z[ind, ind] = 1
    z[ind[::-1], ind] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. plot::

    # Slicing - Example 6
    #
    # Demonstrate a variety of ways to slice an array.
    #

    import matplotlib.pyplot as plt
    import numpy as np

    # Grid size
    n = 100

    # Diagonals
    z = np.zeros((n, n))
    ind = list(range(n))
    z[ind, ind] = 1
    z[ind[::-1], ind] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. code-block:: python

    # Columns and rows
    z = np.zeros((n, n))
    z[:, 20:25] = 1
    z[80:90, :] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. plot::

    # Slicing - Example 6
    #
    # Demonstrate a variety of ways to slice an array.
    #

    import matplotlib.pyplot as plt
    import numpy as np

    # Grid size
    n = 100

    # Columns and rows
    z = np.zeros((n, n))
    z[:, 20:25] = 1
    z[80:90, :] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. code-block:: python

    # Points
    z = np.zeros((n, n))
    r = [10, 15, 66]
    c = [22, 9, 4]
    z[r, c] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. plot::

    # Slicing - Example 6
    #
    # Demonstrate a variety of ways to slice an array.
    #

    import matplotlib.pyplot as plt
    import numpy as np

    # Grid size
    n = 100

    # Points
    z = np.zeros((n, n))
    r = [10, 15, 66]
    c = [22, 9, 4]
    z[r, c] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. code-block:: python

    # Block
    z = np.zeros((n, n))
    r = range(10, 40)
    c = range(20, 30)
    z[np.ix_(r, c)] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. plot::

    # Slicing - Example 6
    #
    # Demonstrate a variety of ways to slice an array.
    #

    import matplotlib.pyplot as plt
    import numpy as np

    # Grid size
    n = 100

    # Block
    z = np.zeros((n, n))
    r = range(10, 40)
    c = range(20, 30)
    z[np.ix_(r, c)] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. code-block:: python

    # Corners
    z = np.zeros((n, n))
    ind = list(range(10)) + list(range(90, 100))
    z[np.ix_(ind, ind)] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


.. plot::

    # Slicing - Example 6
    #
    # Demonstrate a variety of ways to slice an array.
    #

    import matplotlib.pyplot as plt
    import numpy as np

    # Grid size
    n = 100

    # Corners
    z = np.zeros((n, n))
    ind = list(range(10)) + list(range(90, 100))
    z[np.ix_(ind, ind)] = 1

    fig = plt.figure(facecolor='white')
    plt.imshow(z, interpolation='none')
    plt.show()


Example 7
---------

.. code-block:: python

    # Logical arrays - Example 7
    #
    # Demonstrate use of logical arrays and their faster performance to slicing.
    #

    import matplotlib.pyplot as plt
    import numpy as np
    import time

    # Grid
    n = 500
    z = np.random.rand(n, n)

    # Plot
    fig = plt.figure(facecolor='white')
    plt.imshow(z)
    plt.show()

    # For loop
    tic = time.time()
    z1 = np.copy(z)
    for i in range(n):
        for j in range(n):
            if  z1[i, j] < 0.5:
                z1[i, j] = 0
            else:
                z1[i, j] = 1
    print('\n\nFor loop: %.5f' % (time.time()-tic) + 's')

    # Slicing
    tic = time.time()
    z2 = np.copy(z)
    r1, c1 = np.where(z2 < 0.5)
    r2, c2 = np.where(z2 >= 0.5)
    z2[r1, c1] = 0
    z2[r2, c2] = 1
    print('Slicing array: %.5f' % (time.time()-tic) + 's')

    # Logical array
    tic = time.time()
    z3 = np.copy(z)
    log = z3 < 0.5
    z3 = ~log
    print('Logical array: %.5f' % (time.time()-tic) + 's')

    # Plot
    fig = plt.figure(facecolor='white')
    plt.imshow(z3)
    plt.show()
