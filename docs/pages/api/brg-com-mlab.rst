
********************************************************************************
brg.com.mlab
********************************************************************************

Matlab communication through engine or (sub)process.



brg.com.mlab.process
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

   brg-com-mlab-process-MatlabProcessError
   brg-com-mlab-process-MatlabProcess



brg.com.mlab.engine
================================================================================

Matlab communication through the Matlab Engine.

This module defines a class for starting and interacting with the Matlab Engine.

>>> m = MatlabEngine()
>>> m.isprime(37)
True



.. toctree::
   :glob:

   brg-com-mlab-engine-MatlabEngineError
   brg-com-mlab-engine-MatlabEngine



brg.com.mlab.session
================================================================================

Matlab communication through the Matlab Engine.

This module defines a class for interacting with an existing (shared) Matlab Session.

>>> m = MatlabSession()
>>> m.isprime(37)
True



.. toctree::
   :glob:

   brg-com-mlab-session-MatlabSessionError
   brg-com-mlab-session-MatlabSession

