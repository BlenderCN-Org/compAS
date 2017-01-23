__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class MatlabEngineError(Exception):

    def __init__(self, message=None):
        if not message:
            message = """Could not start the Matlab engine.
Note that the Matlab engine for Python is only available since R2014b.
For older versions of Matlab, use *MatlabProcess* instead.
On Windows, *MatlabClient* is also available.
See <https://ch.mathworks.com/help/matlab/matlab-engine-for-python.html?s_tid=gn_loc_drop>
for instructions.
"""
        super(MatlabEngineError, self).__init__(message)


class MatlabEngine(object):
    """Communicate with Matlab through the MATLAB engine.

    For more information,
    see `MATLAB Engine API for Python <https://ch.mathworks.com/help/matlab/matlab-engine-for-python.html?s_tid=gn_loc_drop>`_.
    
    Examples:
        >>> m = MatlabEngine()
        >>> m.isprime(37)
        True

    """

    def __init__(self, delay_start=False):
        self.matlab = None
        self.engine = None
        self.init()
        if not delay_start:
            self.start()

    def init(self):
        try:
            import matlab.engine
        except ImportError:
            raise MatlabEngineError()
        self.matlab = matlab.engine    

    def __getattr__(self, name):
        if self.engine:
            method = getattr(self.engine, name)
            def wrapper(*args, **kwargs):
                return method(*args, **kwargs)
            return wrapper
        else:
            raise MatlabEngineError()

    def start(self):
        print 'starting engine. this may take a few seconds...'
        self.engine = self.matlab.start_matlab()
        print 'engine started!'

    def stop(self):
        print 'stopping engine...'
        self.engine.quit()
        print 'engine stopped!'


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    m = MatlabEngine()

    print m.isprime(37)

