import numpy as np
from scipy.fftpack import dct, idct

def normalize_array(arr, low = 0, high = 1):
    """
    1. Find the Minimum and Maximum: Calculate the minimum and maximum values in the array.
    2. Apply the Normalization Formula: Subtract the minimum value from each element of the array, and then divide by the range (maximum - minimum) of the array.

    Example:
    Original Array:
        [[10 20]
        [30 40]]

    Normalized Array:
        [[0.   0.25]
        [0.75 1.  ]]
    """
    min_val = np.min(arr)
    max_val = np.max(arr)
    normalized_arr = low + (arr - min_val) * (high - low) / (max_val - min_val)
    return normalized_arr

def compute_gradient(array):
    """
    In image processing, gradients are often used to detect edges within images.
    """
    rows, cols = array.shape
    grad_x = np.zeros_like(array)
    grad_x[:, 0: cols - 1] = np.diff(array, axis=1)

    grad_y = np.zeros_like(array)
    grad_y[0:rows - 1, :] = np.diff(array, axis=0)

    gradient_array = np.concatenate((grad_x[..., np.newaxis], grad_y[..., np.newaxis]), axis=-1)

    return gradient_array

def compute_divergence(array):
    """
    Divergence is a scalar field that measures the magnitude of a vector field's source or sink at a given point.
    """
    m, n, _ = array.shape
    div = np.zeros((m, n))

    T = array[:, :, 0]
    grad_x = np.zeros(shape=(m, n))
    grad_x[:, 1 : n] = T[: , 0 : n - 1]

    div += T - grad_x

    T = array[:, :, 1]
    grad_y = np.zeros(shape=(m, n))
    grad_y[1 : m, :] = T[0 : m - 1, :]
    div += T - grad_y

    return div

def compute_laplacian(array, h = None):
    """
    The Laplacian of an image highlights regions of rapid intensity change and is therefore often used for edge detection.
    """
    dimensions = 2

    grads = compute_gradient(array)

    if h is not None:
        norm = np.linalg.norm(grads, axis=-1)
        mask = (norm < h)[..., np.newaxis].repeat(dimensions, axis=-1)
        grads[mask] = 0

    laplacian = compute_divergence(grads)
    return laplacian

def double_dct(array):
    """
    The Discrete Cosine Transform (DCT) is used in image compression and is the basis for the JPEG image format.
    """
    return dct(dct(array.T, norm='ortho').T, norm='ortho')

def double_idct(array):
    """
    The Inverse Discrete Cosine Transform (IDCT) is used to reconstruct an image from its DCT coefficients.
    """
    return idct(idct(array.T, norm='ortho').T, norm='ortho')