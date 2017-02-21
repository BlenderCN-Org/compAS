from compas.exceptions import BRGInputError


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def multiply_matrices(A, B):
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
        BRGGeometryInputError:
        If the shapes of the matrices are not compatible.

        BRGGeometryInputError:
        If the row length of B is inconsistent.

    Examples:
        >>> A = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
        >>> B = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
        >>> dot_matrices(A, B)
        [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]]

    """
    n = len(B)  # number of rows in B
    o = len(B[0])  # number of cols in B
    if not all([len(row) == o for row in B]):
        raise BRGInputError('Row length in matrix B is inconsistent.')
    if not all([len(row) == n for row in A]):
        raise BRGInputError('Matrix shapes are not compatible.')
    B = zip(*B)
    return [[sum(x * y for x, y in zip(row, col)) for col in B] for row in A]


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
        BRGGeometryInputError:
        If not all rows of the matrix have the same length as the vector.

    Examples:
        >>> matrix = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
        >>> vector = [1.0, 2.0, 3.0]
        >>> dot_matrix_vector(matrix, vector)
        [2.0, 4.0, 6.0]

    """
    v = len(vector)
    if not all([len(row) == v for row in matrix]):
        raise BRGInputError('Matrix shape is not compatible with vector length.')
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
