"""brg.numerical.statistics : Numerical statistical methods."""

from numpy import asarray
from scipy.linalg import svd


__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__author__     = ['Tom Van Mele <vanmelet@ethz.ch>']


def principal_component_analysis(data):
    """PCA of a dtat set finds the directions along which the variance of the data
    is largest, i.e. the directions along which the data is most spread out.

    Parameters:
        data (list) :
            A list of `m` observations, measuring `n` variables.
            For example, if the data are points in 2D space, the data parameter
            should contain `m` nested lists of `2` variables, the `x` and `y`
            coordinates.

    Returns:
        list :
            A list of principle directions. The number of principle directions
            is equal to the dimensionality of the problem(?!).
            For example, if the data points are locations in 3D space, three
            principle components will be returned. If the data points are
            locations in 2D space, only two principle components will be returned.

    Note:
        ...

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
    eigenvec = u[:, :nvar]
    # eigenvec = vT[:, :nvar]
    # eigenvalues
    eigenval = s[:nvar]
    # return
    return eigenvec, eigenval


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy import random

    import matplotlib.pyplot as plt

    data = random.rand(100, 2)
    data[:, 0] *= 10.0
    data[:, 1] *= 2.0

    average = (data.sum(axis=0) / data.shape[0]).reshape((-1, data.shape[1]))

    eigenvec, eigenval = principal_component_analysis(data)

    print eigenvec
    print eigenval

    plt.plot(data[:, 0], data[:, 1], 'ko')
    plt.plot(average[:, 0], average[:, 1], 'ro')

    plt.plot([average[:, 0], average[:, 0] + eigenvec[0, 0]],
             [average[:, 1], average[:, 1] + eigenvec[0, 1]], 'g-')

    plt.plot([average[:, 0], average[:, 0] + eigenvec[1, 0]],
             [average[:, 1], average[:, 1] + eigenvec[1, 1]], 'b-')

    ax = plt.gca()
    ax.set_aspect('equal')

    plt.show()
