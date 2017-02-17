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
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'cuda_abs', 'cuda_argmax', 'cuda_argmin', 'cuda_acos', 'cuda_asin',
    'cuda_atan', 'cuda_ceil', 'cuda_cos', 'cuda_cosh', 'cuda_exp', 'cuda_floor',
    'cuda_log', 'cuda_max', 'cuda_min', 'cuda_mean', 'cuda_sin', 'cuda_sinh',
    'cuda_sqrt', 'cuda_sum', 'cuda_tan', 'cuda_tanh',
]


def cuda_abs(a):
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


def cuda_argmax(a, axis):
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


def cuda_argmin(a, axis):
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


def cuda_acos(a):
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


def cuda_asin(a):
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


def cuda_atan(a):
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


def cuda_ceil(a):
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


def cuda_cos(a):
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


def cuda_cosh(a):
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


def cuda_exp(a):
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


def cuda_floor(a):
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


def cuda_log(a):
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


def cuda_log10(a):
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


def cuda_max(a, axis):
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


def cuda_min(a, axis):
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


def cuda_mean(a, axis):
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


def cuda_sin(a):
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


def cuda_sinh(a):
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


def cuda_sqrt(a):
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


def cuda_sum(a, axis):
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


def cuda_tan(a):
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


def cuda_tanh(a):
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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
