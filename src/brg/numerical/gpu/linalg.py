"""brg.numerical.gpu.linalg : Linear algebra equivalents for GPUArrays."""

from numpy import float64
from numpy import ceil

from brg.numerical.gpu.math import sqrt
from brg.numerical.gpu.math import sum

try:
    import pycuda
    import pycuda.autoinit
except ImportError as e:
    pass

try:
    import skcuda
    import skcuda.linalg
except ImportError as e:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 17, 2016'


def conj(a):
    """ Complex conjugate of GPUArray elements.

    Parameters:
        a (gpu): Complex GPUArray.

    Returns:
        gpu: The complex conjugate of the GPUArray.

    Examples:
        a = conj(give([1 + 2j, 3 - 4j], type='complex'))
        array([ 1.-2.j,  3.+4.j], dtype=complex64)
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.linalg.conj(a)


try:
    kernel_code_template = """
    __global__ void cross_product(float *a, float *b, float *c)
    {
        int i = threadIdx.x + blockDim.x * blockIdx.x;
        int n = 3;
        float A1 = a[i * n + 0];
        float A2 = a[i * n + 1];
        float A3 = a[i * n + 2];
        float B1 = b[i * n + 0];
        float B2 = b[i * n + 1];
        float B3 = b[i * n + 2];
        c[i * n + 0] = A2 * B3 - A3 * B2;
        c[i * n + 1] = A3 * B1 - A1 * B3;
        c[i * n + 2] = A1 * B2 - A2 * B1;
    }
    """
    kernel_code = kernel_code_template % {'m': 3}
    mod = pycuda.compiler.SourceModule(kernel_code)
    cross_product = mod.get_function("cross_product")
except NameError as e:
    pass


def cross(a, b, bsize):
    """ Cross-product of two GPUArrays (row by row).

    Parameters:
        a (gpu): GPUArray 1 of vectors (m x 3).
        b (gpu): GPUArray 2 of vectors (m x 3).
        bsize (int): < Blocksize divided by 3.

    Returns:
        gpu: Returns the m vectors from a x b
    """
    m = a.shape[0]
    c = pycuda.gpuarray.empty((m, 3), float64)
    grid = (int(ceil(m/bsize)), 1)
    cross_product(a, b, c, block=(bsize, 3, 1), grid=grid)
    return c


def det(a):
    """ GPUArray square matrix determinant.

    Parameters:
        a (gpu): GPUArray matrix of size (n x n).

    Returns:
        Determinant of the square matrix.

    Examples:
        >>> det(give([[5, -2, 1], [0, 3, -1], [2, 0, 7]]))
        103
    """
    return skcuda.linalg.det(a)


def dot(a, b):
    """ Matrix multiplication of two GPUArrays.

    Parameters:
        a (gpu): GPUArray matrix 1 (m x n).
        b (gpu): GPUArray matrix 2 (n x o).

    Returns:
        gpu: [c] = [a][b] of size (m x o)

    Examples:
        >>> a = give([[0, 1], [2, 3]])
        >>> b = give([[0, 1], [1, 0]])
        >>> c = dot(a, b)
        array([[ 1.,  0.],
               [ 3.,  2.]])
        >>> type(c)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.linalg.dot(a, b)


def eig(a):
    """ Matrix Eigenvectors and Eigenvalues of GPUArray.

    Note:
        Input GPUArray is a square matrix, either real or complex.

    Parameters:
        a (gpu): GPUArray of a square matrix (m x m).

    Returns:
        gpu: Normalised Eigenvectors (right)
        gpu: Eigenvalues.

    """
    vr, w = skcuda.linalg.eig(a)
    return vr, w


def hermitian(a):
    """ Hermitian conjugate transpose of GPUArray.

    Parameters:
        a (gpu): Complex GPUArray.

    Returns:
        gpu: The complex conjugate transpose of the GPUArray.

    Examples:
        >>> a = hermitian(give([[1 + 2j, 3 - 4j],[0 - 5j, 6 - 1j]], type='complex'))
        array([[ 1.-2.j,  0.+5.j],
               [ 3.+4.j,  6.+1.j]], dtype=complex64)
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.linalg.hermitian(a)


def inv(a):
    """ Inverse of GPUArray matrix.

    Parameters:
        a (gpu): Input square GPUArray.

    Returns:
        gpu: Matrix inverse as GPUArray.

    Examples:
        >>> a = inv(give([[4, 7], [2, 6]]))
        array([[ 0.6, -0.7],
               [-0.2,  0.4]])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.linalg.inv(a)


def normrow(a):
    """ GPUArray of vectors norm.2 (row by row).

    Parameters:
        a (gpu): GPUArray of vectors (m x n).

    Returns:
        gpu: Vector lengths (m,).

    Examples:
        >>> a = normrow(give([[1, 2], [3, 4]]))
        array([ 2.23606798,  5.])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return sqrt(sum(a*a, axis=1))


def pinv(a):
    """ Moore-Penrose pseudo inverse of GPUArray matrix.

    Notes:
        Singular values smaller than 10^-15 are set to zero.

    Parameters:
        a (gpu): Input matrix (m x n).

    Returns:
        gpu: Matrix pseudoinverse inverse.

    Examples:
        >>> a = pinv(give([[1, 3, -1], [2, 0, 3]]))
        array([[ 0.1056338 ,  0.16197183],
               [ 0.27464789,  0.02112676],
               [-0.07042254,  0.22535211]])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.linalg.pinv(a)


def svd(a, jobu='S', jobvt='S'):
    """ GPUArray Singular Value Decomposition.

    Parameters:
        a (gpu): GPUArray (m x n) to decompose.

    Returns:
        gpu: Unitary matrix (m x k).
        gpu: Singular values.
        gpu: vh matrix (k x n).

    """
    return skcuda.linalg.svd(a)


def trace(a):
    """ GPUArray trace, sum along main diagonal.

    Parameters:
        a (gpu): Input GPUArray.

    Returns:
        float: tr(GPUArray).

    Examples:
        >>> a = trace(give([[0, 1], [2, 3]]))
        3.0
        >>> type(a)
        numpy.float64
    """
    return skcuda.linalg.trace(a)


def transpose(a):
    """ Transpose of GPUArray matrix.

    Parameters:
        a (gpu): GPUArray of size (m x n).

    Returns:
        gpu: GPUArray transpose (n x m).

    Examples:
        >>> a = transpose(give([[0, 1], [2, 3]]))
        array([[ 0.,  2.],
               [ 1.,  3.]])
        >>> type(a)
        pycuda.gpuarray.GPUArray
    """
    return skcuda.linalg.transpose(a)
