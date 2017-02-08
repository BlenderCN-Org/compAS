.. _getting-started:

********************************************************************************
Getting started
********************************************************************************


Dependencies
============


Download
========


Installation
============

Currently, we do not provide an installer. This may change in the future, but then
again, it may not :)


Setup
=====

If you have pulled the framework from our BitBucket repository, the only thing
left is to set a few environment variables. This makes importing modules in
different contexts and environments much simpler.

On Windows
----------

If you don't have a path editor for Windows yet, now might be a good time to get
one. A free download is available at https://patheditor2.codeplex.com/.

Otherwise you can find the environment variables here::
    
    Control Panel > System > Advanced system settings > Environment Variables...


Add the location of the BRG framework to your ``PYTHONPATH``. I have the following 
directories listed there::

    Z:\Code\brg_projects
    Z:\Code\brg_packages
    Z:\Code\brg_framework\src

Only the last one is really important. Obviously change the paths to whatever
makes sense on your system.

Also make sure that Python and/or your Scientific Python distribution is on the
system ``PATH``. I have the following directories listed at the beginning of the
path::

    C:\Anaconda2
    C:\Anaconda2\Scripts
    C:\Anaconda2\Library\bin
    C:\IronPython27


In Rhino, open the *PythonScriptEditor*, and go to options.  


First steps
===========

