
********************************************************************************
brg.com.matlab
********************************************************************************

Matlab communication through engine or (sub)process.



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



brg.com.matlab.engine
================================================================================

Matlab communication through the Matlab Engine.

This module defines a class for starting and interacting with the Matlab Engine.

>>> m = MatlabEngine()
>>> m.isprime(37)
True



.. toctree::
   :glob:

   brg-com-matlab-engine-MatlabEngineError
   brg-com-matlab-engine-MatlabEngine



brg.com.matlab.session
================================================================================

Matlab communication through the Matlab Engine.

This module defines a class for interacting with an existing (shared) Matlab Session.

>>> m = MatlabSession()
>>> m.isprime(37)
True



.. toctree::
   :glob:

   brg-com-matlab-session-MatlabSessionError
   brg-com-matlab-session-MatlabSession

