"""brg.numerical.statistics : Numerical statistical methods."""

from numpy import asarray

from scipy.linalg import svd


__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__author__     = ['Tom Van Mele <vanmelet@ethz.ch>']


def principal_component_analysis(data):
    """PCA of a dataset finds the directions along which the variance of the data
    is largest, i.e. the directions along which the data is most spread out.

    Parameters:
        data (list):
            A list of `m` observations, measuring `n` variables.
            For example, if the data are points in 2D space, the data parameter
            should contain `m` nested lists of `2` variables, the `x` and `y`
            coordinates.

    Returns:
        list:
            A list of principle directions. The number of principle directions
            is equal to the dimensionality of the problem(?!).
            For example, if the data points are locations in 3D space, three
            principle components will be returned. If the data points are
            locations in 2D space, only two principle components will be returned.

    Examples:
        >>> vectors = PCA(data)
        >>> for vector in vectors:
        ...     print vector
    """
    data = asarray(data)
    nobs, nvar = data.shape
    assert nobs >= nvar, "The number of observations should be higher than the number of measured variables."
    # the average of the observations for each of the variables
    # for example, if the data are 2D point coordinates,
    # the average is the average of the x-coordinate across all observations
    # and the average of the y-coordinate across all observations
    average = (data.sum(axis=0) / nobs).reshape((-1, nvar))
    # the spread matrix
    # i.e. the variation of each variable compared to the average of the variable
    # across all observations
    Yt = data - average
    Y = Yt.T
    # covariance matrix of spread
    # note: there is a covariance function in NumPy...
    # the shape of the covariance matrix is nvar x nvar
    # for example, if the data are 2D point coordinates, the shape of C is 2 x 2
    # the diagonal of the covariance matrix contains the variance of each variable
    # the off-diagonal elements of the covariannce matrix contain the covariance
    # of two independent variables
    n = 1. / (nobs - 1)
    C = n * Y.dot(Yt)
    assert C.shape[0] == nvar, "The shape of the covariance matrix is not correct."
    # SVD of covariance matrix
    u, s, vT = svd(C)
    # eigenvectors
    # note: the eigenvectors are normalised
    # note: vT is exactly what it says it will be => the transposed eigenvectors
    vectors = vT[:, :nvar]
    # eigenvalues
    values = s[:nvar]
    # return
    return average, vectors, values


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy import random

    import matplotlib.pyplot as plt

    from brg.numerical.xforms import rotation_matrix

    from brg.utilities.plotters import Axes3
    from brg.utilities.plotters import Cloud3
    from brg.utilities.plotters import Bounds3

    data = random.rand(300, 3)
    data[:, 0] *= 10.0
    data[:, 1] *= 1.0
    data[:, 2] *= 4.0

    a = 3.14159 * 30.0 / 180
    Ry = rotation_matrix(a, [0, 1.0, 0.0])

    a = -3.14159 * 45.0 / 180
    Rz = rotation_matrix(a, [0, 0, 1.0])

    data[:] = data.dot(Ry).dot(Rz)

    average, vectors, values = principal_component_analysis(data)

    axes = plt.figure().add_subplot(111, projection='3d', aspect='equal')

    Bounds3(data).plot(axes)
    Cloud3(data).plot(axes)
    Axes3(average, vectors).plot(axes)

    plt.show()
