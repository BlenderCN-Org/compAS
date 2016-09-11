
********************************************************************************
brg.com.matlab
********************************************************************************

Matlab communication through engine or (sub)process.



brg.com.matlab.engine
================================================================================

None

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

    >>> m = MatlabProcess()
    >>> m.start()
    >>> m.write_value('a', 37)
    >>> m.run_command('tf = isprime(a);')
    >>> m.read_workspace()
    >>> m.stop()
    >>> print m.ws_data



.. toctree::
   :glob:

   brg-com-matlab-process-MatlabProcessError
   brg-com-matlab-process-MatlabProcess

