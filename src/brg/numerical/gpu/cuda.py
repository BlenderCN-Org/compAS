"""This module gives access to PyCUDA and SciKit-CUDA for GPU computing.

..  Copyright 2016 BLOCK Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        `http://www.apache.org/licenses/LICENSE-2.0`_

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import numpy as np
import pycuda
import pycuda.autoinit
import skcuda
import skcuda.linalg
skcuda.linalg.init()

__author__     = ['Andrew Liew']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'GNU - General Public License'
__version__    = '0.10'
__email__      = 'liew@arch.ethz.ch'
__status__     = 'Development'
__date__       = '15.08.2016'
__contact__    = """ETH Zurich,
Institute for Technology in Architecture,
BLOCK Research Group,
Stefano-Franscini-Platz 5,
HIL H 47,
8093 Zurich, Switzerland
"""


def abs(a):
    """ Absolute value of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with the elements for absolute values.

    Returns:
        b = abs(a)

    """
    b = pycuda.cumath.fabs(a)
    return b


def asin(a):
    """ Trigonometric arcsine of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = arcsin(a)

    """
    b = pycuda.cumath.asin(a)
    return b


def acos(a):
    """ Trigonometric arccosine of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = arccos(a)

    """
    b = pycuda.cumath.acos(a)
    return b


def atan(a):
    """ Trigonometric arctangent of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = arctan(a)

    """
    b = pycuda.cumath.atan(a)
    return b


def ceil(a):
    """ Ceiling of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with the elements to calculate ceiling.

    Returns:
        b = ceil(a)

    """
    b = pycuda.cumath.ceil(a)
    return b


def conj(a):
    """ Complex conjugate of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : Complex GPUArray a.

    Returns:
        The complex conjugate of the GPUArray.

    """
    b = skcuda.linalg.conj(a)
    return b


def cos(a):
    """ Trigonometric cosine of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = cos(a)

    """
    b = pycuda.cumath.cos(a)
    return b


def cosh(a):
    """ Hyperbolic cosine of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = cosh(a)

    """
    b = pycuda.cumath.cosh(a)
    return b


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


def cross(a, b, m, bsize):
    """ Cross-product of two GPUArrays (row by row).

    Notes:
        None

    Parameters:
        a (gpu)     : GPUArray 1.
        b (gpu)     : GPUArray 2.
        m (int)     : Number of rows.
        bsize (int) : < Blocksize divided by 3.

    Returns:
        c = a x b per row.
    """
    c = pycuda.gpuarray.empty((m, 3), np.float32)
    grid = (int(np.ceil(m/bsize)), 1)
    cross_product(a, b, c, block=(bsize, 3, 1), grid=grid)
    return c


def device():
    """ Displays the GPU CUDA device details.

    Notes:
        None

    Parameters:
        None

    Returns:
        None

     """
    pycuda.driver.init()
    dev = pycuda.driver.Device(0)
    print('Device: ' + dev.name())
    print('Compute Capability: %d.%d' % dev.compute_capability())
    print('Total Memory: %s MB' % (dev.total_memory()//(1024000)))
    atts = [(str(att), value) for att, value in dev.get_attributes().items()]
    atts.sort()
    for att, value in atts:
        print('%s: %s' % (att, value))


def det(a):
    """ GPUArray square matrix determinant.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray matrix of size (n x n).

    Returns:
        Determinant of the square matrix.

    """
    b = skcuda.linalg.det(a)
    return b


def diag(a):
    """ Construct or extract GPUArray diagonal.

    Notes:
        - If a is 1D a GPUArray is constructed, if 2D, diagonal is extracted.

    Parameters:
        a (gpu) : GPUArray (1D or 2D).

    Returns:
        GPUArray matrix with inserted diagonal, or vector of diagonal.

    """
    b = skcuda.linalg.diag(a)
    return b


def dot(a, b):
    """ Matrix multiplication of two GPUArrays.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray matrix 1.
        b (gpu) : GPUArray matrix 2.

    Returns:
        [c] = [a][b]

    """
    c = skcuda.linalg.dot(a, b)
    return c


def eig(a):
    """ Matrix Eigenvectors and Eigenvalues of GPUArray.

    Notes:
        - Input GPUArray is a square matrix, either real or complex.

    Parameters:
        a (gpu) : GPUArray square matrix.

    Returns:
        Normalised Eigenvectors (right) and Eigenvalues.

    """
    vr, w = skcuda.linalg.eig(a)
    return vr, w


def eye(n):
    """ Create GPUArray identity matrix (ones on diagonal) of size (n x n).

    Notes:
        None

    Parameters:
        n (int) : Size of matrix (n x n).

    Returns:
        (n x n) identity matrix as GPUArray.

    """
    a = skcuda.linalg.eye(n)
    return a


def exp(a):
    """ Exponential of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with the elements to calculate exponential.

    Returns:
        b = exp(a)

    """
    b = pycuda.cumath.exp(a)
    return b


def floor(a):
    """ Floor of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with the elements to calculate floor.

    Returns:
        b = floor(a)

    """
    b = pycuda.cumath.floor(a)
    return b


def get(a):
    """ Get float or array from GPU memory.

    Notes:
        None

    Parameters:
        a (gpu) : Data on the GPU memory to retrieve.

    Returns:
        Value/array to RAM.

    """
    b = a.get()
    return b


def give(a):
    """ Give float or array to GPU memory.

    Notes:
        - Data are converted to np.array type and of float32 precision.

    Parameters:
        a (array) : Data to send to GPU memory.

    Returns:
        GPUArray of a.

    """
    b = pycuda.gpuarray.to_gpu(np.array(a).astype(np.float32))
    return b


def hermitian(a):
    """ Hermitian conjugate transpose matrix.

    Notes:
        None

    Parameters:
        a (gpu) : The (m x n) GPUArray.

    Returns:
        (n x m) GPUArray conjugate transpose.

    """
    b = skcuda.linalg.hermitian(a)
    return b


def hstack(a, n=3):
    """ Horizontally stack a GPUArray n times.

    Notes:
        - a is currently a vector (m x 1).
        - function will be slow for large n.

    Parameters:
        a (gpu) : GPUArray to stack horizontally.
        n (int) : Number of horizontal tiles.

    Returns:
        Horizontally stacked GPUArray b (m x n).

    """
    b = zeros((a.shape[0], n))
    for i in range(n):
        b[:, i] = a
    return b


def inv(a):
    """ Inverse of GPUArray matrix.

    Notes:
        None

    Parameters:
        a (gpu) : Input square matrix.

    Returns:
        Matrix inverse as GPUArray.

    """
    b = skcuda.linalg.inv(a)
    return b


def log(a):
    """ Natural logarithm of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with the elements to calculate natural logarithm.

    Returns:
        b = log(a)

    """
    b = pycuda.cumath.log(a)
    return b


def log10(a):
    """ Base10 logarithm of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with the elements to calculate base10 logarithm.

    Returns:
        b = log10(a)

    """
    b = pycuda.cumath.log10(a)
    return b


def mean(a, axis):
    """ GPUArray mean in a given axis direction.

    Notes:
        None

    Parameters:
        a    (gpu) : GPUArray to be mean averaged.
        axis (int) : Axis direction to average across.

    Returns:
        Mean averaged GPUArray.

    """
    b = skcuda.misc.mean(a, axis)
    return b


def norm(a):
    """ Matrix of vectors norm.2 (row by row) of GPUArray.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray of vectors (rows).

    Returns:
        Vector of lengths.

    """
    b = sqrt(sum(a*a, axis=1))
    return b


def pinv(a):
    """ Inverse (Moore-Penrose pseudoinverse) of GPUArray matrix.

    Notes:
        Singular values smaller than 10^-15 are set to zero.

    Parameters:
        a (gpu) : Input matrix (m x n).

    Returns:
        Matrix pseudoinverse inverse as GPUArray.

    """
    b = skcuda.linalg.pinv(a)
    return b


def random(shape):
    """ Random values [0, 1] GPUArray.

    Notes:
        None

    Parameters:
        shape (tup) : GPUArray size.

    Returns:
        Random floats from 0 to 1 in GPUArray.

    """
    b = pycuda.curandom.rand(shape, dtype=np.float32)
    return b


def sin(a):
    """ Trigonometric sine of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = sin(a)

    """
    b = pycuda.cumath.sin(a)
    return b


def sinh(a):
    """ Hyperbolic sine of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = sinh(a)

    """
    b = pycuda.cumath.sinh(a)
    return b


def sqrt(a):
    """ Square-root of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with the elements that are to be rooted.

    Returns:
        b = sqrt(a)

    """
    b = pycuda.cumath.sqrt(a)
    return b


def sum(a, axis):
    """ Sum of GPUArray elements in given axis direction.

    Notes:
        None

    Parameters:
        a    (gpu) : GPUArray for which the elements are to be summed.
        axis (int) : Axis direction to sum across.

    Returns:
        GPUArray of result.

    """
    b = skcuda.misc.sum(a, axis=axis)
    return b


def svd(a, jobu='S', jobvt='S'):
    """ GPUArray Singular Value Decomposition.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray (m x n) to decompose.

    Returns:
        GPUArrays: unitary matrix (m x k), singular values, vh matrix (k x n).

    """
    b = skcuda.linalg.svd(a)
    return b


def tan(a):
    """ Trigonometric tangent of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = tan(a)

    """
    b = pycuda.cumath.tan(a)
    return b


def tanh(a):
    """ Hyperbolic tangent of GPUArray elements.

    Notes:
        None

    Parameters:
        a (gpu) : GPUArray with elements to be operated on.

    Returns:
        b = tanh(a)

    """
    b = pycuda.cumath.tanh(a)
    return b


def trace(a):
    """ GPUArray trace, sum along main diagonal.

    Notes:
        None

    Parameters:
        a (gpu) : Input GPUArray.

    Returns:
        Trace of a.

    """
    b = skcuda.linalg.trace(a)
    return b


def transpose(a):
    """ Transpose of GPUArray matrix.

    Notes:
        None

    Parameters:
        a (gpu) : The (m x n) GPUArray.

    Returns:
        (n x m) GPUArray transpose.

    """
    b = skcuda.linalg.transpose(a)
    return b


def trapz(x, dx):
    """ 1D trapezoidal integration.

    Notes:
        None

    Parameters:
        dx (float) : Fixed spacing of x data.
        x  (gpu)   : GPUArray with data points in x to integrate.

    Returns:
        Definite integral (area A) based on trapezoidal rule.

    """
    A = skcuda.integrate.trapz(x, dx=dx)
    return A


def zeros(shape):
    """ Create GPUArray of zeros.

    Notes:
        None

    Parameters:
        shape (tup) : Dimensions of the GPUArray.

    Returns:
        GPUArray of zeros.

    """
    a = pycuda.gpuarray.zeros(shape, dtype='float32')
    return a
