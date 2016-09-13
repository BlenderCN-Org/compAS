
********************************************************************************
brg.com.matlab
********************************************************************************

Matlab communication through engine or (sub)process.



brg.com.matlab.engine
================================================================================

Matlab communication through the Matlab Engine.

This module defines classes for starting and interacting with the Matlab Engine,
and for interacting with an existing (shared) Matlab Session.

>>> m = MatlabEngine()
>>> m.isprime(37)
True



.. toctree::
   :glob:

   brg-com-matlab-engine-MatlabEngineError
   brg-com-matlab-engine-MatlabSessionError
   brg-com-matlab-engine-MatlabEngine
   brg-com-matlab-engine-MatlabSession



brg.com.matlab.process
================================================================================

Matlab (sub)process.

Examples:

    >>> m = MatlabProcess(verbose=False)
    >>> m.start()
    >>> m.write_value('a', 17)
    >>> m.run_command('res = isprime(a);')
    >>> m.read_value('res')
    1
    >>> m.stop()

Todo:
    - handle timeouts properly
    - check for availability of Matlab
    - catch Matlab errors



.. toctree::
   :glob:

   brg-com-matlab-process-MatlabProcessError
   brg-com-matlab-process-MatlabProcess

