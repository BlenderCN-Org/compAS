from numpy import array
from numpy import float32
from numpy import float64

import pycuda
import pycuda.autoinit
import pycuda.gpuarray


def get(a):
    """ Get GPUArray back from GPU memory.

    Parameters:
        a (gpu): Data on the GPU memory to retrieve.

    Returns:
        array: The GPUArray returned to RAM.
    
    Examples:
        >>> a = give([1, 2, 3], bit=64)
        >>> b = a.get()
        >>> type(b)
        numpy.ndarray
    """
    b = a.get()
    return b


def give(a, bit=64):
    """ Give a list or an array to GPU memory.

    Parameters:
        a (array, list): Data to send to the GPU memory.
        bit (int): 32 or 64 for corresponding float precision.

    Returns:
        gpu: GPUArray of input array.
        
    Creates and sends an array of float32 or float64 dtype from RAM to GPU 
    memory.
    
    Examples:
        >>> a = give([[1, 2, 3], [4, 5, 6]], bit=64)
        array([[ 1.,  2.,  3.],
               [ 4.,  5.,  6.]])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    if  bit == 32:
        b = pycuda.gpuarray.to_gpu(array(a).astype(float32))
    elif  bit == 64:
        b = pycuda.gpuarray.to_gpu(array(a).astype(float64))
    return b


def zeros(shape, bit=64):
    """ Create GPUArray of zeros directly on GPU memory.

    Parameters:
        shape (tuple): Dimensions of the GPUArray.
        bit (int, str): 32 or 64 for corresponding float precision.

    Returns:
        gpu: GPUArray of zeros.
        
    Examples:
        >>> a = zeros((3, 2), bit=64)
        array([[ 0.,  0.],
               [ 0.,  0.],
               [ 0.,  0.]])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    a = pycuda.gpuarray.zeros(shape, dtype='float' + str(bit))
    return a
    