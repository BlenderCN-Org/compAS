__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'multiply_matrix_vector',
    'multiply_matrix_matrix',
]


def multiply_matrix_vector(matrix, vector):
    r"""Multiply a matrix with a vector.

    This is a Python version of the following linear algebra procedure:

    .. math::

        \mathbf{A} \cdot \mathbf{x} = \mathbf{b}

    with :math:`\mathbf{A}` a *m* by *n* matrix, :math:`\mathbf{x}` a vector of
    length *n*, and :math:`\mathbf{b}` a vector of length *m*.

    Parameters:
        matrix (list of list): The matrix.
        vector (list): The vector.

    Returns:
        list: The resulting vector

    Raises:
        AssertionError: If not all rows of the matrix have the same length as the vector.

    Examples:
        >>> matrix = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
        >>> vector = [1.0, 2.0, 3.0]
        >>> multiply_matrix_vector(matrix, vector)
        [2.0, 4.0, 6.0]

    """
    v = len(vector)
    assert all([len(row) == v for row in matrix]), 'Matrix shape is not compatible with vector length'
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


def multiply_matrix_matrix(A, B):
    r"""Mutliply a matrix with a matrix.

    This is a pure Python version of the following linear algebra procedure:

    .. math::

        \mathbf{A} \cdot \mathbf{B} = \mathbf{C}

    with :math:`\mathbf{A}` a *m* by *n* matrix, :math:`\mathbf{B}` a *n* by *o*
    matrix, and :math:`\mathbf{C}` a *m* by *o* matrix.

    Parameters:
        A (sequence of sequence of float): The first matrix.
        B (sequence of sequence of float): The second matrix.

    Returns:
        list of list of float: The result matrix.

    Raises:
        AssertionError: If the shapes of the matrices are not compatible.
        AssertionError: If the row length of B is inconsistent.

    Examples:
        >>> A = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
        >>> B = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
        >>> multiply_matrix_matrix(A, B)
        [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]]

    """
    n = len(B)  # number of rows in B
    o = len(B[0])  # number of cols in B
    assert all([len(row) == o for row in B]), 'Row length in matrix B is inconsistent.'
    assert all([len(row) == n for row in A]), 'Matrix shapes are not compatible.'
    B = zip(*B)
    return [[sum(x * y for x, y in zip(row, col)) for col in B] for row in A]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    matrix = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    vector = [1.0, 2.0, 3.0]

    print multiply_matrix_vector(matrix, vector)

    A = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    B = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]

    print multiply_matrix_matrix(A, B)
