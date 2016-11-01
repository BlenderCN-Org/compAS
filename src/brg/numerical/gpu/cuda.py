#def eig(a):
#    """ Matrix Eigenvectors and Eigenvalues of GPUArray.
#
#    Notes:
#        - Input GPUArray is a square matrix, either real or complex.
#
#    Parameters:
#        a (gpu) : GPUArray square matrix.
#
#    Returns:
#        Normalised Eigenvectors (right) and Eigenvalues.
#
#    """
#    vr, w = skcuda.linalg.eig(a)
#    return vr, w
#
#

#def svd(a, jobu='S', jobvt='S'):
#    """ GPUArray Singular Value Decomposition.
#
#    Notes:
#        None
#
#    Parameters:
#        a (gpu) : GPUArray (m x n) to decompose.
#
#    Returns:
#        GPUArrays: unitary matrix (m x k), singular values, vh matrix (k x n).
#
#    """
#    b = skcuda.linalg.svd(a)
#    return b

