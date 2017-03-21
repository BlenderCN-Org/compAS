.. _getting-started:

********************************************************************************
Getting started
********************************************************************************

Before getting started, make sure the following tools are available on your system:

* A version control system (Git, Mercurial, ...).
* A repository manager (for example, SourceTree).
* A code editor or and IDE (Eclipse, Sublime Text, Notepad++, ...).
* A +2.6 version of the CPython implementation.

Any other requirements are either optional, or related to specific environments,
and will be further discussed where relevant throughout this page.


Installation
============

Currently, we do not provide an installer. This may change in the future, but then
again, it may not :)

The Mercurial repo can be cloned from https://bitbucket.org/brgbits/compAS, and
a Git fork is available at https://bitbucket.org/GramazioKohlerResearch/compAS.

Obviously you are entirely free to choose where to place these clones on your system,
but a folder structure that seems to make a lot of sense is this:

::

    .../compAS/core
    .../compAS/packages

After pulling one of the above repositories into core, that folder should contain
the following:

* data
* docs
* examples
* libs
* src
  * compas
  * compas_blender
  * compas_dynamo
  * compas_grasshopper
  * compas_maya
  * compas_rhino
  * compas_web

* tools


Dependencies
============

The BRG framework has very few dependencies, and most of them are optional. If
you are happy working in Rhino or Blender, and you are not interested in or don't
need any of the numerical stuff, then everything should work out of the box;
provided you have Python installed, of course.

.. note::

    Currently we support only Python +2.6. Most things will probably also work in
    Python 3.x, but not everything, yet.


The current version of compAS has the following **optional** dependencies:

* Numpy & Scipy (http://www.numpy.org/ and https://www.scipy.org/):
  For all numerical calculations and algorithms.

* Matplotlib (http://matplotlib.org/):
  For two-dimensional visualisations.

* PyOpenGL (http://pyopengl.sourceforge.net/>):
  For three-dimensional visualisations.

* PySide (https://wiki.qt.io/PySide):
  For some of the standalone tools.

* NetworkX (https://networkx.github.io/):
* Planarity (https://github.com/hagberg/planarity):

* Cython (http://cython.org/):
  For performance optimisation.

* Numba (http://numba.pydata.org/):
  For just-in-time compilation.

* PyCuda (https://mathema.tician.de/software/pycuda/):
  For parallel computation through Nvidia's CUDA.

* PyOpenCL (https://mathema.tician.de/software/pyopencl/):
  For parallel computation though OpenCL.

* CVXPY (http://www.cvxpy.org/):
  For convex optimisation problems.

* Imageio (https://imageio.github.io/):
  For reading and writing of image data.

* PIL (http://www.pythonware.com/products/pil):
  For general image processing.


Scientific Python distributions like `Anaconda <https://www.continuum.io/>`_ or
`Enthought EPD <https://www.enthought.com/products/epd/>`_ provide most of the
optional dependencies (and of course Python), or a package manager to
install them with. Make sure to get a version that ships with Python 2.x (see
note above).

On Windows, many installers for remaining and otherwise difficult-to-install packages
can be found on Christof Gholke's page 
`Unofficial Windows Binaries for Python Extension Packages <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_.
On mac, installing whatever doesn't ship with a scientific distribution is
relatively easy with a package manager like `macports <https://www.macports.org/>`_
or `homebrew <http://brew.sh/>`_.


Setup
=====

Once you have pulled the code from one of the repositories, the only thing
left to do is to set a few environment variables. This simplifies importing modules
in different contexts and environments.


On Windows
++++++++++

On Windows, you can find the environment variables here

::

    Control Panel > System > Advanced system settings > Environment Variables...


First, make sure that Python and/or your Scientific Python distribution is on the
system ``PATH``. Usually, this is already taken care of by their installers.
For example, if you installed Anaconda2, in PathEditor you should see the following
lines in the list of directories

::

    C:\Anaconda2
    C:\Anaconda2\Scripts
    C:\Anaconda2\Library\bin


Then, add the location of the compAS framework to your ``PYTHONPATH``

::

    C:\path\to\compAS\src


Start an interactive Python session (type ``python`` on the command line)
and try the following

::

    >>> import compas
    >>> from compas.datastructures.network import Network
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    >>> print network


On Mac
++++++

If you are on a Mac, the procedure is similar. Open the Terminal and use your
favourite text editing application to modify your ``.profile``

::

    $ nano ~/.profile

::

    export PATH="/path/to/anaconda/bin:$PATH"
    export PYTHONPATH="/path/to/compAS/src:$PYTHONPATH"

Restart the Terminal or type

::

    $ source ~/.profile

Start an interactive Python session (type ``python`` in the Terminal)
and try the following

::

    >>> import compas
    >>> from compas.datastructures.network import Network
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    >>> print network


Working in Rhino
================

Rhino uses IronPython to interpret your Python scripts. It ships with its own
version of IronPython, but, at least in Rhino 5, this bundled IronPython is a buggy
beta version. For example, using the version of IronPython that ships with Rhino,
you will not be able to import the *Abstract Syntax Tree* (``ast``) module. To
verify which version of IronPython you have, try this:

.. code-block:: python

    import sys

    print sys.version_info


This is likely to result in the following::

    sys.version_info()


Therefore, if you are using Rhino 5, you should install your own
copy of IronPython and add it to your system path  and to Rhino's search paths.
Make sure to install IronPython 2.7.5, and not the latest version.

.. note::
    
    If you are test driving Rhino 6, the bundled IronPython should work fine as it is.


To fix this, open the *ScriptEditor* in Rhino, and go to::

    Tools > Options > Files


Add the following to the *Modules Search Paths*::

    C:\IronPython27
    C:\IronPython27\Lib
    C:\IronPython27\DLLs


Then restart Rhino and try running the previous snippet again


.. code-block:: python

    import sys

    print sys.version_info


Now, this should print something like this::

    sys.version_info(major=2, minor=7, micro=5, releaselevel='final', serial=0)


Rhino also doesn't use your Windows System Variables, so you will have to tell it
where compAS is as well. Therefore, also add that to your *Modules Search Paths*::

    C:\path\to\compAS\src


After that you should be able to run the following script.

.. code-block:: python

    import compas
    import compas_rhino

    from compas.datastructures.network import Network

    network = Network.from_obj(compas.get_data('lines.obj'))

    compas_rhino.draw_network(network)


If this draws a network without throwing an error, you are all set.


.. note::

    For those of you who work on Mac and use a Windows virtual machine for Rhino.

    Although you can use the code on your Mac from your Windows virtual
    machine, you can't use the Mac Python installation from that side.
    This means that you will need to install the same Python setup on both sides,
    to be able to access the all functionality from Rhino.


