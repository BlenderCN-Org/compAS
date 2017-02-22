.. _getting-started:

********************************************************************************
Getting started
********************************************************************************


Tools
=====

Before getting started, make sure you have the necessary tools installed on your
system. At the very least, you will need a code editor and a source control
management tool.

Some installation instructions for different editors and repo managers, and a
few other helpful bits and pieces can be found here: :doc:`/pages/devenv`.


Download
========

Currently, we do not provide an installer. This may change in the future, but then
again, it may not :)

The mercurial repo can be cloned from::

    https://bitbucket.org/brgbits/compAS

A Git fork is available here::

    https://bitbucket.org/GramazioKohlerResearch/compAS


Dependencies
============

The BRG framework has very few dependencies, and most of them are optional. If
you are happy working in Rhino or Blender, and are not interested in any of the
numerical stuff, then everything should work out of the box;
provided you have Python installed, of course.

For plotting two-dimensional representations of data structures (and to some extent
three-dimensional as well), we use `Matplotlib <http://matplotlib.org/>`_.
For three-dimensional visualisations, we use `PyOpenGL <http://pyopengl.sourceforge.net/>`_ 
and `PySide <https://wiki.qt.io/PySide>`_. Installation instructions for both, 
and for the libraries they depend on are under construction and will be available
here :doc:`/pages/devenv`.

For all numerical calculations and algorithms, we rely on `NumPy <http://www.numpy.org/>`_ 
and `SciPy <https://www.scipy.org/>`_.

Some network algorithms use `NetworkX <https://networkx.github.io/>`_ and
`Planarity <https://github.com/hagberg/planarity>`_.
In future versions, `Triangle <http://www.cs.cmu.edu/~quake/triangle.html>`_ and
`TetGen <http://wias-berlin.de/software/tetgen/>`_ might be used through
`MeshPy <https://mathema.tician.de/software/meshpy/>`_ for some of the mesh
algorithms, especially those relating to meshing for FE Analysis, but this is not
case now.


Setup
=====

Scientific Python distributions like `Anaconda <https://www.continuum.io/>`_ or
`Enthought EPD <https://www.enthought.com/products/epd/>`_ provide most of these,
or at least a package manager to install them with.

On Windows, many installers for remaining and otherwise difficult-to-install packages
can be found on Christof Gholke's page 
`Unofficial Windows Binaries for Python Extension Packages <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_.
On mac, installing whatever doesn't ship with a scientific distribution is
relatively easy with a package manager like `macports <https://www.macports.org/>`_
or `homebrew <http://brew.sh/>`_.

If you prefer a bit more control and want to try a manual install, SciPy provides
some instructions for installing a `scientific Python stack <http://www.scipy.org/about.html>`_.

Also remeber that all of this is optional. Most functionality is available out-of-the-box.


Further Setup
=============

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


Then, add the location of the BRG framework to your ``PYTHONPATH``

::

    C:\path\to\the\compas_framework\src


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
    export PYTHONPATH="/path/to/the/compas_framework/src:$PYTHONPATH"

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


Rhino
=====

Rhino uses IronPython to interpret your Python scripts. It ships with its own
version of IronPython, but, at least in Rhino 5, this bundled IronPython is a buggy
beta version. Therefore, if you are using Rhino 5, you should install your own
copy of IronPython and add it to your system path  and to Rhino's search paths.
Make sure to install IronPython 2.7.5, and not the latest version.

.. note::
    
    If you are test driving Rhino 6, the bundled IronPython should work fine


In Rhino, open the *ScriptEditor*, and go to::

    Tools > Options > Files


Add the following to the *Modules Search Paths* for IronPython::

    C:\IronPython27
    C:\IronPython27\Lib
    C:\IronPython27\DLLs


and this path for the framework library::

    C:\path\to\the\compas_framework\src


Then restart Rhino and run the following scripts


.. code-block:: python

    import sys

    print sys.version_info


This should print something like this::

    sys.version_info(major=2, minor=7, micro=5, releaselevel='final', serial=0)


.. code-block:: python

    import ast


This should not throw an error.


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

