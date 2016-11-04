try:
    import pycuda
    import pycuda.autoinit
    import pycuda.cumath
except ImportError as e:
    pass

try:
    import skcuda
    import skcuda.autoinit
except ImportError as e:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 17, 2016'


def abs(a):
    """ Absolute values of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with the elements to take absolute values of.

    Returns:
        gpu: abs(GPUArray)

    Examples:
        >>> a = abs(give([-0.1, -1.7]))
        array([0.1, 1.7])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.fabs(a)

    
def argmax(a, axis):
    """ Location of maximum GPUArray elements.

    Parameters:
        a (gpu): GPUArray with the elements to find maximum values.
        axis (int): The dimension to evaluate across.

    Returns:
        gpu: Location of maximum values.

    Examples:
        >>> a = argmax(give([[1, 2, 3], [6, 5, 4]]), axis=1)
        array([[2],
               [0]], dtype=uint32)
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.misc.argmax(a, axis, keepdims=True)
    
    
def argmin(a, axis):
    """ Location of minimum GPUArray elements.

    Parameters:
        a (gpu): GPUArray with the elements to find minimum values.
        axis (int): The dimension to evaluate across.

    Returns:
        gpu: Location of minimum values.

    Examples:
        >>> a = argmin(give([[1, 2, 3], [6, 5, 4]]), axis=1)
        array([[0],
               [2]], dtype=uint32)
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.misc.argmin(a, axis, keepdims=True)
    
    
def acos(a):
    """ Trigonometric arccosine of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: acos(GPUArray)

    Examples:
        >>> a = acos(give([0.5, 1]))
        array([ 1.04719755,  0.])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.acos(a)


def asin(a):
    """ Trigonometric arcsine of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: asin(GPUArray)

    Examples:
        >>> a = asin(give([0.5, 1]))
        array([ 0.52359878,  1.57079633])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.asin(a)


def atan(a):
    """ Trigonometric arctangent of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: atan(GPUArray)

    Examples:
        >>> a = atan(give([0.5, 1]))
        array([ 0.46364761,  0.78539816])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.atan(a)


def ceil(a):
    """ Ceiling of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: ceil(GPUArray)

    Examples:
        >>> a = ceil(give([0.5, 0.1, 0.9]))
        array([ 1.,  1.,  1.])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.ceil(a)


def cos(a):
    """ Trigonometric cosine of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: cos(GPUArray)

    Examples:
        >>> a = cos(give([0, pi/4]))
        array([ 1.,  0.70710678])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.cos(a)


def cosh(a):
    """ Hyperbolic cosine of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: cosh(GPUArray)

    Examples:
        >>> a = cosh(give([0, pi/4]))
        array([ 1.,  1.32460909])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.cosh(a)


def exp(a):
    """ Exponential of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: exp(GPUArray)

    Examples:
        >>> a = exp(give([0, 1]))
        array([ 1.,  2.71828183])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.exp(a)


def floor(a):
    """ Floor of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        b = floor(GPUArray)

    Examples:
        >>> a = floor(give([0.5, 0.1, 0.9]))
        array([ 0.,  0.,  0.])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.floor(a)


def log(a):
    """ Natural logarithm of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: log(GPUArray)

    Examples:
        >>> a = log(give([1, 10]))
        array([ 0.,  2.30258509])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.log(a)


def log10(a):
    """ Base10 logarithm of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: log10(GPUArray)

    Examples:
        >>> a = log10(give([1, 10]))
        array([ 0.,  1.])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.log10(a)


def max(a, axis):
    """ Values of maximum GPUArray elements.

    Parameters:
        a (gpu): GPUArray with the elements to find maximum values.
        axis (int): The dimension to evaluate across.

    Returns:
        gpu: Maximum values.

    Examples:
        >>> a = max(give([[1, 2, 3], [6, 5, 4]]), axis=1)
        array([[3],
               [6]], dtype=uint32)
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.misc.max(a, axis, keepdims=True)
    
    
def min(a, axis):
    """ Values of minimum GPUArray elements.

    Parameters:
        a (gpu): GPUArray with the elements to find minimum values.
        axis (int): The dimension to evaluate across.

    Returns:
        gpu: Minimum values.

    Examples:
        >>> a = min(give([[1, 2, 3], [6, 5, 4]]), axis=1)
        array([[1],
               [4]], dtype=uint32)
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.misc.min(a, axis, keepdims=True)
    
    
def mean(a, axis):
    """ Mean of GPUArray elements in a given axis direction.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.
        axis (int): Axis direction to mean average across.

    Returns:
        gpu: GPUArray mean across dimension specified.

    Examples
        >>> mean(give([[1, 2], [3, 4]]), axis=0)
        array([ 2.,  3.])
    """
    return skcuda.misc.mean(a, axis)


def sin(a):
    """ Trigonometric sine of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: sin(GPUArray)

    Examples:
        >>> a = sin(give([0, pi/4]))
        array([ 0.,  0.70710678])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.sin(a)


def sinh(a):
    """ Hyperbolic sine of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: sinh(GPUArray)

    Examples:
        >>> a = sinh(give([0, pi/4]))
        array([ 0.,  0.86867096])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.sinh(a)


def sqrt(a):
    """ Square-root of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: sqrt(GPUArray)

    Examples:
        >>> a = sqrt(give([4, 9]))
        array([ 2.,  3.])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.sqrt(a)


def sum(a, axis):
    """ Sum of GPUArray elements in given axis direction.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.
        axis (int) : Axis direction to sum through.

    Returns:
        gpu: GPUArray sum across dimension specified.

    Examples:
        >>> sum(give([[1, 2], [3, 4]]), axis=0)
        array([ 4.,  6.])
    """
    return skcuda.misc.sum(a, axis=axis)


def tan(a):
    """ Trigonometric tangent of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: tan(GPUArray)

    Examples:
        >>> a = tan(give([0, pi/4]))
        array([ 0.,  1])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.tan(a)


def tanh(a):
    """ Hyperbolic tangent of GPUArray elements.

    Parameters:
        a (gpu): GPUArray with elements to be operated on.

    Returns:
        gpu: tanh(GPUArray)

    Examples:
        >>> a = tanh(give([0, pi/4]))
        array([ 0.,  0.6557942])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return pycuda.cumath.tanh(a)
