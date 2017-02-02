import numpy as np

try:
    import pycuda
    import pycuda.autoinit
    import pycuda.curandom
    import pycuda.gpuarray
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
    'cuda_diag', 'cuda_eye', 'cuda_get', 'cuda_give', 'cuda_ones', 'cuda_random',
    'cuda_real', 'cuda_reshape', 'cuda_flatten', 'cuda_tile', 'cuda_zeros',
]


def cuda_diag(a):
    """ Construct or extract GPUArray diagonal.

    Note:
        If a is 1D, GPUArray is constructed, if 2D, the diagonal is extracted.

    Parameters:
        a (gpu): GPUArray (1D or 2D).

    Returns:
        gpu: GPUArray with inserted diagonal, or vector of diagonal.

    Examples:
        >>> a = diag(give([1, 2, 3]))
        array([[ 1.,  0.,  0.],
               [ 0.,  2.,  0.],
               [ 0.,  0.,  3.]])
        >>> b = diag(a)
        array([ 1.,  2.,  3.])
        >>> type(b)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.linalg.diag(a)


def cuda_eye(n, bit=64):
    """ Create GPUArray identity matrix (ones on diagonal) of size (n x n).

    Parameters:
        n (int): Size of identity matrix (n x n).
        bit (int): 32 or 64 for corresponding float precision.

    Returns:
        gpu: Identity matrix (n x n) as GPUArray.

    Examples:
        >>> a = eye(3)
        array([[ 1.,  0.,  0.],
               [ 0.,  1.,  0.],
               [ 0.,  0.,  1.]])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    if bit == 32:
        a = skcuda.linalg.eye(n, dtype=np.float32)
    elif bit == 64:
        a = skcuda.linalg.eye(n, dtype=np.float64)
    return a


def cuda_get(a):
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


def cuda_give(a, bit=64, type='real'):
    """ Give a list or an array to GPU memory.

    Parameters:
        a (array, list): Data to send to the GPU memory.
        bit (int): 32 or 64 for corresponding float precision.
        type (str): 'real' or 'complex'.

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
        >>> a.shape
        (2, 3)
        >>> a.dtype
        dtype('float64')
        >>> a.reshape((1, 6))
        array([[ 1.,  2.,  3.,  4.,  5.,  6.]])
    """
    if type == 'real':
        if bit == 32:
            b = pycuda.gpuarray.to_gpu(np.array(a).astype(np.float32))
        elif bit == 64:
            b = pycuda.gpuarray.to_gpu(np.array(a).astype(np.float64))
    elif type == 'complex':
        if bit == 32:
            raise NotImplementedError
            # b = pycuda.gpuarray.to_gpu(array(a).astype(complex32))
        elif bit == 64:
            b = pycuda.gpuarray.to_gpu(np.array(a).astype(np.complex64))
    return b


def cuda_ones(shape, bit=64):
    """ Create GPUArray of ones directly on GPU memory.

    Parameters:
        shape (tuple): Dimensions of the GPUArray.
        bit (int, str): 32 or 64 for corresponding float precision.

    Returns:
        gpu: GPUArray of ones.

    Examples:
        >>> a = ones((3, 2), bit=64)
        array([[ 1.,  1.],
               [ 1.,  1.],
               [ 1.,  1.]])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    if bit == 32:
        a = skcuda.misc.ones(shape, np.float32)
    if bit == 64:
        a = skcuda.misc.ones(shape, np.float64)
    return a


def cuda_random(shape, bit=64):
    """ Create random values in the range [0, 1] as GPUArray.

    Parameters:
        shape (tuple): Size of the random array.

    Returns:
        gpu: Random floats from 0 to 1 in GPUArray.

    Examples:
        >>> a = random((2, 2), bit=64)
        array([[ 0.80916596,  0.82687163],
               [ 0.03921388,  0.44197764]])
        >>> type(a)
        pycuda.gpuarray.GPUArray

    """
    if bit == 32:
        a = pycuda.curandom.rand(shape, dtype=np.float32)
    if bit == 64:
        a = pycuda.curandom.rand(shape, dtype=np.float64)
    return a


def cuda_real(a):
    return a.real


def cuda_reshape(a, shape):
    return a.reshape(shape)


def cuda_flatten(a):
    return a.ravel()


def cuda_tile(a, shape):
    """ Horizontally and vertically tile a GPUArray.

    Notes:
        May be slow for large tiling shapes as for loops are used.

    Parameters:
        a (gpu): GPUArray to tile.
        shape (tuple): Number of vertical and horizontal tiles.

    Returns:
        gpu: Tiled GPUArray.

    Examples:
        >>> a = tile([[1, 2], [3, 4]], (2, 2))
        array([[ 1.,  2.,  1.,  2.],
               [ 3.,  4.,  3.,  4.],
               [ 1.,  2.,  1.,  2.],
               [ 3.,  4.,  3.,  4.]])
        >>> type(a)
        pycuda.gpuarray.GPUArray

    """
    m = a.shape[0]
    n = a.shape[1]
    b = cuda_zeros((m * shape[0], n))
    for i in range(shape[0]):
        b[i * m:i * m + m, :] = a
    c = cuda_zeros((m * shape[0], n * shape[1]))
    for i in range(shape[1]):
        c[:, i * n:i * n + n] = b
    return c


def cuda_zeros(shape, bit=64):
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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
