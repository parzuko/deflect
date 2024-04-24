import numpy as np
from scipy.fftpack import dct, idct
from scipy.ndimage import laplace


def laplacian(A):
    """
    Computes the Laplacian of a 2D numpy array.

    Args:
        A (np.ndarray): 2D input array.

    Returns:
        np.ndarray: Laplacian of the input array.
    """
    return laplace(A)


def divergence(grad_x, grad_y):
    """
    Computes the divergence of a vector field.

    Args:
        grad_x (np.ndarray): Gradient of the array along x (rows).
        grad_y (np.ndarray): Gradient of the array along y (columns).

    Returns:
        np.ndarray: Divergence of the vector field.
    """
    div_x = np.gradient(grad_x, axis=0)
    div_y = np.gradient(grad_y, axis=1)
    return div_x + div_y


def gradient(A):
    """
    Computes gradients of input numpy array A along both axes.

    Args:
        A (np.ndarray): Input numpy array.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Tuple of numpy arrays denoting gradients along rows and columns.
    """
    grad_x = np.gradient(A, axis=0)
    grad_y = np.gradient(A, axis=1)
    return grad_x, grad_y


def dct2(a):
    """
    Perform a 2-dimensional Discrete Cosine Transform.

    Args:
        a (np.ndarray): 2D input array.

    Returns:
        np.ndarray: 2D DCT of the input array.
    """
    return dct(dct(a.T, norm="ortho").T, norm="ortho")


def idct2(a):
    """
    Perform a 2-dimensional Inverse Discrete Cosine Transform.

    Args:
        a (np.ndarray): 2D input array.

    Returns:
        np.ndarray: 2D inverse DCT of the input array.
    """
    return idct(idct(a.T, norm="ortho").T, norm="ortho")
